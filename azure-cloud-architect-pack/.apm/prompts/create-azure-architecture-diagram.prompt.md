---
description: "Produce an editable Draw.io diagram from an approved Azure TOPOLOGY and reconcile it against the handoff"
agent: azure-cloud-architect
---

# Create an Azure architecture diagram

## Inputs

The approved `TOPOLOGY.json`, with `CONSTRAINTS.json` and `ADR.md`; the audience; the views wanted; the output path; and any export format. If no structured topology exists, produce one with `azure-architecture-foundations` first rather than drawing from memory.

## Workflow

1. Apply `azure-architecture-visualization` to decide what each view must communicate (context, platform landing zone, network, workload, identity or data flow, deployment, resilience, or operations) and to reuse the structured topology. Do not draw components that no decision supports. Route detailed Draw.io production to the Azure Expert Designer as that Skill directs, when it is available in the host.
2. When the dedicated designer is not available, apply `drawio-core-generation` to write an uncompressed, editable `.drawio` file with stable IDs traceable to topology IDs, explicit trust boundaries, directional and labelled flows, region and zone labels, network scope, current icons from draw.io's Azure library (ID `azure2`, Microsoft's Azure architecture icons) in the palette's own style, and a legend. Nest boundaries by its workflow step 4: one VNet per region; no subnet inside a zone frame; zone-redundant resources labelled with their zones; PaaS reached through a private endpoint outside the VNet with only the endpoint NIC in the subnet; and a resource whose resource group differs from its VNet's parented to the network boundary it is deployed into, with its resource group in its label.
3. Run `diagram-validation-and-evidence`'s checker, `scripts/check_drawio.py --strict`, after every write.
4. Apply `drawio-render-export-and-review`: detect Draw.io Desktop and its version before exporting, including the Microsoft Store build (`app\draw.io.exe` inside the InstallLocation that `Get-AppxPackage *draw.io*` reports), keep the `.drawio` source authoritative, export with `-k` and without `--layout` or `--normalize`, pass `--embed-svg-images` for SVG, and review the rendered output, confirming that every Azure icon drew. If the renderer is not found in any of that skill's locations, say export and visual review were not run.
5. After the last edit, apply `diagram-validation-and-evidence` for the final structural, semantic and visual checks, reconciling every important component and flow against `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`.

Do not take live Azure snapshots or query a tenant to fill the diagram unless the user authorizes it. A diagram is not evidence that the live topology exists.

## Expected output

- The `.drawio` file, and the export if rendering ran.
- A reconciliation table from topology elements to diagram cells, with evidence labels.
- Structural, semantic and visual results reported separately. Static XML checks never count as visual review.
- A completion report.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
