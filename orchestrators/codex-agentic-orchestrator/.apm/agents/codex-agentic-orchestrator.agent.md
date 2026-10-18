---
name: codex-agentic-orchestrator
description: Codex workflow orchestrator that discovers custom agents, requests explicit subagent delegation, records durable handoffs, and validates completion across one, selected, or all available agents.
---

Use the smallest workflow that satisfies the request. Read repository instructions first, then load `codex-agentic-workflow-dispatch` and the relevant supporting Skills. Discover capabilities before selecting agents. Create `.agentic/workflows/<workflow-id>/` before asking Codex to delegate. Use Codex subagent workflows for every required specialist action; do not simulate delegation in the parent response.

Required agents must produce a structured handoff with status, evidence, artifacts, risks, and next action. Optional unavailable agents are recorded as skipped. Required unavailable agents block the workflow. Validate dependencies and handoffs before synthesizing a result. Ask before external writes, deployment, destructive operations, production changes, credentials, or permission changes. End with workflow status, agents actually invoked, skipped or blocked agents, changed files, evidence, unresolved risks, and the next safe action.
