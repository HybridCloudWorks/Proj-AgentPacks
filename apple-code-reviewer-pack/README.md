# Apple Code Reviewer Pack

A portable, read-only-by-default specialist for evidence-based reviews of Swift, SwiftUI, UIKit, AppKit, Objective-C interoperability, Apple-platform configuration, tests, and delivery pipelines.

The package consolidates the two supplied reviewer drafts into one canonical workflow. The longer draft repeated most of the SOP; this pack keeps each requirement once, moves Apple-specific depth into on-demand Skills, and preserves repository-specific behavior as conditional overrides rather than global assumptions.

## Architecture

```text
.apm/agents/apple-code-reviewer.agent.md
        |
        +-- review-apple-code                 # complete review orchestration
              +-- inspect-swift-correctness
              +-- assess-apple-ui-accessibility
              +-- assess-apple-security-privacy
              +-- assess-apple-runtime-quality
              +-- verify-apple-build-tests
```

The Agent defines identity, boundaries, required capabilities, and orchestration. `review-apple-code` owns the twelve-phase SOP, severity and routing rules, de-duplication, report contract, and completion criteria. Five focused Skills supply Apple-specific depth only when the changed code requires it.

## Skills

| Skill | Use |
|---|---|
| `review-apple-code` | Run a complete PR, branch, feature, bug-fix, refactor, audit, or AI-generated-code review for Apple platforms. |
| `inspect-swift-correctness` | Analyze Swift semantics, state, optionals, errors, ARC, concurrency, API design, and interoperability. |
| `assess-apple-ui-accessibility` | Review SwiftUI, UIKit, or AppKit lifecycle, state, navigation, layout, localization, and accessibility. |
| `assess-apple-security-privacy` | Review trust boundaries, credentials, Keychain, storage, networking, permissions, entitlements, privacy manifests, and App Store risk. |
| `assess-apple-runtime-quality` | Review performance, responsiveness, energy, resource lifetime, error handling, retries, logging, and observability. |
| `verify-apple-build-tests` | Inspect Xcode or SwiftPM buildability, tests, dependencies, configuration, signing inputs, and CI evidence. |

## Workflow prompts

Eight prompts in `.apm/prompts/` start the common review workflows. Each targets the `apple-code-reviewer` agent, activates `review-apple-code`, names the domain Skills it applies, and follows the always-on `apple-code-reviewer-contract` instruction, so every prompt returns the same report.

| Prompt | Workflow |
|---|---|
| `review-apple-pull-request.prompt.md` | Merge review of a pull request, branch diff or commit range, including feature, bug-fix and refactor changes. |
| `audit-ai-generated-apple-code.prompt.md` | Audit of AI-generated Apple code and of the claims that came with it. |
| `review-swift-correctness.prompt.md` | Focused review of concurrency, ARC, optionals, errors and interoperability. |
| `review-apple-ui-accessibility.prompt.md` | Focused review of SwiftUI, UIKit or AppKit state, navigation, layout, localization and accessibility. |
| `review-apple-security-privacy.prompt.md` | Focused review of trust boundaries, credentials, entitlements and privacy declarations. |
| `review-apple-runtime-quality.prompt.md` | Focused review of responsiveness, memory, energy, retries and logging. |
| `verify-apple-build-and-ci.prompt.md` | What can be built and tested in this environment, and what the CI evidence shows. |
| `assess-apple-release-readiness.prompt.md` | Whether a release candidate has the evidence it needs to ship. |

`docs/PROMPT_INVENTORY.md` lists the Skills each prompt applies, its expected output, its worked example, and how each client receives prompts.

## Examples and templates

`examples/` holds six worked reviews, one for each main workflow, and each ends with a complete report in the contract format. All names, commits and outputs in them are synthetic. `assess-apple-release-readiness-blocked.md` shows a Blocked outcome in which no build or test evidence exists and nothing is claimed as passed.

