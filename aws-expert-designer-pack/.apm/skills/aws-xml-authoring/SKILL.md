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

- Copy every AWS icon and group style whole from draw.io's current AWS library, as `drawio-core-generation` describes, and keep its category `fillColor`, `strokeColor` and bottom label position. Service icons are `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<name>`, resource icons `shape=mxgraph.aws4.<resource>`, and groups `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.<group>`. Never write AWS18 `productIcon` or `prIcon`, `mxgraph.aws3.*` or `mxgraph.aws3d.*` styles for new work.
- Nest account > Region > VPC > Availability Zone > subnet as real containers, with each subnet parented to exactly one Availability Zone, and parent every resource to the boundary it really sits in.
- Library group styles carry `container=1`. A frame used decoratively must set `container=0` explicitly, and no cell may be parented to a `container=0` cell. The library's Availability Zone rectangle has no `container=1`; add `container=1;collapsible=0;recursiveResize=0` before parenting subnets to it.
- Category tiles, when the house style uses them, are `container=0` siblings placed before their icon, never parents.
- Use `fontFamily=Helvetica` consistently unless the user explicitly chooses sketch mode. Typography is the only part of a library style the pack changes.
- Edges connect to service or resource icons, never to boundaries or tiles. Use `exitX`, `exitY`, `entryX`, and `entryY` deliberately.
- Use orthogonal edges with waypoints when a direct line would cross a boundary, label, or unrelated service. Do not hide cross-AZ, cross-Region, hybrid, or egress edges.
- After every write, run `check_drawio.py --strict` from `diagram-validation-and-evidence`. Use the default mode only when the user asked to keep a legacy icon set to match an existing diagram, and report its warnings.

Read [references/aws-xml-checklist.md](references/aws-xml-checklist.md) before making a low-level repair.
