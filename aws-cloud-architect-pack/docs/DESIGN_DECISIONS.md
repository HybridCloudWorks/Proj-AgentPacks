# Design Decisions

## Broad architect, focused Skills

The Agent is broad enough to route full-lifecycle AWS work, but the detailed procedures are split so ordinary service selection does not load migration, MCP, landing-zone, and operations material at once.

## Frameworks are decision lenses

AWS Well-Architected's six pillars and AWS CAF's six perspectives organize discovery, trade-offs, readiness, and review. They do not replace workload-specific requirements, current AWS documentation, or evidence.

## Architect versus implementer

The pack understands CloudFormation, CDK, Terraform, AWS CLI, and deployment lifecycles so its designs are implementable. It asks before mutating infrastructure and produces a handoff contract instead of silently applying changes.

## MCP is evidence and controlled action

Official AWS Knowledge MCP is preferred for current documentation and Region/service facts. AWS MCP/API and specialized servers are routed only when present, authorized, and needed. The pack does not assume an MCP tool exists or treat tool output as proof beyond the data actually retrieved.

## Cost, resilience, and operations are architecture concerns

Cross-AZ/cross-Region transfer, NAT, endpoints, managed-service trade-offs, backup/restore, observability, runbooks, and ownership are included in architecture decisions rather than deferred as implementation trivia.

## Visualization is integrated but not duplicated

Architecture diagrams are a first-class output, but the detailed AWS Draw.io generation capability remains in the AWS Expert Designer pack. This pack provides routing, evidence, and handoff integration.

## Gap fill 2026-10-18

The pack shipped without `examples/`, `templates/` or `.apm/prompts/`. They were authored from the existing agent, its 17 skills and the `aws-cloud-architect-contract` instruction. No agent, skill or instruction file was changed, and neither was `apm.yml` or `compatibility/tool-permissions.yml`.

### Decisions

- **Ten prompts, one per primary workflow.** Seven match the existing trigger cases: greenfield workload, landing zone, hybrid network, migration and DR, deployment review, MCP evidence, diagram. The other three serve workflows the skills define but no trigger case covered: Well-Architected review (`aws-well-architected-and-frameworks`), cost review (`aws-cost-sustainability-and-finops`) and incident troubleshooting (`aws-operations-observability-and-troubleshooting`). No standalone handoff prompt was written, because every design prompt ends in the `aws-architecture-handoff-and-adr` handoff.
- **Prompts reference only installed content.** They name skills and the contract instruction. They never point to `templates/`, `docs/` or `tests/`, so they describe the handoff artifacts inline instead of linking to the templates. Frontmatter is limited to `description` and `agent`. APM drops `agent` for Claude Code commands.
- **Handoff template file names follow the hook.** The skill names the artifacts REQ, TOPOLOGY, CONSTRAINTS and ADR, and `hooks/architecture-review.ps1` checks for `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`. The templates use those exact names and formats, so a handoff built from them passes the hook.
- **The skill's handoff extras live inside the four artifacts.** `aws-architecture-handoff-and-adr` also asks for implementation implications, verification criteria, telemetry, rollback, ownership, open questions and a "not proven" section. These went into the four files rather than a fifth one the hook does not know about:
  - verification criteria, ownership, open questions and "not proven" in REQ
  - recovery and rollback in CONSTRAINTS
  - implementation, operations and rollback consequences in each ADR
- **Six templates.** The four handoff files, the contract's completion report, and the Well-Architected review record whose per-pillar fields the skill defines. The evidence record from `aws-docs-mcp-and-evidence` is a table inside the completion report, not a separate template.
- **Six examples, each ending in the contract's twelve sections.** Section names are used verbatim as headings, together with the contract's six evidence labels.
  - `deployment-review-blocked.md` shows a **blocked** outcome: a bundled request to deploy, edit an SCP and delete a stack, which covers the `unsafe-mutation` trigger case.
  - `architecture-diagram.md` shows an **unverified** outcome: structurally validated, but no renderer was available.
  - `incident-troubleshooting.md` separates a live-verified mitigation from a root cause that is inferred.
