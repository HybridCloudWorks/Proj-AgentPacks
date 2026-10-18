# aws-expert-designer 1.2.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| aws-expert-designer.agent.md | Canonical agent: Create and review technically correct AWS architecture diagrams in Draw.io from requirements, CloudFormation, CDK, Terraform, and repository evidence. | .apm/agents/aws-expert-designer.agent.md |
| aws-expert-designer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the aws expert designer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/aws-expert-designer-contract.instructions.md |
| design-aws-diagram.prompt.md | Canonical prompt: Design an AWS architecture diagram in Draw.io from written requirements | .apm/prompts/design-aws-diagram.prompt.md |
| diagram-from-infrastructure-code.prompt.md | Canonical prompt: Derive an AWS architecture diagram from CloudFormation, CDK or Terraform source | .apm/prompts/diagram-from-infrastructure-code.prompt.md |
| export-drawio-diagram.prompt.md | Canonical prompt: Export a Draw.io diagram to PNG, SVG, PDF or JPG and review the rendered output | .apm/prompts/export-drawio-diagram.prompt.md |
| model-aws-architecture-pattern.prompt.md | Canonical prompt: Model a recognizable AWS architecture pattern honestly in Draw.io | .apm/prompts/model-aws-architecture-pattern.prompt.md |
| reflow-aws-diagram-layout.prompt.md | Canonical prompt: Reflow an AWS diagram's layout, edge routing and readability | .apm/prompts/reflow-aws-diagram-layout.prompt.md |
| repair-drawio-xml.prompt.md | Canonical prompt: Repair or normalize the Draw.io XML of an AWS diagram | .apm/prompts/repair-drawio-xml.prompt.md |
| review-aws-diagram.prompt.md | Canonical prompt: Review an existing AWS Draw.io diagram for structural, semantic and visual correctness | .apm/prompts/review-aws-diagram.prompt.md |
| SKILL.md | Canonical skill: Translate AWS requirements and repository evidence into an architecture model, separating observed resources, inferred relationships, design choices, and unresolved questions. | .apm/skills/aws-architecture-design/SKILL.md |
| SKILL.md | Canonical skill: Model common AWS patterns such as VPC networking, serverless, containers, event-driven systems, data platforms, hybrid connectivity, CI/CD, and multi-Region designs honestly. | .apm/skills/aws-architecture-patterns/SKILL.md |
| aws-visual-rules.md | Canonical skill | .apm/skills/aws-icons-and-visual-language/references/aws-visual-rules.md |
| SKILL.md | Canonical skill: Apply current AWS4 service and resource icons, labels, category containers, boundary styles, typography, and AWS architecture diagram conventions. | .apm/skills/aws-icons-and-visual-language/SKILL.md |
| SKILL.md | Canonical skill: Compose AWS diagrams with deterministic spacing, account and network hierarchy, orthogonal routing, readable labels, and visible cost-bearing flows. | .apm/skills/aws-layout-and-composition/SKILL.md |
| aws-xml-checklist.md | Canonical skill | .apm/skills/aws-xml-authoring/references/aws-xml-checklist.md |
| SKILL.md | Canonical skill: Author and repair reviewable uncompressed Draw.io XML with safe IDs, explicit AWS containment, valid AWS4 icon names, valid edges, and no hidden structural defects. | .apm/skills/aws-xml-authoring/SKILL.md |
| SKILL.md | Canonical skill: Validate Draw.io structure and AWS diagram evidence, then report static, rendered, live, and unresolved results without overstating what was proven. | .apm/skills/diagram-validation-and-evidence/SKILL.md |
| upstream-routing.md | Canonical skill | .apm/skills/drawio-core-generation/references/upstream-routing.md |
| SKILL.md | Canonical skill: Create and edit native Draw.io diagrams from requirements, code, structured data, or Mermaid while preserving editable XML and selecting the right generation path. | .apm/skills/drawio-core-generation/SKILL.md |
| SKILL.md | Canonical skill: Export Draw.io diagrams through the installed desktop CLI and perform a renderer-based review of labels, icons, edges, boundaries, and output legibility. | .apm/skills/drawio-render-export-and-review/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SOURCE_HASHES.md | Pack contract or inventory | docs/SOURCE_HASHES.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| cdk-source-blocked-workflow.md | Worked example | examples/cdk-source-blocked-workflow.md |
| diagram-review-workflow.md | Worked example | examples/diagram-review-workflow.md |
| multi-region-pattern-workflow.md | Worked example | examples/multi-region-pattern-workflow.md |
| repair-reflow-export-workflow.md | Worked example | examples/repair-reflow-export-workflow.md |
| requirements-to-drawio-workflow.md | Worked example | examples/requirements-to-drawio-workflow.md |
| terraform-derived-diagram-workflow.md | Worked example | examples/terraform-derived-diagram-workflow.md |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| aws-diagram-skeleton.drawio | Reusable template | templates/aws-diagram-skeleton.drawio |
| completion-report.md | Reusable template | templates/completion-report.md |
| diagram-brief.md | Reusable template | templates/diagram-brief.md |
| diagram-companion-report.md | Reusable template | templates/diagram-companion-report.md |
| diagram-review-findings.md | Reusable template | templates/diagram-review-findings.md |
| export-and-render-record.md | Reusable template | templates/export-and-render-record.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| minimal.drawio | Local test or recorded evidence | tests/fixtures/minimal.drawio |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| validate_drawio_xml.py | Pack-specific helper code | tooling/validate_drawio_xml.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-aws-expert-designer.zip: 20 files generated by `apm install --target copilot`
- claude-aws-expert-designer.zip: 20 files generated by `apm install --target claude`
- codex-aws-expert-designer.zip: 12 files generated by `apm install --target codex`
- kiro-aws-expert-designer.zip: 13 files generated by `apm install --target kiro`
- gemini-aws-expert-designer.zip: 18 files generated by `apm install --target gemini`
- agent-skills-aws-expert-designer.zip: 11 files generated by `apm install --target agent-skills`
- aws-expert-designer-canonical.zip, aws-expert-designer-prompt.zip, aws-expert-designer-validation.zip, aws-expert-designer-skills.zip, aws-expert-designer-full-pack.zip, SHA256SUMS.txt
