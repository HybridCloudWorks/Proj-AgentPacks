# Plan and task templates

## Spec parsing checklist

- Functional requirements: user capabilities, system behaviors, data handled, integrations.
- Non-functional requirements: performance, security, privacy, accessibility, availability, compliance.
- Acceptance criteria: explicit ones, plus criteria implied by requirements. Rewrite vague ones ("fast", "easy") as measurable checks, and label the rewrite as proposed.
- Constraints: technical, business, timeline.
- Scope: in, out, deferred.
- Dependencies: other teams, services, data, decisions.
- Risks and the spec's own mitigations.
- Open questions and conflicts, each with its impact.

Clarification item format: requirement reference, current wording, question, impact on tasks, working assumption (if any), owner to ask.

## Implementation plan outline

Title: "Implementation plan - <feature>".

1. Overview and a link to the spec.
2. Requirements summary with references.
3. Approach.
4. Phases: for each, the goal, its tasks as a checklist of links, and the exit criteria.
5. Dependencies.
6. Risks and mitigations.
7. Milestones and target dates, marked as proposed until the team agrees.
8. Success criteria.
9. Status overview: phase states and task counts by status, with the date of the last update.
10. Change log.

## Task page outline

Title: an action verb and the specific outcome, for example "Implement password reset email" or "Test checkout with expired cards".

1. Context: links to the spec and the plan phase.
2. Objective: what this task delivers.
3. Requirements covered, by reference.
4. Acceptance criteria as a checklist of testable statements.
5. Approach notes and components affected.
6. Dependencies: blocked by, blocks.
7. Estimate, marked as proposed.
8. Progress: dated notes added during the work.

## Sizing and naming

- Target half a day to two days per task. Split anything larger; merge anything smaller than an hour or two into a neighbour.
- Early phases can carry larger setup tasks; late phases should be small and precise.
- Prefix by kind when the team does: Setup, Implement, Integrate, Test, Document, Fix, Refactor.

## Priority scale

Map the spec's language to the team's scale: must have or critical to the highest priority, should have to high, could have to medium, won't have now to deferred. Security and data-integrity requirements are never deferred silently.

## Sequencing

Order along the critical path (data model, interfaces, core logic, integration, testing, release), run independent tracks in parallel, and record each dependency as a relation when the database supports it.

## Progress note

"Progress - <YYYY-MM-DD>": completed, in progress, next, blockers (with who or what is needed), decisions made.

## Milestone summary

"Phase <n> complete - <YYYY-MM-DD>": what was delivered with links, tasks closed, metrics if measured, what changed in scope or timeline and why, next phase.

## Spec-change log entry

Date, what changed in the spec, affected requirements, tasks added, changed or removed (with links), timeline impact, who approved.
