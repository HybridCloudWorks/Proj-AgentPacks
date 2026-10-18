---
description: "Design an AWS architecture diagram in Draw.io from written requirements"
agent: aws-expert-designer
---

# Design an AWS architecture diagram from requirements

## Inputs

The user's requirements or design notes; the diagram's purpose, audience and output location; and any stated constraints on accounts, Regions, availability, data sensitivity, traffic, connectivity, identity and scale. Take from the text whatever it already settles. Ask only the questions that change the architecture or the visual scope; record everything else as an assumption and continue.

## Workflow

1. Apply `drawio-core-generation` to fix purpose, audience, scope, fidelity, output path and generation path. Native XML is the default when AWS4 icons, custom boundaries or precise edge routing matter.
2. Apply `aws-architecture-design` in interactive design mode. Build the model: Organization, OU and account; Region and Availability Zone; VPC, subnets, ingress and egress; compute, data, messaging, identity, secrets and observability. Mark every relationship observed (stated by the user), inferred or designed. Offer a minimal architecture with optional security, reliability, observability and governance layers rather than drawing every possible service.
3. Apply `aws-architecture-patterns` when the design follows a recognizable pattern, and record where it deviates.
4. Apply `aws-icons-and-visual-language` for AWS4 icons, product labels, category containers and boundary styles. Use general icons for non-AWS systems and record any approximate mapping.
5. Apply `aws-layout-and-composition` for flow direction, spacing, hierarchy, numbered steps and the legend, and to keep cross-AZ, cross-Region, hybrid and egress paths visible.
6. Apply `aws-xml-authoring` to write uncompressed XML with stable semantic IDs and real containment for VPC, Availability Zone and subnet.
7. Apply `diagram-validation-and-evidence` after every write. Apply `drawio-render-export-and-review` when Draw.io Desktop is available.

## Expected output

A new `.drawio` file at the agreed path; a companion report with the model, evidence labels, design decisions, legend notes and unresolved questions; and a completion report. Do not overwrite or change an existing diagram without explicit approval.

Follow the `aws-expert-designer-contract` instruction: report every section it lists, label evidence with its labels, and never describe an unexecuted check as passed.
