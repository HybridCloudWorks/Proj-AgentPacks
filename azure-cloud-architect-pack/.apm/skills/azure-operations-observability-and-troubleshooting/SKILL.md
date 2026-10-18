---
name: azure-operations-observability-and-troubleshooting
description: Designs and diagnoses Azure operations using Azure Monitor, Log Analytics, Activity Log, Resource Graph, health signals, alerts, runbooks, and evidence-aware incident analysis.
---

# Azure Operations and Troubleshooting

Define ownership, SLOs, signals, alert thresholds, escalation, runbooks, and change correlation. Cover Azure Monitor, Log Analytics, Application Insights, diagnostic settings, Activity Log, Resource Health, Service Health, Advisor, Resource Graph, Defender, and Sentinel as appropriate.

Diagnose from actual evidence: error text, deployment operation, activity log, resource state, metrics, traces, policy evaluation, network path, identity token/role, quota, and recent change. Locate the boundary: bootstrap, auth, validation, plan, deployment, data plane, or post-deployment.

Separate confirmed cause from hypothesis. Check partial changes, state locks, orphaned resources, policy effects, regional incidents, and rollback impact. Report commands for the operator; do not rerun a mutating command or delete/repair a resource without approval.
