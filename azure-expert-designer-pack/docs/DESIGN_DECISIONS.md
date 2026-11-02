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

`templates/azure-diagram-skeleton.drawio` encodes the XML and layout invariants: root cells, stable IDs, real `container=1` subscription, resource group, VNet and subnet boundaries, a decorative `container=0` region frame, 120 px tiles with 180 px gaps, 30 px boundary padding, Helvetica, and a legend for the four edge styles, boundary kinds and the numbered badge. It contains no `image=` paths, so it does not assert any icon file name that could not be verified. Its IDs, parents, sources and targets were checked by hand. The pack's former Draw.io helper script under `tooling/` (removed in 1.5.0) was not run on it, because the fill environment did not permit running it.

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

## Version 1.5.0: shared checker, library icon style and shared boundary rules (2026-11-01)

An independent review of the Azure packs' draw.io content (findings F1 to F18) and a live generation test, both on 2026-11-01, found defects in this pack's own material around the shared draw.io skills. This release fixes them. It also ships updated copies of the shared skills (`drawio-core-generation`, `diagram-validation-and-evidence`, `drawio-render-export-and-review`), which are maintained in the repository's `shared-primitives/` and changed in the same release; the first bullet below says what changed. A pre-PR review the same day found that an earlier draft of this record said the shared skills were not changed, and found three smaller gaps; its findings are cited as "pre-PR F1", "pre-PR F4", "pre-PR F5" and "pre-PR F9".

### Changes

