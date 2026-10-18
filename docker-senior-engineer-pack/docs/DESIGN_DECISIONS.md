# Design decisions

Pack 1.0.0, generated 2026-10-18 to agent-pack-prompt v2.3 without the ability to ask questions. Assumptions are marked as such.

## Role and scope

1. Assumption: a Docker Senior Engineer owns the container image, its build, its Compose definition and its behaviour on a Docker engine. Kubernetes and other orchestrator manifests, cloud container services and the overall CI/CD pipeline are non-goals; the agent states the boundary and hands over the image runtime contract. This matches the boundary in the reference material and keeps the pack from half-answering cluster questions.
2. Assumption: Linux containers on Docker Engine 23.0 or later (BuildKit default), Buildx and Compose v2 are the baseline. Older releases, Podman and Buildah are handled by feature detection. Windows containers are out of scope because their base images, isolation modes and tooling differ enough to need their own guidance.
3. Assumption: no Docker CLI, scanner, registry or CI access exists until discovered. Every skill has a static-only path and the fallback sentence for unverified work.

## Agents

4. One user-facing primary, `docker-senior-engineer`, can do every workflow alone.
5. Two specialists, justified under section 3 of the prompt: `container-security-reviewer` adds independence with narrower permissions (read only); `container-build-verifier` adds execution evidence produced by someone other than the author and keeps long build and scan output out of the primary's context (read and shell). No specialist was created for Compose, CI or diagnosis, because those need the same permissions and context as the primary.
6. The verifier has a shell but must not edit. A shell can write files, so the agent body, tool-permission file and capability map all say the no-edit rule is behavioural unless the host sandboxes the profile, rather than presenting it as enforced.
7. Agents declare no `tools` field. Intents live in `compatibility/tool-permissions.yml`; vendor translations in `compatibility/capability-map.yml`.
8. The primary has a `web` intent so it can confirm current documentation, base image tags and platform manifests. Gemini CLI's verified built-in tools include no web tool, so that intent has no Gemini translation; recorded rather than invented.
9. Specialists set `include-custom-instructions: true`, a documented Copilot field, so Copilot subagents receive the installed contract instruction. APM copies it verbatim to Claude Code, where it is an unused key; Codex and Kiro drop it. Each specialist body also restates its core prohibitions so it degrades safely if instructions are not delivered.
10. The Claude Code `skills` preload field is not used: APM copies frontmatter verbatim to Copilot, where `skills` is not a documented agent field. Agents name their skills in the body instead.

## Skills

11. Six skills, chosen from the role: dockerfile-engineering, container-security-hardening, compose-environments, image-build-and-supply-chain, container-runtime-operations and docker-change-review. Thinner splits (image size, multi-platform, scanning, logging) were folded in because they share discovery and validation steps.
12. Two skills carry supporting files in their own folders (`dockerfile-patterns.md`, `review-checklist.md`) so they stay useful when installed alone and installed content references only installed content.
13. Base image versions in `dockerfile-patterns.md` are labelled examples. Assumption: users replace them with the versions their repositories declare.

## Contract and evidence

14. The always-on `docker-senior-engineer-contract` instruction carries the approval levels, handoff rules and completion report. Approval levels are written in Docker terms: engine context first; local builds, disposable runs and task-scoped Compose projects at Level 1; login, push, sign, prune, engine changes, privileged runs and deployments at Level 2.
15. The completion report adds Docker-specific fields (image impact, runtime contract impact, supply chain impact, platform compatibility), an `environment` field on every check, and evidence levels (static, local build, local runtime, scan, live), because a Docker result depends on the engine, builder and platform and local evidence must never be presented as registry or production proof.
16. The status vocabulary (COMPLETE_VERIFIED and the others) and severity scale are framework-level conventions and are kept. The fallback sentence is role-specific: "Container change is prepared, but completion is not verified."

## Hooks and tooling

17. No native hooks ship (APM would copy commands without their scripts). Helpers and a reviewed Copilot sample live in `hooks/`. Only a Copilot sample ships because the client-locations record does not document other clients' hook output formats; the installer wires the rest.
18. `tooling/container_lint.py` is a deliberately small, heuristic, read-only checker so hooks can give a bounded preflight without running Docker. It never echoes secret values. It complements `docker build --check`, hadolint and `docker compose config`, and says so in its output.
19. The completion report path for the optional stop hook is `.docker-engineering/completion.json` in the working repository, independent of any one code host.
20. The shell helpers do not use `timeout`, which stock macOS lacks; hook wall-clock limits come from the host's `timeoutSec`.

## Delivery

21. Following the brief: no AGENT-PACK-README.md, VALIDATION_REPORT.md, `dist/` or archives are written by hand; the shared engine produces them. No copy of the shared validator or builder is placed in the pack.
22. `examples/repository/copilot-instructions.md` is an optional extra for GitHub Copilot code review on GitHub.com, self-contained and never a prerequisite.
23. Reference corrections (obsolete Compose `version` key, the retired `docker-compose` binary, deprecated npm flags, end-of-life base images, an incomplete secret example) are listed in SOURCE_TRACEABILITY.md.
