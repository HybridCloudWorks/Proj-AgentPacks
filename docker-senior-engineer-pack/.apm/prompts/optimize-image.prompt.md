---
description: "Reduce container image size and build time with measured before-and-after evidence"
agent: docker-senior-engineer
---

# Optimise an image

## Inputs

The image or Dockerfile, how it is built (context, target, arguments, CI cache), the consumers that must keep working, and the goal: smaller image, faster cold build, faster rebuild, or all three. Use an existing baseline if one is supplied; otherwise measure one first.

## Workflow

Measure the baseline (size, largest layers from `docker history`, cold build, rebuild after a source change). Apply dockerfile-engineering for base, stages, layer order, cache mounts and context, and image-build-and-supply-chain for CI cache export. Change one thing at a time where the effect is uncertain, and keep the runtime contract unless the user accepts a change.

## Expected output

Before-and-after numbers from the same environment and commands, the changes that produced them, trade-offs (debuggability, compatibility, cache scope) and a completion report under the `docker-senior-engineer-contract` instruction. Never report an improvement that was not measured.
