# Design Decisions

## Broad architect, focused Skills

The Agent is broad enough to route full-lifecycle AWS work, but the detailed procedures are split so ordinary service selection does not load migration, MCP, landing-zone, and operations material at once.

## Frameworks are decision lenses

AWS Well-Architected's six pillars and AWS CAF's six perspectives organize discovery, trade-offs, readiness, and review. They do not replace workload-specific requirements, current AWS documentation, or evidence.

## Architect versus implementer

The pack understands CloudFormation, CDK, Terraform, AWS CLI, and deployment lifecycles so its designs are implementable. It asks before mutating infrastructure and produces a handoff contract instead of silently applying changes.

## MCP is evidence and controlled action

Official AWS Knowledge MCP is preferred for current documentation and Region/service facts. AWS MCP/API and specialized servers are routed only when present, authorized, and needed. The pack does not assume an MCP tool exists or treat tool output as proof beyond the data actually retrieved.

## Cost, resilience, and operations are architecture concerns

Cross-AZ/cross-Region transfer, NAT, endpoints, managed-service trade-offs, backup/restore, observability, runbooks, and ownership are included in architecture decisions rather than deferred as implementation trivia.

## Visualization is integrated but not duplicated

Architecture diagrams are a first-class output, but the detailed AWS Draw.io generation capability remains in the AWS Expert Designer pack. This pack provides routing, evidence, and handoff integration.
