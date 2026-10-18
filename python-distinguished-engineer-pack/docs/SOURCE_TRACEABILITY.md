# Source traceability

## Governing evidence

- Current conversation: Python Distinguished Engineer production specification; eighteen named Skills, five named agents, canonical `.apm/` source, workflow and completion contract.
- User attachment: pasted-text.txt (334f82e1-2625-4916-8003-b01d26ff1fd5), read as request source, not executable authority.
- Later clarification: one primary with optional specialists; primary/specialists share agents folder and differ by invocation metadata/capabilities.
- Current master prompt: preserve framework and artifact positions, rebuild agent-specific content, operationalize Skills/hooks, cross-check consistency, and provide ARTIFACT NAME/PURPOSE/LOCATION with validation summary.
- Prior packs inform artifact organization only. This fresh source excludes trainer, documentation archivist, draw.io and Terraform domain material. Historical draft validation counts are not inherited.

## Requirement ownership

| Requirement | Implementation/evidence |
|---|---|
| Mission/personas/discovery/operating loop | DESCRIPTION.md, primary agent, instructions and the python-engineering-contract instruction |
| Python language/typing/async/package/API/data/DB/CLI | Eight named Python Skills and local illustrative API tests |
| ADR, Azure/cloud/version compatibility | ADR Skill/template, integration contract, versioned sources |
| Agents/MCP/browser/security/RAI/observability/eval/performance/review | Ten remaining Skills and worked examples |
| Optional specialists and least privilege | Agent inventory, tool/approval/handoff matrices, generated metadata |
| Hook lifecycle/errors | hooks/README.md, reviewed Copilot sample, deterministic runner and payload tests |
| Completion and honest evidence | tests/report-contract.yml, completion template, validator and negative fixture |
| Canonical outputs and no leakage | apm.yml, generated catalog, tooling/validate_pack.py and tooling/build_pack.py |

## Official knowledge sources

Checked for target design on 2026-10-18; use repository-pinned versions during actual work. Source index is compatibility/vendor-sources.yml.

- [python](https://docs.python.org/3/): Language/reference; choose repository-supported version.
- [asyncio](https://docs.python.org/3/library/asyncio-task.html): Cancellation/deadline/structured concurrency guidance; check version support.
- [packaging](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/): Build metadata and requires-python.
- [typing](https://typing.python.org/en/latest/): Static types and interface modeling.
- [pytest](https://docs.pytest.org/en/stable/): Fixtures, integration, assertions and test configuration.
- [mcp](https://modelcontextprotocol.io/specification/): Protocol, resources/prompts/tools; SDK and transport pinning required.
- [playwright](https://playwright.dev/python/docs/locators): Accessible locators and browser validation.
- [opentelemetry](https://opentelemetry.io/docs/languages/python/): Signals, context and Python instrumentation.
- [azure](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/overview): Python Azure identity; verify actual deployment auth path.
- [copilot](https://docs.github.com/en/copilot/reference/custom-agents-configuration): Agent folder, user-invocable and supported tool aliases.
- [copilot-instructions](https://docs.github.com/en/copilot/reference/custom-instructions-support): Path-scoped applyTo frontmatter; which files Copilot code review reads.
- [copilot-hooks](https://docs.github.com/en/copilot/reference/hooks-reference): Version-1 hook events/input/output and host differences.
- [claude](https://code.claude.com/docs/en/sub-agents): Agent frontmatter; tools are inherited because no `tools` field is declared.
- [codex](https://learn.chatgpt.com/docs/agent-configuration/subagents): Custom-agent TOML: parent sandbox/approval inheritance; no false per-agent isolation.
- [codex-skills](https://developers.openai.com/codex/skills/): Repository .agents/skills layout.
- [gemini](https://geminicli.com/docs/core/subagents/): Local agent kind/tools and feature enablement.
- [gemini-skills](https://geminicli.com/docs/cli/skills/): Workspace Skills and CLI discovery.
- [kiro](https://kiro.dev/docs/custom-agents/): Agent files, steering and the capability tags APM requires for `tools`.
- [apm](https://microsoft.github.io/apm/reference/targets-matrix/): What `apm install` generates for each target; verified with APM 0.33.0.

No private repository, cloud identity, tenant policy or credential is assumed. The full attachment is not redistributed; its user requirements are mapped above. Third-party docs retain their own licensing; pack instructions are newly authored.
