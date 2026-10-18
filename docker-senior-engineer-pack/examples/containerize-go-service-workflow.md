# Worked example: containerising a Go HTTP service

Synthetic scenario for the `containerize-application` prompt and the dockerfile-engineering and container-security-hardening skills. Names, versions and numbers are illustrative.

## Discover and frame

The repository has `go.mod` declaring the Go version, `cmd/server`, no Dockerfile, and a CI job that will later push to a registry. The image will run on a Compose host now and on an orchestrator later. `docker context show` prints `default` (local Desktop engine); `docker version` and `docker buildx version` are recorded.

Acceptance criteria, labelled as proposed until the user confirms them: builds for linux/amd64; runs as a numeric non-root user; read-only root filesystem works; answers `/healthz` on 8080; stops within 10 seconds on SIGTERM; no build tools in the runtime image.

## Runtime contract first

| Item | Value |
|---|---|
| Process | `/app/server`, no arguments |
| Port | 8080, bound to all interfaces inside the container |
| User | 65532:65532 |
| Writable paths | none; `/tmp` as tmpfs if a library needs it |
| Configuration | environment variables `LOG_LEVEL`, `DATABASE_URL_FILE` |
| Secrets | database URL from a file under `/run/secrets` |
| Health | `GET /healthz`; probed by the orchestrator, not by `HEALTHCHECK`, because the runtime image has no shell or curl |
| Stop | SIGTERM, drains in under 5 seconds |

## Design and change

Builder: the official Go image at the version in `go.mod`, run on `$BUILDPLATFORM` and cross-compiling with `TARGETOS`/`TARGETARCH` so arm64 can be added later without emulation. `CGO_ENABLED=0` because the service has no cgo dependencies; checked with `go list -deps`. Runtime: a distroless static `nonroot` base pinned by digest; `scratch` was the alternative but would need CA certificates and a passwd entry copied in by hand. Cache mounts for the module and build caches. An ignore file excludes `.git`, local env files and editor folders. Exec-form `ENTRYPOINT`; `USER 65532:65532`; `EXPOSE 8080`.

## Verify

- `docker build --check .`: no warnings.
- Cold build, then rebuild after editing one handler: the `go mod download` step is reported as cached.
- `docker image inspect --format '{{.Config.User}} {{json .Config.Entrypoint}}'`: `65532:65532 ["/app/server"]`.
- `docker run --rm -d --name task-go-smoke --read-only -p 127.0.0.1:18080:8080 <task tag>`, then `curl -fsS http://127.0.0.1:18080/healthz` succeeds and `docker top task-go-smoke` shows the process running as UID 65532.
- `docker stop task-go-smoke` returns in about one second and the container exits 0 (if the image had a shell-form entrypoint it would wait 10 seconds and exit 137).
- The task image and container are removed afterwards.

## Report

Status COMPLETE_VERIFIED only for the criteria above at local runtime level. The registry push and arm64 build are follow-ups requiring Level 2 approval and a multi-platform build; they are listed as not in scope, not as verified. See `final-completion-report.md`.
