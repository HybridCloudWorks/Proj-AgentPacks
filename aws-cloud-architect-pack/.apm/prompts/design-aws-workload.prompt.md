---
description: "Design a production AWS workload from business requirements and hand it off as REQ, TOPOLOGY, CONSTRAINTS and ADR"
agent: aws-cloud-architect
---

# Design a production AWS workload

## Inputs

- Business outcome, users, critical journeys and the engagement type (greenfield, modernization, expansion).
- Non-functional targets: availability, RTO, RPO, latency, throughput, concurrency, growth, and a budget with currency and time window.
- Data classification, compliance scope, Region or partition constraints, and the target accounts.
- Existing evidence: account inventory, landing-zone facts, IaC repositories, current architecture, team skills and operating model.
- Where the handoff should be written, if the user wants files rather than an inline answer.

Discover missing facts from the supplied evidence first. Ask only when the answer would change the architecture, such as data residency or recovery objectives; otherwise record an assumption and continue.

## Workflow

1. `aws-architecture-foundations`: capture the discovery contract, separate must-haves from preferences, and inventory what already exists before proposing anything new.
2. `aws-workload-and-service-selection`: compare at least two plausible options for each material choice (compute, data store, integration) and state the rejected trade-off.
3. `aws-data-and-application-patterns`: state delivery, ordering, duplication, retry, dead-letter and idempotency behavior for every asynchronous path, and authentication, throttling, timeout and failure contracts for every API.
4. `aws-networking-hybrid-and-edge` and `aws-security-identity-and-compliance`: subnets and routing intent, ingress and egress, endpoints, workload roles, KMS ownership and secrets handling.
5. `aws-resilience-dr-and-migration`, `aws-operations-observability-and-troubleshooting` and `aws-cost-sustainability-and-finops`: recovery against the stated RTO and RPO, SLOs, alarms, runbooks and owners, cost dimensions and ownership tags.
6. `aws-docs-mcp-and-evidence`: verify every quota, Region availability, pricing or feature-maturity fact the design depends on, or mark it not-verified.
7. `aws-well-architected-and-frameworks`: test the design against the six pillars and record gaps, not a pass.
8. `aws-architecture-handoff-and-adr`: produce REQ, TOPOLOGY, CONSTRAINTS and one ADR per material decision. Use `aws-iac-deployment-and-lifecycle` to state CloudFormation, CDK or Terraform implications without writing or applying infrastructure code unless asked.

## Expected output

- A proposed architecture with account, Region, AZ, VPC and service placement, data flows and failure domains.
- The four handoff artifacts. When files are requested, write `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md` to the folder the user names.
- A completion report in the contract's section order, with every fact and check labelled.

## Guardrails

Design work is read-only. Do not deploy, create accounts, change IAM or SCPs, or call write-capable tools. Never call the design compliant, costed, resilient or Well-Architected-approved without the evidence and review scope to support it. Follow the `aws-cloud-architect-contract` instruction for the completion report, evidence labels and handoff artifacts.
