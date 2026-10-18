# Source Traceability

| Source | Treatment |
|---|---|
| User's cross-client orchestration requirements | Converted into a Codex-specific adapter with an explicit registry, durable state, native subagent request, and structured handoff contract. |
| Existing domain Agent packs in the workspace | Represented as registry entries by Codex TOML agent name; domain content is not copied or duplicated. |
| Official OpenAI/Codex documentation | Used for `.codex/agents`, `.agents/skills`, subagent workflows, hooks, trust review, and concurrency boundaries. |
| Runtime and client availability | Intentionally not asserted by static files; validated only by a live Codex installation and authenticated smoke test. |
