# Cost and governance record: <change title>

The record cost-allocation-and-governance-review keeps for a change that adds, resizes or reconfigures billable resources, or that relies on a policy exception. Summarize it in the report's operations, rollback, cost and inputs section.

## Cost assumptions

Do not invent pricing. Give the source of every figure; mark estimates as estimates and require current pricing evidence when the figure decides the gate.

| Item | Value | Source | Label |
|---|---|---|---|
| Owner | <person or team> | <tag, CODEOWNERS, plan> | <label> |
| Cost center | <allocation identifier> | <tag or plan> | <label> |
| Environment and region | <environment, region> | <file and line> | observed |
| SKU or tier | <SKU> | <file and line> | observed |
| Expected utilization | <figure> | <author estimate, telemetry> | <label> |
| Storage and log growth | <figure per month> | <source> | <label> |
| Backup, egress, private connectivity | <figures> | <source> | <label> |
| Shared-service allocation | <how shared cost is split> | <source> | <label> |
| Recurring cost change | <amount per month> | <source and date> | <label> |
| One-time cost | <amount> | <source> | <label> |
| Documented ceiling | <amount, and the repository contract that sets it; or "none documented"> | <file> | observed |
| Position against ceiling | <under, over, or unknown, with the figures used> | | <label> |

## Allocation and controls

| Control | Required by | Status | Evidence |
|---|---|---|---|
| Mandatory tags | <policy or constraint> | <present, missing> | <file and line> |
| Budget and alert | <constraint> | <present, missing, out of scope> | <source> |
| Quota impact | <subscription or region quota> | <within, at risk, unknown> | <source> |
| Idle and non-production behavior | <constraint> | <scale to zero, schedule, always on> | <file and line> |
| Retention and autoscaling | <constraint> | <setting> | <file and line> |
| Commitments | <reservation or savings plan> | <applies, not applicable> | <source> |
| Sustainability trade-off | <constraint> | <note> | <source> |

## Policy exceptions

One row per exemption, exclusion or waiver the change relies on. An exception with no expiry or no owner is a governance failure; a deny policy with no legitimate exception path is a delivery risk.

| Policy and assignment | Effect | Exception scope | Owner | Rationale | Expires | Compensating control | Removal plan |
|---|---|---|---|---|---|---|---|
| <definition or initiative, assignment scope> | <audit, modify, deployIfNotExists, deny, denyAction> | <exact scope> | <owner> | <why> | <date> | <control> | <how and when it is removed> |
