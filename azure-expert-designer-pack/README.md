# Azure Expert Designer Pack

Portable Agent/Skill package for producing correct Azure architecture diagrams in Draw.io. The canonical source uses a thin routing Agent and eight focused Skills so generic Draw.io mechanics, Azure semantics, layout, XML, templates, rendering, and evidence are loaded only when relevant.

## Primary downloads

- `dist/azure-expert-designer-pack.zip` — complete source, targets, tests, tooling, and archives.
- `dist/azure-expert-designer-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/azure-expert-designer-prompt.zip` — reusable pack-authoring prompt.
- `dist/azure-expert-designer-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `azure-expert-designer-skills.zip`.

## Prompts, examples and templates

- `.apm/prompts/`: eight installed prompts, one per primary workflow. They cover designing from requirements, deriving from infrastructure source, modeling a pattern, reviewing a diagram, auditing a diagram against source, repairing XML, reflowing a layout, and exporting with a render review. `docs/PROMPT_INVENTORY.md` maps each prompt to its Skills, expected output and worked example.
- `examples/`: six worked walkthroughs, each ending with a completion report in the contract format. `export-blocked-workflow.md` shows a blocked outcome, and `terraform-derived-diagram-workflow.md` shows a partly unverified one.
- `templates/`: the documents the workflows produce: diagram brief, source inventory, companion report, review findings and completion report. It also holds `azure-diagram-skeleton.drawio`, a starting file with real subscription, resource group, VNet and subnet containers, a decorative region frame, and a legend for edge styles, boundaries and numbered badges. The skeleton uses neutral shapes only; replace each tile with an Azure2 icon (`shape=image;image=img/lib/azure2/<category>/<File_Name>.svg`) after checking the current icon catalog.

Templates and examples are pack documentation and are not installed. The installed prompts describe the documents they produce instead of pointing at these files.

## Build and validate

From this pack folder, using the tooling shared at the pack repository root:

```text
python ../tooling/validate_pack.py . --install-check
python ../tooling/build_pack.py .
```

The validator writes `VALIDATION_REPORT.md` unless `--no-report` is passed. The pack's own helper, `tooling/validate_drawio_xml.py <file.drawio>`, runs the static Draw.io checks on a single diagram.

The build is deterministic and does not call Azure, Draw.io, or modify external systems. Static validation does not prove that a diagram is visually legible in a renderer, that an Azure service relationship is deployable, or that a live architecture is secure, resilient, or cost-effective.

## Rendering prerequisite

For true PNG/SVG/PDF render checks, install Draw.io Desktop and expose its CLI executable. Without it, the pack can still perform XML, schema, icon-path, ID, parentage, edge, and packaging checks, but the report must say that visual rendering was not executed.

## Design boundary

The supplied Azure Designer files are treated as reference material. Duplicate exports are consolidated. The current public Draw.io skill is treated as the generic upstream foundation; the canonical pack adds Azure-specific architecture semantics, Azure2 icon rules, layout invariants, and evidence contracts instead of copying a large generic prompt into every Skill.
