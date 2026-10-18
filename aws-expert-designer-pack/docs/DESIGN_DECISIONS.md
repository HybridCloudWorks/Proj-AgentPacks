# Design Decisions

## Draw.io is the primary product

The pack is optimized for editable `.drawio` XML, not a generic architecture-writing Agent. Mermaid and other importers may accelerate standard diagrams, but custom AWS4 icons, boundaries, edge routing, and reviewable layout require native Draw.io XML or a controlled normalization step.

## Thin router plus focused Skills

The Agent contains only shared scope, evidence, safety, and routing. Generic Draw.io generation is separate from AWS semantics so a diagram task does not load every AWS pattern and icon rule.

## AWS correctness is semantic and visual

The pack checks both whether relationships are plausible and whether the drawing communicates them correctly. An account, Region, AZ, VPC, subnet, NAT gateway, endpoint, Transit Gateway, replication path, or egress edge must not be represented by a merely decorative shape.

## Source-derived diagrams have precedence

When CloudFormation, CDK, Terraform, or application code is available, the diagram starts from extracted evidence. Missing relationships are labeled as assumptions or design proposals rather than silently invented.

## Cost-bearing edges are first-class

Cross-AZ, cross-Region, internet, hybrid, and data-transfer paths should be visible when relevant. The diagram does not calculate a bill, but it makes cost-sensitive design choices reviewable.

## Static and visual evidence are separate

XML parsing, schema checks, icon namespace checks, and edge-reference checks are structural evidence. Opening or rendering in Draw.io and inspecting the result is visual evidence. Neither proves a deployed or secure AWS system.
