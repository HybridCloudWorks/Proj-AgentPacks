# Source Traceability

## User-provided source material

| Source | Use | Treatment |
|---|---|---|
| `python-engineer.md` attachment | Consolidation, tool ownership, maturity and reproducibility ideas | Reference data only; Python-specific commands and assumptions were not copied into this TypeScript pack. |
| User's detailed TypeScript/JavaScript agent specification | Governing requirements, identity, loop, expertise, approvals, structure, and completion contract | Authoritative for this pack. |

## Official documentation consulted

| Topic | Source | Pack decision |
|---|---|---|
| TypeScript strictness | https://www.typescriptlang.org/tsconfig/strict | Use strictness as a repository-aware default and avoid claiming a config change is safe without inspection. |
| TypeScript implicit any | https://www.typescriptlang.org/tsconfig/noImplicitAny.html | Treat implicit any as a boundary/type design issue, not merely a lint warning. |
| Node packages and modules | https://nodejs.org/api/packages.html | Inspect `type`, exports, imports, engines, and package boundaries. |
| Node TypeScript support | https://nodejs.org/api/typescript.html | Verify runtime and type-stripping constraints instead of assuming a loader or build step. |
| Playwright best practices | https://playwright.dev/docs/best-practices | Prefer user-facing behavior and accessible locators. |
| Playwright locators | https://playwright.dev/docs/locators | Use role, label, text, and stable test IDs before brittle selectors. |
| Playwright tracing | https://playwright.dev/docs/api/class-tracing | Preserve traces as failure diagnostics when configured. |
| MCP tools | https://modelcontextprotocol.io/specification/2025-06-18/server/tools | Use input/output schemas, bounded results, and explicit tool annotations/side-effect review. |
| MCP TypeScript SDK | https://github.com/modelcontextprotocol/typescript-sdk | Follow the repository's SDK generation; review current v1/v2 status before choosing imports. |
| MCP TypeScript server guide | https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/server.md | Separate tools/resources/prompts and select stdio versus Streamable HTTP deliberately. |
| OpenTelemetry JavaScript | https://opentelemetry.io/docs/languages/js/ | Prefer compatible traces, metrics, logs, propagation, and privacy controls. |
| GitHub custom agents | https://docs.github.com/en/copilot/reference/custom-agents-configuration | Generate `.github/agents` files with frontmatter. |
| Claude Code subagents | https://code.claude.com/docs/en/sub-agents | Generate `.claude/agents` files and preserve narrow agent scope. |
| OpenAI Codex Skills | https://developers.openai.com/codex/skills/ | Generate discoverable `.agents/skills` and Codex agent TOML. |
| Gemini CLI Agent Skills | https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md | Generate discoverable `.agents/skills` and `.gemini/agents`. |

URLs are maintained references, not copied documentation. Recheck version-sensitive behavior before using this pack for implementation.
