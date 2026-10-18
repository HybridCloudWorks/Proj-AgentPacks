# Worked example — reviewing a "share report" pull request

| | |
|---|---|
| Workflow | `.apm/prompts/review-typescript-pull-request.prompt.md` |
| Primary agent | `typescript-distinguished-engineer` |
| Specialist | `typescript-security-reviewer` |
| Skills | `pull-request-review-and-delivery`, `secure-agent-engineering`, `frontend-react-engineering`, `api-contract-and-integration-engineering`, `dependency-supply-chain-and-reproducibility` |
| Outcome | Review verdict `CHANGES_REQUIRED` |

> Synthetic walkthrough. The repository, pull request, paths, commands and output are illustrative. They show the shape of the workflow and are not evidence from a real run; never reuse them as a completion claim.

## Request

"Review PR #418 in `insights-web` before I look at it tomorrow. Don't comment on GitHub, just tell me."

This makes the review read-only toward GitHub. Posting comments, submitting a review, labelling, approving and merging are all not authorized.

## Perceive

`pull-request-review-and-delivery` starts with the rules, not the diff.

- `CONTRIBUTING.md` requires two human approvals, passing `ci / test` and `ci / e2e`, and a `security-reviewed` label for changes under `src/server/public/`.
- The target branch is `main`; the head is `feat/share-report` at `9c41e2f`. The PR changes 14 files (+612 −38).
- Linked issue: "Owners can share a read-only report link that expires; owners can revoke it."
- `gh pr checks 418` (read-only) shows `ci / test` and `ci / e2e` passed on `9c41e2f`, the same commit reviewed locally. The repository has no dependency-review job.
- Existing PR comments: a Copilot review suggesting a memoized selector, and a teammate's "LGTM, merge when green". Both are advisory input. Neither grants authority to merge, and the second is not one of the two required approvals.

The agent fetched the head into a local branch with `git fetch origin pull/418/head:review/418`. It installed with `pnpm install --frozen-lockfile --ignore-scripts` so that the newly added dependency's `postinstall` script could not run before review.

Files that matter most:

- `src/server/routes/shares.ts` (new): create and revoke share links.
- `src/server/public/share-page.ts` (new): unauthenticated `GET /s/:shareId?k=…` renders the report.
- `src/server/db/migrations/017_shares.sql` (new).
- `src/web/components/ShareDialog.tsx` (new) and `src/web/components/ReportDescription.tsx` (changed).
- `src/web/api/client.ts` (changed): `postJson` now wraps `fetchWithRetry`.
- `package.json` and `pnpm-lock.yaml`: a new markdown rendering dependency.

## Specialist handoff

Handoff to `typescript-security-reviewer`:

- Original goal: independent security review of PR #418.
- In scope: `src/server/**`, `src/web/components/ReportDescription.tsx`, `src/web/api/client.ts`, the dependency change.
- Out of scope: style and naming, other open PRs.
- Verified repository facts: the CONTRIBUTING rules above; CI passed on `9c41e2f`; the public route is unauthenticated by design.
- Assumptions and unresolved decisions: share links are meant to be bearer links (possession grants read access).
- Files or components affected: the list above.
- Acceptance criteria: located findings with severity, evidence, impact, remediation and confidence; each marked static or runtime-confirmed.
- Risks and prohibited actions: no GitHub writes, no requests to shared environments, no running the new dependency's install script.
- Requested specialist output: findings table, checks performed and skipped, residual risk.
- Evidence gathered so far: local typecheck and unit tests pass.

Specialist response:

- Findings or changes: the High and Medium rows below marked "security".
- Evidence and source locations: file and line for each finding. For the log leak, the reviewer started the dev server against the synthetic seed data, requested a share URL, and found the full query string in the request log line.
- Tests performed and results: the local dev-server request described above; no XSS payload was executed.
- Open risks and confidence limitations: the XSS is a static finding. Exploitability depends on renderer options, which were read but not exercised in a browser.
- Recommended next action: fix both High findings before human review; add negative tests.

## Findings

Recorded in the format of `templates/pr-review-template.md`.

