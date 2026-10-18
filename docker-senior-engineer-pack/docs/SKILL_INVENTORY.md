# Skill inventory

| Skill | Activation | Supporting files | Workflow prompt | Used by |
|---|---|---|---|---|
| dockerfile-engineering | An application needs containerising, an image is too large or slow to build, a Dockerfile changes, or caching, stages, build arguments or entrypoints are in question. | `dockerfile-patterns.md` | containerize-application.prompt.md, optimize-image.prompt.md | primary, build verifier |
| container-security-hardening | Production readiness, scanner findings, secrets possibly in layers, requests for extra privileges, or a container security review. | none | harden-container.prompt.md | primary, security reviewer |
| compose-environments | A Compose file changes, services start out of order or never become healthy, containers cannot reach each other, configuration or secrets need structure, or a development loop is needed. | none | build-compose-environment.prompt.md | primary, build verifier |
| image-build-and-supply-chain | Multi-architecture builds, slow or uncached CI builds, tag or registry design, SBOM, provenance or signing, base image pinning and update automation. | none | set-up-image-pipeline.prompt.md | primary, build verifier, security reviewer |
| container-runtime-operations | Unexpected exits, restarts or kills, failing builds, unreachable services, volume permission errors, full disks, environment differences, engine settings. | none | diagnose-container-issue.prompt.md | primary, build verifier |
| docker-change-review | A pull request, branch, staged diff or set of container files needs review, audit or a second opinion. | `review-checklist.md` | review-container-change.prompt.md | primary, security reviewer |

## Why six

The role divides along the artefacts a Docker engineer owns and the distinct ways of working on them: authoring the image (Dockerfile), constraining it (security), composing services (Compose), building and publishing it (supply chain), operating and diagnosing it (runtime), and reviewing changes to all of these. Narrower splits (image size, multi-platform, scanning, log rotation as separate skills) were rejected because each would be thin and would repeat the same discovery and validation steps.

Each SKILL.md states purpose and activation, scope and exclusions, inputs, dependencies and tools, workflow, output, validation, failure handling and escalation, permissions and guardrails, and its connection to the pack. Each works when installed alone; supporting files sit in the skill's own folder. These are operational instructions, not a promise that a model always follows them. `tests/skill-coverage.yml` is generated from the SKILL.md files by the repository's `tooling/skill_coverage.py`.
