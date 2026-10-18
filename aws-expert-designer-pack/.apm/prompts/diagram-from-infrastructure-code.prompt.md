---
description: "Derive an AWS architecture diagram from CloudFormation, CDK or Terraform source"
agent: aws-expert-designer
---

# Derive an AWS diagram from infrastructure code

## Inputs

The repository paths that hold the CloudFormation templates, CDK app or Terraform configuration; the stacks, modules, environments or workspaces in scope; any existing diagram the result must replace or match; and the audience and output path. Read the source before asking anything, and ask only about scope the files cannot settle.

## Workflow

1. Apply `aws-architecture-design` in source-derived mode and inventory the files before drawing.
   - CloudFormation: resource types, `Ref`, `Fn::GetAtt`, `DependsOn`, parameters, mappings and nested stacks.
   - CDK: use synthesized output when it is available; otherwise read the constructs and label the logical-to-physical mapping as uncertain.
   - Terraform: AWS resources, modules, providers, references, outputs and backend context.
   Preserve unknown values such as parameters without defaults, variable-driven counts and lookups. Mark each relationship observed, inferred or designed. A declared resource does not prove runtime traffic, DNS, IAM authorization, routing or data flow.
2. Apply `drawio-core-generation` to choose the generation path: native XML for AWS4 icons and precise boundaries; an installed importer or a controlled extraction as a starting point; structured generation with autolayout for large graphs, followed by AWS normalization.
3. Apply `aws-icons-and-visual-language`, `aws-layout-and-composition` and `aws-xml-authoring`. Derive cell IDs from logical IDs or resource addresses, normalized to safe characters, so a later regeneration diffs cleanly.
4. Apply `aws-architecture-patterns` when the source implements a recognizable pattern, and record where it deviates.
5. Apply `diagram-validation-and-evidence` as a source-to-diagram audit: every component and edge traces to a file location or carries an explicit label.
6. Apply `drawio-render-export-and-review` when Draw.io Desktop is available.

Ask before any step that needs AWS credentials, such as a CDK context lookup that is not cached, a Terraform plan against remote state, or a live account snapshot. Ask before changing an existing diagram; otherwise write a new file.

## Expected output

A `.drawio` file; a companion report that maps each component and relationship to its source location and evidence label; the relationships that still need deployment, CloudTrail, AWS Config or runtime evidence; and a completion report.

Follow the `aws-expert-designer-contract` instruction: report every section it lists, label evidence with its labels, and never describe an unexecuted check as passed.
