# AWS Expert Designer Pack

Portable Agent/Skill package for producing correct AWS architecture diagrams in Draw.io. The canonical source combines reusable Draw.io mechanics with AWS-specific architecture semantics, AWS4 icon rules, boundaries, patterns, layout, and evidence.

## Primary downloads

- `dist/aws-expert-designer-pack.zip` — complete source, examples, templates, tests, tooling, and archives.
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
| `repair-drawio-xml` | repair or normalize broken, compressed or legacy-icon XML |
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
- `aws-diagram-skeleton.drawio`, a starting file with AWS boundary conventions

Templates and examples are reference material for people. They are not installed with the agent.

## Build and validate

From the pack repository root, which holds the shared tooling:

```text
python tooling/skill_coverage.py aws-expert-designer-pack
python tooling/validate_pack.py aws-expert-designer-pack --install-check
python tooling/build_pack.py aws-expert-designer-pack
```

The validator writes `VALIDATION_REPORT.md` unless it is given `--no-report`. The pack's own helper, `tooling/validate_drawio_xml.py <file.drawio>`, runs static checks on a single diagram.

The build is deterministic and does not call AWS, Draw.io, or modify external systems. Static validation does not prove visual legibility in a renderer, live account topology, IAM effectiveness, cost behavior, or production safety.

## Rendering prerequisite

For true PNG/SVG/PDF render checks, install Draw.io Desktop and expose its CLI executable. Without it, the pack can still perform XML, shape, icon namespace, ID, parentage, edge, and packaging checks, but the report must say that visual rendering was not executed.

## Design boundary

The supplied AWS files are reference material. Duplicate exports are consolidated. The current public Draw.io skill is reused as the generic foundation; the canonical pack adds AWS-specific architecture semantics, AWS4 icon rules, layout invariants, and evidence contracts instead of copying a large generic prompt into every Skill.
