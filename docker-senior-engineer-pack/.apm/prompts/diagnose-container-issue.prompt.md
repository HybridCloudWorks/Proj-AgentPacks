---
description: "Diagnose a failing container, build, network, storage or disk problem from evidence"
agent: docker-senior-engineer
---

# Diagnose a container issue

## Inputs

The symptom and when it started, the command or Compose project, the image reference, the engine context and host type, recent changes, and any logs or `inspect` output already collected. Confirm the engine context before running anything.

## Workflow

Apply container-runtime-operations: collect narrow read-only evidence, classify the symptom, test hypotheses with a disposable reproduction at Level 1, and separate the confirmed cause from ruled-out ones. A diagnose-only request authorises analysis, not changes; fixes go through dockerfile-engineering or compose-environments when requested. Engine changes, prunes and work on shared or production hosts need Level 2 approval.

## Expected output

Timeline, evidence (redacted), root cause, the proposed or applied fix, verification, prevention steps, and a completion report under the `docker-senior-engineer-contract` instruction, with status ANALYSIS_ONLY when nothing was changed.
