# Design Decisions

## Draw.io is the primary product

The pack is optimized for editable `.drawio` XML, not a generic architecture-writing Agent. Mermaid and other importers may accelerate standard diagrams, but custom AWS4 icons, boundaries, edge routing, and reviewable layout require native Draw.io XML or a controlled normalization step.

## Thin router plus focused Skills

The Agent contains only shared scope, evidence, safety, and routing. Generic Draw.io generation is separate from AWS semantics so a diagram task does not load every AWS pattern and icon rule.

## AWS correctness is semantic and visual

The pack checks both whether relationships are plausible and whether the drawing communicates them correctly. An account, Region, AZ, VPC, subnet, NAT gateway, endpoint, Transit Gateway, replication path, or egress edge must not be represented by a merely decorative shape.

## Source-derived diagrams have precedence

When CloudFormation, CDK, Terraform, or application code is available, the diagram starts from extracted evidence. Missing relationships are labeled as assumptions or design proposals rather than silently invented.

## Cost-bearing edges are first-class

Cross-AZ, cross-Region, internet, hybrid, and data-transfer paths should be visible when relevant. The diagram does not calculate a bill, but it makes cost-sensitive design choices reviewable.

## Static and visual evidence are separate

XML parsing, schema checks, the icon catalog check (`check_drawio.py`, which judges each AWS icon by style and name, because the `mxgraph.aws4` namespace is shared with the legacy AWS18 library), and edge-reference checks are structural evidence. Opening or rendering in Draw.io and inspecting the result is visual evidence. Neither proves a deployed or secure AWS system.

## Gap fill 2026-10-18

This pass added `.apm/prompts/`, `examples/` and `templates/`, which the pack lacked, and updated `docs/PROMPT_INVENTORY.md` (new), `README.md`, `tests/capability-coverage.yml` and `tests/trigger-cases.yml` to match. Agents, skills, instructions, `apm.yml` and `compatibility/tool-permissions.yml` were not changed. Nobody was available to answer questions, so the decisions below are assumptions made on the evidence in the pack.

### Workflows and prompts

1. **Seven primary workflows.** The agent names four task types: design, reconstruction, review and export. The skills define three more workflows of their own:
   - `aws-architecture-patterns` defines pattern modeling;
   - `aws-xml-authoring` defines repair and normalization;
   - `aws-layout-and-composition` defines reflow.

   That gives seven prompts. No prompt adds a capability the skills do not describe.
2. **One prompt covers CloudFormation, CDK and Terraform.** `aws-architecture-design` treats source-derived mode as one workflow with per-format rules, so the prompt follows it. Two trigger cases (Terraform and CloudFormation) and one blocked case (CDK) point to that prompt.
3. **Every prompt names `drawio-core-generation` and `diagram-validation-and-evidence`.** The agent says to always use both. Review and export apply the core skill's output contract as the standard they check against, not as a generator.
4. **Prompts reference only installed content:** skill names and the `aws-expert-designer-contract` instruction. They do not reference `templates/`, `examples/` or the pack's former Draw.io helper in `tooling/` (removed in 1.5.0), because APM installs none of them.
5. **Approval rules in prompts are restated from the agent.** The contract instruction defines only the completion report. The approval rules (ask before changing an existing diagram, overwriting source files, publishing externally, or using credentialed AWS snapshots) live in the agent body, so the prompts restate them from there.

### Review and report vocabulary

6. **Review impact scale.** The pack defines no severity scale for findings. Reviews classify impact on interpretation as misleading, ambiguous, structural or cosmetic, plus a yes/no "blocks the stated purpose". The four words come from the skills' own failure language: false containment, ambiguous direction, structural defects and readability. This is a reporting format, not a new capability.
7. **No status vocabulary was invented.** The contract defines report sections and evidence labels but no status names, so the examples state each outcome in one plain sentence.
8. **Two label sets, kept apart.** Completion reports use only the contract's seven labels. Companion-report evidence matrices use `observed`, `inferred`, `designed` and `unresolved`, the four that `diagram-validation-and-evidence` and `aws-architecture-design` define for semantic evidence.

### Templates

