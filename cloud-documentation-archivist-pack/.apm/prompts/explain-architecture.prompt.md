---
description: "Explain a cloud architecture: rationale, boundaries, data flows and trade-offs, with current, target and proposed state kept apart"
agent: cloud-documentation-archivist
---

# Explain a cloud architecture

## Inputs

- The system boundary and the audience: engineers, operators, reviewers or leadership.
- Sources: infrastructure code, diagrams, service inventory, decision records, runbooks and requirements.
- Whether the page describes current state, target state, a proposal, or more than one of these.
- The audience's classification, which sets how much topology may be shown.

## Workflow

1. Apply explanation-and-architecture-docs. Explain why the system is shaped the way it is, how its components interact, and which constraints drive the design. Cover scope, requirements, quality attributes, alternatives, the chosen approach, consequences, risks and revisit triggers. Name component owners, trust boundaries, data flows, failure domains and operational responsibilities. Add a diagram or table only when it makes a relationship clearer.
2. Label every statement as current, target or proposed, and as implemented, inferred or not verified. A diagram, a proposal or unapplied infrastructure code is not evidence of deployed state.
3. Apply diataxis-content-design to keep procedures out. Link to how-to guides and runbooks instead.
4. Apply adr-and-decision-records to link existing decisions. List any significant decision that has no record as a candidate for a new decision record. Do not write one unless asked.
5. Apply docs-security-privacy-and-redaction. Leave out internal hostnames, account or subscription identifiers, and any topology the audience should not see.
6. Apply documentation-validation-and-link-checking to the page and its diagram source.

## Expected output

An architecture explanation with every statement labelled by state and evidence, a list of candidate decision records, and links to related reference, how-to and runbook pages.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report.
