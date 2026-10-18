---
description: "Harden a container image and its runtime settings, and triage its vulnerabilities"
agent: docker-senior-engineer
---

# Harden a container

## Inputs

The Dockerfile, Compose file or run configuration, what the container handles and can reach, existing scanner output and policy, and whether the task is review-only or includes remediation.

## Workflow

Apply container-security-hardening: image contents and secrets, user and file ownership, capabilities and security profiles, read-only root filesystem, exposure and limits, then vulnerability triage with the repository's scanner if one is installed. Use the container-security-reviewer specialist for an independent review when it adds value. Remediate only when asked, then re-run the negative checks and the same scan.

## Expected output

Located findings with severity and blocking flag, the remediation patch if requested, negative checks with results, residual and accepted risks with owners, and a completion report under the `docker-senior-engineer-contract` instruction. Never include secret values; review-only work stays read-only.
