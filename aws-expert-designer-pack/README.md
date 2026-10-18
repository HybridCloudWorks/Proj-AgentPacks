# AWS Expert Designer Pack

Portable Agent/Skill package for producing correct AWS architecture diagrams in Draw.io. The canonical source combines reusable Draw.io mechanics with AWS-specific architecture semantics, AWS4 icon rules, boundaries, patterns, layout, and evidence.

## Primary downloads

- `dist/aws-expert-designer-pack.zip` — complete source, targets, tests, tooling, and archives.
- `dist/aws-expert-designer-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/aws-expert-designer-prompt.zip` — reusable pack-authoring prompt.
- `dist/aws-expert-designer-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `aws-expert-designer-skills.zip`.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
```

The build is deterministic and does not call AWS, Draw.io, or modify external systems. Static validation does not prove visual legibility in a renderer, live account topology, IAM effectiveness, cost behavior, or production safety.

## Rendering prerequisite

For true PNG/SVG/PDF render checks, install Draw.io Desktop and expose its CLI executable. Without it, the pack can still perform XML, shape, icon namespace, ID, parentage, edge, and packaging checks, but the report must say that visual rendering was not executed.

## Design boundary

The supplied AWS files are reference material. Duplicate exports are consolidated. The current public Draw.io skill is reused as the generic foundation; the canonical pack adds AWS-specific architecture semantics, AWS4 icon rules, layout invariants, and evidence contracts instead of copying a large generic prompt into every Skill.
