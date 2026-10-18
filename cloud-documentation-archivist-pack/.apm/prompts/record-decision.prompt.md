---
description: "Record a significant architecture or operating decision as an ADR, or supersede an existing one, with options, consequences and evidence"
agent: cloud-documentation-archivist
---

# Record an architecture decision

## Inputs

- The decision question, and who decides.
- Context: requirements, constraints, incidents, reviews and meeting notes that bear on it.
- The options considered and the evidence for each.
- The repository's decision log: its location, its numbering, and any record this decision would supersede.

## Workflow

1. Apply adr-and-decision-records. Write one significant decision per record. Include the identifier, title, status, date, deciders, context and problem, forces, the options with honest trade-offs, the decision, consequences, risks, follow-ups and links to evidence.
2. Store the record where the repository's convention says. Without a convention, use `docs/decisions/` or `docs/adr/` and continue the existing numbering.
3. Set a new record to Proposed unless the user says the deciders have accepted it. Never change the decision text of an Accepted record. Supersede it with a new record and link the two in both directions. Change the older record's status only when the new decision is accepted.
4. Do not invent versions, prices or capacity figures. When a consequence carries a cost, say so and leave the estimate to the owner.
5. Apply explanation-and-architecture-docs to keep the rationale apart from implementation detail. Link requirements, diagrams, runbooks and plans.
6. Apply documentation-validation-and-link-checking to the new record and every page it links to.

## Expected output

The new or superseding decision record, any link or index entries the decision log needs, and the list of deciders who still have to act.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report. A Proposed record that still needs acceptance is REVIEW_REQUIRED.
