---
description: "Dockerfile, Containerfile and ignore-file changes: pinned bases, multi-stage graphs, cache-friendly layers, no secrets in layers, non-root exec-form runtime."
applyTo: "**/Dockerfile,**/Dockerfile.*,**/*.Dockerfile,**/*.dockerfile,**/Containerfile,**/Containerfile.*,**/.dockerignore,**/*.dockerignore"
---

# Dockerfile instructions

Follow dockerfile-engineering; use container-security-hardening for the runtime stage. Find out how the file is built (context path, target stage, build args, platforms) and who runs the image before changing it; the build context, not the Dockerfile's folder, decides which ignore file applies. Keep stage names, ports, users and paths that CI, Compose or orchestrators depend on, or report the contract change.

Pin base images to a specific version tag, and by digest where reproducibility matters; never introduce `latest`. Copy dependency manifests and lockfiles before source so dependency layers stay cached, and use BuildKit cache mounts instead of leaving package caches in layers. Never pass credentials through ARG, ENV, COPY, labels or files that reach any stage; use secret or SSH mounts. The runtime stage carries only what runs, sets a numeric non-root `USER`, uses exec-form `ENTRYPOINT`/`CMD`, and adds a `HEALTHCHECK` only when the consumer uses it and the probe tool exists in the image. Validate with `docker build --check` or the repository's linter, then a build and a disposable run when Level 1 allows; otherwise report the build as unverified.
