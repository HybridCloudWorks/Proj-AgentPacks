---
name: aws-security-identity-and-compliance
description: Design AWS identity, authorization, network and data protection, detection, incident response, and compliance controls using shared-responsibility boundaries.
---

# AWS Security, Identity, and Compliance

Use this Skill for IAM, IAM Identity Center, federation, cross-account roles, SCPs, permission boundaries, resource policies, KMS, Secrets Manager, WAF, GuardDuty, Security Hub, Config, CloudTrail, Macie, Inspector, compliance, or threat-informed architecture.

## Identity

Prefer federated human access through IAM Identity Center and temporary role credentials. Use workload roles, instance profiles, task roles, IRSA/EKS Pod Identity, and OIDC where appropriate. Review trust policies, session boundaries, external IDs, permission boundaries, resource policies, key policies, and cross-account paths together.

Never design around shared root access, long-lived access keys, broad `AdministratorAccess` as an application dependency, or secrets in source, user data, logs, or plain parameters.

## Protection and detection

Use private network paths, TLS, encryption at rest, Block Public Access, KMS ownership, rotation, backup, and data classification appropriate to the workload. Centralize CloudTrail and security findings where possible. Map controls to threats, evidence, response owner, retention, and recovery; do not confuse a service being enabled with effective coverage.

Compliance claims require the exact control scope, partition/Region, evidence period, and authoritative framework. Static architecture advice is not an audit opinion.
