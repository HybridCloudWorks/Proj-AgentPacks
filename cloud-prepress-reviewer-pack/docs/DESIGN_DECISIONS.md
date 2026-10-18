# Design Decisions

## Reviewer boundary

The Agent sits after implementation/build and before pull-request or deployment approval. It reviews and reports; it does not implement fixes, merge, publish, or mutate cloud state.

## Thin router, focused review Skills

The supplied files repeat code review, architecture review, security, policy, onboarding, validation, role verification, and error guidance. They were consolidated into focused Skills so a routine review does not load unrelated cloud, security, or deployment material.

## Evidence and severity discipline

Findings must be grounded in a file, line, diff, test, preview, or authorized read-only observation. Confirmed defects, validation hypotheses, accepted risks, human blockers, skipped checks, and not-verified evidence are distinct. Severity is tied to impact and trigger, not reviewer preference.

## Safe automation

Pre-review inventory and post-review report validation are deterministic, non-mutating helpers. They do not run `apply`, `deploy`, `delete`, `force-unlock`, identity/policy changes, PR publication, or live queries without explicit authorization.

## Azure preview and policy

The reviewer recognizes Bicep `validate`/`what-if`, AZD preview, Terraform plan, and Azure Policy evidence as bounded evidence. It does not treat a plan or what-if as a successful deployment or live compliance proof.

## Handoff over hidden autonomy

The final report has one recommendation and a precise engineer handoff. A clean report is not authorization to deploy; the next actor and approval gate remain explicit.

## Gap fill 2026-10-18

The pack lacked `.apm/prompts/`, `examples/` and `templates/`. They were authored from the existing agent, skills and contract instruction, which were not changed. Questions could not be asked, so the assumptions below were made.

### Prompts

- **Eight workflows.** The set comes from the agent's operating contract, the routing sequence in cloud-prepress-orchestration, and the six existing trigger cases: pre-PR review, pre-deployment review, preview interpretation, security and supply chain, architecture and ADR alignment, operability with rollback and cost, handoff readiness, and report validation.
- **One combined workflow.** Operability, rollback and cost share a prompt because the contract reports them in one section (`operations_rollback_cost_and_inputs`) and the coverage file treats them as one capability.
- **Preview interpretation stands alone.** "Is this what-if or plan safe?" is a common request on its own, and deployment-preview-and-environment-review defines its own evidence boundary.
- **No new capabilities.** Each prompt step restates what the named skill already defines.
- **Frontmatter.** Prompts set only `description` and `agent: cloud-prepress-reviewer`.
- **Installed-only references.** Prompts name only skills, the agent and the contract instruction. They do not repeat the helper-script paths from review-hooks-and-automation, because APM does not deploy hook scripts. Instead they say "if the pack's pre-review and post-review helpers are available", and treat absent helpers as skipped.
- **Recommendation choice.** The contract defines the five recommendations but not how to choose between them, so the prompts and examples apply this rule:
  - `BLOCKED_ON_HUMAN_DECISION` when an open decision could remove or reshape the changed component, even if confirmed findings exist.
  - `CHANGES_REQUIRED` when the design is settled and the code contradicts it.
  - `NOT_VERIFIED` when evidence is missing but no decision is pending.

### Report format

- **Section headings.** The report's twelve headings map in order to the contract's required sections. Each starts with the word the post-review validator looks for: Scope, Evidence, Findings, Recommendation, Engineer Handoff.
- **Finding status values.** The contract names a `status` field but no values. The four categories the skills separate are used: `confirmed`, `validation-hypothesis`, `accepted-risk`, `human-blocker`.
- **Constraints from `tooling/validate_review_report.py`.** This helper is not a file the gap fill may change, so reports work within it:
  - It treats any repeated `F<n>` as a duplicate ID. Each finding ID is therefore written once, in its table, and other sections refer to findings by severity and subject.
  - It requires exactly one recommendation token anywhere in the report, so a report never names a second recommendation, even to rule it out.
  - It rejects secret-like `name: value` text, so reports avoid that phrasing.
