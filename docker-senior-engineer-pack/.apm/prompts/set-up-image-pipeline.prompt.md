---
description: "Set up multi-platform image builds with caching, tags, SBOM, provenance and signing"
agent: docker-senior-engineer
---

# Set up an image pipeline

## Inputs

The images to build, target platforms, the CI system and existing workflows, registries and the identity allowed to push, the tag scheme, and policy for SBOM, provenance, signing, scanning and base image updates.

## Workflow

Apply image-build-and-supply-chain: define tags and labels, choose cross-compilation, emulation or native builders, configure cache export, write Bake or workflow steps, add attestations and digest-based signing, restrict push permissions, and configure base image update automation. Validate statically and with local multi-platform builds. Prepare every login, push, sign, promote and registry setting as a Level 2 request instead of performing it.

## Expected output

Workflow and Bake changes, the tag and platform matrix, cache and attestation settings, a publish plan with each Level 2 step, consumer verification commands, and a completion report under the `docker-senior-engineer-contract` instruction. Local builds do not prove registry or CI behaviour.
