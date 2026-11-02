# AWS Expert Designer Pack

Portable Agent/Skill package for producing correct AWS architecture diagrams in Draw.io. The canonical source combines reusable Draw.io mechanics with AWS-specific architecture semantics, AWS4 icon rules, boundaries, patterns, layout, and evidence.

## Primary downloads

- `dist/aws-expert-designer-pack.zip` — complete source, examples, templates, tests, and archives.
- `dist/aws-expert-designer-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/aws-expert-designer-prompt.zip` — reusable pack-authoring prompt.
- `dist/aws-expert-designer-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `aws-expert-designer-skills.zip`.

## Workflows

Invoke the `aws-expert-designer` agent directly, or start from one of the seven workflow prompts in `.apm/prompts/`. Copilot installs them as prompt files and Claude Code installs them as commands. Every workflow ends with the completion report defined by the always-on `aws-expert-designer-contract` instruction.

| Prompt | Use it to |
|---|---|
| `design-aws-diagram` | design a new diagram from written requirements |
| `diagram-from-infrastructure-code` | derive a diagram from CloudFormation, CDK or Terraform, labeling observed versus inferred |
| `model-aws-architecture-pattern` | draw a VPC, serverless, container, data, hybrid, CI/CD or multi-Region pattern honestly |
| `review-aws-diagram` | review an existing diagram read-only, with located findings |
| `repair-aws-drawio-xml` | repair or normalize broken, compressed or legacy-icon XML |
| `reflow-aws-diagram-layout` | fix spacing, routing and readability, or split crowded views |
| `export-drawio-diagram` | export PNG, SVG, PDF or JPG through Draw.io Desktop and review the render |

`docs/PROMPT_INVENTORY.md` maps each prompt to its skills, outputs and worked example.

## Examples and templates

`examples/` holds six synthetic walkthroughs. Each one ends with a completion report in the contract's format. `cdk-source-blocked-workflow.md` shows a blocked, unverified outcome.

`templates/` holds the documents the workflows produce:

- diagram brief
- companion report with evidence matrices
- review findings
- export and render record
- completion report
- `aws-diagram-skeleton.drawio`, a starting file built from draw.io's AWS library styles: account, Region, VPC, two Availability Zones with public and private subnets, sample icons, Amazon S3 in the Region outside the VPC reached through an S3 gateway endpoint, an auxiliary-services frame and a legend

Templates and examples are reference material for people. They are not installed with the agent.

## Build and validate

From the pack repository root, which holds the shared tooling:

```text
python tooling/skill_coverage.py aws-expert-designer-pack
python tooling/validate_pack.py aws-expert-designer-pack --install-check
python tooling/build_pack.py aws-expert-designer-pack
```

The validator writes `VALIDATION_REPORT.md` unless it is given `--no-report`. It also runs the pack's `tests/test_drawio_assets.py`, which checks the skeleton and the test fixture with the shared checker in strict mode and fails on hand-typed boundary styles, stripped icon styles, children under a `container=0` frame, unlabelled edges, or an AWS icon outside every Region frame other than an external actor.

To check a single diagram, run the checker that ships with the shared `diagram-validation-and-evidence` skill:

```text
python aws-expert-designer-pack/.apm/skills/diagram-validation-and-evidence/scripts/check_drawio.py --strict <file.drawio>
```

It checks the XML structure, IDs, parents and edges, and matches every AWS, Azure and Google Cloud icon against draw.io's catalog; `--strict` fails legacy and retired icons as well as unknown ones. The build is deterministic and does not call AWS, Draw.io, or modify external systems. Static validation does not prove visual legibility in a renderer, live account topology, IAM effectiveness, cost behavior, or production safety.

## Rendering prerequisite

For true PNG/SVG/PDF render checks, install Draw.io Desktop: the installer, or the Microsoft Store build, whose executable is `app\draw.io.exe` inside the package folder that `Get-AppxPackage *draw.io*` reports. Without it, the pack can still run the checker above and its packaging checks, but the report must say that visual rendering was not executed.

## Design boundary

The supplied AWS files are reference material. Duplicate exports are consolidated. The current public Draw.io skill is reused as the generic foundation; the canonical pack adds AWS-specific architecture semantics, AWS4 icon rules, layout invariants, and evidence contracts instead of copying a large generic prompt into every Skill.
