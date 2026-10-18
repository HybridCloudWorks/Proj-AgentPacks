---
name: dockerfile-engineering
description: "Author, refactor and optimise Dockerfiles and Containerfiles with deliberate base images, multi-stage graphs, cache-efficient layers, tight build contexts and an explicit runtime contract. Use when an application needs containerising, an image is too large or slow to build, a Dockerfile is being changed, or build behaviour such as caching, stages, build arguments or entrypoints is in question."
---

# Dockerfile Engineering

## Purpose and activation

Produce a Dockerfile a reviewer can reason about: every stage has one job, the runtime stage carries only what runs, and the image states how it expects to be run. Activate when an application is containerised for the first time, a Dockerfile or ignore file changes, an image is too large or slow to build, a base image is being replaced, or a container misbehaves because of how it was built (wrong user, lost signals, missing files, cache that never hits).

## Scope and exclusions

In scope: Dockerfile and Containerfile syntax and frontend features, parser directives, base image choice, stage graph, layer order and cache behaviour, BuildKit mounts, build context and ignore files, build arguments and environment, user, ports, entrypoint and command, stop signal, health checks, OCI labels, and ecosystem-specific build patterns.

Out of scope, with the owner: multi-platform builders, CI cache backends, tagging, pushing, SBOM, provenance and signing (image-build-and-supply-chain); vulnerability triage and runtime privilege hardening beyond the runtime stage basics (container-security-hardening); Compose files (compose-environments); Kubernetes, ECS, Nomad or other orchestrator manifests, which belong to their owners: hand them the runtime contract instead. Application code changes, such as adding a health endpoint or binding to all interfaces, are proposed separately, not slipped into a Dockerfile change.

## Inputs

- Application layout, language and toolchain versions, lockfiles, build and start commands, native libraries the artefact needs at runtime.
- Existing Dockerfiles, ignore files, Bake or Compose `build` sections and CI build commands: context path, target stage, build arguments, platforms.
- The consumer of the image (Compose, Kubernetes, a cloud container service, developer machines) and what it expects: port, user, health probe, signals, read-only root filesystem, writable paths.
- Base image policy (approved registries, hardened or vendor bases, licence limits) and acceptance criteria such as a size or build-time budget.

## Dependencies and tools

- Read and search for discovery; edit for changes.
- A Docker CLI with BuildKit (default builder since Engine 23.0), when available and permitted at Level 1. `docker build --check` runs the Dockerfile build checks without building on current Buildx releases; use hadolint instead or as well when the repository already does.
- `dockerfile-patterns.md` in this skill folder: a stage skeleton, ecosystem notes and an ignore-file baseline.
- Podman or Buildah builds accept most of this, but verify each BuildKit-specific feature against the installed version.
- With no CLI the work is static; say so in the report.

## Workflow

