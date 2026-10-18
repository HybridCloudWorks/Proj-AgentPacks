---
description: "Report observed agent, skill and tool activity for a session or run without estimating what the source does not expose"
agent: hypervelocity-engineer
---

# Report agent usage

## Inputs

- The source: a session transcript, hook output, run log or tool output.
- Time window and session or run identifier.
- Whether the optional usage hook is installed and enabled in this repository.

## Workflow

1. Apply `agent-usage-reporting`: count only what the selected source shows, state the counting rules, and separate exact counts from estimates.
2. If the optional Claude Stop hook is not installed or not enabled, report from the selected source directly and say so. Do not install or enable the hook without the repository's permission.
3. Read the source without modifying it. Leave out prompt text, tool arguments the report does not need, secrets and other transcript content.

## Expected output

A report naming source, window, identifiers and counting rules; a count table by agent, skill and tool; metrics the source does not expose; and a note that the counts are telemetry, not proof of correctness. Follow the `hypervelocity-engineer-contract` instruction for the completion report.
