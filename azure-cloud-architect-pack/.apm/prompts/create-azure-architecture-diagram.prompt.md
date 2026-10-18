---
description: "Produce an editable Draw.io diagram from an approved Azure TOPOLOGY and reconcile it against the handoff"
agent: azure-cloud-architect
---

# Create an Azure architecture diagram

## Inputs

The approved `TOPOLOGY.json`, with `CONSTRAINTS.json` and `ADR.md`; the audience; the views wanted; the output path; and any export format. If no structured topology exists, produce one with `azure-architecture-foundations` first rather than drawing from memory.

## Workflow

1. Apply `azure-architecture-visualization` to decide what each view must communicate (context, platform landing zone, network, workload, identity or data flow, deployment, resilience, or operations) and to reuse the structured topology. Do not draw components that no decision supports. Route detailed Draw.io production to the Azure Expert Designer as that Skill directs, when it is available in the host.
2. When the dedicated designer is not available, apply `drawio-core-generation` to write an uncompressed, editable `.drawio` file with stable IDs traceable to topology IDs, explicit trust boundaries, directional flows, region and zone labels, network scope, official Azure2 icons and a legend.
3. Apply `drawio-render-export-and-review`: detect Draw.io Desktop and its version before exporting, keep the `.drawio` source authoritative, and review the rendered output. If the renderer is unavailable, say export and visual review were not run.
4. Apply `diagram-validation-and-evidence` for structural, semantic and visual checks, reconciling every important component and flow against `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`.

Do not take live Azure snapshots or query a tenant to fill the diagram unless the user authorizes it. A diagram is not evidence that the live topology exists.

## Expected output

- The `.drawio` file, and the export if rendering ran.
- A reconciliation table from topology elements to diagram cells, with evidence labels.
- Structural, semantic and visual results reported separately. Static XML checks never count as visual review.
- A completion report.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
