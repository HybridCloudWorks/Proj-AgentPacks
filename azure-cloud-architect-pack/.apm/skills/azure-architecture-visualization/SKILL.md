---
name: azure-architecture-visualization
description: Routes Azure topology diagrams to the Azure Expert Designer while preserving architecture evidence, boundaries, legend, views, and handoff consistency.
---

# Azure Architecture Visualization

Use this Skill to decide what a diagram must communicate: context, platform landing zone, network, workload, identity/data flow, deployment, resilience, or operational view. Reuse the structured `TOPOLOGY`; do not invent visual components that are absent from the architecture decision.

Route detailed Draw.io generation, Azure2 icon selection, spacing, styles, XML authoring, rendering, export, and visual QA to the Azure Expert Designer pack. Require official icon sources, explicit trust boundaries, directional flows, region/zone labels, network scope, and a legend where symbols or abbreviations could be ambiguous.

After rendering, reconcile the diagram against `TOPOLOGY`, `CONSTRAINTS`, and `ADR`. A visually attractive diagram is not evidence that the live topology exists.
