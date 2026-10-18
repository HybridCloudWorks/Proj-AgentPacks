# Design Decisions

## Draw.io is the primary product

The pack is optimized for editable `.drawio` XML, not a generic architecture-writing Agent. Mermaid and other importers may accelerate standard diagrams, but custom Azure icons, boundaries, edge routing, and reviewable layout require native Draw.io XML or a controlled post-processing step.

## Thin router plus focused Skills

The Agent contains only shared scope, evidence, safety, and routing. Generic Draw.io generation is separate from Azure semantics so a diagram task does not load every Azure pattern and icon rule.

## Azure correctness is semantic and visual

The pack checks both whether relationships are plausible and whether the drawing communicates them correctly. A private endpoint, subnet, region, zone, Front Door path, governance scope, or identity relationship must not be represented by a merely decorative shape.

## Source-derived diagrams have precedence

When Bicep, ARM, Terraform, Azure Developer CLI, Kubernetes, workflows, or application code is available, the diagram starts from extracted evidence. Missing relationships are labeled as assumptions or design proposals rather than silently invented.

## Static and visual evidence are separate

XML parsing, schema checks, icon-path checks, and edge-reference checks are structural evidence. Opening or rendering in Draw.io and inspecting the result is visual evidence. Neither proves a deployed or secure Azure system.

## Upstream Draw.io material is not duplicated

The current public Draw.io skill is recorded as an upstream dependency and its generic mechanics are distilled into `drawio-core-generation` and `drawio-render-export-and-review`. Azure-specific content is maintained in this pack.

## Gap fill 2026-10-18

The pack shipped with empty `examples/`, `templates/` and `.apm/prompts/` folders. This fill added those artifacts without changing the agent, Skills, contract instruction, `apm.yml` or `compatibility/tool-permissions.yml`. The fill was done without questions to the owner and without web access, so the decisions and assumptions below are recorded for review.

### Workflows come from the Skills' own activation text

Eight primary workflows were identified, each grounded in text the Skills already contain, and each became one prompt:

| Prompt | Grounding |
|---|---|
| `design-diagram-from-requirements.prompt.md` | `azure-architecture-design` interactive design mode |
| `derive-diagram-from-infrastructure.prompt.md` | `azure-architecture-design` source-derived mode |
| `model-azure-architecture-pattern.prompt.md` | `azure-architecture-patterns` pattern checks |
| `review-azure-diagram.prompt.md` | `diagram-validation-and-evidence` "final review", plus the review clauses in the patterns and layout Skills |
| `audit-diagram-against-source.prompt.md` | `diagram-validation-and-evidence` "regression checking, source-to-diagram audits" |
| `repair-drawio-xml.prompt.md` | `drawio-xml-authoring` "repair, normalization" |
| `reflow-diagram-layout.prompt.md` | `drawio-layout-and-composition` "layout, reflow, edge routing" |
| `export-and-review-render.prompt.md` | `drawio-render-export-and-review` |

Review and audit are separate prompts, because they take different inputs (a reference versus current source) and produce different outputs (findings versus a drift table). Repair and reflow are separate, because they belong to different Skills and fail in different ways.

### Prompts name Skills and the contract only

Prompts are installed content, so they name Skills, Skill reference files and the `azure-expert-designer-contract` instruction, and never paths under `templates/`, `docs/` or `tests/`. Each prompt describes the document it produces in words. Every prompt names `drawio-core-generation` and `diagram-validation-and-evidence`, because the agent says to always use both. Read-only prompts use the `drawio-core-generation` output contract as the structural yardstick, rather than generating anything.

### Approval behavior encoded in prompts

The agent's rule "ask before changing or deleting an existing diagram, overwriting source files, publishing externally" is applied in every prompt. Creating prompts write new files. Repair and reflow write a copy under a new name unless an overwrite is approved. Review and audit are read-only and confirm the file is unchanged at the end. Export never overwrites the source, and asks before replacing an existing export or publishing.

### No handoff template

The pack has one agent and no specialists, and the contract instruction defines no handoff format. The completion report's `next_safe_action` carries the handoff to whichever person must act next. A separate handoff template would invent a capability the pack does not have.

### Completion report layout

The contract fixes the nine section names and seven evidence labels, but not a layout. The fill chose one heading per section, in contract order, with one evidence label at the end of each fact or check. This is used in `templates/completion-report.md` and every example. The task type and outcome go in the first bullet of `scope_and_inputs`, because the contract has no separate outcome field.

### "Unresolved" is a semantic status, not an evidence label

`diagram-validation-and-evidence` records semantic evidence as observed, inferred, designed or unresolved, but the contract's evidence labels do not include "unresolved". The evidence matrix in the templates and examples uses "unresolved" only in the semantic tables. Unresolved items then appear in the completion report's `unresolved_risks`, and their checks are labeled `not-verified`.

### Examples are fictional, and icon file names were not re-verified

