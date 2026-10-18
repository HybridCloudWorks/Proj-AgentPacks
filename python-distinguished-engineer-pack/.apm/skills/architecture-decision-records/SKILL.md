---
name: architecture-decision-records
description: Record significant Python, API, identity, persistence, cloud and agent architecture choices with alternatives. Use when a change affects durable public contracts, runtime minimums, core tooling, shared coupling, deployment, cost or difficult-to-reverse architecture.
---

# Architecture Decision Records

## Activation and scope

A change affects durable public contracts, runtime minimums, core tooling, shared coupling, deployment, cost or difficult-to-reverse architecture. An ADR draft cannot approve deployment, data loss or permission changes.

## Inputs and dependencies

- Inputs: Problem, constraints, candidate options, affected consumers, evidence and decision owner.
- Dependencies: Existing ADR conventions and adr-template.md in this Skill.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Identify the decision boundary and reversibility. Use an ADR for significant decisions; leave local reversible implementation details in the change report.
2. Compare viable alternatives against correctness, complexity, security/privacy, reliability, performance/cost, team cognitive load, portability, testability, migration and reversibility.
3. Draft with context, decision drivers, selected option, rationale, consequences, ownership, validation and revisit criteria. Distinguish proposed from accepted status.
4. Map the decision to concrete implementation and tests; record rollout, migration and recovery constraints. Supersede accepted records rather than silently rewriting history.

## Output and validation

One decision record per significant decision, with alternatives, evidence, owner/status and implementation validation. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Missing decision owner, unsupported claim, incompatible consumer need or an alternative eliminated without evidence. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `design-python-change.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
