---
name: aws-architecture-foundations
description: Discover AWS workload requirements and turn them into explicit architecture scope, constraints, assumptions, topology, and decision inputs.
---

# AWS Architecture Foundations

Use this Skill at the start of AWS architecture work or whenever requirements, current state, ownership, or constraints are unclear.

## Discovery contract

Capture business outcome, users, workload type, critical journeys, data classification, compliance, regions, accounts, availability target, RTO/RPO, latency, throughput, growth, budget, ownership, skills, operations model, and migration constraints. Separate must-have requirements from preferences.

Identify whether the work is greenfield, migration, modernization, expansion, incident recovery, optimization, or architecture review. Inventory existing AWS accounts, Regions, IaC, shared services, dependencies, and evidence before proposing a replacement.

## Architecture principles

- Prefer the simplest managed-service architecture that satisfies explicit requirements.
- Reduce blast radius with account, Region, AZ, VPC, workload, and data boundaries that match the risk model.
- Make shared responsibility explicit; AWS service selection does not transfer application, identity, data, or configuration responsibility to AWS.
- Do not design production on one AZ, public data stores, static human credentials, or unbounded capacity without a documented exception.
- Validate service limits, regional availability, pricing, and feature maturity before committing to a design.

Route detailed work to the framework, network, security, workload, resilience, deployment, operations, cost, evidence, and handoff Skills as needed.
