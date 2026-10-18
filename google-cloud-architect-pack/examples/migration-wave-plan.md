# Worked example: data-centre exit wave plan

Synthetic scenario for the `plan-migration.prompt.md` workflow.

## Inputs

300 VMs (Linux and Windows), two PostgreSQL databases (2 TB and 6 TB), 40 TB of file shares, a 5 Gbps Interconnect available for migration, nine-month deadline, maximum two hours of downtime for customer-facing systems. The landing zone exists and has been confirmed with gcp-landing-zone.

## Approach per workload group

| Group | Count | Approach | Target | Reason |
|---|---|---|---|---|
| Stateless web and API servers | 80 | Replatform | Cloud Run or managed instance groups | Low effort, removes patching |
| Line-of-business apps with vendor support | 150 | Rehost | Compute Engine with Migrate to Virtual Machines | Vendor support requires the same OS |
| Batch servers | 40 | Replatform | Batch on Spot VMs | Fault-tolerant, cost-sensitive |
| Unused or duplicate servers | 30 | Retire | none | No owner after review |
| PostgreSQL databases | 2 | Replatform | Cloud SQL for PostgreSQL via Database Migration Service with continuous replication | Keeps engine, shrinks cutover |

## Data transfer arithmetic

File shares: 40 TB × 8,000 Gb/TB = 320,000 Gb. Usable bandwidth 5 Gbps × 0.7 utilization = 3.5 Gbps. 320,000 / 3.5 ≈ 91,400 seconds ≈ 25 hours of transfer, plus verification and an incremental sync before cutover. Online transfer with Storage Transfer Service fits; Transfer Appliance is not needed.

## Waves

1. Wave 0 (pilot): ten low-risk internal apps to prove tooling, runbooks and rollback. Exit: all ten pass smoke tests, rollback rehearsed once.
2. Wave 1: batch and stateless groups. Exit: error rates and latency within 10% of baseline for two weeks.
3. Wave 2: line-of-business apps in dependency groups. Exit: business sign-off per group.
4. Wave 3: databases and customer-facing systems, with continuous replication running for at least a week before cutover.

## Cutover outline for the databases

Lower DNS TTLs three days before; freeze writes; let replication lag reach zero; validate row counts and checksums on key tables; promote the Cloud SQL instance; switch connection strings; run smoke and business checks. The point of no return is the first write to the new primary; until then rollback is to unfreeze the source.

## Result

Status PREPARED_NOT_VERIFIED. "The design is prepared, but completion is not verified." The inventory came from the user's CMDB export, not from discovery, and no rehearsal has run. Starting any transfer, migration job or cutover is a Level 2 action.
