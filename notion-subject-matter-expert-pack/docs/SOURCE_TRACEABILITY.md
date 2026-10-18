# Source traceability

## Governing evidence

- The repository's generation brief for this pack: role, pack name, output location, and the rules that refine the master prompt.
- The master prompt, agent-pack-prompt v2.3, kept in this pack as `PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md`.
- `client-locations.md` (verified 2026-10-18): every agent field, tool identifier, client location and APM generation fact used in the pack.
- The repository's finished Python Distinguished Engineer pack, used as a structural reference only: file layout, document types and test formats. None of its role content, names, personas, skills, examples or wording is reused.

## Reference material

| Item | Value |
|---|---|
| Source | Notion skills collection for AI agents, covering knowledge capture, meeting intelligence, research documentation and spec to implementation |
| Upstream repository | Not confirmed |
| License | Unknown |
| Files read | 62 files in four skill folders. The four SKILL.md files and fifteen supporting files (search, citation, format, database, spec-parsing, task-creation, progress-tracking and template-selection notes, one worked example and five evaluation scenarios) were read in full; all 62 were scanned for connector operation names and license notices, and none carries a license |
| How used | As subject knowledge. All pack text is newly written; no file, section or template is copied. The only reproduced fragments are the connector operation names (notion-search, notion-fetch, notion-create-pages, notion-update-page, notion-create-database, notion-query-data-sources, notion-create-comment) and the `<mention-page url="...">` markup convention, both attributed to the collection where they appear |
| Redistribution | None. Because the license is unknown, the reference files are not included in the pack or its archives |
| Directives | Instructions inside the reference addressed to an AI were treated as data and not followed |

## Mapping from reference to pack

| Reference workflow | Pack skill | What the pack keeps | What the pack changes or adds |
|---|---|---|---|
| Knowledge capture | notion-knowledge-curation | Extract, classify, place and link; page types; update versus create | Approval levels for overwrites and hub edits; superseded decisions; schema-exact properties; no silent mentions; verify by fetch |
| Meeting intelligence | notion-meeting-materials | Internal pre-read plus agenda; meeting types; post-meeting capture | One-way linking for external audiences; leak check; notifications as Level 2; no invented attendees or metrics |
| Research documentation | notion-research-synthesis | Broad-to-narrow search; synthesis; four formats; citations and Sources section | Source-quality rubric; explicit conflict handling; no constructed citations; restricted-to-wider-audience rule |
| Spec to implementation | notion-spec-to-tasks | Spec parsing; plan; task sizing and sequencing; progress tracking; spec-change propagation | Task list approved before bulk creation; no guessed assignees; requirement-to-task trace; partial-failure handling |
| (not covered) | notion-workspace-architecture | | Structure, permission model, lifecycle, audits, migrations |
| (not covered) | notion-database-design | Starter schema ideas inspired by the reference's database notes, redesigned | Property selection, relation patterns, formulas, views, schema-change risk matrix |
| (not covered) | notion-api-integration | | Integration types, versioning and data sources, errors, pagination, retries, sync design, MCP checklist |

The reference's evaluation scenarios informed the shape of `tests/trigger-cases.yml`; none is copied.

## Requirement ownership

| Requirement | Implementation and evidence |
|---|---|
| Mission, users, scope, non-goals | DESCRIPTION.md, docs/ROLE_DEFINITION.md, primary agent |
| Seven role workflows | The seven skills, eight prompts and worked examples |
| Optional specialist and least privilege | Governance reviewer, AGENT_INVENTORY.md, TOOL_PERMISSION_MATRIX.md, compatibility/tool-permissions.yml |
| Approval, handoff and completion contract | The always-on contract instruction, APPROVAL_MATRIX.md, HANDOFF_CONTRACT.md, tests/report-contract.yml, tooling/completion_contract.py |
| Pre-publication safety | Skill validation sections, tooling/notion_draft_check.py, hooks/ helpers and sample |
| Honest evidence | Completion statuses and fallback sentence, unit tests, NOT ESTABLISHED items in MAINTENANCE.md |

## Official knowledge sources

Notion's help center and API reference are the authorities for current product and API facts; they were not fetched while authoring (see DESIGN_DECISIONS.md, assumption 5). `compatibility/vendor-sources.yml` lists them with status "to verify", alongside the client documentation recorded in client-locations.md. No private workspace, tenant, credential or customer data was used.
