# VALIDATION_REPORT

Pack: google-cloud-architect 1.1.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 183  Passed: 183  Failed: 0  Skipped: 0

## Scope

3 agents, 20 skills, 3 instruction files, 10 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | google-cloud-architect vs google-cloud-architect-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent gcp-estate-inspector: name and description present | pass |  |
| structural | agent gcp-estate-inspector: file name equals name | pass |  |
| structural | agent gcp-estate-inspector: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent gcp-estate-inspector: description within 1024 characters | pass |  |
| structural | agent gcp-estate-inspector: body within 300 lines | pass |  |
| structural | agent gcp-security-reviewer: name and description present | pass |  |
| structural | agent gcp-security-reviewer: file name equals name | pass |  |
| structural | agent gcp-security-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent gcp-security-reviewer: description within 1024 characters | pass |  |
| structural | agent gcp-security-reviewer: body within 300 lines | pass |  |
| structural | agent google-cloud-architect: name and description present | pass |  |
| structural | agent google-cloud-architect: file name equals name | pass |  |
| structural | agent google-cloud-architect: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent google-cloud-architect: description within 1024 characters | pass |  |
| structural | agent google-cloud-architect: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill diagram-validation-and-evidence: SKILL.md with name equal to folder | pass |  |
| structural | skill diagram-validation-and-evidence: description within 1024 characters | pass |  |
| structural | skill drawio-core-generation: SKILL.md with name equal to folder | pass |  |
| structural | skill drawio-core-generation: description within 1024 characters | pass |  |
| structural | skill drawio-render-export-and-review: SKILL.md with name equal to folder | pass |  |
| structural | skill drawio-render-export-and-review: description within 1024 characters | pass |  |
| structural | skill gcp-ai-agent-architecture: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-ai-agent-architecture: description within 1024 characters | pass |  |
| structural | skill gcp-architecture-decisions: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-architecture-decisions: description within 1024 characters | pass |  |
| structural | skill gcp-cost-sustainability: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-cost-sustainability: description within 1024 characters | pass |  |
| structural | skill gcp-data-analytics: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-data-analytics: description within 1024 characters | pass |  |
| structural | skill gcp-estate-discovery: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-estate-discovery: description within 1024 characters | pass |  |
| structural | skill gcp-gke-platform: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-gke-platform: description within 1024 characters | pass |  |
| structural | skill gcp-iac-validation: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-iac-validation: description within 1024 characters | pass |  |
| structural | skill gcp-identity-access: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-identity-access: description within 1024 characters | pass |  |
| structural | skill gcp-landing-zone: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-landing-zone: description within 1024 characters | pass |  |
| structural | skill gcp-migration-planning: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-migration-planning: description within 1024 characters | pass |  |
| structural | skill gcp-network-design: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-network-design: description within 1024 characters | pass |  |
| structural | skill gcp-observability-operations: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-observability-operations: description within 1024 characters | pass |  |
| structural | skill gcp-reliability-dr: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-reliability-dr: description within 1024 characters | pass |  |
| structural | skill gcp-security-controls: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-security-controls: description within 1024 characters | pass |  |
| structural | skill gcp-serverless-apps: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-serverless-apps: description within 1024 characters | pass |  |
| structural | skill gcp-solution-architecture: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-solution-architecture: description within 1024 characters | pass |  |
| structural | skill gcp-well-architected-review: SKILL.md with name equal to folder | pass |  |
| structural | skill gcp-well-architected-review: description within 1024 characters | pass |  |
| structural | instruction gcp-cli-scripts.instructions.md: description and applyTo | pass |  |
| structural | instruction gcp-terraform.instructions.md: description and applyTo | pass |  |
| structural | instruction google-cloud-architect-contract.instructions.md: description and applyTo | pass |  |
| structural | prompt create-architecture-diagram.prompt.md: description | pass |  |
| structural | prompt design-landing-zone.prompt.md: description | pass |  |
| structural | prompt design-network.prompt.md: description | pass |  |
| structural | prompt design-solution.prompt.md: description | pass |  |
| structural | prompt optimize-cost.prompt.md: description | pass |  |
| structural | prompt plan-migration.prompt.md: description | pass |  |
| structural | prompt plan-resilience.prompt.md: description | pass |  |
| structural | prompt record-decision.prompt.md: description | pass |  |
| structural | prompt review-architecture.prompt.md: description | pass |  |
| structural | prompt validate-iac.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/gcp-estate-inspector.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/gcp-security-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/google-cloud-architect.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/gcp-cli-scripts.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/gcp-terraform.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/google-cloud-architect-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/create-architecture-diagram.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-landing-zone.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-network.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-solution.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/optimize-cost.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/plan-migration.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/plan-resilience.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/record-decision.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-architecture.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/validate-iac.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/diagram-validation-and-evidence/references/provider-checks.md: references only installed things | pass |  |
| structural | installed content .apm/skills/diagram-validation-and-evidence/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-core-generation/references/providers.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-core-generation/references/upstream-routing.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-core-generation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-render-export-and-review/references/export-cli.md: references only installed things | pass |  |
| structural | installed content .apm/skills/drawio-render-export-and-review/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-ai-agent-architecture/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-architecture-decisions/decision-record-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-architecture-decisions/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-cost-sustainability/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-data-analytics/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-estate-discovery/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-gke-platform/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-iac-validation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-identity-access/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-landing-zone/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-migration-planning/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-network-design/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-observability-operations/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-reliability-dr/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-security-controls/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-serverless-apps/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-solution-architecture/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-solution-architecture/solution-guide-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/gcp-well-architected-review/SKILL.md: references only installed things | pass |  |
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
| structural | tests/capability-coverage.yml names every skill exactly once | pass | 20 requirements for 20 skills |
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
| executable | claude: instructions generated as rules | pass | found 3 |
| executable | generated vendor files reference only installed things | pass |  |
