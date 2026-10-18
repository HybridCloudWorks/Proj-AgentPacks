---
name: azure-architecture-handoff-and-adr
description: Produces implementation-ready Azure architecture handoffs, ADRs, topology contracts, acceptance criteria, risks, ownership, and safe next actions.
---

# Azure Architecture Handoff and ADR

Deliver a handoff that an IaC, platform, security, operations, or diagram specialist can execute without guessing. Include `REQ`, `TOPOLOGY`, `CONSTRAINTS`, and `ADR` with stable IDs, owners, assumptions, evidence, dependencies, and unresolved decisions.

`TOPOLOGY` should express tenant, management groups, subscriptions, resource groups, regions/zones, VNets/subnets, routing, identities, services, data stores, trust boundaries, flows, and recovery paths. `CONSTRAINTS` should include regions, tags, names, policy, quotas, SKUs, data, identity, budgets, and approval gates.

Each ADR states context, alternatives, decision, consequences, evidence, rollback/revisit trigger, and implementation owner. Include acceptance criteria for security, reliability, cost, performance, operations, and deployment. Do not claim handoff completion if a required input is unknown.
