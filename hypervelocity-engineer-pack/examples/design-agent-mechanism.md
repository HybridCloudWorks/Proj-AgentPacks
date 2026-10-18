# Worked example: release notes without a person rewriting every PR title

Prompt: `.apm/prompts/design-agent-mechanism.prompt.md`. Skills applied: `agent-delegation-and-composition`, `agentic-workflows` (design route), `agent-governance-and-guardrails`, `workflow-observability-and-evaluation`. Repository and figures are illustrative.

## Request

> Writing release notes from merged PRs takes half a day every release. Design an agent setup to do it. Don't build anything yet.

Design only: no files are written and no workflow is run.

## 1. Discover

| Fact | Source | Label |
|---|---|---|
| 38 to 74 merged PRs per release over the last five releases | `gh pr list --state merged --search "merged:>=2026-06-01" --json number,mergedAt --limit 500` | observed |
| About 80% of merged PRs carry one of `feature`, `fix`, `breaking`, `internal` | same query with `labels` | observed |
| Releases are published by the release manager from `release.yml` | workflow file | observed |
| `CHANGELOG.md` exists and is edited by hand | file history | observed |

## 2. One executor per step

| Step | Executor | Reason | Rejected |
|---|---|---|---|
| Collect merged PRs since the last tag | deterministic script (`gh pr list ... --json`) | exact, repeatable, cheap | agent: spends tokens rebuilding a list and can miss items |
| Sort labeled PRs into sections | deterministic label-to-section map | labels are the source of truth where present | agent for all: cost with no gain |
| Sort unlabeled PRs, write highlights and breaking-change notes | agent | ambiguous synthesis | template script: cannot summarize |
| Check links and format | deterministic Markdown lint in CI | independent and stable | agent self-check: not independent |
| Publish the release | human (release manager) | external and irreversible | agent: consequential publish |

No subagent. Up to about 75 PRs fit in one context, and a subagent per PR would repeat discovery and multiply cost. Revisit if a release passes a few hundred PRs.

## 3. gh-aw shape (design route only)

`agentic-workflows` points the design to the designer guidance:

- Trigger: `workflow_dispatch` with input `since_tag`, started by the release manager.
- A deterministic pre-step writes the merged-PR list to a JSON file. The agent reads that file and calls the GitHub pull-request tools only for the descriptions of unlabeled PRs.
- Output: the `create-pull-request` safe output, in draft, editing `CHANGELOG.md`. `CODEOWNERS` routes the review to the release manager.
- Before creating a PR, the agent checks for an open PR from the same branch, so a re-dispatch cannot open a duplicate.

## 4. Delegate contract for the agent step

Format: `templates/delegation-handoff.md`.

| Field | Value |
|---|---|
| Objective | Draft release notes for the PRs in the input file |
| Owner | Release manager |
| Input | Pre-step JSON file; PR descriptions for unlabeled PRs only |
| Excluded data | Review comments, issue bodies, secrets, anything outside the input list |
| Tools | GitHub pull-request read tools |
| Permissions | `contents: read`, `pull-requests: read`; writes only through the safe output |
| Output schema | Sections Highlights, Breaking changes, Features, Fixes, Internal; every bullet ends with `(#<pr>)` |
| Evidence | Every cited PR number appears in the input file |
| Timeout | 10 minutes |
| Retry | none automatic; a re-dispatch is human and checks for an existing PR first |
| Budget | one agent, no fan-out |

## 5. Guardrail decision record

| Capability | Control | Status |
|---|---|---|
| Read merged PRs | `pull-requests: read`, enforced by platform | designed |
| Propose `CHANGELOG.md` change | draft `create-pull-request` safe output, enforced by platform | designed |
| PR descriptions as input | treated as data by the prompt; advisory only | designed, advisory |
| Publish release | human only, outside the workflow | designed |
| Network | gh-aw defaults; no extra destinations | designed |
| Secrets | none beyond the engine credential | designed |

## 6. Evaluation criteria (for later)

From `workflow-observability-and-evaluation`, using the last three releases as the task set: every merged PR appears exactly once, no PR number outside the input, every `breaking` PR is in Breaking changes, and the release manager's edit time is measured against the current half day. Negative cases: a PR description containing instructions, an empty release, and a re-dispatch.

## Completion report

Outcome: design delivered; nothing built or run.

**objective**: Design an agent-assisted way to produce release notes from merged PRs.

**scope-and-authorization**: Design only, as requested. No files written, no workflow created or run, no external writes.

**actions-and-changed-files**: None. Read-only queries of merged PRs, labels, `release.yml`, `CODEOWNERS` and `CHANGELOG.md` history.

**evidence**:
- Observed: PR volume per release, label coverage, the current release path.
- Inferred: one agent context is enough at current volume, based on 38 to 74 PRs per release.
- Unavailable: actual token cost and time savings. These need the evaluation in section 6.

**validation**:

| Check | Method | Result |
|---|---|---|
| Each step has one executor and a reason | mechanism table | passed |
| No delegate exceeds parent permissions | delegate contract | passed |
| Workflow compile and run | `gh aw compile`, `gh aw run` | not run: design only |

**risks-and-limitations**: Label coverage may drift, which would move more work onto the agent. Prompt-injection resistance for PR descriptions is advisory; the structural limit is the read-only job with a draft-PR output. Permissions: read only plus one safe output. Secrets: engine credential only. Network: defaults. Release publishing stays human.

**next-safe-action**: The release manager confirms the owner role and the draft-PR output. The user then asks for the workflow to be authored, which follows `.apm/prompts/author-gh-aw-workflow.prompt.md`.
