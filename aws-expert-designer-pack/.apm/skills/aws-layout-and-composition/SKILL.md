---
name: aws-layout-and-composition
description: Compose AWS diagrams with deterministic spacing, account and network hierarchy, orthogonal routing, readable labels, and visible cost-bearing flows.
---

# AWS Layout and Composition

Use this Skill for diagram layout, reflow, edge routing, visual hierarchy, or readability review.

## Layout defaults

- Prefer left-to-right request/data flow; use top-to-bottom for governance, deployment, or control-plane flows.
- Give each service a 120 px slot: a 48x48 icon with its label, or an optional decorative category tile. Leave approximately 180 px horizontally and 120 px vertically between slots. For 13 or more services, use approximately 220 px horizontally and 160 px vertically.
- Keep external actors below the title block, usually at y >= 140. Align major coordinates to 10 px increments.
- Make the account > Region > VPC > Availability Zone > subnet hierarchy legible, nested in that order, with each subnet inside exactly one Availability Zone frame. Do not nest by service category. A flat layout may group services, but never changes subnet or Availability Zone placement.
- Use teal 28x28 numbered badges near primary flow sources and a right-side legend for seven or more primary services or multiple branches. Auxiliary services do not need step numbers unless they are part of the requested flow.

## Edges and cost visibility

Use orthogonal edges with clear entry and exit points. Route around boundaries and containers with waypoints; keep roughly 20 px of straight clearance from unrelated shapes. Avoid crossings, overlapping labels, parallel ambiguity, and arrows that enter a service from the wrong side. Label synchronous calls, asynchronous messages, replication, control-plane, cross-AZ, cross-Region, hybrid, and egress relationships distinctly when they affect interpretation.

## Review loop

Start with the smallest useful diagram. After the first render, fix clipping, collisions, false containment, inconsistent icon scale, excessive whitespace, crossed edges, weak contrast, and ambiguous direction. Do not solve a crowded diagram by shrinking everything until labels are unreadable; split views or add a detail diagram when needed.
