# Prompt inventory

One prompt per primary workflow. Every prompt targets the `azure-expert-designer` agent, names the Skills it applies, and ends by following the always-on `azure-expert-designer-contract` instruction. Prompts reference only installed content: Skills, their reference files, and the contract instruction.

| Prompt | Workflow | Skills applied | Expected output | Worked example |
|---|---|---|---|---|
| `design-diagram-from-requirements.prompt.md` | Design from written requirements | azure-architecture-design, azure-architecture-patterns, drawio-core-generation, azure-icons-and-visual-language, drawio-layout-and-composition, drawio-xml-authoring, diagram-validation-and-evidence, drawio-render-export-and-review | New `.drawio`, companion report with evidence labels and decisions, completion report | `examples/requirements-to-drawio-workflow.md` |
| `derive-diagram-from-infrastructure.prompt.md` | Reconstruct from Bicep, ARM, Terraform, azd or Kubernetes | azure-architecture-design, drawio-core-generation, azure-icons-and-visual-language, drawio-layout-and-composition, drawio-xml-authoring, azure-architecture-patterns, diagram-validation-and-evidence, drawio-render-export-and-review | New `.drawio` traced to source, source inventory, evidence matrix, completion report | `examples/terraform-derived-diagram-workflow.md` |
| `model-azure-architecture-pattern.prompt.md` | Model a recognizable pattern honestly | azure-architecture-patterns, azure-architecture-design, drawio-layout-and-composition, azure-icons-and-visual-language, drawio-core-generation, drawio-xml-authoring, diagram-validation-and-evidence, drawio-render-export-and-review | New `.drawio` with routing, replication, failover and active/passive semantics; deviations; completion report | `examples/multi-region-pattern-workflow.md` |
| `review-azure-diagram.prompt.md` | Read-only review of an existing diagram | diagram-validation-and-evidence, drawio-core-generation, drawio-xml-authoring, azure-architecture-design, azure-architecture-patterns, azure-icons-and-visual-language, drawio-layout-and-composition, drawio-render-export-and-review | Prioritized findings by page and cell ID, checks run and not run, completion report | `examples/private-endpoint-review-workflow.md` |
| `audit-diagram-against-source.prompt.md` | Read-only source-to-diagram drift audit | azure-architecture-design, drawio-core-generation, diagram-validation-and-evidence, azure-architecture-patterns | Drift table, proposed update scope, completion report | none; the review example shows the read-only pattern |
| `repair-azure-drawio-xml.prompt.md` | Repair or normalize Draw.io XML | drawio-xml-authoring, azure-icons-and-visual-language, drawio-core-generation, diagram-validation-and-evidence, drawio-render-export-and-review | Repaired `.drawio` at an approved path, change log with ID map, completion report | `examples/xml-repair-and-reflow-workflow.md` |
| `reflow-diagram-layout.prompt.md` | Reflow a crowded diagram without changing its meaning | drawio-layout-and-composition, azure-icons-and-visual-language, drawio-xml-authoring, drawio-core-generation, diagram-validation-and-evidence, drawio-render-export-and-review | Reflowed `.drawio` or added views, layout change list, completion report | `examples/xml-repair-and-reflow-workflow.md` |
| `export-and-review-render.prompt.md` | Export and renderer-based review | drawio-render-export-and-review, diagram-validation-and-evidence, drawio-core-generation | Exports with renderer version, visual findings, completion report; blocked when no renderer is found | `examples/export-blocked-workflow.md` |

## Skill coverage

Every shipped Skill is applied by at least one prompt.

| Skill | Prompts |
|---|---|
| drawio-core-generation | all eight |
| diagram-validation-and-evidence | all eight |
| azure-architecture-design | design, derive, pattern, review, audit |
| azure-architecture-patterns | design, derive, pattern, review, audit |
| azure-icons-and-visual-language | design, derive, pattern, review, repair, reflow |
| drawio-xml-authoring | design, derive, pattern, review, repair, reflow |
| drawio-layout-and-composition | design, derive, pattern, review, reflow |
| drawio-render-export-and-review | design, derive, pattern, review, repair, reflow, export |

## Templates the prompts produce

The prompts describe the documents they produce, without pointing at pack files, because `templates/` is not installed. The matching templates for people adopting the pack are:

| Template | Produced by |
|---|---|
| `templates/diagram-brief.md` | the first step of every creating or editing prompt |
| `templates/source-inventory.md` | derive, audit |
| `templates/diagram-companion-report.md` | design, derive, pattern |
| `templates/diagram-review-findings.md` | review, audit |
| `templates/completion-report.md` | every prompt |
| `templates/azure-diagram-skeleton.drawio` | a starting file for design and pattern work |

## Installation behavior

Prompts live in `.apm/prompts/`. Per the vendor facts this pack follows, APM drops prompt frontmatter keys that Claude commands do not support, such as `agent`, with a warning. A user-scope APM install (`apm install -g`) delivers prompts for Claude Code and Copilot, but not for Codex. Users of a client without prompts invoke `azure-expert-designer` directly with the same request. The validator's install check runs `apm install` for every declared target with these prompts present. It does not report where each client placed them, so per-client prompt placement is not established here.
