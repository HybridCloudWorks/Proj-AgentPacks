---
name: agent-usage-reporting
description: Measure observed agent, skill, and tool activity with an optional non-blocking report hook when a repository needs lightweight usage visibility.
---

# Agent Usage Reporting

Use this skill when the user asks for agent usage, skill usage, tool-call counts, adoption reporting, or a lightweight activity summary.

## Contract

- Report only activity that is actually observable in the selected transcript, hook event, run log, or tool output.
- State the time window, session or run identifier, source file, and counting rules.
- Separate exact counts from estimates; do not invent token, cost, latency, or quality measurements.
- Never include prompt text, tool arguments, secrets, credentials, or transcript content that is not required by the report.
- Treat the report as operational telemetry, not proof that the agent was correct or that a workflow completed successfully.

## Optional Claude Stop hook

The pack includes `.apm/hooks/agent-report.ps1` for Claude Code installations that support a Stop hook. It is deliberately opt-in and must remain non-blocking:

1. Copy it to `.claude/hooks/agent-report.ps1` in the target repository.
2. Enable it only through the repository's approved Claude hook configuration.
3. Set `AGENT_REPORT_ENABLED=1` only after confirming the repository permits local activity reporting.
4. The hook reads the supplied transcript JSONL, counts observed `Agent`, `Skill`, and tool-use blocks, and emits a short `systemMessage`.
5. Failures, unreadable transcripts, malformed lines, and unsupported hook payloads must exit successfully so a report cannot block the agent.

The hook stores only a per-session byte offset and current counts in `.claude/agent-report.json`. It does not claim universal vendor support and does not calculate usage that the input does not expose.

## Validation

- Verify the hook is disabled by default in a new installation.
- Test empty, missing, truncated, and valid transcript inputs.
- Confirm repeated Stop events do not double-count earlier transcript bytes.
- Confirm secrets and transcript content are absent from emitted messages.
- Label results as observed, inferred, unavailable, or requiring vendor telemetry.
