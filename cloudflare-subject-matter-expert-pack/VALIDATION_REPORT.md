# VALIDATION_REPORT

Pack: cloudflare-subject-matter-expert 1.0.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 153  Passed: 153  Failed: 0  Skipped: 0

## Scope

3 agents, 11 skills, 4 instruction files, 9 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | cloudflare-subject-matter-expert vs cloudflare-subject-matter-expert-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent cloudflare-migration-analyst: name and description present | pass |  |
| structural | agent cloudflare-migration-analyst: file name equals name | pass |  |
| structural | agent cloudflare-migration-analyst: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent cloudflare-migration-analyst: description within 1024 characters | pass |  |
| structural | agent cloudflare-migration-analyst: body within 300 lines | pass |  |
| structural | agent cloudflare-security-reviewer: name and description present | pass |  |
| structural | agent cloudflare-security-reviewer: file name equals name | pass |  |
| structural | agent cloudflare-security-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent cloudflare-security-reviewer: description within 1024 characters | pass |  |
| structural | agent cloudflare-security-reviewer: body within 300 lines | pass |  |
| structural | agent cloudflare-subject-matter-expert: name and description present | pass |  |
| structural | agent cloudflare-subject-matter-expert: file name equals name | pass |  |
| structural | agent cloudflare-subject-matter-expert: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent cloudflare-subject-matter-expert: description within 1024 characters | pass |  |
| structural | agent cloudflare-subject-matter-expert: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill cloudflare-agents-and-ai: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-agents-and-ai: description within 1024 characters | pass |  |
| structural | skill cloudflare-application-security: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-application-security: description within 1024 characters | pass |  |
| structural | skill cloudflare-change-control: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-change-control: description within 1024 characters | pass |  |
| structural | skill cloudflare-edge-delivery-and-performance: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-edge-delivery-and-performance: description within 1024 characters | pass |  |
| structural | skill cloudflare-iac-and-api-automation: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-iac-and-api-automation: description within 1024 characters | pass |  |
| structural | skill cloudflare-migration-planning: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-migration-planning: description within 1024 characters | pass |  |
| structural | skill cloudflare-observability-and-troubleshooting: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-observability-and-troubleshooting: description within 1024 characters | pass |  |
| structural | skill cloudflare-solution-architecture: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-solution-architecture: description within 1024 characters | pass |  |
| structural | skill cloudflare-storage-and-state: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-storage-and-state: description within 1024 characters | pass |  |
| structural | skill cloudflare-workers-development: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-workers-development: description within 1024 characters | pass |  |
| structural | skill cloudflare-zero-trust: SKILL.md with name equal to folder | pass |  |
| structural | skill cloudflare-zero-trust: description within 1024 characters | pass |  |
| structural | instruction cloudflare-ci-deploy.instructions.md: description and applyTo | pass |  |
| structural | instruction cloudflare-iac.instructions.md: description and applyTo | pass |  |
| structural | instruction cloudflare-subject-matter-expert-contract.instructions.md: description and applyTo | pass |  |
| structural | instruction cloudflare-workers-config.instructions.md: description and applyTo | pass |  |
| structural | prompt build-agent-or-mcp-server.prompt.md: description | pass |  |
| structural | prompt build-workers-application.prompt.md: description | pass |  |
| structural | prompt deploy-zero-trust-access.prompt.md: description | pass |  |
| structural | prompt design-cloudflare-architecture.prompt.md: description | pass |  |
| structural | prompt plan-cloudflare-migration.prompt.md: description | pass |  |
| structural | prompt release-cloudflare-change.prompt.md: description | pass |  |
| structural | prompt review-cloudflare-change.prompt.md: description | pass |  |
| structural | prompt secure-zone-and-apis.prompt.md: description | pass |  |
| structural | prompt troubleshoot-cloudflare-issue.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/cloudflare-migration-analyst.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/cloudflare-security-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/cloudflare-subject-matter-expert.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/cloudflare-ci-deploy.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/cloudflare-iac.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/cloudflare-subject-matter-expert-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/cloudflare-workers-config.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-agent-or-mcp-server.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-workers-application.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/deploy-zero-trust-access.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-cloudflare-architecture.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/plan-cloudflare-migration.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/release-cloudflare-change.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-cloudflare-change.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/secure-zone-and-apis.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/troubleshoot-cloudflare-issue.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-agents-and-ai/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-application-security/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-change-control/change-plan-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-change-control/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-edge-delivery-and-performance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-iac-and-api-automation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-migration-planning/rule-accounting-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-migration-planning/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-observability-and-troubleshooting/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-solution-architecture/decision-record-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-solution-architecture/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-storage-and-state/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-workers-development/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloudflare-zero-trust/SKILL.md: references only installed things | pass |  |
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
| structural | tests/capability-coverage.yml names every skill exactly once | pass | 11 requirements for 11 skills |
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
