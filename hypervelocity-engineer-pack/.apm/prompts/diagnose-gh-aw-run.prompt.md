---
description: "Debug or audit a failed or misbehaving GitHub Agentic Workflow run from its logs, audit data and compiled workflow"
agent: hypervelocity-engineer
---

# Diagnose a GitHub Agentic Workflow run

## Inputs

- Run URL or ID, workflow name, and the commit it ran on.
- The symptom and the expected behavior.
- Whether this task may change files, and whether a confirming live run is authorized.

## Workflow

1. Apply `agentic-workflows` on its debug and audit route. Use `gh aw` commands, not the Copilot CLI and not plain `gh workflow run`.
2. Apply `workflow-observability-and-evaluation`: collect `gh aw logs` and `gh aw audit <run-id>` evidence, keep step summaries and artifacts, and label each conclusion observed, inferred, unavailable, or requiring a live check.
3. Apply `workflow-lifecycle-and-release`: compare the Markdown source with its `.lock.yml` at the run's commit and rule source and lock drift in or out.
4. When the failure is a tool denial, permission error, network block or rejected safe output, apply `agent-governance-and-guardrails` and do not broaden permissions to make the error disappear. When it is an AI-credit, budget, timeout or max-turns limit, apply `optimize-agentic-workflow`.
5. Propose the smallest fix. A diagnose-only request authorizes analysis, not edits. If edits are authorized, recompile and validate; re-run only with authorization.

## Expected output

A short timeline, the confirmed root cause separated from ruled-out and open hypotheses, an evidence table with sources, the proposed or applied fix, validation results, what stays unverified until a live run, and the completion report required by the `hypervelocity-engineer-contract` instruction.
