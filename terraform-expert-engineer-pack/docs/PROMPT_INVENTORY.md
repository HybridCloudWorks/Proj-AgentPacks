# Prompt inventory

There are eleven prompts in `.apm/prompts/`, one per primary workflow. Nine come from the agent's Skill routes; the state Skill contributes two, migration and import, because they have different inputs and gates. The last two, implement and review, come from the agent's operating contract. Every prompt targets `terraform-expert-engineer`, names the Skills it applies, and ends with a completion report under the always-on `terraform-expert-engineer-contract` instruction.

| Prompt | Skills applied | Expected output |
|---|---|---|
| implement-terraform-change.prompt.md | terraform-core-and-style, terraform-testing-and-validation; routes to the others by what the change touches | Diff, commands and results, plan summary with every replace or destroy named, limits of each check. Diagnose-only requests stop at the cause. |
| review-terraform-change.prompt.md | terraform-core-and-style, plus the Skills the diff calls for | Read-only, severity-ordered findings with file and line, plan impact, checks actually run, what was not reviewed. |
| refactor-terraform-module.prompt.md | terraform-modules-and-refactoring, terraform-core-and-style, terraform-testing-and-validation, terraform-state-backends-and-imports for state-only moves | Diff with `moved` blocks, address map, per-environment plans with no unintended replace or destroy, release label, migration notes. |
| migrate-terraform-state.prompt.md | terraform-state-backends-and-imports, terraform-cloud-and-stacks for HCP workspaces | Backend diff, migration record, pre-checks, authorization request; verification only after an authorized run. |
| import-terraform-resources.prompt.md | terraform-state-backends-and-imports, terraform-core-and-style, terraform-modules-and-refactoring | `import` blocks, cleaned configuration, object-to-address map, a pure-import plan, drift reconciliation. |
| add-terraform-tests.prompt.md | terraform-testing-and-validation, terraform-ci-cd-and-quality when wiring CI | Test files, results per test mode, mock limits, cleanup status; unrun tests reported as unrun. |
| author-terraform-policy.prompt.md | terraform-policy-and-governance, terraform-cloud-and-stacks, terraform-ci-cd-and-quality | Policy and tests, non-equivalent constructs listed, runner results or their absence, enforcement map. |
| build-terraform-pipeline.prompt.md | terraform-ci-cd-and-quality, terraform-testing-and-validation, terraform-policy-and-governance, terraform-cloud-and-stacks | Pipeline diff, stage table of what each stage proves, job identities, plan artifact handling, apply gate. |
| design-hcp-terraform-workflow.prompt.md | terraform-cloud-and-stacks, terraform-state-backends-and-imports, terraform-policy-and-governance | Workspace or Stack configuration, run flow and permissions, credential plan, linked-output contracts, static versus live labels. |
| develop-terraform-provider.prompt.md | terraform-provider-development, terraform-testing-and-validation | Go diff, schema summary, commands and results, acceptance test status, release-readiness notes. |
| review-terraform-avm-module.prompt.md | azure-verified-modules, terraform-core-and-style, terraform-modules-and-refactoring, terraform-testing-and-validation | Requirement table (pass, fail, not applicable, unable to verify), located findings, what lies outside AVM style; never a certification claim. |

## Skill coverage

| Skill | Prompts |
|---|---|
| terraform-core-and-style | implement-terraform-change, review-terraform-change |
| terraform-modules-and-refactoring | refactor-terraform-module |
| terraform-state-backends-and-imports | migrate-terraform-state, import-terraform-resources |
| terraform-cloud-and-stacks | design-hcp-terraform-workflow |
| terraform-testing-and-validation | add-terraform-tests |
| terraform-policy-and-governance | author-terraform-policy |
| terraform-ci-cd-and-quality | build-terraform-pipeline |
| terraform-provider-development | develop-terraform-provider |
| azure-verified-modules | review-terraform-avm-module |

The same mapping is in `tests/capability-coverage.yml` (`prompt_map`). `tests/trigger-cases.yml` (`workflow_prompt`) links each trigger case to its prompt.

## Names

Every prompt name contains "terraform". At user scope, prompts from different packs share one command namespace, so generic names such as `review-change` would collide.

## How the prompts install

These facts come from the verified vendor notes for APM 0.33.0. They were not re-observed during the gap fill.

- APM ships commands as prompts. Copilot receives them as prompt files, and the `agent` key is honoured there.
- Claude Code receives them as commands. APM drops the `agent` key with a warning, because Claude commands support only `description`, `input`, `allowed-tools`, `model` and `argument-hint`. The prompt still works; the user picks the agent.
- At user scope (`apm install -g`), Copilot receives prompts and instructions, and Codex receives no prompts. Codex users invoke `terraform-expert-engineer` directly.
- Gemini CLI and Kiro prompt deployment is not recorded in the verified notes, so it is not established here.
