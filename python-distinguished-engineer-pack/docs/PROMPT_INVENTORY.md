# Prompt inventory

| Prompt | Expected output |
|---|---|
| investigate-repository.prompt.md | Facts with paths, version/toolchain conflicts, interface map, unknowns and proposed validation commands. |
| design-change.prompt.md | Design/ADR, interface/data impact, risk/approval classification, implementation/test plan and rollout/recovery. |
| implement-feature.prompt.md | Scoped diff, criterion status, commands/results, compatibility/dependency/migration/operations impact and completion report. |
| review-pull-request.prompt.md | Prioritized located findings with evidence/impact/remediation/blocking status; checks actually run and review limits. |
| build-python-api.prompt.md | Versioned contract, runtime validation, typed implementation, auth/error/idempotency tests, telemetry and rollback. |
| build-mcp-server.prompt.md | Tool schema/effects/authz/approval contract, implementation, protocol/negative tests, redaction, eval and rollback. |
| debug-python-issue.prompt.md | Evidence and root cause, minimal proposed fix or requested patch, regression checks, limits and recovery. |
| modernize-python-code.prompt.md | Incremental compatible plan/patch, version and dependency migration impact, tests and reversal strategy. |
| validate-web-flow.prompt.md | Actual user-flow assertions, visible error/keyboard behavior, sanitized evidence, persistence checks and cleanup/limits. |
| evaluate-agent.prompt.md | Versioned dataset, deterministic/model/human scoring, failures, budget evidence, draft thresholds and release recommendation. |

APM installs these as Copilot prompt files, Claude commands (the `agent` key is dropped) and Gemini commands. Codex and Kiro receive no prompts; their users invoke the primary agent directly.
