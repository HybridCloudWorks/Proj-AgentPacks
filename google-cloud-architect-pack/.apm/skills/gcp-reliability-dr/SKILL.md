---
name: gcp-reliability-dr
description: "Design Google Cloud reliability and disaster recovery - user-centred SLOs and error budgets, composite availability, redundancy across zones and regions, graceful degradation, backup and restore, DR patterns matched to RTO and RPO, and recovery testing. Use when setting availability targets, choosing redundancy or a DR pattern, planning backups, or checking a design against RTO and RPO."
---

# Google Cloud Reliability and Disaster Recovery

## Purpose and activation

Make availability and recoverability explicit numbers that the design is shown to meet, and make recovery something that has been tested rather than assumed. Activate for availability targets, SLO design, redundancy and archetype choices, backup design, DR planning, migration cutover risk, or post-incident redesign.

## Scope and exclusions

In scope: SLIs, SLOs and error budgets; failure-mode analysis; composite availability; zone and region redundancy; load and traffic management for resilience; graceful degradation; backup, snapshot and replication design; DR patterns; recovery testing and postmortem practice. Monitoring implementation belongs to gcp-observability-operations. Running a failover, restore or chaos experiment on a live system is out of scope without Level 2 approval.

## Inputs

Critical user journeys, the availability target or contractual SLA, RTO and RPO per data store, dependencies and their SLAs, residency limits on where replicas may live, traffic patterns and peaks, budget, and the current backup and recovery setup.

## Dependencies and tools

[Well-Architected reliability pillar](https://docs.cloud.google.com/architecture/framework/reliability/printable.md.txt), [infrastructure reliability guide](https://docs.cloud.google.com/architecture/infra-reliability-guide.md.txt), [deployment archetypes comparison](https://docs.cloud.google.com/architecture/deployment-archetypes/comparison.md.txt), [DR planning guide](https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide.md.txt), [DR for cloud infrastructure outages](https://docs.cloud.google.com/architecture/disaster-recovery.md.txt), [Backup and DR Service best practices](https://docs.cloud.google.com/backup-disaster-recovery/docs/concepts/backup-plan-policy-best-practices.md.txt). Each product's current SLA page. `scripts/availability.py` in this skill folder computes error budgets, composite availability and RTO and RPO fit offline (Python 3.10 or later, standard library only).

## Workflow

1. Define reliability from the user's point of view: pick SLIs for each critical journey (availability, latency, freshness, correctness), set SLOs that balance cost and complexity against business need, and derive error budgets. Run `python scripts/availability.py budget --slo 99.9 --days 30` for the allowed downtime.
2. Compute what the architecture can deliver. Serial dependencies multiply availabilities; redundant independent replicas improve it. Use the published SLA for the exact edition and configuration of each managed service (SLAs differ between zonal, regional and multi-regional options and between editions). Run `python scripts/availability.py compose --serial 99.95 99.99 --parallel 99.5x2`. If the result is below the SLO, change the design, not the arithmetic.
3. Remove single points of failure: regional managed services or multi-zone managed instance groups, regional GKE clusters, Cloud Run's regional redundancy, regional persistent disks or database HA configurations for stateful tiers, and multiple regions behind a global load balancer when region failure is in scope. Stateful multi-region designs need a data replication and consistency decision (Spanner multi-region configurations, cross-region replicas, dual- or multi-region buckets, BigQuery dataset replication).
4. Design for overload and partial failure: autoscaling with tested limits and quotas, load shedding and rate limiting, retries with exponential backoff and jitter and bounded attempts, timeouts on every call, circuit breakers, queues to absorb bursts, and degraded modes that keep the core journey working.
5. Choose a DR pattern per tier and check it against RTO and RPO:
   - Backup and restore (cold): lowest cost; RTO is the restore and rebuild time; RPO is the backup interval. IaC can rebuild compute on demand.
   - Pilot light or warm standby: replicated data with minimal or scaled-down compute in the recovery region; RTO is scale-up time; RPO is replication lag.
   - Active-active (hot): live in more than one region; lowest RTO and RPO; highest cost and data complexity.
   Run `python scripts/availability.py dr-check --rpo-minutes 15 --rto-minutes 60 --backup-interval-minutes 5 --restore-minutes 40` and record the margins. Prefer cold or serverless standby where the objectives allow it, since idle capacity costs money and energy.
6. Backups: Backup and DR Service or product-native backups (Cloud SQL automated backups and point-in-time recovery, Backup for GKE for cluster state and volumes, persistent disk snapshot schedules, BigQuery table snapshots, Cloud Storage object versioning and retention). Store backups in a separate project with restricted access and immutability or retention locks to resist ransomware, encrypt with keys whose loss would not also lose the backups, and keep copies in a second location if region loss is in scope and residency allows.
7. Plan tests: scheduled restore tests that measure actual RTO and RPO, region or zone failover game days in non-production first, dependency failure injection, and blameless postmortems with tracked actions.
8. Record the SLOs, the archetype and the DR pattern as decision records.

## Output

SLO and error-budget table, composite availability calculation with sources, failure-mode analysis (component, failure, detection, impact, mitigation), DR pattern per tier with RTO and RPO evidence from `dr-check`, backup design, test schedule, runbook outline and decision records.

## Validation

`scripts/availability.py` results are included with their inputs; each SLA figure cites the product's SLA page for the exact configuration or is marked unverified; every data store has a backup or replication method, a restore procedure and a test; every RTO and RPO margin is non-negative or the gap is reported.

## Failure handling and escalation

Objectives that the budget cannot buy: show the cost of meeting them and the best design within budget, and ask the user to choose (BLOCKED_ON_HUMAN_DECISION). Residency that forbids a second region: design for zone resilience and in-region backups and state that region loss is not covered. Missing RTO or RPO: do not invent them; propose tiers with examples and ask.

## Permissions and guardrails

Creating backup plans, replicas or standby resources, and triggering restores, failovers or fault injection, are Level 2. Never delete backups or snapshots, shorten retention or remove locks. Without the pack's contract installed, treat every change to backup or replication settings as needing explicit approval.

## Connection to the pack

The optional `plan-resilience.prompt.md` recipe runs this skill with gcp-observability-operations; gcp-solution-architecture, gcp-migration-planning and gcp-well-architected-review use it for the reliability pillar. Installed on its own, this skill still works and the guardrails above still apply. Installed with the pack, it follows the always-on `google-cloud-architect-contract` instruction for approval levels, handoffs and the completion report.
