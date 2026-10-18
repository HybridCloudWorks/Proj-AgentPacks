# Worked example — release readiness for a candidate the evidence does not cover

| | |
|---|---|
| Workflow | `.apm/prompts/release-readiness.prompt.md` |
| Primary agent | `typescript-distinguished-engineer` |
| Specialist | `typescript-security-reviewer` (identity change only) |
| Skills | `typescript-distinguished-engineer-orchestration`, `pull-request-review-and-delivery`, `dependency-supply-chain-and-reproducibility`, `cloud-integration-and-identity`, `performance-reliability-and-operability`, `secure-agent-engineering` |
| Outcome | Review verdict `NOT_VERIFIED` |

> Synthetic walkthrough. The repository, tags, commit ids, paths, commands and output are illustrative. They show the shape of the workflow and are not evidence from a real run; never reuse them as a completion claim.

## Request

"Is `search-api` 2.8.0-rc.1 ready to go to the release reviewers? Don't tag or deploy anything."

The agent may read the repository and GitHub metadata and run local checks. Tagging, workflow dispatch, publishing images and deploying are not authorized.

## Perceive

- `RELEASING.md` sets the gates: CI green on the tagged commit, a 24-hour staging soak, and sign-off from the service owner.
- Tag `v2.8.0-rc.1` points at commit `e4f5a6b`. `git log --oneline v2.7.3..v2.8.0-rc.1` lists 23 commits. Three of them matter for release:
  1. `@example/search-sdk` moves from 4.x to 5.x (internal registry). The lockfile diff shows 31 changed transitive packages.
  2. Object-storage reads switch from a static access key in the `STORAGE_ACCESS_KEY` environment variable to the platform's workload identity, via `storage.auth: workload-identity`. The deployment overlay references a principal named `search-api-reader`.
  3. An additive migration, `0031_add_synonym_index.sql`, uses `create index concurrently`.
- CI: the last release-workflow run is green on `a1b2c3d`. The tagged commit `e4f5a6b` is two commits later: `chore: regenerate lockfile` and `config: enable workload identity in prod overlay`. `gh run list --commit e4f5a6b` returns no runs.
- `docs/runbooks/release.md` describes rollback as "redeploy the previous image".
- PR #377, which made the identity switch, says the static key "will be revoked after rollout".

## Evidence gathered locally on the tagged commit

The agent ran these on `e4f5a6b` in a detached checkout. They stand in only for the checks they cover, on this machine.

| Command | Result |
|---|---|
| `git switch --detach v2.8.0-rc.1` | at `e4f5a6b` |
| `pnpm install --frozen-lockfile --ignore-scripts` | succeeded; lockfile consistent with manifests |
| `pnpm typecheck` | 0 errors |
| `pnpm lint` | 0 errors |
| `pnpm test` | 402 passed |
| `pnpm build` | succeeded |
| `pnpm test:integration` | 57 passed, 9 skipped. The storage-identity suite skips itself when no workload identity is present |
| `pnpm audit --prod` | no high or critical advisories reported by the registry at run time. CI already runs this; it sends package names and versions, not source |
| `pnpm licenses list --prod`, compared with 2.7.3 | no new license types |

`dependency-supply-chain-and-reproducibility`:

- The SDK comes from the internal registry under the pinned version in the lockfile, and none of the new transitive packages adds an install script.
- The SDK's 5.x changelog says the default request timeout is now 30 s. `src/search/client.ts` sets an explicit 2-second timeout, so behaviour is unchanged. Confirmed by reading the code and by the existing timeout unit test.

## Specialist handoff

Handoff to `typescript-security-reviewer`:

- Original goal: decide whether the identity change is safe to send for release review.
- In scope: the diff of PR #377 and the config overlays.
- Out of scope: everything else in the release.
- Verified repository facts: the overlay names `search-api-reader`; the storage-identity tests are skipped locally.
- Assumptions and unresolved decisions: none.
- Files or components affected: `src/storage/client.ts`, `config/overlays/*/storage.yaml`.
- Acceptance criteria: no remaining reads of the static key; the requested permission is least-privilege.
- Risks and prohibited actions: no cloud API calls; do not assume live role state.
- Requested specialist output: findings with severity, evidence, remediation and confidence.
- Evidence gathered so far: the local checks above.

Specialist response:

- Findings or changes: no defects. Code search finds no remaining reads of `STORAGE_ACCESS_KEY`, and moving to workload identity removes a long-lived secret. The overlay comment says the principal needs read access on the index-snapshots bucket only, which is least-privilege as written.
- Evidence and source locations: `src/storage/client.ts:18`; `config/overlays/prod/storage.yaml:7`.
- Tests performed and results: static review only.
- Open risks and confidence limitations: whether `search-api-reader` exists, and what its role binding grants, cannot be seen from the repository (`cloud-integration-and-identity`: do not invent live state).
- Recommended next action: the service owner confirms the binding before the staging soak.

