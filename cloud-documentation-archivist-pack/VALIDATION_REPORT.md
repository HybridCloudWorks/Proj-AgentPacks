# VALIDATION_REPORT

Pack: cloud-documentation-archivist 1.2.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 149  Passed: 148  Failed: 0  Skipped: 1

## Scope

1 agents, 18 skills, 1 instruction files, 11 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | required artifact docs (contains at least one file) | pass |  |
| structural | required artifact compatibility (contains at least one file) | pass |  |
| structural | required artifact examples (contains at least one file) | pass |  |
| structural | required artifact templates (contains at least one file) | pass |  |
| structural | required artifact hooks/README.md | pass |  |
| structural | required artifact tests (contains at least one file) | pass |  |
| structural | required artifact .apm/agents (contains at least one file) | pass |  |
| structural | required artifact .apm/skills (contains at least one file) | pass |  |
| structural | required artifact .apm/instructions (contains at least one file) | pass |  |
| structural | required artifact .apm/prompts (contains at least one file) | pass |  |
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
| structural | apm.yml name equals the pack folder name without -pack | pass | cloud-documentation-archivist vs cloud-documentation-archivist-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent cloud-documentation-archivist: name and description present | pass |  |
| structural | agent cloud-documentation-archivist: file name equals name | pass |  |
| structural | agent cloud-documentation-archivist: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent cloud-documentation-archivist: description within 1024 characters | pass |  |
| structural | agent cloud-documentation-archivist: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill adr-and-decision-records: SKILL.md with name equal to folder | pass |  |
| structural | skill adr-and-decision-records: description within 1024 characters | pass |  |
| structural | skill changelogs-release-notes-and-migration: SKILL.md with name equal to folder | pass |  |
| structural | skill changelogs-release-notes-and-migration: description within 1024 characters | pass |  |
| structural | skill diataxis-content-design: SKILL.md with name equal to folder | pass |  |
| structural | skill diataxis-content-design: description within 1024 characters | pass |  |
| structural | skill docs-as-code-and-publishing: SKILL.md with name equal to folder | pass |  |
| structural | skill docs-as-code-and-publishing: description within 1024 characters | pass |  |
| structural | skill docs-security-privacy-and-redaction: SKILL.md with name equal to folder | pass |  |
| structural | skill docs-security-privacy-and-redaction: description within 1024 characters | pass |  |
| structural | skill documentation-archivist-orchestration: SKILL.md with name equal to folder | pass |  |
| structural | skill documentation-archivist-orchestration: description within 1024 characters | pass |  |
| structural | skill documentation-hooks-and-automation: SKILL.md with name equal to folder | pass |  |
| structural | skill documentation-hooks-and-automation: description within 1024 characters | pass |  |
| structural | skill documentation-purpose-and-information-architecture: SKILL.md with name equal to folder | pass |  |
| structural | skill documentation-purpose-and-information-architecture: description within 1024 characters | pass |  |
| structural | skill documentation-style-and-editorial-quality: SKILL.md with name equal to folder | pass |  |
| structural | skill documentation-style-and-editorial-quality: description within 1024 characters | pass |  |
| structural | skill documentation-validation-and-link-checking: SKILL.md with name equal to folder | pass |  |
| structural | skill documentation-validation-and-link-checking: description within 1024 characters | pass |  |
| structural | skill explanation-and-architecture-docs: SKILL.md with name equal to folder | pass |  |
| structural | skill explanation-and-architecture-docs: description within 1024 characters | pass |  |
| structural | skill knowledge-base-and-taxonomy: SKILL.md with name equal to folder | pass |  |
| structural | skill knowledge-base-and-taxonomy: description within 1024 characters | pass |  |
| structural | skill repository-and-project-doc-governance: SKILL.md with name equal to folder | pass |  |
| structural | skill repository-and-project-doc-governance: description within 1024 characters | pass |  |
| structural | skill research-synthesis-and-source-traceability: SKILL.md with name equal to folder | pass |  |
| structural | skill research-synthesis-and-source-traceability: description within 1024 characters | pass |  |
| structural | skill runbooks-and-operational-docs: SKILL.md with name equal to folder | pass |  |
| structural | skill runbooks-and-operational-docs: description within 1024 characters | pass |  |
| structural | skill technical-reference-and-api-docs: SKILL.md with name equal to folder | pass |  |
| structural | skill technical-reference-and-api-docs: description within 1024 characters | pass |  |
| structural | skill templates-and-content-models: SKILL.md with name equal to folder | pass |  |
| structural | skill templates-and-content-models: description within 1024 characters | pass |  |
| structural | skill tutorials-and-how-to-guides: SKILL.md with name equal to folder | pass |  |
| structural | skill tutorials-and-how-to-guides: description within 1024 characters | pass |  |
| structural | instruction cloud-documentation-archivist-contract.instructions.md: description and applyTo | pass |  |
| structural | prompt document-reference.prompt.md: description | pass |  |
| structural | prompt document-release.prompt.md: description | pass |  |
| structural | prompt explain-architecture.prompt.md: description | pass |  |
| structural | prompt govern-documentation.prompt.md: description | pass |  |
| structural | prompt plan-documentation.prompt.md: description | pass |  |
| structural | prompt prepare-publication.prompt.md: description | pass |  |
| structural | prompt record-decision.prompt.md: description | pass |  |
| structural | prompt review-documentation.prompt.md: description | pass |  |
| structural | prompt synthesize-research.prompt.md: description | pass |  |
| structural | prompt write-runbook.prompt.md: description | pass |  |
| structural | prompt write-tutorial-or-how-to.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/cloud-documentation-archivist.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/cloud-documentation-archivist-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/document-reference.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/document-release.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/explain-architecture.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/govern-documentation.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/plan-documentation.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/prepare-publication.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/record-decision.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-documentation.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/synthesize-research.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/write-runbook.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/write-tutorial-or-how-to.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/adr-and-decision-records/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/changelogs-release-notes-and-migration/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/diataxis-content-design/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/docs-as-code-and-publishing/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/docs-security-privacy-and-redaction/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/documentation-archivist-orchestration/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/documentation-hooks-and-automation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/documentation-purpose-and-information-architecture/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/documentation-style-and-editorial-quality/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/documentation-validation-and-link-checking/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/explanation-and-architecture-docs/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/knowledge-base-and-taxonomy/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/repository-and-project-doc-governance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/research-synthesis-and-source-traceability/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/runbooks-and-operational-docs/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/technical-reference-and-api-docs/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/templates-and-content-models/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/tutorials-and-how-to-guides/SKILL.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/PROMPT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/SOURCE_TRACEABILITY.md: describes the current layout | pass |  |
| structural | pack doc compatibility/capability-map.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/compatibility-matrix.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/optional-skills.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/tool-permissions.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/vendor-sources.yml: describes the current layout | pass |  |
| structural | tests/skill-coverage.yml lists exactly the shipped skills | pass | missing: [] extra: [] |
| structural | tests/skill-coverage.yml has an activation statement for every skill | pass |  |
| structural | tests/capability-coverage.yml prompt files exist | pass |  |
| structural | tests/capability-coverage.yml names every skill exactly once | pass | 18 requirements for 18 skills |
| structural | tests/trigger-cases.yml prompt files exist | pass |  |
| structural | an always-on contract instruction exists (.apm/instructions/*contract*.instructions.md) | pass |  |
| structural | contract instruction states every short value listed in report-contract.yml | pass |  |
| structural | status names used in installed content are defined in report-contract.yml | pass |  |
| executable | pack unit tests | skipped | no test_*.py in tests/ |
| executable | apm compile --validate | pass | [*] All primitives validated successfully! |
| executable | apm install --target copilot,claude,codex,kiro,gemini,agent-skills succeeds | pass |  |
| executable | copilot: 1 agents generated | pass | found 1 |
| executable | claude: 1 agents generated | pass | found 1 |
| executable | codex: 1 agents generated | pass | found 1 |
| executable | kiro: 1 agents generated | pass | found 1 |
| executable | no hook files generated | pass |  |
| executable | claude: instructions generated as rules | pass | found 1 |
| executable | generated vendor files reference only installed things | pass |  |
