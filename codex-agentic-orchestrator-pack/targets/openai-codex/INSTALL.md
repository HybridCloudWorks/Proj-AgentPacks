# Codex installation

Copy this target into the repository root. Merge `.codex/hooks.json` into the existing project hook configuration and merge `.codex/config.agentic-orchestrator.toml` into `.codex/config.toml`; do not overwrite existing files. Review and trust the project hooks with `/hooks` before enabling them.

Use the `codex-agentic-orchestrator` custom agent from Codex app, CLI, or IDE. Domain agents remain separate: install any combination of the user's domain packs under `.codex/agents` and `.agents/skills`.

The orchestrator records local state under `.agentic/`. It performs no network calls by itself. Review sandbox and approval behavior before allowing delegated subagents to edit files or use external tools.

If the repository already has `AGENTS.md`, merge the supplied `AGENTS.agentic-orchestrator.md` guidance into the relevant section instead of replacing the file.
