---
name: aws-xml-authoring
description: Author and repair reviewable uncompressed Draw.io XML with safe IDs, explicit AWS containment, valid AWS4 icon names, valid edges, and no hidden structural defects.
---

# AWS Draw.io XML Authoring

Use this Skill for direct `.drawio` XML generation, repair, normalization, or code review.

## Minimum structure

Use `mxfile` → `diagram` → `mxGraphModel` → `root`. The root must contain cells `id="0"` and `id="1"`. Every vertex has a unique ID, a parent, geometry, and a style. Every edge has a unique ID, a parent, and valid `source` and `target` references. Escape XML labels and attribute values.

Use readable IDs based on stable semantic names, not random values that change on every run. Keep source and target relationships explicit. Put edge labels in child cells of the edge when the renderer requires it.

## AWS-specific XML invariants

- Use valid `mxgraph.aws4.*` and `resIcon=mxgraph.aws4.*` styles from the installed/current AWS4 catalog.
- Main AWS service icons use `resourceIcon;resIcon=`; category containers carry category labels, not duplicated service names.
- Use `fontFamily=Helvetica` consistently unless the user explicitly chooses sketch mode.
- Parent children under real VPC/AZ/subnet boundaries; use `container=0` for decorative Region or account frames when appropriate.
- Edges connect to service/resource icons, not only to containers. Use `exitX`, `exitY`, `entryX`, and `entryY` deliberately.
- Use orthogonal edges with waypoints when a direct line would cross a boundary, label, or unrelated service. Do not hide cross-AZ, cross-Region, hybrid, or egress edges.

Read [references/aws-xml-checklist.md](references/aws-xml-checklist.md) before making a low-level repair.
