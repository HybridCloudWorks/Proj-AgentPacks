# Design and De-duplication Decisions

## One Agent, Six Skills

One reviewer Agent preserves a clear invocation surface. One orchestration Skill owns the complete twelve-phase SOP, and five domain Skills load only when the changed code requires them. This avoids both a monolithic prompt and dozens of tiny Skills whose discovery metadata and coordination would cost more context than they save.

## Primary Workflow as a Skill

`review-apple-code` is the Agent's operating procedure and the portable fallback for clients that support Skills more consistently than custom Agents. The Agent does not repeat the twelve phases, severity model, routing rules, or report template; it activates the Skill that owns them.

## Progressive Disclosure

Only Skill names and descriptions are intended to be visible during discovery. Full Skill instructions load on activation, and detailed references or scripts load only when the workflow calls for them. Repository exceptions are isolated in `repository-overrides.md` and remain dormant unless their explicit conditions are present.

## Read-Only by Default

Review needs source reading, search, current documentation, review metadata, and non-destructive validation. It does not need edits, deployment, signing, publishing, or production credentials. Generated adapters omit file-write tools; Claude uses plan mode; Codex uses a read-only sandbox; Gemini receives no write tool. Shell access is still governed by the Agent's non-destructive command contract and the host's sandbox, policy, and approval controls.

## Domain Ownership

- Swift correctness owns language semantics, ARC, concurrency, state, API behavior, and Objective-C interoperability.
- UI and accessibility owns presentation lifecycle, state ownership, interaction, navigation, layout, localization, and accessibility.
- Security and privacy owns trust boundaries, authorization, sensitive data, entitlements, permissions, privacy declarations, and store-policy risk.
- Runtime quality owns responsiveness, performance, energy, resource lifetime, failures, retries, logging, and observability.
- Build and tests owns executable evidence, Xcode and SwiftPM configuration, dependencies, tests, signing-input boundaries, CI interpretation, and release validation.

When multiple domains observe one root cause, `review-apple-code` merges it into one finding instead of counting it repeatedly.

## Repository-Specific Content

The original drafts contained file names, commands, historical findings, and environment details from one repository. Those rules are preserved in `repository-overrides.md` and activate only when their named evidence exists. They are not embedded in the portable Agent or universal Apple checklists.

## Vendor Adapters

The canonical Agent uses a compact capability-oriented tool vocabulary. `generate_targets.py` maps that contract to each target's native tool names, frontmatter, directories, and permission controls without changing the Agent body. Generated files are compatibility artifacts, not independent behavioral sources.

APM currently deploys the Agent directly to Copilot and Claude. Its Codex transformation may lose tool restrictions, so the generated read-only TOML adapter is retained. APM's current matrix still does not deploy a Gemini Agent even though Gemini CLI has a native subagent format, so the pack generates that adapter explicitly. Skills use the native or interoperable discovery path supported by each target.

## Toolchain Detection

`detect_apple_toolchain.py` is the only deterministic helper because environment detection is repetitive and error-prone. It reports capabilities rather than assuming that the presence of Swift implies Xcode. Interpretation, review judgment, and reporting remain model-owned.

## Source Ownership and De-duplication

`docs/SOURCE_TRACEABILITY.md` assigns every source requirement to exactly one canonical owner. Supporting references and generated adapters may consume a rule but do not redefine it. `tooling/validate_pack.py` checks source ownership, repeated long prose, references, trigger fixtures, output fields, hidden Unicode, possible secrets, and generated-target drift.

## Completeness Claim

The pack supplies every procedure, capability, output field, validation rule, and stop condition required by the defined Apple review contract. Correct results still depend on the actual change, repository evidence, current official documentation, compatible Apple toolchain, CI results, and access granted by the host. The design reports missing evidence instead of inventing it.

## Gap fill 2026-10-18

The pack was missing `.apm/prompts/`, `examples/` and `templates/`. This fill added eight prompts, six worked examples, five templates and `docs/PROMPT_INVENTORY.md`, and updated `README.md`, `tests/capability-coverage.yml` and `tests/trigger-cases.yml` to reference the prompts by file name. Agents, Skills, instructions, `apm.yml` and `compatibility/tool-permissions.yml` were not changed.

### Assumptions

