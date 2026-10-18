---
description: "Repair or normalize the Draw.io XML of an AWS diagram"
agent: aws-expert-designer
---

# Repair Draw.io XML

## Inputs

The `.drawio` file; the symptoms, such as a file that does not open, missing or dangling edges, a compressed payload, legacy or invented AWS shapes, or broken containment; and where to write the result. Repairing in place overwrites a source file and needs explicit approval. Without that approval, write a new file beside the original.

## Workflow

1. Apply `aws-xml-authoring` and read its checklist reference before making any low-level repair. The repaired file needs `mxfile`, `diagram`, `mxGraphModel`, `root` and cells `0` and `1`, unique stable IDs, resolvable parents, edges with existing sources and targets, and escaped labels.
2. Apply `drawio-core-generation` for the output contract: uncompressed, diffable and editable.
3. Apply `aws-icons-and-visual-language` to replace legacy or invented shapes with valid AWS4 names from the installed library. Where no valid name exists, use a neutral labeled shape. Record every approximate mapping.
4. Keep every existing ID that is valid, so the change diffs cleanly. Separate repairs that preserve meaning from corrections that change what the diagram claims. A correction needs evidence under `aws-architecture-design` and is recorded as a decision.
5. Apply `diagram-validation-and-evidence`, and `drawio-render-export-and-review` when Draw.io Desktop is available.

## Expected output

The repaired file; a change list giving, for each change, the cell ID, the defect, the repair, and whether the meaning changed and on what evidence; and a completion report.

Follow the `aws-expert-designer-contract` instruction: report every section it lists, label evidence with its labels, and never describe an unexecuted check as passed.
