---
description: "Plan an Azure migration and disaster recovery strategy with RTO/RPO tiers, cutover, rollback and recovery rehearsal"
agent: azure-cloud-architect
---

# Plan an Azure migration and DR strategy

## Inputs

A workload inventory with dependencies, data sizes and change rates; business continuity targets (RTO and RPO per workload or tier); licensing; connectivity; identity dependencies; maintenance windows; existing backup and DR arrangements; deadlines and target regions. Say how the dependency data was gathered and what period it covers.

## Workflow

1. Apply `azure-architecture-foundations` to set scope, target boundaries and the continuity requirements.
2. Apply `azure-resilience-dr-and-migration`: classify workloads and dependencies, translate targets into failure domains and recovery tiers, and choose per workload between zones, paired or other regions, active/active or active/passive, backup and restore, replication, and rebuild from IaC. Include identity, DNS, secrets, keys, observability, quotas, network paths, operator access and data consistency in the recovery plan. Plan cutover, rollback, validation and decommissioning, and mark irreversible steps.
3. Apply `azure-workload-and-service-selection` and `azure-data-and-application-patterns` where a workload is replatformed rather than rehosted, including replication, failover and data consistency.
4. Add `azure-networking-hybrid-and-edge`, `azure-security-identity-and-compliance`, `azure-operations-observability-and-troubleshooting` and `azure-cost-sustainability-and-finops` for connectivity and DNS cutover, identity and keys, runbooks and monitoring, and the cost of standby capacity.
5. Apply `azure-docs-mcp-and-evidence` to supported versions, replication objectives and regional availability.
6. Apply `azure-architecture-handoff-and-adr`, with every irreversible step recorded as an ADR.

This is a plan. Do not start replication, migrate data, run failovers or tests against production, or decommission anything without explicit, scoped approval. A plan or diagram is not a recovery test: RTO and RPO stay unproven until a rehearsal measures them.

## Expected output

- Inventory and dependency classification with evidence labels and known gaps.
- A strategy per workload, the DR design per tier, and migration waves.
- A cutover runbook outline with go/no-go criteria and the rollback window for each phase.
- A rehearsal plan that measures recovery time and data loss.
- `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`, and a completion report.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
