# Skill inventory

| Skill | Activation | Reference file in the skill folder | Workflow prompt |
|---|---|---|---|
| notion-workspace-architecture | Where content should live, workspace or teamspace organization, who can see what, consolidation or migration, findability, staleness, duplication or over-sharing. | workspace-design-reference.md | design-workspace.prompt.md, audit-workspace.prompt.md |
| notion-database-design | New database or tracker, modeling questions, formulas, relations, rollups, views, or renaming, retyping, merging or deleting properties. | property-and-schema-reference.md | design-database.prompt.md |
| notion-knowledge-curation | Save, document, write up or record something; wiki page, FAQ, how-to or decision record; keep documentation current. | page-structures.md | capture-knowledge.prompt.md |
| notion-meeting-materials | Prep, plan or run a meeting; agenda or pre-read; recurring meeting page; notes, decisions and follow-ups. | meeting-templates.md | prepare-meeting.prompt.md |
| notion-research-synthesis | What the workspace says about a topic; findings across many pages; research documents, comparisons, status synthesis with sources. | report-formats.md | research-and-document.prompt.md |
| notion-spec-to-tasks | Break down a spec, PRD or design document; implementation plan; progress against a spec; updates after a spec change. | plan-and-task-templates.md | plan-spec-implementation.prompt.md |
| notion-api-integration | Connect an agent or tool to Notion; automate Notion from a script; sync with another system; debug API errors. | api-reference-notes.md | connect-notion-integration.prompt.md |

## Why seven

The role has seven distinct jobs with different inputs, outputs and risks. Four come from the reference collection's workflows (capture, meetings, research, specs), reworked to add approval levels, audience separation and verification. Three fill gaps a Notion expert is regularly asked about and the reference did not cover: workspace structure and sharing, database modeling and schema-change safety, and API or MCP integration. Narrower candidates were folded in rather than shipped thin: audits and migrations live in workspace architecture, formulas and automations in database design, progress tracking in spec-to-tasks, and post-meeting capture in meeting materials.

## Operational sections

Every SKILL.md states purpose and activation, scope and exclusions, inputs, dependencies and tools, workflow, output, validation, failure handling and escalation, permissions and guardrails, and its connection to the agents and prompts. Each one restates its own approval rules for standalone installs, and refers only to its own folder, other skills and the contract instruction. These are operational instructions, not a guarantee that a model always follows them.
