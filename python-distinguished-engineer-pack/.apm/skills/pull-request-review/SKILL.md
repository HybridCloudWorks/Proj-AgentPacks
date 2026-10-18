---
name: pull-request-review
description: Review Python and agent changes with located evidence, compatibility and operational readiness. Use when pR, branch, staged diff or requested pre-merge review is in scope.
---

# Pull Request Review

## Activation and scope

PR, branch, staged diff or requested pre-merge review is in scope. Review-only requests do not authorize remediation, posting, approval or merge.

## Inputs and dependencies

- Inputs: Exact base/head or diff, repository instructions, acceptance criteria and relevant consumers/tests.
- Dependencies: Read/search tools; test execution by primary when authorized and available.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Resolve review scope and inspect full relevant diff plus callers/tests/configuration; distinguish changed defects from unrelated existing issues.
2. Review requirements, correctness, version/public compatibility, typing/runtime validation, errors/async/resources, dependencies, data/migrations, security/privacy, telemetry, performance/cost and rollback.
3. Use Blocker, High, Medium, Low, Suggestion or Question. Each finding needs location, evidence, failure/impact, recommended change and blocking status; avoid style noise already covered by tools.
4. State actual checks and unverified dependencies. Reconcile security/test/performance/evaluation findings through the primary; local review neither posts comments nor approves/merges a remote PR.

## Output and validation

Prioritized findings, evidence/commands, criterion coverage, residual risks and readiness recommendation. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Unknown diff base, fabricated finding, missing caller context, unrun check represented as passed or unapproved external write. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `review-pull-request.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
