---
name: container-runtime-operations
description: "Diagnose and operate containers and image builds on a Docker host, covering exit codes, restarts, OOM kills, signals, resource limits, logging, networking, storage, engine settings and disk usage. Use when a container exits, restarts or is killed unexpectedly, a build fails, a service cannot be reached, a volume cannot be written, logs or images fill the disk, behaviour differs between environments, or daemon and runtime settings need review."
---

# Container Runtime Operations

## Purpose and activation

Find the real cause of container and build failures from evidence, fix it in the right layer, and leave the host with limits, rotation and health signals that prevent a repeat. Activate for crashes and restart loops, OOM kills, slow or stuck stops, unreachable services, permission errors on mounts, build failures, disk exhaustion, "works on my machine" differences, and reviews of engine or runtime settings.

## Scope and exclusions

In scope: Docker Engine and Docker Desktop on a single host or engine context: container state and exit codes, PID 1 and signals, restart policies, cgroup resource limits, logging drivers, bridge and user-defined networks, DNS, port publishing, volumes and bind mounts, the storage driver, `daemon.json`, contexts, rootless mode, disk usage and cleanup, and diagnosis of failing builds.

Out of scope, with the owner: cluster-level debugging of Kubernetes pods or cloud container tasks (the container-level reasoning transfers, the tooling and authority do not); application debugging past the container boundary (the application owners); host kernel tuning beyond Docker settings; incident command for production outages, where this skill supplies evidence to the incident owner.

## Inputs

- The symptom with timestamps, the exact command or Compose project, the image reference and digest, and what changed recently.
- The engine context and host: local, remote or production; Engine or Desktop; version; rootless or not; architecture.
- The service's runtime contract (port, user, health, stop signal, limits) if it is written down.

## Dependencies and tools

- Read and search; a Docker CLI for evidence (`ps -a`, `inspect`, `logs`, `events`, `stats`, `system df`, `compose ps`, `compose logs`).
- Edit for fixes in Dockerfiles, Compose files or scripts. Engine configuration changes are Level 2.
- `dockerd --validate --config-file <path>` checks a daemon configuration file without applying it, on Engine 23.0 and later.

## Workflow

1. Locate the engine first: `docker context show`, `DOCKER_HOST`. On a remote or production engine, every change is Level 2 and even reading logs needs authority, because logs and environment can hold personal data and secrets.
2. Collect evidence read-only and narrowly. Use `docker inspect --format` to pull only `State` (`ExitCode`, `OOMKilled`, `Error`, `StartedAt`, `FinishedAt`, `Health`), `RestartCount`, and selected `HostConfig` fields (memory, CPU, PID limit, restart policy, capabilities, privileged); avoid dumping `Config.Env`. Add `docker logs --tail 200 --timestamps`, `docker events --since <time> --filter container=<name>` for kill, OOM and die events, `docker stats --no-stream`, and `docker system df`. Summarise logs and redact values.
3. Classify the symptom:

| Evidence | Usual cause | Next check |
|---|---|---|
| Exit 0 at once | Command finished or daemonised into the background; command overridden | `Config.Cmd` and `Entrypoint`; foreground flag of the server |
| Exit 125 | `docker run` itself failed: bad flag, name conflict | The CLI error text |
| Exit 126 | Command not executable: permissions, `noexec` mount | File mode in the image, mount options |
| Exit 127 | Command not found: wrong PATH, binary absent from a minimal base, shell-form command with no shell | Image contents, exec form |
| Exit 137 and `OOMKilled` true | Memory limit or host memory exhausted | Limit versus peak use, runtime heap sizing |
| Exit 137 and `OOMKilled` false | SIGKILL from `docker kill` or a stop timeout: the process ignored SIGTERM, often because a shell is PID 1 | Events; exec form, `exec` in wrapper scripts, init, stop grace period |
| Exit 139 | Segmentation fault: native library or C library mismatch, emulation | Base image libc, platform |
| Exit 143 | SIGTERM: a normal stop | Who stopped it, in the events |
| `exec format error` | Wrong architecture, or a script without a valid shebang | `docker image inspect --format '{{.Architecture}}'`, script first line and line endings |
| `no such file or directory` for a file that exists | Missing dynamic loader (a glibc binary on Alpine or scratch) or a CRLF shebang | `ldd` in the builder, line endings |
| Restart loop | Crash plus a restart policy | The first failure's logs, not the latest |
| Unhealthy but running | Probe failing; plain Docker and Compose do not restart unhealthy containers | `inspect` health log; the probe tool exists |