All six example scenarios are fictional. The Azure2 icon file names in them (for example `Application_Gateways.svg`, `App_Services.svg`, `SQL_Database.svg`, `Storage_Accounts.svg`, `Key_Vaults.svg` and `Front_Doors.svg`) come from the author's knowledge of the Draw.io Azure2 library and were not checked against a catalog during the fill. The Skills require that check at task time, and the examples show it being done. The Draw.io version 24.7.17 in the examples matches `tests/fixtures/minimal.drawio`.

### The skeleton diagram uses neutral shapes only

`templates/azure-diagram-skeleton.drawio` encodes the XML and layout invariants: root cells, stable IDs, real `container=1` subscription, resource group, VNet and subnet boundaries, a decorative `container=0` region frame, 120 px tiles with 180 px gaps, 30 px boundary padding, Helvetica, and a legend for the four edge styles, boundary kinds and the numbered badge. It contains no `image=` paths, so it does not assert any icon file name that could not be verified. Its IDs, parents, sources and targets were checked by hand. The pack's `tooling/validate_drawio_xml.py` helper was not run on it, because the fill environment did not permit running it.

### Per-user Draw.io install location

The render Skill names `C:\Program Files\draw.io\draw.io.exe` and "the user installation directory". The examples assume the per-user directory is `%LOCALAPPDATA%\Programs\draw.io\draw.io.exe`, and label that `inferred`.

### Files touched outside the three folders

- `docs/PROMPT_INVENTORY.md` was created. It maps prompts to Skills, outputs, examples and templates, and includes a Skill-to-prompt coverage table.
- `docs/SKILL_INVENTORY.md` does not exist in this pack. The fill rules allow only updating it, not creating it, so it was not created. The Skill-to-prompt mapping lives in `docs/PROMPT_INVENTORY.md` and in the new `prompt_map` in `tests/capability-coverage.yml`.
- `tests/trigger-cases.yml` gained a `prompt_file` key on each existing case, so the existing `prompt` key, which holds the user's words, keeps its meaning. It also gained four cases that exercise the new prompts: source drift audit, XML repair, layout reflow, and export without a renderer. The `unsafe-mutation` case has no prompt file, because no single workflow owns it.
- `README.md` gained a section on prompts, examples and templates. Its build and validate commands were corrected: they named `tooling/build_pack.py` and `tooling/validate_pack.py --write-report` inside the pack, but that tooling is shared at the repository root and the validator has no `--write-report` flag. The corrected form follows the exemplar pack.

### Observed issue outside the fill's scope

`tests/fixtures/minimal.drawio` uses `img/lib/azure2/app_services/App_Service.svg`. The Azure2 library file for App Service is believed to be `App_Services.svg`. This was not verified, and the fixture is outside the files this fill may change, so it is flagged for the maintainer rather than edited.

### Gaps

- `audit-diagram-against-source.prompt.md` has no dedicated worked example. The read-only review example shows the same approval and evidence pattern.
- No model-behavior evaluation of the new prompts was run. The trigger cases describe expected routing, but they are not executed against a live client.

## Version 1.3.0: shared diagram skills (2026-10-18)

- drawio-core-generation, drawio-render-export-and-review and diagram-validation-and-evidence are now shared skills. The AWS and Azure packs had shipped two different versions of drawio-core-generation and diagram-validation-and-evidence under the same names, so whichever pack was installed last silently replaced the other's. One canonical copy now ships byte-identical in the AWS and Azure architect and designer packs and the Google Cloud architect pack, and CI fails if a copy drifts.
- The skills cover AWS, Azure and Google Cloud alone or in one diagram: each provider's current draw.io library ("AWS <year>", "Azure", "Google Cloud Platform 2026"), the legacy libraries to avoid, and each provider's network scope rules. The facts were verified on 2026-10-18 against draw.io 32.5.5 source and the providers' official icon and network pages.
- The skills now follow the master prompt's ten-part skill structure, which the previous versions did not.
- diagram-validation-and-evidence gained a standard-library checker with an icon catalog generated from draw.io's source. It validates IDs per page and reports every AWS, Azure and Google Cloud icon as current, legacy, retired or unknown.
- This pack's provider-specific skills keep setting house style. The shared skills decide which library is current and how boundaries nest.
- `tests/fixtures/minimal.drawio` used `img/lib/azure2/app_services/App_Service.svg`, which draw.io does not have, so the icon drew without its symbol. The new checker caught it, and the fixture now uses `app_services/App_Services.svg`.

## Prompt names qualified (1.4.0, 2026-10-18)

Several packs shipped prompts under the same name with different content, so installing two of them into the user profile silently replaced one pack's slash command with the other's. This pack's prompts now carry the language or provider inside the name; the qualifier is never a prefix. Slash commands change accordingly.

| Old name | New name |
|---|---|
| `repair-drawio-xml` | `repair-azure-drawio-xml` |