- **The shared draw.io skills change in this release too, so a diagram that passed 1.4.0 can fail now (pre-PR F1).** The icon catalog in `diagram-validation-and-evidence` is rebuilt from draw.io 32.6.9 (1.4.0 shipped a catalog of icon names only, from an earlier draw.io release) and records every palette entry's title, form, default size and full style, leaving out the palette's connection points; `check_drawio.py --find "<product>"` prints the style to copy. The checker reports new errors: an Azure path in the letter case that draw.io's palette inserts for four files, which draws a broken image (for example `management_governance/solutions.svg` for the file `Solutions.svg`); an AWS or Google Cloud icon without its palette `fillColor`, or with a palette colour set to `none`, which draws incompletely; and an AWS name used in a form the library does not offer (wrong-form). A recoloured AWS or Google Cloud icon, or one without its `strokeColor`, is a warning, and an error with `--strict`. Azure icons are images, so the checker looks up their path and does not compare colours. `drawio-core-generation`'s provider reference gains a "Which file to use" table for Azure products that draw.io offers more than once or that Microsoft publishes outside the Azure set (Microsoft Entra ID, private endpoint, private DNS zone and others), and its workflow step 4 gains the boundary rules this pack routes to (see below). `drawio-render-export-and-review` adds a `reg query` fallback for finding the Microsoft Store build and render checks for partly drawn icons, wrapped labels and edge labels.
- **The pack's own Draw.io helper is gone (F1).** The script under `tooling/` accepted misspelled `img/lib/azure2/` paths, an invented `img/lib/general/` path and Cloud & Enterprise (`mxgraph.mscae.*`) stencils, and it checked IDs across the whole file, so every valid multi-page diagram failed. README, the artifact catalog and the five worked examples that cited it now use the shared checker, `diagram-validation-and-evidence/scripts/check_drawio.py --strict`, and quote its catalog version and Azure icon summary. The examples no longer present a path-prefix check as `structurally-validated`, and no longer claim that IDs are unique across pages: the checker validates each page on its own.
- **Icon style is the library's (F2, F10, pre-PR F4).** README, `azure-icons-and-visual-language` and `drawio-xml-authoring` give the palette's full style as `check_drawio.py --find "<product>"` prints it, `image;aspect=fixed;html=1;align=center;fontSize=12;image=img/lib/azure2/<category>/<File_Name>.svg;`, and say to append only typography and label placement. The palette's `points=[...]` are optional: they are connection points, they do not change how an icon draws, and the catalog and `--find` leave them out (an earlier draft required them). The skeleton and fixtures keep them. `xml-checklist.md` item 1 now describes the parser the checker uses, a standard parser that refuses DOCTYPE and ENTITY declarations (draw.io XML has no namespaces), instead of "a namespace-aware parser", and item 10 lists what the checker covers and what still needs reading. The library style wins over this pack's house style, which sets typography, sizes, layout and legend. "Azure" is draw.io's library name and `azure2` its ID; the icons are Microsoft's Azure architecture icons. The wording now says "use" rather than "prefer", and the forbidden list is crop, flip, rotate, distort, recolour and change shape. Do not add `whiteSpace=wrap` to an icon style: it wraps the label to the icon's width.
- **Icon size is defined (F18).** "48 px" means 48 px on the longest side with `aspect=fixed` (SQL Database is 36 by 48). Scope icons in frame corners are 24 px on the longest side.
- **No legacy fallback (F3).** `drawio-xml-authoring` names every legacy family (`mxgraph.azure.*`, `mxgraph.mscae.*`, `img/lib/mscae/`), allows them only to match an existing diagram on the user's request, and drops `mxgraph.azure2`, which is not a draw.io shape namespace.
- **Boundary rules come from the shared skills (F4, F5).** The design, review, repair and pattern prompts, `azure-icons-and-visual-language`, `azure-visual-rules.md`, `azure-architecture-design` and `azure-architecture-patterns` route boundary nesting to `drawio-core-generation` workflow step 4 and the scope-rule table in `diagram-validation-and-evidence/references/provider-checks.md`, and state the Azure rules in the same terms: a VNet lives in one region; subnets span every zone, so a subnet never sits in a zone frame; zone-redundant resources are labelled with their zones; PaaS behind a private endpoint stays outside the VNet with only the endpoint NIC in the subnet; App Service with regional VNet integration stays outside the VNet with an outbound edge into its delegated subnet. The resource-group-versus-subnet conflict is resolved by one rule: network containment wins, so a resource whose resource group differs from its VNet's is parented to the network boundary it is deployed into, with its resource group in its label or a decorative `container=0` frame. A subscription or resource group frame is a real container only for cells that truly belong to it, and a `container=0` frame never has child cells.
- **Renderer detection and export options (F6, F7).** Every prompt that renders, and every example that detects draw.io, includes the Microsoft Store build: `app\draw.io.exe` inside the InstallLocation that `Get-AppxPackage *draw.io*` reports, or, without PowerShell, the package folder that `reg query "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages" | findstr draw.io` names. Exports pass `-k`, SVG exports pass `--embed-svg-images`, review exports never pass `--layout` or `--normalize`, and `diagram-validation-and-evidence` runs again after the render and the last edit. `export-blocked-workflow.md` now declares the export blocked only after the PATH, installer, per-user and Store checks all come back empty, and its next action gives the full SVG export command.
- **References to material that does not exist are gone (F11).** `azure-architecture-patterns` no longer points at "basic and advanced templates", and `azure-visual-rules.md` no longer cites "the supplied Azure Designer references".
- **Skeleton rebuilt (F12, F18).** `templates/azure-diagram-skeleton.drawio` now has scope icons in each frame's top-left corner labelled with the frame's name (`general/Subscriptions.svg`, `general/Resource_Groups.svg`, `networking/Virtual_Networks.svg`, `networking/Subnet.svg`); decorative region and global-resource frames with no child cells and the zones as a label; a private endpoint (`other/Private_Endpoints.svg`) in its subnet whose resource group differs from the VNet's; a private DNS zone drawn with the DNS Zones icon labelled "Private DNS zone", with a dotted "VNet link" edge; a transport label on the ingress edge ("HTTPS via [public endpoint, regional gateway or Private Link origin]"); a label on every edge, positioned clear of frame borders; and legend line samples drawn as shapes, so every edge in the file is a real, labelled flow.
- **Fixture fixed (F2).** `tests/fixtures/minimal.drawio` uses the palette style, 48 px icons and no children under its decorative region frame.
- **Edge labels (live test).** `drawio-layout-and-composition` now says that draw.io places an edge label at the midpoint of the whole bent edge, so a label on an edge that crosses nested frames often lands on a frame border, and how to move it with the geometry's relative `x` and an offset point.
- **Example renderer version.** The examples' Draw.io Desktop version moved from 24.7.17 to 32.6.1, the build this release's renders used. It is older than the checker's catalog (draw.io 32.6.9), so an icon draw.io added after 32.6.1 could pass the checker and still not draw in it: only a render shows that an icon draws. Every icon in the skeleton and fixtures drew in 32.6.1 (evidence below). Guidance for a renderer older than the catalog belongs to the shared skills, which today cover only a newer one.
- **Examples quote the shipped checker (pre-PR F5).** Every example's checker output now prints `catalog: draw.io 32.6.9, built 2026-11-01`, as the shipped checker does, and the completion reports cite catalog draw.io 32.6.9. The error lines the examples quote (a legacy `mxgraph.azure` stencil, a compressed page, duplicate IDs, missing edge targets) were reproduced word for word by running the checker on probe files.
- **Regression guard (pre-PR F9).** `tests/test_drawio_assets.py` replaces the unshipped script, and the validator now runs it. It runs the pack's own `check_drawio.py --strict` on every `.drawio` file in the pack, then checks what the checker does not decide for Azure: each icon starts with the palette style `--find` prints, keeps `aspect=fixed` and the palette's aspect ratio, appends only `points`, typography and label placement, never `whiteSpace=wrap`, and is 48 px on its longest side (24 px for a scope icon); no cell is parented to a `container=0` frame or another non-container; no subnet sits inside a zone frame, by parent or by position; each scope icon is labelled with its scope; every edge has a label; nothing mentions the removed helper; and the icon-style guidance neither requires `points` nor says "namespace-aware". Negative tests show each guard failing on a known defect, including the 1.4.0 fixture, which the strict checker passes. The same file ships in the Azure Cloud Architect pack.
- `AGENT-PACK-README.md` was edited by hand (version, the removed helper's row and the new test's row). `tooling/build_pack.py` regenerates it with the vendor package counts on the next build.

