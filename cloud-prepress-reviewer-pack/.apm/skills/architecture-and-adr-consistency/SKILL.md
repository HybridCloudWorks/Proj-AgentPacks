---
name: architecture-and-adr-consistency
description: Reviews implementation and infrastructure changes against approved architecture, topology, ADRs, service boundaries, ownership, and stated acceptance criteria.
---

# Architecture and ADR Consistency

Locate the applicable architecture brief, `REQ`, `TOPOLOGY`, `CONSTRAINTS`, ADRs, diagrams, deployment plan, and acceptance criteria. Compare the built change to those artifacts, not to an imagined ideal.

Find architecture drift, undocumented service or boundary changes, conflicting names/tags, missing dependencies, wrong environment placement, changed data flows, and decisions implemented without an accepted ADR. If the change alters an accepted decision, require a new or superseding ADR before implementation.

Report missing design evidence separately from a proven contradiction. Route detailed cloud architecture questions to the relevant cloud architect; the pre-press reviewer decides whether the implementation is sufficiently aligned to proceed.
