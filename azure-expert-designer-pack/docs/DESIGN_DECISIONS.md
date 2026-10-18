# Design Decisions

## Draw.io is the primary product

The pack is optimized for editable `.drawio` XML, not a generic architecture-writing Agent. Mermaid and other importers may accelerate standard diagrams, but custom Azure icons, boundaries, edge routing, and reviewable layout require native Draw.io XML or a controlled post-processing step.

## Thin router plus focused Skills

The Agent contains only shared scope, evidence, safety, and routing. Generic Draw.io generation is separate from Azure semantics so a diagram task does not load every Azure pattern and icon rule.

## Azure correctness is semantic and visual

The pack checks both whether relationships are plausible and whether the drawing communicates them correctly. A private endpoint, subnet, region, zone, Front Door path, governance scope, or identity relationship must not be represented by a merely decorative shape.

## Source-derived diagrams have precedence

When Bicep, ARM, Terraform, Azure Developer CLI, Kubernetes, workflows, or application code is available, the diagram starts from extracted evidence. Missing relationships are labeled as assumptions or design proposals rather than silently invented.

## Static and visual evidence are separate

XML parsing, schema checks, icon-path checks, and edge-reference checks are structural evidence. Opening or rendering in Draw.io and inspecting the result is visual evidence. Neither proves a deployed or secure Azure system.

## Upstream Draw.io material is not duplicated

The current public Draw.io skill is recorded as an upstream dependency and its generic mechanics are distilled into `drawio-core-generation` and `drawio-render-export-and-review`. Azure-specific content is maintained in this pack.
