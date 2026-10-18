# Worked example: diagnosing a workflow that never ran

Prompt: `diagnose-actions-failure.prompt.md`. Skills applied: github-expert-orchestration, github-actions-debugging-and-troubleshooting, github-api-cli-and-mcp-operations, github-actions-workflows-and-security.

The organization, repository, SHAs and run IDs are fictional. Output is abridged.

## Request

> API CI never ran on PR #538 in `example-org/payments-api`, and the PR is stuck waiting for the required `build` check. Why?

This is a diagnosis. Rerunning, dispatching, pushing and settings changes were not authorized.

## 1. Orient

- Expected event: `pull_request` targeting `main`. PR #538 head SHA `2b9d0f4`, from a branch in the same repository (`gh pr view 538 --json headRepositoryOwner` returns `example-org`), so fork approval rules do not apply.
- Changed files: `gh pr diff 538 --repo example-org/payments-api --name-only` lists `apps/api/src/routes/refunds.ts` and `apps/api/test/refunds.test.ts`.

## 2. Classify

Each failure class was checked in order, cheapest first:

| Class | Check | Result |
|---|---|---|
| Not discovered or disabled | `tools/query-workflows.sh --owner example-org --repo payments-api` | `API CI`, path `.github/workflows/api-ci.yml`, state `active` |
| Actions not running at all for this SHA | `gh run list --repo example-org/payments-api --commit 2b9d0f4 --json workflowName,conclusion` | `lint` ran and succeeded, so the event fired and Actions is enabled |
| No run for this workflow | `gh run list --repo example-org/payments-api --workflow api-ci.yml --commit 2b9d0f4` | empty: no run was created |
| Event or path filter mismatch | workflow file at the exact commit (below) | **match found** |

```text
git show 2b9d0f4:.github/workflows/api-ci.yml
on:
  pull_request:
    branches: [main]
    paths:
      - "services/api/**"
      - ".github/workflows/api-ci.yml"
```

Neither changed file matches either pattern, so GitHub never created a run. The history shows why the filter is stale:

```text
git log --oneline -1 -- services/api
a8e77c2 Move services/api to apps/api (#530)
```

## 3. Why the PR is stuck

The ruleset on `main` requires a check named `build`, and only `api-ci.yml` produces it. GitHub documents that when path or branch filtering skips a workflow, its checks stay pending, and a PR that requires them cannot merge. So PR #538 shows `build` as "Expected — Waiting for status to be reported". The same is true of every PR since #530 that touches only `apps/api/`, and of any PR that changes no API files at all.

## 4. Same cause elsewhere

```text
git grep -n "services/api" -- .github/
.github/workflows/api-ci.yml:6:      - "services/api/**"
.github/workflows/deploy-api.yml:7:      - "services/api/**"
.github/workflows/deploy-api.yml:24:        working-directory: services/api
```

`deploy-api.yml` deploys on `push` to `main` with the same stale filter:

```text
gh run list --repo example-org/payments-api --workflow deploy-api.yml --limit 2 --json databaseId,headSha,conclusion,createdAt
[{"databaseId": 11790544987, "headSha": "a8e77c2", "conclusion": "failure", "createdAt": "2026-10-04T09:12:44Z"},
 {"databaseId": 11744120356, "headSha": "5d1c3aa", "conclusion": "success", "createdAt": "2026-10-02T15:40:03Z"}]

gh run view 11790544987 --repo example-org/payments-api --log-failed | tail -n 2
deploy  Install  ##[error]An error occurred trying to start process '/usr/bin/bash' with working directory '/home/runner/work/payments-api/payments-api/services/api'. No such file or directory
```

The rename commit itself matched the filter, because deleted paths count as changes, and that deploy failed on the missing directory. No deploy has run since. Nine commits touching `apps/api/` have merged to `main` and none has been deployed.

## 5. Hypotheses ruled out

- Fork PR waiting for workflow approval: ruled out, because the head repository is `example-org/payments-api`.
- Workflow disabled: ruled out, because the state is `active`.
- Actions policy or billing block: ruled out, because `lint` ran on the same SHA.

## 6. Local remediation

A branch `fix/api-workflow-paths` was prepared locally and not pushed:

