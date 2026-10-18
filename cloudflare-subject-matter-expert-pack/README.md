# Cloudflare Subject Matter Expert agent pack

Version 1.0.0. Built to agent-pack-prompt v2.3. One user-facing primary agent, two optional specialists, eleven skills, four instruction files and nine prompts for designing, building, securing, migrating, operating and releasing work on Cloudflare.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source. `agents/`, `skills/` (three skills carry their own Python checkers under `scripts/`, three carry templates), `instructions/`, `prompts/`. Every vendor file is generated from here.
- `docs/`: approval, handoff, integration and permission contracts for humans, inventories, design decisions with assumptions, source traceability and maintenance notes.
- `compatibility/`: capability map, compatibility matrix, optional skills, vendor sources, and `tool-permissions.yml` (each agent's intended permissions).
- `hooks/`: helper scripts and a reviewed Copilot hook sample. Nothing here is installed as a native hook.
- `examples/`: worked workflows and a completion report; `examples/repository/` holds an optional repository instruction file for GitHub Copilot code review.
- `templates/`: completion report, specialist handoff and a baseline Wrangler configuration.
- `tests/`: offline unit tests, fixtures, and the capability, trigger, report-contract and generated skill-coverage files.
- `tooling/`: pack-specific helpers only (completion report validator and hook runner).

The repository's engine adds `AGENT-PACK-README.md` (artifact catalog) and `VALIDATION_REPORT.md` when it builds the pack.

## Install

Into a project with APM, for the clients that project uses:

```bash
apm install saulpatinojr/Proj-Agent_Packs/cloudflare-subject-matter-expert-pack --target claude,copilot,codex
```

APM generates `.claude/agents`, `.claude/rules`, `.claude/commands`, `.github/agents`, `.github/instructions`, `.github/prompts`, `.codex/agents`, `.kiro/agents`, `.kiro/steering`, `.gemini/commands`, and skills under `.agents/skills`, `.claude/skills` and `.kiro/skills`. Gemini CLI has no agents primitive in APM; it receives skills, commands and context only.

Into the user profile, so the pack works in every repository: use the Code Workflow installer. APM's `-g` install covers Claude Code fully but leaves Copilot agents at project scope.

The pack declares no MCP servers. If you use Cloudflare's remote MCP servers (documentation, bindings, builds, observability, API), connect them yourself; the agents use them when present and treat their write tools as approval-gated.

## Use

Invoke `cloudflare-subject-matter-expert` from the client's agent picker, or run one of the prompts (Copilot prompts, Claude commands, Gemini commands). The specialists `cloudflare-security-reviewer` (read-only review) and `cloudflare-migration-analyst` (offline rule accounting) are not user-invocable; the primary delegates to them. The `agent` field on prompts is honoured by Copilot and dropped by Claude.

Every write to a Cloudflare account is a Level 2 action: the agent prepares the change, snapshot and rollback, then asks for approval for the exact account, zone, resource and environment. Approval already given for that exact action is reused, not asked again.

## Permissions

Canonical agents declare no `tools`; see `docs/TOOL_PERMISSION_MATRIX.md` and `compatibility/tool-permissions.yml`. Written instructions guide behavior; real enforcement comes from the client's permission settings, the scope of the Cloudflare API token you configure, and your CI protections.

## Build and validate

From the repository root:

```bash
python tooling/skill_coverage.py cloudflare-subject-matter-expert-pack                  # regenerate tests/skill-coverage.yml
python tooling/validate_pack.py cloudflare-subject-matter-expert-pack --install-check   # shared validator
python tooling/build_pack.py cloudflare-subject-matter-expert-pack                      # shared builder
```

The pack's own tests run offline with `python -m unittest discover -s tests` from the pack folder; the validator runs them too. Build outputs are not committed.
