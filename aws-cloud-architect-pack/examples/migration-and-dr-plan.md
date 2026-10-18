# Worked example: order-portal migration with cross-Region DR

Workflow: `plan-migration-and-dr.prompt.md`. Skills applied: `aws-architecture-foundations`, `aws-resilience-dr-and-migration`, `aws-workload-and-service-selection`, `aws-networking-hybrid-and-edge`, `aws-security-identity-and-compliance`, `aws-operations-observability-and-troubleshooting`, `aws-cost-sustainability-and-finops`, `aws-docs-mcp-and-evidence`, `aws-architecture-handoff-and-adr`.

The company and figures are fictional.

## Request

> Meridian Parts wants to move its B2B order portal off VMware into our existing AWS landing zone. The board also requires that the portal survives the loss of an AWS Region. Plan the migration and DR.

## Inputs and discovery

| Fact | Value | Label |
|---|---|---|
| App tier | 4 RHEL 8 VMs running Java on Tomcat behind an on-premises load balancer | observed (VM inventory) |
| Batch tier | 2 VMs for nightly EDI processing, reading and writing a 600 GB NFS share | observed (VM inventory) |
| Database | PostgreSQL 13 primary plus a streaming replica, 2.1 TB, about 30 GB of changes per day | observed (DBA export) |
| Dependencies | Staff LDAP, SMTP relay and the ERP system stay on premises; partner SFTP endpoints are external | observed (dependency export) |
| Objectives | Portal RTO 4 h, RPO 15 min. Batch RTO 24 h, RPO 24 h | observed (business continuity plan) |
| Recovery authority | VP Operations declares a Region failover | observed (business continuity plan) |
| Regions | us-east-2 primary, us-west-2 recovery | observed (brief) |
| Landing zone | Workload accounts `orders-prod` and `orders-dr` exist. Direct Connect at 1 Gbps with VPN backup | observed (account list, network diagram) |
| Window | Saturday 22:00 to Sunday 06:00 local time | observed (change calendar) |

`aws-architecture-foundations` classified this as **both** migration and DR, with different objectives per tier.

## Strategy per component

Using `aws-workload-and-service-selection` and `aws-resilience-dr-and-migration`:

| Component | Migration | Rejected option | DR strategy |
|---|---|---|---|
| Portal app tier | Rehost with AWS MGN onto EC2 in two AZs behind an ALB. After migration, bake an AMI and move to an Auto Scaling group | Refactor to containers now. It would add risk to the cutover window; deferred to a later ADR | Pilot light: launch template and AMI copies in us-west-2, ASG at zero, scaled out on failover |
| Database | Replatform to Aurora PostgreSQL with AWS DMS (full load plus change data capture) | Self-managed PostgreSQL on EC2: more operations, and no managed cross-Region replication | Aurora Global Database secondary cluster in us-west-2 |
| NFS share | Amazon EFS, copied with AWS DataSync | FSx: not needed, because the access pattern is plain NFS | EFS replication to us-west-2 |
| Batch | Rehost with MGN | n/a | Backup and restore with AWS Backup cross-Region copies, which meets RTO 24 h |

**Failure-domain finding.** Staff sign-in depends on on-premises LDAP over Direct Connect in both Regions. Losing a Region does not break it, but losing the data center or the Direct Connect location would block staff, not customers. This is recorded as a dependency risk with the identity team as owner. It is not something the DR design can solve.

## Waves and gates

| Wave | Scope | Exit gate |
|---|---|---|
| 0: readiness | VPC subnets for replication, DMS and MGN; security groups; KMS keys in **both** Regions; backup policy; Direct Connect routes to the new VPCs | An MGN test instance boots, and a DMS endpoint connection test succeeds |
| 1: batch | EDI VMs and the NFS share via DataSync | Three consecutive nightly runs reconcile with the on-premises output |
| 2: portal | DMS full load plus change data capture, MGN replication, cutover | The cutover runbook completes, and validation passes |
| 3: DR | Global Database secondary, AMI copies, pilot-light stacks, failover runbook | The first game day meets the 4 h RTO |
| 4: decommission | On-premises VMs and database | 30 days stable, reverse replication stopped, sign-off from the application owner and the DBA |

**Transfer estimate.** The 2.1 TB full load at about 60% of the 1 Gbps link is about 2.1 × 10¹² × 8 / 0.6 × 10⁹ ≈ 28,000 s, or 7.8 h. That is designed arithmetic, not a measurement. The full load therefore runs days ahead of cutover, with change data capture keeping the target in sync, and never inside the window.

## Cutover and rollback

The runbook outline comes from `aws-operations-observability-and-troubleshooting`:

1. T-7 days: lower the DNS TTL on `orders.meridianparts.example` to 60 s.
2. T-1 h: confirm DMS change-data-capture latency is near zero and validation tasks are clean.
3. 22:00: show the maintenance page and stop the on-premises app writers.
4. Wait for change data capture to drain, then stop the DMS task.
5. Reset PostgreSQL sequences on Aurora. DMS moves data, not every secondary object, so sequences must be set explicitly.
6. Compare row counts and checksums on the 12 core tables.
7. Point the app tier at Aurora, run smoke tests, switch DNS, and remove the maintenance page.

Rollback has two stages:

