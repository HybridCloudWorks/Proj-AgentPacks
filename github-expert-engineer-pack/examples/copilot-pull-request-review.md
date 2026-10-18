# Worked example: reviewing a Copilot-authored pull request

Prompt: `review-pull-request.prompt.md`. Skills applied: github-expert-orchestration, github-review-automation-and-hooks, github-pull-requests-and-code-review, github-branch-protection-and-rulesets, github-copilot-engineering.

The organization, repository, SHAs, run IDs and teams are fictional. Output is abridged.

## Request

> Copilot opened PR #512 in `example-org/payments-api` to fix webhook retry timeouts, and Copilot code review left comments. Is it safe to merge?

The user asked for a review only. Replies, approvals, pushes and thread resolution were not authorized.

## 1. Orient

- Host github.com; repository `example-org/payments-api`; base `main`; head `copilot/fix-webhook-retry-timeout`.
- Author: the Copilot cloud agent, assigned to issue #498 ("Retries outlive the 30 s delivery deadline") by a maintainer.
- Actor: the user's own `gh` login, which has write access. This task uses it read-only.

## 2. Local inventory

The PR head goes into a separate worktree so the user's working tree is untouched:

```text
git fetch origin pull/512/head:pr-512
git worktree add ../pr-512 pr-512
cd ../pr-512
"$PACK_HOME/hooks/pre-github-review.sh" --out ../pr-512-inventory.json
{"out": "/home/dev/src/pr-512-inventory.json", "github_files": 14, "live_github_read": false}
Pre-review inventory written to ../pr-512-inventory.json. No GitHub API call was made.
```

`$PACK_HOME` is the path the installer gives the pack's helper scripts. The PR's own diff comes from Git:

```text
git diff --stat origin/main...pr-512
 .github/workflows/ci.yml        |  9 ++++++---
 src/dispatcher/retry.test.ts    | 21 +++++++++++++++++++++
 src/dispatcher/retry.ts         | 38 +++++++++++++++++++++++++++++---------
```

No dependency manifest or lockfile changed.

## 3. Pull request state

```text
gh pr view 512 --repo example-org/payments-api \
  --json isDraft,headRefOid,mergeStateStatus,reviewDecision,latestReviews,reviewRequests
```

- `isDraft` false; `headRefOid` `7c41e9a`; `mergeStateStatus` BLOCKED.
- `latestReviews`: one review from `copilot-pull-request-reviewer` in state COMMENTED. Copilot code review only ever leaves comment reviews, so it cannot satisfy the approval requirement. No human has reviewed.
- `reviewRequests`: `@example-org/platform-team`, the CODEOWNERS owner of `/.github/`.

Check runs on the current head SHA:

```text
gh api repos/example-org/payments-api/commits/7c41e9a/check-runs --jq '.check_runs[] | [.name, .conclusion] | @tsv'
lint              success
unit-tests        success
coverage-comment  success
```

Workflows do not run on a Copilot push until someone with write access approves the run. The run that produced these checks is on `7c41e9a`, which is still the head, so the results are current.

## 4. Rules on the base branch

```text
gh api repos/example-org/payments-api/rules/branches/main --jq '.[] | {type, ruleset_id, parameters}'
```

The effective rules come from repository ruleset 4412 (`main-protection`) and organization ruleset 87 (`org-baseline`): a pull request with one approval and code-owner review, required status checks `lint` and `test`, plus blocked force pushes and deletion.

The required check `test` has no matching check run on `7c41e9a`, because the PR renames the job `test` to `unit-tests`. The PR page shows `test` as "Expected — Waiting for status to be reported". The PR can never satisfy the rule, and that turns into pressure to bypass it.

The ruleset detail did not include bypass actors for this actor, so bypass configuration stays unknown.

## 5. Diff review

`.github/workflows/ci.yml` at `7c41e9a`:

```diff
 permissions:
-  contents: read
+  contents: write
+  pull-requests: write
 jobs:
-  test:
+  unit-tests:
     runs-on: ubuntu-latest
@@
+  coverage-comment:
+    needs: unit-tests
+    runs-on: ubuntu-latest
+    steps:
+      - uses: example-tools/coverage-comment@v2
```

The workflow-level grant gives every job a write token on same-repository PR runs, including the job that runs a third-party action referenced by a mutable tag. Only the comment job needs `pull-requests: write`, and no job needs `contents: write`.

`src/dispatcher/retry.ts:41` computes `const delay = baseDelayMs * 2 ** attempt;` with `maxAttempts = 8` and `baseDelayMs = 500`. The scheduled waits add up to 127.5 s, but `src/dispatcher/config.ts:12` sets the delivery deadline to 30 000 ms, so the PR does not fix issue #498. The new tests in `retry.test.ts` cover attempts 1 to 3 with fake timers and never assert against the deadline.

`actionlint .github/workflows/ci.yml` ran on the head version and reported nothing. actionlint checks syntax and expressions, not whether permissions are appropriate.

## 6. Copilot review comments

