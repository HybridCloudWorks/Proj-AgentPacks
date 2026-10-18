---
name: codex-agentic-workflow-dispatch
description: Plan and execute OpenAI Codex multi-agent workflows when a request needs one or more custom agents, explicit handoffs, dependency ordering, bounded concurrency, or verifiable completion.
---

Use this Skill whenever the work spans specialist roles or the user asks for delegation, orchestration, parallel review, handoff, or an all-agent workflow.

## Dispatch contract

1. Read repository instructions and identify the requested outcome, authorization boundary, and acceptance criteria.
2. Run `python tooling/workflow.py discover` when capability availability is unknown. Treat discovery output as evidence, not authorization.
3. Select `one`, `selected`, or `all` from `agent-registry.yml`. Mark each node required or optional for this workflow.
4. Run `python tooling/workflow.py init` before asking Codex to spawn a subagent. The workflow directory is the source of truth for status.
5. Build a dependency-aware plan. Parallelize only independent nodes and respect Codex's `agents.max_concurrent_threads_per_session` setting.
6. Ask Codex to spawn each required node using the exact registered custom agent `name`. Give it the task, relevant files, acceptance criteria, authorization limits, and required handoff path.
7. Require the subagent to write a handoff conforming to `references/handoff-contract.md`. A natural-language summary alone is not a completed handoff.
8. Run `python tooling/workflow.py validate --workflow <workflow-id>` before synthesis. Do not claim success while required nodes are missing, blocked, or unverified.
9. Synthesize only from recorded handoffs and artifacts. Preserve disagreements and uncertainty.

## Selection rules

- `one`: select the smallest capable registered agent.
- `selected`: use the explicitly named agents; missing optional names are skipped, missing required names block.
- `all`: select every registry entry whose `enabled_by_default` is true. Installed entries are required; unavailable entries are skipped as optional unless `--require-all` is explicit.
- A domain agent may be invoked once per workflow unless the workflow explicitly creates a retry node.
- Do not invoke the parent orchestrator as its own specialist node.

## Safety

Planning, discovery, inspection, and local validation are the default. Ask before external publication, PR creation, deployment, cloud mutation, state mutation, deletion, permission changes, secrets, or production work. Never use `--yolo` or a bypass flag as an orchestration shortcut.

Read [references/handoff-contract.md](references/handoff-contract.md) for the required handoff shape and [references/dispatch-examples.md](references/dispatch-examples.md) for one, selected, and all-agent examples.
