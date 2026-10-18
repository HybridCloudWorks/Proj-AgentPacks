---
name: azure-caf-landing-zones-and-governance
description: Designs and audits Azure platform and application landing zones, management groups, subscriptions, policy, shared services, naming, tags, and governance inheritance.
---

# Azure CAF Landing Zones and Governance

Treat a landing zone as a set of governance, identity, network, management, security, and workload boundaries. Distinguish the platform landing zone from application landing zones and centralize only capabilities with a clear governance, operational, or economic benefit.

## Placement method

For each component answer: which tenant, management group, subscription, resource group, region, and owner? Explain whether the boundary is for policy, billing, quota, RBAC, lifecycle, data, or blast radius. Keep workload spokes with workloads; place shared hubs and shared DNS/services in platform subscriptions when justified.

## Governance

Design Azure Policy initiatives, allowed regions/SKUs, tags, diagnostic settings, Defender/Sentinel integration, locks, budgets, RBAC/PIM, exemptions, and policy lifecycle. Keep management-group hierarchies reasonably flat and do not create platform components that have no current purpose.

Never rename live globally unique resources to chase convention. Record exceptions for storage, Key Vault, Cosmos DB, web apps, reserved subnet names, and private DNS zones. Require subscription vending, ownership, onboarding, decommissioning, and exception processes.
