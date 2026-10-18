---
name: aws-operations-observability-and-troubleshooting
description: Design AWS operating models and investigate incidents using CloudWatch, CloudTrail, Config, VPC telemetry, service events, runbooks, and evidence-aware troubleshooting.
---

# AWS Operations, Observability, and Troubleshooting

Use this Skill for operational readiness, SLOs, dashboards, alarms, logs, traces, CloudTrail, Config, VPC Flow Logs, incident response, performance issues, service events, or production troubleshooting.

## Operating model

Define owners, on-call, SLO/SLI, dashboards, alarms, log retention, trace context, runbooks, change management, escalation, incident roles, post-incident learning, and cost/PII controls. Observability must support a decision, not merely collect data.

## Troubleshooting loop

Establish impact and time window; preserve evidence; check AWS Health/service events, deployment/change history, CloudTrail, CloudWatch metrics/logs/traces, DNS, routes, security policies, quotas, dependencies, and recent drift. Form a falsifiable hypothesis, run the least risky diagnostic, and state confidence.

Do not restart, scale, detach, delete, modify IAM, or change networking in production without explicit authorization and a rollback/containment plan. Separate symptom mitigation from root-cause correction.
