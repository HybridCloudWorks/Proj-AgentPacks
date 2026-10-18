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
