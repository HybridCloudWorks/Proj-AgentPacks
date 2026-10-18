---
name: change-scope-and-impact
description: Determines the exact change boundary, architecture context, resource blast radius, state and dependency impact, and files that must be reviewed before approval.
---

# Change Scope and Impact

Start from the actual diff or supplied file list. Inspect repository instructions, status, changed paths, configuration entry points, dependency edges, deployment roots, state boundaries, and generated artifacts. Do not treat a summary, ticket, or agent claim as the diff.

Classify changes as application, infrastructure, identity, networking, data, policy, CI/CD, documentation, or mixed. Identify environments, subscriptions, regions, tenants, resource groups, state backends, consumers, migrations, replacement risk, downtime, cost, and trust-boundary changes.

For stateful resources, look for rename/replacement, `prevent_destroy`, imports/moved blocks, data migration, backup, locking, and rollback evidence. Expand beyond the changed file only when a dependency or contract makes it necessary, and record why each expanded path was inspected.