1. **Primary workflows.** The workflows come from the agent description and the activation text of `review-apple-code`: pull-request or branch review, audit of AI-generated code, and release review, plus one focused review for each domain Skill. Feature, bug-fix and refactor reviews differ only in the change type recorded in scope, so `review-apple-pull-request.prompt.md` serves all three instead of three near-identical prompts.
2. **Every prompt runs through `review-apple-code`.** The agent's orchestration requires it, and the domain Skills return findings to the parent review. A focused prompt therefore still produces the full contract report, with out-of-focus categories marked not reviewed or not applicable and a reason, which satisfies completion criterion 3 of `review-apple-code`.
3. **Recommendation semantics.** The pack lists the four allowed recommendations but does not define when each applies. The examples use: Approved when no finding needs a change and the evidence suits the risk; Approved with comments when only Low findings or measurement suggestions remain; Changes requested when engineering-resolvable findings must be fixed first; Blocked when a human decision, required access or required evidence is missing, or a Critical finding exists. This is recorded here only, because installed Skills and instructions could not be edited in a fill. A later Skill revision should state it in `references/severity-labels-routing.md`.
4. **Templates.** The canonical report template stays the `review-apple-code` asset `assets/review-report-template.md`. `templates/completion-report.md` mirrors it with the allowed values written in and must change whenever the asset changes. The other templates expand records the Skills already require: the scope summary (step 1 of `review-apple-code`), the build and test evidence record (the output contract of `verify-apple-build-tests`), documentation-impact entries (`severity-labels-routing.md`) and the engineer handoff (completion criterion 6). The pack has no specialist agents, so "handoff" means the handoff to the engineer who fixes the change.
5. **Prompt frontmatter.** Prompts carry only `description` and `agent: apple-code-reviewer`. `argument-hint` and `input` were left out because their support across Copilot and Claude is not fully recorded in the vendor reference this repository verified.
6. **Prompt deployment.** `docs/PROMPT_INVENTORY.md` states only what the vendor reference records: Copilot honors `agent`, Claude drops it with a warning, Codex receives no prompts. Kiro and Gemini prompt deployment is not recorded there and is described as unverified.
7. **Installed references.** Prompts name Skills, the contract instruction and files bundled inside Skills (the toolchain detector, the official-source lists), but no path outside a Skill, so they stay valid after install. They use ASCII only, because `apm install` blocks on hidden-Unicode findings.
8. **Synthetic examples.** Apps, packages, domains, commits, CI runs and command output in `examples/` are invented to show the workflow. Xcode and OS release numbers are avoided except deployment targets, so the examples do not age into false version claims. The one place secrets appear is written as `[REDACTED_POSSIBLE_SECRET]`.
9. **Blocked example.** `assess-apple-release-readiness-blocked.md` shows the unverified outcome required by the fill brief: a host without any Apple toolchain, release CI cancelled by a time limit, and two human blockers. It exercises both conditional repository overrides (Linux environment, cancelled CI).
10. **Skill inventory.** `docs/SKILL_INVENTORY.md` does not exist, and the fill rules allow creating only `docs/PROMPT_INVENTORY.md`. The skill-to-prompt mapping therefore lives in `docs/PROMPT_INVENTORY.md` and in the new `requirements` list of `tests/capability-coverage.yml`, which has exactly one entry per Skill.

### Gaps observed and left for a separate change

- The canonical agent's frontmatter has a dangling list (`- Read`, `- Grep` and so on) under `description` with no `tools:` key. YAML folds those lines into the description text, so the description ends with tool names. Agents were out of scope for this fill.
- The contract instruction carries the completion-report rules but no approval levels or handoff rules of its own, although the authoring prompt says the contract carries all three. Instructions were out of scope for this fill.
- `README.md` still describes `tooling/validate_pack.py`, `tooling/build_pack.py` and a `dist/` vendor layout produced by `tooling/generate_targets.py`. The shared validator lives at the repository root and the pack has no `build_pack.py`. The fill added sections without rewriting those parts.
- The pack has no `AGENT-PACK-README.md` artifact catalog and no `VALIDATION_REPORT.md`; neither was in this fill's scope.
- Validation at fill time: shell access was denied in the fill session, so `tooling/validate_pack.py --install-check` was not run. The new files were checked by hand against the validator's rules (forbidden installed-content patterns, prompt file references, one requirement per Skill, status-name tokens). Run the validator before merging.
