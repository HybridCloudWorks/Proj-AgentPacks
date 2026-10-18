# Handoff contract

The binding text is the always-on `docker-senior-engineer-contract` instruction; `templates/handoff.md` is a fill-in form for people who want to see a handoff written out.

## Parent request

Carry the original goal and current task; scope and non-goals; files in scope (Dockerfiles, ignore files, Compose, Bake, CI build steps); build context path and target stage; target platforms; observed engine, Buildx and Compose versions and the engine context; base image and registry policy; acceptance criteria; for the build verifier, the exact commands or command classes it may run, the tag prefix or Compose project name and the cleanup expected; prohibited actions; evidence already collected; approval state; requested output. Share only sanitised context: never registry credentials, tokens or secret values. No private parent context is assumed to be inherited.

## Specialist return

- container-security-reviewer: findings with severity, confidence, location, evidence, impact, recommended change and blocking flag; the negative checks that would prove each fix; evidence it could not obtain and the command that would settle it; residual risk. It never edits, runs commands or contacts the network.
- container-build-verifier: every check with command, exit code, status, environment and evidence; resources created and whether they were removed; skipped checks with reasons; observations such as cache misses, warnings, image size and runtime user. It never edits files, fixes failures, prunes, logs in, pushes or signs.

## Reconciliation

The primary resolves conflicting evidence against the current request, the acceptance criteria and the actual files and build results; reviews the final diff; and owns the completion report. A specialist cannot approve its own scope expansion; it reports the need. If delegation is unavailable, the primary performs the same narrow task with the same skills and states that the review or verification was not independent.
