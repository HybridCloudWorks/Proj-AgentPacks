# VALIDATION_REPORT

Pack: notion-subject-matter-expert 1.0.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 134  Passed: 134  Failed: 0  Skipped: 0

## Scope

2 agents, 7 skills, 2 instruction files, 8 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

## Failed checks

- None

## Not established

- Agents appear and run in the VS Code agent pane for Claude Code, Codex, and GitHub Copilot.
- A user-profile install (Code Workflow installer, or `apm install -g`) behaves identically on Windows and macOS.
- Kiro and Antigravity IDE behaviour, and Gemini CLI behaviour, on a live install.
- Model behaviour of the agents when actually invoked; tests cover helper code and contracts only.
- Hook behaviour: hooks ship as helper scripts and samples; no native hook was installed or exercised.

## Check inventory

| Kind | Check | Result | Detail |
|---|---|---|---|
| structural | required artifact apm.yml | pass |  |
| structural | required artifact DESCRIPTION.md | pass |  |
| structural | required artifact README.md | pass |  |
| structural | required artifact LICENSE | pass |  |
| structural | required artifact PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | pass |  |
| structural | required artifact docs | pass |  |
| structural | required artifact compatibility | pass |  |
| structural | required artifact examples | pass |  |
| structural | required artifact templates | pass |  |
| structural | required artifact hooks/README.md | pass |  |
| structural | required artifact tests | pass |  |
| structural | required artifact .apm/agents | pass |  |
| structural | required artifact .apm/skills | pass |  |
| structural | required artifact .apm/instructions | pass |  |
| structural | required artifact .apm/prompts | pass |  |
| structural | no stale folder targets/ | pass |  |
| structural | no stale folder claude-code/ | pass |  |
| structural | no stale folder gemini-cli/ | pass |  |
| structural | no stale folder github-copilot/ | pass |  |
| structural | no stale folder openai-codex/ | pass |  |
| structural | no stale folder instructions/ | pass |  |
| structural | no stale folder prompts/ | pass |  |
| structural | no __pycache__ or .pyc outside tests/ and tooling/ | pass |  |
| structural | no archives at pack root | pass |  |
| structural | no native hook JSON for APM to deploy | pass | native hooks would carry repository-relative commands; hooks ship as helper scripts and samples |
| structural | no per-pack copy of tooling/validate_pack.py (shared tooling lives at the repository root) | pass |  |
| structural | no per-pack copy of tooling/build_pack.py (shared tooling lives at the repository root) | pass |  |
| structural | apm.yml uses only APM-defined fields | pass |  |
| structural | apm.yml has name and version | pass |  |
| structural | apm.yml version is semantic | pass |  |
| structural | apm.yml name equals the pack folder name without -pack | pass | notion-subject-matter-expert vs notion-subject-matter-expert-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent notion-governance-reviewer: name and description present | pass |  |
| structural | agent notion-governance-reviewer: file name equals name | pass |  |
| structural | agent notion-governance-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent notion-governance-reviewer: description within 1024 characters | pass |  |
| structural | agent notion-governance-reviewer: body within 300 lines | pass |  |
| structural | agent notion-subject-matter-expert: name and description present | pass |  |
| structural | agent notion-subject-matter-expert: file name equals name | pass |  |
| structural | agent notion-subject-matter-expert: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent notion-subject-matter-expert: description within 1024 characters | pass |  |
| structural | agent notion-subject-matter-expert: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill notion-api-integration: SKILL.md with name equal to folder | pass |  |
| structural | skill notion-api-integration: description within 1024 characters | pass |  |
| structural | skill notion-database-design: SKILL.md with name equal to folder | pass |  |
| structural | skill notion-database-design: description within 1024 characters | pass |  |
| structural | skill notion-knowledge-curation: SKILL.md with name equal to folder | pass |  |
| structural | skill notion-knowledge-curation: description within 1024 characters | pass |  |
| structural | skill notion-meeting-materials: SKILL.md with name equal to folder | pass |  |
| structural | skill notion-meeting-materials: description within 1024 characters | pass |  |
| structural | skill notion-research-synthesis: SKILL.md with name equal to folder | pass |  |
| structural | skill notion-research-synthesis: description within 1024 characters | pass |  |
| structural | skill notion-spec-to-tasks: SKILL.md with name equal to folder | pass |  |
| structural | skill notion-spec-to-tasks: description within 1024 characters | pass |  |
| structural | skill notion-workspace-architecture: SKILL.md with name equal to folder | pass |  |
| structural | skill notion-workspace-architecture: description within 1024 characters | pass |  |
| structural | instruction notion-integration-code.instructions.md: description and applyTo | pass |  |
| structural | instruction notion-subject-matter-expert-contract.instructions.md: description and applyTo | pass |  |
| structural | prompt audit-workspace.prompt.md: description | pass |  |
| structural | prompt capture-knowledge.prompt.md: description | pass |  |
| structural | prompt connect-notion-integration.prompt.md: description | pass |  |
| structural | prompt design-database.prompt.md: description | pass |  |
| structural | prompt design-workspace.prompt.md: description | pass |  |
| structural | prompt plan-spec-implementation.prompt.md: description | pass |  |
| structural | prompt prepare-meeting.prompt.md: description | pass |  |
| structural | prompt research-and-document.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/notion-governance-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/notion-subject-matter-expert.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/notion-integration-code.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/notion-subject-matter-expert-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/audit-workspace.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/capture-knowledge.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/connect-notion-integration.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-database.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-workspace.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/plan-spec-implementation.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/prepare-meeting.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/research-and-document.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-api-integration/api-reference-notes.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-api-integration/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-database-design/property-and-schema-reference.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-database-design/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-knowledge-curation/page-structures.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-knowledge-curation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-meeting-materials/meeting-templates.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-meeting-materials/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-research-synthesis/report-formats.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-research-synthesis/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-spec-to-tasks/plan-and-task-templates.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-spec-to-tasks/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-workspace-architecture/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/notion-workspace-architecture/workspace-design-reference.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/AGENT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/APPROVAL_MATRIX.md: describes the current layout | pass |  |
| structural | pack doc docs/HANDOFF_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/INTEGRATION_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/MAINTENANCE.md: describes the current layout | pass |  |
| structural | pack doc docs/PROMPT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/ROLE_DEFINITION.md: describes the current layout | pass |  |
| structural | pack doc docs/SKILL_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/SOURCE_TRACEABILITY.md: describes the current layout | pass |  |
| structural | pack doc docs/TOOL_PERMISSION_MATRIX.md: describes the current layout | pass |  |
| structural | pack doc compatibility/capability-map.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/compatibility-matrix.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/optional-skills.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/tool-permissions.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/vendor-sources.yml: describes the current layout | pass |  |
| structural | tests/skill-coverage.yml lists exactly the shipped skills | pass | missing: [] extra: [] |
| structural | tests/skill-coverage.yml has an activation statement for every skill | pass |  |
| structural | tests/capability-coverage.yml prompt files exist | pass |  |
| structural | tests/capability-coverage.yml names every skill exactly once | pass | 7 requirements for 7 skills |
| structural | tests/trigger-cases.yml prompt files exist | pass |  |
| structural | an always-on contract instruction exists (.apm/instructions/*contract*.instructions.md) | pass |  |
| structural | contract instruction states every short value listed in report-contract.yml | pass |  |
| structural | contract instruction states the fallback sentence | pass |  |
| structural | status names used in installed content are defined in report-contract.yml | pass |  |
| executable | pack unit tests (python -m unittest discover -s tests) | pass | OK |
| executable | apm compile --validate | pass | [*] All primitives validated successfully! |
| executable | apm install --target copilot,claude,codex,kiro,gemini,agent-skills succeeds | pass |  |
| executable | copilot: 2 agents generated | pass | found 2 |
| executable | claude: 2 agents generated | pass | found 2 |
| executable | codex: 2 agents generated | pass | found 2 |
| executable | kiro: 2 agents generated | pass | found 2 |
| executable | no hook files generated | pass |  |
| executable | claude: instructions generated as rules | pass | found 2 |
| executable | generated vendor files reference only installed things | pass |  |
