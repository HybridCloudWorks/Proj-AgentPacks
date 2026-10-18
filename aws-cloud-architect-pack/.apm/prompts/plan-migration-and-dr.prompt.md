---
description: "Plan an AWS migration or disaster-recovery strategy from explicit RTO and RPO, with waves, cutover, rollback and recovery testing"
agent: aws-cloud-architect
---

# Plan a migration or disaster-recovery strategy

## Inputs

- Application portfolio, dependency map and business criticality for each application.
- RTO, RPO and data-loss tolerance per application, and who has authority to declare a recovery.
- Source platforms, versions, data volumes and change rates, licensing constraints and maintenance windows.
- Landing-zone readiness, connectivity to the source environment, and target and recovery Regions.
- Operational skills and the acceptable cost of standby capacity.

## Workflow

1. `aws-architecture-foundations`: classify the work as migration, DR, or both, and record current-state evidence.
2. `aws-resilience-dr-and-migration`: choose backup and restore, pilot light, warm standby, hot standby, active/active or service-native recovery from the objectives. Map failure domains, plan waves with entry and exit gates, and define cutover, rollback, decommissioning and recovery testing.
3. `aws-workload-and-service-selection`: decide rehost, replatform or refactor per component, and state the rejected option.
4. `aws-networking-hybrid-and-edge`: transfer paths, DNS cutover and connectivity for the recovery Region.
5. `aws-security-identity-and-compliance`: KMS keys in the recovery Region, cross-account backup access and restore permissions.
6. `aws-operations-observability-and-troubleshooting`: cutover runbooks, monitoring, game days and decision checkpoints.
7. `aws-cost-sustainability-and-finops`: replication, standby, transfer and dual-running costs.
8. `aws-docs-mcp-and-evidence`: verify source-version support for AWS MGN, DMS or DataSync, and service availability in both Regions.
9. `aws-architecture-handoff-and-adr`: REQ, TOPOLOGY for both Regions, CONSTRAINTS with recovery objectives, and ADRs for the strategy.

## Expected output

- The strategy per application, traced to its RTO and RPO, with an estimated recovery timeline that is labelled designed until tested.
- A wave plan with gates, a cutover runbook outline, rollback paths before and after traffic moves, and decommissioning criteria.
- A recovery-test plan, the handoff artifacts, and a completion report in the contract's format.

## Guardrails

Keep source systems intact until a replacement and a rollback path are approved. Do not start replication, migrate data, cut over, fail over or decommission without explicit, scoped authorization. Replication is not recoverability, and multi-AZ is not multi-Region DR. An RTO or RPO is live-verified only by a recovery test. Follow the `aws-cloud-architect-contract` instruction.
