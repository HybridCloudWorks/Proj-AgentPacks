# Design Decisions

## Broad Azure architect, focused Skills

The Agent is broad enough to route full-lifecycle Azure work, but the detailed procedures are split so ordinary service selection does not load migration, MCP, landing-zone, AVM, and operations material at once.

## Frameworks are decision lenses

Azure Well-Architected's five pillars and Cloud Adoption Framework for Azure organize workload quality, adoption, landing zones, governance, trade-offs, readiness, and review. They do not replace workload-specific requirements, current Microsoft documentation, or evidence.

## Architect versus implementer

The pack understands Bicep/ARM, Terraform, AzAPI/AzureRM, AVM, deployment stacks, Azure CLI, what-if, and deployment lifecycles so its designs are implementable. It asks before mutating infrastructure and produces a handoff contract instead of silently applying changes.

## MCP is evidence and controlled action

Official Microsoft Learn and Azure MCP are preferred for current documentation, Azure resource guidance, and read-only evidence. Azure MCP/API and specialized servers are routed only when present, authorized, and needed. The pack does not assume an MCP tool exists or treat tool output as proof beyond the data actually retrieved.

## Cost, resilience, and operations are architecture concerns

Zone/region transfer, Private Link, NAT, egress, managed-service trade-offs, backup/restore, observability, runbooks, and ownership are included in architecture decisions rather than deferred as implementation trivia.

## Visualization is integrated but not duplicated

Architecture diagrams are a first-class output, but the detailed Azure Draw.io generation capability remains in the Azure Expert Designer pack. This pack provides routing, evidence, and handoff integration.
