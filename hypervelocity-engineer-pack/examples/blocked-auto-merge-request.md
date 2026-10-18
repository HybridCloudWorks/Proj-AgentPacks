# Worked example: blocked request to auto-merge and release

Prompt: `.apm/prompts/review-agent-guardrails.prompt.md`. Skills applied: `agent-governance-and-guardrails`, `workflow-lifecycle-and-release`, `agent-delegation-and-composition`. This example ends **blocked**: the request needs decisions the agent may not make. Repository, teams and settings are illustrative.

## Request

> Our `deps-refresh` agentic workflow opens dependency PRs. Make it merge them itself when CI is green, and cut a patch release every Friday.

The request gives no authorization for permission changes, branch-protection changes, merges or releases, and names no owner for any of them.

## 1. Discover the current state (read-only)

| Fact | Source | Label |
|---|---|---|
| `deps-refresh.md` agent job: `contents: read`, `pull-requests: read` | workflow source and lock | observed |
| Write path: `create-pull-request` safe output only | lock | observed |
| `main` requires 1 approving review and checks `ci/test`, `ci/lint`; administrators included | `gh api repos/example-org/inventory-service/branches/main/protection` | observed |
| No ruleset adds a bypass actor for `main` | `gh api repos/example-org/inventory-service/rules/branches/main` | observed |
| Repository auto-merge disabled | `gh api repos/example-org/inventory-service --jq .allow_auto_merge` returns `false` | observed |
| `release.yml` publishes to the package registry with `REGISTRY_TOKEN` on tag push | `.github/workflows/release.yml` | observed |
| `CODEOWNERS`: `* @example-org/platform-team` | file | observed |

## 2. Decision record for the requested capabilities

Format: `templates/guardrail-decision-record.md`.

| Capability | Needs | Mutation | Approval point | Control | Status |
|---|---|---|---|---|---|
| Agent merges its own PR | `contents: write`, `pull-requests: write`, and a way past the required review | merge to `main` | branch protection | enforced by platform | blocked: needs a self-approval or a protection change |
| Auto-merge when CI is green | repository setting enabled by an admin, then per-PR enablement | merge to `main` | repository admin | enforced by repository policy | not enabled |
| Weekly patch release | tag push, which runs `release.yml` with `REGISTRY_TOKEN` | external publish | release owner | enforced by platform | blocked: production impact, no owner named |
| Current PR path | `create-pull-request` safe output | branch and PR | human review | enforced by platform | keep |

## 3. Findings

1. **High.** Agent-authored dependency changes merged by the same agent remove the only human review on that path. A compromised or broken upstream release would reach `main` and then the registry with no person in the loop.
2. **High.** The Friday release publishes externally. The contract requires asking before releases or production impact, and no release owner is named.
3. **Medium.** Every merge route needs a change to branch protection, rulesets or repository settings. These are shared systems owned by `@example-org/platform-team`.
4. **Low.** `agent-delegation-and-composition` notes that version bumps are a stable transform, so a deterministic updater is the better executor for the bump itself. The agent adds value in the risk summary, not in the merge.

## 4. Reviewable alternative (offered, not implemented)

1. Keep `create-pull-request`. Have the agent add a structured risk summary to each PR: semver level, changelog link, known advisories.
2. A human approves each PR. If the platform team enables repository auto-merge, an approving human can turn it on per PR, and GitHub merges once checks pass. The approval stays human; the platform does the merge.
3. Releases stay with the release owner. Optionally, the agent drafts release notes through a safe output for that owner to edit.

## Completion report

Outcome: blocked. Owner decisions are needed before any change. No files changed and nothing was written externally.

**objective**: Assess making `deps-refresh` merge its own pull requests when CI passes and cut a weekly patch release.

**scope-and-authorization**: Treated as a guardrail review. Permission changes, branch-protection or ruleset changes, merges and releases were not authorized and were not attempted. Reads only.

**actions-and-changed-files**: No files changed. Read the workflow source and lock, branch protection, effective rules, repository settings, `release.yml` and `CODEOWNERS`.

**evidence**:
- Observed: current permissions and safe output; the required review and checks on `main`; no bypass actor; auto-merge disabled; the release path and its secret; code owners.
- Inferred: any agent-only merge needs self-approval or a protection change, based on the protection settings above.
- Unavailable: the organization's policy on bot approvals and release cadence. Nothing in the repository states it.

**validation**:

| Check | Method | Result |
|---|---|---|
| Current permissions minimal | lock review | passed |
| Requested merge path within policy | branch protection and rules review | failed: requires a protection change |
| Requested release path authorized | request and repository review | failed: no owner or approval |
| Workflow compile | `gh aw compile deps-refresh` | not run: nothing changed |

**risks-and-limitations**: Doing what was asked would widen the agent from read-only with a pull-request output to write access on `main` plus an external publish using `REGISTRY_TOKEN`. Network and MCP configuration were not changed or assessed beyond the lock. This review is structural; no live run took place.

**next-safe-action**: The user takes three questions to their owners. Platform team: will you enable repository auto-merge for human-approved dependency pull requests? Release owner: who owns the Friday patch release, and is it wanted? Security owner: is a bot approval ever acceptable on `main`? Implementation of the alternative starts only after those answers.
