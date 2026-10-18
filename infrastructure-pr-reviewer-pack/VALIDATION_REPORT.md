# VALIDATION_REPORT

Pack: infrastructure-pr-reviewer 1.1.0
Standard: agent-pack-prompt v2.2
Validated: 2026-10-18
Status: PASS

Checks: 116  Passed: 115  Failed: 0  Skipped: 1

## Scope

1 agents, 8 skills, 2 instruction files, 0 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | infrastructure-pr-reviewer vs infrastructure-pr-reviewer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent infrastructure-pr-reviewer: name and description present | pass |  |
| structural | agent infrastructure-pr-reviewer: file name equals name | pass |  |
| structural | agent infrastructure-pr-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent infrastructure-pr-reviewer: description within 1024 characters | pass |  |
| structural | agent infrastructure-pr-reviewer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill review-ansible-automation: SKILL.md with name equal to folder | pass |  |
| structural | skill review-ansible-automation: description within 1024 characters | pass |  |
| structural | skill review-bicep-arm: SKILL.md with name equal to folder | pass |  |
| structural | skill review-bicep-arm: description within 1024 characters | pass |  |
| structural | skill review-cicd-deployment: SKILL.md with name equal to folder | pass |  |
| structural | skill review-cicd-deployment: description within 1024 characters | pass |  |
| structural | skill review-infrastructure-pr: SKILL.md with name equal to folder | pass |  |
| structural | skill review-infrastructure-pr: description within 1024 characters | pass |  |
| structural | skill review-kubernetes-packaging: SKILL.md with name equal to folder | pass |  |
| structural | skill review-kubernetes-packaging: description within 1024 characters | pass |  |
| structural | skill review-powershell-automation: SKILL.md with name equal to folder | pass |  |
| structural | skill review-powershell-automation: description within 1024 characters | pass |  |
| structural | skill review-terraform-opentofu: SKILL.md with name equal to folder | pass |  |
| structural | skill review-terraform-opentofu: description within 1024 characters | pass |  |
| structural | skill verify-infrastructure-evidence: SKILL.md with name equal to folder | pass |  |
| structural | skill verify-infrastructure-evidence: description within 1024 characters | pass |  |
| structural | instruction infrastructure-pr-reviewer-contract.instructions.md: description and applyTo | pass |  |
| structural | instruction infrastructure-review.instructions.md: description and applyTo | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/infrastructure-pr-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/infrastructure-pr-reviewer-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/infrastructure-review.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-ansible-automation/references/official-sources.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-ansible-automation/references/review-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-ansible-automation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-bicep-arm/references/official-sources.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-bicep-arm/references/review-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-bicep-arm/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-cicd-deployment/references/official-sources.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-cicd-deployment/references/review-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-cicd-deployment/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-infrastructure-pr/assets/infrastructure-pull-request-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-infrastructure-pr/assets/repository-enforcement-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-infrastructure-pr/assets/review-report-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-infrastructure-pr/references/github-copilot-setup.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-infrastructure-pr/references/review-protocol.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-infrastructure-pr/references/severity-and-output.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-infrastructure-pr/references/universal-gates.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-infrastructure-pr/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-kubernetes-packaging/references/official-sources.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-kubernetes-packaging/references/review-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-kubernetes-packaging/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-powershell-automation/references/official-sources.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-powershell-automation/references/review-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-powershell-automation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-terraform-opentofu/references/official-sources.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-terraform-opentofu/references/review-checklist.md: references only installed things | pass |  |
| structural | installed content .apm/skills/review-terraform-opentofu/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/verify-infrastructure-evidence/references/evidence-matrix.md: references only installed things | pass |  |
| structural | installed content .apm/skills/verify-infrastructure-evidence/references/official-sources.md: references only installed things | pass |  |
| structural | installed content .apm/skills/verify-infrastructure-evidence/SKILL.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
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
| executable | claude: instructions generated as rules | pass | found 2 |
| executable | generated vendor files reference only installed things | pass |  |
