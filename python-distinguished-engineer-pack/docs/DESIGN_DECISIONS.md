# Design decisions

## Original decisions (version 2.0.0)

1. Recreate Python Distinguished Engineer from its user specification and later primary/specialist clarification. The existing trainer pack is an independent artifact; none of its curriculum or persona content is imported.
2. Keep the established canonical .apm source, uppercase DESCRIPTION/VALIDATION_REPORT, authoring prompt, compatibility/docs/tests/tooling/hooks, instructions/prompts/examples/templates, vendor targets and archive families. Copilot retains the exact five-agent/eighteen-Skill/five-instruction/ten-prompt/six-example map.
3. One user-facing primary owns all workflows. Specialists remain optional and in the same agents directory. Copilot uses user-invocable false for specialists and agent delegation on primary; other hosts use documented role/config capabilities without a false universal picker promise.
4. Security gets read/search only, since shell access would defeat a genuine read-only boundary. Performance gets bounded measurement without edit. Tests/eval workers have narrowly assigned edits, with host policy enforcing actual execution permissions.
5. No generic browser/test/mcp tool aliases. External tools and SDKs require independently verified identity/scope; none is preinstalled. Codex approval/sandbox inheritance is documented accurately.
6. Hooks inspect metadata and completion evidence deterministically; they do not auto-run arbitrary repository scripts or approve actions. Missing post-session evidence requests one correction then returns a bounded failure status to avoid loops.
7. Build from an explicit manifest into deterministic archives, omitting cache/legacy files. Generate an ordered full-content artifact catalog and verify archive bytes, paths, parity and embedded report freshness.
8. APM-friendly means preserved source layout and manifest; no undocumented APM schema/version compatibility claim. Live client invocation, cloud behavior and provider evaluation require separate evidence.

## 2026-10-18: restructured to agent-pack-prompt v2

- `apm.yml` limited to APM-defined fields; `targets` declared (copilot, claude, codex, kiro, gemini, agent-skills).
- Instructions and prompts moved under `.apm/` so APM generates `.github/instructions`, `.claude/rules`, `.kiro/steering`, Claude commands, Copilot prompts and Gemini commands from one source.
- Hand-built `targets/` removed; vendor packages are produced by `tooling/build_pack.py` through `apm install` into a scratch project.
- `tools` removed from agents in favour of `compatibility/tool-permissions.yml` (see TOOL_PERMISSION_MATRIX.md).
- Native hook JSON moved to `hooks/samples/`; see hooks/README.md.
- Repository-level `copilot-instructions.md` moved to `examples/repository/` as an optional extra for GitHub Copilot code review.
- Archives are build outputs under `dist/`, not committed. The artifact catalog lists files instead of embedding them.

## Shared Python and TypeScript primitives (2.2.0, 2026-10-18)

- The Python and TypeScript Distinguished Engineer packs had shipped different files under the same names: the agent-evaluation-engineer agent, the skills agent-evaluation, agentic-workflow-design, playwright-validation and secure-agent-engineering, the agentic-security instruction, and the evaluate-agent and validate-web-flow prompts. Installed together into the user profile, whichever pack went last silently replaced the other's. In the instruction's case that also dropped the security rules for one language, because each version matched only its own file types.
- Each of these is now one shared copy, byte-identical in both packs and kept in sync from the repository's canonical copy; CI fails if a copy drifts.
- Unlike cloud providers, the two languages differ in concepts: runtime typing (neither enforces types at runtime, for different reasons), concurrency and cancellation (asyncio tasks against one always-running event loop with abort signals), package installation (source builds against npm lifecycle scripts), and test tooling (pytest against Vitest, Jest and Playwright Test). Each shared skill therefore decides the language from the code under change, carries a table of where the languages differ for that work, and keeps one reference per language. It translates concepts and never carries one language's code or idioms into the other.
- Because both languages are in every copy, either pack alone can handle code in either language; the other pack's deeper language skills are simply absent.
- The shared agent states no status names, because the two contracts define different ones; it follows the contract of the pack whose primary delegated the work. Its tool intent is the narrower of the two former sets: edit, read and shell, without web.
- The shared instruction applies to `.py`, `.ts`, `.tsx`, `.mts`, `.cts`, `.js`, `.jsx`, `.mjs` and `.cjs` files plus agent Markdown and MCP JSON files. The TypeScript version had also matched every Markdown, JSON and YAML file, which was broader than its rules need.
- The shared prompts carry no `agent` key, because one prompt cannot name both primary agents; Copilot then runs them with the active agent. Language-specific prompts with the same name in both packs (build-mcp-server, design-change, implement-feature, review-pull-request) still collide and await a naming decision.
- The `dist/` archives that were still tracked in git, contrary to the decision above that archives are build outputs, were removed from version control; the build produces them.