9. **No handoff template.** The pack has one agent and no specialists. The contract instruction's description mentions handoff, but its body defines no handoff rules. Continuity is carried by the companion report and the completion report's `next_safe_action`, so a handoff form would have invented a contract.
10. **Skeleton boundaries are plain rectangles.** `templates/aws-diagram-skeleton.drawio` draws its boundaries as plain styled rectangles in the colors from the `aws-icons-and-visual-language` reference, not as AWS4 group shapes. The skill forbids asserting shape names that have not been checked against the installed library, and the skeleton cannot know which library a user has. Its header comment explains how to add services with names from that library. Superseded in 1.5.0: the skeleton now uses the library's group styles.
11. **The skeleton was not run through the pack's former Draw.io helper** (removed in 1.5.0). This session could not execute the helper. Instead it was reviewed by hand against that script's rules: unique IDs, resolvable parents, no edges, no `image=` paths, no legacy namespace and no compression.

### Examples

12. **Examples are synthetic.** Names, paths, CIDRs and counts are fictional. The AWS behaviors they rely on come from general knowledge and were not re-checked against current AWS documentation, because this gap fill could not browse. The behaviors are:
    - a NAT gateway is scoped to one AZ;
    - an RDS Multi-AZ standby does not serve reads;
    - Aurora storage replicates across AZs;
    - an uncached CDK context lookup needs credentials;
    - S3 Replication is one-way unless configured both ways;
    - DynamoDB global tables replicate asynchronously with last-writer-wins.

    Each example labels live and documentation checks as not-verified.
13. **Draw.io Desktop flags and paths are illustrative.** The CLI flags in the examples (`--export`, `--format`, `--page-index`, `--scale`, `--border`, `--output`) and the Windows install paths come from general knowledge. `drawio-render-export-and-review` requires detecting the executable and recording its version before use. Superseded in 1.5.0: the examples now use the options verified in the shared skill's export reference and include the Microsoft Store build in detection.

### Docs and tests

14. **`docs/SKILL_INVENTORY.md` was not created.** The gap-fill rules allow creating only the prompt inventory. The skill-to-prompt map is in `docs/PROMPT_INVENTORY.md` instead.
15. **`tests/trigger-cases.yml` gained a `prompt_file` key,** because its existing `prompt` key holds the user's request text. `tests/capability-coverage.yml` gained a `workflow_prompts` map.
16. **README build commands corrected.** They called per-pack `tooling/build_pack.py` and a `--write-report` flag that does not exist. They now call the shared tooling from the repository root.

### Gaps left open