- **Before traffic reopens.** Switch DNS back and restart the on-premises writers. The source has not changed.
- **After traffic reopens.** A reverse DMS task from Aurora to on-premises PostgreSQL runs for 14 days, so rolling back does not lose new orders. The rollback decision deadline is 72 h after cutover. After that, rollback requires a planned reverse migration.

## DR timeline (designed)

| Step | Budget |
|---|---|
| Detect and assess | 30 min |
| Failover declared by VP Operations | 30 min |
| Promote the Aurora secondary cluster | under 30 min |
| Scale the app tier ASG in us-west-2 and attach EFS | 45 min |
| Switch DNS and validate | 30 min |
| **Total** | **about 2 h 45 min, against a 4 h RTO** |

This timeline is designed. It stays unproven until the Wave 3 game day.

## Evidence

`aws-docs-mcp-and-evidence`:

| Claim | Source | Label |
|---|---|---|
| AWS MGN supports RHEL 8 source servers | MGN supported operating systems, retrieved 2026-10-18 | observed |
| DMS supports PostgreSQL 13 as a source | DMS source endpoints, retrieved 2026-10-18 | observed |
| Aurora Global Database is available in us-east-2 and us-west-2 | AWS Knowledge MCP Region listing, retrieved 2026-10-18 | observed |
| Global Database replication lag stays within the 15 min RPO under this write rate | Documented typical lag only; not measured for this workload | not-verified |
| Aurora PostgreSQL offers a version compatible with the application's extensions | Extension list not yet supplied by the DBA | not-verified |

## Completion report

Pack: aws-cloud-architect. Date: 2026-10-18.

Outcome: the migration and DR plan is designed. No replication has started, nothing has migrated, and neither RTO nor RPO has been tested.

### scope_and_inputs

Order portal and EDI batch, from VMware to `orders-prod` (us-east-2) with recovery in `orders-dr` (us-west-2). Inputs were the VM inventory, the DBA export, the dependency export, the business continuity plan, the account list, the network diagram and the change calendar (observed). Authority covered planning and writing files to `handoff/order-portal-migration/`.

### business_outcomes_and_requirements

- Exit VMware for the portal.
- Survive a Region loss with portal RTO 4 h and RPO 15 min, and batch RTO 24 h and RPO 24 h.
- Cut over inside one weekend window, with a rollback path that keeps new orders.

### source_facts_and_evidence

- Estate and objectives: observed from the user's exports.
- Service support and Region availability via the AWS Knowledge MCP Server: observed, 2026-10-18.
- Replication lag under load and extension compatibility: not-verified.

### framework_alignment

- Reliability: objectives are traced to a strategy per tier, and the game day is planned.
- Operational Excellence: cutover and failover runbooks.
- Security: KMS keys and backup access in both Regions.
- Cost: dual running and pilot light are modelled.
- Gaps: the LDAP dependency, and an untested RTO.

### proposed_architecture

- MGN-rehosted EC2 behind an ALB across two AZs.
- Aurora PostgreSQL with a Global Database secondary.
- EFS with replication.
- A pilot-light app tier in us-west-2.
- AWS Backup copies for batch.

All designed. TOPOLOGY covers both Regions.

### assumptions_and_tradeoffs

- ADR-001: rehost before refactor.
- ADR-002: Aurora Global Database for the portal RPO.
- ADR-003: pilot light rather than warm standby. It costs less and the designed 2 h 45 min timeline leaves margin against the 4 h RTO. Revisit if the game day exceeds 3 h.
- Assumption: the DBA confirms the extension list before Wave 2.

### implementation_and_operating_implications

- Wave gates as listed. Full load runs days before cutover.
- The cutover runbook includes resetting sequences.
- Reverse replication runs for 14 days.
- Owners: migration lead (waves), DBA (data validation), VP Operations (failover declaration), platform team (DR stacks).

### security_resilience_cost_and_sustainability

- Security (designed): KMS keys per Region, cross-account backup vault access limited to a restore role, DMS and MGN replication over Direct Connect only.
- Resilience (designed): multi-AZ primary, cross-Region pilot light. Not tested.
- Cost: Global Database secondary, EFS replication, AMI and backup copies and 14 days of dual running are modelled by dimension. Prices are not-verified.
- Sustainability: on-premises hardware is retired at Wave 4.

### output_files

| File | Purpose | Check run | Label |
|---|---|---|---|
| `handoff/order-portal-migration/REQ.md` | Objectives per tier, verification criteria including the game day | Reviewed against the template | designed |
| `handoff/order-portal-migration/TOPOLOGY.json` | Both Regions, dependencies, failure domains | Parsed as JSON | structurally-validated |
| `handoff/order-portal-migration/CONSTRAINTS.json` | Recovery objectives, KMS, backup policy, change window | Parsed as JSON | structurally-validated |
| `handoff/order-portal-migration/ADR.md` | ADR-001 to ADR-003 | Alternatives and revisit triggers present | designed |

### live_or_external_checks

- Documentation and Region lookups: executed (observed).
- DMS endpoint tests, MGN replication, replication-lag measurement and the game day: not executed (not-verified).

### unresolved_risks

- Staff sign-in depends on on-premises LDAP (owner: identity team).
- Extension compatibility is unknown (owner: DBA).
- The RTO and RPO are unproven until the Wave 3 game day (owner: VP Operations).

### next_safe_action

The DBA supplies the extension list. The platform team then builds the Wave 0 readiness resources in `orders-prod` after explicit approval of the Wave 0 change. Do not start replication until Wave 0 passes its gate.
