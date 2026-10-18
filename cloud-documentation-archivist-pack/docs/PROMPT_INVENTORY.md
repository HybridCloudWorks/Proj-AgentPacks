# Prompt inventory

The pack has eleven prompts, one for each primary workflow that the `documentation-archivist-orchestration` Skill routes. All of them live in `.apm/prompts/`, name `cloud-documentation-archivist` as their agent, and end with the completion report defined by the always-on `cloud-documentation-archivist-contract` instruction.

| Prompt | Workflow | Skills applied | Expected output | Worked example |
| --- | --- | --- | --- | --- |
| plan-documentation.prompt.md | Decide reader, task, mode, canonical source, location and owner before writing; plan reorganizations | documentation-archivist-orchestration, documentation-purpose-and-information-architecture, diataxis-content-design | Documentation plan, open questions, and a mapping, redirect and rollback plan for any move | how-to-guide-workflow.md (orientation step) |
| write-tutorial-or-how-to.prompt.md | Write a tutorial or how-to guide | diataxis-content-design, tutorials-and-how-to-guides, templates-and-content-models, docs-security-privacy-and-redaction, documentation-style-and-editorial-quality, documentation-validation-and-link-checking | Guide, with observed steps kept apart from untested ones | how-to-guide-workflow.md |
| document-reference.prompt.md | Reference for an API, CLI, configuration, schema or errors | technical-reference-and-api-docs, diataxis-content-design, templates-and-content-models, docs-security-privacy-and-redaction, documentation-validation-and-link-checking | Reference pages, source version, uncertain items, validated examples | configuration-reference-workflow.md |
| explain-architecture.prompt.md | Explain architecture, rationale and trade-offs | explanation-and-architecture-docs, diataxis-content-design, adr-and-decision-records, docs-security-privacy-and-redaction, documentation-validation-and-link-checking | Explanation with current, target and proposed state labelled; candidate decision records | — |
| record-decision.prompt.md | Record or supersede an architecture decision | adr-and-decision-records, explanation-and-architecture-docs, documentation-validation-and-link-checking | Proposed or superseding decision record, links, deciders still to act | architecture-decision-workflow.md |
| write-runbook.prompt.md | Create or review a runbook or incident record | runbooks-and-operational-docs, research-synthesis-and-source-traceability, docs-security-privacy-and-redaction, templates-and-content-models, documentation-validation-and-link-checking | Runbook with honest last-exercised value, evidence table, findings | runbook-from-incident-workflow.md |
| synthesize-research.prompt.md | Turn sources into a cited brief or comparison | research-synthesis-and-source-traceability, documentation-style-and-editorial-quality, docs-security-privacy-and-redaction, knowledge-base-and-taxonomy | Brief, source ledger, conflicts, not-verified statements | research-brief-workflow.md |
| document-release.prompt.md | Changelog, release notes, deprecation or migration guide | changelogs-release-notes-and-migration, templates-and-content-models, docs-security-privacy-and-redaction, documentation-validation-and-link-checking | Shipped-only entries with evidence; migration with sequence and rollback | — |
| review-documentation.prompt.md | Review existing documents for accuracy, structure, links, freshness and exposure | documentation-hooks-and-automation, documentation-validation-and-link-checking, docs-security-privacy-and-redaction, diataxis-content-design, documentation-style-and-editorial-quality, repository-and-project-doc-governance | Located findings with the contract's fields; checks run and skipped | documentation-review-workflow.md |
| govern-documentation.prompt.md | Documentation contract, ownership, taxonomy and templates for a repository or knowledge base | repository-and-project-doc-governance, knowledge-base-and-taxonomy, templates-and-content-models, documentation-hooks-and-automation | Inventory, contract, taxonomy, template changes, change plan | — |
| prepare-publication.prompt.md | Build, preview and package for publication; publish only with explicit authorization | docs-as-code-and-publishing, documentation-validation-and-link-checking, docs-security-privacy-and-redaction, knowledge-base-and-taxonomy | Publish-ready package or tool-proven published location; unpublish steps; handoff | publication-blocked-workflow.md |

## Skill to prompt

Every Skill is applied by at least one prompt. `tests/capability-coverage.yml` records the primary prompt for each Skill and the other prompts that also apply it.

| Skill | Primary prompt |
| --- | --- |
| documentation-archivist-orchestration | plan-documentation.prompt.md |
| documentation-purpose-and-information-architecture | plan-documentation.prompt.md |
| diataxis-content-design | plan-documentation.prompt.md |
| documentation-style-and-editorial-quality | review-documentation.prompt.md |
| technical-reference-and-api-docs | document-reference.prompt.md |
| tutorials-and-how-to-guides | write-tutorial-or-how-to.prompt.md |
| explanation-and-architecture-docs | explain-architecture.prompt.md |
| adr-and-decision-records | record-decision.prompt.md |
| runbooks-and-operational-docs | write-runbook.prompt.md |
| repository-and-project-doc-governance | govern-documentation.prompt.md |
| templates-and-content-models | govern-documentation.prompt.md |
| docs-as-code-and-publishing | prepare-publication.prompt.md |
| documentation-validation-and-link-checking | review-documentation.prompt.md |
| research-synthesis-and-source-traceability | synthesize-research.prompt.md |
| changelogs-release-notes-and-migration | document-release.prompt.md |
| docs-security-privacy-and-redaction | review-documentation.prompt.md |
| knowledge-base-and-taxonomy | govern-documentation.prompt.md |
| documentation-hooks-and-automation | review-documentation.prompt.md |

## Installed behaviour

Prompts are installed content. They name only Skills and the contract instruction, and never pack folders that are not installed.

According to the APM notes verified on 2026-10-18:

- GitHub Copilot reads the prompts as prompt files and honours the `agent` field.
- Claude Code receives them as commands. APM drops the `agent` field with a warning.
- A user-scope APM install gives Codex no prompts. Codex users invoke the agent directly.

The shared validator's scratch install with every declared target succeeds with these prompts present. This fill did not inspect the exact files generated for Gemini CLI or Kiro.
