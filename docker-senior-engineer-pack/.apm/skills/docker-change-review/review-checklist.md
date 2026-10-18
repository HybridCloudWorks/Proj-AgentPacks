# Container change review checklist

Used by the docker-change-review skill. Each item says what to look for and why it matters. A matched item is a candidate finding, not a finding: confirm it with evidence and a failure scenario first.

## Correctness and runtime contract

- Stage names used by `--target`, Compose `build.target` or Bake still exist. Renaming one silently builds the wrong stage or fails.
- `EXPOSE`, the listening port, published ports and health probes agree. Mismatches produce containers that start but never serve.
- The process binds to all interfaces inside the container. A server bound to 127.0.0.1 is unreachable through a published port.
- `ENTRYPOINT`/`CMD` are exec form, wrapper scripts end with `exec "$@"`, and an init is used when the process spawns children. Otherwise SIGTERM never reaches the application and every stop becomes a SIGKILL after the timeout.
- Paths the application writes to are writable by the runtime user, and are volumes or tmpfs under a read-only root filesystem.
- Scripts copied into the image have an executable bit and LF line endings; a CRLF shebang fails with "no such file or directory".

## Reproducibility

- Bases are pinned to a specific version tag, and by digest where builds must be reproducible. `latest` or a bare major version makes the same commit build different images.
- Package installs follow the lockfile (`npm ci`, `pip install --require-hashes` or a locked tool, `go mod download`); unpinned installs drift between builds.
- Downloads are verified with a checksum or signature (`ADD --checksum` or an explicit check). An unverified download is a supply-chain entry point.

## Cache and size

- Manifests and lockfiles are copied and dependencies installed before the source is copied. Otherwise every source change reinstalls every dependency.
- Package caches use cache mounts or are removed in the same `RUN`. Removing them in a later layer does not shrink the image.
- The runtime stage copies only artefacts. Toolchains, compilers, test data and source in the runtime stage cost size and attack surface.
- The ignore file excludes VCS metadata, local env files, credentials and host-built dependencies, and does not exclude something the build needs.
- Frequently changing arguments (revision, date) are not declared before expensive steps, where they would bust the cache on every build.

## Image and build security

- No credentials in `ARG`, `ENV`, labels or copied files in any stage. Build-argument values show up in history and in maximum-mode provenance; copied files stay in their layer and in exported cache.
- Private dependencies use `--mount=type=secret` or `--mount=type=ssh`.
- The final `USER` is a numeric non-root UID. A name cannot be verified as non-root by orchestrators, and the base image's default is usually root.
- No setuid helpers, shells or package managers in the runtime stage unless the workload needs them.
- No `curl ... | sh` without verification, no disabled TLS or signature checks, no `chmod 777`.

## Runtime privileges and exposure

- No `privileged`, host network, PID or IPC namespaces, `SYS_ADMIN`, extra devices or `unconfined` security profiles without a written justification.
- No Docker socket mount. It hands control of the host to the container, read-only or not.
- Capabilities are dropped to the minimum and `no-new-privileges` is set for production services.
- Published ports are limited to what the host needs and bound to 127.0.0.1 when local; on Linux, published ports bypass host firewalls.
- Memory and PID limits exist for services that could exhaust the host.

## Compose semantics

- No top-level `version` key and no reliance on the retired `docker-compose` v1 binary.
- `depends_on` conditions are backed by real healthchecks; dependent services still retry connections.
- Secrets come from `secrets` or external injection, not literal values in `environment` or committed env files.
- Volumes holding data are named and survive `down`; nothing in the change runs `down -v` against existing data.
- No fixed `container_name` where the project might run twice or scale.

## CI and supply chain

- Third-party actions or templates are pinned to an immutable reference.
- Registry write permissions are limited to the pushing job; untrusted pull requests cannot push or read registry credentials.
- Tags include an immutable identifier; deployments and signatures use digests.
- Registry cache exports with `mode=max` cannot expose secrets from intermediate stages, and the cache repository is access-controlled like the image.
- SBOM, provenance and signing settings match policy, and maximum-mode provenance is not combined with sensitive build arguments.
- Scans run before promotion, and promotion copies the scanned digest instead of rebuilding.

## Operability

- Stop signal and grace period cover the application's drain time.
- Health checks exist where the consumer uses them, with a probe tool present in the image and a `start_period` that covers start-up.
- Logs go to stdout and stderr, and log rotation is configured where the host uses `json-file`.
- Resource limits match measured use, and runtimes that size memory from the container limit are configured to do so.
