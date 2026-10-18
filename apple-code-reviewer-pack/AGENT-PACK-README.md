# apple-code-reviewer 1.1.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| apple-code-reviewer.agent.md | Canonical agent: Review Swift, SwiftUI, UIKit, AppKit, Objective-C interoperability, Xcode, and Apple-platform changes for correctness, security, privacy, accessibility, performance, tests, configuration, and release risk. Use for pull requests, branch diffs, feature work, bug fixes, refactors, security or performance changes, and audits of AI-generated Apple code. | .apm/agents/apple-code-reviewer.agent.md |
| apple-code-reviewer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the apple code reviewer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/apple-code-reviewer-contract.instructions.md |
| openai.yaml | Canonical skill | .apm/skills/assess-apple-runtime-quality/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/assess-apple-runtime-quality/references/official-sources.md |
| runtime-quality-checklist.md | Canonical skill | .apm/skills/assess-apple-runtime-quality/references/runtime-quality-checklist.md |
| SKILL.md | Canonical skill: Assess Apple-platform changes for UI stalls, excessive work, memory or resource leaks, rendering churn, unbounded growth, network and storage inefficiency, battery or thermal risk, unsafe retries, weak failure handling, sensitive or noisy logging, and missing observability. Use when reviewing hot paths, main-actor work, lists, media, networking, persistence, background tasks, timers, notifications, logging, metrics, or performance-sensitive code. | .apm/skills/assess-apple-runtime-quality/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/assess-apple-security-privacy/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/assess-apple-security-privacy/references/official-sources.md |
| security-privacy-checklist.md | Canonical skill | .apm/skills/assess-apple-security-privacy/references/security-privacy-checklist.md |
| SKILL.md | Canonical skill: Assess Apple-platform code and configuration for trust-boundary failures, authentication or authorization bypass, secret exposure, unsafe storage or networking, WebKit and deep-link attacks, entitlement misuse, permission problems, privacy-manifest gaps, sensitive logging, and App Store security or privacy risk. Use when changes handle user or external input, identity, credentials, personal data, files, URLs, network calls, Keychain, permissions, entitlements, extensions, or third-party SDKs. | .apm/skills/assess-apple-security-privacy/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/assess-apple-ui-accessibility/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/assess-apple-ui-accessibility/references/official-sources.md |
| ui-accessibility-checklist.md | Canonical skill | .apm/skills/assess-apple-ui-accessibility/references/ui-accessibility-checklist.md |
| SKILL.md | Canonical skill: Assess SwiftUI, UIKit, and AppKit changes for lifecycle and state defects, navigation errors, invalid update flow, adaptive-layout failures, localization problems, input and focus issues, and accessibility regressions. Use when reviewing views, view controllers, scenes, windows, navigation, forms, lists, gestures, custom controls, animations, or UI tests; do not use for visual taste or product-design changes unsupported by requirements. | .apm/skills/assess-apple-ui-accessibility/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/inspect-swift-correctness/agents/openai.yaml |
| official-sources.md | Canonical skill | .apm/skills/inspect-swift-correctness/references/official-sources.md |
| swift-correctness-checklist.md | Canonical skill | .apm/skills/inspect-swift-correctness/references/swift-correctness-checklist.md |
| SKILL.md | Canonical skill: Inspect Swift and Objective-C-interoperable code for behavioral defects, unsafe state, optional and error misuse, ARC ownership problems, concurrency violations, API-design hazards, and data-integrity risks. Use when reviewing Swift source, async or actor code, closures, protocols, persistence models, collection or string logic, or Objective-C and C boundaries; do not use for UI-only layout or build-system analysis. | .apm/skills/inspect-swift-correctness/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/review-apple-code/agents/openai.yaml |
| review-report-template.md | Canonical skill | .apm/skills/review-apple-code/assets/review-report-template.md |
| core-review-checklist.md | Canonical skill | .apm/skills/review-apple-code/references/core-review-checklist.md |
| repository-overrides.md | Canonical skill | .apm/skills/review-apple-code/references/repository-overrides.md |
| severity-labels-routing.md | Canonical skill | .apm/skills/review-apple-code/references/severity-labels-routing.md |
| SKILL.md | Canonical skill: Review an Apple-platform code change end to end and produce a severity-classified, evidence-based, handoff-ready report. Use for Swift, SwiftUI, UIKit, AppKit, Objective-C interoperability, Xcode, SwiftPM, Apple CI, pull requests, branch diffs, feature or bug-fix reviews, refactors, security or performance changes, and audits of AI-generated Apple code; do not use for implementing fixes or broad documentation cleanup. | .apm/skills/review-apple-code/SKILL.md |
| openai.yaml | Canonical skill | .apm/skills/verify-apple-build-tests/agents/openai.yaml |
| build-test-matrix.md | Canonical skill | .apm/skills/verify-apple-build-tests/references/build-test-matrix.md |
| official-sources.md | Canonical skill | .apm/skills/verify-apple-build-tests/references/official-sources.md |
| detect_apple_toolchain.py | Canonical skill | .apm/skills/verify-apple-build-tests/scripts/detect_apple_toolchain.py |
| SKILL.md | Canonical skill: Verify the build, test, dependency, configuration, signing-input, and CI evidence for Apple-platform changes. Use when reviewing Xcode projects or workspaces, Swift packages, schemes, build settings, XCTest or Swift Testing, XCUITest, dependency locks, entitlements, Info.plist, privacy manifests, xcconfig, CI workflows, archives, or release readiness; do not claim Apple app validation when macOS and the required Xcode toolchain are unavailable. | .apm/skills/verify-apple-build-tests/SKILL.md |
| .gitignore | Pack file | .gitignore |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| generate_targets.py | Pack-specific helper code | tooling/generate_targets.py |
| verify_distributions.py | Pack-specific helper code | tooling/verify_distributions.py |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-apple-code-reviewer.zip: 29 files generated by `apm install --target copilot`
- claude-apple-code-reviewer.zip: 29 files generated by `apm install --target claude`
- codex-apple-code-reviewer.zip: 28 files generated by `apm install --target codex`
- kiro-apple-code-reviewer.zip: 29 files generated by `apm install --target kiro`
- gemini-apple-code-reviewer.zip: 27 files generated by `apm install --target gemini`
- agent-skills-apple-code-reviewer.zip: 27 files generated by `apm install --target agent-skills`
- apple-code-reviewer-canonical.zip, apple-code-reviewer-prompt.zip, apple-code-reviewer-validation.zip, apple-code-reviewer-skills.zip, apple-code-reviewer-full-pack.zip, SHA256SUMS.txt
