# Design Decisions

## Codex-first adapter

The first implementation targets Codex's project-local `.codex/agents`, `.agents/skills`, `.codex/config.toml`, and `.codex/hooks.json`. Other clients can receive adapters later without changing the workflow contract.

## Thin parent, specialist children

The parent custom agent routes, records state, and synthesizes. Domain work remains in separate custom agents and Skills so the parent does not duplicate the user's specialist packs.

## Durable state before delegation

The workflow directory is created before the first subagent request. This makes partial execution, retries, and “did it actually run?” questions answerable from files rather than memory.

## Required versus optional availability

The registry is data-driven. Optional missing agents produce a recorded skip. Required missing agents block. This avoids hard-coding the assumption that every pack is installed.

## Trust-aware hooks

Codex documents that project hooks require trust review. The target ships a reviewable `hooks.json` rather than silently modifying a user's existing config. Hooks are evidence and continuation guardrails; they cannot make a subagent appear to have run.

## No universal success promise

The pack guarantees a truthful terminal outcome, not successful model execution under unavailable authentication, permissions, network, quota, or client conditions.
