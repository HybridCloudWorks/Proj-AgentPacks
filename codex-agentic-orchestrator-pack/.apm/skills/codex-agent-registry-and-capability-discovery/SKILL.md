---
name: codex-agent-registry-and-capability-discovery
description: Discover Codex custom agents and map them to capabilities, required or optional workflow nodes, and safe invocation names.
---

Use this Skill before dispatch when the user asks for any, all, available, installed, or best agent, or when the requested role is not known.

Use `python tooling/workflow.py discover --out .agentic/discovery.json`. Compare discovered `.codex/agents/*.toml` names with `agent-registry.yml`; Codex's TOML `name` field is the invocation identity, not necessarily the filename.

Classify each requested node:

- `available`: matching custom agent exists and is enabled for this project or user.
- `optional-unavailable`: not installed or disabled and the workflow permits omission.
- `required-unavailable`: not installed or disabled and the workflow requires it.
- `ambiguous`: more than one agent claims the capability; stop and select explicitly.

Do not infer that a Skill is an agent. Skills provide knowledge or workflows; only an actual Codex subagent invocation satisfies the agentic delegation requirement.
