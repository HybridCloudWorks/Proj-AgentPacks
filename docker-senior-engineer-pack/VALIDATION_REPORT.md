# VALIDATION_REPORT

Pack: docker-senior-engineer 1.0.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 133  Passed: 133  Failed: 0  Skipped: 0

## Scope

3 agents, 6 skills, 4 instruction files, 7 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | docker-senior-engineer vs docker-senior-engineer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent container-build-verifier: name and description present | pass |  |
| structural | agent container-build-verifier: file name equals name | pass |  |
| structural | agent container-build-verifier: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent container-build-verifier: description within 1024 characters | pass |  |
| structural | agent container-build-verifier: body within 300 lines | pass |  |
| structural | agent container-security-reviewer: name and description present | pass |  |
| structural | agent container-security-reviewer: file name equals name | pass |  |
| structural | agent container-security-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent container-security-reviewer: description within 1024 characters | pass |  |
| structural | agent container-security-reviewer: body within 300 lines | pass |  |
| structural | agent docker-senior-engineer: name and description present | pass |  |
| structural | agent docker-senior-engineer: file name equals name | pass |  |
| structural | agent docker-senior-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent docker-senior-engineer: description within 1024 characters | pass |  |
| structural | agent docker-senior-engineer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill compose-environments: SKILL.md with name equal to folder | pass |  |
| structural | skill compose-environments: description within 1024 characters | pass |  |
| structural | skill container-runtime-operations: SKILL.md with name equal to folder | pass |  |
| structural | skill container-runtime-operations: description within 1024 characters | pass |  |
| structural | skill container-security-hardening: SKILL.md with name equal to folder | pass |  |
| structural | skill container-security-hardening: description within 1024 characters | pass |  |
| structural | skill docker-change-review: SKILL.md with name equal to folder | pass |  |
| structural | skill docker-change-review: description within 1024 characters | pass |  |
| structural | skill dockerfile-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill dockerfile-engineering: description within 1024 characters | pass |  |
| structural | skill image-build-and-supply-chain: SKILL.md with name equal to folder | pass |  |
| structural | skill image-build-and-supply-chain: description within 1024 characters | pass |  |
| structural | instruction compose.instructions.md: description and applyTo | pass |  |
| structural | instruction docker-senior-engineer-contract.instructions.md: description and applyTo | pass |  |
| structural | instruction dockerfile.instructions.md: description and applyTo | pass |  |
| structural | instruction image-build.instructions.md: description and applyTo | pass |  |
| structural | prompt build-compose-environment.prompt.md: description | pass |  |
| structural | prompt containerize-application.prompt.md: description | pass |  |
| structural | prompt diagnose-container-issue.prompt.md: description | pass |  |
| structural | prompt harden-container.prompt.md: description | pass |  |
| structural | prompt optimize-image.prompt.md: description | pass |  |
| structural | prompt review-container-change.prompt.md: description | pass |  |
| structural | prompt set-up-image-pipeline.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/container-build-verifier.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/container-security-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/docker-senior-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/compose.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/docker-senior-engineer-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/dockerfile.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/image-build.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-compose-environment.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/containerize-application.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/diagnose-container-issue.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/harden-container.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/optimize-image.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-container-change.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/set-up-image-pipeline.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/compose-environments/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/container-runtime-operations/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/container-security-hardening/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/docker-change-review/review-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/docker-change-review/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/dockerfile-engineering/dockerfile-patterns.md: references only installed things | pass |  |
| structural | installed content .apm/skills/dockerfile-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/image-build-and-supply-chain/SKILL.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/AGENT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/APPROVAL_MATRIX.md: describes the current layout | pass |  |
| structural | pack doc docs/HANDOFF_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/INTEGRATION_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/MAINTENANCE.md: describes the current layout | pass |  |
| structural | pack doc docs/PROMPT_INVENTORY.md: describes the current layout | pass |  |
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
| structural | tests/capability-coverage.yml names every skill exactly once | pass | 6 requirements for 6 skills |
| structural | tests/trigger-cases.yml prompt files exist | pass |  |
| structural | an always-on contract instruction exists (.apm/instructions/*contract*.instructions.md) | pass |  |
| structural | contract instruction states every short value listed in report-contract.yml | pass |  |
| structural | contract instruction states the fallback sentence | pass |  |
| structural | status names used in installed content are defined in report-contract.yml | pass |  |
| executable | pack unit tests (python -m unittest discover -s tests) | pass | OK |
| executable | apm compile --validate | pass | [*] All primitives validated successfully! |
| executable | apm install --target copilot,claude,codex,kiro,gemini,agent-skills succeeds | pass |  |
| executable | copilot: 3 agents generated | pass | found 3 |
| executable | claude: 3 agents generated | pass | found 3 |
| executable | codex: 3 agents generated | pass | found 3 |
| executable | kiro: 3 agents generated | pass | found 3 |
| executable | no hook files generated | pass |  |
| executable | claude: instructions generated as rules | pass | found 4 |
| executable | generated vendor files reference only installed things | pass |  |
