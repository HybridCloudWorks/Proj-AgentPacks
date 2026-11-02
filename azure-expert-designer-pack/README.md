# Azure Expert Designer Pack

Portable Agent/Skill package for producing correct Azure architecture diagrams in Draw.io. The canonical source uses a thin routing Agent and eight focused Skills so generic Draw.io mechanics, Azure semantics, layout, XML, templates, rendering, and evidence are loaded only when relevant.

## Primary downloads

- `dist/azure-expert-designer-pack.zip` — complete source, tests, and archives.
- `dist/azure-expert-designer-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/azure-expert-designer-prompt.zip` — reusable pack-authoring prompt.
- `dist/azure-expert-designer-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `azure-expert-designer-skills.zip`.

## Prompts, examples and templates

- `.apm/prompts/`: eight installed prompts, one per primary workflow. They cover designing from requirements, deriving from infrastructure source, modeling a pattern, reviewing a diagram, auditing a diagram against source, repairing XML, reflowing a layout, and exporting with a render review. `docs/PROMPT_INVENTORY.md` maps each prompt to its Skills, expected output and worked example.
- `examples/`: six worked walkthroughs, each ending with a completion report in the contract format. `export-blocked-workflow.md` shows a blocked outcome, and `terraform-derived-diagram-workflow.md` shows a partly unverified one.
- `templates/`: the documents the workflows produce: diagram brief, source inventory, companion report, review findings and completion report. It also holds `azure-diagram-skeleton.drawio`, a starting file with real subscription, resource group, VNet and subnet containers, each with its scope icon in the top-left corner labelled with the frame's name; decorative region and global-resource frames with no child cells; a private endpoint in its subnet whose resource group differs from the VNet's; a private DNS zone with a VNet link; a label on every edge; and a legend for edge styles, boundaries, placeholders and numbered badges. Replace each dashed placeholder with an icon from draw.io's Azure library (ID `azure2`), copying the palette's full style, `image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/<category>/<File_Name>.svg` plus its `points`, at 48 px on the longest side, after checking that the path is current in the shared icon catalog. `drawio-core-generation`'s `references/providers.md` describes the library.

Templates and examples are pack documentation and are not installed. The installed prompts describe the documents they produce instead of pointing at these files.

## Build and validate

From this pack folder, using the tooling shared at the pack repository root:

```text
python ../tooling/validate_pack.py . --install-check
python ../tooling/build_pack.py .
```

The validator writes `VALIDATION_REPORT.md` unless `--no-report` is passed.

To check a single diagram, run the shared checker that ships in the `diagram-validation-and-evidence` Skill:

```text
python .apm/skills/diagram-validation-and-evidence/scripts/check_drawio.py --strict <file.drawio>
```

It checks the page layout, compression, root cells, IDs per page, parents, edges and geometry, and reports every AWS, Azure and Google Cloud icon as current, legacy, retired or unknown against its catalog of draw.io's libraries. `--strict` turns legacy and retired icons into errors. `templates/azure-diagram-skeleton.drawio` and `tests/fixtures/minimal.drawio` pass it. The pack no longer ships its own Draw.io helper.

The build is deterministic and does not call Azure, Draw.io, or modify external systems. Static validation does not prove that a diagram is visually legible in a renderer, that an Azure service relationship is deployable, or that a live architecture is secure, resilient, or cost-effective.

## Rendering prerequisite

For true PNG/SVG/PDF render checks, Draw.io Desktop must be installed. It does not need to be on PATH: the `drawio-render-export-and-review` Skill also looks in the installer and per-user locations and finds the Microsoft Store build, whose executable is `app\draw.io.exe` inside the folder that `Get-AppxPackage *draw.io*` reports. Exports pass `-k`, SVG exports pass `--embed-svg-images`, and review exports never use `--layout` or `--normalize`. Without a renderer, the pack can still perform XML, schema, icon-catalog, ID, parentage, edge, and packaging checks, but the report must say that visual rendering was not executed.

## Design boundary

The supplied Azure Designer files are treated as reference material. Duplicate exports are consolidated. The current public Draw.io skill is treated as the generic upstream foundation; the canonical pack adds Azure-specific architecture semantics, Azure icon house style, layout invariants, and evidence contracts instead of copying a large generic prompt into every Skill.
