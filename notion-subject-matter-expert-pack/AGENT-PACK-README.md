# notion-subject-matter-expert 1.0.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| notion-governance-reviewer.agent.md | Canonical agent: Read-only independent reviewer of Notion sharing exposure, internal and external content separation, and the safety of schema, move and bulk changes; returns located findings and never writes to the workspace. | .apm/agents/notion-governance-reviewer.agent.md |
| notion-subject-matter-expert.agent.md | Canonical agent: Notion subject matter expert that designs workspaces and databases, captures knowledge, prepares meeting materials, synthesizes research, turns specs into tracked tasks and builds Notion integrations, with approval-gated writes. | .apm/agents/notion-subject-matter-expert.agent.md |
| notion-integration-code.instructions.md | Canonical instruction: Rules for code that calls the Notion API or a Notion MCP server: token handling, pinned API version, rate limits, pagination, payload limits and safe logging. | .apm/instructions/notion-integration-code.instructions.md |
| notion-subject-matter-expert-contract.instructions.md | Canonical instruction: Approval levels, specialist handoff rules and the completion report format for the Notion Subject Matter Expert pack. Always on; the pack's agents, skills and prompts refer to it. | .apm/instructions/notion-subject-matter-expert-contract.instructions.md |
| audit-workspace.prompt.md | Canonical prompt: Audit a Notion workspace area for findability, freshness, ownership and sharing exposure | .apm/prompts/audit-workspace.prompt.md |
| capture-knowledge.prompt.md | Canonical prompt: Save a conversation, decision, procedure or lesson to Notion as a durable page | .apm/prompts/capture-knowledge.prompt.md |
| connect-notion-integration.prompt.md | Canonical prompt: Connect a tool or agent to Notion, or build and debug Notion API code | .apm/prompts/connect-notion-integration.prompt.md |
| design-database.prompt.md | Canonical prompt: Design a new Notion database or change an existing schema safely | .apm/prompts/design-database.prompt.md |
| design-workspace.prompt.md | Canonical prompt: Design or restructure a Notion workspace or teamspace | .apm/prompts/design-workspace.prompt.md |
| plan-spec-implementation.prompt.md | Canonical prompt: Break a Notion spec into an implementation plan and tracked tasks | .apm/prompts/plan-spec-implementation.prompt.md |
| prepare-meeting.prompt.md | Canonical prompt: Prepare a Notion pre-read and agenda for a meeting, or capture its outcomes | .apm/prompts/prepare-meeting.prompt.md |
| research-and-document.prompt.md | Canonical prompt: Research a topic across the Notion workspace and write a cited report | .apm/prompts/research-and-document.prompt.md |
| api-reference-notes.md | Canonical skill | .apm/skills/notion-api-integration/api-reference-notes.md |
| SKILL.md | Canonical skill: Build, review and troubleshoot code and connections that use the Notion API or a Notion MCP server - integration types and capabilities, sharing pages with an integration, pinned API versions and data sources, pagination, rate limits, payload limits, webhooks, sync jobs and safe token handling. Use when a user wants to connect an agent or tool to Notion, automate Notion from a script, sync Notion with another system, or debug Notion API errors such as 401, 403, 404, 409, 429 or validation failures. | .apm/skills/notion-api-integration/SKILL.md |
| property-and-schema-reference.md | Canonical skill | .apm/skills/notion-database-design/property-and-schema-reference.md |
| SKILL.md | Canonical skill: Design and change Notion databases - data sources, property types, relations and rollups, formulas, status workflows, views and filters, templates, buttons, forms and automations - and assess what a schema change breaks before it is made. Use when a user wants a new database or tracker, asks how to model information in Notion, needs a formula, relation, rollup or view, or wants to rename, retype, merge or delete properties in an existing database. | .apm/skills/notion-database-design/SKILL.md |
| page-structures.md | Canonical skill | .apm/skills/notion-knowledge-curation/page-structures.md |
| SKILL.md | Canonical skill: Capture conversations, decisions, procedures, answers and lessons as durable Notion pages - choose the page type and destination, update existing pages instead of duplicating them, set database properties exactly, and link new pages into hubs so people can find them. Use when a user asks to save, document, write up or record something in Notion, turn a discussion into a wiki page, FAQ, how-to or decision record, or bring existing documentation up to date. | .apm/skills/notion-knowledge-curation/SKILL.md |
| meeting-templates.md | Canonical skill | .apm/skills/notion-meeting-materials/meeting-templates.md |
| SKILL.md | Canonical skill: Prepare and follow up meetings in Notion - gather project context from the workspace, write an internal pre-read and a participant-facing agenda that keeps internal material out of external hands, and record decisions and action items afterwards. Use when a user asks to prep for, plan or run a meeting, build an agenda or pre-read, set up a recurring meeting page, or capture meeting notes, decisions and follow-ups in Notion. | .apm/skills/notion-meeting-materials/SKILL.md |
| report-formats.md | Canonical skill | .apm/skills/notion-research-synthesis/report-formats.md |
| SKILL.md | Canonical skill: Research a question across a Notion workspace and the sources connected to it, judge which pages are current and authoritative, reconcile conflicts, and write a cited brief, summary, comparison or full report as a Notion page or database entry. Use when a user asks what the workspace says about a topic, wants findings gathered from many pages, or needs a research document, comparison, competitive or technical analysis, or status synthesis with sources. | .apm/skills/notion-research-synthesis/SKILL.md |
| plan-and-task-templates.md | Canonical skill | .apm/skills/notion-spec-to-tasks/plan-and-task-templates.md |
| SKILL.md | Canonical skill: Turn a product or technical specification in Notion into an implementation plan, right-sized tasks in the team's task database with testable acceptance criteria and dependencies, and progress updates that keep spec, plan and tasks linked as work and the spec change. Use when a user asks to break down a spec, PRD or design document into tasks, create an implementation plan, track progress against a spec, or update tasks after a spec changes. | .apm/skills/notion-spec-to-tasks/SKILL.md |
| SKILL.md | Canonical skill: Design, restructure and audit how a Notion workspace is organized and governed - teamspaces, page hierarchy, wikis and hub pages, naming and tagging, sharing and permission models, content lifecycle, migrations and workspace health. Use when a user asks where content should live, how to organize or reorganize a workspace or teamspace, who can see what, how to consolidate or migrate pages into Notion, or why content is hard to find, stale, duplicated or over-shared. | .apm/skills/notion-workspace-architecture/SKILL.md |
| workspace-design-reference.md | Canonical skill | .apm/skills/notion-workspace-architecture/workspace-design-reference.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| AGENT_INVENTORY.md | Pack contract or inventory | docs/AGENT_INVENTORY.md |
| APPROVAL_MATRIX.md | Pack contract or inventory | docs/APPROVAL_MATRIX.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| HANDOFF_CONTRACT.md | Pack contract or inventory | docs/HANDOFF_CONTRACT.md |
| INTEGRATION_CONTRACT.md | Pack contract or inventory | docs/INTEGRATION_CONTRACT.md |
| MAINTENANCE.md | Pack contract or inventory | docs/MAINTENANCE.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| ROLE_DEFINITION.md | Pack contract or inventory | docs/ROLE_DEFINITION.md |
| SKILL_INVENTORY.md | Pack contract or inventory | docs/SKILL_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| TOOL_PERMISSION_MATRIX.md | Pack contract or inventory | docs/TOOL_PERMISSION_MATRIX.md |
| database-change-workflow.md | Worked example | examples/database-change-workflow.md |
| final-completion-report.md | Worked example | examples/final-completion-report.md |
| knowledge-capture-workflow.md | Worked example | examples/knowledge-capture-workflow.md |
| meeting-prep-workflow.md | Worked example | examples/meeting-prep-workflow.md |
| research-report-workflow.md | Worked example | examples/research-report-workflow.md |
| spec-to-tasks-workflow.md | Worked example | examples/spec-to-tasks-workflow.md |
| workspace-audit-workflow.md | Worked example | examples/workspace-audit-workflow.md |
| post-notion-work.ps1 | Hook helper script | hooks/post-notion-work.ps1 |
| post-notion-work.sh | Hook helper script | hooks/post-notion-work.sh |
| pre-notion-publish.ps1 | Hook helper script | hooks/pre-notion-publish.ps1 |
| pre-notion-publish.sh | Hook helper script | hooks/pre-notion-publish.sh |
| README.md | Hook helper script | hooks/README.md |
| notion-sme.claude-settings.sample.json | Reviewed hook sample, not installed | hooks/samples/notion-sme.claude-settings.sample.json |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| handoff.md | Reusable template | templates/handoff.md |
| workspace-change-request.md | Reusable template | templates/workspace-change-request.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| external-agenda-leak.md | Local test or recorded evidence | tests/fixtures/external-agenda-leak.md |
| invalid-completion.json | Local test or recorded evidence | tests/fixtures/invalid-completion.json |
| research-draft-clean.md | Local test or recorded evidence | tests/fixtures/research-draft-clean.md |
| valid-completion.json | Local test or recorded evidence | tests/fixtures/valid-completion.json |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| test_behavior.py | Local test or recorded evidence | tests/test_behavior.py |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| completion_contract.py | Pack-specific helper code | tooling/completion_contract.py |
| notion_draft_check.py | Pack-specific helper code | tooling/notion_draft_check.py |
| requirements.txt | Pack-specific helper code | tooling/requirements.txt |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-notion-subject-matter-expert.zip: 26 files generated by `apm install --target copilot`
- claude-notion-subject-matter-expert.zip: 26 files generated by `apm install --target claude`
- codex-notion-subject-matter-expert.zip: 16 files generated by `apm install --target codex`
- kiro-notion-subject-matter-expert.zip: 18 files generated by `apm install --target kiro`
- gemini-notion-subject-matter-expert.zip: 22 files generated by `apm install --target gemini`
- agent-skills-notion-subject-matter-expert.zip: 14 files generated by `apm install --target agent-skills`
- notion-subject-matter-expert-canonical.zip, notion-subject-matter-expert-prompt.zip, notion-subject-matter-expert-validation.zip, notion-subject-matter-expert-skills.zip, notion-subject-matter-expert-full-pack.zip, SHA256SUMS.txt
