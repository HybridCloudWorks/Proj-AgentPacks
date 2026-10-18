---
description: "Analyze cloud spend for a period and write an audience-ready narrative with top movers and labelled figures"
argument-hint: "period, billing scope, audience (finance, engineering or leadership)"
agent: finops-professional-practitioner
---

# Analyze cloud spend

## Inputs

The period, the billing scope, the audience and the decision the analysis supports. Locate the billing data the user pointed to and read its metadata before asking for anything; ask only for scope that changes the answer.

## Workflow

Apply focus-billing-data-analysis. Choose the cost column for the audience's question, check data health (corrections, purchases, allocation coverage, freshness), compare day-normalized periods, separate one-time charges, find the top movers and their drivers, and reconcile BilledCost to the invoice when one is available. Delegate large exploratory query work to finops-data-analyst when it helps.

## Expected output

A narrative led by the changes and their drivers, a top-movers table, every figure labelled with cost column, filters, period and currency, the data-health summary, the reconciliation result, owners for any follow-up, and the completion report from the `finops-professional-practitioner-contract` instruction. Distributing the narrative is a Level 2 action.
