# VALIDATION_REPORT

Pack: typescript-distinguished-engineer 1.4.0
Standard: agent-pack-prompt v2.3
Validated: 2026-10-18
Status: PASS

Checks: 193  Passed: 192  Failed: 0  Skipped: 1

## Scope

4 agents, 20 skills, 6 instruction files, 9 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | typescript-distinguished-engineer vs typescript-distinguished-engineer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent agent-evaluation-engineer: name and description present | pass |  |
| structural | agent agent-evaluation-engineer: file name equals name | pass |  |
| structural | agent agent-evaluation-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent agent-evaluation-engineer: description within 1024 characters | pass |  |
| structural | agent agent-evaluation-engineer: body within 300 lines | pass |  |
| structural | agent typescript-distinguished-engineer: name and description present | pass |  |
| structural | agent typescript-distinguished-engineer: file name equals name | pass |  |
| structural | agent typescript-distinguished-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent typescript-distinguished-engineer: description within 1024 characters | pass |  |
| structural | agent typescript-distinguished-engineer: body within 300 lines | pass |  |
| structural | agent typescript-security-reviewer: name and description present | pass |  |
| structural | agent typescript-security-reviewer: file name equals name | pass |  |
| structural | agent typescript-security-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent typescript-security-reviewer: description within 1024 characters | pass |  |
| structural | agent typescript-security-reviewer: body within 300 lines | pass |  |
| structural | agent typescript-test-engineer: name and description present | pass |  |
| structural | agent typescript-test-engineer: file name equals name | pass |  |
| structural | agent typescript-test-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent typescript-test-engineer: description within 1024 characters | pass |  |
| structural | agent typescript-test-engineer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill agent-evaluation: SKILL.md with name equal to folder | pass |  |
| structural | skill agent-evaluation: description within 1024 characters | pass |  |
| structural | skill agent-observability-and-telemetry: SKILL.md with name equal to folder | pass |  |
| structural | skill agent-observability-and-telemetry: description within 1024 characters | pass |  |
| structural | skill agent-state-and-context-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill agent-state-and-context-engineering: description within 1024 characters | pass |  |
| structural | skill agentic-cost-and-budget-controls: SKILL.md with name equal to folder | pass |  |
| structural | skill agentic-cost-and-budget-controls: description within 1024 characters | pass |  |
| structural | skill agentic-workflow-design: SKILL.md with name equal to folder | pass |  |
| structural | skill agentic-workflow-design: description within 1024 characters | pass |  |
| structural | skill api-contract-and-integration-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill api-contract-and-integration-engineering: description within 1024 characters | pass |  |
| structural | skill cloud-integration-and-identity: SKILL.md with name equal to folder | pass |  |
| structural | skill cloud-integration-and-identity: description within 1024 characters | pass |  |
| structural | skill dependency-supply-chain-and-reproducibility: SKILL.md with name equal to folder | pass |  |
| structural | skill dependency-supply-chain-and-reproducibility: description within 1024 characters | pass |  |
| structural | skill enterprise-architecture-and-adr: SKILL.md with name equal to folder | pass |  |
| structural | skill enterprise-architecture-and-adr: description within 1024 characters | pass |  |
| structural | skill frontend-react-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill frontend-react-engineering: description within 1024 characters | pass |  |
| structural | skill javascript-node-runtime-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill javascript-node-runtime-engineering: description within 1024 characters | pass |  |
| structural | skill layered-testing-and-test-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill layered-testing-and-test-engineering: description within 1024 characters | pass |  |
| structural | skill mcp-typescript-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill mcp-typescript-engineering: description within 1024 characters | pass |  |
| structural | skill performance-reliability-and-operability: SKILL.md with name equal to folder | pass |  |
| structural | skill performance-reliability-and-operability: description within 1024 characters | pass |  |
| structural | skill playwright-validation: SKILL.md with name equal to folder | pass |  |
| structural | skill playwright-validation: description within 1024 characters | pass |  |
| structural | skill pull-request-review-and-delivery: SKILL.md with name equal to folder | pass |  |
| structural | skill pull-request-review-and-delivery: description within 1024 characters | pass |  |
| structural | skill requirements-and-change-planning: SKILL.md with name equal to folder | pass |  |
| structural | skill requirements-and-change-planning: description within 1024 characters | pass |  |
| structural | skill secure-agent-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill secure-agent-engineering: description within 1024 characters | pass |  |
| structural | skill typescript-distinguished-engineer-orchestration: SKILL.md with name equal to folder | pass |  |
| structural | skill typescript-distinguished-engineer-orchestration: description within 1024 characters | pass |  |
| structural | skill typescript-strict-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill typescript-strict-engineering: description within 1024 characters | pass |  |
| structural | instruction agentic-security.instructions.md: description and applyTo | pass |  |
| structural | instruction evidence-completion.instructions.md: description and applyTo | pass |  |
| structural | instruction repository-discovery.instructions.md: description and applyTo | pass |  |
| structural | instruction tests.instructions.md: description and applyTo | pass |  |
| structural | instruction typescript-distinguished-engineer-contract.instructions.md: description and applyTo | pass |  |
| structural | instruction typescript.instructions.md: description and applyTo | pass |  |
| structural | prompt build-typescript-mcp-server.prompt.md: description | pass |  |
| structural | prompt design-agentic-system.prompt.md: description | pass |  |
| structural | prompt design-typescript-change.prompt.md: description | pass |  |
| structural | prompt diagnose-failure.prompt.md: description | pass |  |
| structural | prompt evaluate-agent.prompt.md: description | pass |  |
| structural | prompt implement-typescript-feature.prompt.md: description | pass |  |
| structural | prompt release-readiness.prompt.md: description | pass |  |
| structural | prompt review-typescript-pull-request.prompt.md: description | pass |  |
| structural | prompt validate-web-flow.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/agent-evaluation-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/typescript-distinguished-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/typescript-security-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/typescript-test-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/agentic-security.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/evidence-completion.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/repository-discovery.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/tests.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/typescript-distinguished-engineer-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/typescript.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-typescript-mcp-server.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-agentic-system.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-typescript-change.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/diagnose-failure.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/evaluate-agent.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/implement-typescript-feature.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/release-readiness.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-typescript-pull-request.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/validate-web-flow.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-evaluation/references/python.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-evaluation/references/typescript.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-evaluation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-observability-and-telemetry/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-state-and-context-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agentic-cost-and-budget-controls/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agentic-workflow-design/references/python.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agentic-workflow-design/references/typescript.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agentic-workflow-design/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/api-contract-and-integration-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/cloud-integration-and-identity/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/dependency-supply-chain-and-reproducibility/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/enterprise-architecture-and-adr/adr-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/enterprise-architecture-and-adr/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/frontend-react-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/javascript-node-runtime-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/layered-testing-and-test-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/mcp-typescript-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/performance-reliability-and-operability/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/playwright-validation/references/python.md: references only installed things | pass |  |
| structural | installed content .apm/skills/playwright-validation/references/typescript.md: references only installed things | pass |  |
| structural | installed content .apm/skills/playwright-validation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/pull-request-review-and-delivery/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/requirements-and-change-planning/adr-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/requirements-and-change-planning/handoff-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/requirements-and-change-planning/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/secure-agent-engineering/references/python.md: references only installed things | pass |  |
| structural | installed content .apm/skills/secure-agent-engineering/references/typescript.md: references only installed things | pass |  |
| structural | installed content .apm/skills/secure-agent-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/typescript-distinguished-engineer-orchestration/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/typescript-strict-engineering/SKILL.md: references only installed things | pass |  |
| structural | pack doc README.md: describes the current layout | pass |  |
| structural | pack doc DESCRIPTION.md: describes the current layout | pass |  |
| structural | pack doc hooks/README.md: describes the current layout | pass |  |
| structural | pack doc docs/AGENT_HANDOFF_CONTRACT.md: describes the current layout | pass |  |
| structural | pack doc docs/APPROVAL_MATRIX.md: describes the current layout | pass |  |
| structural | pack doc docs/END_TO_END_WORKFLOW.md: describes the current layout | pass |  |
| structural | pack doc docs/GOVERNANCE.md: describes the current layout | pass |  |
| structural | pack doc docs/PROMPT_INVENTORY.md: describes the current layout | pass |  |
| structural | pack doc docs/SOURCE_TRACEABILITY.md: describes the current layout | pass |  |
| structural | pack doc docs/TOOL_PERMISSION_MATRIX.md: describes the current layout | pass |  |
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
| executable | copilot: 4 agents generated | pass | found 4 |
| executable | claude: 4 agents generated | pass | found 4 |
| executable | codex: 4 agents generated | pass | found 4 |
| executable | kiro: 4 agents generated | pass | found 4 |
| executable | no hook files generated | pass |  |
| executable | claude: instructions generated as rules | pass | found 6 |
| executable | generated vendor files reference only installed things | pass |  |
