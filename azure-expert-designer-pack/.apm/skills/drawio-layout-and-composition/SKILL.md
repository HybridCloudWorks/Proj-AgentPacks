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

## Edges

Use orthogonal edges with clear entry and exit points. Route around boundaries and containers with waypoints; keep roughly 20 px of straight clearance from unrelated shapes. Avoid crossings, overlapping labels, parallel ambiguity, and arrows that enter a service from the wrong side. Use distinct styles for synchronous calls, asynchronous messages, replication, and control-plane relationships.

## Review loop

Start with the smallest useful diagram. After the first render, fix clipping, collisions, false containment, inconsistent icon scale, excessive whitespace, crossed edges, weak contrast, and ambiguous direction. Do not solve a crowded diagram by shrinking everything until labels are unreadable; split views or add a detail diagram when needed.
