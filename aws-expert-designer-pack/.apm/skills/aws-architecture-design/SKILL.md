---
name: aws-architecture-design
description: Translate AWS requirements and repository evidence into an architecture model, separating observed resources, inferred relationships, design choices, and unresolved questions.
---

# AWS Architecture Design

Use this Skill when the diagram represents AWS architecture, whether the input is prose, CloudFormation, CDK, Terraform, or an application repository.

## Establish the model

Extract or clarify:

- Organization, OU, account, partition, Region, Availability Zone, and edge-location scope;
- VPC, subnet, route table, security group, network ACL, gateway, endpoint, Transit Gateway, Direct Connect, VPN, ingress, and egress;
- compute, containers, serverless, data, messaging, identity, secrets, observability, governance, and deployment services;
- trust, data classification, replication, failover, dependency, traffic direction, and cost-bearing boundaries.

Mark each relationship as `observed`, `inferred`, or `designed`. A resource declared in IaC does not prove that its runtime traffic, DNS, IAM authorization, route, or data relationship is configured correctly.

## Source-derived mode

Inventory files before drawing. For CloudFormation, use resource types, `Ref`, `Fn::GetAtt`, `DependsOn`, parameters, mappings, and nested stacks. For CDK, use construct/resource synthesis when available and label logical-to-physical mapping uncertainty. For Terraform, use AWS resources, modules, providers, references, outputs, and backend context. Preserve unknown values and flag relationships that require deployment, CloudTrail, AWS Config, or runtime evidence.

## Interactive design mode

Ask only questions that change the architecture or visual scope: audience, workload flow, account/Region model, data sensitivity, availability target, traffic pattern, connectivity, identity, scale, and required output. Offer a minimal architecture and optional security, reliability, observability, and governance layers rather than drawing every possible AWS service.

Never use a diagram to hide a design decision. Include a legend or notes for non-obvious routing, replication, IAM, account boundaries, or cross-AZ/cross-Region/egress paths.
