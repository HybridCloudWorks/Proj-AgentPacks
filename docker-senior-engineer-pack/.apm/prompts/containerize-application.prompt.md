---
description: "Containerise an application with a production-ready Dockerfile and ignore file"
agent: docker-senior-engineer
---

# Containerise an application

## Inputs

The application to containerise, the authorised repository, who will run the image (Compose, an orchestrator, a cloud service, developers) and any acceptance criteria such as platforms, size budget or base image policy. Discover the toolchain, lockfiles, build and start commands from the repository before asking.

## Workflow

Write the runtime contract first. Apply dockerfile-engineering for the stage graph, base images, cache-friendly layers and ignore file, and container-security-hardening for the runtime stage. Build and smoke-test at Level 1 when a Docker CLI is available, and measure size and rebuild behaviour. Add a Compose file only if requested, using compose-environments.

## Expected output

The Dockerfile and ignore file, the runtime contract table, the commands to build and run, measurements with their environment, and a completion report under the `docker-senior-engineer-contract` instruction. Any build or run that could not happen is listed as unverified; a grant given for one target does not cover another.
