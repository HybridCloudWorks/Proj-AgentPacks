---
name: azure-architecture-visualization
description: Routes Azure topology diagrams to the Azure Expert Designer while preserving architecture evidence, boundaries, legend, views, and handoff consistency.
---

# Azure Architecture Visualization

Use this Skill to decide what a diagram must communicate: context, platform landing zone, network, workload, identity/data flow, deployment, resilience, or operational view. Reuse the structured `TOPOLOGY`; do not invent visual components that are absent from the architecture decision.

Route detailed Draw.io generation, Azure icon selection (draw.io's current Azure library, ID `azure2`), spacing, styles, XML authoring, rendering, export, and visual QA to the Azure Expert Designer pack, or to this pack's shared `drawio-core-generation`, `drawio-render-export-and-review` and `diagram-validation-and-evidence` Skills when the designer is not installed. Require current official icons, explicit trust boundaries, directional flows, region/zone labels, network scope nested by `drawio-core-generation` workflow step 4, and a legend where symbols or abbreviations could be ambiguous.

After rendering, reconcile the diagram against `TOPOLOGY`, `CONSTRAINTS`, and `ADR`. A visually attractive diagram is not evidence that the live topology exists.