```diff
 # api-ci.yml
     paths:
-      - "services/api/**"
+      - "apps/api/**"
       - ".github/workflows/api-ci.yml"
 # deploy-api.yml
     paths:
-      - "services/api/**"
+      - "apps/api/**"
@@
-        working-directory: services/api
+        working-directory: apps/api
```

```text
actionlint .github/workflows/api-ci.yml .github/workflows/deploy-api.yml
(exit 0, no output)
```

Permissions, triggers and action references were left unchanged, so the fix does not widen anything.

Merging the fix will start `deploy-api.yml` and ship nine undeployed commits at once. That is a release decision, so it goes to the release owner rather than being folded into the fix.

## Completion report

### Scope

Why `api-ci.yml` produced no run for PR #538 (`example-org/payments-api`, head `2b9d0f4`), and other workflows with the same cause. Read-only diagnosis plus a local, unpushed fix branch.

### Evidence

- CONFIRMED: `api-ci.yml` at `2b9d0f4` filters on `services/api/**`; PR #538 changes only `apps/api/` files (`git show`, `gh pr diff --name-only`).
- CONFIRMED: no `api-ci.yml` run exists for `2b9d0f4`, while `lint` ran on it (`gh run list --commit`).
- CONFIRMED: `services/api` moved to `apps/api` in `a8e77c2` (#530).
- CONFIRMED: the last `deploy-api.yml` run (11790544987, on `a8e77c2`) failed on the missing `services/api` working directory, and no run has happened since.
- CONFIRMED: `actionlint` reports no errors in the patched files.
- INFERRED: every PR touching only `apps/api/` since #530 has been blocked on `build`, from the filter and the required check.

### Findings

#### ACT-1 · Medium · CI path filter no longer matches the API code

- evidence: `.github/workflows/api-ci.yml:6` (`services/api/**`), against the files changed in PR #538; rename in `a8e77c2`.
- impact: API changes get no CI, and the required `build` check never reports, so affected PRs cannot merge without a bypass.
- remediation: change the filter to `apps/api/**` (prepared on the local branch `fix/api-workflow-paths`).
- verification: after an authorized push, `gh run list --workflow api-ci.yml --commit <new SHA>` shows a run, and PR #538 reports `build`.

#### ACT-2 · High · Production deploys have silently stopped since the directory move

- evidence: `.github/workflows/deploy-api.yml:7` and `:24` still reference `services/api`; run 11790544987 failed on the missing directory; no deploy has run since 2026-10-04 although nine `apps/api/` commits have merged.
- impact: production is nine commits behind `main` with no alert, and the first deploy after the fix will ship all of them together.
- remediation: update the filter and the working directory (prepared locally). The release owner decides whether the catch-up deploy happens at merge or in a planned window.
- verification: after the merge, a `deploy-api.yml` run on the merge SHA succeeds, and the deployment record for `production` shows that SHA.

#### ACT-3 · Medium · A required check comes from a path-filtered workflow

- evidence: the ruleset on `main` requires `build`, which only `api-ci.yml` produces, and `api-ci.yml` has a `paths` filter.
- impact: any PR that changes no API files (docs, other services) is blocked waiting on `build` even after the path filter is corrected.
- remediation: remove the trigger-level `paths` filter and gate the build job on a changed-files step instead. A job skipped by its condition reports success, so the required check always resolves.
- verification: a docs-only test PR shows `build` resolved, and an API PR shows it run.

### Skipped checks

- Live trigger behavior with the new filter: not verified. Proving it needs an authorized push of `fix/api-workflow-paths`.
- Production state outside GitHub (what version is running): not verified. Only the release owner can read it.
- Rerun of run 11790544987: not done. It would deploy from a missing directory and was not authorized.

### Recommendation

READY_FOR_REVIEW

- Rationale: the cause is confirmed and a minimal local fix exists. The stalled-deploy finding carries a release decision, so the fix should not merge until the release owner has made it.
- Owner: `payments-api` maintainers for the fix branch; the release owner for the catch-up deploy.
- Next safe action: the user authorizes `git push origin fix/api-workflow-paths` and opens a PR. The release owner chooses the deploy window before it merges.
