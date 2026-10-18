# Worked example: planning an organization-wide ruleset (blocked on a decision)

Prompt: `review-repository-governance.prompt.md`. Skills applied: github-expert-orchestration, github-platform-administration, github-repository-lifecycle-and-governance, github-branch-protection-and-rulesets, github-review-automation-and-hooks.

This example ends blocked: the plan is complete, but applying it needs decisions and authority that only an organization owner has. The organization, repositories and IDs are fictional.

## Request

> Create an organization-wide ruleset for `example-org`: default branches of all repositories need a pull request with two approvals, code-owner review and the `ci` status check. We want it live this week.

## 1. Orient

- Host github.com. The user states the organization is on GitHub Enterprise Cloud, so evaluate mode is available. The plan was not read from the API.
- Actor: a fine-grained token with organization `Administration: read` and repository `Metadata`, `Contents` and `Checks` read on all repositories. It cannot create or edit rulesets, and it cannot read legacy branch protection.
- Outcome: a change plan. Applying it is a privileged organization change and needs the owner's explicit authorization of the exact payload.

## 2. Before-state

```text
gh api orgs/example-org/rulesets --jq '.[] | {id, name, target, enforcement}'
{"id": 87, "name": "org-baseline", "target": "branch", "enforcement": "active"}
{"id": 91, "name": "release-tags", "target": "tag", "enforcement": "disabled"}

gh repo list example-org --no-archived --limit 300 --json name,defaultBranchRef --jq length
112
```

`org-baseline` blocks force pushes and deletion on `~DEFAULT_BRANCH` and has no pull request rule. Nine repositories have their own default-branch rulesets requiring one approval (`gh api "repos/example-org/<repo>/rulesets?includes_parents=false"`).

## 3. Impact analysis

For each of the 112 repositories, the check runs on the default branch's head commit were listed (`gh api repos/example-org/<repo>/commits/<branch>/check-runs --jq '[.check_runs[].name]'`), and CODEOWNERS was looked for in `.github/`, the root and `docs/`. With the repository ruleset reads, that came to 560 GET requests (five per repository), within the 5,000-per-hour budget; `X-RateLimit-Remaining` never dropped below 4,400.

| Group | Repositories | Effect of the requested ruleset |
|---|---|---|
| Report a check named `ci` | 75 | Rule can be met |
| Report checks under other names (`build`, `test`, `CI / build`) | 31 | Every PR blocked: `ci` never reports |
| Report no checks at all (docs, infrastructure) | 6 | Every PR blocked |
| No CODEOWNERS file | 48 (overlaps the groups above) | The code-owner rule has no owners to route review to; how it evaluates there is to be observed in evaluate mode |
| Own ruleset requiring 1 approval | 9 | Layered: the stricter organization rule (2) applies |

The requested ruleset, enforced as asked, would block all merges in 37 of 112 repositories on the first day.

## 4. Draft payload (local file, not sent)

`org-default-branch-ruleset.json`:

```json
{
  "name": "org-default-branch-review",
  "target": "branch",
  "enforcement": "evaluate",
  "conditions": {
    "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] },
    "repository_name": { "include": ["~ALL"], "exclude": [], "protected": false }
  },
  "rules": [
    { "type": "pull_request", "parameters": {
        "required_approving_review_count": 2,
        "require_code_owner_review": true,
        "dismiss_stale_reviews_on_push": true,
        "require_last_push_approval": true,
        "required_review_thread_resolution": false } },
    { "type": "required_status_checks", "parameters": {
        "strict_required_status_checks_policy": false,
        "required_status_checks": [ { "context": "ci" } ] } }
  ],
  "bypass_actors": []
}
```

The payload starts in `evaluate` mode. It has no bypass actors and an empty exclusion list until the owner decides on the 37 repositories. Pinning `ci` to the GitHub Actions app with `integration_id` would stop another app from satisfying the check; that is listed as an open question.

## 5. Mutation preview and guard

```text
python tooling/query_guard.py "gh api --method POST orgs/example-org/rulesets --input org-default-branch-ruleset.json"
{'mutation_detected': True, 'allowed': False, 'patterns': ['\\bgh\\s+api\\b.*--method\\s+(POST|PATCH|PUT|DELETE)']}
BLOCKED: explicit human authorization is required before executing this command.
(exit 2)
```

