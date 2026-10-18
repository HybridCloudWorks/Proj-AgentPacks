# Handoff contract

The model-facing version is the specialist handoff section of the `notion-subject-matter-expert-contract` instruction. `templates/handoff.md` is a fill-in form for the same fields.

## Primary to reviewer

The request carries the goal and current task; scope and non-goals; the target pages, databases or teamspaces as URLs or IDs; the fetched content, draft or change list under review; the intended audience (internal, external, public); the data classification; the approval state; the specific questions; and the prohibited actions (no create, edit, comment, move, share or notify). Only the sanitized content the reviewer needs is shared; no private context is inherited.

## Reviewer return

Located findings with severity, location, evidence, impact, recommended change and a blocking flag; the items checked; what could not be seen, such as sharing settings, member lists or automations the connector does not expose; and a recommendation to proceed, proceed with changes, or stop. If the host gave the reviewer write-capable Notion tools anyway, it states that it left them unused.

## Reconciliation

The primary weighs the findings against the user's request and acceptance criteria and the actual workspace facts, makes or proposes the changes, asks the user for any Level 2 decision, and owns completion. A reviewer cannot widen its own assignment or approve a consequential step. When delegation is unavailable, the primary runs the same review with the same skills and records in `independent_review` that it was not independent.
