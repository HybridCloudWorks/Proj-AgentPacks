---
description: "Repair or normalize Draw.io XML so an Azure diagram is uncompressed, reviewable and structurally valid"
agent: azure-expert-designer
---

# Repair Draw.io XML

## Inputs

- The `.drawio` file, and the validation errors or symptoms the user has seen.
- Whether overwriting the file is authorized, or the path for a repaired copy.
- Whether other documents or tools refer to cell IDs in the file.

Ask before changing the existing file. Without that approval, write a repaired copy under a new name next to it.

## Workflow

1. Record the file path, a content hash and the reported problems.
2. Apply `drawio-xml-authoring` and read its XML checklist reference before any low-level repair. Decode a compressed diagram payload into an inline `mxGraphModel`; resolve duplicate IDs, dangling parents, edges with a missing source or target, invalid geometry and unescaped labels.
3. Assign stable, semantic IDs to cells that need new ones, keep existing unique IDs, and record an old-to-new ID map.
4. Apply `azure-icons-and-visual-language`: replace legacy `mxgraph.azure` shapes with Azure2 image paths only when the product match is exact; otherwise use a neutral labeled shape and record the limitation. Set `container=0` on decorative frames, and give real subscription, resource group, VNet and subnet boundaries `container=1` with correct parentage.
5. Do not change what the diagram means. Do not add or remove services or flows. Reconnect a broken edge only when its label and geometry make the target unambiguous, and label that `inferred`. Otherwise ask the user, and if the edge cannot be resolved, leave it out of the repaired copy and list it as an unresolved risk. Record any parentage change that alters containment as a semantic correction.
6. Apply `drawio-core-generation` to confirm the output contract, then `diagram-validation-and-evidence` after the write. Apply `drawio-render-export-and-review` when Draw.io Desktop is detected.

## Expected output

- A repaired, uncompressed `.drawio` file at the approved path.
- A change log: each defect, the fix, the old-to-new ID map and any semantic corrections.
- A completion report that follows the `azure-expert-designer-contract` instruction.
