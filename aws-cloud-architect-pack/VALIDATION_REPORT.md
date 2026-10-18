# VALIDATION_REPORT

Pack: aws-cloud-architect 1.3.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 150  Passed: 149  Failed: 0  Skipped: 1

## Scope

1 agents, 17 skills, 1 instruction files, 10 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | aws-cloud-architect vs aws-cloud-architect-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent aws-cloud-architect: name and description present | pass |  |
| structural | agent aws-cloud-architect: file name equals name | pass |  |
| structural | agent aws-cloud-architect: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent aws-cloud-architect: description within 1024 characters | pass |  |
| structural | agent aws-cloud-architect: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill aws-architecture-foundations: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-architecture-foundations: description within 1024 characters | pass |  |
| structural | skill aws-architecture-handoff-and-adr: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-architecture-handoff-and-adr: description within 1024 characters | pass |  |
| structural | skill aws-architecture-visualization: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-architecture-visualization: description within 1024 characters | pass |  |
| structural | skill aws-caf-landing-zones-and-governance: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-caf-landing-zones-and-governance: description within 1024 characters | pass |  |
| structural | skill aws-cost-sustainability-and-finops: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-cost-sustainability-and-finops: description within 1024 characters | pass |  |
| structural | skill aws-data-and-application-patterns: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-data-and-application-patterns: description within 1024 characters | pass |  |
| structural | skill aws-docs-mcp-and-evidence: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-docs-mcp-and-evidence: description within 1024 characters | pass |  |
| structural | skill aws-iac-deployment-and-lifecycle: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-iac-deployment-and-lifecycle: description within 1024 characters | pass |  |
| structural | skill aws-networking-hybrid-and-edge: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-networking-hybrid-and-edge: description within 1024 characters | pass |  |
| structural | skill aws-operations-observability-and-troubleshooting: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-operations-observability-and-troubleshooting: description within 1024 characters | pass |  |
| structural | skill aws-resilience-dr-and-migration: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-resilience-dr-and-migration: description within 1024 characters | pass |  |
| structural | skill aws-security-identity-and-compliance: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-security-identity-and-compliance: description within 1024 characters | pass |  |
| structural | skill aws-well-architected-and-frameworks: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-well-architected-and-frameworks: description within 1024 characters | pass |  |
| structural | skill aws-workload-and-service-selection: SKILL.md with name equal to folder | pass |  |
| structural | skill aws-workload-and-service-selection: description within 1024 characters | pass |  |
| structural | skill diagram-validation-and-evidence: SKILL.md with name equal to folder | pass |  |
| structural | skill diagram-validation-and-evidence: description within 1024 characters | pass |  |
| structural | skill drawio-core-generation: SKILL.md with name equal to folder | pass |  |
| structural | skill drawio-core-generation: description within 1024 characters | pass |  |
| structural | skill drawio-render-export-and-review: SKILL.md with name equal to folder | pass |  |
| structural | skill drawio-render-export-and-review: description within 1024 characters | pass |  |
| structural | instruction aws-cloud-architect-contract.instructions.md: description and applyTo | pass |  |
| structural | prompt create-architecture-diagram.prompt.md: description | pass |  |
| structural | prompt design-aws-workload.prompt.md: description | pass |  |
| structural | prompt design-hybrid-network.prompt.md: description | pass |  |
| structural | prompt design-landing-zone.prompt.md: description | pass |  |
| structural | prompt plan-migration-and-dr.prompt.md: description | pass |  |
| structural | prompt review-aws-cost.prompt.md: description | pass |  |
| structural | prompt review-deployment-plan.prompt.md: description | pass |  |
| structural | prompt review-well-architected.prompt.md: description | pass |  |
| structural | prompt troubleshoot-aws-incident.prompt.md: description | pass |  |
| structural | prompt verify-aws-evidence.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/aws-cloud-architect.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/aws-cloud-architect-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/create-architecture-diagram.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-aws-workload.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-hybrid-network.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-landing-zone.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/plan-migration-and-dr.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-aws-cost.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-deployment-plan.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-well-architected.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/troubleshoot-aws-incident.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/verify-aws-evidence.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-architecture-foundations/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-architecture-handoff-and-adr/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-architecture-visualization/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-caf-landing-zones-and-governance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-cost-sustainability-and-finops/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-data-and-application-patterns/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-docs-mcp-and-evidence/references/mcp-routing.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-docs-mcp-and-evidence/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-iac-deployment-and-lifecycle/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-networking-hybrid-and-edge/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-operations-observability-and-troubleshooting/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-resilience-dr-and-migration/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-security-identity-and-compliance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-well-architected-and-frameworks/references/framework-routing.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-well-architected-and-frameworks/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/aws-workload-and-service-selection/SKILL.md: references only installed things | pass |  |
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
| structural | pack doc docs/SKILL_INVENTORY.md: describes the current layout | pass |  |
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
