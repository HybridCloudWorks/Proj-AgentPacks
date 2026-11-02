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
4. Apply `azure-icons-and-visual-language`: replace legacy shapes (`mxgraph.azure.*`, `mxgraph.mscae.*`, `img/lib/mscae/`) with current icons from draw.io's Azure library (`azure2`), in the palette's full style, only when the product match is exact; otherwise use a neutral labeled shape and record the limitation. Keep legacy shapes only when the user asks to match a legacy diagram.
5. Fix containment by `drawio-core-generation` workflow step 4 and the scope rules in `diagram-validation-and-evidence`'s `references/provider-checks.md`. Set `container=0` on decorative frames, and move any child of a decorative frame to the real container around it. Give VNet and subnet boundaries `container=1`, and give a subscription or resource group frame `container=1` only for cells that truly belong to it. Network containment wins: a resource whose resource group differs from its VNet's, such as a private endpoint or gateway, is parented to the subnet it is deployed into, with its resource group in its label or a decorative frame. Never leave a subnet inside a zone frame, and keep PaaS reached through a private endpoint outside the VNet.
6. Do not change what the diagram means. Do not add or remove services or flows. Reconnect a broken edge only when its label and geometry make the target unambiguous, and label that `inferred`. Otherwise ask the user, and if the edge cannot be resolved, leave it out of the repaired copy and list it as an unresolved risk. Record any parentage change that alters containment as a semantic correction.
7. Apply `drawio-core-generation` to confirm the output contract, then `diagram-validation-and-evidence` after the write, including its checker with `--strict`. Apply `drawio-render-export-and-review` when Draw.io Desktop is detected, including the Microsoft Store build that `drawio-render-export-and-review` lists; export with `-k`, never with `--layout` or `--normalize`, and with `--embed-svg-images` for SVG, and confirm that every Azure icon drew. Run `diagram-validation-and-evidence` again after the last edit.

## Expected output

- A repaired, uncompressed `.drawio` file at the approved path.
- A change log: each defect, the fix, the old-to-new ID map and any semantic corrections.
- A completion report that follows the `azure-expert-designer-contract` instruction.
