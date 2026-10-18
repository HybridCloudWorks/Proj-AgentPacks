---
name: drawio-xml-authoring
description: Author and repair reviewable uncompressed Draw.io XML with safe IDs, explicit containment, Azure2 image paths, valid edges, and no hidden structural defects.
---

# Draw.io XML Authoring

Use this Skill for direct `.drawio` XML generation, repair, normalization, or code review.

## Minimum structure

Use `mxfile` → `diagram` → `mxGraphModel` → `root`. The root must contain cells `id="0"` and `id="1"`. Every vertex has a unique ID, a parent, geometry, and a style. Every edge has a unique ID, valid `source` and `target`, a parent, and geometry. Escape XML labels and attribute values.

Use readable IDs based on stable semantic names, not random values that change on every run. Keep source and target relationships explicit. Put edge labels in child cells of the edge when the renderer requires it.

## Azure-specific XML invariants

- Use `image=img/lib/azure2/<category>/<File_Name>.svg`; do not use legacy `mxgraph.azure` or `mxgraph.azure2` shape names when the catalog supplies an image.
- Use `fontFamily=Helvetica` consistently unless the user explicitly chooses a supplied style preset.
- Parent children under real boundaries; use `container=0` for decorative regions.
- Use orthogonal edges with waypoints when a direct line would cross a boundary, label, or unrelated service.
- Keep XML uncompressed and free of illegal comments, duplicate IDs, dangling parents, missing sources, missing targets, and invalid geometry.

Read [references/xml-checklist.md](references/xml-checklist.md) before making a low-level repair.
