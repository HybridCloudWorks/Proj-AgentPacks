# Design Decisions

## Hypervelocity is an operating model

The Agent is broader than a workflow author but remains grounded in the supplied gh-aw domain. It helps choose the right automation mechanism and guardrail level; it does not become a generic software architect or deployment operator.

## Thin Agent and progressive Skills

The two supplied Agent files are duplicates. One canonical Agent owns routing and boundaries. Procedures remain in nine Skills so the runtime loads only the relevant guidance.

## Gap closures

- `workflow-lifecycle-and-release` adds compile, validate, run, lock-file, upgrade, and source/compiled parity controls.
- `agent-governance-and-guardrails` adds permission, safe-output, MCP, network, secret, and approval decision rules.
- `agent-delegation-and-composition` adds agent selection, subagent boundaries, context handoff, deterministic-tool choice, and failure containment.
- `workflow-observability-and-evaluation` adds run summaries, telemetry, cost/quality measurement, experiments, and regression evidence.
- `agent-usage-reporting` gives the supplied hook one owner and preserves its non-blocking, opt-in behavior.

## Source versus additions

Source-derived gh-aw routing, token efficiency, Copilot review handling, and the usage hook are retained. Gap closures are pack additions supported by current gh-aw guidance and clearly labeled as additions in this document.