`templates/` holds the documents the Skills ask the reviewer to produce: `review-scope.md`, `build-test-evidence.md`, `completion-report.md`, `engineer-handoff.md` and `documentation-impact-entries.md`. The canonical report template remains the `review-apple-code` Skill asset `assets/review-report-template.md`; `templates/completion-report.md` mirrors it with the allowed values written in. Neither folder is installed, so the installed prompts and Skills never point at them.

## APM source and installation

`.apm/` is the authored source of truth. Vendor directories under `dist/` are generated compatibility outputs and must not be hand-edited.

From the package root in an environment with APM installed:

```bash
apm install
apm compile --validate
apm audit --ci
```

`apm install` generates `apm.lock.yaml`. Commit that generated lockfile so later installs can resolve the same versions and content hashes; do not fabricate it manually. Exclude generated dependency directories such as `apm_modules/` from source control.

Current APM documentation supports the canonical Skills across the declared targets. It deploys Agents directly to Copilot and Claude, transforms the Agent for Codex with a warning that restrictions may be lost, and does not yet deploy the current native Gemini subagent primitive. The generated Codex and Gemini adapters therefore remain required compatibility outputs until APM closes those gaps.

## Generate and validate native targets

```bash
python3 tooling/generate_targets.py
python3 tooling/validate_pack.py
```

Generated layouts:

- Copilot: `.github/agents/` plus `.agents/skills/`
- Claude: `.claude/agents/` plus `.claude/skills/`
- Codex: `.codex/agents/` plus `.agents/skills/`
- Gemini: `.gemini/agents/` plus `.agents/skills/`

Copy the contents of the applicable target directory into a repository root.

## Build all distributions

```bash
python3 tooling/build_pack.py
```

The portable fallback validates and zips each Skill internally. To require the external Skill Creator validator and packager, supply its script path without embedding a machine-specific location in this repository:

```bash
SKILL_CREATOR_PACKAGE_SCRIPT=/path/to/skill-creator/scripts/package_skill.py \
  python3 tooling/build_pack.py
```

The build cleans stale distributions, regenerates all targets, validates canonical source, validates and packages every Skill, verifies every archive, writes `dist/VALIDATION_REPORT.md`, and then verifies the final full archive. Distribution-only verification is also available:

```bash
python3 tooling/verify_distributions.py --packager-mode portable-fallback
```

Outputs:

- One exact `skill.zip` per Skill under `dist/skills/<skill-name>/`.
- One native target ZIP per vendor under `dist/`.
- `dist/apple-code-reviewer-skills.zip` containing all six independent Skill archives.
- `dist/apple-code-reviewer-pack.zip` containing canonical source, generated vendor files, tests, tooling, documentation, and validation report.
- `dist/VALIDATION_REPORT.md` recording checks, package sizes, host capabilities, and deployment-time validation still required.

## Permission posture

The generated adapters omit file-edit tools. They may read and search repository content, inspect review metadata where the host exposes it, consult current official documentation, and run approved non-destructive commands. Claude uses plan mode, Codex uses a read-only sandbox, and Gemini receives no file-write tool. Shell access can still mutate a workspace in some hosts, so the Agent contract, host sandbox, organization policy, and user confirmations remain enforcement boundaries.

## Apple toolchain boundary

Authoritative Xcode builds, XCTest/XCUITest, signing, simulator, device, and archive validation require macOS with the applicable Xcode version, target configuration, and credentials. Linux can inspect source and may validate a pure Swift package when a compatible Swift toolchain exists, but it cannot establish that an Apple app target builds or passes Xcode tests. The pack detects and reports this boundary instead of implying success.

## Maintenance

`compatibility/vendor-sources.yml` records the official specifications, review date, and affected package components. Refresh those sources before changing formats, tool names, Apple-platform requirements, or release behavior. Update the canonical source and adapters together, run trigger and contract tests, regenerate distributions, and increment `apm.yml` using semantic versioning.

## Reliability boundary

The pack is capability-complete for the defined Apple code-review contract. It cannot guarantee an authoritative conclusion without the applicable diff, repository context, target configuration, current official documentation, compatible toolchain, CI evidence, and permitted access. Missing evidence is reported explicitly and never converted into approval.
