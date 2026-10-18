# azure-expert-designer 1.2.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| azure-expert-designer.agent.md | Canonical agent: Create and review technically correct Azure architecture diagrams in Draw.io from requirements, source code, infrastructure definitions, and repository evidence. | .apm/agents/azure-expert-designer.agent.md |
| azure-expert-designer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the azure expert designer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/azure-expert-designer-contract.instructions.md |
| audit-diagram-against-source.prompt.md | Canonical prompt: Audit an existing Azure diagram against current infrastructure source and report drift | .apm/prompts/audit-diagram-against-source.prompt.md |
| derive-diagram-from-infrastructure.prompt.md | Canonical prompt: Derive an Azure diagram from Bicep, ARM, Terraform, Azure Developer CLI or Kubernetes source | .apm/prompts/derive-diagram-from-infrastructure.prompt.md |
| design-diagram-from-requirements.prompt.md | Canonical prompt: Design an editable Azure architecture diagram in Draw.io from written requirements | .apm/prompts/design-diagram-from-requirements.prompt.md |
| export-and-review-render.prompt.md | Canonical prompt: Export a Draw.io diagram to PNG, SVG, PDF or JPG and review the rendered output | .apm/prompts/export-and-review-render.prompt.md |
| model-azure-architecture-pattern.prompt.md | Canonical prompt: Model a recognizable Azure architecture pattern in Draw.io without misleading flows | .apm/prompts/model-azure-architecture-pattern.prompt.md |
| reflow-diagram-layout.prompt.md | Canonical prompt: Reflow a crowded or hard-to-read Azure Draw.io diagram without changing what it means | .apm/prompts/reflow-diagram-layout.prompt.md |
| repair-drawio-xml.prompt.md | Canonical prompt: Repair or normalize Draw.io XML so an Azure diagram is uncompressed, reviewable and structurally valid | .apm/prompts/repair-drawio-xml.prompt.md |
| review-azure-diagram.prompt.md | Canonical prompt: Review an existing Azure Draw.io diagram for semantic, boundary, icon, layout and structural correctness | .apm/prompts/review-azure-diagram.prompt.md |
| SKILL.md | Canonical skill: Translate Azure requirements and repository evidence into an architecture model, separating observed resources, inferred relationships, design choices, and unresolved questions. | .apm/skills/azure-architecture-design/SKILL.md |
| SKILL.md | Canonical skill: Model common Azure architecture patterns such as private networking, AKS, serverless, analytics, CI/CD, landing zones, hybrid connectivity, and multi-region designs without misleading flows. | .apm/skills/azure-architecture-patterns/SKILL.md |
| azure-visual-rules.md | Canonical skill | .apm/skills/azure-icons-and-visual-language/references/azure-visual-rules.md |
| SKILL.md | Canonical skill: Apply official Azure2 icons, labels, boundary styles, typography, and visual conventions without distorting service meaning or implying false isolation. | .apm/skills/azure-icons-and-visual-language/SKILL.md |
| SKILL.md | Canonical skill: Validate Draw.io structure and Azure diagram evidence, then report static, rendered, live, and unresolved results without overstating what was proven. | .apm/skills/diagram-validation-and-evidence/SKILL.md |
| upstream-routing.md | Canonical skill | .apm/skills/drawio-core-generation/references/upstream-routing.md |
| SKILL.md | Canonical skill: Create and edit native Draw.io diagrams from requirements, code, structured data, or Mermaid while preserving editable XML and selecting the right generation path. | .apm/skills/drawio-core-generation/SKILL.md |
| SKILL.md | Canonical skill: Compose Azure diagrams with deterministic spacing, hierarchy, orthogonal routing, readable labels, and clear flow direction across dense architecture views. | .apm/skills/drawio-layout-and-composition/SKILL.md |
| SKILL.md | Canonical skill: Export Draw.io diagrams through the installed desktop CLI and perform a renderer-based review of labels, icons, edges, boundaries, and output legibility. | .apm/skills/drawio-render-export-and-review/SKILL.md |
| xml-checklist.md | Canonical skill | .apm/skills/drawio-xml-authoring/references/xml-checklist.md |
| SKILL.md | Canonical skill: Author and repair reviewable uncompressed Draw.io XML with safe IDs, explicit containment, Azure2 image paths, valid edges, and no hidden structural defects. | .apm/skills/drawio-xml-authoring/SKILL.md |
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
| export-blocked-workflow.md | Worked example | examples/export-blocked-workflow.md |
| multi-region-pattern-workflow.md | Worked example | examples/multi-region-pattern-workflow.md |
| private-endpoint-review-workflow.md | Worked example | examples/private-endpoint-review-workflow.md |
| requirements-to-drawio-workflow.md | Worked example | examples/requirements-to-drawio-workflow.md |
| terraform-derived-diagram-workflow.md | Worked example | examples/terraform-derived-diagram-workflow.md |
| xml-repair-and-reflow-workflow.md | Worked example | examples/xml-repair-and-reflow-workflow.md |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| azure-diagram-skeleton.drawio | Reusable template | templates/azure-diagram-skeleton.drawio |
| completion-report.md | Reusable template | templates/completion-report.md |
| diagram-brief.md | Reusable template | templates/diagram-brief.md |
| diagram-companion-report.md | Reusable template | templates/diagram-companion-report.md |
| diagram-review-findings.md | Reusable template | templates/diagram-review-findings.md |
| source-inventory.md | Reusable template | templates/source-inventory.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| minimal.drawio | Local test or recorded evidence | tests/fixtures/minimal.drawio |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| validate_drawio_xml.py | Pack-specific helper code | tooling/validate_drawio_xml.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-azure-expert-designer.zip: 21 files generated by `apm install --target copilot`
- claude-azure-expert-designer.zip: 21 files generated by `apm install --target claude`
- codex-azure-expert-designer.zip: 12 files generated by `apm install --target codex`
- kiro-azure-expert-designer.zip: 13 files generated by `apm install --target kiro`
- gemini-azure-expert-designer.zip: 19 files generated by `apm install --target gemini`
- agent-skills-azure-expert-designer.zip: 11 files generated by `apm install --target agent-skills`
- azure-expert-designer-canonical.zip, azure-expert-designer-prompt.zip, azure-expert-designer-validation.zip, azure-expert-designer-skills.zip, azure-expert-designer-full-pack.zip, SHA256SUMS.txt
