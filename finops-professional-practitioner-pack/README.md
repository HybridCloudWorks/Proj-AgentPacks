# FinOps Professional Practitioner agent pack

Version 1.0.0. Built to agent-pack-prompt v2.3. One user-facing primary agent, two optional specialists, eight skills, three instruction files and eleven prompts for FinOps practice work grounded in FOCUS billing data.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source. `agents/`, `skills/` (each with its reference file), `instructions/`, `prompts/`. Every vendor file is generated from here.
- `docs/`: approval, handoff, integration, permission, security and evaluation documents, inventories, design decisions and source traceability.
- `compatibility/`: capability map, compatibility matrix, optional skills, vendor sources, and `tool-permissions.yml` (each agent's intended permissions).
- `hooks/`: helper scripts and a reviewed Copilot hook sample. Nothing here is installed as a native hook.
- `examples/`: worked workflows with synthetic figures, a worked completion report and an optional repository-level Copilot review file.
- `templates/`: completion report guide, specialist handoff form, monthly business review and realized-savings tracker.
- `tests/`: unit tests, synthetic fixtures, capability coverage, trigger cases, the report contract and the generated skill coverage.
- `tooling/`: pack-specific helpers (completion contract validator, FinOps arithmetic, hook runner). Validation and build tooling is shared at the repository root.
- `AGENT-PACK-README.md` and `VALIDATION_REPORT.md` are produced by the shared build and validation tooling.

## Install

Into a project with APM, for the clients that project uses:

```bash
apm install saulpatinojr/Proj-Agent_Packs/finops-professional-practitioner-pack --target claude,copilot,codex
```

APM generates `.claude/agents`, `.claude/rules`, `.claude/commands`, `.claude/skills`, `.github/agents`, `.github/instructions`, `.github/prompts`, `.codex/agents`, `.kiro/agents`, `.kiro/steering`, `.kiro/skills`, `.gemini/commands` and skills under `.agents/skills`. Gemini CLI has no agents primitive in APM; it receives skills, commands and context only.

Into the user profile, so the pack works in every repository: use the Code Workflow installer. APM's `-g` install covers Claude Code fully but leaves Copilot agents at project scope and does not deploy Codex instructions.

## Use

Invoke `finops-professional-practitioner` from the client's agent picker and describe the question: a spend summary, an invoice mismatch, an anomaly, a tagging or chargeback design, a forecast or estimate, a waste hunt, a commitment decision, a maturity assessment or a policy. The specialists are not user-invocable; the primary delegates to them. Prompts appear as Copilot prompts, Claude Code commands and Gemini CLI commands.

Point the agent at billing data you already have: a FOCUS export in the workspace, or a query tool configured with read-only credentials. The pack installs no connector.

## Permissions and approvals

Canonical agents declare no `tools`; see `docs/TOOL_PERMISSION_MATRIX.md` and `compatibility/tool-permissions.yml`. Anything that spends, commits, deletes, changes shared state, communicates or shares billing data is Level 2 and needs explicit approval (`docs/APPROVAL_MATRIX.md`). Written instructions are not access control; run the agents with read-only billing credentials.

## Build and validate

```bash
python ../tooling/skill_coverage.py .                 # regenerate tests/skill-coverage.yml
python ../tooling/validate_pack.py . --install-check   # shared validator; writes VALIDATION_REPORT.md
python -m unittest discover -s tests                   # pack unit tests only
```

Archives and the artifact catalog are build outputs of the shared tooling and are not committed.
