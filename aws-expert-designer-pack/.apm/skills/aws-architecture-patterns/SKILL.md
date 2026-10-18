---
name: aws-architecture-patterns
description: Model common AWS patterns such as VPC networking, serverless, containers, event-driven systems, data platforms, hybrid connectivity, CI/CD, and multi-Region designs honestly.
---

# AWS Architecture Patterns

Use this Skill when a diagram needs a recognizable AWS architecture pattern or a review of whether a pattern is represented honestly.

## Pattern checks

- VPC/network: distinguish VPC, AZ, public/private subnet, route table, security group, NACL, NAT Gateway, Internet Gateway, endpoints, load balancers, and Transit Gateway. A public subnet is a route-table property, not a label that makes every resource public.
- Serverless: show API Gateway, Lambda, Step Functions, EventBridge, SQS/SNS, DynamoDB, S3, identity, and observability only where they are part of the flow. Distinguish synchronous invocation from asynchronous delivery.
- Containers: separate ECS/EKS control plane, node/task placement, ingress, service discovery, workload identity, network policy, registries, and managed dependencies. Do not treat every Kubernetes object as an AWS resource.
- Data and analytics: show ingestion, streaming/batch processing, storage, catalog/governance, serving, and replication; distinguish data movement from query access.
- CI/CD: show source, build, artifact, deployment identity, environment gates, and target accounts/Regions; do not imply that a pipeline is a runtime dependency.
- Hybrid and multi-Region: label routing, latency, failover authority, replication direction, active/active versus active/passive, and transfer boundaries. Do not imply that Route 53, Global Accelerator, CloudFront, or an edge service automatically replicates or moves database traffic.
- Security and governance: show Organizations/OUs, SCPs, IAM, KMS, CloudTrail, Config, and GuardDuty as governance/security layers when requested, not as generic clutter in every application diagram.

Use current AWS reference architectures and the user's actual source evidence to adapt these patterns. Record deviations and unresolved assumptions.
