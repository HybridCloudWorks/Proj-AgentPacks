# VALIDATION_REPORT

Pack: python-distinguished-engineer 2.1.0
Standard: agent-pack-prompt v2.2
Validated: 2026-10-18
Status: PASS

Checks: 190  Passed: 190  Failed: 0  Skipped: 0

## Scope

5 agents, 18 skills, 6 instruction files, 10 prompts; targets copilot, claude, codex, kiro, gemini, agent-skills.

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
| structural | apm.yml name equals the pack folder name without -pack | pass | python-distinguished-engineer vs python-distinguished-engineer-pack |
| structural | apm.yml targets are valid APM targets | pass | targets: ['copilot', 'claude', 'codex', 'kiro', 'gemini', 'agent-skills'] |
| structural | at least one agent | pass |  |
| structural | agent agent-evaluation-engineer: name and description present | pass |  |
| structural | agent agent-evaluation-engineer: file name equals name | pass |  |
| structural | agent agent-evaluation-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent agent-evaluation-engineer: description within 1024 characters | pass |  |
| structural | agent agent-evaluation-engineer: body within 300 lines | pass |  |
| structural | agent python-distinguished-engineer: name and description present | pass |  |
| structural | agent python-distinguished-engineer: file name equals name | pass |  |
| structural | agent python-distinguished-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent python-distinguished-engineer: description within 1024 characters | pass |  |
| structural | agent python-distinguished-engineer: body within 300 lines | pass |  |
| structural | agent python-performance-engineer: name and description present | pass |  |
| structural | agent python-performance-engineer: file name equals name | pass |  |
| structural | agent python-performance-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent python-performance-engineer: description within 1024 characters | pass |  |
| structural | agent python-performance-engineer: body within 300 lines | pass |  |
| structural | agent python-security-reviewer: name and description present | pass |  |
| structural | agent python-security-reviewer: file name equals name | pass |  |
| structural | agent python-security-reviewer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent python-security-reviewer: description within 1024 characters | pass |  |
| structural | agent python-security-reviewer: body within 300 lines | pass |  |
| structural | agent python-test-engineer: name and description present | pass |  |
| structural | agent python-test-engineer: file name equals name | pass |  |
| structural | agent python-test-engineer: no tools field (declared in compatibility/tool-permissions.yml) | pass |  |
| structural | agent python-test-engineer: description within 1024 characters | pass |  |
| structural | agent python-test-engineer: body within 300 lines | pass |  |
| structural | exactly one user-invocable primary agent | pass | user-invocable agents: 1 |
| structural | tool-permissions.yml covers every agent | pass | missing: [] |
| structural | at least one skill | pass |  |
| structural | skill agent-evaluation: SKILL.md with name equal to folder | pass |  |
| structural | skill agent-evaluation: description within 1024 characters | pass |  |
| structural | skill agent-observability: SKILL.md with name equal to folder | pass |  |
| structural | skill agent-observability: description within 1024 characters | pass |  |
| structural | skill agentic-workflow-design: SKILL.md with name equal to folder | pass |  |
| structural | skill agentic-workflow-design: description within 1024 characters | pass |  |
| structural | skill architecture-decision-records: SKILL.md with name equal to folder | pass |  |
| structural | skill architecture-decision-records: description within 1024 characters | pass |  |
| structural | skill mcp-python-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill mcp-python-engineering: description within 1024 characters | pass |  |
| structural | skill playwright-validation: SKILL.md with name equal to folder | pass |  |
| structural | skill playwright-validation: description within 1024 characters | pass |  |
| structural | skill pull-request-review: SKILL.md with name equal to folder | pass |  |
| structural | skill pull-request-review: description within 1024 characters | pass |  |
| structural | skill python-api-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill python-api-engineering: description within 1024 characters | pass |  |
| structural | skill python-async-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill python-async-engineering: description within 1024 characters | pass |  |
| structural | skill python-cli-automation: SKILL.md with name equal to folder | pass |  |
| structural | skill python-cli-automation: description within 1024 characters | pass |  |
| structural | skill python-data-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill python-data-engineering: description within 1024 characters | pass |  |
| structural | skill python-database-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill python-database-engineering: description within 1024 characters | pass |  |
| structural | skill python-language-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill python-language-engineering: description within 1024 characters | pass |  |
| structural | skill python-packaging: SKILL.md with name equal to folder | pass |  |
| structural | skill python-packaging: description within 1024 characters | pass |  |
| structural | skill python-performance-analysis: SKILL.md with name equal to folder | pass |  |
| structural | skill python-performance-analysis: description within 1024 characters | pass |  |
| structural | skill python-static-typing: SKILL.md with name equal to folder | pass |  |
| structural | skill python-static-typing: description within 1024 characters | pass |  |
| structural | skill secure-agent-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill secure-agent-engineering: description within 1024 characters | pass |  |
| structural | skill secure-python-engineering: SKILL.md with name equal to folder | pass |  |
| structural | skill secure-python-engineering: description within 1024 characters | pass |  |
| structural | instruction agentic-security.instructions.md: description and applyTo | pass |  |
| structural | instruction python-engineering-contract.instructions.md: description and applyTo | pass |  |
| structural | instruction python-packaging.instructions.md: description and applyTo | pass |  |
| structural | instruction python-security.instructions.md: description and applyTo | pass |  |
| structural | instruction python-tests.instructions.md: description and applyTo | pass |  |
| structural | instruction python.instructions.md: description and applyTo | pass |  |
| structural | prompt build-mcp-server.prompt.md: description | pass |  |
| structural | prompt build-python-api.prompt.md: description | pass |  |
| structural | prompt debug-python-issue.prompt.md: description | pass |  |
| structural | prompt design-change.prompt.md: description | pass |  |
| structural | prompt evaluate-agent.prompt.md: description | pass |  |
| structural | prompt implement-feature.prompt.md: description | pass |  |
| structural | prompt investigate-repository.prompt.md: description | pass |  |
| structural | prompt modernize-python-code.prompt.md: description | pass |  |
| structural | prompt review-pull-request.prompt.md: description | pass |  |
| structural | prompt validate-web-flow.prompt.md: description | pass |  |
| structural | authoring prompt is version 2.2 or later | pass |  |
| structural | installed content .apm/agents/agent-evaluation-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/python-distinguished-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/python-performance-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/python-security-reviewer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/agents/python-test-engineer.agent.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/agentic-security.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/python-engineering-contract.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/python-packaging.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/python-security.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/python-tests.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/instructions/python.instructions.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-mcp-server.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/build-python-api.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/debug-python-issue.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/design-change.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/evaluate-agent.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/implement-feature.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/investigate-repository.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/modernize-python-code.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/review-pull-request.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/prompts/validate-web-flow.prompt.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-evaluation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agent-observability/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/agentic-workflow-design/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/architecture-decision-records/adr-template.md: references only installed things | pass |  |
| structural | installed content .apm/skills/architecture-decision-records/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/mcp-python-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/playwright-validation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/pull-request-review/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-api-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-async-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-cli-automation/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-data-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-database-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-language-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-packaging/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-performance-analysis/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/python-static-typing/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/secure-agent-engineering/SKILL.md: references only installed things | pass |  |
| structural | installed content .apm/skills/secure-python-engineering/SKILL.md: references only installed things | pass |  |
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
| structural | capability-coverage.yml names every skill exactly once | pass | 18 requirements for 18 skills |
| structural | capability-coverage.yml prompts exist | pass |  |
| structural | capability-coverage.yml agents exist | pass |  |
| structural | trigger-cases.yml covers every skill | pass |  |
| structural | trigger-cases.yml names only real skills | pass |  |
| structural | trigger-cases.yml prompts exist | pass |  |
| structural | an always-on contract instruction exists (.apm/instructions/*contract*.instructions.md) | pass |  |
| structural | contract instruction states every report field, status and severity from report-contract.yml | pass |  |
| structural | contract instruction states the fallback sentence | pass |  |
| executable | pack unit tests (python -m unittest discover -s tests) | pass | OK |
| executable | apm compile --validate | pass | [*] All primitives validated successfully! |
| executable | apm install --target copilot,claude,codex,kiro,gemini,agent-skills succeeds | pass |  |
| executable | copilot: 5 agents generated | pass | found 5 |
| executable | claude: 5 agents generated | pass | found 5 |
| executable | codex: 5 agents generated | pass | found 5 |
| executable | kiro: 5 agents generated | pass | found 5 |
| executable | no hook files generated | pass |  |
| executable | claude: instructions generated as rules | pass | found 6 |
| executable | generated vendor files reference only installed things | pass |  |
