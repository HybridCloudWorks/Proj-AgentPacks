---
name: drawio-layout-and-composition
description: Compose Azure diagrams with deterministic spacing, hierarchy, orthogonal routing, readable labels, and clear flow direction across dense architecture views.
---

# Draw.io Layout and Composition

Use this Skill for diagram layout, reflow, edge routing, visual hierarchy, or readability review.

## Layout defaults

- Prefer left-to-right data flow; use top-to-bottom for governance, deployment, or control-plane flows.
- Leave approximately 180 px horizontally and 120 px vertically between 120 px service containers. For 13 or more services, use approximately 220 px horizontally and 160 px vertically.
- Keep 30 px inside real boundaries and align major coordinates to 10 px increments.
- Place global ingress outside regional frames and regional resources inside the appropriate region. Use 28 px numbered badges plus a right-side legend when seven or more primary services need explanation.
- Size icons by `azure-icons-and-visual-language`: 48 px on the longest side with `aspect=fixed`, 24 px for scope icons in frame corners. Do not add `whiteSpace=wrap` to an icon style; break a long label with `<br>`.

## Edges

Use orthogonal edges with clear entry and exit points. Route around boundaries and containers with waypoints; keep roughly 20 px of straight clearance from unrelated shapes. Avoid crossings, overlapping labels, parallel ambiguity, and arrows that enter a service from the wrong side. Use distinct styles for synchronous calls, asynchronous messages, replication, and control-plane relationships.

Label every edge with what crosses it (protocol, transport or relationship). draw.io places an edge label at the midpoint of the whole edge, measured along every bend, not at the midpoint of its longest segment, and the midpoint of an edge that crosses nested frames often falls on a frame border. Move the label along the edge with the geometry's relative `x` (from `-1` at the source to `1` at the target), and off the line with an `<mxPoint as="offset">` child, so that it sits clear of every frame border, icon and other label. Give edge labels `labelBackgroundColor=#FFFFFF` and check their position in the render.

## Review loop

Start with the smallest useful diagram. After the first render, fix clipping, collisions, false containment, inconsistent icon scale, excessive whitespace, crossed edges, weak contrast, ambiguous direction, and edge labels that sit on a frame border. Do not solve a crowded diagram by shrinking everything until labels are unreadable; split views or add a detail diagram when needed.