- The contract instruction's description promises approval and handoff rules that its body does not contain. Fixing that means editing `.apm/instructions/`, which this pass may not do.
- The pack's former Draw.io helper checked ID uniqueness across the whole file. Every page of a multi-page diagram has its own root cells `0` and `1`, so the helper reported false duplicates on multi-page files, like the two-page result in `examples/repair-reflow-export-workflow.md`. This pass could not change the helper; 1.5.0 removed it.
- The pack has no `tests/test_*.py`, so trigger cases and examples are metadata, not executed behavior tests. Model behavior when the prompts are invoked is not established. (1.5.0 added `tests/test_drawio_assets.py` for the pack's draw.io files; prompt behavior is still not established.)

## Version 1.3.0: shared diagram skills (2026-10-18)

- drawio-core-generation, drawio-render-export-and-review and diagram-validation-and-evidence are now shared skills. The AWS and Azure packs had shipped two different versions of drawio-core-generation and diagram-validation-and-evidence under the same names, so whichever pack was installed last silently replaced the other's. One canonical copy now ships byte-identical in the AWS and Azure architect and designer packs and the Google Cloud architect pack, and CI fails if a copy drifts.
- The skills cover AWS, Azure and Google Cloud alone or in one diagram: each provider's current draw.io library ("AWS <year>", "Azure", "Google Cloud Platform 2026"), the legacy libraries to avoid, and each provider's network scope rules. The facts were verified on 2026-10-18 against draw.io 32.5.5 source and the providers' official icon and network pages.
- The skills now follow the master prompt's ten-part skill structure, which the previous versions did not.
- diagram-validation-and-evidence gained a standard-library checker with an icon catalog generated from draw.io's source. It validates IDs per page and reports every AWS, Azure and Google Cloud icon as current, legacy, retired or unknown.
- This pack's provider-specific skills keep setting house style. The shared skills decide which library is current and how boundaries nest.
- The shared checker validates IDs per page, so it does not repeat the false multi-page duplicates recorded above for the pack's former Draw.io helper.

## Prompt names qualified (1.4.0, 2026-10-18)

Several packs shipped prompts under the same name with different content, so installing two of them into the user profile silently replaced one pack's slash command with the other's. This pack's prompts now carry the language or provider inside the name; the qualifier is never a prefix. Slash commands change accordingly.

| Old name | New name |
|---|---|
| `repair-drawio-xml` | `repair-aws-drawio-xml` |

## Version 1.5.0: draw.io library styles and the shared checker (2026-11-01)

An independent review and a live generation test on 2026-11-01 found that this pack's own content contradicted draw.io's current AWS library and the shared draw.io skills. The shared skills were right about AWS; this release brings the pack in line with them. Finding IDs refer to that review.

- **Boundary styles come from the library (AWS-01, AWS-07, AWS-14).** `aws-visual-rules.md` gave hand-typed colours: public subnet `#248814`, private subnet `#147EBA`, "group text color matches the stroke", and a decorative Region. Those two colours are the library's label colours, not strokes, and `#147EBA` is also the Availability Zone stroke. The reference now tells the agent to copy every style from draw.io's library, restates the "AWS / Groups" palette from `Sidebar-AWS4.js` at draw.io 32.6.9 so that a drifted copy is recognisable, and sets the nesting account > Region > VPC > Availability Zone > subnet as real containers, with each subnet in exactly one Availability Zone and a Local Zone, Wavelength Zone or Outpost subnet in exactly one frame of that type. Library group styles carry `container=1`, so a decorative frame must set `container=0` explicitly; the library's Availability Zone rectangle lacks `container=1`, so the pack adds it. `aws-icons-and-visual-language`, `aws-xml-authoring`, `aws-layout-and-composition`, the prompts and the examples say the same. Fonts, sizes, badges and the legend stay the pack's house style.
- **Category containers are no longer parents (AWS-02).** The 120x120 category tile stays available as house style, but only as a decorative `container=0` sibling placed before its icon: never a parent, never an edge endpoint, never stroked or filled in a boundary colour such as the VPC purple. The skeleton and every example parent icons to their real boundary.
- **The pack-local validator was removed (AWS-03, AWS-04, AWS-11).** The former helper in `tooling/` passed AWS17, AWS18, AWS 3D, retired and invented icons, failed valid Azure icons, reported false duplicates on multi-page files and did not refuse DOCTYPE declarations. It was removed from this pack and from the AWS Cloud Architect pack. Skills, prompts, examples, templates and the README now name `check_drawio.py --strict` from `diagram-validation-and-evidence`, and the examples report its exit code, icon counts and catalog version instead of a namespace check. New-diagram, repair, reflow and export workflows use `--strict`; the default mode is kept only for a diagram that must keep a legacy icon set, and its warnings are reported.
- **Skeleton and fixture rebuilt (AWS-06, AWS-13).** `templates/aws-diagram-skeleton.drawio` and `tests/fixtures/minimal.drawio` were generated from the exact palette strings in `Sidebar-AWS4.js` (full icon styles with the category `fillColor`, `strokeColor` and bottom label, and the library group styles), with only typography changed. The skeleton adds an AWS account frame, sample icons (internet gateway, NAT gateways, EC2 instances, Amazon S3 in the Region outside the VPC), and a decorative auxiliary frame whose icons are parented to the Region. The fixture's edge now runs from Amazon S3 to AWS Lambda, the direction in which S3 event notifications flow, and its icons are 48x48 inside an account and a Region.
- **Rendering (AWS-08, AWS-09, AWS-15).** Renderer detection now includes the Microsoft Store build: `app\draw.io.exe` inside the InstallLocation that `Get-AppxPackage *draw.io*` reports, or, without PowerShell, the package that `reg query "HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages" | findstr draw.io` names under `C:\Program Files\WindowsApps\`. Exports use `-x -k`, SVG adds `--embed-svg-images`, review exports never use `--layout` or `--normalize`, and every prompt completes `diagram-validation-and-evidence` after the render.
- **Other providers (AWS-10).** Azure and Google Cloud components use their own provider's current library, as `drawio-core-generation` describes. Only custom applications, teams and third-party systems get labelled neutral shapes.
- **Application Load Balancer icon (AWS-12).** The examples use the `application_load_balancer` resource icon.
- **Regression guard.** `tests/test_drawio_assets.py` runs the shared checker in strict mode on every `.drawio` file in the pack. It fails on boundaries drawn without the library group styles, recoloured group styles, nesting other than account > Region > VPC > Availability Zone > subnet, a cell parented to anything but a boundary container, AWS icons without the palette `fillColor` or bottom label, an unlabelled edge, an AWS icon outside every Region frame other than an external actor, any mention of the removed validator, and visual rules that lose the library values. The same file ships in the AWS Cloud Architect pack.
- **The shared draw.io skills changed with this release.** `drawio-core-generation`, `diagram-validation-and-evidence` and `drawio-render-export-and-review` are maintained once for every diagram pack and ship byte-identical in this one, so 1.5.0 ships their updated copies. The icon catalog is rebuilt from draw.io 32.6.9 and records every palette entry's full style, and `check_drawio.py --find "<product>"` prints the style to copy. The checker gained new errors: an AWS or Google Cloud icon whose palette `fillColor` is missing, or whose palette colour is set to `none`, draws incompletely; an AWS name used in the wrong form (a service name as a bare stencil, or a resource or group name inside `resourceIcon`) draws without its square or on a square AWS never published; an Azure path in the palette's wrong letter case draws a broken image. A recoloured icon, or a missing `strokeColor` where the palette sets one, is a warning, and an error with `--strict`. A diagram that passed the 1.4.0 checker can therefore fail with 1.5.0; fix it by copying the style `--find` prints. The checker also reports an Azure file that `diagram-validation-and-evidence/scripts/icon_preferences.json` marks superseded (the pre-rename Azure Active Directory pyramid `identity/Azure_Active_Directory.svg` and the older `networking/Private_Endpoint.svg`) as a warning, or an error with `--strict`, naming the file to use; treats a colour where the palette sets `none`, such as a filled AWS boundary, as recolouring; and refuses a compressed page that inflates past 10 MB. `--find` lists a product's preferred file first and superseded files last.
- **Skeleton follow-up (pre-PR review F6, 2026-11-01).** Edge `edge_nat_b_igw` had no label while its twin read "to the internet"; both now carry it. Amazon S3 was already parented to the Region, outside the VPC, but stood unconnected. It is now reached from both private subnets through an S3 gateway endpoint drawn in the VPC, outside every Availability Zone and subnet: AWS documents a gateway endpoint as a gateway you specify in your route table, without AWS PrivateLink and without a NAT device, whereas an interface endpoint is network interfaces with private IP addresses from subnets and would be drawn in its subnet (sources in `SOURCE_TRACEABILITY.md`, read 2026-11-01). The edges read "to Amazon S3" and "bypasses NAT". Subnets narrowed to 300 and the Region and account widened by 40 to make room for the endpoint column. The styles were regenerated from the palette strings, and each was checked against the 32.6.9 catalog style that `--find` prints (the catalog omits connection points).
- **Skill description.** `aws-icons-and-visual-language` no longer advertises category containers. `tests/skill-coverage.yml` is generated from skill descriptions and must be regenerated with `tooling/skill_coverage.py aws-expert-designer-pack`.
- **Source traceability.** The AWS icon page is no longer credited with usage guidance it does not carry, and `Sidebar-AWS4.js` is recorded as the source of the group and icon styles.

Evidence, 2026-11-01, local, run with the shared checker this release ships:

- `check_drawio.py --strict`, this pack's copy, reporting `catalog: draw.io 32.6.9, built 2026-11-01`: the skeleton passes with 17 AWS icons and groups current, 0 errors and 0 warnings (25 vertices, 8 edges); the fixture passes with 4 current, 0 errors and 0 warnings.
- draw.io Desktop 32.6.1, the Microsoft Store build, rendered both files with `-x -k -f png`. Every icon and group drew its symbol. The first skeleton render showed an edge running through the internet gateway's label and an edge label sitting on the account border; both were fixed and the second render was clean. After the F6 follow-up, the first render showed the "bypasses NAT" label covering the VPC border; the Region was widened, and the final render is clean, with every edge labelled and Amazon S3 between the VPC and the Region border.
- `tooling/validate_pack.py` and the pack tests: see `VALIDATION_REPORT.md`.

Not verified:

- The catalog is built from draw.io 32.6.9 and the renders used Desktop 32.6.1, which is older. Every name the skeleton and fixture use is current in the 32.6.9 catalog and drew completely in 32.6.1; a name draw.io added after 32.6.1 could pass the checker and still not draw in that Desktop build.
- Decorative category tiles were not rendered; the live generation test and these renders used 48x48 icons without tiles.
- Model behaviour when the prompts run is not established.
