# Rollback and operability readiness: <change title>

The record operability-resilience-and-rollback-review keeps before deployment. Summarize it in the report's operations, rollback, cost and inputs section. Label every row: a rollback narrative is `designed` until a rehearsal exercises it, and a rehearsal is not live evidence.

## Operating readiness

| Item | Value | Evidence label |
|---|---|---|
| Service owner and on-call | <team, escalation path> | <label> |
| SLOs | <objective and measurement window; or "none defined"> | <label> |
| Health signals | <logs, metrics, traces, diagnostic settings that show the change working or failing> | <label> |
| Alerts and dashboards | <alert names and thresholds> | <label> |
| Runbook | <location and the failure modes it covers> | <label> |
| Post-deployment verification | <the checks the operator runs, and their pass condition> | designed |
| Secret and sensitive data exposure in signals | <confirmed none, or the finding raised> | <label> |

## Rollout

| Item | Value | Evidence label |
|---|---|---|
| Deployment order | <sequence across resources and consumers> | <label> |
| Strategy | <slot swap, revision traffic split, canary, blue-green, in place> | <label> |
| Expected downtime | <duration, or "none expected" with reason> | <label> |
| Dependency compatibility | <old and new versions that must coexist during rollout> | <label> |
| Health probes | <probe path and gate> | <label> |
| Capacity and quotas | <headroom and the quota checked> | <label> |
| Regional failure assumption | <single region, paired region, zone redundant> | <label> |

## Stateful and shared resources

| Resource | Data at risk | Safeguard | Backup and restore evidence | Evidence label |
|---|---|---|---|---|
| <resource> | <what is lost if it is replaced or deleted> | <`prevent_destroy`, resource lock, soft delete, purge protection> | <last restore test, or rebuild procedure> | <label> |

Migration sequence and data consistency: <ordering, dual-write or backfill, verification query>.

State and lock recovery: <how a stuck or corrupted state or lock is recovered, and who is authorized to do it>.

## Rollback boundary

| Item | Value |
|---|---|
| Rollback method | <revert commit and redeploy, slot swap back, traffic shift, feature flag> |
| Rollback owner | <person or role> |
| Point of no return | <the step after which rollback becomes restore or forward-fix, for example the first schema migration or the first data write in the new format> |
| Restore or forward-fix plan beyond that point | <procedure and its evidence> |
| Rehearsal | <date, environment, what it exercised; or "not rehearsed"> |
