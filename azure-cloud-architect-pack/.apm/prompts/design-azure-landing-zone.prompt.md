---
description: "Design or audit Azure platform and application landing zones: management groups, subscriptions, policy, identity, network hub and governance"
agent: azure-cloud-architect
---

# Design or audit an Azure landing zone

## Inputs

The organization and ownership model, tenants, and the current management groups, subscriptions, policy assignments and role assignments as a read-only export or listing. Add what is known of compliance obligations, allowed regions, connected sites, identity model, expected subscription demand, budget ownership and operating model. Treat an export as evidence of the estate at the time it was taken.

## Workflow

1. Apply `azure-architecture-foundations` to set scope and boundaries. Keep the observed current state separate from the target design.
2. Apply `azure-caf-landing-zones-and-governance`: separate the platform landing zone from application landing zones, answer the placement questions for every component (tenant, management group, subscription, resource group, region, owner, and why that boundary), and keep the hierarchy reasonably flat. Design policy initiatives, allowed regions and SKUs, tags, naming with its exceptions for globally unique and reserved names, budgets, locks, and the subscription vending, onboarding, decommissioning and exception processes.
3. Apply `azure-security-identity-and-compliance` for RBAC and PIM, break-glass access, privileged roles, managed identities, Defender for Cloud and Sentinel integration, and the control-plane versus data-plane split. Treat compliance as a scoped assessment, not a property of the design.
4. Apply `azure-networking-hybrid-and-edge` for hub-spoke versus Virtual WAN, address ownership, shared and private DNS, ingress, egress and inspection.
5. Apply `azure-cost-sustainability-and-finops` for budgets, tagging and the ownership and showback of shared platform cost.
6. Apply `azure-well-architected-and-frameworks` to name gaps against the CAF Ready, Govern, Secure and Manage concerns.
7. Apply `azure-docs-mcp-and-evidence` to version-sensitive guidance, then `azure-architecture-handoff-and-adr` to write the handoff.

An audit stays read-only. Creating management groups, moving subscriptions, assigning policy or roles, and renaming resources change inherited governance: design and sequence them, and ask before any of them happens. Never rename live globally unique resources to chase a convention.

## Expected output

- Current-state findings with evidence labels (for an audit).
- The target hierarchy and a component placement matrix.
- Policy and RBAC design with staged enforcement, exemptions with owners and expiry, and a migration sequence that lists the inherited assignments each move gains and loses.
- `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`, and a completion report.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
