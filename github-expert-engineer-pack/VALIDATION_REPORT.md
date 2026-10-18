# VALIDATION_REPORT

Pack: github-expert-engineer 1.2.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 146  Passed: 145  Failed: 0  Skipped: 1

## Scope

1 agents, 18 skills, 1 instruction files, 10 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | github-expert-engineer vs github-expert-engineer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent github-expert-engineer: name and description present | pass |  |
| structural | agent github-expert-engineer: file name equals name | pass |  |
| structural | agent github-expert-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent github-expert-engineer: description within 1024 characters | pass |  |
| structural | agent github-expert-engineer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill github-actions-debugging-and-troubleshooting: SKILL.md with name equal to folder | pass |  |
| structural | skill github-actions-debugging-and-troubleshooting: description within 1024 characters | pass |  |
| structural | skill github-actions-workflows-and-security: SKILL.md with name equal to folder | pass |  |
| structural | skill github-actions-workflows-and-security: description within 1024 characters | pass |  |
| structural | skill github-api-cli-and-mcp-operations: SKILL.md with name equal to folder | pass |  |
| structural | skill github-api-cli-and-mcp-operations: description within 1024 characters | pass |  |
| structural | skill github-apps-tokens-and-webhooks: SKILL.md with name equal to folder | pass |  |
| structural | skill github-apps-tokens-and-webhooks: description within 1024 characters | pass |  |
| structural | skill github-audit-evidence-and-compliance: SKILL.md with name equal to folder | pass |  |
| structural | skill github-audit-evidence-and-compliance: description within 1024 characters | pass |  |
| structural | skill github-branch-protection-and-rulesets: SKILL.md with name equal to folder | pass |  |
| structural | skill github-branch-protection-and-rulesets: description within 1024 characters | pass |  |
| structural | skill github-ci-cd-and-deployment-environments: SKILL.md with name equal to folder | pass |  |
| structural | skill github-ci-cd-and-deployment-environments: description within 1024 characters | pass |  |
| structural | skill github-copilot-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill github-copilot-engineering: description within 1024 characters | pass |  |
| structural | skill github-documentation-and-repository-contracts: SKILL.md with name equal to folder | pass |  |
| structural | skill github-documentation-and-repository-contracts: description within 1024 characters | pass |  |
| structural | skill github-expert-orchestration: SKILL.md with name equal to folder | pass |  |
| structural | skill github-expert-orchestration: description within 1024 characters | pass |  |
| structural | skill github-issues-discussions-and-projects: SKILL.md with name equal to folder | pass |  |
| structural | skill github-issues-discussions-and-projects: description within 1024 characters | pass |  |
| structural | skill github-migrations-backups-and-recovery: SKILL.md with name equal to folder | pass |  |
| structural | skill github-migrations-backups-and-recovery: description within 1024 characters | pass |  |
| structural | skill github-platform-administration: SKILL.md with name equal to folder | pass |  |
| structural | skill github-platform-administration: description within 1024 characters | pass |  |
| structural | skill github-pull-requests-and-code-review: SKILL.md with name equal to folder | pass |  |
| structural | skill github-pull-requests-and-code-review: description within 1024 characters | pass |  |
| structural | skill github-releases-packages-and-artifacts: SKILL.md with name equal to folder | pass |  |
| structural | skill github-releases-packages-and-artifacts: description within 1024 characters | pass |  |
| structural | skill github-repository-lifecycle-and-governance: SKILL.md with name equal to folder | pass |  |
| structural | skill github-repository-lifecycle-and-governance: description within 1024 characters | pass |  |
| structural | skill github-review-automation-and-hooks: SKILL.md with name equal to folder | pass |  |
| structural | skill github-review-automation-and-hooks: description within 1024 characters | pass |  |
| structural | skill github-security-and-supply-chain: SKILL.md with name equal to folder | pass |  |
| structural | skill github-security-and-supply-chain: description within 1024 characters | pass |  |
| structural | instruction github-expert-engineer-contract.instructions.md: description and applyTo | pass |  |
| structural | prompt assess-release-readiness.prompt.md: description | pass |  |
| structural | prompt audit-security-posture.prompt.md: description | pass |  |
| structural | prompt design-github-integration.prompt.md: description | pass |  |
| structural | prompt diagnose-actions-failure.prompt.md: description | pass |  |
| structural | prompt harden-actions-workflow.prompt.md: description | pass |  |
| structural | prompt plan-migration-or-recovery.prompt.md: description | pass |  |
| structural | prompt query-github-activity.prompt.md: description | pass |  |
| structural | prompt review-copilot-setup.prompt.md: description | pass |  |
| structural | prompt review-pull-request.prompt.md: description | pass |  |
| structural | prompt review-repository-governance.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/github-expert-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/github-expert-engineer-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/assess-release-readiness.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/audit-security-posture.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-github-integration.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/diagnose-actions-failure.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/harden-actions-workflow.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/plan-migration-or-recovery.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/query-github-activity.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-copilot-setup.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-pull-request.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-repository-governance.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-actions-debugging-and-troubleshooting/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-actions-workflows-and-security/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-api-cli-and-mcp-operations/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-apps-tokens-and-webhooks/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-audit-evidence-and-compliance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-branch-protection-and-rulesets/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-ci-cd-and-deployment-environments/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-copilot-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-documentation-and-repository-contracts/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-expert-orchestration/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-issues-discussions-and-projects/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-migrations-backups-and-recovery/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-platform-administration/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-pull-requests-and-code-review/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-releases-packages-and-artifacts/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-repository-lifecycle-and-governance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-review-automation-and-hooks/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/github-security-and-supply-chain/SKILL.md: references only installed things | pass |  |
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
