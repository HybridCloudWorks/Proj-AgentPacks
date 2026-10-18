# Design and De-duplication Decisions

## One Agent, Eight Skills

The Agent stays narrow and owns role, scope, permissions, orchestration, evidence posture, and completion. `review-infrastructure-pr` owns the end-to-end protocol. Six technology Skills load only for stacks present in the diff. `verify-infrastructure-evidence` owns safe checks and evidence integrity. This preserves complete coverage without loading every technology adapter into every review.

## Core Protocol Remains Central

Changed-line coverage, cross-tool tracing, existing-environment reasoning, universal gates, severity, de-duplication, adversarial review, and final output apply to every infrastructure review. They remain references of the orchestration Skill rather than separate always-invoked Skills, avoiding coordination and discovery overhead.

## Technology Adapters Become Skills

Terraform/OpenTofu, Bicep/ARM, PowerShell, Ansible, CI/CD and scripts, and Kubernetes packaging have distinct runtime semantics. Each adapter is an independently triggerable Skill so irrelevant technology guidance does not consume context and one adapter can be versioned or replaced without changing the others.

## Evidence Is a Separate Capability

Static checks and evidence interpretation are deterministic and reusable but do not prove semantic correctness. The evidence Skill runs only safe local checks, records passes/failures/skips, validates provenance, and requests target-specific artifacts. The reviewer remains responsible for judgment.

## GitHub Copilot Is a Target, Not the Canonical Identity

The supplied sources were designed for Copilot code review, but the review method itself is vendor-neutral. The canonical Agent is `infrastructure-pr-reviewer`. Copilot-specific skill paths, instructions, environment setup, PR template, and enforcement guidance live in the Copilot target or conditional setup resources.

## Read-Only by Default

Review requires repository access, search, current documentation, PR metadata, and explicitly safe validation. It does not require edits or deployment privileges. Generated adapters deny or omit write tools, Claude uses plan mode, Codex uses a read-only sandbox, and Gemini receives no write tools.

## Source Ownership

Every rule has one canonical owner listed in `docs/SOURCE_TRACEABILITY.md`. Technology checklists support their Skill but do not redefine the universal gates or final output. Generated targets are build artifacts and must not be edited directly.

## Completeness Boundary

The pack is capability-complete for the supplied infrastructure review contract. Correct conclusions still depend on the actual repository, complete diff, current official documentation, target-specific evidence, installed tools, and host access. Missing evidence is reported rather than converted into unsupported assurance.

## Gap fill 2026-10-18

The pack shipped without `.apm/prompts/`, `examples/` or `templates/`. They were authored from the existing agent, Skills and contract instruction, which were not changed.

### Prompts

