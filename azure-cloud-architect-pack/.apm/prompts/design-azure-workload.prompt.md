---
description: "Design an Azure workload from business requirements and produce the REQ, TOPOLOGY, CONSTRAINTS and ADR handoff"
agent: azure-cloud-architect
---

# Design an Azure workload

## Inputs

The user's business outcomes and workload description, plus whatever is supplied of: users and dependencies, data classification and residency, regions, SLA/SLO, RTO/RPO, throughput, latency, growth, budget, ownership, delivery model, and the existing tenant, landing zone or repository. Read the supplied files before asking. Mark anything still unknown as unknown; do not fill it with defaults.

## Workflow

1. Apply `azure-architecture-foundations`: record the requirements and place the workload on the tenant, management group, subscription, resource group, resource, region/zone and network chain, stating what each boundary supplies (governance, billing, quota, RBAC, lifecycle, residency, blast radius).
2. Apply `azure-workload-and-service-selection` to compare a small set of viable services against runtime, state, scaling, team skills and operational fit. Apply `azure-data-and-application-patterns` to choose data stores and messaging from access patterns, consistency, retention and recovery, and to make synchronous and asynchronous boundaries, idempotency and retries explicit.
3. Add `azure-security-identity-and-compliance`, `azure-networking-hybrid-and-edge`, `azure-resilience-dr-and-migration`, `azure-operations-observability-and-troubleshooting` and `azure-cost-sustainability-and-finops` only for the concerns this workload actually raises.
4. Apply `azure-docs-mcp-and-evidence` to every drift-prone claim: regional availability, zone support, SKU behaviour, limits and pricing. Record what was retrieved; downgrade what was not to an assumption or a validation task.
5. Apply `azure-well-architected-and-frameworks`: for each material choice state the outcome, trade-off, residual risk and owner across the five pillars.
6. Apply `azure-architecture-handoff-and-adr` to write the handoff with stable IDs, owners, acceptance criteria, dependencies and open decisions.

This is a design task. Do not deploy, assign roles or policy, create subscriptions, or query a live tenant unless the user authorizes that scope.

## Expected output

- `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md` in a handoff folder the user names. `ADR.md` holds one section per decision, each Proposed until its decision owner accepts it.
- The service comparison, with the reason each alternative lost.
- A completion report.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
