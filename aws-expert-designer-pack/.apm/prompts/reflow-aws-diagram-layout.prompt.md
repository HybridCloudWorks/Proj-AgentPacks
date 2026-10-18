---
description: "Reflow an AWS diagram's layout, edge routing and readability"
agent: aws-expert-designer
---

# Reflow an AWS diagram layout

## Inputs

The `.drawio` file; the consumption size (slide, document page, screen or print); what must stay fixed, such as page count, cell IDs or positions that other documents reference; and the output path. Changing the existing file needs explicit approval. Without it, write a new file.

## Workflow

1. Apply `aws-layout-and-composition`. Set flow direction and spacing for the service count. Keep external actors below the title block and align to 10 px. Make the account, Region, AZ, VPC and subnet hierarchy legible, and use numbered badges and a right-side legend for seven or more primary services or multiple branches.
2. Route orthogonal edges with deliberate entry and exit points, waypoints and clearance from unrelated shapes. Label synchronous, asynchronous, replication, control-plane, cross-AZ, cross-Region, hybrid and egress relationships distinctly.
3. Apply `aws-xml-authoring` to change geometry, waypoints and containment while keeping IDs stable, and keep the `drawio-core-generation` output contract: uncompressed, editable and diffable. Apply `aws-icons-and-visual-language` for a consistent icon scale.
4. Render before and after with `drawio-render-export-and-review` when Draw.io Desktop is available, and run the review loop. When a diagram is too crowded, split it into views or add a detail page rather than shrinking text until it is unreadable.
5. Apply `diagram-validation-and-evidence`, and confirm that the reflow changed no parent that carries meaning, such as a subnet, AZ or VPC.

## Expected output

The reflowed file, or files when views were split; a short account of what moved and why; and a completion report.

Follow the `aws-expert-designer-contract` instruction: report every section it lists, label evidence with its labels, and never describe an unexecuted check as passed.
