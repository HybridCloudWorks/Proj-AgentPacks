---
description: "Plan reliability, observability and disaster recovery for a Google Cloud workload"
agent: google-cloud-architect
---

# Plan reliability and disaster recovery

## Inputs

The workload architecture, user journeys, availability target or SLO, RTO and RPO per data store, dependencies, residency constraints, budget and the current backup and monitoring setup.

## Workflow

Apply gcp-reliability-dr to define SLOs and error budgets, compute composite availability with the skill's calculator, select a deployment archetype and DR pattern per tier and check each against RTO and RPO. Apply gcp-observability-operations for SLO monitoring, alerting, logging and incident readiness. Plan recovery tests; do not trigger failovers or restores.

## Expected output

SLO and error-budget table, failure-mode analysis, DR pattern per tier with RTO and RPO evidence, backup and restore plan, monitoring and alerting design, test schedule and runbook outline, and the completion report. Apply the `google-cloud-architect-contract` instruction.
