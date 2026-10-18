# Tool and permission matrix

| Agent | Read and search | Edit | Shell | Web | Delegate | Cloud changes |
|---|---|---|---|---|---|---|
| google-cloud-architect | Workspace and supplied material | Design documents, decision records and IaC in the approved workspace | Local validators, `terraform plan`, read-only cloud CLI commands on a named scope | Official documentation | gcp-security-reviewer, gcp-estate-inspector | Only an explicitly approved, exact Level 2 action |
| gcp-security-reviewer | Assigned documents, IaC, plan output and sanitized inventory | None | None | None | None | None |
| gcp-estate-inspector | Assigned scope's CLI output | None | Read-only cloud CLI commands only | None | None | None |

## Tool contracts

- Read and search: Level 0; record the paths and documents behind each fact.
- Edit: Level 1 in the approved workspace; preserve the user's work and review the final diff.
- Shell: Level 1 only for local validators, plans and read-only CLI commands on a scope the user named. A shell can run anything, so the real limits are the host's sandbox and approval settings and the cloud identity's IAM roles. The gcp-estate-discovery classifier rates commands before they run but enforces nothing.
- Web: official documentation; no source code, secrets or customer data in queries.
- Delegate: send only the handoff fields in the contract; the primary keeps accountability.
- Cloud changes: absent from every default profile; added only for an explicit, scoped, user-authorized action.

## How permissions are declared

No agent file under `.apm/agents` has a `tools` field, because no single value would work everywhere: APM passes the field unchanged to Claude Code and GitHub Copilot, which use different tool names, removes it for Codex, and refuses the agent for Kiro unless every value is a Kiro capability tag. The intended permissions are written instead as intents (read, edit, shell, web, delegate) in `compatibility/tool-permissions.yml`, with per-client translations in `compatibility/capability-map.yml` for installers that generate vendor files. An agent installed by APM therefore has the host's full tool set, and the pack's instructions shape its behaviour without limiting what it can technically do.
