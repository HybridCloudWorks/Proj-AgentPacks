---
name: gcp-migration-planning
description: "Plan migrations to Google Cloud from on-premises, other clouds or other Google Cloud regions - assessment and discovery, migration approach per workload, service mapping, foundation readiness, wave planning, data and database migration, cutover and rollback, and post-migration optimization. Use when a user needs a migration strategy, wave plan, data transfer plan or cutover plan for moving workloads to or within Google Cloud."
---

# Google Cloud Migration Planning

## Purpose and activation

Move workloads with a plan that is grounded in an inventory, sequences dependencies, bounds downtime and keeps a working way back until the point of no return. Activate for data centre exits, cloud-to-cloud moves, region moves, database or warehouse migrations, modernization roadmaps, or migration business cases.

## Scope and exclusions

In scope: discovery and assessment, approach selection, service mapping, target foundation checks, wave design, data transfer planning, database migration design, cutover and rollback planning, cost of dual running, and the optimization phase. Out of scope: running migration jobs, transfers, replication or cutovers, which are Level 2, and application code changes.

## Inputs

Source environment and inventory (or permission to discover it), application owners, business drivers and deadlines, downtime tolerance per workload, data volumes and change rates, network bandwidth available for transfer, dependencies, licensing, compliance and residency, and the target foundation's state.

## Dependencies and tools

[Migrate to Google Cloud: get started](https://docs.cloud.google.com/architecture/migration-to-gcp-getting-started.md.txt), [assess and discover](https://docs.cloud.google.com/architecture/migration-to-gcp-assessing-and-discovering-your-workloads.md.txt), [plan and build the foundation](https://docs.cloud.google.com/architecture/migration-to-google-cloud-building-your-foundation.md.txt), [transfer large datasets](https://docs.cloud.google.com/architecture/migration-to-google-cloud-transferring-your-large-datasets.md.txt), [database migration concepts](https://docs.cloud.google.com/architecture/database-migration-concepts-principles-part-1.md.txt), [migrating from AWS](https://docs.cloud.google.com/architecture/migration-from-aws-get-started.md.txt), [migrating from Azure](https://docs.cloud.google.com/architecture/migration-from-azure-get-started.md.txt), [migrating across regions](https://docs.cloud.google.com/architecture/migrate-across-regions.md.txt). Migration Center for discovery and cost estimates, Migrate to Virtual Machines, Database Migration Service, Storage Transfer Service, Transfer Appliance, BigQuery Migration Service.

## Workflow

1. Assess: build or import an inventory (servers, databases, storage, applications, dependencies, utilization) with Migration Center or the user's CMDB; record criticality, complexity, compliance, owners and dependencies for each workload.
2. Choose an approach per workload and record why: rehost (move VMs as they are), replatform (move and improve, for example to managed databases or containers), refactor (change the architecture to cloud-native services), rebuild, retire or retain. Prefer the least change that meets the driver; modernize after the move when the deadline is tight.
3. Map services. Treat mappings as starting points and verify feature parity, limits and pricing: virtual machines to Compute Engine; managed Kubernetes to GKE; functions to Cloud Run functions or Cloud Run; object storage to Cloud Storage; managed MySQL or SQL Server to Cloud SQL; PostgreSQL-compatible services to Cloud SQL or AlloyDB; key-value or document stores to Firestore, Bigtable or Spanner depending on access patterns and consistency; warehouses to BigQuery; queues and topics to Pub/Sub or Cloud Tasks. Use gcp-architecture-decisions for contested choices.
4. Confirm the foundation with gcp-landing-zone: hierarchy, identity, connectivity bandwidth, IP plan without overlaps, logging and policies must exist before the first wave.
5. Design waves: start with low-risk, low-dependency workloads to prove tooling and runbooks; keep tightly coupled systems in the same wave or plan hybrid connectivity between waves; define entry criteria, exit criteria and a rollback plan per wave.
6. Plan data transfer: estimate online transfer time as data volume divided by usable bandwidth (for example, 100 TB over a 10 Gbps link at 70% utilization takes about 100 x 8,000 / (10 x 0.7) / 3,600, roughly 32 hours, before verification); use Storage Transfer Service for cloud and on-premises sources, Transfer Appliance when the network is too slow, and incremental syncs before cutover.
7. Plan databases: Database Migration Service for supported homogeneous and heterogeneous paths (with schema and code conversion for heterogeneous moves), continuous change data capture to shrink the cutover window, validation by row counts and checksums, and a rehearsal in a non-production environment. BigQuery Migration Service for SQL translation from other warehouses.
8. Plan cutover: freeze window and communication, lowered DNS TTLs in advance, the order of switching (data, then services, then traffic), smoke tests and business checks, the explicit point of no return, and rollback steps that work until then (reverse replication or keeping the source writable).
9. Cost: estimate dual-running cost during migration, licence changes, egress from the source, and the optimized target cost; use gcp-cost-sustainability.
10. Optimize after each wave: rightsize from real utilization, adopt managed services, commit to steady baselines, and retire source resources only after a confirmed retention period.

## Output

Assessment summary, approach per workload with reasons, service mapping table, foundation readiness checklist, wave plan with entry and exit criteria, data transfer plan with time estimates, database migration design, cutover runbook outline with point of no return, rollback plan, cost of migration and target, risks and decision records.

## Validation

Every in-scope workload has an approach, an owner, a wave and its dependencies resolved; every data store has a transfer method and a time estimate with its arithmetic; every wave has measurable exit criteria and a rollback path; the foundation checklist is complete before wave one. Rehearsal results, when the user runs them, replace estimates.

## Failure handling and escalation

Missing inventory or owners: produce the discovery plan first and report the migration plan as PREPARED_NOT_VERIFIED. Downtime tolerance that the data volume cannot meet: present continuous replication, phased cutover or re-scoping, and ask the user to decide. Unsupported database path: name the gap and the manual or partner alternatives.

## Permissions and guardrails

Discovery that installs collectors, starting transfers, creating migration jobs or replicas, changing DNS and decommissioning source systems are Level 2. Never delete source data or disable source writes outside an approved cutover. Without the pack's contract installed, treat every migration action as needing explicit approval.

## Connection to the pack

The optional `plan-migration.prompt.md` recipe runs this skill with gcp-landing-zone, gcp-architecture-decisions, gcp-reliability-dr and gcp-cost-sustainability. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
