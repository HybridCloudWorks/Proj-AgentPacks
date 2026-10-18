---
name: codex-subagent-delegation-and-concurrency
description: Delegate work to Codex custom agents with explicit prompts, scoped context, dependency handoffs, bounded concurrency, and permission-aware execution.
---

Use this Skill when the orchestrator is ready to dispatch a registered Codex custom agent.

Ask Codex to use the native subagent workflow and exact custom agent `name` from the registry. The delegation prompt must include workflow ID, agent ID, objective, acceptance criteria, files in scope, dependencies, required output path, authorization boundary, prohibited actions, and the instruction to write the structured handoff before responding.

The parent remains responsible for routing and final synthesis. Prefer parallel subagents for independent read-heavy tasks. Be careful with parallel write-heavy work because Codex documents possible edit conflicts. Respect `agents.max_concurrent_threads_per_session`; never assume unlimited agents.

Custom agents inherit parent permission choices unless explicitly configured otherwise. Do not use `--yolo`, bypass flags, or elevated approvals merely to make delegation appear successful.
