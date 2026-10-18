# Worked completion report

For the synthetic Go containerisation in `containerize-go-service-workflow.md`. Values are illustrative; real reports carry the actual commands and output.

Status: COMPLETE_VERIFIED for the agreed local criteria. Registry, arm64 and orchestrator behaviour were out of scope and are listed as follow-ups, not as verified.

Outcome: the service has a multi-stage Dockerfile and ignore file producing a non-root, read-only-compatible runtime image.

| Criterion | Status | Evidence level | Evidence |
|---|---|---|---|
| Builds for linux/amd64 | passed | local build | `docker build -t task-go:local .` exit 0 |
| Numeric non-root user | passed | local runtime | `docker image inspect` shows `Config.User` `65532:65532`; `docker top` on the running container shows the process UID 65532 (the image has no shell for `id`) |
| Read-only root filesystem | passed | local runtime | started with `--read-only`; health endpoint answered |
| Stops within 10 s | passed | local runtime | `docker stop` returned in about 1 s; exit 0 |
| No build tools in runtime | passed | static | `docker history` shows only the binary layer above the base |

Files changed: `Dockerfile`, `.dockerignore`.

Decisions: distroless static base over `scratch` (CA certificates and passwd entry included); cross-compiling builder for later arm64 support; no `HEALTHCHECK` because the image has no probe tool and the consumer probes over HTTP.

Image impact: one runtime layer above the base; size recorded with the command and engine used. Runtime contract impact: new image; contract table delivered. Security review: non-root, read-only compatible, no shell, no secrets in arguments or environment. Supply chain impact: bases pinned by digest; no SBOM, provenance or signature yet. Platform compatibility: linux/amd64 verified; arm64 not built. Operational impact: none until deployed.

Checks: each recorded with command, exit code, status, environment (local Desktop engine, default builder, linux/amd64, versions) and evidence. Unverified: none within scope. Remaining risks: base digest ages without update automation. Rollback: remove the files; no consumer depends on them yet. Follow-ups: multi-platform build and first push (Level 2), Renovate digest updates, orchestrator probes using the contract table.

If any criterion above had lacked executed evidence, the status would have been IMPLEMENTATION_PREPARED_NOT_VERIFIED and the report would end with: "Container change is prepared, but completion is not verified."

The JSON fixtures in `tests/fixtures` exercise the report validator only; their values are synthetic and are never a real completion claim.
