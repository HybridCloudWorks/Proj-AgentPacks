# Azure Expert Designer Pack

Portable Agent/Skill package for producing correct Azure architecture diagrams in Draw.io. The canonical source uses a thin routing Agent and eight focused Skills so generic Draw.io mechanics, Azure semantics, layout, XML, templates, rendering, and evidence are loaded only when relevant.

## Primary downloads

- `dist/azure-expert-designer-pack.zip` — complete source, targets, tests, tooling, and archives.
- `dist/azure-expert-designer-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/azure-expert-designer-prompt.zip` — reusable pack-authoring prompt.
- `dist/azure-expert-designer-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `azure-expert-designer-skills.zip`.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
```

The build is deterministic and does not call Azure, Draw.io, or modify external systems. Static validation does not prove that a diagram is visually legible in a renderer, that an Azure service relationship is deployable, or that a live architecture is secure, resilient, or cost-effective.

## Rendering prerequisite

For true PNG/SVG/PDF render checks, install Draw.io Desktop and expose its CLI executable. Without it, the pack can still perform XML, schema, icon-path, ID, parentage, edge, and packaging checks, but the report must say that visual rendering was not executed.

## Design boundary

The supplied Azure Designer files are treated as reference material. Duplicate exports are consolidated. The current public Draw.io skill is treated as the generic upstream foundation; the canonical pack adds Azure-specific architecture semantics, Azure2 icon rules, layout invariants, and evidence contracts instead of copying a large generic prompt into every Skill.
