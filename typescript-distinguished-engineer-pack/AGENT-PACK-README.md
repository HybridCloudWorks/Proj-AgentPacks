# typescript-distinguished-engineer 1.4.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| agent-evaluation-engineer.agent.md | Canonical agent: Evaluation specialist for agentic systems written in Python or TypeScript; designs and runs scoped outcome and process evaluations, safety cases, rubrics, cost checks and human-review gates. | .apm/agents/agent-evaluation-engineer.agent.md |
| typescript-distinguished-engineer.agent.md | Canonical agent: Hands-on Distinguished Engineer for enterprise TypeScript and JavaScript systems, Node.js, React, APIs, MCP, agentic applications, testing, security, operations, and evidence-based delivery. | .apm/agents/typescript-distinguished-engineer.agent.md |
| typescript-security-reviewer.agent.md | Canonical agent: Read-only security reviewer for TypeScript, Node.js, React, APIs, MCP servers and clients, agentic workflows, dependencies, and CI/CD trust boundaries. | .apm/agents/typescript-security-reviewer.agent.md |
| typescript-test-engineer.agent.md | Canonical agent: Test engineering specialist for TypeScript, Node.js, React, APIs, integration boundaries, and Playwright browser journeys. | .apm/agents/typescript-test-engineer.agent.md |
| agentic-security.instructions.md | Canonical instruction: Security boundaries for agents, MCP tools and AI workflows in Python and TypeScript: untrusted content, authorization outside the model, approvals, tenant isolation, limits, redaction and each language's dangerous APIs. | .apm/instructions/agentic-security.instructions.md |
| evidence-completion.instructions.md | Canonical instruction: Before using a success label, compare every acceptance criterion with observed evidence. Report files changed, commands and results, security review status, operational and cost impact, unverified ite | .apm/instructions/evidence-completion.instructions.md |
| repository-discovery.instructions.md | Canonical instruction: Inspect repository-level instructions, contribution policies, manifests, lockfiles, TypeScript configuration, build and test scripts, CI, deployment descriptors, architecture records, and recent patte | .apm/instructions/repository-discovery.instructions.md |
| tests.instructions.md | Canonical instruction: Choose the cheapest test layer that proves the behavior: unit, contract, integration, browser end-to-end, security, performance, or regression. Test invalid input, authorization, timeouts, retries, pa | .apm/instructions/tests.instructions.md |
| typescript-distinguished-engineer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the typescript distinguished engineer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/typescript-distinguished-engineer-contract.instructions.md |
| typescript.instructions.md | Canonical instruction: Prefer the repository's supported TypeScript or JavaScript runtime and module system. Use strict typing, explicit public contracts, runtime validation at untrusted boundaries, safe narrowing, clear er | .apm/instructions/typescript.instructions.md |
| build-typescript-mcp-server.prompt.md | Canonical prompt: Build or Review an MCP Server | .apm/prompts/build-typescript-mcp-server.prompt.md |
| design-agentic-system.prompt.md | Canonical prompt: Design an Agentic System | .apm/prompts/design-agentic-system.prompt.md |
| design-typescript-change.prompt.md | Canonical prompt: Design a Change | .apm/prompts/design-typescript-change.prompt.md |
| diagnose-failure.prompt.md | Canonical prompt: Diagnose a Failure | .apm/prompts/diagnose-failure.prompt.md |
| evaluate-agent.prompt.md | Canonical prompt: Evaluate an agent workflow written in Python or TypeScript: scenarios, deterministic and judged checks, budgets, cost and a release recommendation | .apm/prompts/evaluate-agent.prompt.md |
| implement-typescript-feature.prompt.md | Canonical prompt: Implement a Feature | .apm/prompts/implement-typescript-feature.prompt.md |
| release-readiness.prompt.md | Canonical prompt: Assess Release Readiness | .apm/prompts/release-readiness.prompt.md |
| review-typescript-pull-request.prompt.md | Canonical prompt: Review a Pull Request | .apm/prompts/review-typescript-pull-request.prompt.md |
| validate-web-flow.prompt.md | Canonical prompt: Validate a web journey with Playwright in Python or TypeScript, with accessible locators, web-first assertions, isolated authentication and replayable evidence | .apm/prompts/validate-web-flow.prompt.md |
| python.md | Canonical skill | .apm/skills/agent-evaluation/references/python.md |
| typescript.md | Canonical skill | .apm/skills/agent-evaluation/references/typescript.md |
| SKILL.md | Canonical skill: Evaluate the outcomes and tool-use process of agentic systems written in Python or TypeScript, with scenario datasets, deterministic checks, rubrics, model judges and human review. Use when agent behavior, a release gate, a prompt, tool or model change, or reliability and safety evaluation is requested. | .apm/skills/agent-evaluation/SKILL.md |
| SKILL.md | Canonical skill: Design useful, privacy-aware observability for TypeScript services, tool calls, agent runs, workflows, and operational decisions. | .apm/skills/agent-observability-and-telemetry/SKILL.md |
| SKILL.md | Canonical skill: Engineer reliable agent state, memory, context selection, compaction, retrieval grounding, provenance, and handoff behavior. | .apm/skills/agent-state-and-context-engineering/SKILL.md |
| SKILL.md | Canonical skill: Bound and measure model, tool, workflow, and cloud consumption in agentic TypeScript applications. | .apm/skills/agentic-cost-and-budget-controls/SKILL.md |
| python.md | Canonical skill | .apm/skills/agentic-workflow-design/references/python.md |
| typescript.md | Canonical skill | .apm/skills/agentic-workflow-design/references/typescript.md |
| SKILL.md | Canonical skill: Design bounded, auditable agent applications and multi-step tool workflows in Python or TypeScript: state, tools, memory, budgets, cancellation and optional specialist handoffs, using autonomy only where it adds value. Use when an agent application or tool-calling workflow needs design or change in either language. | .apm/skills/agentic-workflow-design/SKILL.md |
| SKILL.md | Canonical skill: Design or review versionable TypeScript APIs and integrations with validated contracts, safe retries, idempotency, and observable failure handling. | .apm/skills/api-contract-and-integration-engineering/SKILL.md |
| SKILL.md | Canonical skill: Integrate TypeScript systems with Azure, AWS, and Google Cloud using explicit identity, configuration, resilience, and provider-neutral operational boundaries. | .apm/skills/cloud-integration-and-identity/SKILL.md |
| SKILL.md | Canonical skill: Manage TypeScript and JavaScript dependencies for compatibility, provenance, reproducible builds, vulnerability response, and minimal supply-chain risk. | .apm/skills/dependency-supply-chain-and-reproducibility/SKILL.md |
| adr-template.md | Canonical skill | .apm/skills/enterprise-architecture-and-adr/adr-template.md |
| SKILL.md | Canonical skill: Make consequential TypeScript system decisions explicit through boundaries, trade-offs, ADRs, migration plans, and operational ownership. | .apm/skills/enterprise-architecture-and-adr/SKILL.md |
| SKILL.md | Canonical skill: Design and implement maintainable React and modern web changes with accessible behavior, state clarity, performance awareness, and browser evidence. | .apm/skills/frontend-react-engineering/SKILL.md |
| SKILL.md | Canonical skill: Engineer Node.js services and JavaScript modules with correct ESM/CommonJS behavior, lifecycle management, resource cleanup, and operational readiness. | .apm/skills/javascript-node-runtime-engineering/SKILL.md |
| SKILL.md | Canonical skill: Build a proportionate layered test strategy for TypeScript systems, public contracts, integrations, browser journeys, and regression coverage. | .apm/skills/layered-testing-and-test-engineering/SKILL.md |
| SKILL.md | Canonical skill: Build or review TypeScript MCP servers and clients with precise schemas, safe transports, authorization, bounded results, and approval-aware actions. | .apm/skills/mcp-typescript-engineering/SKILL.md |
| SKILL.md | Canonical skill: Improve TypeScript system performance and production operability using measured bottlenecks, resilience controls, and recovery evidence. | .apm/skills/performance-reliability-and-operability/SKILL.md |
| python.md | Canonical skill | .apm/skills/playwright-validation/references/python.md |
| typescript.md | Canonical skill | .apm/skills/playwright-validation/references/typescript.md |
| SKILL.md | Canonical skill: Validate web journeys with Playwright in Python or TypeScript, using accessible locators, web-first assertions, isolated authentication and diagnostic traces, and prove observable user outcomes. Use when a web flow, accessibility behavior, browser regression or UI-to-backend integration needs verification. | .apm/skills/playwright-validation/SKILL.md |
| SKILL.md | Canonical skill: Review implementation diffs and pull requests for correctness, maintainability, security, tests, operations, and delivery readiness without silently merging or publishing. | .apm/skills/pull-request-review-and-delivery/SKILL.md |
| adr-template.md | Canonical skill | .apm/skills/requirements-and-change-planning/adr-template.md |
| handoff-template.md | Canonical skill | .apm/skills/requirements-and-change-planning/handoff-template.md |
| SKILL.md | Canonical skill: Turn ambiguous enterprise engineering requests into explicit scope, acceptance criteria, options, risks, dependencies, and reviewable implementation plans. | .apm/skills/requirements-and-change-planning/SKILL.md |
| python.md | Canonical skill | .apm/skills/secure-agent-engineering/references/python.md |
| typescript.md | Canonical skill | .apm/skills/secure-agent-engineering/references/typescript.md |
| SKILL.md | Canonical skill: Assess and harden agentic applications written in Python or TypeScript: prompt injection, tool misuse, memory poisoning, tenant isolation, unsafe code execution, supply chain, privacy and responsible AI, plus each language's own dangerous APIs. Use when agent, retrieval, browser, model output, MCP, dependency or durable-memory boundaries are in scope. | .apm/skills/secure-agent-engineering/SKILL.md |
| SKILL.md | Canonical skill: Route substantial enterprise TypeScript and JavaScript work through repository discovery, scoped planning, implementation, validation, and evidence-based completion. | .apm/skills/typescript-distinguished-engineer-orchestration/SKILL.md |
| SKILL.md | Canonical skill: Design, implement, or review maintainable strict TypeScript with explicit contracts, safe narrowing, runtime validation, and reliable asynchronous behavior. | .apm/skills/typescript-strict-engineering/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| AGENT_HANDOFF_CONTRACT.md | Pack contract or inventory | docs/AGENT_HANDOFF_CONTRACT.md |
| APPROVAL_MATRIX.md | Pack contract or inventory | docs/APPROVAL_MATRIX.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| END_TO_END_WORKFLOW.md | Pack contract or inventory | docs/END_TO_END_WORKFLOW.md |
| GOVERNANCE.md | Pack contract or inventory | docs/GOVERNANCE.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| TOOL_PERMISSION_MATRIX.md | Pack contract or inventory | docs/TOOL_PERMISSION_MATRIX.md |
| build-mcp-server.md | Worked example | examples/build-mcp-server.md |
| design-and-evaluate-agentic-system.md | Worked example | examples/design-and-evaluate-agentic-system.md |
| design-and-implement-feature.md | Worked example | examples/design-and-implement-feature.md |
| diagnose-failure.md | Worked example | examples/diagnose-failure.md |
| release-readiness.md | Worked example | examples/release-readiness.md |
| review-pull-request.md | Worked example | examples/review-pull-request.md |
| validate-web-flow.md | Worked example | examples/validate-web-flow.md |
| post-engineering-review.ps1 | Hook helper script | hooks/post-engineering-review.ps1 |
| post-engineering-review.sh | Hook helper script | hooks/post-engineering-review.sh |
| pre-engineering-review.ps1 | Hook helper script | hooks/pre-engineering-review.ps1 |
| pre-engineering-review.sh | Hook helper script | hooks/pre-engineering-review.sh |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| adr-template.md | Reusable template | templates/adr-template.md |
| agentic-workflow-spec.md | Reusable template | templates/agentic-workflow-spec.md |
| completion-report-template.md | Reusable template | templates/completion-report-template.md |
| evaluation-scenario.yml | Reusable template | templates/evaluation-scenario.yml |
| handoff-template.md | Reusable template | templates/handoff-template.md |
| pr-review-template.md | Reusable template | templates/pr-review-template.md |
| tool-contract.md | Reusable template | templates/tool-contract.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| command_guard.py | Pack-specific helper code | tooling/command_guard.py |
| repository_inventory.py | Pack-specific helper code | tooling/repository_inventory.py |
| validate_engineering_report.py | Pack-specific helper code | tooling/validate_engineering_report.py |
| validate_evaluation_scenario.py | Pack-specific helper code | tooling/validate_evaluation_scenario.py |
| README.md | Pack file | tools/README.md |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-typescript-distinguished-engineer.zip: 50 files generated by `apm install --target copilot`
- claude-typescript-distinguished-engineer.zip: 50 files generated by `apm install --target claude`
- codex-typescript-distinguished-engineer.zip: 35 files generated by `apm install --target codex`
- kiro-typescript-distinguished-engineer.zip: 41 files generated by `apm install --target kiro`
- gemini-typescript-distinguished-engineer.zip: 40 files generated by `apm install --target gemini`
- agent-skills-typescript-distinguished-engineer.zip: 31 files generated by `apm install --target agent-skills`
- typescript-distinguished-engineer-canonical.zip, typescript-distinguished-engineer-prompt.zip, typescript-distinguished-engineer-validation.zip, typescript-distinguished-engineer-skills.zip, typescript-distinguished-engineer-full-pack.zip, SHA256SUMS.txt
