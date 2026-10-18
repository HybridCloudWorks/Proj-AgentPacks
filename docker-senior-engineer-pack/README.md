# Docker Senior Engineer agent pack

Version 1.0.0. Built to agent-pack-prompt v2.3. One user-facing primary agent, two optional specialists, six skills, four instruction files and seven prompts for container image, Compose, build and supply-chain, and runtime engineering on Docker.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source, with `.apm/agents`, `.apm/skills`, `.apm/instructions` and `.apm/prompts`. Every vendor file is generated from here.
- `docs/`: agent, skill and prompt inventories; approval, handoff, integration and permission contracts; design decisions; source traceability; maintenance.
- `compatibility/`: capability map, compatibility matrix, optional skills, vendor sources, and `tool-permissions.yml` (each agent's intended permissions).
- `hooks/`: helper scripts and a reviewed Copilot hook sample. Nothing here is installed as a native hook.
- `examples/`: worked workflows, a completion report, and an optional repository-level file for Copilot code review.
- `templates/`: completion report, specialist handoff, image runtime contract.
- `tests/`: capability coverage, trigger cases, the report contract, generated skill coverage, fixtures and unit tests for the pack's tooling.
- `tooling/`: pack-specific helpers only: a static Dockerfile and Compose checker, a completion report validator and the hook runner. Standard library only.
- `AGENT-PACK-README.md` (artifact catalog) and `VALIDATION_REPORT.md` are written by the repository's shared build and validation tooling, not by hand.

## Install

Into a project with APM, for the clients that project uses:

```bash
apm install saulpatinojr/Proj-Agent_Packs/docker-senior-engineer-pack --target claude,copilot,codex
```

Per client, the result is: Claude Code agents, rules, commands and skills under `.claude/`; Copilot agents, instructions and prompts under `.github/`; Codex agents under `.codex/agents`; Kiro agents, steering and skills under `.kiro/`; Gemini CLI commands under `.gemini/commands`; and shared skills under `.agents/skills`. APM gives Gemini CLI no agents, so there the workflows arrive as skills, commands and context.

For a user-profile install that applies in every repository, use the Code Workflow installer: `apm install -g` is complete for Claude Code, but Copilot agents still land at project scope.

## Use

Invoke `docker-senior-engineer` from the client's agent picker. The specialists (`container-security-reviewer`, `container-build-verifier`) are not user-invocable; the primary delegates to them. Prompts appear as Copilot prompts, Claude Code commands and Gemini CLI commands: `containerize-application`, `optimize-image`, `harden-container`, `build-compose-environment`, `diagnose-container-issue`, `set-up-image-pipeline`, `review-container-change`. The `agent` field on prompts is honoured by Copilot and dropped by Claude Code.

The always-on `docker-senior-engineer-contract` instruction carries the approval levels, handoff rules and completion report format, so the pack depends on nothing at a repository root.

## Permissions

Canonical agents declare no `tools`; see `docs/TOOL_PERMISSION_MATRIX.md` and `compatibility/tool-permissions.yml`. Written instructions are guidance; real limits come from the host's permission settings and sandbox, who can reach the Docker engine, and registry access controls.

## Build and validate

From the repository root:

```bash
python tooling/skill_coverage.py docker-senior-engineer-pack                  # regenerate tests/skill-coverage.yml
python tooling/validate_pack.py docker-senior-engineer-pack --install-check   # shared validator; writes VALIDATION_REPORT.md
```

Release archives are build outputs of the shared build tooling and are not committed.
