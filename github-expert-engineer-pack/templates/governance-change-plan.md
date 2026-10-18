# GitHub governance change plan template

The plan that `github-branch-protection-and-rulesets`, `github-platform-administration` and `github-repository-lifecycle-and-governance` require before any ruleset, branch protection, organization policy, access, visibility or default-branch change. Writing the plan authorizes nothing: it ends with the owner's decision.

## Change summary

- Requested by: <role>
- Approval owner: <organization owner, enterprise owner, repository admin>
- Host and plan: <github.com Team | Enterprise Cloud | GHES version>; evaluate mode available: <yes / no>
- Scope: <organization, repository selection rule, ref pattern>
- Change window: <approved window, or "to be agreed">
- Privileged elements: <bypass grants, disabled enforcement, visibility, transfer, archive, default branch, access grants: list each or "none">

## Before-state

| Object | Read-back command | Captured at (UTC) | Summary |
|---|---|---|---|
| Organization rulesets | `gh api orgs/<org>/rulesets` | | |
| Repository rulesets, including inherited | `gh api "repos/<owner>/<repo>/rulesets?includes_parents=true"` | | |
| Effective rules on the ref | `gh api repos/<owner>/<repo>/rules/branches/<branch>` | | |
| Legacy branch protection | `gh api repos/<owner>/<repo>/branches/<branch>/protection` (admin only; a 404 can mean "none" or "no access") | | |

## Policy diff

| Setting | Before | After | Reason |
|---|---|---|---|
| <rule or field> | | | |

## Conflict analysis

Rulesets layer with each other and with legacy branch protection, and the most restrictive applicable setting wins. List every overlap and the effective result.

| Ref or repository | Existing rule | New rule | Effective result | Conflict |
|---|---|---|---|---|

## Impact matrix

| Repository | Required check exists and reports | CODEOWNERS present | Merge queue | Current bypass actors | Effect of the change |
|---|---|---|---|---|---|

Cover forks, reusable workflows, required checks, release automation, package consumers and existing branch rules.

## Required approvals

- <approver role>: <what they approve>

## Rollout

1. <pilot repositories, or evaluate mode with rule insights reviewed for N days>
2. <widen scope>
3. <switch to active enforcement>

## Test plan

- <a PR that should be blocked, and the expected message>
- <a PR that should pass>
- <bypass actor behavior>

## Mutation preview (not executed)

```text
<exact command, for example: gh api --method POST orgs/<org>/rulesets --input <payload>.json>
```

- Payload file: <name>, reviewed by <role>
- Guard: run the command text through `tooling/query_guard.py`. It must report the mutation and stay blocked until the owner authorizes this exact command.

## Rollback

- <exact reversal: disable or delete the ruleset by ID, restore the previous payload>
- <how quickly it can be applied, and by whom>

## Post-change read-back

- <read-only commands from the before-state, rerun; expected differences only>

## Decision

- Decision needed from: <owner>
- Open questions: <exceptions, bypass actors, timing>
