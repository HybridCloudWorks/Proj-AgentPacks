---
name: aws-resilience-dr-and-migration
description: Design AWS availability, backup, disaster recovery, migration, modernization, cutover, rollback, and recovery-testing strategies from explicit RTO and RPO.
---

# AWS Resilience, DR, and Migration

Use this Skill for HA, DR, backups, multi-AZ, multi-Region, migration waves, replication, cutover, rollback, AWS MGN, DMS, DataSync, Snow services, modernization, or recovery testing.

## Start with objectives

Define business criticality, RTO, RPO, data loss tolerance, dependency order, recovery authority, operational skill, Region/partition constraints, and acceptable cost. Select pilot light, warm standby, hot standby, active/active, backup/restore, or service-native recovery based on those objectives and test the result.

## Design for failure

Map failure domains from process to AZ, Region, account, provider dependency, identity, network, data, and operator error. Include backups, immutable copies, encryption keys, cross-account access, retention, restore permissions, runbooks, monitoring, game days, and configuration drift. Multi-AZ is not multi-Region DR; replication is not recoverability.

## Migration

Use discovery, dependency mapping, wave sequencing, landing-zone readiness, data transfer, validation, cutover, rollback, and decommissioning gates. Preserve existing systems during migration unless a replacement and rollback path are approved. Do not make destructive changes based only on a migration diagram.
