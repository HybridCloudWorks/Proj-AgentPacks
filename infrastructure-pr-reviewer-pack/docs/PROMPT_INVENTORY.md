# Prompt inventory

Seven prompts in `.apm/prompts/`, one per primary workflow of the `review-infrastructure-pr` and `verify-infrastructure-evidence` Skills. Every prompt names `infrastructure-pr-reviewer` as its agent, applies the full changed-line protocol, and returns the report defined by the `infrastructure-pr-reviewer-contract` instruction.

| Prompt | Workflow | Skills applied | Expected output | Worked example |
|---|---|---|---|---|
| review-infrastructure-pull-request.prompt.md | Complete review of a PR or diff | `review-infrastructure-pr`, matching technology Skills, `verify-infrastructure-evidence` | Full report: coverage, line-anchored findings, evidence gaps, residual risk, disposition, handoff | `examples/kustomize-gitops-prune-blocked-review.md` |
| re-review-infrastructure-pull-request.prompt.md | Re-review after a new push | `review-infrastructure-pr` (Re-review), technology Skills for newly changed lines, `verify-infrastructure-evidence` | Full report with each earlier Finding ID's status at the new head | `examples/ansible-rollout-re-review.md` |
| assess-existing-environment-impact.prompt.md | Identity, ownership, replacement and deletion against existing state | `review-infrastructure-pr`, `review-terraform-opentofu`, `review-bicep-arm`, `review-kubernetes-packaging`, `review-ansible-automation`, `review-powershell-automation`, `verify-infrastructure-evidence` | Full report naming targets and state considered, and the existing-state evidence required | `examples/terraform-count-to-for-each-review.md` |
| review-deployment-pipeline.prompt.md | CI/CD trust boundary, identity, conditions, concurrency and artifact provenance | `review-infrastructure-pr`, `review-cicd-deployment`, technology Skills for invoked tools, `verify-infrastructure-evidence` | Full report with event-to-job trust map and artifact chain | `examples/github-actions-plan-trust-review.md` |
| trace-cross-tool-handoffs.prompt.md | Multi-tool execution chain and every boundary in it | `review-infrastructure-pr` and each technology Skill in the chain, `verify-infrastructure-evidence` | Full report with the execution sequence and each handoff's result | `examples/bicep-powershell-ansible-chain-review.md` |
| verify-review-evidence.prompt.md | Safe local checks and artifact integrity | `verify-infrastructure-evidence`, `review-infrastructure-pr` | Full report with checks executed and skipped, and an integrity verdict per artifact | `examples/bicep-diagnostics-evidence-review.md` |
| request-review-evidence.prompt.md | Risk-proportional evidence request before or during review | `review-infrastructure-pr` (PR template asset), `verify-infrastructure-evidence` (evidence matrix) | Full report with each requested artifact under Evidence Gaps and a drafted request under Handoff | Handoff of `examples/kustomize-gitops-prune-blocked-review.md` |

## Skills to prompts

There is no separate skill inventory; this table maps every shipped Skill to the prompts that apply it.

| Skill | Prompts |
|---|---|
| `review-infrastructure-pr` | all seven |
| `review-terraform-opentofu` | review-infrastructure-pull-request, assess-existing-environment-impact, review-deployment-pipeline, trace-cross-tool-handoffs |
| `review-bicep-arm` | review-infrastructure-pull-request, assess-existing-environment-impact, review-deployment-pipeline, trace-cross-tool-handoffs |
| `review-powershell-automation` | review-infrastructure-pull-request, assess-existing-environment-impact, trace-cross-tool-handoffs |
| `review-ansible-automation` | review-infrastructure-pull-request, assess-existing-environment-impact, trace-cross-tool-handoffs |
| `review-cicd-deployment` | review-infrastructure-pull-request, review-deployment-pipeline, trace-cross-tool-handoffs |
| `review-kubernetes-packaging` | review-infrastructure-pull-request, assess-existing-environment-impact, trace-cross-tool-handoffs |
| `verify-infrastructure-evidence` | all seven |

`re-review-infrastructure-pull-request` applies whichever technology Skills match the newly changed lines, so it is left out of the technology rows.

Technology Skills have no prompt of their own. Each returns findings to `review-infrastructure-pr` and does not write a report, and a single-technology review would leave other changed lines without a disposition.

## How the prompts install

APM honours the `agent` field for GitHub Copilot and drops it, with a warning, when it generates Claude Code commands. A user-scope APM install delivers prompts to Copilot and Claude Code and none to Codex. What Gemini CLI and Kiro receive from prompts is not recorded in the verified vendor facts; check the `apm install` output for those targets. Users of a client without prompts invoke `infrastructure-pr-reviewer` directly with the same request.

Prompts reference only installed content: Skill names, files inside those Skills (`assets/`, `references/`, `scripts/`), and the contract instruction by name. They never point at `examples/`, `templates/` or `docs/`.
