---
name: aws-architecture-handoff-and-adr
description: Produce implementation-ready AWS architecture handoffs with REQ, TOPOLOGY, CONSTRAINTS, ADRs, risks, verification criteria, and downstream ownership.
---

# AWS Architecture Handoff and ADR

Use this Skill when an architecture must be handed to Terraform, CloudFormation, CDK, platform, security, migration, operations, or FinOps engineers.

## Required artifacts

- `REQ`: sanitized business, functional, non-functional, compliance, scale, cost, and lifecycle requirements;
- `TOPOLOGY`: structured accounts, OUs, Regions, AZs, VPCs, subnets, routes, identities, services, dependencies, data flows, and failure domains;
- `CONSTRAINTS`: Regions/partitions, quotas, naming, tags, versions, encryption, network, IAM, budget, recovery, policy, and operational guardrails;
- `ADR`: decision, context, alternatives, selected option, consequences, evidence, assumptions, and revisit trigger.

Include implementation implications, test/verification criteria, telemetry, rollback, ownership, open questions, and a clear "not proven" section. Keep topology facts separate from recommendations and do not include secrets.

## Handoff quality

The downstream engineer should be able to identify what to build, where, under which identity, how to validate it, what can replace data, what can fail, how to roll back, and who approves the next step. A diagram alone is not a handoff.