4. Network problems. The application must listen on all interfaces inside the container, not 127.0.0.1. Check the port mapping order (`host:container`), the host IP it is bound to, and that both containers share a user-defined network: name resolution works there through the embedded DNS server, not on the default bridge. `localhost` inside a container is the container itself; reach the host with `host.docker.internal`, which on Linux needs `--add-host=host.docker.internal:host-gateway`. A bridge subnet that overlaps a VPN or corporate range breaks routing; fixing it with `default-address-pools` is an engine change.
5. Storage problems. Permission denied on a bind mount usually means the container UID does not match the host files, rootless UID mapping, or SELinux labels (`:z`, `:Z`). A read-only mount or a read-only root filesystem without a tmpfs also causes it. Named volumes copy image content only when first created empty.
6. Disk exhaustion. `docker system df -v` shows images, containers, volumes and build cache. The default `json-file` log driver does not rotate; configure `max-size` and `max-file` per container or service, or daemon-wide, or use the `local` driver. Cleaning up anything the task did not create, including prunes, is Level 2: propose the exact command and what it will remove.
7. Environment differences. Compare architecture, image digest, user, read-only setting, limits, environment and secrets presence (not values), DNS and proxy settings, mounted file permissions and line endings between the working and failing environments.
8. Slowness. Look for CPU throttling against `--cpus`, memory pressure and swap, slow bind mounts on Desktop file sharing (prefer named volumes or watch-based sync), and emulated architectures.
9. Build failures. Read the failing step and its exit code. `COPY` cannot find a file: the path is relative to the context, or the ignore file excludes it. Network or DNS errors inside `RUN`: proxies are predefined build arguments and are not persisted. Missing secret: the `--secret` flag was not passed. Wrong platform base: check `--platform`. Retry a suspect step with `--no-cache` for that one build rather than pruning shared caches.
10. Reproduce at Level 1 with the same image digest, flags, user and limits, under a task-specific name. For shell-less images, attach a debug container to the target's namespaces (`docker run --rm -it --pid=container:<name> --network=container:<name> <debug-image>`) on local disposable containers only; `docker debug` exists in Docker Desktop and depends on the subscription.
11. Fix in the right layer (Dockerfile, Compose, run flags, application config, engine config), verify, and add prevention: limits sized from measurements, log rotation, a stop grace period that covers draining, health checks, and alerts owned by the operators.

## Output

- A timeline, the evidence collected, the root cause separated from hypotheses that were ruled out, the fix, its verification, and prevention steps.
- For engine changes: the exact `daemon.json` diff, the validation command, the restart impact (`live-restore` keeps containers running during a daemon restart, outside Swarm mode) and the rollback.

## Validation

- The fix reproduces the failing condition and shows it resolved: the same exit code no longer occurs, `docker stop` completes within the grace period with exit 0 or 143, the service answers from its peer container, the volume write succeeds as the runtime user.
- Record commands, exit codes, environment and evidence; a fix verified only locally does not prove the production host.

## Failure handling and escalation

- No access to the failing host: work from the evidence supplied, state which checks need the host, and mark them unverified.
- Evidence contains secrets or personal data: stop copying it, summarise, and tell the user where the sensitive data appeared.
- The cause is in the application or the orchestrator: hand over the evidence and the container-level facts to that owner.
- A fix needs an engine restart, a prune or changes to a shared host: request Level 2 approval with impact and rollback.

## Permissions and guardrails

- Read-only evidence collection on a local or authorised engine is Level 0; disposable reproductions are Level 1; anything on a shared or production engine, any engine configuration change, restart or cleanup of resources the task did not create is Level 2.
- Never run `docker system prune -a --volumes` as a fix. Never paste unredacted environment, `inspect` or log output.

## Connection to the pack

The docker-senior-engineer agent uses this skill through the optional `diagnose-container-issue` prompt; the container-build-verifier specialist uses it to explain the failures it observes. dockerfile-engineering and compose-environments supply the fixes for causes found in images or stacks. The skill is complete when installed alone; with the full pack, the `docker-senior-engineer-contract` instruction supplies the approval levels, handoff rules and completion report.
