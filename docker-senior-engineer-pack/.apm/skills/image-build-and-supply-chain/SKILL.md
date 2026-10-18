---
name: image-build-and-supply-chain
description: "Build, tag, cache, attest, sign and publish container images reproducibly across platforms with Buildx, Bake and CI, and keep base images and digests current. Use when images must be built for several architectures, CI image builds are slow or uncached, tags or registry layout are being designed, SBOM, provenance or signatures are required, or base image pinning and update automation is in scope."
---

# Image Build and Supply Chain

## Purpose and activation

Turn a working Dockerfile into images that can be rebuilt, traced to their source, verified by consumers and rolled back by digest. Activate for multi-architecture builds, slow or cache-less CI builds, tag and registry design, attestation and signing requirements, base image pinning and update automation, and the image-building steps of CI workflows.

## Scope and exclusions

In scope: Buildx builders and drivers, multi-platform strategies (cross-compilation, emulation, native nodes), cache backends, Bake files, tag strategy, OCI labels and annotations, SBOM and provenance attestations, signing and verification, promotion by digest, registry hygiene (immutability, retention, mirrors, pull limits), base image digest pinning and update automation, and the build, scan and push steps of CI workflows.

Out of scope, with the owner: the overall CI/CD pipeline design and deployment stages (platform owners); registry infrastructure provisioning (infrastructure-as-code owners); signing key and identity management (the PKI or security owners); Dockerfile contents (dockerfile-engineering).

## Inputs

- CI workflows and scripts that build images, Bake files, and current builder setup (`docker buildx ls`).
- Registries and repositories, the existing tag scheme, the cache configuration, and access model (who may push, with which identity).
- The platforms consumers run on (x86-64 servers, arm64 cloud instances, Apple silicon laptops) and whether every base image publishes them.
- Organisation policy for SBOM, provenance level, signing tool and verification point, vulnerability gates and base image sources.

## Dependencies and tools

- Read, search and edit for workflow and Bake changes.
- Buildx (`docker buildx build`, `bake`, `imagetools`) at Level 1 for local builds; registry pushes, logins and signing are Level 2.
- Optional, when installed and approved: cosign or Notation for signing and verification, a scanner, actionlint or the CI system's linter, Renovate or Dependabot configuration for updates.
- Without a CLI or registry access, the work is static and the report says so.

## Workflow

1. Discover the current build path end to end: trigger, builder, platforms, cache, tags, scan, push, sign and the consumer that pulls the image. Note where credentials enter and which events can push.
2. Define the image identity. Name repositories consistently. Give every build an immutable tag (for example the commit) and release builds a version tag; treat `latest` and branch tags as conveniences only. Consumers deploy, sign and promote by digest. Set OCI labels or annotations for source, revision, version, licences, and base image name and digest.
3. Choose a multi-platform strategy. Cross-compile in builder stages running on `$BUILDPLATFORM` with `TARGETOS`/`TARGETARCH` for compiled languages; use QEMU emulation only where cross-compilation is impossible, accepting slower and occasionally fragile builds; use native builder nodes or runners for heavy workloads. Check that each base image publishes every target platform with `docker buildx imagetools inspect <base>`. A multi-platform result must go to a registry or an OCI layout, or into a containerd-backed image store, which recent installations use by default (`docker info` shows it); the classic store cannot load it. Installing binfmt emulators on a shared host is Level 2.
4. Cache. CI runners are usually ephemeral, so export cache: `type=gha` on GitHub Actions, `type=registry,ref=<repo>:buildcache` elsewhere, scoped per branch or target to avoid churn. Inline cache covers only the final stage. `mode=max` exports every intermediate stage: no stage may ever contain a secret, and the cache repository needs the same access controls as the image. Check that early `ARG` values such as build dates or revisions do not invalidate the cache on every run.
5. Bake when there are several images, targets or platform sets: variables for registry and tag, groups, `inherits`, and `matrix`. Render with `docker buildx bake --print` before running.
6. Attestations. Request an SBOM (`--sbom=true`) and provenance (`--provenance=mode=min` or `mode=max`). Buildx adds minimal provenance by default for images it exports to a registry. Maximum mode records build-argument values, so it is only safe when no argument is sensitive. Attestations are stored alongside the image index, so they need a registry or an OCI export and a registry that accepts them. Inspect them with `docker buildx imagetools inspect <ref> --format '{{ json .SBOM }}'` or `'{{ json .Provenance }}'`.
7. Signing. Sign the digest, never a tag, with the tool and identity the organisation uses: keyless Sigstore signing from CI identity, or keys held in a KMS, or Notation. Signing only matters if a consumer verifies: name the verification point (admission policy, deployment script, pull-time policy). Docker Content Trust is a legacy mechanism; do not introduce it for new work.
8. Base image currency. Pin `FROM name:tag@sha256:...` and let Renovate or Dependabot propose digest and version updates with tests, rebuild on a schedule so base fixes reach images without code changes, and track base image end-of-life dates.
9. CI hygiene. Pin third-party actions or templates to an immutable reference. Grant registry write permission only to the job that pushes. Never push, or expose registry credentials, on builds of untrusted pull requests, since their `RUN` steps are untrusted code. Prefer short-lived identity-based registry credentials to stored passwords. Scan before promotion, and promote by copying the scanned digest (`docker buildx imagetools create`) rather than rebuilding.
10. Registry hygiene. Recommend tag immutability where the registry supports it, retention policies for untagged and old images, authenticated pulls and a mirror or pull-through cache where public registry pull limits bite. Changing registry settings is Level 2.

## Output

- Workflow, Bake and Dockerfile changes, with the tag scheme, platforms, cache configuration and attestation settings stated.
- A publish plan listing each Level 2 step (login, push, sign, promote, registry settings) with its target and identity, ready for approval.
- Verification commands for consumers: digest inspection, attestation inspection and signature verification.

## Validation

- Static: `docker buildx bake --print`, the CI system's linter, and `docker build --check`.
- Local build: build every target platform at Level 1, exporting to an OCI layout or the containerd store, or one platform at a time; confirm the second build hits the cache.
- Live, only after approved pushes: `docker buildx imagetools inspect` shows every platform and the attestations; signature verification passes against the digest with the expected identity.
- Record the evidence level for each criterion; local evidence does not prove registry or CI behaviour.

## Failure handling and escalation

- A base image lacks a platform: choose another base, build that platform from a different base with a recorded decision, or drop the platform with consumer agreement.
- Emulated builds crash or time out: move to cross-compilation or native builders.
- Constant cache misses: check cache scope and key, changing build arguments early in the Dockerfile, and files in the context that change every run.
- A registry rejects attestations or the image index: confirm OCI support; disabling attestations requires a recorded decision.
- Pull rate limits: authenticate pulls or use a mirror; never embed credentials in a Dockerfile.

## Permissions and guardrails

- Login, push, retag, promote, delete, sign, builder creation on shared hosts, cloud builders, emulator installation and registry settings are Level 2.
- Never print or log registry tokens; never sign by tag; never use maximum-mode provenance with sensitive arguments; never disable signature or digest verification to unblock a release.

## Connection to the pack

The docker-senior-engineer agent applies this skill through the optional `set-up-image-pipeline` prompt; the container-build-verifier specialist runs its local build checks; docker-change-review uses it for CI and Bake diffs. The skill is complete when installed alone; with the full pack, the `docker-senior-engineer-contract` instruction supplies the approval levels, handoff rules and completion report.
