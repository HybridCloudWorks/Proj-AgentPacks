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

XML parsing, schema checks, icon namespace checks, and edge-reference checks are structural evidence. Opening or rendering in Draw.io and inspecting the result is visual evidence. Neither proves a deployed or secure AWS system.

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
4. **Prompts reference only installed content:** skill names and the `aws-expert-designer-contract` instruction. They do not reference `templates/`, `examples/` or the pack's `tooling/validate_drawio_xml.py`, because APM installs none of them.
5. **Approval rules in prompts are restated from the agent.** The contract instruction defines only the completion report. The approval rules (ask before changing an existing diagram, overwriting source files, publishing externally, or using credentialed AWS snapshots) live in the agent body, so the prompts restate them from there.

### Review and report vocabulary

6. **Review impact scale.** The pack defines no severity scale for findings. Reviews classify impact on interpretation as misleading, ambiguous, structural or cosmetic, plus a yes/no "blocks the stated purpose". The four words come from the skills' own failure language: false containment, ambiguous direction, structural defects and readability. This is a reporting format, not a new capability.
7. **No status vocabulary was invented.** The contract defines report sections and evidence labels but no status names, so the examples state each outcome in one plain sentence.
8. **Two label sets, kept apart.** Completion reports use only the contract's seven labels. Companion-report evidence matrices use `observed`, `inferred`, `designed` and `unresolved`, the four that `diagram-validation-and-evidence` and `aws-architecture-design` define for semantic evidence.

### Templates

9. **No handoff template.** The pack has one agent and no specialists. The contract instruction's description mentions handoff, but its body defines no handoff rules. Continuity is carried by the companion report and the completion report's `next_safe_action`, so a handoff form would have invented a contract.
10. **Skeleton boundaries are plain rectangles.** `templates/aws-diagram-skeleton.drawio` draws its boundaries as plain styled rectangles in the colors from the `aws-icons-and-visual-language` reference, not as AWS4 group shapes. The skill forbids asserting shape names that have not been checked against the installed library, and the skeleton cannot know which library a user has. Its header comment explains how to add services with names from that library.
11. **The skeleton was not run through `tooling/validate_drawio_xml.py`.** This session could not execute the helper. Instead it was reviewed by hand against that script's rules: unique IDs, resolvable parents, no edges, no `image=` paths, no legacy namespace and no compression.

### Examples

12. **Examples are synthetic.** Names, paths, CIDRs and counts are fictional. The AWS behaviors they rely on come from general knowledge and were not re-checked against current AWS documentation, because this gap fill could not browse. The behaviors are:
    - a NAT gateway is scoped to one AZ;
    - an RDS Multi-AZ standby does not serve reads;
    - Aurora storage replicates across AZs;
    - an uncached CDK context lookup needs credentials;
    - S3 Replication is one-way unless configured both ways;
    - DynamoDB global tables replicate asynchronously with last-writer-wins.

    Each example labels live and documentation checks as not-verified.
13. **Draw.io Desktop flags and paths are illustrative.** The CLI flags in the examples (`--export`, `--format`, `--page-index`, `--scale`, `--border`, `--output`) and the Windows install paths come from general knowledge. `drawio-render-export-and-review` requires detecting the executable and recording its version before use.

### Docs and tests

14. **`docs/SKILL_INVENTORY.md` was not created.** The gap-fill rules allow creating only the prompt inventory. The skill-to-prompt map is in `docs/PROMPT_INVENTORY.md` instead.
15. **`tests/trigger-cases.yml` gained a `prompt_file` key,** because its existing `prompt` key holds the user's request text. `tests/capability-coverage.yml` gained a `workflow_prompts` map.
16. **README build commands corrected.** They called per-pack `tooling/build_pack.py` and a `--write-report` flag that does not exist. They now call the shared tooling from the repository root.

### Gaps left open

- The contract instruction's description promises approval and handoff rules that its body does not contain. Fixing that means editing `.apm/instructions/`, which this pass may not do.
- `tooling/validate_drawio_xml.py` checks ID uniqueness across the whole file. Every page of a multi-page diagram has its own root cells `0` and `1`, so the helper reports false duplicates on multi-page files, like the two-page result in `examples/repair-reflow-export-workflow.md`. This pass may not change the helper.
- The pack has no `tests/test_*.py`, so trigger cases and examples are metadata, not executed behavior tests. Model behavior when the prompts are invoked is not established.

## Version 1.3.0: shared diagram skills (2026-10-18)

- drawio-core-generation, drawio-render-export-and-review and diagram-validation-and-evidence are now shared skills. The AWS and Azure packs had shipped two different versions of drawio-core-generation and diagram-validation-and-evidence under the same names, so whichever pack was installed last silently replaced the other's. One canonical copy now ships byte-identical in the AWS and Azure architect and designer packs and the Google Cloud architect pack, and CI fails if a copy drifts.
- The skills cover AWS, Azure and Google Cloud alone or in one diagram: each provider's current draw.io library ("AWS <year>", "Azure", "Google Cloud Platform 2026"), the legacy libraries to avoid, and each provider's network scope rules. The facts were verified on 2026-10-18 against draw.io 32.5.5 source and the providers' official icon and network pages.
- The skills now follow the master prompt's ten-part skill structure, which the previous versions did not.
- diagram-validation-and-evidence gained a standard-library checker with an icon catalog generated from draw.io's source. It validates IDs per page and reports every AWS, Azure and Google Cloud icon as current, legacy, retired or unknown.
- This pack's provider-specific skills keep setting house style. The shared skills decide which library is current and how boundaries nest.
- The shared checker validates IDs per page, so it does not repeat the false multi-page duplicates recorded above for `tooling/validate_drawio_xml.py`.

## Prompt names qualified (1.4.0, 2026-10-18)

Several packs shipped prompts under the same name with different content, so installing two of them into the user profile silently replaced one pack's slash command with the other's. This pack's prompts now carry the language or provider inside the name; the qualifier is never a prefix. Slash commands change accordingly.

| Old name | New name |
|---|---|
| `repair-drawio-xml` | `repair-aws-drawio-xml` |
