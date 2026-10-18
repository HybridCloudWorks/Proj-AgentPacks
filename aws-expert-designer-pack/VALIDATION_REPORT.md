# VALIDATION_REPORT

Pack: aws-expert-designer 1.4.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 116  Passed: 115  Failed: 0  Skipped: 1

## Scope

1 agents, 8 skills, 1 instruction files, 7 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | aws-expert-designer vs aws-expert-designer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent aws-expert-designer: name and description present | pass |  |
| structural | agent aws-expert-designer: file name equals name | pass |  |
| structural | agent aws-expert-designer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent aws-expert-designer: description within 1024 characters | pass |  |
| structural | agent aws-expert-designer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill aws-architecture-design: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-architecture-design: description within 1024 characters | pass |  |
| structural | skill aws-architecture-patterns: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-architecture-patterns: description within 1024 characters | pass |  |
| structural | skill aws-icons-and-visual-language: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-icons-and-visual-language: description within 1024 characters | pass |  |
| structural | skill aws-layout-and-composition: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-layout-and-composition: description within 1024 characters | pass |  |
| structural | skill aws-xml-authoring: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-xml-authoring: description within 1024 characters | pass |  |
| structural | skill diagram-validation-and-evidence: SKILL.md with name equal to folder | pass |  |
| structural | skill diagram-validation-and-evidence: description within 1024 characters | pass |  |
| structural | skill drawio-core-generation: SKILL.md with name equal to folder | pass |  |
| structural | skill drawio-core-generation: description within 1024 characters | pass |  |
| structural | skill drawio-render-export-and-review: SKILL.md with name equal to folder | pass |  |
| structural | skill drawio-render-export-and-review: description within 1024 characters | pass |  |
| structural | instruction aws-expert-designer-contract.instructions.md: description and applyTo | pass |  |
| structural | prompt design-aws-diagram.prompt.md: description | pass |  |
| structural | prompt diagram-from-infrastructure-code.prompt.md: description | pass |  |
| structural | prompt export-drawio-diagram.prompt.md: description | pass |  |
| structural | prompt model-aws-architecture-pattern.prompt.md: description | pass |  |
| structural | prompt reflow-aws-diagram-layout.prompt.md: description | pass |  |
| structural | prompt repair-aws-drawio-xml.prompt.md: description | pass |  |
| structural | prompt review-aws-diagram.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/aws-expert-designer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/aws-expert-designer-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-aws-diagram.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/diagram-from-infrastructure-code.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/export-drawio-diagram.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/model-aws-architecture-pattern.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/reflow-aws-diagram-layout.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/repair-aws-drawio-xml.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-aws-diagram.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-architecture-design/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-architecture-patterns/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-icons-and-visual-language/references/aws-visual-rules.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-icons-and-visual-language/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-layout-and-composition/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-xml-authoring/references/aws-xml-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-xml-authoring/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/diagram-validation-and-evidence/references/provider-checks.md: references only installed things | pass |  |
| structural | installed content .apm/skills/diagram-validation-and-evidence/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-core-generation/references/providers.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-core-generation/references/upstream-routing.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-core-generation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-render-export-and-review/references/export-cli.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-render-export-and-review/SKILL.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/PROMPT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/SOURCE_HASHES.md: describes the current layout | pass |  |
| structural | pack doc docs/SOURCE_TRACEABILITY.md: describes the current layout | pass |  |
| structural | pack doc compatibility/capability-map.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/compatibility-matrix.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/tool-permissions.yml: describes the current layout | pass |  |
| structural | pack doc compatibility/vendor-sources.yml: describes the current layout | pass |  |
| structural | tests/skill-coverage.yml lists exactly the shipped skills | pass | missing: [] extra: [] |
| structural | tests/skill-coverage.yml has an activation statement for every skill | pass |  |
| structural | tests/capability-coverage.yml prompt files exist | pass |  |
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
