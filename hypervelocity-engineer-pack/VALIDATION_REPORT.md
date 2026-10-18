# VALIDATION_REPORT

Pack: hypervelocity-engineer 1.1.0
Standard: agent-pack-prompt v2.2
Validated: 2026-10-18
Status: PASS

Checks: 98  Passed: 97  Failed: 0  Skipped: 1

## Scope

1 agents, 9 skills, 1 instruction files, 0 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | hypervelocity-engineer vs hypervelocity-engineer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent hypervelocity-engineer: name and description present | pass |  |
| structural | agent hypervelocity-engineer: file name equals name | pass |  |
| structural | agent hypervelocity-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent hypervelocity-engineer: description within 1024 characters | pass |  |
| structural | agent hypervelocity-engineer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill agent-delegation-and-composition: SKILL.md with name equal to folder | pass |  |
| structural | skill agent-delegation-and-composition: description within 1024 characters | pass |  |
| structural | skill agent-governance-and-guardrails: SKILL.md with name equal to folder | pass |  |
| structural | skill agent-governance-and-guardrails: description within 1024 characters | pass |  |
| structural | skill agent-usage-reporting: SKILL.md with name equal to folder | pass |  |
| structural | skill agent-usage-reporting: description within 1024 characters | pass |  |
| structural | skill agentic-workflows: SKILL.md with name equal to folder | pass |  |
| structural | skill agentic-workflows: description within 1024 characters | pass |  |
| structural | skill copilot-review-feedback: SKILL.md with name equal to folder | pass |  |
| structural | skill copilot-review-feedback: description within 1024 characters | pass |  |
| structural | skill optimize-agentic-workflow: SKILL.md with name equal to folder | pass |  |
| structural | skill optimize-agentic-workflow: description within 1024 characters | pass |  |
| structural | skill prompt-token-efficiency: SKILL.md with name equal to folder | pass |  |
| structural | skill prompt-token-efficiency: description within 1024 characters | pass |  |
| structural | skill workflow-lifecycle-and-release: SKILL.md with name equal to folder | pass |  |
| structural | skill workflow-lifecycle-and-release: description within 1024 characters | pass |  |
| structural | skill workflow-observability-and-evaluation: SKILL.md with name equal to folder | pass |  |
| structural | skill workflow-observability-and-evaluation: description within 1024 characters | pass |  |
| structural | instruction hypervelocity-engineer-contract.instructions.md: description and applyTo | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/hypervelocity-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/hypervelocity-engineer-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-delegation-and-composition/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-governance-and-guardrails/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-usage-reporting/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agentic-workflows/OFFICIAL_SOURCES.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agentic-workflows/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/copilot-review-feedback/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/optimize-agentic-workflow/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/prompt-token-efficiency/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/workflow-lifecycle-and-release/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/workflow-observability-and-evaluation/SKILL.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/OFFICIAL_SOURCES.md: describes the current layout | pass |  |
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
