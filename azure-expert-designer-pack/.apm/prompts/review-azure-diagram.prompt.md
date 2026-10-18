---
description: "Review an existing Azure Draw.io diagram for semantic, boundary, icon, layout and structural correctness"
agent: azure-expert-designer
---

# Review an Azure diagram

## Inputs

- The `.drawio` file to review, and any exported image the audience sees.
- What the diagram claims to represent: requirements, infrastructure source or a named pattern.
- The review focus, if any, such as private connectivity, identity, resilience or readability.

This is a read-only review. Do not modify the diagram, its exports or the source files.

## Workflow

1. Record the diagram path, a content hash, the reference sources and the review focus.
2. Apply `diagram-validation-and-evidence` structural checks, using the `drawio-core-generation` output contract and the `drawio-xml-authoring` XML checklist as the yardstick: parsing, root cells, unique IDs, parents, edge sources and targets, geometry, compression, Azure2 image paths, fonts, container styles, and orphaned or hidden cells.
3. Apply `azure-architecture-design` to check boundaries: subscriptions, resource groups, regions, zones, VNets, subnets, governance scopes and data boundaries must stay distinct, and no relationship may be drawn more strongly than the evidence supports.
4. Apply `azure-architecture-patterns` to check that each pattern is represented honestly, for example a private endpoint NIC in its subnet, private DNS resolution, and the PaaS target outside the subnet.
5. Apply `azure-icons-and-visual-language` for legacy shapes, distorted or substituted icons, missing product labels, product icons used for custom components, and decorative frames that imply isolation.
6. Apply `drawio-layout-and-composition` for clipping, collisions, crossings, ambiguous arrow direction and false containment.
7. If a rendered check is needed and Draw.io Desktop is detected, apply `drawio-render-export-and-review` and export only to a scratch location outside the repository. Otherwise state that visual checks were not run.
8. Confirm the reviewed file is unchanged at the end.

## Expected output

- Prioritized findings, each with severity, page and cell ID, category, the evidence and its label, the impact on a reader, and a recommended fix.
- The checks run and not run, and the limits of the review.
- A completion report that follows the `azure-expert-designer-contract` instruction. Any fix is a separate edit that needs the user's approval.
