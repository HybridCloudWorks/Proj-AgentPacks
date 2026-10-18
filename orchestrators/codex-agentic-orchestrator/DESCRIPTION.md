# Codex Agentic Orchestrator

OpenAI Codex-native orchestration for multi-agent engineering workflows. The pack discovers Codex custom agents, selects required and optional capabilities from a registry, creates durable workflow state, asks Codex to delegate through its native subagent mechanism, validates structured handoffs, and reports completed, skipped, failed, or blocked work without silently falling back to parent-only execution.

This is a workflow controller, not a replacement for domain agents. Install it alongside any combination of the domain Agent/Skill packs. A missing optional agent is recorded as skipped; a missing required agent blocks completion with an actionable reason.
