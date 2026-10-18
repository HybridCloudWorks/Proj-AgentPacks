---
description: "Reflow a crowded or hard-to-read Azure Draw.io diagram without changing what it means"
agent: azure-expert-designer
---

# Reflow a diagram layout

## Inputs

- The `.drawio` file and the readability problems the user has seen.
- How the diagram is consumed: slide, wiki page width or print size.
- Whether overwriting the file is authorized, or the path for a reflowed copy, and whether additional view pages are acceptable.

Ask before changing the existing file. Without that approval, write a reflowed copy under a new name.

## Workflow

1. Record the file path, a content hash, the number of primary services and the consumption size.
2. Apply `drawio-layout-and-composition`. Prefer left-to-right data flow and top-to-bottom governance, deployment or control-plane flow. Use about 180 px horizontal and 120 px vertical gaps between 120 px service containers, or about 220 px and 160 px for 13 or more services. Keep 30 px inside real boundaries, align to 10 px, and keep global ingress outside regional frames. Add 28 px numbered badges and a right-side legend when seven or more primary services need explanation.
3. Route edges orthogonally with waypoints and about 20 px of clearance from unrelated shapes. Remove crossings, overlapping labels and arrows that enter from the wrong side, and use distinct styles for synchronous calls, asynchronous messages, replication and control-plane relationships.
4. Do not shrink text until it is unreadable. Split into views or add a detail page instead.
5. Keep semantics fixed: the same cells, parents and edges. Moving a cell into or out of a container changes its meaning; do that only to correct false containment, and record it as a semantic change.
6. Apply `azure-icons-and-visual-language` for consistent icon scale and labels, and `drawio-xml-authoring` so cell IDs stay stable and the diff shows geometry and style changes only. Apply `drawio-core-generation` to confirm the output contract.
7. Apply `diagram-validation-and-evidence` after the write. When Draw.io Desktop is detected, apply `drawio-render-export-and-review` and repeat the review loop until the render is clean at the consumption size.

## Expected output

- A reflowed uncompressed `.drawio` file at the approved path, with any new view pages named.
- A list of layout changes and any semantic corrections.
- A completion report that follows the `azure-expert-designer-contract` instruction.
