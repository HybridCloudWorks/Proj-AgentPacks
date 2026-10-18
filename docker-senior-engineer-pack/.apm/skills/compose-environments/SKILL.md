---
name: compose-environments
description: "Design, fix and validate Docker Compose applications for local development, CI test stacks and single-host deployments using the Compose Specification. Use when a compose file is created or changed, services start in the wrong order or never become healthy, containers cannot reach each other, environment or secret handling in Compose is unclear, or a development loop with watch, profiles or override files is needed."
---

# Compose Environments

## Purpose and activation

Make a multi-container application start the same way on every machine, become ready in the right order, expose only what it must and keep secrets out of files. Activate when a Compose file is written or changed, a stack fails to start or to become healthy, services cannot reach each other, configuration and secrets need structure, a development loop is slow, or a CI job needs a disposable stack.

## Scope and exclusions

In scope: the Compose Specification as implemented by Docker Compose v2 (`docker compose`): services, `build` and `image`, `command` and `entrypoint`, `environment` and `env_file`, interpolation, `ports` and `expose`, networks, volumes, `secrets` and `configs`, `healthcheck`, `depends_on` conditions, `restart`, `init`, `user`, `read_only`, capability and security options, resource limits, logging, profiles, override files, `include`, `extends`, `develop.watch`, and project naming.

Out of scope, with the owner: Swarm stack operations at scale and conversion to Kubernetes manifests (orchestrator owners); database backup and retention policy (the data owner, although volume handling here must not lose data); image contents (dockerfile-engineering); privilege review beyond the defaults below (container-security-hardening).

## Inputs

- Compose files and how they are really invoked: which files are merged with `-f`, active profiles, env files, project name, wrapper scripts, Makefiles and CI jobs.
- Compose and engine versions (`docker compose version`), because features such as `include`, `watch` and `depends_on.required` need recent releases.
- Each service's runtime contract: port, health signal, user, writable paths, required configuration and secrets.
- Environment intent: local development, CI test stack, or single-host production.

## Dependencies and tools

- Read, search and edit.
- Docker Compose v2 when available: `docker compose config`, `up --wait`, `ps`, `logs`, `exec`, `down`. The standalone `docker-compose` v1 binary is end of life; migrate commands to `docker compose`.
- No CLI means static review only; say so.

## Workflow

1. Render the real configuration: `docker compose config --quiet` validates the merged result; `docker compose config` prints it after merging and interpolation, so it can contain secret values; use `--no-interpolate` or summarise rather than pasting. Remove the obsolete top-level `version` key.
2. Model readiness. `depends_on` with `condition: service_healthy` requires a real healthcheck on the dependency; use `service_completed_successfully` for migration or seed jobs and `required: false` for optional dependencies. Startup ordering applies only when Compose starts the stack, not when a dependency restarts later, so applications must still retry connections. A container that is running is not necessarily ready.
3. Healthchecks: test what clients need (an HTTP endpoint, `pg_isready`, a CLI ping) with a tool that exists in the image; set `interval`, `timeout`, `retries` and `start_period`, and `start_interval` on engines that support it. Plain Docker and Compose report an unhealthy container but do not restart it.
4. Networking. The default project network resolves service names; services reach each other at `service:container-port`, never at the published host port. Use separate networks to isolate tiers and `internal: true` for networks with no outside access. Publish only what the host needs, as `127.0.0.1:<host>:<container>` for local-only access. Avoid fixed `container_name`, which blocks scaling and running two copies of the project.
5. Configuration and secrets. The `.env` file in the project directory feeds interpolation of the Compose file itself; `env_file` sets variables inside containers; they are different mechanisms. Fail fast on required values with `${VAR:?message}` and give defaults with `${VAR:-default}`. Commit an example env file, never the real one. Values in `environment` are visible through `docker inspect`; prefer top-level `secrets` (from a file, or from an environment variable on recent Compose), mounted at `/run/secrets/<name>`, with images that support a `*_FILE` variable convention.
6. Data. Use named volumes for state and bind mounts for source code in development, read-only (`:ro`) where possible. Watch for UID mismatches between the container user and bind-mounted files, and SELinux labels (`:z` or `:Z`). A named volume is populated from the image only while it is empty. `docker compose down` keeps named volumes; `down -v` deletes them.
7. Development loop. Prefer `develop.watch` (`sync`, `rebuild`, `sync+restart`, with `ignore` rules) on Compose releases that support it over bind-mounting the whole tree; otherwise bind-mount source and keep dependency folders in an anonymous volume. Point `build.target` at a development stage, put optional tools behind `profiles`, and keep development-only settings in an override file.
8. Single-host production. Run built images, not `build:`, pinned by digest or an immutable tag; set a `restart` policy, healthchecks, `init: true` where the process spawns children, `stop_grace_period` long enough to drain, resource limits (`deploy.resources.limits` or `mem_limit` and `cpus`), log rotation, `read_only` with `tmpfs`, `cap_drop: [ALL]` with only the needed additions, and `security_opt: [no-new-privileges:true]`.
9. CI test stacks: a unique project name per job (`-p`), `docker compose up --wait` to wait for health, `--abort-on-container-exit --exit-code-from <tests>` for a test runner service, and teardown of that project only with `down -v --remove-orphans`.

## Output

- The Compose changes, with a short note per service on readiness, exposure, configuration and data handling.
- The exact commands to run the stack in each intended environment, including file order, profiles and project name.
- Migration notes for anything renamed or removed (services, volumes, ports, variables).

## Validation

- Static: `docker compose config --quiet` with the same files, profiles and env files that real use passes.
- Local runtime at Level 1: `docker compose -p <task-project> up --wait`, then `ps` shows every service healthy; one connectivity check per dependency through `exec`; then `docker compose -p <task-project> down -v` for that task project only.
- Record each check with command, exit code, environment and evidence; mark features that need a newer Compose release as unverified when the installed release lacks them.

## Failure handling and escalation

- Never healthy: read `docker compose logs <service>` and `docker inspect` health output, check the probe exists in the image and that `start_period` covers start-up time.
- Port already allocated or name conflicts: change the host port or project name; do not stop other projects' containers.
- Variable unset warnings: add `${VAR:?}` guards and document the variable.
- A feature missing in the installed Compose: feature-detect with `docker compose version`, fall back, and record the minimum version.
- A change that would delete or move existing volume data: stop and request Level 2 approval with a backup plan.

## Permissions and guardrails

- Never run `down -v`, `rm` or prune against a stack the task did not create. Never commit real secrets or paste rendered config containing them.
- Do not publish databases or admin interfaces on all interfaces by default, and do not add `privileged`, host namespaces or a Docker socket mount without a security review.
- Running a stack against a remote or production engine is Level 2.

## Connection to the pack

The docker-senior-engineer agent uses this skill through the optional `build-compose-environment` prompt and when diagnosing multi-service problems with container-runtime-operations; docker-change-review uses it to review Compose diffs. The skill is complete when installed alone; with the full pack, the `docker-senior-engineer-contract` instruction supplies the approval levels, handoff rules and completion report.
