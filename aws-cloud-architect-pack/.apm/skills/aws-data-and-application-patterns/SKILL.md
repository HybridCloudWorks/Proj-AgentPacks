---
name: aws-data-and-application-patterns
description: Design AWS serverless, event-driven, container, API, data platform, analytics, and AI application patterns with clear consistency and failure semantics.
---

# AWS Data and Application Patterns

Use this Skill for application topology, event-driven systems, APIs, data platforms, analytics, streaming, microservices, containers, or Bedrock/AI-enabled workloads.

## Make semantics explicit

For every asynchronous path, state delivery, ordering, duplication, retry, dead-letter, idempotency, replay, and poison-message behavior. For every data path, state ownership, consistency, retention, encryption, lineage, classification, recovery, and deletion behavior. For every API, state authentication, authorization, throttling, timeout, versioning, observability, and failure contract.

## Architecture patterns

Use API Gateway/ALB/CloudFront/WAF for appropriate edge paths; Lambda, ECS/Fargate, EKS, or EC2 based on workload constraints; SQS/SNS/EventBridge/Kinesis/Step Functions for the actual integration semantics; and S3, Aurora/RDS, DynamoDB, OpenSearch, Redshift, or purpose-built stores based on access patterns.

For AI workloads, include model/provider region, data residency, prompt and retrieval boundaries, guardrails, evaluation, cost, latency, observability, and fallback. Verify current Bedrock/AgentCore service and model availability before committing.