- **Seven prompts, one per workflow the Skills already define.** The main review (`review-infrastructure-pr` Workflow), re-review (its Re-review section), existing-environment impact (review protocol section 5 and the lifecycle and ownership gates), deployment pipeline review (the `review-cicd-deployment` Workflow), cross-tool tracing (review protocol sections 3 and 4), evidence verification (`verify-infrastructure-evidence`), and evidence requests (the Skill's instruction to use `assets/infrastructure-pull-request-template.md` to request reviewable evidence).
- **No per-technology prompts.** Technology Skills return findings to `review-infrastructure-pr` and never write a report, and a review limited to one technology would leave other changed lines without a disposition, which is a stop condition. Technology routing stays inside every prompt.
- **No Copilot setup prompt.** Installing or tuning Copilot code review changes repository files, and the agent is review-only. Enforcement gaps are recorded in the report's Handoff under configuration dependencies, using `assets/repository-enforcement-checklist.md`.
- **Focused prompts do not narrow coverage.** Each one still runs the full changed-line protocol; the focus changes which gates and evidence get emphasis.
- **One output for every prompt.** The contract instruction defines a single completion report, so every prompt returns it, including the evidence-only and evidence-request workflows.
- **Writes need explicit authorization.** Prompts tell the agent not to post comments, approve, resolve conversations or change review state unless the user explicitly authorizes it, following the agent's Capability Contract that external systems are read-only by default. This is an instruction, not enforcement: `compatibility/tool-permissions.yml` declares `inherit`, so the host's permissions decide.
- **Installed-content boundary.** Prompts name only Skills, files inside those Skills (`assets/`, `references/`, `scripts/`) and the contract instruction. They never reference `examples/`, `templates/` or `docs/`.

### Templates

- Six templates, each a document the Skills tell the agent to produce: the completion report (contract instruction and `assets/review-report-template.md`), the changed-line coverage ledger (review protocol section 2), the evidence record (`verify-infrastructure-evidence` Output Contract), the technology adapter return (the shared adapter Output Contract), the review handoff (the report's Handoff section), and the re-review reconciliation (Re-review section).
- Templates are human-facing and not installed. Where a template and the installed asset or contract instruction disagree, the installed files win; the completion-report template annotates the asset rather than replacing it.

### Conventions the contract leaves open

The contract fixes section names, finding fields, severities and dispositions but not these, so the examples and templates assume:

- Finding IDs are `F-01`, `F-02`, and keep their ID across re-reviews while the root cause is unchanged.
- `Category` takes the name of the universal gate the finding falls under, such as "Lifecycle and destructive impact".
- `Confidence` in a finding is High or Medium. Low-confidence concerns become evidence gaps, as `references/severity-and-output.md` advises.
- `Location` uses new-file line numbers; a deletion anchors to the nearest changed line and names the removed control.
- Evidence gaps use the `[<Severity> evidence gap] <title>` header from `references/severity-and-output.md`, followed by artifact, commit, inputs, target and identity, and the risk resolved.

### Examples

- Six synthetic walkthroughs. Repository names, SHAs, run numbers, line numbers and command output are illustrative; nothing was executed against real infrastructure or captured from a real run.
- Together they exercise all eight Skills and four of the five dispositions: Changes requested (three), Insufficient evidence for a safe recommendation (the Kustomize and Argo CD example, which is the required blocked or unverified outcome), Ready with conditions, and Ready for human approval. Blocked by a human or external decision is not exemplified.
- The product behaviors the examples rely on (Terraform `count` to `for_each` addressing, the `ConvertTo-Json` default depth, Ansible's exit status when a host pattern matches nothing, `pull_request_target` permissions, Argo CD prune, nginx validation from a temporary path, Azure's rejection of duplicate diagnostic destinations) come from the author's knowledge. Web access was not permitted for this fill, so they were not re-verified against current official documentation. A reviewer applying the pack must still verify version-specific behavior as the Skills require.

### Inventories and tests

- `docs/PROMPT_INVENTORY.md` was created. `docs/SKILL_INVENTORY.md` does not exist and the fill rules permit creating only the prompt inventory, so the Skill-to-prompt map lives in `docs/PROMPT_INVENTORY.md`.
- `tests/capability-coverage.yml` gained a `prompts` list per capability and `tests/trigger-cases.yml` a `prompt` per case. Nothing in the pack's own tooling reads either file; the shared validator checks that every named prompt exists.
- The prompt inventory states only the prompt-deployment facts recorded in the verified vendor facts: Copilot honours `agent`, Claude Code drops it with a warning, and a user-scope install gives Codex no prompts. Gemini CLI and Kiro prompt handling is not recorded there and is left to the install output.

### Gaps found in files this fill may not change

- `.apm/agents/infrastructure-pr-reviewer.agent.md` has seven tool names (`- Read` through `- Skill`) indented under `description` with no `tools:` key. The shared validator's line parser ignores them, but a YAML parser reads them as a continuation of the description, so generated agents may carry "- Read - Grep …" at the end of their description. The pack owner should delete those lines.
- `.apm/instructions/infrastructure-review.instructions.md` points at `.github/skills/review-infrastructure-pr/SKILL.md`, a repository path that exists only in the Copilot code-review layout, not in a user-scope install.
- The "Read-Only by Default" decision above says generated adapters deny write tools, Claude uses plan mode and Codex a read-only sandbox. The current canonical agent declares no tools and `compatibility/tool-permissions.yml` declares `inherit`, so nothing in the source produces those restrictions.
- The README's Build section runs `python3 tooling/build_pack.py` as if it lived in the pack; build tooling is shared at the repository root. It was left unchanged because the shared builder's interface is not in this workspace.
