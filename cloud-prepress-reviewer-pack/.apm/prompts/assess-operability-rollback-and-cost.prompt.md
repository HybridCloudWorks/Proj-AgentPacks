---
description: "Assess day-two readiness of a change: observability, recovery, rollback boundary, cost, allocation and policy exceptions"
agent: cloud-prepress-reviewer
---

# Assess operability, rollback and cost readiness

## Inputs

- The exact change and its deployment plan: deployment order, rollout strategy (slot, revision or canary) and expected downtime.
- Operating evidence: owner, SLOs, health signals, alerts, dashboards, runbooks, escalation path, and post-deployment verification steps.
- Recovery evidence: backup and restore or rebuild evidence for stateful resources, migration sequence, and any rehearsal results.
- Cost assumptions: recurring and one-time cost, SKU or tier, region, expected utilization, storage and log growth, egress, cost center, and any documented budget ceiling.
- Any policy exception or exemption the change relies on.

## Workflow

1. Apply change-scope-and-impact to identify stateful and shared resources, consumers and dependency order.
2. Apply operability-resilience-and-rollback-review to check observability of failure paths without exposing secrets, backup and restore evidence, deployment order, health probes, capacity and quotas, regional failure assumptions, and the point beyond which rollback becomes restore or forward-fix.
3. Apply cost-allocation-and-governance-review to compare stated cost with any documented ceiling, check mandatory tags, budgets and alerts, idle and non-production behavior, retention and autoscaling, and review every policy exception for owner, rationale, scope, expiration, compensating control and removal plan. Do not invent pricing; mark estimates and require current pricing evidence when the figure is material.
4. Apply azure-evidence-and-mcp-review to label a rollback narrative `designed`, a rehearsal result by what it actually exercised, and live evidence only when an authorized read produced it.
5. Apply review-report-and-pr-gate to write the report.

## Expected output

A pre-press report whose operations, rollback, cost and inputs section states the rollback boundary and point of no return, recovery evidence with its label, the cost position against the ceiling with the source of each figure, tag and budget status, each policy exception with its expiry, and any new required inputs by name and secret reference only. A rollback plan that was never rehearsed is not a tested recovery result.

Follow the `cloud-prepress-reviewer-contract` instruction. Never describe an unexecuted check as passed.
