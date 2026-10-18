---
description: "Audit an existing Azure diagram against current infrastructure source and report drift"
agent: azure-expert-designer
---

# Audit a diagram against its source

## Inputs

- The `.drawio` file and the infrastructure source it is meant to reflect: Bicep, ARM, Terraform, Azure Developer CLI, Kubernetes or CI/CD definitions, with the commit or branch.
- The environment the diagram represents, and its parameter or variable files.

This is a read-only audit. Do not modify the diagram or the source. Do not query live Azure unless the user approves that specific read.

## Workflow

1. Record the diagram path and content hash, the source paths and commit, and the environment.
2. Apply `azure-architecture-design` in source-derived mode to inventory the source: resources, modules, names, regions, network references, identities and dependencies. Preserve unknown values.
3. Inventory the diagram: components, real containers, decorative frames and edges, by page and cell ID. Use the `drawio-core-generation` output contract to judge whether the file itself is structurally sound.
4. Apply `diagram-validation-and-evidence` semantic checks and match the two inventories. Classify every item as matched, in source but not on the diagram, on the diagram but not in source, placed in the wrong boundary (subscription, resource group, region, VNet or subnet), or a relationship that differs. Label the evidence for each `observed` or `inferred`, and keep anything that needs deployment evidence unresolved.
5. Apply `azure-architecture-patterns` where drift changes how a pattern reads, for example a private endpoint added in source but still drawn as a public path.
6. Treat an importer or snapshot output as evidence of its input at a point in time, not of the live environment.
7. Confirm the diagram file is unchanged at the end.

## Expected output

- A drift table with each item's classification, diagram location, source location and evidence label.
- The proposed update scope, which needs the user's approval before any edit.
- A completion report that follows the `azure-expert-designer-contract` instruction.