Copilot left three comments. Each was checked against the code:

| Location | Copilot suggestion | Disposition |
|---|---|---|
| `retry.ts:41` | Cap the computed delay | Confirmed; folded into the deadline finding below |
| `retry.ts:55` | Add jitter to avoid synchronized retries | Advisory: an improvement, not a defect |
| `retry.test.ts:12` | Rename the test for clarity | Advisory: style |

Copilot did not comment on the workflow permission change.

## 7. Post-review check

```text
"$PACK_HOME/hooks/post-github-review.sh" pr-512-review.md
PASS
```

## Completion report

### Scope

PR #512 in `example-org/payments-api` (base `main`, head `7c41e9a`), authored by the Copilot cloud agent. Covered: diff, workflow change, effective base-branch rules, check runs on the head SHA, review state and Copilot review comments. Review-only; nothing was posted.

### Evidence

- CONFIRMED: the diff and `ci.yml` at `7c41e9a` (`git diff`, `git show`).
- CONFIRMED: check runs on `7c41e9a` are `lint`, `unit-tests` and `coverage-comment`, all successful (`GET /repos/example-org/payments-api/commits/7c41e9a/check-runs`).
- CONFIRMED: effective rules on `main` require `lint` and `test`, one approval and code-owner review (`GET /repos/example-org/payments-api/rules/branches/main`).
- CONFIRMED: the only review is a Copilot comment review; platform-team review is pending (`gh pr view --json latestReviews,reviewRequests`).
- CONFIRMED: `actionlint` reports no syntax or expression errors in `ci.yml`.
- INFERRED: the cumulative retry wait (127.5 s) exceeds the 30 s deadline, from `retry.ts:41` and `config.ts:12`; no test exercises it.

### Findings

#### GH-1 · High · Workflow token escalated to write for every CI job

- evidence: the workflow-level `permissions` block of `.github/workflows/ci.yml` at `7c41e9a` replaces `contents: read` with workflow-level `contents: write` and `pull-requests: write`. The new `coverage-comment` job runs `example-tools/coverage-comment@v2`, a mutable tag.
- impact: any step in any CI job, including a compromised third-party action, can push to branches and edit pull requests on same-repository PR runs.
- remediation: restore workflow-level `contents: read`. Grant `pull-requests: write` only on the `coverage-comment` job, and pin the action to a full commit SHA with a version comment.
- verification: actionlint on the revised file. On the next run, the "GITHUB_TOKEN Permissions" block in each job's set-up log shows `Contents: read`, and `PullRequests: write` only for `coverage-comment`.

#### GH-2 · Medium · Required check `test` can never report

- evidence: the effective rules require `test`; the `jobs` block of `ci.yml` renames the job to `unit-tests`; no `test` check run exists on `7c41e9a`.
- impact: the PR stays blocked. Merging it through a bypass would block every later PR the same way, or push someone into an unreviewed ruleset change.
- remediation: keep the job ID `test`, or set `name: test` on the renamed job. If the check really must be renamed, change the ruleset first as a separate, approved governance change.
- verification: the check runs on the new head SHA include `test` with conclusion `success`.

#### GH-3 · Medium · Retry schedule still outlives the delivery deadline

- evidence: `src/dispatcher/retry.ts:41` computes an uncapped exponential delay (500 ms × 2^attempt, 8 attempts, 127.5 s in total). `src/dispatcher/config.ts:12` sets the deadline to 30 000 ms. `retry.test.ts` covers attempts 1 to 3 only. Copilot's comment on `retry.ts:41` raised the same point.
- impact: deliveries keep retrying about 97 s past the deadline, which is the defect issue #498 asked to fix.
- remediation: cap each delay, and stop scheduling when elapsed time plus the next delay would pass the deadline. Add a fake-timer test asserting that no attempt is scheduled after 30 s.
- verification: the new test fails on `7c41e9a` and passes on the fix; CI passes on the new head SHA.

#### Advisory (not findings)

- Copilot, `retry.ts:55`: add jitter. Worth doing, but not a defect.
- Copilot, `retry.test.ts:12`: test naming. Style only.

### Skipped checks

- Bypass actors on rulesets 4412 and 87: not readable with this actor's access, so not verified. An organization owner can read them.
- Local execution of the PR code: not run. Generated code was not executed outside CI without authorization, so test results come only from the CI run on `7c41e9a`.
- Source review of `example-tools/coverage-comment`: not done. Pinning it, as the token-escalation finding recommends, limits but does not remove the trust decision.

### Recommendation

CHANGES_REQUIRED

- Rationale: three confirmed findings. The workflow change widens token privilege, the job rename makes the PR unmergeable without a bypass, and the retry change does not fix the issue it was opened for.
- Owner: the maintainer who assigned the issue to Copilot, plus `@example-org/platform-team` for the workflow change.
- Next safe action: the maintainer shares this report and asks Copilot to revise the PR, or pushes fixes. Re-review from the new head SHA. Nothing was posted to the PR.
