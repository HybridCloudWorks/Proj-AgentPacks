---
description: "Review a Dockerfile, Compose, Bake or CI image-build change"
agent: docker-senior-engineer
---

# Review a container change

## Inputs

The exact base and head, or the diff; the repository's container policies; the consumers of changed stages, services and tags; acceptance criteria if any.

## Workflow

Apply docker-change-review with its checklist, and the domain skills for the files that changed. Run only static checks that do not execute the change. Delegate the security portion to container-security-reviewer, or execution evidence in an isolated, credential-free environment to container-build-verifier, when independence adds value. Keep the review read-only and do not post, approve or merge.

## Expected output

Findings ordered by severity with location, evidence, impact, recommended change and blocking flag; consumer contract changes; checks run and not run; the verdict and status under the `docker-senior-engineer-contract` instruction (CHANGES_REQUIRED when findings block readiness, otherwise ANALYSIS_ONLY).
