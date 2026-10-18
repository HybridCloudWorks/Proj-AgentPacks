# Python engineering hooks

| Hook | Purpose/activation | Input/dependencies | Behavior/output | Failure/guardrail |
|---|---|---|---|---|
| sessionStart / preflight | Discover Python metadata when a session starts | Host JSON cwd; Python 3.11+; optional pyproject.toml | Parse metadata without imports or code execution; return bounded additionalContext | Invalid/unreadable metadata produces a safe diagnostic, no content/secret dump |
| agentStop / completion | Check requested completion evidence when primary stops | Host JSON and optional .github/python-engineering/completion.json; tooling/completion_contract.py | Validate criterion/check status and session binding; complete claims must have evidence | One corrective block if invalid, then allow incomplete termination when stop_hook_active is true; no self-approval or infinite loop |
| post-python-engineering wrappers | Manual completion contract check | Exact report path and Python 3.11+ | Exit 0 valid / 1 invalid; print sanitized error names | No arbitrary repository commands |

Hook definitions are not installed natively by this pack. APM copies hook commands verbatim and does not deploy the scripts they call, so a repository-relative command such as `.github/hooks/scripts/hook_runner.py` would break in every target. The Copilot-format definition is kept as a reviewed sample in `samples/`; wire it up yourself, or let the Code Workflow installer register hooks that point at its own pack home.

The helper scripts in this folder call fixed pack code in `tooling/` with bounded timeouts. They do not grant permissions or run a chosen test suite. The completion report is optional when no completion file is requested; if present it must carry the current session_id, preventing reuse of a stale report.

Completion JSON is a local evidence index, not trusted proof. Review command outputs and host approvals independently. Do not record raw prompts, arguments, source, secrets or customer data.
