# Agent Packs

Canonical source for agent packs built with the master prompt in Code Workflow (`docs/agent-pack-prompt.md`). Each folder is one complete pack: `apm.yml`, `.apm/agents`, `.apm/skills`, docs, tests, hooks, tooling, generated vendor targets, and distribution archives.

This folder is source control only. Nothing here is read by an AI client directly. The Code Workflow installer validates a pack and copies its vendor targets into the user profile, on every machine this folder syncs to.
