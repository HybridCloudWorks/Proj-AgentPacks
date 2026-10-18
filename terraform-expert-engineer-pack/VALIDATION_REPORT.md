# VALIDATION_REPORT

Pack: terraform-expert-engineer 1.2.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 121  Passed: 120  Failed: 0  Skipped: 1

## Scope

1 agents, 9 skills, 1 instruction files, 11 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | terraform-expert-engineer vs terraform-expert-engineer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent terraform-expert-engineer: name and description present | pass |  |
| structural | agent terraform-expert-engineer: file name equals name | pass |  |
| structural | agent terraform-expert-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent terraform-expert-engineer: description within 1024 characters | pass |  |
| structural | agent terraform-expert-engineer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill azure-verified-modules: SKILL.md with name equal to folder | pass |  |
| structural | skill azure-verified-modules: description within 1024 characters | pass |  |
| structural | skill terraform-ci-cd-and-quality: SKILL.md with name equal to folder | pass |  |
| structural | skill terraform-ci-cd-and-quality: description within 1024 characters | pass |  |
| structural | skill terraform-cloud-and-stacks: SKILL.md with name equal to folder | pass |  |
| structural | skill terraform-cloud-and-stacks: description within 1024 characters | pass |  |
| structural | skill terraform-core-and-style: SKILL.md with name equal to folder | pass |  |
| structural | skill terraform-core-and-style: description within 1024 characters | pass |  |
| structural | skill terraform-modules-and-refactoring: SKILL.md with name equal to folder | pass |  |
| structural | skill terraform-modules-and-refactoring: description within 1024 characters | pass |  |
| structural | skill terraform-policy-and-governance: SKILL.md with name equal to folder | pass |  |
| structural | skill terraform-policy-and-governance: description within 1024 characters | pass |  |
| structural | skill terraform-provider-development: SKILL.md with name equal to folder | pass |  |
| structural | skill terraform-provider-development: description within 1024 characters | pass |  |
| structural | skill terraform-state-backends-and-imports: SKILL.md with name equal to folder | pass |  |
| structural | skill terraform-state-backends-and-imports: description within 1024 characters | pass |  |
| structural | skill terraform-testing-and-validation: SKILL.md with name equal to folder | pass |  |
| structural | skill terraform-testing-and-validation: description within 1024 characters | pass |  |
| structural | instruction terraform-expert-engineer-contract.instructions.md: description and applyTo | pass |  |
| structural | prompt add-terraform-tests.prompt.md: description | pass |  |
| structural | prompt author-terraform-policy.prompt.md: description | pass |  |
| structural | prompt build-terraform-pipeline.prompt.md: description | pass |  |
| structural | prompt design-hcp-terraform-workflow.prompt.md: description | pass |  |
| structural | prompt develop-terraform-provider.prompt.md: description | pass |  |
| structural | prompt implement-terraform-change.prompt.md: description | pass |  |
| structural | prompt import-terraform-resources.prompt.md: description | pass |  |
| structural | prompt migrate-terraform-state.prompt.md: description | pass |  |
| structural | prompt refactor-terraform-module.prompt.md: description | pass |  |
| structural | prompt review-terraform-avm-module.prompt.md: description | pass |  |
| structural | prompt review-terraform-change.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/terraform-expert-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/terraform-expert-engineer-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/add-terraform-tests.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/author-terraform-policy.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-terraform-pipeline.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-hcp-terraform-workflow.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/develop-terraform-provider.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/implement-terraform-change.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/import-terraform-resources.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/migrate-terraform-state.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/refactor-terraform-module.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-terraform-avm-module.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-terraform-change.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/azure-verified-modules/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/terraform-ci-cd-and-quality/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/terraform-cloud-and-stacks/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/terraform-core-and-style/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/terraform-modules-and-refactoring/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/terraform-policy-and-governance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/terraform-provider-development/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/terraform-state-backends-and-imports/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/terraform-testing-and-validation/SKILL.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/OFFICIAL_SOURCES.md: describes the current layout | pass |  |
| structural | pack doc docs/PROMPT_INVENTORY.md: describes the current layout | pass |  |
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
