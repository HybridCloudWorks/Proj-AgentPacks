---
description: "Plan a migration to Google Cloud"
agent: google-cloud-architect
---

# Plan a migration to Google Cloud

## Inputs

The source environment (on-premises, another cloud or another Google Cloud region), the workload inventory or how to obtain it, business drivers, downtime tolerance, data volumes, dependencies, compliance constraints and the target timeline.

## Workflow

Apply gcp-migration-planning. Assess and group workloads, choose a migration approach per workload, confirm the landing zone with gcp-landing-zone, map source services to Google Cloud services with gcp-architecture-decisions, plan data transfer and cutover with gcp-reliability-dr, and define wave exit criteria and rollback.

## Expected output

Workload assessment, approach per workload, service mapping, wave plan, data migration and cutover runbook outline, risks, cost estimate with its basis, rollback plan and decision records. Apply the `google-cloud-architect-contract` instruction; no migration job, transfer or cutover is started without Level 2 approval.
