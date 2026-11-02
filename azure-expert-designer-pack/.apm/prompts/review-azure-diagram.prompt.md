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
2. Apply `diagram-validation-and-evidence` step 1: run its checker, `scripts/check_drawio.py --strict`, and record the catalog version and the Azure icon summary it prints. Use the `drawio-core-generation` output contract and the `drawio-xml-authoring` XML checklist as the yardstick for what the checker cannot see: fonts, container styles, cells parented to `container=0` frames, and unlabelled edges.
3. Apply `diagram-validation-and-evidence` step 2 and the scope-rule table in its `references/provider-checks.md`, with `drawio-core-generation` workflow step 4 as the rule source, to check boundaries:
   - each VNet sits inside exactly one region frame;
   - no subnet sits inside a zone frame, and zone-redundant resources are labelled with their zones rather than drawn in zone frames;
   - PaaS reached through a private endpoint is outside the VNet, with only the endpoint NIC in the subnet, and App Service with regional VNet integration is outside the VNet with an outbound edge into its delegated subnet;
   - a resource whose resource group differs from its VNet's is parented to the network boundary it is deployed into, with its resource group in its label or a decorative frame;
   - ownership scopes are not drawn as network boundaries, and governance scopes are not drawn as packet paths.
   Then apply `azure-architecture-design`: subscriptions, resource groups, regions, zones, VNets, subnets, governance scopes and data boundaries must stay distinct, and no relationship may be drawn more strongly than the evidence supports.
4. Apply `azure-architecture-patterns` to check that each pattern is represented honestly, for example a private endpoint NIC in its subnet, private DNS resolution, and the PaaS target outside the VNet.
5. Apply `azure-icons-and-visual-language` for legacy shapes, distorted or substituted icons, missing product labels, product icons used for custom components, and decorative frames that imply isolation.
6. Apply `drawio-layout-and-composition` for clipping, collisions, crossings, ambiguous arrow direction and false containment.
7. If a rendered check is needed and Draw.io Desktop is detected, including the Microsoft Store build that `drawio-render-export-and-review` lists, apply that skill and export only to a scratch location outside the repository; export with `-k`, never with `--layout` or `--normalize`, and with `--embed-svg-images` for SVG. Confirm that every Azure icon drew and none shows a broken-image placeholder. Otherwise state that visual checks were not run.
8. Close with `diagram-validation-and-evidence` steps 4 and 5, so the visual results from the render sit beside the checker's results in one report.
9. Confirm the reviewed file is unchanged at the end.

## Expected output

- Prioritized findings, each with severity, page and cell ID, category, the evidence and its label, the impact on a reader, and a recommended fix.
- The checks run and not run, with the checker's catalog version and icon summary, and the limits of the review.
- A completion report that follows the `azure-expert-designer-contract` instruction. Any fix is a separate edit that needs the user's approval.
