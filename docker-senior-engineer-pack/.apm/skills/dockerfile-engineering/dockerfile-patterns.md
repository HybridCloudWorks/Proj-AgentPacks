# Dockerfile patterns

Reference material for the dockerfile-engineering skill. Versions shown in `ARG` defaults are examples only: replace them with the versions the repository declares, and pin digests where the build must be reproducible.

## Stage skeleton

```dockerfile
# syntax=docker/dockerfile:1

ARG RUNTIME_IMAGE=gcr.io/distroless/static-debian12:nonroot

FROM --platform=$BUILDPLATFORM golang:1.24-bookworm AS build
WORKDIR /src
# Manifests first: this layer stays cached until dependencies change.
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
COPY . .
ARG TARGETOS TARGETARCH
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH \
    go build -trimpath -ldflags="-s -w" -o /out/server ./cmd/server

FROM build AS test
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go test ./...

FROM ${RUNTIME_IMAGE} AS runtime
COPY --from=build /out/server /app/server
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/app/server"]
# Late, frequently changing metadata does not invalidate the layers above.
ARG REVISION=unknown
LABEL org.opencontainers.image.revision=$REVISION
```

`docker build --target test .` runs the tests; the default build produces only the runtime stage, and the test stage is skipped because nothing depends on it.

## Ecosystem notes

- Go: build statically with `CGO_ENABLED=0` for `scratch` or distroless static bases. With cgo, use a glibc runtime base that matches the builder's C library. Cross-compile from `$BUILDPLATFORM` instead of emulating the target.
- Node.js: install with `npm ci` (or the repository's lockfile-respecting command) in a dependency stage and `npm ci --omit=dev` for the runtime set; cache `/root/.npm`. Run `node` directly as PID 1, not `npm start`, so signals reach the application. Official Node images include a `node` user with UID 1000.
- Python: build wheels or a virtual environment in the builder and copy it to a slim runtime stage; cache `/root/.cache/pip` or, with uv, `/root/.cache/uv` (set `UV_LINK_MODE=copy` when the cache is a mount). Set `PYTHONUNBUFFERED=1` so logs are not held in a buffer.
- JVM: build with the JDK image and run on a JRE or a minimal runtime image; use the framework's layered-jar extraction where it exists so dependency layers are cached apart from application classes. Size the heap from the container limit with `-XX:MaxRAMPercentage` rather than fixed `-Xmx` values.
- .NET: `dotnet publish` in the SDK image, run on the ASP.NET or runtime image (or a chiseled variant). Current official images define a non-root `app` user, exposed as `$APP_UID`.
- Rust: cache `/usr/local/cargo/registry` and the target directory with cache mounts, and copy the binary out of the target directory within the same `RUN`, because a cache mount's content is not part of the layer.

## Package managers in RUN

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends ca-certificates
```

Without cache mounts: `apt-get update && apt-get install -y --no-install-recommends <packages> && rm -rf /var/lib/apt/lists/*` in one `RUN`, and `apk add --no-cache <packages>` on Alpine. Debian-based official images delete downloaded packages automatically through an apt configuration file; remove it in the cache-mount variant if the cache should be kept.

## Build secrets

```dockerfile
RUN --mount=type=secret,id=npm_token,target=/run/secrets/npm_token \
    NPM_TOKEN="$(cat /run/secrets/npm_token)" npm ci
```

Build with `docker build --secret id=npm_token,env=NPM_TOKEN .` (or `src=<file>`). The value exists only for that `RUN`; it is not stored in a layer, the history or the cache. Recent Dockerfile frontends can also expose a secret directly as an environment variable for one `RUN` step.

## Ignore-file baseline

```
# VCS and tooling
.git
.gitignore
.github
.vscode
.idea
# Local configuration and credentials
.env
.env.*
!.env.example
*.pem
*.key
.npmrc
.pypirc
# Host-built dependencies and outputs
node_modules
.venv
__pycache__
dist
build
target
coverage
# Container files themselves
Dockerfile*
*.dockerignore
compose*.y*ml
docker-compose*.y*ml
```

Adjust for the repository: if the build needs a file listed here, re-include it with a `!` line rather than deleting the exclusion.
