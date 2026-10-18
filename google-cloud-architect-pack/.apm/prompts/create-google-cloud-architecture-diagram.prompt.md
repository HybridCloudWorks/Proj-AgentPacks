---
description: "Turn an approved Google Cloud architecture into an editable Draw.io diagram with current Google Cloud icons, validate it structurally, semantically and visually, and report what was proven"
agent: google-cloud-architect
---

# Create a Google Cloud architecture diagram

## Inputs

- The approved design: the solution guide and decision records, or a design description the user confirms is approved.
- Audience and views, for example a runtime and data-flow view or a network and connectivity view.
- Any other provider or on-premises system the diagram must show.
- Output path for the `.drawio` source, and any export formats, page sizes or scale.

## Workflow

1. `drawio-core-generation`: list the providers shown and read their sections in its provider reference. Take every Google Cloud icon from the "Google Cloud Platform 2026" library: a core product icon where Google defines one, and a category icon with the product's label for everything else. Nest ownership as organization, folder and project, and the network as VPC network, then region, then subnet, with zonal resources in zone frames inside their subnet. Draw Shared VPC host and service projects as separate frames. Add nothing that is absent from the approved design.
2. `drawio-render-export-and-review`: detect Draw.io Desktop and its version, export to explicit paths without overwriting the source, and inspect the render, including that every icon drew its symbol.
3. `diagram-validation-and-evidence`: run its checker, then compare every component and relationship with the design, then run visual checks only on the rendered output.

## Expected output

- The `.drawio` source at the requested path, plus exports when a renderer is available.
- The validation report: structural, icon, semantic and visual results, the catalog's draw.io version, and any item drawn as unresolved.
- A completion report in the contract's format.

## Guardrails

Static XML validation is never visual validation. If Draw.io Desktop is unavailable, say so, stop at static checks and report the visual checks as not run. A diagram is not proof of a deployed environment, and drawing it changes no cloud resource. Follow the `google-cloud-architect-contract` instruction.
