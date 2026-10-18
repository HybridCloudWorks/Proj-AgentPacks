# Prompt inventory

| Prompt | Skills applied | Expected output |
|---|---|---|
| design-workspace.prompt.md | notion-workspace-architecture, notion-database-design | Structure outline, naming and tagging rules, governance rules, sequenced change list with permission effect and undo. |
| audit-workspace.prompt.md | notion-workspace-architecture, notion-database-design; reviewer when available | Located findings with severity, coverage and blind spots, prioritized remediation for approval. |
| design-database.prompt.md | notion-database-design | Schema table, relation map, views, templates and automations, risk-classified change plan, verified result. |
| capture-knowledge.prompt.md | notion-knowledge-curation | Page URL, properties set, links added or proposed. |
| prepare-meeting.prompt.md | notion-meeting-materials, notion-research-synthesis; reviewer for high-stakes external meetings | Pre-read and agenda URLs or drafts, their linking, what each audience sees. |
| research-and-document.prompt.md | notion-research-synthesis | Cited report, source list with dates, open questions and confidence. |
| plan-spec-implementation.prompt.md | notion-spec-to-tasks, notion-database-design | Plan URL, task URLs, requirement-to-task trace, clarification items. |
| connect-notion-integration.prompt.md | notion-api-integration | Code or configuration with tests, capability list, diagnosis, live behaviour not exercised. |

Every prompt ends with the completion report from the contract instruction. APM installs these as Copilot prompt files, Claude commands (the `agent` key is dropped) and Gemini commands. Codex and Kiro receive no prompts; their users invoke the primary agent directly.
