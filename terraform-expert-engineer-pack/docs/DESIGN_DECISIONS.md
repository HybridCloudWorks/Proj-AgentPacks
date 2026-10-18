# Design Decisions

## Broad trigger, narrow Skills

Terraform and Terraform-based IaC should route to this Agent broadly. Detailed procedures remain in nine Skills so a normal HCL edit does not load HCP Stacks, policy conversion, provider Go, and AVM certification guidance at once.

## Main Terraform first

The pack prioritizes Terraform language, modules, state, tests, CI/CD, and plan safety. HCP Terraform/Enterprise, Stacks, policy, provider development, and AVM are included because the supplied sources and user request identify them as high-value adjacent HCL products. Individual provider-specific cloud recipes were not promoted to separate Skills.

## State is a first-class boundary

S3 and Azure Storage are treated as distinct backend choices with locking, access, versioning/recovery, identity, migration, and sensitivity considerations. HCP Terraform state is treated as a workspace-controlled product boundary, not as a synonym for local CLI workspaces.

## Version-sensitive material

Terraform Search, mock providers, Stacks syntax, tfpolicy, provider framework behavior, AVM requirements, and backend locking details can change. Skills route to current official documentation and require checking the installed version before making exact claims.

## Source versus additions

The Agent, core style, modules, state, Stacks, tests, policies, provider development, CI/CD, and AVM content are source-derived and consolidated. The explicit routing/evidence contract and the pack-level gap closure around backend/security/state safety are editorial additions needed to make the expert complete and portable.

## Gap fill 2026-10-18

The pack shipped without `.apm/prompts/`, `examples/` or `templates/`. They were authored from the existing agent, the nine Skills and the contract instruction. None of those changed, and neither did `apm.yml` or `compatibility/tool-permissions.yml`.

### Prompts

- **Eleven prompts, one per primary workflow.** The agent routes to nine Skills. The state Skill defines two workflows with different inputs and gates, a migration gate and import, so each has its own prompt. The agent's operating contract adds two cross-cutting workflows: implement a change, and review a change with its plan. That puts the count one over the usual 5 to 10, but merging either pair would blur an authorization boundary (a review is read-only; an import writes state).
- **Troubleshooting is folded into `implement-terraform-change`.** The error classification from terraform-core-and-style is a step there, not a separate prompt. A diagnose-only request stops at the cause, which keeps the "analysis is not implementation" boundary without a twelfth prompt.
- **Every prompt targets `terraform-expert-engineer`,** the only agent.
- **Every prompt name contains "terraform".** Prompts become user-scope commands, and the repository holds other packs whose generic names (review, implement) would collide.
- **Prompts reference only installed content:** Skill names and the contract instruction by name. They describe the completion report rather than pointing at `templates/`, because templates are not installed.
- **Prompts state no status tokens.** The contract and `tests/report-contract.yml` define none, and the validator rejects undefined ones. Outcomes are written in plain words.

### Examples

- **Seven examples:** refactor, state migration, import, tests, CI/CD, policy conversion and AVM review. They favour the "main Terraform first" workflows from this file, and the adjacent products the trigger cases name.
- **The blocked outcome** is `state-migration-blocked.md`. The test, CI, policy and AVM examples each also leave something unverified, and say so.
- **All examples are synthetic.** Account and subscription IDs, bucket names, commits and versions are illustrative. Commands and outputs show what the agent would run and see. Nothing in them was executed during the gap fill, and every example says so.
- **Version-sensitive details are tied to "the installed version" rather than a release number:** S3 lockfile locking, `for_each` in `import` blocks, `mock_provider`, Terraform Search, and azurerm container import IDs. This follows the Skills' instruction to check the installed version, and avoids stating release facts that could not be verified offline.
- **The policy example writes no tfpolicy syntax.** The Skill says tfpolicy syntax is version-sensitive and must be checked with the installed runner. The example follows the target repository's existing policies, and reports the tests as not run. The Sentinel excerpt is trimmed to constructs that are stable.
- **HCP Terraform/Stacks and provider development have prompts but no worked example.** Recorded as a gap.

### Templates

- **The six templates are the records the Skills and contract require.** The completion report comes from the contract. The plan review comes from the agent's plan-review list and the CI apply gate. The state migration record comes from the migration gate. The state address map comes from the refactor and import rules. The AVM requirement review comes from the AVM Skill's result categories.
- **The approval handoff stands in for a specialist handoff.** The pack has a single agent, so there is no specialist to hand off to. What the agent does hand off is a gated operation, to the human who can authorize it. The template is built from the agent's "ask before" list.
- **Evidence classes are defined in `templates/completion-report.md`.** The contract names static, local, live-cloud, inferred and unavailable, but does not define them. The definitions in the template are an assumption: local means executed on the machine without reading live cloud, backend or HCP state; live-cloud means it read or changed real cloud, backend or HCP state.

### Other files

- **`docs/SKILL_INVENTORY.md` was not created.** The gap-fill rules allow creating only `docs/PROMPT_INVENTORY.md`. The Skill-to-prompt mapping lives there instead, and in `tests/capability-coverage.yml` (`prompt_map`).
- **Trigger cases.** `tests/trigger-cases.yml` gained a `workflow_prompt` field, because `prompt` already holds the user utterance. Three cases were added, for the prompts that had none: `configuration-change`, `import` and `ci-pipeline`. Before this, terraform-ci-cd-and-quality had no trigger case at all.
- **README.** The README's build and validate commands named a pack-local `tooling/` and a `--write-report` flag, and neither exists. They now point at the shared tooling at the repository root, in the same form other packs use.
- **Prompt install behaviour.** `docs/PROMPT_INVENTORY.md` uses the verified APM 0.33.0 notes. A scratch `apm install` to observe it directly was not permitted in this session, so Gemini CLI and Kiro prompt deployment is recorded as not established.
