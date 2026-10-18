# docker-senior-engineer 1.0.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| container-build-verifier.agent.md | Canonical agent: Runs assigned container builds, static checks, scans and disposable smoke tests in isolation and returns exact commands, environments, exit codes and evidence; never edits files, logs in or publishes. | .apm/agents/container-build-verifier.agent.md |
| container-security-reviewer.agent.md | Canonical agent: Read-only reviewer of container image, Dockerfile, Compose, engine and image supply-chain security; returns located, evidence-backed findings without editing files or running commands. | .apm/agents/container-security-reviewer.agent.md |
| docker-senior-engineer.agent.md | Canonical agent: Senior Docker engineer for container images, Dockerfiles, Compose environments, multi-platform builds and image supply chain, runtime diagnosis and container change review, delivered with build and runtime evidence. | .apm/agents/docker-senior-engineer.agent.md |
| compose.instructions.md | Canonical instruction: Docker Compose file changes: Compose Specification semantics, health-gated startup, scoped networks and ports, file-based secrets, task-scoped validation. | .apm/instructions/compose.instructions.md |
| docker-senior-engineer-contract.instructions.md | Canonical instruction: Approval levels, specialist handoff rules and the completion report format for the Docker Senior Engineer pack. Always on; every agent, skill and prompt in the pack relies on it. | .apm/instructions/docker-senior-engineer-contract.instructions.md |
| dockerfile.instructions.md | Canonical instruction: Dockerfile, Containerfile and ignore-file changes: pinned bases, multi-stage graphs, cache-friendly layers, no secrets in layers, non-root exec-form runtime. | .apm/instructions/dockerfile.instructions.md |
| image-build.instructions.md | Canonical instruction: Bake files and CI steps that build, cache, attest, sign or push container images: immutable tags, safe cache export, digest-based signing, least-privilege publishing. | .apm/instructions/image-build.instructions.md |
| build-compose-environment.prompt.md | Canonical prompt: Create or fix a Docker Compose environment for development, CI or a single host | .apm/prompts/build-compose-environment.prompt.md |
| containerize-application.prompt.md | Canonical prompt: Containerise an application with a production-ready Dockerfile and ignore file | .apm/prompts/containerize-application.prompt.md |
| diagnose-container-issue.prompt.md | Canonical prompt: Diagnose a failing container, build, network, storage or disk problem from evidence | .apm/prompts/diagnose-container-issue.prompt.md |
| harden-container.prompt.md | Canonical prompt: Harden a container image and its runtime settings, and triage its vulnerabilities | .apm/prompts/harden-container.prompt.md |
| optimize-image.prompt.md | Canonical prompt: Reduce container image size and build time with measured before-and-after evidence | .apm/prompts/optimize-image.prompt.md |
| review-container-change.prompt.md | Canonical prompt: Review a Dockerfile, Compose, Bake or CI image-build change | .apm/prompts/review-container-change.prompt.md |
| set-up-image-pipeline.prompt.md | Canonical prompt: Set up multi-platform image builds with caching, tags, SBOM, provenance and signing | .apm/prompts/set-up-image-pipeline.prompt.md |
| SKILL.md | Canonical skill: Design, fix and validate Docker Compose applications for local development, CI test stacks and single-host deployments using the Compose Specification. Use when a compose file is created or changed, services start in the wrong order or never become healthy, containers cannot reach each other, environment or secret handling in Compose is unclear, or a development loop with watch, profiles or override files is needed. | .apm/skills/compose-environments/SKILL.md |
| SKILL.md | Canonical skill: Diagnose and operate containers and image builds on a Docker host, covering exit codes, restarts, OOM kills, signals, resource limits, logging, networking, storage, engine settings and disk usage. Use when a container exits, restarts or is killed unexpectedly, a build fails, a service cannot be reached, a volume cannot be written, logs or images fill the disk, behaviour differs between environments, or daemon and runtime settings need review. | .apm/skills/container-runtime-operations/SKILL.md |
| SKILL.md | Canonical skill: Harden container images and their runtime configuration, and assess privilege, secret, exposure and vulnerability risk with located evidence. Use when an image or container must be made production-ready, a scan reports vulnerabilities, a secret may have reached a layer, a container asks for extra privileges, or a security review of Dockerfiles, Compose files or engine settings is requested. | .apm/skills/container-security-hardening/SKILL.md |
| review-checklist.md | Canonical skill | .apm/skills/docker-change-review/review-checklist.md |
| SKILL.md | Canonical skill: Review Dockerfile, ignore-file, Compose, Bake and CI image-build changes with located, evidence-backed findings and a readiness verdict. Use when a pull request, branch, staged diff or set of container files needs a pre-merge review, an audit against container practice, or an independent second opinion on image security, reproducibility and runtime behaviour. | .apm/skills/docker-change-review/SKILL.md |
| dockerfile-patterns.md | Canonical skill | .apm/skills/dockerfile-engineering/dockerfile-patterns.md |
| SKILL.md | Canonical skill: Author, refactor and optimise Dockerfiles and Containerfiles with deliberate base images, multi-stage graphs, cache-efficient layers, tight build contexts and an explicit runtime contract. Use when an application needs containerising, an image is too large or slow to build, a Dockerfile is being changed, or build behaviour such as caching, stages, build arguments or entrypoints is in question. | .apm/skills/dockerfile-engineering/SKILL.md |
| SKILL.md | Canonical skill: Build, tag, cache, attest, sign and publish container images reproducibly across platforms with Buildx, Bake and CI, and keep base images and digests current. Use when images must be built for several architectures, CI image builds are slow or uncached, tags or registry layout are being designed, SBOM, provenance or signatures are required, or base image pinning and update automation is in scope. | .apm/skills/image-build-and-supply-chain/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| AGENT_INVENTORY.md | Pack contract or inventory | docs/AGENT_INVENTORY.md |
| APPROVAL_MATRIX.md | Pack contract or inventory | docs/APPROVAL_MATRIX.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| HANDOFF_CONTRACT.md | Pack contract or inventory | docs/HANDOFF_CONTRACT.md |
| INTEGRATION_CONTRACT.md | Pack contract or inventory | docs/INTEGRATION_CONTRACT.md |
| MAINTENANCE.md | Pack contract or inventory | docs/MAINTENANCE.md |
| PROMPT_INVENTORY.md | Pack contract or inventory | docs/PROMPT_INVENTORY.md |
| SKILL_INVENTORY.md | Pack contract or inventory | docs/SKILL_INVENTORY.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| TOOL_PERMISSION_MATRIX.md | Pack contract or inventory | docs/TOOL_PERMISSION_MATRIX.md |
| compose-local-stack-workflow.md | Worked example | examples/compose-local-stack-workflow.md |
| container-stop-timeout-diagnosis-workflow.md | Worked example | examples/container-stop-timeout-diagnosis-workflow.md |
| containerize-go-service-workflow.md | Worked example | examples/containerize-go-service-workflow.md |
| final-completion-report.md | Worked example | examples/final-completion-report.md |
| image-size-and-build-time-workflow.md | Worked example | examples/image-size-and-build-time-workflow.md |
| multi-platform-release-workflow.md | Worked example | examples/multi-platform-release-workflow.md |
| copilot-instructions.md | Optional repository-level file | examples/repository/copilot-instructions.md |
| security-review-workflow.md | Worked example | examples/security-review-workflow.md |
| lint-containers.ps1 | Hook helper script | hooks/lint-containers.ps1 |
| lint-containers.sh | Hook helper script | hooks/lint-containers.sh |
| post-docker-engineering.ps1 | Hook helper script | hooks/post-docker-engineering.ps1 |
| post-docker-engineering.sh | Hook helper script | hooks/post-docker-engineering.sh |
| pre-docker-engineering.ps1 | Hook helper script | hooks/pre-docker-engineering.ps1 |
| pre-docker-engineering.sh | Hook helper script | hooks/pre-docker-engineering.sh |
| README.md | Hook helper script | hooks/README.md |
| docker-engineering.copilot-hooks.sample.json | Reviewed hook sample, not installed | hooks/samples/docker-engineering.copilot-hooks.sample.json |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| completion-report.md | Reusable template | templates/completion-report.md |
| handoff.md | Reusable template | templates/handoff.md |
| image-runtime-contract.md | Reusable template | templates/image-runtime-contract.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| hardened.compose.yaml | Local test or recorded evidence | tests/fixtures/hardened.compose.yaml |
| hardened.Dockerfile | Local test or recorded evidence | tests/fixtures/hardened.Dockerfile |
| insecure.compose.yaml | Local test or recorded evidence | tests/fixtures/insecure.compose.yaml |
| insecure.Dockerfile | Local test or recorded evidence | tests/fixtures/insecure.Dockerfile |
| invalid-completion.json | Local test or recorded evidence | tests/fixtures/invalid-completion.json |
| valid-completion.json | Local test or recorded evidence | tests/fixtures/valid-completion.json |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| test_behavior.py | Local test or recorded evidence | tests/test_behavior.py |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| completion_contract.py | Pack-specific helper code | tooling/completion_contract.py |
| container_lint.py | Pack-specific helper code | tooling/container_lint.py |
| hook_runner.py | Pack-specific helper code | tooling/hook_runner.py |
| requirements.txt | Pack-specific helper code | tooling/requirements.txt |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-docker-senior-engineer.zip: 22 files generated by `apm install --target copilot`
- claude-docker-senior-engineer.zip: 22 files generated by `apm install --target claude`
- codex-docker-senior-engineer.zip: 11 files generated by `apm install --target codex`
- kiro-docker-senior-engineer.zip: 15 files generated by `apm install --target kiro`
- gemini-docker-senior-engineer.zip: 15 files generated by `apm install --target gemini`
- agent-skills-docker-senior-engineer.zip: 8 files generated by `apm install --target agent-skills`
- docker-senior-engineer-canonical.zip, docker-senior-engineer-prompt.zip, docker-senior-engineer-validation.zip, docker-senior-engineer-skills.zip, docker-senior-engineer-full-pack.zip, SHA256SUMS.txt
