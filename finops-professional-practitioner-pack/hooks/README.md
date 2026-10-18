# FinOps hooks and helpers

Nothing in this folder is installed as a native hook. APM copies hook commands verbatim and does not deploy the scripts they call, so any command path would break after install. The scripts here are portable helpers you run by hand; the JSON in `samples/` is a reviewed GitHub Copilot hook definition you can wire up yourself, or let the Code Workflow installer register against its own pack home.

| Helper | Purpose and activation | Inputs and dependencies | Behaviour and output | Failure handling and guardrails |
|---|---|---|---|---|
| sessionStart (`tooling/hook_runner.py sessionStart`, sample) | Tell the agent which billing exports a workspace holds when a session starts | Host JSON on stdin with `cwd` and `sessionId` or `session_id`; Python 3.11 or later | Walks at most four folder levels, reads the first line of at most 25 CSV files, classifies each as FOCUS, AWS CUR, Azure cost details or Google Cloud billing export, counts Parquet files, returns bounded `additionalContext` | Never reads data rows; reports only known column names; file names with spaces or unusual characters become `<unlisted name>`; invalid input returns a fixed error without echoing it |
| agentStop (`tooling/hook_runner.py agentStop`, sample) | Check an optional completion report when the primary agent stops | Host JSON; optional `.finops/completion.json` in the workspace; `tooling/completion_contract.py` | Validates statuses, criteria, checks, cost basis, recommendation ranges and the session binding | Blocks once with the contract errors, then allows the stop when `stop_hook_active` is set, so it cannot loop; a missing report never blocks |
| `pre-finops-session.sh` and `.ps1` | Manual dataset preflight for a folder | Folder path (default current folder) | Prints the preflight JSON | Read-only; same bounds as sessionStart |
| `post-finops-completion.sh` and `.ps1` | Manual completion-report check | Path to a completion JSON file | Prints `valid` and the error names; exit 0 valid, 1 invalid | Read-only; never runs commands named in the report |

The helpers call fixed pack code in `tooling/` with short timeouts. They grant no permissions, run no queries and contact nothing. The completion report is a local evidence index, not proof: the hook checks its shape and session binding, not whether the figures are true. Do not record raw billing rows, negotiated rates or personal data in it.

Hooks for Claude Code, Codex, Kiro and Gemini CLI are not provided as samples because their payload and output formats differ and were not exercised for this pack. The runner accepts both `sessionId` and `session_id`, and both `stop_hook_active` and `stopHookActive`, so an installer can adapt it.
