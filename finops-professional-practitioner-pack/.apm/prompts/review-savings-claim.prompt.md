---
description: "Independently review a savings claim, forecast, allocation or commitment recommendation before it reaches Finance or leadership"
argument-hint: "the claim or document, the evidence behind it"
agent: finops-professional-practitioner
---

# Review a savings claim

## Inputs

The claim or document under review, the figures and queries behind it, the baseline and comparison periods, and the audience it is meant for.

## Workflow

Delegate to finops-evidence-reviewer with the handoff fields from the `finops-professional-practitioner-contract` instruction, supplying the aggregates and queries rather than raw rows. The reviewer applies focus-billing-data-analysis and the skill matching the claim. When the reviewer names a check that needs data, run it yourself or through finops-data-analyst and return the result for a second pass. If delegation is unavailable, perform the same review and state that it was not independent.

## Expected output

Located findings with severity, evidence, impact, correction and blocking flag, recomputed figures where possible, the corrected claim labelled estimated or realized, and the completion report. A claim with blocking findings is reported as CHANGES_REQUIRED.