The guard does what it should. Its override flag is never a substitute for the owner's authorization, and this actor's token could not make the call anyway.

## 6. Rollout, rollback and read-back

The full plan is written with `templates/governance-change-plan.md`. In summary:

1. Create the ruleset in `evaluate` mode. For 14 days, review rule insights (`gh api orgs/example-org/rulesets/rule-suites`) for PRs that would have been blocked.
2. Rename the jobs, or add exclusions, for the 31 repositories with other check names. Add CI or exclusions for the 6 repositories without checks.
3. Switch `enforcement` to `active` once rule insights show no unexpected blocks.

Rollback: `gh api --method PUT orgs/example-org/rulesets/<id>` with `"enforcement": "disabled"`, which an organization owner can run within minutes. Read-back: rerun the section 2 commands and `gh api repos/example-org/<repo>/rules/branches/<branch>` on three pilot repositories.

## Completion report

### Scope

A plan for an organization ruleset on the default branches of `example-org` (112 non-archived repositories). Read-only inventory, impact analysis and a local draft payload. Nothing was applied.

### Evidence

- CONFIRMED: existing organization rulesets 87 (`org-baseline`, active) and 91 (`release-tags`, disabled) (`GET /orgs/example-org/rulesets`).
- CONFIRMED: 112 non-archived repositories; 75 report a `ci` check on the default branch, 31 report other check names, and 6 report none.
- CONFIRMED: 48 repositories have no CODEOWNERS file in any supported location.
- CONFIRMED: `tooling/query_guard.py` blocks the creating call (exit 2).
- INFERRED: the organization is on Enterprise Cloud, so evaluate mode is available (stated by the user, not read from the API).
- HYPOTHESIS: on repositories without CODEOWNERS, the code-owner rule will not block. To be observed in evaluate mode before enforcement.

### Findings

#### GH-1 · High · The ruleset as requested blocks every merge in 37 repositories

- evidence: the impact table in section 3; 31 repositories report other check names and 6 report none.
- impact: on day one, 37 teams cannot merge, and the likely response is ad hoc bypass grants.
- remediation: start in evaluate mode, then fix check names or exclude those repositories before active enforcement.
- verification: rule insights over the evaluation window show blocked PRs only where intended.

#### GH-2 · Medium · "Live this week" leaves no evaluation window

- evidence: the request's timeline, against the 37 blocked repositories and the code-owner behavior still to be observed.
- impact: going straight to active enforcement turns unknowns into outages.
- remediation: run evaluate mode for 14 days, or for a shorter window the owner accepts with the exclusions in place.
- verification: rule-suite results are reviewed and signed off by the owner before `enforcement` becomes `active`.

#### GH-3 · Medium · 48 repositories have no code owners

- evidence: no CODEOWNERS file in `.github/`, the root or `docs/` in 48 repositories.
- impact: the code-owner requirement cannot route review to an owning team there, so the two-approval rule carries all the weight.
- remediation: the owning teams add CODEOWNERS files (with `templates/handoff.md` per team) before enforcement, or the owner accepts the gap explicitly.
- verification: `gh api repos/example-org/<repo>/codeowners/errors` returns no errors for each added file.

#### GH-4 · Low · The organization tag ruleset is disabled

- evidence: ruleset 91 `release-tags` has `enforcement: disabled`.
- impact: outside this request, but release tags in all repositories can be moved or deleted by anyone with write access.
- remediation: a separate governance change.
- verification: `GET /orgs/example-org/rulesets/91` shows `active`.

### Skipped checks

- Legacy branch protection on each default branch: not readable with this token (needs repository admin), so not verified. Layering with legacy rules is unknown.
- Bypass actors on the nine repository rulesets: not verified, for the same reason.
- Team sizes (whether two approvers exist in small repositories): not readable with this token, so not verified.
- The organization plan: taken from the user, not read from the API.

### Recommendation

BLOCKED_ON_HUMAN_DECISION

- Rationale: the plan is ready, but it cannot go ahead without the owner's decisions on the 37 blocked repositories, the evaluation window, bypass actors and `integration_id` pinning, and this actor cannot apply it.
- Owner: an `example-org` organization owner.
- Next safe action: the owner reviews `org-default-branch-ruleset.json` and the governance change plan, records the decisions, and then either authorizes this exact command for an owner-held token or runs it: `gh api --method POST orgs/example-org/rulesets --input org-default-branch-ruleset.json`.
