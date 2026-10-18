# Terraform Expert Engineer Pack

Portable Agent/Skill package for Terraform and HCL-based infrastructure engineering. It covers ordinary Terraform configuration and module work, plus the high-value products and workflows around it: remote state, S3 and Azure Storage backends, HCP Terraform/Enterprise, Terraform Stacks, policy, tests, provider development, CI/CD, and Azure Verified Modules.

## What is in the pack

- `apm.yml` and `.apm/`: the canonical source. One agent (`terraform-expert-engineer`), nine Skills, the always-on `terraform-expert-engineer-contract` instruction, and eleven prompts. Every vendor file is generated from here.
- `docs/`: design decisions, official sources, source traceability, and the prompt inventory.
- `compatibility/`: capability map, compatibility matrix, vendor sources, and `tool-permissions.yml`.
- `examples/`: seven worked walkthroughs, each ending in a completion report.
- `templates/`: six reusable records the agent produces.
- `hooks/`: a README only; the pack ships no native hooks.
- `tests/`: skill coverage (generated), capability coverage, trigger cases, report contract, version sensitivity.

## Workflows

Each prompt runs one primary workflow through the primary agent. The prompts install as Copilot prompt files and as Claude Code commands. See `docs/PROMPT_INVENTORY.md` for the Skills each prompt applies and for install behaviour.

| Prompt | Use it to |
|---|---|
| `implement-terraform-change` | change or fix configuration, validate it and review the plan |
| `review-terraform-change` | review a diff and its plan, read-only |
| `refactor-terraform-module` | restructure a module with `moved` blocks and no recreation |
| `migrate-terraform-state` | design a backend and prepare a gated state migration |
| `import-terraform-resources` | adopt existing resources with `import` blocks |
| `add-terraform-tests` | add mocked, plan-mode and gated apply-mode tests |
| `author-terraform-policy` | write, convert or test Sentinel and tfpolicy controls |
| `build-terraform-pipeline` | build CI/CD with ordered gates and a protected apply |
| `design-hcp-terraform-workflow` | design HCP Terraform workspaces, run flow and Stacks |
| `develop-terraform-provider` | build a provider with the Plugin Framework |
| `review-terraform-avm-module` | check a module against Azure Verified Modules requirements |

## Examples

Synthetic walkthroughs. Their commands and outputs are illustrative, not recorded results.

| Example | Workflow | Outcome shown |
|---|---|---|
| `examples/module-refactor-workflow.md` | refactor | plan review catches a destroy; pure moves after the fix |
| `examples/state-migration-blocked.md` | state migration | blocked: recovery unverified, state write not authorized |
| `examples/import-resources-workflow.md` | import | pure-import plan; a security finding deferred to its own change |
| `examples/terraform-test-workflow.md` | testing | mocked tests pass; integration test written, not run |
| `examples/ci-pipeline-workflow.md` | CI/CD | workflow linted locally; never run on GitHub |
| `examples/policy-conversion-workflow.md` | policy | conversion with non-equivalences flagged; tests not run |
| `examples/avm-module-review-workflow.md` | AVM review | read-only requirement table; no certification claim |

## Templates

| Template | Record |
|---|---|
| `templates/completion-report.md` | the contract's eight-section completion report, with evidence classes |
| `templates/approval-handoff.md` | a request for authorization before apply, state mutation, force-unlock or other gated work |
| `templates/plan-review.md` | what a plan does, what it is tied to, and whether it is ready for an apply request |
| `templates/state-migration-record.md` | the migration gate fields required before a backend change |
| `templates/state-address-map.md` | address moves for refactors, and object-to-address bindings for imports |
| `templates/avm-requirement-review.md` | AVM requirement results kept apart from correctness and certification |

The templates and examples are for people reading the pack. They are not installed. The installed agent follows the contract instruction, which carries the same report sections.

## Primary downloads

- terraform-expert-engineer-pack.zip - complete source and generated vendor files.
- terraform-expert-engineer-canonical.zip - APM-friendly canonical source.
- terraform-expert-engineer-prompt.zip - reusable authoring prompt.
- terraform-expert-engineer-validation.zip - uppercase VALIDATION_REPORT.md.

Also generated: vendor packages generated at build time and one individual skill.zip archive per Skill, collected in terraform-expert-engineer-skills.zip.

## Build and validate

Validation and build tooling is shared at the repository root. From this pack's folder:

    python ../tooling/validate_pack.py . --install-check   # writes VALIDATION_REPORT.md
    python ../tooling/build_pack.py .

The build is deterministic. Static validation does not prove a live Terraform plan, HCP Terraform run, cloud API call, state lock, policy enforcement, provider acceptance test, AVM certification, or production safety.

## Design boundary

The supplied sources include duplicate agents, duplicate AVM guidance, overlapping Terraform style and testing material, policy author/test agents, Terraform Stacks examples, import/search examples, provider scaffolding, CI references, and cloud-specific Terraform guidance. The pack preserves the distinct capabilities, folds examples into focused procedures, and avoids creating low-value Skills for each individual attachment.
