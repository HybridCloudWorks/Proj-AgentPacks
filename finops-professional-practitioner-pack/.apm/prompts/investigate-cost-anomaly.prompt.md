---
description: "Triage an unexpected spend change or a fired alert, find the drivers and route it to an owner"
argument-hint: "segment or alert, period, what was observed"
agent: finops-professional-practitioner
---

# Investigate a cost anomaly

## Inputs

What moved, where it was seen, the period, and any change context the user has (deployments, purchases, incidents). Daily billing history for the segment and its neighbours.

## Workflow

Apply cost-anomaly-management. Confirm the movement in billing data, rule out data artifacts and one-time purchases, segment to accountability, split usage from rate, check for masking at total level, correlate with change events, classify and quantify the daily exposure. If the pattern looks like misuse, tell the user at once and recommend notifying security. Use finops-data-analyst for the segment queries when helpful.

## Expected output

An anomaly report with observed and expected values, direction, drivers that account for the change, classification, owner, exposure range and recommended action with its approval level, plus a draft owner message and the completion report from the `finops-professional-practitioner-contract` instruction. Sending messages or acting on resources is Level 2.
