# Prompt inventory

There are seven prompts, one per primary workflow, all in `.apm/prompts/` and all aimed at the `aws-expert-designer` agent. Each prompt states its inputs, the skills it applies and its expected output. Each one follows the always-on `aws-expert-designer-contract` instruction for the completion report and evidence labels. Prompts reference only installed content: skill names and that instruction.

| Prompt | Workflow | Skills applied | Expected output | Worked example |
|---|---|---|---|---|
| design-aws-diagram.prompt.md | Design from written requirements (interactive design mode) | drawio-core-generation, aws-architecture-design, aws-architecture-patterns, aws-icons-and-visual-language, aws-layout-and-composition, aws-xml-authoring, diagram-validation-and-evidence, drawio-render-export-and-review | New `.drawio`, companion report, completion report | examples/requirements-to-drawio-workflow.md |
| diagram-from-infrastructure-code.prompt.md | Reconstruction from CloudFormation, CDK or Terraform (source-derived mode) | aws-architecture-design, drawio-core-generation, aws-icons-and-visual-language, aws-layout-and-composition, aws-xml-authoring, aws-architecture-patterns, diagram-validation-and-evidence, drawio-render-export-and-review | `.drawio`, source-to-element evidence matrix, relationships needing runtime evidence, completion report | examples/terraform-derived-diagram-workflow.md, examples/cdk-source-blocked-workflow.md |
| model-aws-architecture-pattern.prompt.md | A recognizable AWS pattern drawn honestly | aws-architecture-patterns, aws-architecture-design, aws-layout-and-composition, aws-icons-and-visual-language, drawio-core-generation, aws-xml-authoring, diagram-validation-and-evidence, drawio-render-export-and-review | Pattern diagram with legend, deviations and unresolved assumptions, completion report | examples/multi-region-pattern-workflow.md |
| review-aws-diagram.prompt.md | Read-only review of an existing diagram | diagram-validation-and-evidence, drawio-core-generation, aws-xml-authoring, aws-icons-and-visual-language, aws-architecture-patterns, aws-layout-and-composition, drawio-render-export-and-review | Located findings with evidence, impact and correction; checks run; completion report | examples/diagram-review-workflow.md |
| repair-aws-drawio-xml.prompt.md | Structural repair or normalization of `.drawio` XML | aws-xml-authoring, drawio-core-generation, aws-icons-and-visual-language, aws-architecture-design, diagram-validation-and-evidence, drawio-render-export-and-review | Repaired file, change list separating meaning-preserving repairs from evidence-backed corrections, completion report | examples/repair-reflow-export-workflow.md |
| reflow-aws-diagram-layout.prompt.md | Layout, routing and readability reflow | aws-layout-and-composition, aws-xml-authoring, drawio-core-generation, aws-icons-and-visual-language, drawio-render-export-and-review, diagram-validation-and-evidence | Reflowed file or split views, before-and-after account, completion report | examples/repair-reflow-export-workflow.md |
| export-drawio-diagram.prompt.md | Export to PNG, SVG, PDF or JPG with renderer review | diagram-validation-and-evidence, drawio-core-generation, drawio-render-export-and-review, aws-layout-and-composition, aws-xml-authoring | Exports, render record, completion report; static checks only when Draw.io Desktop is absent | examples/repair-reflow-export-workflow.md |

## Skill coverage

Every skill is applied by at least one prompt. `drawio-core-generation` and `diagram-validation-and-evidence` appear in all seven, because the agent always uses them. Review and export use the core skill's output contract as the standard they check against.

| Skill | Prompts |
|---|---|
| drawio-core-generation | all seven |
| aws-architecture-design | design-aws-diagram, diagram-from-infrastructure-code, model-aws-architecture-pattern, repair-aws-drawio-xml |
| aws-architecture-patterns | design-aws-diagram, diagram-from-infrastructure-code, model-aws-architecture-pattern, review-aws-diagram |
| aws-icons-and-visual-language | all except export-drawio-diagram |
| aws-layout-and-composition | design-aws-diagram, diagram-from-infrastructure-code, model-aws-architecture-pattern, review-aws-diagram, reflow-aws-diagram-layout, export-drawio-diagram |
| aws-xml-authoring | all seven |
| diagram-validation-and-evidence | all seven |
| drawio-render-export-and-review | all seven, when Draw.io Desktop is available |

## Templates the prompts produce

The templates are not installed. They are reference forms for people and for copying into a repository.

| Template | Produced by |
|---|---|
| templates/diagram-brief.md | The framing step of every workflow |
| templates/diagram-companion-report.md | design-aws-diagram, diagram-from-infrastructure-code, model-aws-architecture-pattern, repair-aws-drawio-xml |
| templates/diagram-review-findings.md | review-aws-diagram |
| templates/export-and-render-record.md | export-drawio-diagram, plus the render step of the other workflows |
| templates/completion-report.md | Every workflow |
| templates/aws-diagram-skeleton.drawio | A starting file for design-aws-diagram and model-aws-architecture-pattern |

## How APM installs prompts

APM installs the prompts as Copilot prompt files, which honour the `agent` field, and as Claude Code commands. Claude Code drops the `agent` key with a warning, because its commands support only `description`, `input`, `allowed-tools`, `model` and `argument-hint`. At user scope (`apm install -g`), APM deploys prompts for Copilot and none for Codex. A user of a client without prompts invokes `aws-expert-designer` directly and names the workflow.
