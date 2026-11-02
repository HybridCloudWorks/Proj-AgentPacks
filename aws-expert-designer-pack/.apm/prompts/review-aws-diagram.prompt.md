---
description: "Review an existing AWS Draw.io diagram for structural, semantic and visual correctness"
agent: aws-expert-designer
---

# Review an AWS diagram

## Inputs

The `.drawio` file; its intended purpose, audience and consumption size; and, when available, the requirements or infrastructure code it should match. The review is read-only unless the user asks for changes.

## Workflow

1. Apply `diagram-validation-and-evidence`, judging the file against the `drawio-core-generation` output contract.
   - Structural checks: run `check_drawio.py`, with `--strict` unless the user wants the diagram to keep a legacy icon set, and report every legacy, retired or unknown icon as a finding. The `mxgraph.aws4` namespace alone does not prove that an icon is current. Also check root structure, unique IDs, parent, source and target references, geometry, compression, safe labels, font and container styles, and orphaned or hidden cells.
   - Semantic checks against the supplied requirements or source.
2. Apply `aws-xml-authoring` and its checklist reference for low-level defects. Apply `aws-icons-and-visual-language` for legacy shapes, invented icon names, recoloured or hand-typed boundary styles, icons parented to category tiles, and AWS product icons used for non-AWS components.
3. Apply `aws-architecture-patterns` to judge whether the pattern is represented honestly, including false containment, decorative groups that imply network isolation, and nesting other than account > Region > VPC > Availability Zone > subnet.
4. Apply `aws-layout-and-composition` for readability: clipping, collisions, crossed edges, ambiguous direction and hidden cost-bearing paths.
5. Apply `drawio-render-export-and-review` when Draw.io Desktop is available, including the Microsoft Store build, and write review renders outside the source folder.
6. Complete `diagram-validation-and-evidence` with the visual checks, run only on an output that was actually opened or rendered.

A compressed diagram may be decoded in memory for inspection; do not rewrite the source.

## Expected output

Findings located by page and cell ID. Each finding gives the evidence, its impact on interpretation (misleading, ambiguous, structural or cosmetic), the recommended correction, and whether it blocks the diagram's stated purpose. Then the checks actually run and their limits, the follow-up workflow recommended for each correction, and a completion report. Do not edit, overwrite or publish the diagram without explicit approval.

Follow the `aws-expert-designer-contract` instruction: report every section it lists, label evidence with its labels, and never describe an unexecuted check as passed.
