# Tool and permission matrix

| Agent | Read and search | Edit | Shell | Web | Delegate | Registry, deploy, communication |
|---|---|---|---|---|---|---|
| docker-senior-engineer | Authorised repository and engine metadata | Workspace files | Level 0 and Level 1 Docker commands; Level 2 only with exact authority | Official documentation and public image metadata, no source or secrets in queries | The two specialists | Only an explicitly authorised exact action |
| container-security-reviewer | Assigned files and supplied evidence | None | None | None | None | None |
| container-build-verifier | Assigned files | None (behavioural; a shell can write) | Assigned Level 1 commands only | None | None | None |

## Tool contracts

- Read and search: needed for discovery and evidence. Level 0. Avoid dumping environment values, rendered Compose config or logs that may hold secrets.
- Edit: needed for Dockerfiles, ignore files, Compose, Bake and CI build steps. Level 1 in the authorised workspace; preserve user changes and report runtime contract changes.
- Shell: needed for builds, inspection, disposable runs, Compose stacks, linters and scanners. Level 1 only for local, isolated, reversible commands under task-specific tags and project names. Shell access can do anything the user's account can, including reaching the Docker socket, which is root-equivalent on most Linux hosts; real limits come from the host sandbox and from who can reach the engine. Record command, exit code, environment and a short evidence excerpt.
- Web: needed to confirm current official documentation, base image tags and platform manifests. Never paste source, secrets or private image names into a query.
- Delegate: only to the two specialists, with a contract handoff.
- Registry, deployment and communication: absent from the default profiles; each use is a Level 2 action with an exact target.

## How permissions are declared

There is no `tools` value that every client accepts: APM passes agent frontmatter unchanged to Claude Code and GitHub Copilot, strips it for Codex, and refuses a Kiro agent whose tools are not Kiro capability tags. So the agents in `.apm/agents` leave `tools` out, `compatibility/tool-permissions.yml` records each agent's intents (read, edit, shell, web, delegate), and `compatibility/capability-map.yml` records the per-vendor translations an installer applies (Copilot aliases, Claude Code tool names, Gemini CLI tool names, Kiro capability tags). Gemini CLI's verified built-ins include no web tool, so the primary's web intent has no Gemini translation. APM-generated agents inherit the host's full tool set; Codex agents inherit the parent session's sandbox and approvals. Instructions remain behavioural guidance, not access control.
