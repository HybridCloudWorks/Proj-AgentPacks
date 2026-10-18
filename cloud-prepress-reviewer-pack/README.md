# Cloud Pre-Press Reviewer Pack

Portable Agent/Skill package for the review boundary between implementation/build completion and pull-request or deployment approval. It consolidates the supplied code reviewer, architecture reviewer, security engineer, allocation/policy, onboarding, validation, role-verification, plan-review, error, and repository-contract references into a thin reviewer Agent with focused Skills.

## Primary downloads

- `dist/cloud-prepress-reviewer-pack.zip` — complete source, vendor targets, hooks, tools, tests, and archives.
- `dist/cloud-prepress-reviewer-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/cloud-prepress-reviewer-prompt.zip` — reusable pack-authoring prompt.
- `dist/cloud-prepress-reviewer-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `cloud-prepress-reviewer-skills.zip`.

## Workflow prompts

One prompt per primary workflow, in `.apm/prompts/`. Each targets the `cloud-prepress-reviewer` agent, names the skills it applies, and follows the always-on `cloud-prepress-reviewer-contract` instruction. `docs/PROMPT_INVENTORY.md` maps every prompt to its skills, expected output and worked example.

| Prompt | Use it when |
|---|---|
| `review-before-pr.prompt.md` | A built application or mixed change is about to become a pull request |
| `review-before-deployment.prompt.md` | A Terraform, Bicep, ARM, AZD, policy or RBAC change is heading for deployment review |
| `review-deployment-preview.prompt.md` | A captured plan, what-if or azd preview needs interpreting against the change |
| `review-security-and-supply-chain.prompt.md` | Secrets, identity, trust boundaries, dependencies or CI need a security gate |
| `check-architecture-alignment.prompt.md` | The change must be compared with the approved topology, constraints and ADRs |
| `assess-operability-rollback-and-cost.prompt.md` | Rollback boundary, recovery, cost, tags or policy exceptions need checking before deployment |
| `verify-handoff-readiness.prompt.md` | The next actor needs a complete, safe handoff |
| `validate-review-report.prompt.md` | The pre-review inventory and post-review report validation should run around a review |

## Examples and templates

`examples/` holds worked reviews that between them reach all five recommendations. Each ends with a completion report in the contract's format. The repositories, identities and figures are fictional.

| Example | Outcome |
|---|---|
| `examples/application-pre-pr-review.md` | `CHANGES_REQUIRED`: swallowed exception and missing idempotency key in a queue consumer |
| `examples/terraform-pre-deployment-review.md` | `READY_FOR_DEPLOYMENT_REVIEW`: module move with a `moved` block, plan bound to the reviewed commit |
| `examples/bicep-keyvault-not-verified.md` | `NOT_VERIFIED`: Key Vault permission-model switch with no authorized what-if or live read |
| `examples/architecture-drift-blocked.md` | `BLOCKED_ON_HUMAN_DECISION`: a second data store that contradicts accepted ADRs |
| `examples/ci-supply-chain-security-review.md` | `CHANGES_REQUIRED`: `pull_request_target` running fork code with a deployment identity |
| `examples/hooks-and-report-validation.md` | `READY_FOR_PR`: inventory limits and a report corrected until post-review validation passes |

`templates/` holds the documents the skills produce. These are for people; they are not installed with the pack.

| Template | Produced by |
|---|---|
| `templates/review-report.md` | review-report-and-pr-gate: the completion report, saved as `REVIEW.md` |
| `templates/engineer-handoff.md` | role-authority-and-handoff-review: a handoff that travels separately from the report |
| `templates/evidence-ledger.md` | azure-evidence-and-mcp-review: labelled evidence for drift-prone or gate-deciding claims |
| `templates/deployment-preview-record.md` | deployment-preview-and-environment-review: one record per plan, what-if or azd preview |
| `templates/cost-and-governance-record.md` | cost-allocation-and-governance-review: cost assumptions, allocation controls, policy exceptions |
| `templates/rollback-readiness.md` | operability-resilience-and-rollback-review: operating readiness, rollout and rollback boundary |

## Build and validate

Run from the pack repository root. The validation and build tooling is shared there and is not copied into the pack.

```text
python tooling/build_pack.py
python tooling/validate_pack.py cloud-prepress-reviewer-pack --install-check
```

Use `hooks/pre-review.*` before analysis and `hooks/post-review.*` after the report is written. The hooks and tools are non-mutating. They do not prove a live Azure deployment, policy compliance, plan/apply result, cost estimate, recovery result, or PR approval.

## Review boundary

This pack reviews the built result. It does not implement fixes, replace architecture design, run deployment commands, or merge/publish a PR. It returns a recommendation and a handoff that another authorized actor can act on.

## Official evidence

Prefer current Microsoft Learn, Azure Policy, Bicep/ARM, Azure Developer CLI, Terraform/AVM, and official Azure MCP evidence. Use current documentation for version-sensitive behavior, API versions, policy effects, limits, provider/module requirements, and preview semantics. Record sources and retrieval dates when claims materially affect the gate.
