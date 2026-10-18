# Design Decisions

## Broad Azure architect, focused Skills

The Agent is broad enough to route full-lifecycle Azure work, but the detailed procedures are split so ordinary service selection does not load migration, MCP, landing-zone, AVM, and operations material at once.

## Frameworks are decision lenses

Azure Well-Architected's five pillars and Cloud Adoption Framework for Azure organize workload quality, adoption, landing zones, governance, trade-offs, readiness, and review. They do not replace workload-specific requirements, current Microsoft documentation, or evidence.

## Architect versus implementer

The pack understands Bicep/ARM, Terraform, AzAPI/AzureRM, AVM, deployment stacks, Azure CLI, what-if, and deployment lifecycles so its designs are implementable. It asks before mutating infrastructure and produces a handoff contract instead of silently applying changes.

## MCP is evidence and controlled action

Official Microsoft Learn and Azure MCP are preferred for current documentation, Azure resource guidance, and read-only evidence. Azure MCP/API and specialized servers are routed only when present, authorized, and needed. The pack does not assume an MCP tool exists or treat tool output as proof beyond the data actually retrieved.

## Cost, resilience, and operations are architecture concerns

Zone/region transfer, Private Link, NAT, egress, managed-service trade-offs, backup/restore, observability, runbooks, and ownership are included in architecture decisions rather than deferred as implementation trivia.

## Visualization is integrated but not duplicated

Architecture diagrams are a first-class output, but the detailed Azure Draw.io generation capability remains in the Azure Expert Designer pack. This pack provides routing, evidence, and handoff integration.

## Gap fill 2026-10-18

The pack shipped without `.apm/prompts/`, `examples/` and `templates/`. This entry records how they were added and what was assumed. No agent, Skill, instruction, `apm.yml` or `compatibility/tool-permissions.yml` changed.

### What was added

- Ten prompts, one per primary workflow. The workflows come from the agent's operating contract, the eighteen Skills, and the cases already in `tests/trigger-cases.yml`: workload design, landing zone, hybrid network, migration and DR, IaC and deployment review, Well-Architected review, cost, evidence verification, troubleshooting, and diagrams. Every Skill is applied by at least one prompt; the map is in `PROMPT_INVENTORY.md`.
- Six examples, each ending with a completion report using the contract's twelve section names and evidence labels. `iac-deployment-review-blocked.md` ends blocked; `architecture-diagram-workflow.md` ends unverified.
- Templates: the four handoff artifacts in `templates/handoff/`, plus `completion-report.md` and `evidence-register.md`.

### Assumptions

1. **Handoff file names.** The contract names the artifacts REQ, TOPOLOGY, CONSTRAINTS and ADR but not their formats. `hooks/architecture-review.ps1` checks for `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`, so templates and prompts use exactly those names, and `templates/handoff/` contains those four files. `azure-architecture-foundations` allows JSON or YAML for TOPOLOGY; JSON was chosen to match the hook.
2. **One ADR file.** Because the hook expects a single `ADR.md`, it holds one section per decision (ADR-001, ADR-002 ...), each Proposed until its decision owner accepts it.
3. **Evidence labels.** The contract lists the six labels without defining them. The templates define "observed" as seen in supplied files, command output or retrieved documentation, and treat a requester's statement as observed only as a statement. Acceptance criteria live in `REQ.md`, since `azure-architecture-handoff-and-adr` requires them but names no separate artifact.
4. **Diagram routing.** `azure-architecture-visualization` routes detailed Draw.io work to the Azure Expert Designer, yet the pack also ships `drawio-core-generation`, `drawio-render-export-and-review` and `diagram-validation-and-evidence`, and the `diagram` trigger case expects `drawio-core-generation`. The diagram prompt therefore routes to the designer when the host has it, and otherwise uses the pack's own Draw.io Skills and says so.
5. **Prompts reference only installed content.** They name the agent, the Skills and the `azure-cloud-architect-contract` instruction, never `templates/`, `examples/`, `docs/`, the hook or the pack tooling. The handoff file names they use are files the agent writes in the user's repository.
6. **Approval boundaries.** Each prompt restates the agent's rule 8 for its own workflow (for example, review stays read-only, and a plan does not authorize a failover), because a prompt may be run without the rest of the conversation.
7. **Examples are synthetic.** Contoso, Fabrikam and Northwind are sample names. Without web access during authoring, examples cite only URLs already in `SOURCE_TRACEABILITY.md` and `compatibility/vendor-sources.yml`. Version- and region-sensitive Azure facts in examples are labelled not-verified, and no example quotes a price, limit or replication objective as fact.
8. **No Well-Architected or runbook template.** Review gaps go in the completion report's `framework_alignment` and `unresolved_risks` sections, and runbook outlines appear in the migration example. That keeps the templates to the documents the Skills explicitly name.
9. **`docs/SKILL_INVENTORY.md` was not created.** It did not exist, and the gap-fill rules allow creating only `PROMPT_INVENTORY.md`. The Skill-to-prompt map lives there instead.
10. **Test metadata.** `tests/trigger-cases.yml` gained a `workflow_prompt` key on each case (the existing `prompt` key holds the user's words) and three cases for the prompts that had none. `tests/capability-coverage.yml` gained a `prompt_map` from prompt file to capabilities.
11. **README.** The build and validate commands pointed at a per-pack `tooling/validate_pack.py` and a `--write-report` flag, neither of which exists. They now use the shared tooling at the repository root. The stale mention of "targets" in the full-pack download line was removed.

### Gaps left open

- The `unsafe-mutation` trigger case says "change SCPs", an AWS term. The Azure equivalent is Azure Policy or management-group assignments. The wording was left unchanged, because this gap fill only adds prompt references to that file.
- `tests/capability-coverage.yml` `skill_map` still omits `drawio-core-generation`, `drawio-render-export-and-review` and `diagram-validation-and-evidence`. Their coverage is recorded only through `prompt_map`.
- `compatibility/compatibility-matrix.yml` lists a Gemini agent path although APM deploys no agents to Gemini, and `compatibility/optional-skills.yml` holds a machine-specific local path. Both are outside the files this gap fill may change.
- The pack has no `test_*.py`, so the validator's unit-test check is skipped. The examples' commands and outputs are illustrative; none was executed against Azure.
- `build_pack.py` was not run, and how each host surfaces the prompts has not been observed live.
- Only the shared validator could be executed during the gap fill. `hooks/architecture-review.ps1` was not run against `templates/handoff/`, and the two JSON templates were checked by reading them, not by a parser. The validator does not inspect template content.
