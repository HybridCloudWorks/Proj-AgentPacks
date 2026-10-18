# Azure Cloud Architect Pack

Portable Agent/Skill package for the full Azure cloud-architecture lifecycle. This pack is broader than the Azure Expert Designer: it designs and reviews Azure foundations and workloads, supports controlled deployment and operations, and routes detailed Draw.io production to the separate diagram capability when needed.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source. One primary agent (`azure-cloud-architect`), eighteen Skills, the always-on `azure-cloud-architect-contract` instruction, and ten workflow prompts in `.apm/prompts/`. Every vendor file is generated from here.
- `examples/`: six worked walkthroughs, each ending with a completion report in the contract's format. `iac-deployment-review-blocked.md` shows a blocked outcome and `architecture-diagram-workflow.md` an unverified one.
- `templates/`: `handoff/` holds `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`, the four handoff artifacts under the names the optional hook checks; plus `completion-report.md` and `evidence-register.md`.
- `docs/`: design decisions, source traceability, and the prompt inventory with the Skill-to-prompt map.
- `compatibility/`, `hooks/`, `tests/`, and `tooling/validate_drawio_xml.py` (a pack helper for static Draw.io checks).

## Workflow prompts

| Prompt | Use it to |
|---|---|
| design-azure-workload.prompt.md | Design a workload and produce the REQ, TOPOLOGY, CONSTRAINTS and ADR handoff |
| design-azure-landing-zone.prompt.md | Design or audit platform and application landing zones |
| design-azure-hybrid-network.prompt.md | Design hub-spoke or Virtual WAN, hybrid connectivity, Private Link and DNS |
| plan-azure-migration-and-dr.prompt.md | Plan migration waves, DR tiers, cutover, rollback and rehearsal |
| review-iac-and-deployment-plan.prompt.md | Review Bicep, ARM or Terraform/AVM changes and their what-if or plan |
| review-azure-well-architected.prompt.md | Run a five-pillar and CAF review that returns prioritized gaps |
| estimate-azure-cost.prompt.md | Build an assumption-based cost model with budgets and FinOps controls |
| verify-azure-evidence.prompt.md | Check drift-prone facts against Microsoft Learn and authorized Azure MCP |
| troubleshoot-azure-issue.prompt.md | Diagnose a deployment, access, network or runtime failure from evidence |
| create-azure-architecture-diagram.prompt.md | Produce an editable Draw.io diagram from an approved topology |

Prompts appear as Copilot prompt files and Claude Code commands. The `agent` field is honoured by Copilot and dropped by Claude. Where a host has no prompts, invoke `azure-cloud-architect` directly. Details are in `docs/PROMPT_INVENTORY.md`.

## Primary downloads

- `dist/azure-cloud-architect-pack.zip` — complete source, tests, hooks, tooling, and archives.
- `dist/azure-cloud-architect-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/azure-cloud-architect-prompt.zip` — reusable pack-authoring prompt.
- `dist/azure-cloud-architect-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `azure-cloud-architect-skills.zip`.

## Build and validate

Validation and build tooling is shared at the pack repository root, not copied into this pack. From this folder:

```text
python ../tooling/skill_coverage.py .                    # regenerates tests/skill-coverage.yml from the Skills
python ../tooling/validate_pack.py . --install-check     # shared validator; writes VALIDATION_REPORT.md
python ../tooling/build_pack.py .                        # shared builder; writes dist/
```

Validation is static and non-mutating. It does not prove a live Azure tenant, subscription, deployment, Entra/RBAC/Policy authorization, quota, regional availability, cost, security posture, or recovery result.

## MCP and official evidence

When the host supports it, prefer Microsoft Learn, Azure Architecture Center, CAF, WAF, AVM, and the official Azure MCP Server for current Azure documentation, resource guidance, best practices, and read-only evidence. Use Azure MCP tools only within explicit authorization and least-privilege boundaries. MCP availability is an integration capability, not a reason to bypass approvals.

## Optional hook

`hooks/architecture-review.ps1` checks a proposed handoff directory for the required REQ, TOPOLOGY, CONSTRAINTS, and ADR artifacts (`REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json`, `ADR.md`). It is opt-in and non-mutating; it does not deploy or call Azure, and it checks presence, not content. Copying `templates/handoff/` gives a folder that already has the four names.
