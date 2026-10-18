---
name: aws-caf-landing-zones-and-governance
description: Design AWS Organizations, OUs, Control Tower landing zones, account vending, guardrails, shared services, logging, and governance boundaries.
---

# AWS CAF, Landing Zones, and Governance

Use this Skill for multi-account strategy, Control Tower, Organizations, OUs, SCPs, centralized logging, delegated administration, account vending, or platform foundations.

## Account model

Separate management, log archive, security/audit, identity, network hub, shared services, and workload accounts when their billing, access, compliance, or blast-radius boundaries differ. Keep Dev, Test, and Prod separate when the risk model requires it; do not treat VPCs as a complete substitute for accounts.

## Guardrails

Design preventive SCPs, detective AWS Config/Security Hub/CloudTrail controls, and corrective automation as distinct controls. An SCP limits maximum permissions; it does not grant IAM permissions. Define break-glass access, delegated administration, exceptions, expiry, ownership, and recovery before enforcing a guardrail.

## Platform foundations

Specify Regions, partitions, IPAM/CIDR strategy, centralized CloudTrail and Config, GuardDuty/Security Hub/Macie, KMS ownership, log retention, backup policy, tagging, budgets, identity federation, network hubs, and account vending workflow. Validate Control Tower feature availability and current landing-zone behavior before implementation.
