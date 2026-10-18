# Guardrail decision record

Produced by `agent-governance-and-guardrails` for any agent, workflow, MCP server, copilot or automation that can read external data, modify a repository, open a pull request, publish an output, access secrets or affect production.

| Item | Value |
|---|---|
| Subject | <workflow, agent, MCP server or automation> |
| Files reviewed | <source and generated paths, with commit> |
| Requested change | <capability being added or reviewed, or "review only"> |
| Reviewer and date | |

## Capabilities

One row per capability. Control is one of: enforced by platform, enforced by repository policy, advisory, missing.

| Actor | Data | Tool | Permission | Destination | Mutation | Approval point | Failure behavior | Rollback | Control |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## Review checks

| Check | Evidence | Result |
|---|---|---|
| Workflow `permissions` are the smallest supported set | | |
| Writes go through reviewable safe outputs, with allowlists and limits | | |
| Engine, tool and MCP allowlists declared | | |
| Network destinations declared | | |
| Secrets only through the secret mechanism, absent from prompts, logs and outputs | | |
| Runner labels reviewed; no privileged or self-hosted runner without owner review | | |
| Generated lock does not broaden permissions or add tools | | |
| Write paths are idempotent, with bounded retries and duplicate-output handling | | |
| Untrusted inputs identified: issues, pull requests, web pages, tool results | | |

Mark structural evidence separately from live or third-party evidence.

## Approvals required

| Decision | Owner | Asked | Answer |
|---|---|---|---|
| | | | |

Live runs, permission grants, branch-protection changes, merges, releases and production changes need explicit authorization before they happen.
