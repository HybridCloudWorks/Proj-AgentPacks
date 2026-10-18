---
description: "Turn an approved AWS architecture into an editable Draw.io diagram, validate it structurally, semantically and visually, and report what was proven"
agent: aws-cloud-architect
---

# Create an AWS architecture diagram

## Inputs

- The approved architecture: TOPOLOGY, REQ and ADR content, or a design description the user confirms is approved.
- Audience and views, for example a runtime and data-flow view or a network and egress view.
- Output path for the `.drawio` source, and any export formats, page sizes or scale the user wants.

## Workflow

1. `aws-architecture-visualization`: follow its routing for native AWS4 generation. Show account, Region, AZ, VPC and subnet boundaries, primary data and control flows, identity and security boundaries, failure domains, cost-bearing edges, assumptions and a legend. Add nothing that is absent from the approved architecture.
2. `drawio-core-generation`: choose the generation path, using native XML when AWS4 icons, custom boundaries or precise routing matter. Produce an uncompressed `mxfile` with stable unique IDs, explicit parents and valid edge references.
3. `drawio-render-export-and-review`: detect the Draw.io Desktop executable and its version, export to explicit output paths without overwriting the source, and inspect the rendered result.
4. `diagram-validation-and-evidence`: run structural checks, then compare every component and relationship against the source, then run visual checks only on a rendered output.

## Expected output

- The `.drawio` source at the requested path, plus exports when a renderer is available.
- The diagram report: structural, semantic and visual results and any items drawn as unresolved.
- A completion report in the contract's format. Record per-file structural and visual results under output_files, and renderer or live-account checks under live_or_external_checks.

## Guardrails

Static XML validation is never visual validation. Mark a visual check passed only after opening or rendering the actual output. If Draw.io Desktop is unavailable, say so and stop at static checks. A diagram is not a handoff and not proof of a deployed environment. Follow the `aws-cloud-architect-contract` instruction.