- **Example continuity.** Three examples share the fictional Larkspur tracking platform: design, then incident, then diagram. This shows TOPOLOGY ids carrying through to diagram cell IDs, and an ADR superseding an unrecorded change.
- **Test metadata.** `tests/trigger-cases.yml` gains a `prompt_file` key, because `prompt` already holds the user utterance, and three cases for the new workflows. `tests/capability-coverage.yml` gains a `prompt_map` from each required capability to its prompts. The existing `skill_map` was left as it was.
- **Inventories.** `docs/PROMPT_INVENTORY.md` was created. `docs/SKILL_INVENTORY.md` did not exist; the brief lists it as updatable, so it was created to map each skill to its prompts, examples and templates.
- **README.** Added the prompt, example and template sections. The validate command was corrected to the shared validator's real usage (`validate_pack.py <pack-folder>`); the old `--write-report` flag does not exist.

### Assumptions

- The primary workflows are the ones the agent profile lists (foundations, workload design, deployment, operations, migration, security, resilience, cost, evidence, handoff, visualization). Security has no separate prompt; it runs inside the landing-zone, workload, deployment-review and Well-Architected prompts.
- Every company, account, CIDR, figure and timestamp in the examples is fictional. The evidence-table results for AWS behavior describe well-documented service behavior. Each example still labels them with a retrieval date and treats account-applied values as not-verified.
- The examples assume the AWS Knowledge MCP Server was available in some sessions and not in others, to show both paths. Neither was exercised while authoring.
- The examples quote two documented AWS limits: the NAT gateway connections per unique destination, and the CDK default removal policy for database clusters. Both come from the author's knowledge of AWS documentation, because the brief forbade browsing. They must be rechecked when the examples are next revised.

### Gaps

- No `AGENT-PACK-README.md` artifact catalog exists, and creating one was outside the files this fill may change.
- No `VALIDATION_REPORT.md` was written, because the validator ran with `--no-report` as the brief directs.
- The README build command (`python tooling/build_pack.py`) is unchanged. Its arguments could not be checked, because the shared build script is not in this workspace.
- Prompt and example behavior is not model-evaluated. The trigger cases are metadata and have not been run as a behavioral suite.

## Version 1.3.0: shared diagram skills (2026-10-18)

- drawio-core-generation, drawio-render-export-and-review and diagram-validation-and-evidence are now shared skills. The AWS and Azure packs had shipped two different versions of drawio-core-generation and diagram-validation-and-evidence under the same names, so whichever pack was installed last silently replaced the other's. One canonical copy now ships byte-identical in the AWS and Azure architect and designer packs and the Google Cloud architect pack, and CI fails if a copy drifts.
- The skills cover AWS, Azure and Google Cloud alone or in one diagram: each provider's current draw.io library ("AWS <year>", "Azure", "Google Cloud Platform 2026"), the legacy libraries to avoid, and each provider's network scope rules. The facts were verified on 2026-10-18 against draw.io 32.5.5 source and the providers' official icon and network pages.
- The skills now follow the master prompt's ten-part skill structure, which the previous versions did not.
- diagram-validation-and-evidence gained a standard-library checker with an icon catalog generated from draw.io's source. It validates IDs per page and reports every AWS, Azure and Google Cloud icon as current, legacy, retired or unknown.
- This pack's provider-specific skills keep setting house style. The shared skills decide which library is current and how boundaries nest.

## Prompt names qualified (1.4.0, 2026-10-18)

Several packs shipped prompts under the same name with different content, so installing two of them into the user profile silently replaced one pack's slash command with the other's. This pack's prompts now carry the language or provider inside the name; the qualifier is never a prefix. Slash commands change accordingly.

| Old name | New name |
|---|---|
| `create-architecture-diagram` | `create-aws-architecture-diagram` |
| `design-landing-zone` | `design-aws-landing-zone` |
| `design-hybrid-network` | `design-aws-hybrid-network` |
| `plan-migration-and-dr` | `plan-aws-migration-and-dr` |
| `review-well-architected` | `review-aws-well-architected` |
