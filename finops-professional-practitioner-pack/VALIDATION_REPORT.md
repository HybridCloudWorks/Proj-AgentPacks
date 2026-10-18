# VALIDATION_REPORT

Pack: finops-professional-practitioner 1.0.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 151  Passed: 151  Failed: 0  Skipped: 0

## Scope

3 agents, 8 skills, 3 instruction files, 11 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | finops-professional-practitioner vs finops-professional-practitioner-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent finops-data-analyst: name and description present | pass |  |
| structural | agent finops-data-analyst: file name equals name | pass |  |
| structural | agent finops-data-analyst: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent finops-data-analyst: description within 1024 characters | pass |  |
| structural | agent finops-data-analyst: body within 300 lines | pass |  |
| structural | agent finops-evidence-reviewer: name and description present | pass |  |
| structural | agent finops-evidence-reviewer: file name equals name | pass |  |
| structural | agent finops-evidence-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent finops-evidence-reviewer: description within 1024 characters | pass |  |
| structural | agent finops-evidence-reviewer: body within 300 lines | pass |  |
| structural | agent finops-professional-practitioner: name and description present | pass |  |
| structural | agent finops-professional-practitioner: file name equals name | pass |  |
| structural | agent finops-professional-practitioner: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent finops-professional-practitioner: description within 1024 characters | pass |  |
| structural | agent finops-professional-practitioner: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill cost-allocation-and-chargeback: SKILL.md with name equal to folder | pass |  |
| structural | skill cost-allocation-and-chargeback: description within 1024 characters | pass |  |
| structural | skill cost-anomaly-management: SKILL.md with name equal to folder | pass |  |
| structural | skill cost-anomaly-management: description within 1024 characters | pass |  |
| structural | skill finops-maturity-assessment: SKILL.md with name equal to folder | pass |  |
| structural | skill finops-maturity-assessment: description within 1024 characters | pass |  |
| structural | skill finops-practice-governance: SKILL.md with name equal to folder | pass |  |
| structural | skill finops-practice-governance: description within 1024 characters | pass |  |
| structural | skill focus-billing-data-analysis: SKILL.md with name equal to folder | pass |  |
| structural | skill focus-billing-data-analysis: description within 1024 characters | pass |  |
| structural | skill forecasting-and-unit-economics: SKILL.md with name equal to folder | pass |  |
| structural | skill forecasting-and-unit-economics: description within 1024 characters | pass |  |
| structural | skill rate-optimization: SKILL.md with name equal to folder | pass |  |
| structural | skill rate-optimization: description within 1024 characters | pass |  |
| structural | skill workload-optimization: SKILL.md with name equal to folder | pass |  |
| structural | skill workload-optimization: description within 1024 characters | pass |  |
| structural | instruction billing-data-files.instructions.md: description and applyTo | pass |  |
| structural | instruction finops-professional-practitioner-contract.instructions.md: description and applyTo | pass |  |
| structural | instruction focus-cost-queries.instructions.md: description and applyTo | pass |  |
| structural | prompt analyze-cloud-spend.prompt.md: description | pass |  |
| structural | prompt assess-finops-maturity.prompt.md: description | pass |  |
| structural | prompt build-cost-forecast.prompt.md: description | pass |  |
| structural | prompt design-allocation-model.prompt.md: description | pass |  |
| structural | prompt draft-finops-policy.prompt.md: description | pass |  |
| structural | prompt estimate-workload-cost.prompt.md: description | pass |  |
| structural | prompt find-optimization-opportunities.prompt.md: description | pass |  |
| structural | prompt investigate-cost-anomaly.prompt.md: description | pass |  |
| structural | prompt plan-commitment-strategy.prompt.md: description | pass |  |
| structural | prompt reconcile-billing-data.prompt.md: description | pass |  |
| structural | prompt review-savings-claim.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/finops-data-analyst.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/finops-evidence-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/finops-professional-practitioner.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/billing-data-files.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/finops-professional-practitioner-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/focus-cost-queries.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/analyze-cloud-spend.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/assess-finops-maturity.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-cost-forecast.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-allocation-model.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/draft-finops-policy.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/estimate-workload-cost.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/find-optimization-opportunities.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/investigate-cost-anomaly.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/plan-commitment-strategy.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/reconcile-billing-data.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-savings-claim.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cost-allocation-and-chargeback/allocation-methodology-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cost-allocation-and-chargeback/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cost-anomaly-management/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/finops-maturity-assessment/capability-scorecard.md: references only installed things | pass |  |
| structural | installed content .apm/skills/finops-maturity-assessment/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/finops-practice-governance/policy-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/finops-practice-governance/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/focus-billing-data-analysis/focus-column-reference.md: references only installed things | pass |  |
| structural | installed content .apm/skills/focus-billing-data-analysis/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/forecasting-and-unit-economics/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/rate-optimization/commitment-recommendation-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/rate-optimization/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/workload-optimization/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/workload-optimization/waste-pattern-catalog.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/AGENT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/APPROVAL_MATRIX.md: describes the current layout | pass |  |
| structural | pack doc docs/EVALUATION_PLAN.md: describes the current layout | pass |  |
| structural | pack doc docs/HANDOFF_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/INTEGRATION_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/MAINTENANCE.md: describes the current layout | pass |  |
| structural | pack doc docs/PROMPT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/SECURITY_AND_DATA_HANDLING.md: describes the current layout | pass |  |
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
| structural | tests/capability-coverage.yml names every skill exactly once | pass | 8 requirements for 8 skills |
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
