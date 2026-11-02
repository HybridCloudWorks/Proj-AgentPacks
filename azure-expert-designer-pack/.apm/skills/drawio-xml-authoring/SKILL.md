---
name: drawio-xml-authoring
description: Author and repair reviewable uncompressed Draw.io XML with safe IDs, explicit containment, Azure2 image paths, valid edges, and no hidden structural defects.
---

# Draw.io XML Authoring

Use this Skill for direct `.drawio` XML generation, repair, normalization, or code review.

## Minimum structure

Use `mxfile` → `diagram` → `mxGraphModel` → `root`. Each page's root must contain cells `id="0"` and `id="1"`; IDs must be unique within a page, and every page of a multi-page file repeats `0` and `1`. Every vertex has a unique ID, a parent, geometry, and a style. Every edge has a unique ID, valid `source` and `target`, a parent, and geometry. Escape XML labels and attribute values.

Use readable IDs based on stable semantic names, not random values that change on every run. Keep source and target relationships explicit. Put edge labels in child cells of the edge when the renderer requires it.

## Azure-specific XML invariants

- Use only current `img/lib/azure2/<category>/<File_Name>.svg` paths from the `diagram-validation-and-evidence` catalog, in the palette's full style: `image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/<category>/<File_Name>.svg` plus its `points=[...]`. `azure2` is draw.io's ID for its current Azure library.
- Never use the legacy families: the old Azure stencils `mxgraph.azure.*`, and the Cloud & Enterprise stencils `mxgraph.mscae.*` and images `img/lib/mscae/`. The only exception is a user's explicit request to match an existing diagram; then use the legacy set consistently and record the deviation. When no current icon exists, use Microsoft's current icon download or a labelled neutral shape and record it.
- Use `fontFamily=Helvetica` consistently unless the user explicitly chooses a supplied style preset. Do not add `whiteSpace=wrap` to an icon style.
- Parent children under real boundaries (`container=1`). A decorative frame (`container=0`) never has child cells. When ownership and network disagree, follow the network: see `azure-icons-and-visual-language` and `drawio-core-generation` workflow step 4.
- Use orthogonal edges with waypoints when a direct line would cross a boundary, label, or unrelated service. Give every edge a label, and position it off frame borders as `drawio-layout-and-composition` describes.
- Keep XML uncompressed and free of illegal comments, duplicate IDs, dangling parents, missing sources, missing targets, and invalid geometry.

Read [references/xml-checklist.md](references/xml-checklist.md) before making a low-level repair, and run `diagram-validation-and-evidence`'s `scripts/check_drawio.py --strict` after every write.
