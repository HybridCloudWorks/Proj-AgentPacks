---
name: changelogs-release-notes-and-migration
description: Record shipped changes, release notes, deprecations, breaking changes, migration paths, and upgrade guidance accurately and traceably.
---

# Changelogs, Releases, and Migrations

Document what actually changed, when, for whom, why it matters, compatibility impact, security or cost impact, required action, and links to implementation, issue, PR, ADR, and release evidence. Keep planned work in a roadmap or task list, not in a shipped changelog.

For migrations, state source and target, prerequisites, inventory, sequence, data/state handling, downtime, rollback, validation, owner, and version boundaries. Separate code migration from operational cutover and customer communication.

Use consistent categories such as Added, Changed, Fixed, Security, Deprecated, Removed, and Breaking. Do not claim successful deployment, customer impact, or backward compatibility without evidence.
