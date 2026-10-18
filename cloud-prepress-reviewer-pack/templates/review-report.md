<!--
Pre-press review report: the completion report that review-report-and-pr-gate produces.

How to use
- Save the filled report as REVIEW.md in the handoff folder the user names, outside the source
  tree unless told otherwise. Then run the post-review helper on it (review-hooks-and-automation).
- The twelve section headings below map one-to-one, in order, to the contract's required sections:
  scope_and_inputs, changed_paths_and_methods, evidence_ledger, findings, skipped_checks_and_limits,
  architecture_and_adr_status, security_iac_policy_and_identity_status, tests_build_and_preview_status,
  operations_rollback_cost_and_inputs, unresolved_risks_and_human_blockers, recommendation, engineer_handoff.
  Keep each heading starting with its first word; the post-review validator looks for
  Scope, Evidence, Findings, Recommendation and Engineer Handoff.
- Recommendation: write exactly one of READY_FOR_PR, READY_FOR_DEPLOYMENT_REVIEW, CHANGES_REQUIRED,
  BLOCKED_ON_HUMAN_DECISION, NOT_VERIFIED, and do not write any of the others anywhere in the report.
- Finding IDs are F1, F2, ... and stay stable across review rounds. Write each ID once, in its findings
  table. The post-review validator reads a repeated ID as a duplicate, so other sections refer to a
  finding by severity and subject instead of by ID.
- Finding status is one of: confirmed, validation-hypothesis, accepted-risk, human-blocker.
- Evidence labels: observed, inferred, designed, structurally-validated, preview-verified,
  live-read-verified, accepted-risk, not-verified.
- Never write a secret, a real variable value, or a secret-like "name: value" pair. Redact as
  [REDACTED_POSSIBLE_SECRET].
- Delete this comment block before validating.
-->

# Pre-Press Review: <change title>

## Scope and inputs

| Item | Value |
|---|---|
| Repository and refs | <repository>, base `<ref>`, head `<commit>` |
| Change intent | <what the change is meant to do, from the author or ticket> |
| Change class | <application, infrastructure, identity, networking, data, policy, CI/CD, documentation, or mixed> |
| Target environment | <environment, tenant, subscription, region, resource group or management group scope; or "not applicable"> |
| Requirements and design | <acceptance criteria, architecture brief, ADRs supplied; or "none supplied"> |
| Owner | <change owner and resource owner> |
| Authorization boundary | Read-only review. Live read-only queries: <authorized scope, or "not authorized">. No apply, deploy, delete, force-unlock, import, RBAC, policy or secret change, and no pull request publication. |
| Report location | <path to this REVIEW.md> |

## Changed paths and methods

| Path | Change class | Review method |
|---|---|---|
| `<path>` | <class> | <read in full, traced callers, compared with ADR, ran check, read preview> |

Paths inspected outside the diff, and why:

- `<path>`: <dependency edge or contract that made it necessary>

## Evidence ledger

| Evidence | Label | Source, command or capture | Bound to |
|---|---|---|---|
| <what was examined> | <evidence label> | <file, command and exit code, CI run, or retrieved document and date> | <commit, scope, or "not bound"> |

## Findings

<Ranked Critical, then High, Medium, Low. One block per finding. If there are none, write "No findings.">

#### <short subject of the finding>

| id | severity | status | file | line |
|---|---|---|---|---|
| F<n> | <Critical, High, Medium or Low> | <status> | `<path>` | <line> |

- **scenario:** <trigger or reproduction; expected versus actual behavior>
- **impact:** <who or what is affected, and how badly>
- **recommendation:** <concrete fix>
- **verification:** <the check that proves the fix>

## Skipped checks and limits

| Check | Why skipped or limited | Effect on the recommendation |
|---|---|---|
| <check> | <tool missing, not authorized, environment unavailable, out of scope> | <none, or what it prevents the review from concluding> |

## Architecture and ADR status

<Aligned, contradicted, or design evidence missing, stated separately for each applicable ADR or design artifact.>

## Security, IaC, policy and identity status

<Trust boundaries, identity and role changes by principal, role, scope and operation, policy by scope and effect, IaC state and lifecycle.>

Secret handling: <what was searched, what was redacted, and confirmation that no secret value appears in this report>.

## Tests, build and preview status

| Check | Command or source | Result | Label |
|---|---|---|---|
| <tests, lint, build, fmt, validate, what-if, plan> | `<command>` | <exit code and summary, or "not run"> | <evidence label> |

Preview change counts: <create / modify / delete / replace / no-change, captured at commit and scope; or "no preview">.

## Operations, rollback, cost and inputs

- Observability and ownership: <signals, alerts, runbook, owner>
- Rollback boundary: <how to roll back, and the point beyond which rollback becomes restore or forward-fix>
- Cost: <position against any documented ceiling, with the source of each figure>
- New required inputs: <input names and secret references only, never values>

## Unresolved risks and human blockers

| Item | Type | Owner | Needed to clear |
|---|---|---|---|
| <risk or blocker> | <human blocker, accepted risk, or open risk> | <person or role> | <decision or evidence> |

## Recommendation

<exactly one recommendation value>

<One or two sentences on why, and what the recommendation does not authorize.>

## Engineer handoff

- Next actor: <implementer, pull request approver, deployment operator, decision owner>
- Actions, in order: <refer to findings by severity and subject>
- Evidence the next actor receives: <this report, preview capture, test output>
- Re-review trigger: <what change or evidence returns the work to pre-press review>
- Not done by this review: <deploy, merge, publish, live verification, as applicable>
