# Prompt inventory

| Prompt | Skills | Expected output |
|---|---|---|
| containerize-application.prompt.md | dockerfile-engineering, container-security-hardening, compose-environments (optional) | Dockerfile and ignore file, runtime contract, build and run commands, measurements, completion report. |
| optimize-image.prompt.md | dockerfile-engineering, image-build-and-supply-chain | Before-and-after size and build-time numbers from the same environment, the changes that produced them, trade-offs. |
| harden-container.prompt.md | container-security-hardening | Located findings, remediation patch if requested, negative checks, residual and accepted risks. |
| build-compose-environment.prompt.md | compose-environments | Compose changes, commands per environment, readiness, exposure and data notes, migration notes. |
| diagnose-container-issue.prompt.md | container-runtime-operations | Timeline, redacted evidence, root cause, fix or proposal, verification, prevention; ANALYSIS_ONLY when nothing changed. |
| set-up-image-pipeline.prompt.md | image-build-and-supply-chain | Workflow and Bake changes, tag and platform matrix, cache and attestation settings, Level 2 publish plan, verification commands. |
| review-container-change.prompt.md | docker-change-review plus the domain skills | Severity-ordered findings, consumer contract changes, checks run and not run, verdict and status. |

All prompts set `agent: docker-senior-engineer`. APM installs them as Copilot prompt files, Claude Code commands (the `agent` key is dropped) and Gemini CLI commands. Codex and Kiro receive no prompts; their users invoke the primary agent directly, and the skills carry the same workflows.
