---
description: "Find and plan Google Cloud cost and sustainability improvements"
agent: google-cloud-architect
---

# Optimize Google Cloud cost and sustainability

## Inputs

The scope (billing account, folder or projects), billing export or cost report data the user can supply, workload criticality, utilization data, commitments already held and the savings goal. Ask before querying billing export tables, because queries are billable.

## Workflow

Apply gcp-cost-sustainability. Establish cost attribution, find the largest drivers, evaluate rightsizing, autoscaling, pricing models, storage lifecycle and region choices, and weigh each against reliability and performance requirements. Use gcp-estate-discovery for read-only utilization evidence. Do not purchase commitments, delete resources or change budgets.

## Expected output

Cost-driver breakdown with data sources, a ranked recommendation list with estimated savings, confidence and risk, carbon-footprint considerations, governance actions (labels, budgets, alerts) and a measurement plan. Apply the `google-cloud-architect-contract` instruction.
