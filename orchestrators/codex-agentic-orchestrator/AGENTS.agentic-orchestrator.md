# Codex orchestration merge snippet

When a request spans specialist roles, use the `codex-agentic-orchestrator` custom agent or follow its workflow: discover available `.codex/agents`, initialize durable `.agentic/workflows/<workflow-id>` state, request Codex subagent delegation for every required specialist, require structured handoffs, and validate before synthesis. Missing optional agents are recorded as skipped; missing required agents block. Never claim parent-only work as delegated work.
