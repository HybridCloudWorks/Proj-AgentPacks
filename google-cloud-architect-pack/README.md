# Google Cloud Architect agent pack

Version 1.1.0. Built to agent-pack-prompt version 2.3. One user-facing primary agent, two optional specialists, twenty skills, three instruction files and ten prompts for Google Cloud solution and platform architecture.

Three of the skills, drawio-core-generation, drawio-render-export-and-review and diagram-validation-and-evidence, are shared: the AWS and Azure architect and designer packs ship identical copies, so installing several of these packs leaves one consistent version. They draw Google Cloud, AWS and Azure diagrams, alone or together, with each provider's current icons.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source (`agents/`, `skills/`, `instructions/`, `prompts/`). Every vendor file is generated from here. Skills that need a helper carry it in their own `scripts/` folder, and the design and decision skills carry their templates.
- `docs/`: agent, skill and prompt inventories; approval, handoff, integration and tool-permission contracts; design decisions and assumptions; source traceability; maintenance.
- `compatibility/`: capability map, compatibility matrix, vendor sources, optional skills, and `tool-permissions.yml` (each agent's intended permissions).
- `hooks/`: manual helper scripts and a reviewed Copilot-format sample. Nothing here is installed as a native hook.
- `examples/`: worked design, landing zone, review, IaC, migration and DR examples, a completion report, and an optional repository file for Copilot code review.
- `templates/`: completion report, specialist handoff, requirements questionnaire and an IP plan example.
- `tests/`: capability coverage, trigger and negative cases, the report contract, fixtures, the generated skill coverage and `test_behavior.py`.
- `tooling/`: `completion_contract.py`, the pack-specific completion report validator.

The artifact catalog (`AGENT-PACK-README.md`), `VALIDATION_REPORT.md` and the distribution archives are produced by the repository's build engine and are not kept in the source.

## Install

Into a project with APM, for the clients that project uses:

```bash
apm install saulpatinojr/Proj-Agent_Packs/google-cloud-architect-pack --target claude,copilot,codex
```

The install writes agents to `.claude/agents`, `.github/agents`, `.codex/agents` and `.kiro/agents`; instructions to `.claude/rules`, `.github/instructions` and `.kiro/steering`; prompts to `.claude/commands`, `.github/prompts` and `.gemini/commands`; and skills to `.agents/skills`, `.claude/skills` and `.kiro/skills`. Gemini CLI gets skills, commands and context but no agents, because APM has no agent type for it.

To use the pack in every repository, install it into your user profile with the Code Workflow installer. An APM global install (`-g`) is complete only for Claude Code: Copilot agents stay at project level, and Codex gets no instructions, which is why each agent body repeats the essential approval rules.

## Use

Pick `google-cloud-architect` in your client's agent list and describe the workload, review or plan you need. You cannot pick the two specialists (`gcp-security-reviewer`, `gcp-estate-inspector`) yourself; the primary calls them when they help. The prompts show up as prompt files in Copilot and as commands in Claude Code and Gemini CLI; only Copilot uses their `agent` field.

For live discovery, give the agent the exact organization, folder or project and a read-only identity to impersonate. Anything that changes a cloud environment, IAM, APIs, billing or data, or that bills (queries, inference), needs your explicit approval for that exact action.

## Permissions

The agent files list no tools; their intended permissions are in `compatibility/tool-permissions.yml` and explained in `docs/TOOL_PERMISSION_MATRIX.md`. The pack's instructions guide behaviour, while the host's approval settings and the cloud identity's IAM roles set the actual limits.

## Validate

```bash
python tooling/skill_coverage.py out/google-cloud-architect-pack                              # regenerate tests/skill-coverage.yml
python tooling/validate_pack.py out/google-cloud-architect-pack --install-check --no-report   # shared validator, includes the unit tests
```

Both scripts are shared at the repository root, not copied into the pack. Paths are relative to the folder that holds the shared `tooling/`.
