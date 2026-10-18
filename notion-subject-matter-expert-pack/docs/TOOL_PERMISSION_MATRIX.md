# Tool and permission matrix

| Agent | Read and search | Edit local files | Execute | Web | Notion read | Notion write | Delegate |
|---|---|---|---|---|---|---|---|
| notion-subject-matter-expert | Authorized workspace and repository | Drafts, integration code and tests in the user's repository | The pack's check scripts and the project's tests | Official Notion and vendor documentation | Within task scope | Level 1 as requested; Level 2 after explicit approval | notion-governance-reviewer |
| notion-governance-reviewer | Assigned content and change lists | None | None | None | Assigned pages and schemas only | None | None |

## Tool contracts

- Read and search: needed for discovery and evidence. Stay within the task's scope; do not browse unrelated private pages. Level 0.
- Edit: local drafts, integration code and tests in the repository the user is working in. Level 1. Preserve the user's changes.
- Execute: the pack's `tooling/` scripts and the project's own test commands. Shell access can write files and reach the network, so it is never a read-only guarantee; the reviewer gets none.
- Web: reading official Notion and vendor documentation for current facts. Do not send workspace content in queries without approval.
- Notion read: search, fetch and data-source queries. The connector's identity decides what is reachable; the agent narrows further to the task.
- Notion write: create, update, move, duplicate, archive, comment, schema and sharing operations, gated by the approval matrix. Every write is confirmed by fetching the result.
- Delegate: the primary may launch the reviewer where the host supports subagents.

## How permissions are declared

Canonical agents in `.apm/agents` carry no `tools` field. APM copies agent frontmatter verbatim to Claude Code and GitHub Copilot, drops it for Codex, and rejects anything outside Kiro's capability tags, so no single `tools` value is valid everywhere. Each agent's intended permissions are declared in `compatibility/tool-permissions.yml` as intents (read, edit, shell, web, delegate) plus a `notion` line naming the Notion operations it should receive. `compatibility/capability-map.yml` records the per-vendor translations an installer applies, with the user's Notion MCP server name substituted.

APM-generated agents inherit the host's full tool set, including Notion write tools. Until an installer or the user restricts the reviewer's tools, its read-only behaviour is an instruction, not an enforced control; it is told to leave write tools unused and say so. Real access control comes from the connector's sign-in identity, Notion's sharing settings and the host's permission prompts. Codex subagents inherit the parent session's sandbox and approvals.
