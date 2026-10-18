---
name: codex-hooks-and-guardrails
description: Configure and use Codex command hooks for orchestration audit, subagent lifecycle tracking, and fail-closed workflow completion checks.
---

Use this Skill when installing, reviewing, or troubleshooting the Codex hook integration.

The target settings use synchronous command hooks for `SessionStart`, `SubagentStart`, `SubagentStop`, and `Stop`. The hook script reads Codex's JSON event from stdin, writes local audit records, and performs no network calls. `SubagentStart` is observational because Codex does not allow it to stop a subagent from starting. `SubagentStop` records the actual agent identity and final message. `Stop` returns Codex's documented continuation decision when an active workflow has `enforce_stop: true` and required handoffs are incomplete.

Codex requires review and trust for non-managed hooks. Merge the hook entries into the current `.codex/hooks.json`, preserve local policy, review them with `/hooks`, and do not use `--dangerously-bypass-hook-trust` as a normal installation step.
