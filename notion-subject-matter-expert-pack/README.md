# Notion Subject Matter Expert agent pack

Version 1.0.0. Built to agent-pack-prompt v2.3. One user-facing primary agent, one optional read-only specialist, seven skills, two instruction files and eight prompts for Notion workspace design, databases, knowledge capture, meetings, research, spec-to-task delivery and API integration.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source, with `agents/`, `skills/`, `instructions/` and `prompts/`. Every vendor file is generated from here. Each skill folder carries its own reference file, so a skill works when installed alone.
- `docs/`: role definition, approval, handoff, integration and permission contracts, inventories, design decisions, source traceability and maintenance notes.
- `compatibility/`: capability map, compatibility matrix, optional skills, vendor sources, and `tool-permissions.yml` (each agent's intended permissions).
- `hooks/`: manual helper scripts and a reviewed Claude Code hook sample. Nothing here is installed as a native hook.
- `examples/`: worked workflows and a completion report.
- `templates/`: reviewer handoff, completion report and workspace change request.
- `tests/`: report contract, capability coverage, trigger cases, generated skill coverage, fixtures and offline unit tests.
- `tooling/`: the pack's own helpers, `notion_draft_check.py` (pre-publication and hook check) and `completion_contract.py` (completion report check).

## Before you use it

Connect Notion in your client, usually by adding a Notion MCP server and signing in. The pack does not configure one. Without a connection the agent still designs, reviews and drafts, and labels its output as not written to Notion.

## Install

Into a project with APM, for the clients that project uses:

```bash
apm install saulpatinojr/Proj-Agent_Packs/notion-subject-matter-expert-pack --target claude,copilot,codex
```

APM generates `.claude/agents`, `.claude/rules`, `.claude/commands`, `.github/agents`, `.github/instructions`, `.github/prompts`, `.codex/agents`, `.kiro/agents`, `.kiro/steering`, `.gemini/commands`, and skills under `.agents/skills`, `.claude/skills` and `.kiro/skills`. Gemini CLI has no agents primitive in APM; it receives skills, commands and context only.

Into the user profile, so the pack works in every repository: use the Code Workflow installer. APM's `-g` install covers Claude Code fully but leaves Copilot agents at project scope.

## Use

Invoke `notion-subject-matter-expert` from the client's agent picker, or use a prompt: design-workspace, audit-workspace, design-database, capture-knowledge, prepare-meeting, research-and-document, plan-spec-implementation, connect-notion-integration. The `notion-governance-reviewer` specialist is not user-invocable; the primary delegates to it. Prompts appear as Copilot prompts, Claude commands and Gemini commands; the `agent` field on prompts is honoured by Copilot and dropped by Claude.

## Permissions

Canonical agents declare no `tools`. See `docs/TOOL_PERMISSION_MATRIX.md` and `compatibility/tool-permissions.yml`. APM-generated agents inherit the host's tools, including any Notion write tools, so the reviewer's read-only boundary is behavioural unless your installer or host restricts its tools. The approval levels are in `docs/APPROVAL_MATRIX.md` and, for the model, in the always-on contract instruction.

## Check drafts and reports by hand

```bash
python tooling/notion_draft_check.py draft.md --audience external --kind agenda
python tooling/completion_contract.py report.json
python -m unittest discover -s tests
```

## Build and validate

```bash
python ../tooling/validate_pack.py . --install-check   # shared validator; writes the validation report
python ../tooling/build_pack.py .                      # shared builder; writes the archives and artifact catalog
```

Archives, the artifact catalog and the validation report are build outputs and are not committed with the source.
