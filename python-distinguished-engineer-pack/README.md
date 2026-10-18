# Python Distinguished Engineer agent pack

Version 2.3.0. Built to agent-pack-prompt v2. One user-facing primary agent, four optional specialists, eighteen Skills, five instruction files and ten prompts for enterprise Python and agentic engineering.

Shared with the TypeScript Distinguished Engineer pack: the skills agentic-workflow-design, playwright-validation, secure-agent-engineering and agent-evaluation, the agent-evaluation-engineer specialist, the agentic-security instruction and the evaluate-agent and validate-web-flow prompts. Both packs ship identical copies, so installing both leaves one consistent version, and either pack can handle code in either language. Each shared skill picks the language from the code and keeps a separate Python and TypeScript reference.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source. `agents/`, `skills/`, `instructions/`, `prompts/`. Every vendor file is generated from here.
- `docs/`: handoff, approval, integration and permission contracts, plus inventories.
- `compatibility/`: capability map, vendor sources, optional skills, and `tool-permissions.yml` (each agent's intended permissions).
- `hooks/`: helper scripts and a reviewed Copilot hook sample. Nothing here is installed as a native hook.
- `examples/`, `templates/`, `tests/`, `tooling/`.
- `AGENT-PACK-README.md`: the artifact catalog. `VALIDATION_REPORT.md`: what was checked and what was not.

## Install

Into a project with APM, for the clients that project uses:

```bash
apm install saulpatinojr/Proj-Agent_Packs/python-distinguished-engineer-pack --target claude,copilot,codex
```

APM generates `.claude/agents`, `.claude/rules`, `.claude/commands`, `.github/agents`, `.github/instructions`, `.github/prompts`, `.codex/agents`, `.kiro/agents`, `.kiro/steering`, `.gemini/commands`, and skills under `.agents/skills`, `.claude/skills`, `.kiro/skills`. Gemini CLI has no agents primitive; it receives skills, commands and context only.

Into the user profile, so the pack works in every repository: use the Code Workflow installer. APM's `-g` install covers Claude Code fully but leaves Copilot agents at project scope.

## Use

Invoke `python-distinguished-engineer` from the client's agent picker. The four specialists (`python-security-reviewer`, `python-test-engineer`, `python-performance-engineer`, `agent-evaluation-engineer`) are not user-invocable; the primary delegates to them. Prompts appear as Copilot prompts, Claude commands and Gemini commands. The `agent` field on prompts is honoured by Copilot and dropped by Claude.

## Permissions

Canonical agents declare no `tools`; see `docs/TOOL_PERMISSION_MATRIX.md` and `compatibility/tool-permissions.yml`.

## Build and validate

```bash
python ../tooling/validate_pack.py . --install-check   # shared validator; writes VALIDATION_REPORT.md
python ../tooling/build_pack.py .                      # shared builder; writes dist/ and AGENT-PACK-README.md
```

`dist/` is a build output and is not committed.
