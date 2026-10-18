# Agent inventory

| Profile | Responsibility | Invocation | Declared intent (see TOOL_PERMISSION_MATRIX.md) |
|---|---|---|---|
| docker-senior-engineer | Owns every workflow: containerising, optimising and hardening images, Compose environments, multi-platform builds and supply chain, runtime diagnosis and change review. Integrates specialist results and owns the completion report. | User-facing primary (`user-invocable: true`) | read, edit, shell, web, delegate |
| container-security-reviewer | Independent, read-only security review of Dockerfiles, Compose files, engine settings and image supply chain; returns located findings and negative checks. | Optional specialist (`user-invocable: false`) | read |
| container-build-verifier | Runs the builds, static checks, scans and disposable smoke tests the handoff assigns, and returns commands, environments, exit codes and evidence; cleans up only what it created. | Optional specialist (`user-invocable: false`) | read, shell |

## Why these specialists exist

- The security reviewer gives an independent opinion with genuinely narrower permissions: no edit, no shell, no network. An author reviewing their own image is the failure it prevents.
- The build verifier gives execution evidence produced by someone other than the author, and keeps long build, scan and log output out of the primary's context. It has a shell but no edit permission; a shell can write files, so that restriction is behavioural unless the host sandboxes the profile, and the agent body says so.

No specialist exists for Compose, CI or diagnosis: those need the same permissions and context as the primary, so a separate profile would add handoff cost without independence.

## Placement and activation

All three profiles live in each client's documented agent folder; there is no separate subagents folder. Specialists are activated only by the primary, with a handoff built from the `docker-senior-engineer-contract` instruction (see HANDOFF_CONTRACT.md). Specialists set `include-custom-instructions: true` so GitHub Copilot subagents receive the installed instructions. Gemini CLI receives no agents from APM; there the primary's workflows are reachable through skills, instructions and commands. If delegation is unavailable in any client, the primary does the same narrow work with the same skills and reports that it was not independent.

No canonical agent sets `tools`. When APM generates the vendor files, each agent simply gets whatever tools the host offers; an installer that writes vendor files itself should narrow them to the intents in the table.
