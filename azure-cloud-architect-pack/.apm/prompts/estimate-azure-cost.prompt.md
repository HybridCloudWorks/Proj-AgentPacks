---
description: "Build an assumption-based Azure cost model with drivers, budgets, FinOps controls and sustainability trade-offs"
agent: azure-cloud-architect
---

# Estimate and govern Azure cost

## Inputs

The architecture or `TOPOLOGY.json`, and what is known of region, SKU or tier, quantity, utilization, hours, storage growth, request volume, data transfer, log volume, backup retention, licensing (including existing licence benefits), support plan, commitments, and the number of environments. Add any Cost Management export or current bill if the user supplies one.

## Workflow

1. Apply `azure-cost-sustainability-and-finops`: list every assumption, then model compute and storage plus the costs that are easy to miss: shared services and their chargeback, NAT and firewalls, Private Link, cross-zone and cross-region transfer, egress, observability ingestion and retention, replicas, standby DR capacity, and idle environments. Tie each cost line to an owner and a workload. Design budgets, alerts, tags, and the reservation, savings plan and showback approach. Include sustainability trade-offs such as utilization, region choice, right-sizing, autoscaling and retention.
2. Apply `azure-docs-mcp-and-evidence` to prices and tier behaviour: record the source and retrieval date, or say prices were not retrieved.
3. Apply `azure-workload-and-service-selection` to cost-driven alternatives, and `azure-well-architected-and-frameworks` to weigh the cost changes against reliability, security and performance.

Do not purchase reservations or savings plans, change SKUs, or create budgets. Recommend them and name who approves.

## Expected output

- A cost model with an assumption table, ranges, and the largest drivers first. Without retrieved pricing, rank drivers instead of inventing figures.
- Budget, alert and tag design with owners.
- Optimization options, each with its trade-off.
- A completion report. An estimate is never a quote.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
