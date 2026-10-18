# Docker specialist assignment

For people who want to see a handoff written out; the binding rules are in the always-on `docker-senior-engineer-contract` instruction.

## Goal, scope and criteria

- Original goal and current task:
- In scope (Dockerfiles, ignore files, Compose, Bake, CI steps):
- Out of scope:
- Acceptance criteria and the evidence each needs:

## Build and engine facts

- Build context path and target stage:
- Target platforms:
- Engine context (name, local or remote) and engine, Buildx, Compose versions:
- Base image and registry policy:
- Evidence already collected (commands and results):
- Assumptions:

## Authority and limits

- Specialist: container-security-reviewer (read only) or container-build-verifier (read and shell, no edits)
- Commands or command classes allowed (verifier only):
- Tag prefix or Compose project name, and cleanup expected (verifier only):
- Prohibited actions (always: edits for the verifier, any command for the reviewer, login, push, sign, prune, engine changes):
- Approval state:
- Secrets shared: none. Credentials and secret values are never part of a handoff.

## Requested return

Reviewer: findings (severity, confidence, location, evidence, impact, recommended change, blocking), negative checks, missing evidence, residual risk.
Verifier: each check (command, exit code, status, environment, evidence), resources created and removed, skipped checks with reasons, observations.
Both: risks, limits and the next action. The primary reconciles and owns completion.
