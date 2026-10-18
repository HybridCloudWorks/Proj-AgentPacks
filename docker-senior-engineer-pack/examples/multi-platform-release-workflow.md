# Worked example: amd64 and arm64 images with SBOM, provenance and signatures

Synthetic scenario for the `set-up-image-pipeline` prompt, the image-build-and-supply-chain skill and the container-build-verifier specialist.

## Inputs

A Go service (see `containerize-go-service-workflow.md`) must run on x86-64 servers and arm64 cloud instances. Policy: SBOM and provenance on every release, keyless signing from CI identity, verification before deployment, base images pinned by digest and updated by Renovate.

## Design

- Tags: `sha-<short commit>` on every main-branch build, `v<semver>` on release tags; `latest` is not used. Deployments and signatures use the digest.
- Platforms: cross-compilation in the builder stage on `$BUILDPLATFORM`; no emulation needed. `docker buildx imagetools inspect` confirms the runtime base publishes both platforms.
- Cache: `type=gha`, scoped per branch.
- Attestations: SBOM on; provenance in `mode=max` after confirming that no build argument is sensitive.
- Workflow: pinned third-party actions; `packages: write` and `id-token: write` only on the push job; the push job runs only on pushes to the main branch and on release tags, never on pull requests.
- Signing: keyless signing of the pushed digest; the deployment script verifies the signature and the expected workflow identity before pulling.

## Local verification by the build verifier

The handoff assigns: `docker buildx bake --print`; a two-platform build exported to an OCI layout with a task tag; a disposable run of the amd64 variant. The verifier confirms the engine context first, runs exactly those commands, and returns each with exit code, environment (builder driver, platforms, versions) and evidence. It removes its OCI output and task image, and pushes nothing.

## Level 2 request prepared, not performed

> Action: first push of `registry.example.invalid/team/service` with tags `sha-<commit>` and `v1.0.0` for linux/amd64 and linux/arm64, with SBOM and provenance attestations, followed by keyless signing of the resulting digest.
> Identity: the repository's CI OIDC identity; no stored password.
> Effect: creates the repository's first images and signatures; registry storage cost is small.
> Risk: a wrong tag is visible to consumers; mitigated by immutable tags.
> Rollback: consumers keep pinning the previous digest; the new tags can be deleted by the registry owner.
> Reason: required to complete the release criterion; local OCI evidence cannot prove registry acceptance of attestations.

## Report

Status IMPLEMENTATION_PREPARED_NOT_VERIFIED until the approved push runs and `docker buildx imagetools inspect` and signature verification are executed against the digest. The report ends with: "Container change is prepared, but completion is not verified."
