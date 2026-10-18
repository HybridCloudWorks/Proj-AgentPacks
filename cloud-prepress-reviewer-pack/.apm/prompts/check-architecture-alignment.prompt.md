---
description: "Compare a built change with the approved architecture, topology, constraints and ADRs, and identify decisions that need a new ADR"
agent: cloud-prepress-reviewer
---

# Check a built change against the approved architecture

## Inputs

- The exact change: base and head refs or a supplied file list.
- The approved design artifacts that apply: architecture brief, `REQ`, `TOPOLOGY`, `CONSTRAINTS`, ADRs, diagrams, deployment plan and acceptance criteria.
- The decision owner for each affected ADR, where it is recorded.

If no design artifact exists, say so. Do not compare the change with an imagined ideal design.

## Workflow

1. Apply change-scope-and-impact to list which services, boundaries, data flows, identities, regions and environments the change adds, removes or alters.
2. Apply architecture-and-adr-consistency to compare each of those changes with the approved artifacts. Find drift, undocumented services or boundaries, conflicting names or tags, missing dependencies, wrong environment placement, and decisions implemented without an accepted ADR. A change that alters an accepted decision needs a new or superseding ADR before implementation proceeds.
3. Apply documentation-inputs-and-repository-contracts to check that the decision, new inputs and operating notes land in the artifact the repository uses for each.
4. Apply role-authority-and-handoff-review to name who owns each open decision. A missing owner or missing architecture decision is a human blocker.
5. Apply review-report-and-pr-gate to write the report.

Route detailed cloud design questions to the relevant cloud architect. This review decides only whether the implementation is aligned enough to proceed.

## Expected output

A pre-press report whose architecture and ADR status separates three things: proven contradictions with a located file and line, missing design evidence, and decisions that need a new or superseding ADR, each with its owner. When an unresolved decision could remove or reshape the changed component, recommend `BLOCKED_ON_HUMAN_DECISION`; when the design is settled and the code contradicts it, recommend `CHANGES_REQUIRED`.

Follow the `cloud-prepress-reviewer-contract` instruction. Never describe an unexecuted check as passed.
