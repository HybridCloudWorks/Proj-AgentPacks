---
description: "Choose between Google Cloud options and record the decision"
agent: google-cloud-architect
---

# Choose between Google Cloud options and record the decision

## Inputs

The decision to make (for example a compute platform, database, messaging service, load balancer or connectivity option), the requirements and constraints that drive it, the options the user already has in mind and the decision owner. Ask for the owner and the drivers if they are missing.

## Workflow

Apply gcp-architecture-decisions. Confirm the drivers, shortlist viable options from the decision guides, check each option's release status, regional availability and limits in current documentation, compare them against the drivers, and recommend one with explicit trade-offs and reversibility. Record the result as a decision record with status Proposed.

## Expected output

A comparison table, the recommendation with citations, the decision record, open questions and the conditions that would reverse the choice. Apply the `google-cloud-architect-contract` instruction; a decision record never authorizes a deployment, a data change or an access change.