1. Discover. List every Dockerfile, Containerfile and ignore file. Record the context each one is built with (CI, Compose `build.context`, Bake, scripts). The ignore file that applies is the one at the context root, or a `<Dockerfile-name>.dockerignore` beside the Dockerfile, which BuildKit prefers. Note the `# syntax=` directive; `docker/dockerfile:1` tracks the current stable 1.x frontend.
2. Write down the runtime contract before editing: process and arguments, listening port and bind address (all interfaces inside the container, not 127.0.0.1), user and numeric UID/GID, writable paths, configuration inputs, where runtime secrets come from, health signal, stop signal and drain time, memory and CPU expectations.
3. Choose a base per stage. Builder stages use the toolchain image at the version the repository declares. The runtime stage uses the smallest base that runs the artefact: `scratch` for static binaries (add CA certificates, time zone data and a passwd entry if needed), a distroless or similar shell-less base for runtimes, a slim glibc distribution when a package manager or shell is genuinely needed, Alpine only when musl compatibility is verified for native modules and DNS behaviour. Prefer bases the organisation approves. Pin a specific version tag, never `latest` or a bare major, and pin by digest (`name:tag@sha256:...`) when builds must be reproducible.
4. Design the stage graph: dependencies, build, optional test, runtime, plus a separate development target if developers need one. Independent stages run in parallel under BuildKit. Keep stage names stable because `--target` consumers depend on them. For cross-compiled languages use `FROM --platform=$BUILDPLATFORM` in the builder and the `TARGETOS`/`TARGETARCH` arguments; coordinate multi-platform output with image-build-and-supply-chain.
5. Order layers for the cache. Copy manifests and lockfiles, install dependencies, then copy source. Use `RUN --mount=type=cache` for package-manager caches, `--mount=type=bind` to use files without copying them, and `--mount=type=secret` or `--mount=type=ssh` for credentials. Without a cache mount, clean package indexes in the same `RUN` that created them. Group commands that change together; do not merge unrelated steps just to reduce layer count, because cache reuse matters more than the count.
6. Tighten the context. The ignore file excludes VCS metadata, local env files, keys and credentials, host-built dependency folders, build output, test artefacts and editor files; an allow-list (`*` followed by `!` entries) suits large repositories. In the runtime stage prefer explicit `COPY` paths over copying the whole context.
7. Write the runtime stage. Use or create a non-root user with a fixed numeric UID/GID and set `USER` numerically, because orchestrators can only verify a numeric user as non-root. Copy only artefacts with `COPY --from=<stage>`; keep application files owned by root and read-only to the runtime user unless it must write them. Use an absolute `WORKDIR`, document the port with `EXPOSE`, and use exec-form `ENTRYPOINT`/`CMD`. A wrapper script ends with `exec "$@"` so the application becomes PID 1 and receives signals. Add an init (`docker run --init`, tini, dumb-init) when the process spawns children. Set `STOPSIGNAL` if the application drains on a signal other than SIGTERM.
8. Health checks: add `HEALTHCHECK` only when the consumer uses it (Docker, Compose and Swarm do; Kubernetes ignores it and uses its own probes) and only with a probe that exists in the image. Do not install curl into a minimal image just to probe it.
9. Arguments and labels. Build-argument values used by `RUN` appear in image history and in maximum-mode provenance, and `ENV` persists into every container and `inspect`, so neither may carry secrets. Arguments declared before the first `FROM` are visible only to `FROM` lines unless redeclared in a stage. Put frequently changing arguments (revision, build date) late, ideally only in labels, so they do not invalidate earlier layers. Add OCI labels such as `org.opencontainers.image.source`, `revision`, `version` and `licenses`.
10. Measure before and after: image size (`docker image ls`), large layers (`docker history`), cold build time, and a rebuild after touching one source file, which must reuse the dependency layers.

## Output

- The changed Dockerfiles and ignore files, with a one-line rationale for each non-obvious choice (base, stage graph, user, mounts).
- A runtime contract table: process, port, user and UID, writable paths, configuration, secret source, health, stop signal, resources.
- Before and after measurements with the commands and environment used, or a plain statement that nothing was measured.

## Validation

- Static: `docker build --check` or the repository's linter; compare the ignore file against what the context really contains.
- Build: a cold build, then a rebuild after a source-only change; the dependency steps must show as cached.
- Inspect: `docker image inspect --format` for `Config.User`, `Entrypoint`, `Cmd`, `ExposedPorts` and labels; `docker history --no-trunc` for leaked arguments and unexpectedly large layers.
- Runtime smoke test at Level 1: run the image with `--rm` as the declared user, with `--read-only --tmpfs /tmp` when the contract says read-only; check that it starts, listens on the expected port, passes its health check, and exits within the stop timeout on `docker stop` (exit 0 or 143, not 137).
- Record each check in the contract's check format with the evidence level reached.

## Failure handling and escalation

- Unknown build or start command: derive it from repository scripts and CI; if still unknown, deliver the Dockerfile with the assumption marked and report the build as unverified rather than guessing silently.
- A native dependency fails on a minimal base: move the runtime stage to a slim glibc base or copy the exact runtime library, and record the size trade-off.
- `exec format error`, a missing dynamic loader or line-ending problems at start-up: diagnose with container-runtime-operations.
- Private package feeds or Git repositories: use secret or SSH mounts with credentials the user supplies at build time; registry or feed login is Level 2. Never write credentials into a file to make a build pass.
- A base image outside policy: propose it with rationale; do not adopt it silently.
- No Docker CLI or no Level 1 authority to build: deliver static validation only and use the contract's fallback sentence.

## Permissions and guardrails

- Edits stay in the authorised workspace. Builds go to the local image store under a task-specific tag; no push, login, prune or builder changes.
- Never place secrets in ARG, ENV, labels or copied files; never disable TLS verification or package signature checks to get a build through; never pipe a download into a shell without verifying a checksum or signature (`ADD --checksum` exists for remote files).
- Preserve existing conventions (base family, user names, stage names, paths) unless the requested outcome needs a change, and report every change to the runtime contract.

## Connection to the pack

The docker-senior-engineer agent applies this skill through the optional `containerize-application` and `optimize-image` prompts. container-security-hardening extends the runtime stage, image-build-and-supply-chain takes the Dockerfile to multi-platform builds and registries, and docker-change-review reviews the result. The skill is self-contained when installed alone; with the full pack, the `docker-senior-engineer-contract` instruction supplies the approval levels, handoff rules and completion report.
