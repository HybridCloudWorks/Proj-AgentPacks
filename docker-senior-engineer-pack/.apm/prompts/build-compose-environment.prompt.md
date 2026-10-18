---
description: "Create or fix a Docker Compose environment for development, CI or a single host"
agent: docker-senior-engineer
---

# Build a Compose environment

## Inputs

The services involved, the target environment (local development, CI test stack, single-host deployment), existing Compose and env files, how the stack is invoked today, and each service's port, health signal, data and secrets.

## Workflow

Apply compose-environments: render the current configuration, model readiness with healthchecks and `depends_on` conditions, scope networks and published ports, move secrets into `secrets`, plan volumes, and add the development loop or CI pattern requested. Validate with `docker compose config --quiet`, then `up --wait` under a task-specific project name and tear down only that project.

## Expected output

The Compose changes, the exact commands for each environment, per-service notes on readiness, exposure and data, migration notes for renamed items, and a completion report under the `docker-senior-engineer-contract` instruction. Never delete existing volumes without Level 2 approval.