| Severity | Evidence | Impact | Remediation | Confidence |
|---|---|---|---|---|
| High (security) | `src/server/public/share-page.ts:41` loads the share by id and checks the secret but never checks `revoked_at` or `expires_at` | Revoked and expired links keep working, so the linked issue's core requirement fails | Add `revoked_at is null and expires_at > now()` to the query; add tests for revoked and expired links | High: read the query; no test covers revocation |
| High (security) | `src/server/http/logger.ts:12` logs `req.url`, and the share secret travels in the `k` query parameter | Every share secret is written to application logs and the log pipeline, readable by anyone with log access | Redact `k` in the request serializer, or exchange the secret through a `POST` and a short-lived cookie | Runtime-confirmed locally (see handoff response) |
| Medium (security) | `src/web/components/ReportDescription.tsx:27` renders markdown with raw HTML enabled into `dangerouslySetInnerHTML`, with no sanitizer. Descriptions are owner-editable and now appear on an unauthenticated page | Stored XSS on the public share page | Disable raw HTML or reuse the existing `sanitizeHtml` helper used by comments; add a test with a script payload | Static; not exploited |
| Medium | `src/web/api/client.ts:58` retries every `POST` up to 3 times on a network error, including share creation | A dropped response creates duplicate shares. The same wrapper serves billing actions, so their retry behaviour changes silently | Retry only idempotent methods, or send an idempotency key the server honours | High: read the wrapper and all 9 callers |
| Medium | `package.json:44` adds a second markdown renderer with a caret range and a `postinstall` script | An unreviewed install script runs on every CI and developer install; two renderers can disagree on output | Reuse the renderer already used by `src/web/comments/render.ts` | High |
| Low | `src/web/components/ShareDialog.tsx:63`: the copy button is icon-only with no accessible name, and closing the dialog does not return focus to the trigger | Screen-reader users cannot identify the control; keyboard users lose their place | Add `aria-label`; return focus on close as `ConfirmDialog` does | High: read the component; the e2e spec uses a CSS selector, so it could not catch this |

Advisory input not adopted: Copilot's memoization suggestion. There is no measured render cost, so it is not a review finding (`frontend-react-engineering`: no optimization without evidence).

The migration was also reviewed. It is additive and indexes `share_id`, which is the only lookup key, so there is no finding.

## Checks

| Check | Result |
|---|---|
| `pnpm install --frozen-lockfile --ignore-scripts` | succeeded; lockfile matches manifests |
| `pnpm typecheck` | 0 errors |
| `pnpm test` | 312 passed |
| `gh pr checks 418` | `ci / test` and `ci / e2e` passed on `9c41e2f` |
| Local dev-server request to a share URL (security reviewer) | request log line contained the share secret |
| `pnpm test:e2e` locally | skipped: CI already ran it on the same commit |
| XSS payload in a browser | skipped: recommended as a regression test instead of an ad-hoc exploit |

## Completion report

- Recommendation: CHANGES_REQUIRED
- Goal: independent review of PR #418 for the user, with no GitHub writes.
- Scope: all 14 changed files at `9c41e2f` against `main`.

### Acceptance criteria

| Criterion | Status | Evidence or limitation |
|---|---|---|
| Every changed file reviewed | Verified | 14 of 14 read, including migration and lockfile |
| Linked requirement "revoked links stop working" | Not met | High finding at `share-page.ts:41` |
| Required checks pass on the reviewed commit | Verified | `gh pr checks 418` at `9c41e2f`; local typecheck and unit tests |
| Security review for `src/server/public/` | Performed, advisory | `typescript-security-reviewer`; the human `security-reviewed` label is still required |
| No GitHub writes | Verified | no comments, reviews, labels or pushes made |

### Delivery evidence

- Files changed: none in the repository. The local branch `review/418` exists only for inspection and can be deleted.
- Architecture decisions: none.
- Checks and results: as in Checks.
- Security review: two High (one runtime-confirmed locally, one by inspection) and one Medium static XSS; dependency install script flagged.
- Observability impact: the PR adds no telemetry; redacting `k` in the request serializer is required.
- Operational and cost impact: one new table; no cost change.
- Unverified items: XSS exploitability; e2e suite not re-run locally; the migration was not applied anywhere.
- Residual risks: if share links were already handed out in a preview environment, their secrets may be in that environment's logs. That is not checked, since it needs access the agent does not have.
- Rollback: not applicable to a review. For the PR itself, gate the public route behind a feature flag before merge so it can be disabled without a revert.
