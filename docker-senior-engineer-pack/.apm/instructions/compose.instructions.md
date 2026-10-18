---
description: "Docker Compose file changes: Compose Specification semantics, health-gated startup, scoped networks and ports, file-based secrets, task-scoped validation."
applyTo: "**/compose.yaml,**/compose.yml,**/compose.*.yaml,**/compose.*.yml,**/docker-compose.yaml,**/docker-compose.yml,**/docker-compose.*.yaml,**/docker-compose.*.yml"
---

# Compose instructions

Follow compose-environments. Discover how the project is really invoked (which files are merged, profiles, env files, project name) and validate with `docker compose config --quiet` using the same inputs; rendered config can expose interpolated secrets, so do not paste it. Write to the Compose Specification: drop the obsolete top-level `version` key and use `docker compose`, not the retired `docker-compose` v1 binary.

Gate startup on readiness with `depends_on` conditions backed by real healthchecks, and still expect services to retry connections. Services reach each other by service name and container port; publish only what the host needs, bound to 127.0.0.1 unless wider exposure is required. Keep real secrets out of the file and out of `environment`; use file-based `secrets` and commit only an example env file. Do not add `privileged`, host namespaces or a Docker socket mount without a security review. Run stacks under a task-specific project name, and never use `down -v` on a stack the task did not create.
