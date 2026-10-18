---
name: azure-architecture-foundations
description: Establishes Azure architecture scope, requirements, boundaries, assumptions, service vocabulary, and a structured REQ/TOPOLOGY/CONSTRAINTS/ADR handoff before specialist design.
---

# Azure Architecture Foundations

Start here for Azure architecture. Establish the workload and the control-plane hierarchy before selecting services.

## Discovery

Capture business outcomes, workload classification, users, dependencies, data flows, tenancy, regions, availability zones, environment separation, data residency, compliance, SLA/SLO, RTO/RPO, throughput, latency, growth, budget, ownership, delivery model, and current evidence. Mark unknowns rather than filling them with defaults.

## Azure boundaries

Keep these distinct in every topology:

`Microsoft Entra tenant → management group → subscription → resource group → resource → regional/zone and network boundaries`

State which boundary supplies governance, billing, quota, RBAC, lifecycle, data residency, and blast-radius isolation. A resource group is not a substitute for a subscription or tenant boundary.

## Output contract

- `REQ`: sanitized requirements and nonfunctional priorities.
- `TOPOLOGY`: typed JSON/YAML relationships, scopes, regions, networks, services, flows, and dependencies.
- `CONSTRAINTS`: policy, naming, tags, regions, SKUs, quotas, identity, data, budget, and approval gates.
- `ADR`: alternatives, decision, consequences, evidence, and revisit trigger.

Do not call an architecture complete until assumptions, unresolved decisions, evidence status, and the next safe validation step are visible.
