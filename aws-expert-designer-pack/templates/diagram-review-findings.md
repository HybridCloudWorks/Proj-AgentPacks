# Diagram review findings

The record of a read-only review of an existing AWS diagram. A review changes no files. Corrections become recommendations for a follow-up workflow (repair, reflow or export), and each of those needs approval to change the source.

## Review scope

- Diagram: path, pages, and whether the payload is compressed:
- Compared against: requirements, CloudFormation, CDK, Terraform or application code, with paths:
- Purpose, audience and consumption size:
- Checks run:
  - Structural: method and result
  - Semantic: sources compared
  - Visual: renderer and version, render location (outside the source folder), size reviewed; or "not run" and the reason

## Impact scale

- **misleading**: the diagram states or implies something the evidence contradicts or does not support. Examples: a resource in the wrong subnet, false containment, a decorative group that implies network isolation, hidden replication, a hidden egress or cross-AZ path.
- **ambiguous**: a reader cannot tell what is meant. Examples: an edge that ends on a container, a missing arrowhead, an unlabeled path across a boundary.
- **structural**: a file defect that breaks opening, editing, diffing or rendering. Examples: a dangling reference, a duplicate ID, a compressed payload, a legacy or invented shape.
- **cosmetic**: a breach of convention or a readability issue only, such as font, spacing or label size.

## Findings

| ID | Page / cell ID | Finding | Evidence | Impact | Recommended correction | Blocks the stated purpose? |
|---|---|---|---|---|---|---|
|  |  |  | file:line, cell style, or render observation, with its evidence label |  |  | yes / no |

## Not reviewed

- Areas, pages or claims outside this review, and why.

## Recommended follow-up

| Finding IDs | Workflow | Approval needed |
|---|---|---|
|  | repair / reflow / export | change the existing file, or write a new file |
