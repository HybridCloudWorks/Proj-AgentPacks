# Completion report

The `azure-cloud-architect-contract` instruction requires this report at the end of every workflow. Keep the twelve section names exactly as written so reports can be compared and checked. Write "none" in a section with nothing to say; never drop it.

Header lines:

- Pack: azure-cloud-architect
- Workflow: the prompt or request this report closes
- Date
- Outcome: one sentence that says what was delivered and what is not verified, blocked or unsafe. Lead with the limitation when there is one.

Evidence labels, used on every material claim:

| Label | Meaning |
|---|---|
| observed | Seen directly in supplied files, command output, or retrieved documentation. A requester's statement is observed as a statement, not as a fact about the estate. |
| inferred | Reasoned from observed evidence but not seen directly. |
| designed | A recommendation or decision in this work, not something that exists. |
| structurally-validated | A local static check ran and passed, such as JSON parsing, file presence, `terraform validate` or Draw.io XML checks. |
| live-verified | Confirmed by an authorized read-only query against the real tenant or subscription, with scope and date. |
| not-verified | Not checked. Every unexecuted check is reported here, never as passed. |

## scope_and_inputs

What was requested, the scope (tenant, subscriptions, regions, repositories), the inputs supplied and their dates, the authority granted, and what was explicitly out of scope.

## business_outcomes_and_requirements

The outcomes and nonfunctional targets the work served, with REQ IDs, and the open decisions that still affect them.

## source_facts_and_evidence

| ID | Claim | Source and retrieval date | Evidence type | Label |
|---|---|---|---|---|

Include sources that could not be retrieved, with the claim downgraded.

## framework_alignment

| Pillar or CAF area | Decision or finding | Trade-off | Residual risk | Owner |
|---|---|---|---|---|

Reliability, Security, Cost Optimization, Operational Excellence and Performance Efficiency, plus the CAF concerns in scope. Prioritized gaps, not a score.

## proposed_architecture

The design or recommendation in a few sentences, pointing to `TOPOLOGY.json` and the ADRs rather than repeating them. For a review or diagnosis, the recommended change.

## assumptions_and_tradeoffs

Each assumption with its impact if wrong, and each significant trade-off with its ADR ID.

## implementation_and_operating_implications

What the implementer, platform team and operators must do: IaC approach, deployment identity, approval gates, what-if or plan evidence, rollback, runbooks, ownership.

## security_resilience_cost_and_sustainability

Identity and exposure, failure domains and recovery (with whether RTO and RPO were measured), the cost position (an estimate is never a quote), and sustainability choices.

## output_files

| File | Purpose | Status and label |
|---|---|---|
| REQ.md | Requirements, acceptance criteria, open decisions | |
| TOPOLOGY.json | Typed topology | |
| CONSTRAINTS.json | Implementation constraints and approval gates | |
| ADR.md | Decisions | |

If any of the four handoff artifacts is missing, say which and why, and do not call the handoff complete.

## live_or_external_checks

| Check | Command, tool or source | Scope | Result | Label |
|---|---|---|---|---|

List checks that were not run as not-verified, with the reason (no authorization, tool unavailable, out of scope).

## unresolved_risks

Risks, blockers and open decisions, each with an owner and what would close it.

## next_safe_action

The single next step that is safe to take, who takes it, and what approval or evidence it needs first.
