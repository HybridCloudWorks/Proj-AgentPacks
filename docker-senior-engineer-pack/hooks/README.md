# Docker engineering hooks

Everything in this folder is a helper script or a reviewed sample. Nothing here is installed as a native hook.

| Hook or helper | Purpose and activation | Inputs and dependencies | Behaviour and output | Failure handling and guardrails |
|---|---|---|---|---|
| `sessionStart` (sample) / `pre-docker-engineering` (manual) | Inventory container files when a session starts, so the agent knows what exists before it plans | Host JSON with `cwd` and a session id on stdin, or `--root` for the manual helper; Python 3.11+; `tooling/hook_runner.py` and `tooling/container_lint.py` | Counts Dockerfiles, Compose, Bake and ignore files, runs the static checks, and returns only counts, rule identifiers and severities as `additionalContext`, plus a reminder to confirm the engine context | Never runs Docker, never builds, never returns file contents or secret values; skips symlinks, dependency folders and files over 1 MiB; at most 500 files; invalid input returns a fixed error object and exit 1 |
| `agentStop` (sample) / `post-docker-engineering` (manual) | Check an optional completion report when the agent stops | Host JSON with `cwd`, session id and `stop_hook_active`; optional report at `.docker-engineering/completion.json` in the repository, or `--report <path>` for the manual helper; `tooling/completion_contract.py` | Validates statuses, criteria with evidence levels, checks with exit code and environment, and the session binding; a verified-completion claim needs passing evidence | One corrective block when the report is invalid or stale, then allows the stop when `stop_hook_active` is true, so it cannot loop; no report means no opinion |
| `lint-containers` (manual) | Full static check output for a repository | `--root`; Python 3.11+ | JSON findings (rule, severity, file, line, message, fix) and a summary; exit 1 when a Blocker or High finding exists | Heuristic, line-based checks; `docker build --check`, hadolint and `docker compose config` remain the authoritative static checks |

## Why no native hooks ship

APM copies hook commands verbatim and does not deploy the scripts they call, so a command that points at a repository-relative script would break in every client. `samples/docker-engineering.copilot-hooks.sample.json` shows the Copilot hook wiring with a `<PACK_HOME>` placeholder; replace it with the installed pack path yourself, or let the Code Workflow installer register hooks that point at its own pack home. Wiring for other clients is the installer's job.

## Trust model

The agent writes the completion report about its own work, so the stop hook checks only that the report is well formed and consistent; whether the listed commands really ran, and with what result, is for a human to confirm from the session itself. Binding the report to the current session id stops an old report from passing for a new session. The report must never hold secret values, registry credentials, raw logs or customer data.

The helpers grant no permissions and run no repository commands, Docker commands or test suites. Their work is bounded by file count and size limits in the code; wall-clock limits come from the host hook's `timeoutSec` (30 and 10 seconds in the sample), because `timeout` is not available on every platform the shell helpers run on.
