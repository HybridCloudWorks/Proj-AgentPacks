# Prompt inventory

The pack ships nine prompts in `.apm/prompts/`. Each one starts a workflow for the primary agent, `typescript-distinguished-engineer`. All of them rely on the always-on `typescript-distinguished-engineer-contract` instruction for approvals, handoffs and the completion report.

The prompt files themselves do not name skills. The skills column below lists the skills each workflow applies, derived from the prompt text and the skill descriptions.

| Prompt | Skills the workflow applies | Expected output | Worked example |
|---|---|---|---|
| design-change.prompt.md | requirements-and-change-planning, enterprise-architecture-and-adr, typescript-distinguished-engineer-orchestration | Verified facts and assumptions, acceptance criteria, options compared with a recommendation, implementation slices, tests, telemetry, rollback, approval and ADR needs | examples/design-and-implement-feature.md |
| implement-feature.prompt.md | typescript-strict-engineering, javascript-node-runtime-engineering, api-contract-and-integration-engineering, frontend-react-engineering, layered-testing-and-test-engineering | A scoped diff with tests, the checks run and their results, criteria marked verified or unverified, a completion report | examples/design-and-implement-feature.md |
| review-pull-request.prompt.md | pull-request-review-and-delivery, secure-agent-engineering, dependency-supply-chain-and-reproducibility, frontend-react-engineering | Prioritized findings located by file and line, with impact, remediation and confidence; checks run and skipped; a review verdict | examples/review-pull-request.md |
| build-mcp-server.prompt.md | mcp-typescript-engineering, secure-agent-engineering, agentic-cost-and-budget-controls, typescript-strict-engineering | Capability classification, tool contracts, approval design, implementation, protocol and negative tests, rollback | examples/build-mcp-server.md |
| design-agentic-system.prompt.md | agentic-workflow-design, agent-state-and-context-engineering, agentic-cost-and-budget-controls, agent-observability-and-telemetry, enterprise-architecture-and-adr | A workflow specification, an ADR, budgets and termination rules, and the evidence that can prove completion | examples/design-and-evaluate-agentic-system.md |
| evaluate-agent.prompt.md | agent-evaluation, secure-agent-engineering | A versioned scenario set; a rubric with deterministic and model-judged criteria labelled separately; results, cost and latency, limitations | examples/design-and-evaluate-agentic-system.md |
| validate-web-flow.prompt.md | playwright-validation, frontend-react-engineering, layered-testing-and-test-engineering | Journey assertions and results per browser project, failure diagnostics, accessibility and data-exposure checks | examples/validate-web-flow.md |
| diagnose-failure.prompt.md | javascript-node-runtime-engineering, performance-reliability-and-operability, agent-observability-and-telemetry, layered-testing-and-test-engineering | The recorded evidence, hypotheses tested one at a time, a fix with a regression test, and any cause not yet confirmed | examples/diagnose-failure.md |
| release-readiness.prompt.md | pull-request-review-and-delivery, dependency-supply-chain-and-reproducibility, cloud-integration-and-identity, performance-reliability-and-operability | Evidence tied to the release commit, missing evidence and residual risk, a review verdict; nothing published or deployed | examples/release-readiness.md |

In the examples, specialists join only where independent work adds value:

- `typescript-security-reviewer`: feature, pull request review, MCP server, release readiness.
- `typescript-test-engineer`: feature, web flow.
- `agent-evaluation-engineer`: agentic system evaluation.

## Installation

APM deploys prompts as GitHub Copilot prompt files and as Claude Code commands. Claude drops prompt frontmatter keys it does not support, such as `agent`. At user scope (`apm install -g`), Claude Code and Copilot receive the prompts; Codex receives none.

The verified vendor notes do not record how Gemini CLI or Kiro receive prompts, so this inventory makes no claim for them.
