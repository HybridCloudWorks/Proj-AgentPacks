---
name: operability-resilience-and-rollback-review
description: Reviews observability, alerting, backup, recovery, rollout, rollback, migration, downtime, and day-two operating readiness before deployment.
---

# Operability, Resilience, and Rollback Review

Check ownership, SLOs, health signals, logs, metrics, traces, diagnostic settings, alerts, dashboards, runbooks, incident escalation, and post-deployment verification. Verify that failure paths are observable without exposing secrets or sensitive data.

For stateful or shared resources, require backup/restore or rebuild evidence, migration sequencing, lock/state recovery, `prevent_destroy` or equivalent safeguards, rollback boundaries, data consistency, and an explicit point beyond which rollback becomes restore/forward-fix.

Review deployment order, canary/slot/revision strategy, downtime, dependency compatibility, health probes, capacity, quotas, and regional failure assumptions. A rollback narrative is not a tested recovery result; label rehearsal and live evidence separately.
