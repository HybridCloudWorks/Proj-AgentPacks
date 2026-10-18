---
description: "Investigate an unfamiliar Python repository"
agent: python-distinguished-engineer
---

# Investigate an unfamiliar Python repository

## Inputs

Use the user's current task, authorized repository, acceptance criteria and relevant existing evidence. Discover missing local facts before asking. Do not invent credentials or organizational policy.

## Workflow

Read authorized code/configuration without editing; inspect interpreter/packaging/locks, relevant modules/callers/tests, CI, deployment, ADRs and risk. Use python-language-engineering and python-packaging.

## Expected output

Facts with paths, version/toolchain conflicts, interface map, unknowns and proposed validation commands. State failures and unavailable checks honestly. Follow the `python-engineering-contract` instruction; existing authorization persists only within its scope.
