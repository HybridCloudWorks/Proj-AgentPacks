# Tool and permission matrix

| Agent | Read and search | Edit | Shell | Web | Delegate | Cloud and billing systems | Communication |
|---|---|---|---|---|---|---|---|
| finops-professional-practitioner | Assigned workspace and data | Workspace files (Level 1) | Local checks and bounded read-only queries (Level 1) | Public documentation and pricing only | To the two specialists | Read-only; every change is Level 2 | Drafts only; sending is Level 2 |
| finops-data-analyst | Assigned data and files | None by instruction | Local query engines, read-only credentials | None | None | Read-only queries within the assigned scope and scan bound | None |
| finops-evidence-reviewer | Supplied material only | None | None | None | None | None | None |

## Tool contracts

- **Read and search.** Needed for discovery and evidence. Stay inside the assigned scope; quote aggregates rather than rows.
- **Edit.** Queries, notebooks, models, reports and drafts in the approved workspace. Preserve the user's existing work; never modify a billing export in place.
- **Shell.** Running local query engines, tests and helpers. A shell can write files, delete data and call cloud command-line tools, so a shell-capable agent is never truly read-only. For the data analyst this contradiction is stated openly: its no-edit rule is behavioural, and the host sandbox plus read-only credentials provide the real limit.
- **Web.** Public provider documentation, pricing pages and FinOps Foundation material, cited with the access date. Never send billing data, identifiers or negotiated rates in a request.
- **Delegate.** The primary sends the contract's handoff fields to a specialist and integrates the result.
- **Cloud, billing and FinOps platforms.** Reading through existing read-only credentials is Level 0 or 1. Any purchase, configuration change, policy change, export change or resource action is Level 2.
- **Communication.** Messages, tickets, emails, pull request comments and publication of figures are Level 2. Agents draft; people send.

## How permissions are declared

Canonical agents in `.apm/agents` carry no `tools` field. APM copies agent frontmatter verbatim to Claude Code and GitHub Copilot, keeps only name, description and body for Codex, and refuses a Kiro agent whose tools are not Kiro capability tags, so no single `tools` value is valid everywhere. Each agent's intended permissions are declared in `compatibility/tool-permissions.yml` as intents; `compatibility/capability-map.yml` lists the translations an installer applies (Copilot aliases, Claude Code tool names, Gemini CLI tool names, Kiro tags). APM-generated agents inherit the host's full tool set, so on an APM install these intents are guidance until an installer or the user narrows the tools. Written instructions are not access control.
