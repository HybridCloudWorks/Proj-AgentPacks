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
- The pack has no `test_*.py`, so the validator's unit-test check is skipped. The examples' commands and outputs are illustrative; none was executed against Azure. (1.5.0 added `tests/test_drawio_assets.py` for the pack's draw.io fixture; the examples remain illustrative.)
- `build_pack.py` was not run, and how each host surfaces the prompts has not been observed live.
- Only the shared validator could be executed during the gap fill. `hooks/architecture-review.ps1` was not run against `templates/handoff/`, and the two JSON templates were checked by reading them, not by a parser. The validator does not inspect template content.

## Version 1.3.0: shared diagram skills (2026-10-18)

- drawio-core-generation, drawio-render-export-and-review and diagram-validation-and-evidence are now shared skills. The AWS and Azure packs had shipped two different versions of drawio-core-generation and diagram-validation-and-evidence under the same names, so whichever pack was installed last silently replaced the other's. One canonical copy now ships byte-identical in the AWS and Azure architect and designer packs and the Google Cloud architect pack, and CI fails if a copy drifts.
- The skills cover AWS, Azure and Google Cloud alone or in one diagram: each provider's current draw.io library ("AWS <year>", "Azure", "Google Cloud Platform 2026"), the legacy libraries to avoid, and each provider's network scope rules. The facts were verified on 2026-10-18 against draw.io 32.5.5 source and the providers' official icon and network pages.
- The skills now follow the master prompt's ten-part skill structure, which the previous versions did not.
- diagram-validation-and-evidence gained a standard-library checker with an icon catalog generated from draw.io's source. It validates IDs per page and reports every AWS, Azure and Google Cloud icon as current, legacy, retired or unknown.
- This pack's provider-specific skills keep setting house style. The shared skills decide which library is current and how boundaries nest.
- `tests/fixtures/minimal.drawio` used `img/lib/azure2/app_services/App_Service.svg`, which draw.io does not have, so the icon drew without its symbol. The new checker caught it, and the fixture now uses `app_services/App_Services.svg`.
- `tests/capability-coverage.yml` now maps the three shared skills, which closes the coverage gap recorded in the gap fill.

## Prompt names qualified (1.4.0, 2026-10-18)

Several packs shipped prompts under the same name with different content, so installing two of them into the user profile silently replaced one pack's slash command with the other's. This pack's prompts now carry the language or provider inside the name; the qualifier is never a prefix. Slash commands change accordingly.

| Old name | New name |
|---|---|
| `create-architecture-diagram` | `create-azure-architecture-diagram` |
| `design-landing-zone` | `design-azure-landing-zone` |
| `design-hybrid-network` | `design-azure-hybrid-network` |
| `plan-migration-and-dr` | `plan-azure-migration-and-dr` |
| `review-well-architected` | `review-azure-well-architected` |

## Version 1.5.0: shared checker and renderer detection (2026-11-01)

An independent review of the Azure packs' draw.io content and a live generation test, both on 2026-11-01, found defects in this pack's own diagram material. This release fixes them, and it also ships updated copies of the shared draw.io skills, which changed in the same release. A pre-PR review the same day found that an earlier draft of this record said the shared skills were not changed, and found smaller gaps; its findings are cited as "pre-PR F1", "pre-PR F5" and "pre-PR F9".

- **The shared draw.io skills change in this release too, so a diagram that passed 1.4.0 can fail now (pre-PR F1).** The icon catalog in `diagram-validation-and-evidence` is rebuilt from draw.io 32.6.9 (1.4.0 shipped a catalog of icon names only, from an earlier draw.io release) and records every palette entry's title, form, default size and full style, leaving out the palette's connection points; `check_drawio.py --find "<product>"` prints the style to copy. The checker reports new errors: an Azure path in the letter case that draw.io's palette inserts for four files, which draws a broken image (for example `management_governance/solutions.svg` for the file `Solutions.svg`); an AWS or Google Cloud icon without its palette `fillColor`, or with a palette colour set to `none`, which draws incompletely; and an AWS name used in a form the library does not offer (wrong-form). A recoloured AWS or Google Cloud icon, or one without its `strokeColor`, is a warning, and an error with `--strict`. Azure icons are images, so the checker looks up their path and does not compare colours. `drawio-core-generation`'s provider reference gains a "Which file to use" table for Azure products that draw.io offers more than once or that Microsoft publishes outside the Azure set (Microsoft Entra ID, private endpoint, private DNS zone and others), and its workflow step 4 gains the boundary rules the diagram prompt states. `drawio-render-export-and-review` adds a `reg query` fallback for finding the Microsoft Store build and render checks for partly drawn icons, wrapped labels and edge labels.
- **The pack's own Draw.io helper is gone.** The script under `tooling/` accepted misspelled `img/lib/azure2/` paths, an invented `img/lib/general/` path and Cloud & Enterprise (`mxgraph.mscae.*`) stencils, and it checked IDs across the whole file, so it reported a false duplicate-ID failure on every valid multi-page diagram. `architecture-diagram-workflow.md` showed it printing PASS for a two-page diagram and reported that as `structurally-validated`. README, the artifact catalog and that example now use the shared checker, `diagram-validation-and-evidence/scripts/check_drawio.py --strict`, which validates each page on its own and looks up every Azure icon in its catalog of draw.io's libraries.
- **The example's XML follows the library style.** The excerpt now copies the palette's own icon style (`image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/...;`, as `check_drawio.py --find` prints it, with the palette's optional connection points kept), sizes SQL Database at 36 by 48 (48 px on the longest side), makes the resource group a real container with its scope icon in the corner, and positions the edge label. Zone redundancy is a label on the region frame and on each zone-redundant service, never a zone frame.
- **Renderer detection includes the Microsoft Store build.** `create-azure-architecture-diagram.prompt.md` and the example look for `app\draw.io.exe` inside the InstallLocation that `Get-AppxPackage *draw.io*` reports, as well as PATH and the installer and per-user locations, before reporting that rendering was not run. The prompt now runs the checker after every write, exports with `-k`, passes `--embed-svg-images` for SVG, never passes `--layout` or `--normalize` for review, and runs `diagram-validation-and-evidence` again after the last edit. It also states the Azure boundary rules from `drawio-core-generation` workflow step 4.
- **Wording.** `azure-architecture-visualization` and the diagram prompt call the icons Microsoft's Azure architecture icons from draw.io's Azure library (ID `azure2`), instead of "Azure2 icons".
- **Fixture fixed.** `tests/fixtures/minimal.drawio` uses the palette style and 48 px icons, and no longer parents icons to its decorative (`container=0`) region frame.
- **The example quotes the shipped checker (pre-PR F5).** Its checker output prints `catalog: draw.io 32.6.9, built 2026-11-01`, as the shipped checker does, and its evidence lines cite catalog draw.io 32.6.9.
- **Regression guard (pre-PR F9).** `tests/test_drawio_assets.py`, the same file as in the Azure Expert Designer pack, runs the pack's own `check_drawio.py --strict` on the fixture and checks what the checker does not decide for Azure: the palette icon style `--find` prints with `aspect=fixed` and only `points`, typography and label placement appended, 48 px icons at the palette's aspect ratio (24 px for a scope icon), no cell parented to a `container=0` frame, no subnet inside a zone frame, labelled scope icons and edges, and no mention of the removed helper. Negative tests show each guard failing on a known defect, including the 1.4.0 fixture, which the strict checker passes. The validator now runs these tests instead of skipping the unit-test check.
- `AGENT-PACK-README.md` was edited by hand (version, the removed helper's row and the new test's row). `tooling/build_pack.py` regenerates it on the next build.

Evidence, 2026-11-01: the pack's own `check_drawio.py --strict`, catalog draw.io 32.6.9 built 2026-11-01, passed the fixture with 2 Azure icons current, 0 errors and 0 warnings; the fixture rendered with Draw.io Desktop 32.6.1 (Microsoft Store build, `-x -k -f png`) and both icons drew with their labels below them; `python -I -B -m unittest discover -s tests` (Python 3.14) ran 11 tests, all passing with 1 skipped (the guidance check, because this pack ships no Azure icon-style guidance), and `test_azure_invariants` failed when the 1.4.0 fixture was put back in a scratch copy; `tooling/validate_pack.py azure-cloud-architect-pack --no-report` passed with 143 checks, 0 failures and 1 skipped (`apm install`, which needs `--install-check`); `tooling/skill_coverage.py --check` and `tooling/root_manifest.py --check` reported current; `tooling/check_collisions.py --github --strict` found 0 collisions. The example's checker output is illustrative: it was written to match the checker's text format, not produced by running it on the fictional file. Not verified: Python 3.9 or 3.12 runs of the tests, `apm install` after these corrections, and model behaviour. The root `apm.yml` pins this pack at tag `azure-cloud-architect-v1.5.0`, which does not exist until the release is cut.
