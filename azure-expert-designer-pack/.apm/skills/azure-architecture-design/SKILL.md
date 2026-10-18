---
name: azure-architecture-design
description: Translate Azure requirements and repository evidence into an architecture model, separating observed resources, inferred relationships, design choices, and unresolved questions.
---

# Azure Architecture Design

Use this Skill when the diagram represents Azure architecture, whether the input is prose, Bicep, ARM, Terraform, Azure Developer CLI, Kubernetes, CI/CD, or an application repository.

## Establish the model

Extract or clarify:

- subscription, management group, tenant, resource group, region, availability zone, and sovereign-cloud boundaries;
- VNet, subnet, route, NSG, firewall, private endpoint, private DNS, ingress, egress, and hybrid connectivity;
- compute, data, messaging, identity, secrets, observability, governance, and deployment services;
- trust, data classification, replication, failover, dependency, and traffic direction.

Mark each relationship as `observed`, `inferred`, or `designed`. A resource existing in code does not prove that its runtime traffic, DNS, identity, or data relationship is configured correctly.

## Source-derived mode

Inventory files before drawing. Parse declared resources, modules, variables, outputs, dependencies, names, regions, providers, and network references. For Bicep/ARM, use resource IDs and `dependsOn`; for Terraform, use resource addresses, references, modules, providers, and backend context; for Kubernetes, treat cluster objects as workload evidence rather than a complete Azure network model. Preserve unknown values and flag relationships that require deployment or portal evidence.

## Interactive design mode

Ask only questions that change the architecture or visual scope: audience, business flow, data sensitivity, availability target, regions, connectivity, identity, scale, and required output. Offer a minimal architecture and optional security, reliability, observability, and governance layers rather than drawing every possible Azure service.

Never use a diagram to hide a design decision. Include a legend or notes for non-obvious routing, replication, identity, or boundary semantics.
