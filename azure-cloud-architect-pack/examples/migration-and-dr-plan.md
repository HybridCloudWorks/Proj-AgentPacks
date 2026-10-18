# Worked example: migration and DR plan for an order platform

Synthetic scenario. The company, sizes and dates are illustrative. Prompt: `plan-azure-migration-and-dr.prompt.md`.

## Request

Northwind Traders must leave its leased datacenter by the end of September 2027 and asks for an Azure migration and disaster recovery plan for its order platform. Supplied: a CMDB export, a two-week dependency capture from its monitoring tool, backup reports, licensing notes, and these continuity targets:

| Tier | Workloads | RTO | RPO |
|---|---|---|---|
| 1 | Order API and order database | 2 h | 5 min |
| 2 | Warehouse integration batch, invoice file share | 8 h | 1 h |
| 3 | Reporting | 24 h | 24 h |

Current estate: two IIS web servers on Windows Server 2016 using Integrated Windows Authentication against on-premises AD DS; one SQL Server 2017 instance (1.2 TB, about 20 GB of daily change, SQL Agent jobs, cross-database queries); a 3 TB SMB invoice share; a nightly batch on a scheduled-task server. Connectivity is a site-to-site VPN, with ExpressRoute ordered. Target regions: UK South primary, UK West for recovery. A platform landing zone with hubs in both regions exists.

## 1. Inventory and dependencies

From `azure-resilience-dr-and-migration`:

| ID | Component | Depends on | Data | Tier | Label |
|---|---|---|---|---|---|
| WL-01 | Order web tier (2 VMs) | AD DS (Kerberos), WL-02, payment gateway (internet) | None persistent | 1 | observed (CMDB, capture) |
| WL-02 | Order database | AD DS for SQL logins of the batch account | 1.2 TB, 20 GB/day | 1 | observed |
| WL-03 | Warehouse batch | WL-02, SFTP to the warehouse partner | Staging files | 2 | observed |
| WL-04 | Invoice share | AD DS for NTFS ACLs | 3 TB | 2 | observed |
| WL-05 | Reporting | WL-02 (cross-database queries) | Read-only copy | 3 | observed |
| GAP-01 | Month-end finance export | Unknown | Unknown | Unknown | inferred: the two-week capture misses month-end, and the CMDB lists a finance job with no recorded connections |

GAP-01 must be closed with a capture across a month-end before wave 2.

## 2. Strategy per workload

With `azure-workload-and-service-selection` and `azure-data-and-application-patterns`:

| Workload | Strategy | Target | Reason | ADR |
|---|---|---|---|---|
| WL-01 | Rehost now, modernize later | Two Azure VMs in separate zones behind Application Gateway | Integrated Windows Authentication ties the app to AD DS today; replatforming would change authentication within the deadline | ADR-MIG-001 |
| WL-02 | Replatform | Azure SQL Managed Instance, Business Critical | SQL Agent jobs and cross-database queries rule out Azure SQL Database without rework; Managed Instance keeps instance-level features as a managed service | ADR-MIG-002 |
| WL-03 | Rehost | Azure VM | Low change rate; modernize after the exit | none |
| WL-04 | Replatform | Azure Files with AD DS authentication | Keeps SMB and NTFS ACLs. The redundancy option depends on share tier (E-03) | none |
| WL-05 | Rebuild | Restored from backup into UK West when needed | Tier 3 tolerates restore time | none |

AD DS domain controllers go into the platform identity subscription in both regions before any workload moves; WL-01, WL-02 and WL-04 all depend on them.

Database migration path for WL-02: Managed Instance link, for near-continuous replication and a short online cutover, if the source version and edition are supported (E-01). The fallback is Log Replay Service from backups, with a longer cutover window. Backup and restore offline is rejected, since restoring 1.2 TB does not fit the cutover window.

## 3. DR design

| Tier | Mechanism | Recovery path | Dependencies that must already exist in UK West |
|---|---|---|---|
| 1 | Managed Instance failover group to UK West; web VMs replicated with Azure Site Recovery | Fail over the group, recover the VMs, switch the internal DNS record | Domain controllers, hub with firewall rules, Key Vault with certificates, Application Gateway configuration, monitoring |
| 2 | Batch VM rebuilt from IaC; invoice share redundancy per E-03 | Redeploy, restore or fail over the share, repoint the batch | SFTP allow-list entry at the partner for the UK West egress IP |
| 3 | Restore from backup | Rebuild from IaC and restore the latest backup | None beyond the platform |

Failover group replication is asynchronous. The 5-minute Tier 1 RPO is a target the design aims at, not a measured property. E-02 records Microsoft's stated objective once retrieved; a drill measures the actual figure.

## 4. Cutover and rollback

