---
description: "Approval, handoff and completion-report rules for the codex agentic orchestrator pack. Always on; the agents, skills and prompts in this pack refer to it."
applyTo: "**"
---
# Codex agentic orchestrator contract

This instruction is installed with the pack so that every agent, skill and prompt can rely on it. It replaces references to pack documents that are not installed.

## Completion report

Required final fields: workflow_id, workflow_status, selected_agents, invoked_agents, skipped_agents, blocked_agents, handoff_validation, artifacts, checks_performed, not_verified, next_safe_action.

Never describe an unexecuted check as passed; state what was not verified.
