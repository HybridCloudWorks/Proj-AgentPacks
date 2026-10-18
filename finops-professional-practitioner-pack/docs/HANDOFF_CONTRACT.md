# Handoff contract

The binding text is the `finops-professional-practitioner-contract` instruction; `templates/handoff.md` is a fill-in form for humans.

## Request from the primary

The business question and audience, the decision the result supports, each data source with period, billing scope and FOCUS version or native schema, the cost column and filters, verified facts and assumptions, acceptance criteria, the output wanted, prohibited actions and the approval state. Only the sanitized context the task needs; aggregates and queries rather than raw rows where possible. A specialist inherits no private context.

## Return from a specialist

Results or located findings with evidence (query text, filters, period, row counts, totals), checks with observed results and skips, limitations and data-quality caveats, and the recommended next action.

| Specialist | Must not | Returns in addition |
|---|---|---|
| finops-data-analyst | Edit files, change cloud state, add sources, run unbounded scans | Queries exactly as executed |
| finops-evidence-reviewer | Edit, run commands or queries, use data it was not given | Findings with severity, location, evidence, impact, correction and blocking flag; recomputed arithmetic; named checks for gaps |

## Reconciliation

The primary compares specialist output with the request, the acceptance criteria and the data; reruns or narrows when results disagree; and owns the final figures and completion. A specialist cannot approve its own scope expansion or any Level 2 action. If delegation is unavailable, the primary does the same narrow task with the same skills and reports that the review was not independent.
