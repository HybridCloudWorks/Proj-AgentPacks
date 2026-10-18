# syntax=docker/dockerfile:1
# Synthetic test fixture for tooling/container_lint.py. Digests are placeholders made of zeros and ones.
ARG GO_IMAGE=golang:1.24-bookworm@sha256:0000000000000000000000000000000000000000000000000000000000000000

FROM --platform=$BUILDPLATFORM ${GO_IMAGE} AS build
WORKDIR /src
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends ca-certificates
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
COPY cmd ./cmd
COPY internal ./internal
RUN <<EOF
set -e
# Heredoc body: the next line is shell text, not a Dockerfile instruction.
echo "USER root"
EOF
ARG TARGETOS TARGETARCH
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH go build -trimpath -o /out/server ./cmd/server

FROM gcr.io/distroless/static-debian12:nonroot@sha256:1111111111111111111111111111111111111111111111111111111111111111 AS runtime
COPY --from=build /out/server /app/server
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/app/server"]