## Findings

Recorded in the format of `templates/pr-review-template.md`.

| Severity | Evidence | Impact | Remediation | Confidence |
|---|---|---|---|---|
| High (evidence gap) | No CI run exists for `e4f5a6b`; the last green run is on `a1b2c3d` | The first `RELEASING.md` gate is unmet. The lockfile regeneration and the prod overlay change were never built by CI | Run the release workflow on `e4f5a6b`. That dispatch also pushes a candidate image to the internal registry, so it needs explicit confirmation | High |
| High (evidence gap) | The 9 storage-identity integration tests were skipped, and the principal's role binding cannot be inspected | If the binding is missing or wrong, every storage read fails after deploy, and nothing run so far would detect it | Owner confirms the binding; the staging soak runs with workload identity enabled | High that it is unverified; no claim about live state |
| Medium | The runbook rolls back to 2.7.3, which authenticates with the static key, and PR #377 plans to revoke that key after rollout | If the key is revoked before 2.8.0 is stable, rollback fails | Keep the key until the soak passes, and write that order into the runbook | Medium: based on PR text, not on the key's actual state |
| Medium | SDK 5.x renamed its timeout error class. `src/search/errors.ts` still maps it to the stable `SEARCH_TIMEOUT` domain error, but the `error_class` metric label changes from `SearchTimeoutError` to `TimeoutError` | Any dashboard or alert outside this repository that matches the old label value could go quiet | Owner checks the alert queries, or the service emits the old label value for one release | Medium: alert definitions are not in the repository |
| Low | `0031_add_synonym_index.sql` is additive and concurrent | None. Rolling back leaves an unused index | None | High |

`performance-reliability-and-operability`: the concurrent index build avoids a table lock, and the explicit SDK timeout keeps the latency budget unchanged. Without the soak, though, there is no load evidence for SDK 5.x.

## Completion report

- Recommendation: NOT_VERIFIED
- Goal: say whether `search-api` 2.8.0-rc.1 is ready for the release reviewers.
- Scope: commit `e4f5a6b` against `v2.7.3`. Evidence review and local checks only; nothing was tagged, dispatched, published or deployed.

### Acceptance criteria

These are the `RELEASING.md` gates plus the user's request.

| Criterion | Status | Evidence or limitation |
|---|---|---|
| CI green on the tagged commit | Not verified | no run exists for `e4f5a6b` |
| Type, lint, unit, build and integration checks on the tagged commit | Verified locally | table above; 9 identity tests skipped |
| Dependency changes reviewed | Verified | lockfile diff, audit, license comparison, SDK timeout check |
| Workload identity works in the target environment | Not verified | no staging evidence; role binding not inspectable |
| Rollback path works | Not verified | depends on the static key still existing |
| Operator alerting unaffected | Not verified | alert definitions are outside the repository |
| 24-hour staging soak | Not verified | not started |
| Service owner sign-off | Not verified | a human gate; the agent did not request it |

These four steps would move the verdict to `READY_FOR_REVIEW`:

1. A release-workflow run on `e4f5a6b` passes. This needs explicit confirmation of: workflow `release.yml`, ref `v2.8.0-rc.1`, effect "build, test and push a candidate image to the internal registry", and recovery "delete the candidate image tag".
2. The owner confirms the `search-api-reader` binding, and the staging soak passes with the identity suite enabled.
3. The runbook states that the static key stays until the soak passes.
4. The owner confirms that the alert queries do not depend on the old label value.

### Delivery evidence

- Files changed: none. The detached checkout is local and disposable.
- Architecture decisions: none made. The identity switch was already decided in PR #377.
- Checks and results: as in the local evidence table; all executed checks passed, and 9 tests were skipped.
- Security review: `typescript-security-reviewer`, static. The identity change is an improvement, with no defects found; the live binding is unverified.
- Observability impact: the metric label value changes for timeouts; alert impact is unverified.
- Operational and cost impact: no new resources. The staging soak costs 24 hours of staging capacity, which the team already budgets for each release.
- Unverified items: CI on the tagged commit; workload identity in any environment; the static key's state; the alert queries; behaviour under load.
- Residual risks: the most likely failure after deploy is storage reads failing on a missing binding, and no check run so far would catch it.
- Rollback: as documented it is "redeploy 2.7.3", which works only while the static key exists. Rollback is therefore not ready until step 3 is done.