### Decisions

- **Private endpoint icon.** draw.io's palette offers both `networking/Private_Endpoint.svg` and `other/Private_Endpoints.svg`, and the catalog lists both as current. The skeleton and examples use `other/Private_Endpoints.svg`, because Microsoft's V24 download places its Private Endpoints icon under `other/`. Where the shared provider reference names a file, it wins.
- **Private DNS zone icon.** Microsoft's V24 set has a DNS Zones icon and no separate private DNS zone icon, so a private DNS zone is the DNS Zones icon labelled "Private DNS zone". This replaces the neutral shape in the requirements example.
- **Microsoft Entra ID icon.** Pack content does not choose a file; it defers to the shared provider reference, which states which draw.io file to use for Entra ID.

### Evidence, 2026-11-01

- The pack's own `check_drawio.py --strict`, catalog draw.io 32.6.9 built 2026-11-01: the skeleton passes with 42 vertices, 5 edges, 8 Azure icons current, 0 errors and 0 warnings; the fixture passes with 2 Azure icons current, 0 errors and 0 warnings.
- Both files rendered with Draw.io Desktop 32.6.1 (Microsoft Store build) using `-x -k -f png`, without `--layout` or `--normalize`. The PNGs were opened and inspected: every Azure icon drew, product labels sit below their icons, scope labels sit beside their corner icons, and no edge label sits on a frame border.
- `python -I -B -m unittest discover -s tests` (Python 3.14): 11 tests pass. With the 1.4.0 fixture put back in a scratch copy of the pack, `test_azure_invariants` fails on the icon style, the 120 px icons and three cells parented to the `container=0` frame, while the strict checker passes that fixture. With the pre-correction guidance text, `test_icon_guidance_matches_the_shared_tools` fails on the `points` requirement and on "namespace-aware".
- `tooling/validate_pack.py azure-expert-designer-pack --no-report`: PASS, 111 checks, 0 failures, 1 skipped (`apm install`, which needs `--install-check`); the pack unit tests now run instead of being skipped. `tooling/skill_coverage.py --check`: current. `tooling/root_manifest.py --check`: current. `tooling/check_collisions.py --github --strict`: 0 collisions.

### Not verified

- How each client renders the prompts and skills; no model behaviour was evaluated.
- The worked examples remain illustrative: their summary lines were written to match the checker's text format, not produced by running it on those fictional files. Only their error lines were reproduced, on probe files.
- `tests/test_drawio_assets.py` ran on Python 3.14 only. It uses no syntax or library newer than Python 3.9, but no 3.9 or 3.12 interpreter was run.
- `apm install` (`validate_pack.py --install-check`) was not rerun after these corrections.
- The root `apm.yml` pins this pack at tag `azure-expert-designer-v1.5.0`, which does not exist until the release is cut.
