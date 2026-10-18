---
name: aws-workload-and-service-selection
description: Select and compose AWS compute, containers, serverless, storage, databases, messaging, and managed services from workload requirements and operational constraints.
---

# AWS Workload and Service Selection

Use this Skill for service choice, solution architecture, modernization, workload decomposition, or advanced configuration across AWS compute, containers, serverless, storage, databases, and integration services.

## Decision method

Start from workload characteristics: state, traffic, latency, throughput, concurrency, batch versus interactive behavior, durability, consistency, portability, team skills, operations, compliance, and cost. Compare at least two plausible options when the choice is material and state the rejected trade-off.

Prefer managed services when they materially reduce undifferentiated operations. Do not select a service because it is fashionable, because an icon exists, or because a benchmark was not reproduced in the target workload.

## Common boundaries

- Lambda versus ECS/Fargate versus EC2: execution duration, packaging, concurrency, control, networking, workload shape, and operations.
- SQS/SNS/EventBridge/Kinesis/Step Functions: queueing, fan-out, event routing, ordered streams, replay, orchestration, retries, and delivery semantics.
- S3/EBS/EFS/FSx: object, block, shared file, performance, lifecycle, backup, and access patterns.
- Aurora/RDS/DynamoDB/ElastiCache/OpenSearch: relational transactions, key-value access, caching, search, consistency, scaling, and operational model.

Record service limits and version/Region availability as evidence, not assumed constants.
