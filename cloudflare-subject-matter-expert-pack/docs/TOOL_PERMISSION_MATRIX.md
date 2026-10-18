# Tool and permission matrix

| Agent | Read and search | Edit | Execute | Web and documentation | Cloudflare account | Delegate |
|---|---|---|---|---|---|---|
| Primary | Authorized workspace | Scoped code, configuration, tests and docs | Local builds, tests, checkers, credential-free Wrangler; account commands only under Level 2 approval | Public Cloudflare documentation and connected documentation tools | Read inside stated scope; writes only under Level 2 approval with the user's configured credential | Specialists |
| Security reviewer | Assigned files and exports | None | None | Public documentation only, no account data in queries | None | None |
| Migration analyst | Assigned export files | Mapping artifacts in the assigned folder | Local parsing and the accounting checker | None | None | None |

## Tool contracts

- Read and search: discovery and evidence. Stay inside the authorized workspace; do not open secrets files to read values.
- Edit: scoped implementation. Preserve user changes and review the final diff. Substantial overwrites or deletions are Level 2.
- Execute: local evidence. A shell can mutate the workspace and reach the network, so a shell grant is never a read-only guarantee. Record command, environment label, exit code and summarized result.
- Web: current documentation. Never put account identifiers, hostnames, policy contents, logs or source code into a search or URL.
- Cloudflare account access: through the user's configured Wrangler login, API token or connected Cloudflare MCP tools, scoped by the token's permissions. The pack configures no credential and no MCP server. Read calls stay inside the stated scope; write calls are Level 2.
- Delegation: the primary only, with the handoff fields from the contract.

## How permissions are declared

Canonical agents in `.apm/agents` carry no `tools` field. APM copies agent frontmatter verbatim to Claude Code and GitHub Copilot, drops it for Codex, and rejects anything outside Kiro's capability tags, so no single `tools` value is valid everywhere. Each agent's intended permissions are declared in `compatibility/tool-permissions.yml` as intents (read, edit, shell, web, delegate). APM-generated agents inherit the host's full tool set; the Code Workflow installer translates the intents into each vendor's tool names (see `compatibility/capability-map.yml`). Gemini CLI has no verified web tool name in the vendor facts this pack relies on, so the web intent is not mapped for Gemini.

Instructions are behavioral guidance, not access control. The effective limits are the client's permission mode, the Cloudflare API token's permission groups and resources, CI environment protections and network policy.
