# Skill inventory

| Skill | Activation | Workflow prompt |
|---|---|---|
| python-language-engineering | A Python implementation, defect, library interface, or version-sensitive change needs hands-on work. | implement-feature.prompt.md |
| python-static-typing | Public API typing, model boundaries, checker errors, stub quality, or modernization is in scope. | implement-feature.prompt.md |
| python-async-engineering | Async I/O, worker lifecycle, task leaks, throughput, timeouts or concurrent shared state is affected. | debug-python-issue.prompt.md |
| python-packaging | Dependencies, packaging, distribution, entry points, runtime versions or reproducibility change. | modernize-python-code.prompt.md |
| python-api-engineering | A Python endpoint, event consumer or public integration contract is created or changed. | build-python-api.prompt.md |
| python-data-engineering | Data ingestion, transformation, batch/stream processing or data-quality repair is requested. | implement-feature.prompt.md |
| python-database-engineering | Database access, query performance, consistency, cache behavior or schema migration changes. | design-change.prompt.md |
| python-cli-automation | CLI command, background automation, file processing or subprocess integration is requested. | implement-feature.prompt.md |
| architecture-decision-records | A change affects durable public contracts, runtime minimums, core tooling, shared coupling, deployment, cost or difficult-to-reverse architecture. | design-change.prompt.md |
| mcp-python-engineering | Python MCP resource, prompt, tool, transport, protocol test or supply-chain review is requested. | build-mcp-server.prompt.md |
| agentic-workflow-design | An agent application or tool-calling workflow needs design or change in either language. Shared; Python and TypeScript references. | evaluate-agent.prompt.md |
| playwright-validation | A web flow, accessibility behavior, browser regression or UI-to-backend integration needs verification. Shared; Python and TypeScript references. | validate-web-flow.prompt.md |
| secure-python-engineering | Security review or a Python change affects authentication, input/output, execution, storage or dependencies. | review-pull-request.prompt.md |
| secure-agent-engineering | Agent, retrieval, browser, model output, MCP, dependency or durable-memory boundaries are in scope. Shared; Python and TypeScript references. | evaluate-agent.prompt.md |
| agent-observability | Operational diagnostics, service telemetry, agent tracing or run-cost visibility changes. | debug-python-issue.prompt.md |
| agent-evaluation | Agent behavior, a release gate, a prompt, tool or model change, or reliability and safety evaluation is requested. Shared; Python and TypeScript references. | evaluate-agent.prompt.md |
| python-performance-analysis | A measurable performance issue or explicit performance/cost objective exists. | debug-python-issue.prompt.md |
| pull-request-review | PR, branch, staged diff or requested pre-merge review is in scope. | review-pull-request.prompt.md |

Each SKILL.md states purpose/activation, exclusions, inputs/dependencies, workflow, output/validation, failure/guardrails and workflow connection. Requirements are operational instructions rather than a promise that a model always follows them.
