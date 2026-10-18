# Orchestrators

An orchestrator is not a pack. It is the main agent that coordinates the installed agents and skills in one client, such as Codex or Claude Code. It is created for a desktop when that client is detected there, and its content depends on the tools found on that desktop and on the agents and skills the user selected. Because it changes from one desktop to the next, it is generated, not published as a fixed pack.

This folder keeps orchestrator material as reference until the orchestrator standard is defined, after the packs themselves are standardized. Nothing here is validated, built or released as a pack: the repository's tooling treats only top-level folders with an `apm.yml` as packs, so it skips this folder.

| Folder | What it is | State |
|---|---|---|
| `codex-agentic-orchestrator/` | The Codex orchestrator seed, formerly `codex-agentic-orchestrator-pack` | Kept unchanged as reference; not yet standardized |

The Claude Code orchestrator is installed by the Code Workflow project, not kept here.