| Phase | Go/no-go criteria | Rollback |
|---|---|---|
| 1. Seed replication to Managed Instance | Replication healthy for 7 days; lag within the agreed bound | Stop replication; on-premises unchanged |
| 2. Read-only validation on Azure | Reporting and test transactions return identical results | Repoint readers to on-premises |
| 3. Write cutover (window: Saturday 22:00 to 02:00) | Change freeze; application stopped; replication fully caught up | Before writes start on Managed Instance: repoint to on-premises with no data loss |
| 4. Post-cutover | Orders flowing; batch and reports succeed | After writes start: no supported return path is confirmed for this source version (E-04), so treat this as **irreversible** |

ADR-MIG-003 records the irreversible step, the business owner's sign-off, and the mitigation: keep the on-premises instance read-only for 30 days for reconciliation.

## 5. Rehearsal plan

- Migration rehearsal in non-production with a full-size restored copy, measuring seeding time, catch-up behaviour and cutover duration.
- Tier 1 DR drill: an Azure Site Recovery test failover into an isolated VNet in UK West, plus a planned failover of a non-production Managed Instance failover group, measuring recovery time and data loss end to end.
- Tier 2: restore the invoice share and rebuild the batch VM in UK West from IaC.
- Acceptance AC-REL-01: Tier 1 recovered within 2 h with no more than 5 min of data loss in a recorded drill. It stays not-verified until that drill runs.

## Completion report

- Pack: azure-cloud-architect
- Workflow: `plan-azure-migration-and-dr.prompt.md`
- Outcome: migration and DR plan delivered; nothing was migrated or replicated; no RTO or RPO has been measured; four facts are not-verified; the write cutover is irreversible until E-04 says otherwise.

### scope_and_inputs

Order platform WL-01 to WL-05 moving from Northwind's datacenter to UK South with recovery in UK West. Inputs: CMDB export, two-week dependency capture, backup reports, licensing notes, continuity targets. No live access. Execution is out of scope.

### business_outcomes_and_requirements

Datacenter exit by the end of September 2027. Tier targets as in the request table [observed: supplied]. GAP-01 is an open dependency.

### source_facts_and_evidence

Inventory and dependencies [observed] except GAP-01 [inferred]. Not retrieved [not-verified]: E-01 Managed Instance link support for SQL Server 2017 and its edition; E-02 the failover group replication objective; E-03 Azure Files redundancy options by share tier; E-04 a supported reverse-replication path for this source version.

### framework_alignment

Reliability: tiered recovery, zone-spread Tier 1. Security: AD DS kept in the identity subscription, Key Vault replicated before failover is needed. Cost: standby capacity only where Tier 1 needs it. Operations: runbooks and rehearsals before cutover. Performance: Managed Instance sizing to be validated in the rehearsal. CAF Migrate: inventory, waves and decommissioning.

### proposed_architecture

Rehost WL-01 and WL-03, replatform WL-02 to Managed Instance (ADR-MIG-002) and WL-04 to Azure Files, rebuild WL-05 on demand; the DR mechanisms per tier in section 3 [designed].

### assumptions_and_tradeoffs

Assumed the platform hubs in both regions and the domain controllers exist before wave 1. Rehosting the web tier (ADR-MIG-001) trades modernization for the deadline. Managed Instance trades cost for compatibility. The irreversible write cutover (ADR-MIG-003) is accepted only with business sign-off.

### implementation_and_operating_implications

Wave 0: domain controllers and connectivity. Wave 1: WL-02 and WL-01 together. Wave 2: WL-03 and WL-04 after GAP-01 is closed. Wave 3: WL-05. Runbooks for cutover, failover and failback are written and rehearsed before wave 1. Decommission on-premises servers only after the 30-day read-only period.

### security_resilience_cost_and_sustainability

Security: no new internet exposure, and the partner SFTP allow-list is updated for both regions. Resilience: designed per tier and unproven until drills. Cost: Business Critical Managed Instance plus its secondary and the Site Recovery protection are the largest new costs; existing licence benefits depend on Software Assurance status, which is unknown. Sustainability: Tier 3 holds no standby capacity.

### output_files

| File | Purpose | Status and label |
|---|---|---|
| handoff/order-migration/REQ.md | Tier targets, inventory, GAP-01, acceptance criteria | written [designed] |
| handoff/order-migration/TOPOLOGY.json | Target topology and recovery paths REC-01 to REC-03 | written [designed] |
| handoff/order-migration/CONSTRAINTS.json | Regions, cutover window, change freeze, approval gates | written [designed] |
| handoff/order-migration/ADR.md | ADR-MIG-001 to ADR-MIG-003, Proposed | written [designed] |

### live_or_external_checks

None run. No replication, test failover or restore was performed. Quota for Managed Instance in both regions [not-verified]. E-01 to E-04 [not-verified].

### unresolved_risks

E-01 may force the slower Log Replay Service path. GAP-01 may add an unknown dependency. The irreversible write cutover. The licensing position affects cost materially.

### next_safe_action

Retrieve E-01 to E-04 and start a month-end dependency capture for GAP-01; then schedule the non-production migration rehearsal, which needs Northwind's approval for the non-production environment and a restored copy of the database.