- **Evidence labels for tests.** The contract has no label for executed tests. Unit test results are labelled `observed`, as observed tool output. Lint, format, validate and build results are labelled `structurally-validated`.
- **Report location.** The report is saved as `REVIEW.md` in a folder the user names, outside the source tree, matching what `tooling/validate_review_bundle.py` expects. The reviewer edits no source.

### Templates

There are six: the review report, the engineer handoff, the evidence ledger, the deployment preview record, the cost and governance record, and rollback readiness. Each is tied to the skill that produces it. There is no specialist-assignment template, because the pack has one agent. The handoff template is for the next human or automated actor.

### Examples

- **Coverage.** Six examples between them reach all five recommendations. `examples/bicep-keyvault-not-verified.md` shows the unverified outcome, and `examples/architecture-drift-blocked.md` the blocked one.
- **Fictional content.** Repositories, identities, subscriptions and figures are invented. Cost figures are labelled author estimates, not current pricing. The USD 150/month ceiling appears only where the fictional repository's constraints state it, as cost-allocation-and-governance-review requires.
- **Technical facts.** The examples rely on behavior known at authoring time and not re-checked against live documentation in this session, because web access was not permitted:
  - Service Bus message auto-completion.
  - Terraform `moved` semantics.
  - Key Vault access policies being ignored under the RBAC permission model.
  - Contributor lacking role-assignment write.
  - The meaning of the PostgreSQL `0.0.0.0` firewall rule.
  - `pull_request_target` privileges.
  - The GitHub OIDC environment subject format.
- **Helper output.** In `examples/hooks-and-report-validation.md`, the helper output was derived by reading `tooling/review_inventory.py`, `tooling/validate_review_report.py` and the hook scripts. It was not captured from a run: running ad-hoc scripts was not permitted in this session.
- **How the reports were checked.** For each example's completion report, pattern searches reproduced the validator's four checks: required headings, exactly one recommendation, unique `F<n>` IDs, and the secret-like pattern. They also confirmed all twelve sections, all nine finding fields, and contract-only evidence labels. The validator itself was not executed on them.

### Other files

- **Skill inventory.** `docs/SKILL_INVENTORY.md` was not created. It does not exist, and the gap-fill rules allow creating only `docs/PROMPT_INVENTORY.md`, so the skill-to-prompt mapping lives in `docs/PROMPT_INVENTORY.md`.
- **Trigger cases.** In `tests/trigger-cases.yml`, the existing `prompt` key holds the user's request, so prompt files go in a new `workflow_prompt` key. Five cases were added for workflows and refusals the file did not cover: preview interpretation, rollback and cost, handoff readiness, missing preview, and an unauthorized live query.
- **Capability coverage.** `tests/capability-coverage.yml` gains a `prompt_map`. Every required capability is reached by at least one prompt.
- **README.** The validate command now takes the pack folder and drops `--write-report`, a flag the shared validator does not have; the validator writes the report by default. The `build_pack.py` line is unchanged, because its command line is not available in this workspace.

### Known gaps

- **Inventory helper limits.** `tooling/review_inventory.py` compares the working tree with `HEAD`, so it lists nothing for a committed branch with a clean tree. Its path classification uses substrings, so `keyvault` counts as sensitive and `alarm` as infrastructure. The examples show reviewers working around both; the helper was not changed.
- **Two meanings of `REVIEW.md`.** documentation-inputs-and-repository-contracts uses `REVIEW.md` for a repository's human-only blockers, while the pack's helpers use it for the pre-press report. The templates call the former "the human review record (for example `REVIEW.md`)". The skills should settle the naming.
- **No helper tests.** The pack has no `tests/test_*.py`, so the shared validator skips the helper unit-test check.
- **Unobserved behavior.** Model behavior with these prompts, and how each client lists and runs them after install, have not been observed.
