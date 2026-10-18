---
description: "Design an editable Azure architecture diagram in Draw.io from written requirements"
agent: azure-expert-designer
---

# Design an Azure diagram from requirements

## Inputs

- The written requirements, user stories or architecture notes, and any decisions already made.
- Diagram purpose, audience, expected fidelity, output format and output location.
- Any infrastructure code, existing diagram or repository the user points to. Source evidence takes precedence over prose.

Ask only when a missing input would materially change the architecture or the visual scope; otherwise record an assumption and proceed. Do not invent credentials, subscription names, regions or organizational policy.

## Workflow

1. Record a brief: purpose, audience, scope, source of truth, fidelity, output format, and that the task is design.
2. Apply `azure-architecture-design` in interactive design mode. Ask only questions that change the result: business flow, data sensitivity, availability target, regions, connectivity, identity, scale and required output. Offer a minimal architecture with optional security, reliability, observability and governance layers. Mark each relationship `designed` unless the user supplied evidence for it.
3. Apply `azure-architecture-patterns` when the requirements describe a recognizable pattern, and record where the design deviates from it.
4. Apply `drawio-core-generation` to choose the generation path. Use native XML when Azure2 icons, custom boundaries or precise edge routing matter.
5. Apply `azure-icons-and-visual-language` for Azure2 icon paths, product labels and boundary styles. Use a neutral labeled shape when the exact icon or service name is uncertain, and record the limitation.
6. Apply `drawio-layout-and-composition` for spacing, hierarchy, orthogonal edges and the legend, and `drawio-xml-authoring` for stable IDs, explicit parents and valid edges.
7. Apply `diagram-validation-and-evidence` after every write. If Draw.io Desktop is detected, apply `drawio-render-export-and-review` and fix what the first render shows; otherwise state that rendering was not run.

Write a new file. Ask before changing or overwriting an existing diagram.

## Expected output

- A new uncompressed `.drawio` file at the agreed path.
- A companion report: the brief, component and relationship evidence labeled `observed`, `inferred` or `designed`, design decisions, assumptions, legend notes and open questions.
- A completion report that follows the `azure-expert-designer-contract` instruction. Structural and visual checks are reported separately, and live Azure state is `not-verified` because a design has not been deployed.
