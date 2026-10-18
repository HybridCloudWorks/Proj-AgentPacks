# Prompt inventory

The pack ships eight workflow prompts in `.apm/prompts/`. Each one targets the `apple-code-reviewer` agent and activates `review-apple-code`, which owns scope, routing, de-duplication and the report. Each prompt also names the domain Skills it applies and follows the always-on `apple-code-reviewer-contract` instruction. All eight return the same report; they differ in focus, required inputs and the Skills they bring in.

| Prompt | Use when | Skills applied | Expected output | Worked example |
|---|---|---|---|---|
| review-apple-pull-request.prompt.md | A pull request, branch diff or commit range needs a merge recommendation. Covers feature, bug-fix and refactor changes. | review-apple-code, then routed: inspect-swift-correctness, assess-apple-ui-accessibility, assess-apple-security-privacy, assess-apple-runtime-quality, verify-apple-build-tests | Full report with findings in severity order, severity counts, one allowed recommendation and handoff notes. No host-side comments, approvals or merges. | examples/review-apple-pull-request.md |
| audit-ai-generated-apple-code.prompt.md | Code written by a coding assistant, with claims such as "tests pass", needs checking before a pull request. | review-apple-code, inspect-swift-correctness, verify-apple-build-tests; assess-apple-ui-accessibility, assess-apple-security-privacy, assess-apple-runtime-quality where reached | Full report; Review Scope lists each generator claim as observed, contradicted or not verifiable here. | examples/audit-ai-generated-apple-code.md |
| review-swift-correctness.prompt.md | The user asks about races, actors, tasks, cancellation, ARC, optionals, errors or Objective-C boundaries. | review-apple-code, inspect-swift-correctness; assess-apple-runtime-quality for merged runtime impact | Full report focused on correctness; out-of-focus categories marked not reviewed with a reason. | examples/review-apple-pull-request.md (ACR-001, ACR-002) |
| review-apple-ui-accessibility.prompt.md | SwiftUI, UIKit or AppKit views, navigation, layout, localization or accessibility changed. | review-apple-code, assess-apple-ui-accessibility; inspect-swift-correctness and assess-apple-security-privacy where reached | Full report; each UI finding names platform and OS range, trigger, user and accessibility impact, and a validation method. | examples/review-apple-ui-accessibility.md |
| review-apple-security-privacy.prompt.md | The change crosses a trust, identity, storage, network, permission, entitlement, privacy or SDK boundary. | review-apple-code, assess-apple-security-privacy; verify-apple-build-tests for manifest and lockfile validation | Full report; security findings state attack surface, trust boundary, precondition and mitigation, and carry Security Sensitive. | examples/review-apple-security-privacy.md |
| review-apple-runtime-quality.prompt.md | Responsiveness, memory, energy, retries, logging or telemetry are the concern. | review-apple-code, assess-apple-runtime-quality; inspect-swift-correctness for merged root causes | Full report; findings only above the evidence threshold, measurement suggestions without severity. | examples/review-apple-runtime-quality.md |
| verify-apple-build-and-ci.prompt.md | The question is what can be built and tested here, or what CI evidence shows. | review-apple-code, verify-apple-build-tests | Full report whose Tests and Dependencies and Configuration results list the toolchain, commands with exit status, passes, failures, unavailable validation and validation still required on macOS. | examples/assess-apple-release-readiness-blocked.md |
| assess-apple-release-readiness.prompt.md | A release branch, tag or candidate commit needs a ship recommendation. | review-apple-code, verify-apple-build-tests, assess-apple-security-privacy; inspect-swift-correctness, assess-apple-ui-accessibility, assess-apple-runtime-quality where reached | Full report; Approved only with observed release-configuration build and test results for the candidate. | examples/assess-apple-release-readiness-blocked.md |

## Prompt conventions

- Frontmatter carries only `description` and `agent: apple-code-reviewer`.
- The body has three sections: Inputs, Workflow and Expected output.
- Prompts reference only installed content: Skill names, the contract instruction, and files bundled inside a Skill, such as the toolchain detector and the official-source lists. They never point at `examples/`, `templates/` or `docs/`, which are not installed.
- Prompts grant no permissions. Read-only behavior comes from the agent, the Skills, the contract instruction and the host's own controls.

## How clients receive prompts

According to the vendor reference this pack repository verified on 2026-10-18:

- GitHub Copilot receives prompt files and honors the `agent` field. APM's user-scope install deploys Copilot prompts and instructions.
- Claude Code receives one command per prompt. APM drops the `agent` key with a warning, so the command runs in the current session and activates the Skills itself.
- OpenAI Codex receives no prompts. Ask the agent directly, or invoke `review-apple-code`.
- Kiro and Gemini CLI: that reference does not record prompt deployment for them, so treat it as unverified.
