# Python engineering hooks

| Hook | Purpose/activation | Input/dependencies | Behavior/output | Failure/guardrail |
|---|---|---|---|---|
| sessionStart / preflight | Discover Python metadata when a session starts | Host JSON cwd; Python 3.11+; optional pyproject.toml | Parse metadata without imports or code execution; return bounded additionalContext | Invalid/unreadable metadata produces a safe diagnostic, no content/secret dump |
| agentStop / completion | Check requested completion evidence when primary stops | Host JSON and optional .github/python-engineering/completion.json; tooling/completion_contract.py | Validate criterion/check status and session binding; complete claims must have evidence | One corrective block if invalid, then allow incomplete termination when stop_hook_active is true; no self-approval or infinite loop |
| post-python-engineering wrappers | Manual completion contract check | Exact report path and Python 3.11+ | Exit 0 valid / 1 invalid; print sanitized error names | No arbitrary repository commands |

Copilot uses version-1 hooks/python-engineering.json rendered under .github/hooks with scripts. Commands use cwd '.' and explicit script paths; the host payload cwd is validated. The report is optional when no completion file is requested; the hook does not demand a fixture for every conversational reply. If present it must carry the current session_id, preventing reuse of a stale report.

Other targets ship these helpers and this README under shared/hooks plus shared/tooling; run manually with the commands in INSTALL.md. No Claude/Codex/Gemini native hook behavior is claimed. Shell wrappers invoke fixed pack code with bounded host timeouts; they do not grant permissions or run a chosen test suite.

Completion JSON is a local evidence index, not trusted proof. Review command outputs and host approvals independently. Do not record raw prompts, arguments, source, secrets or customer data.
