# Source Traceability

## Inputs

| Source | SHA-256 | Role |
|---|---|---|
| `code-reviewer (2).md` | `1b5d459f3e110e4edce18b9aa2500487f58034f4d46418f8b30603d5806f3fb6` | Concise SOP, repository exceptions, report contract, and environment constraints. |
| `code-reviewer.md` | `2904d356eae17e4352cc85bf2ef531b0e052a459018f6032e27b0a5ab554b944` | Expanded phase detail plus a second near-duplicate SOP. |

`Agent Terraform.txt` was not used because it describes a different Terraform pack and is outside this Apple reviewer example.

## De-duplication Decision

The expanded source repeats the operating principles and twelve phases in two forms. The pack uses the concise source as the control plane, incorporates unique detail from the expanded source into focused references, and records repository-specific facts as conditional overrides. Each requirement below has one canonical owner; adapters and references may support that owner without redefining it.

## Requirement Mapping

| Source requirement | Canonical owner | Supporting material or adapter |
|---|---|---|
| Senior Apple reviewer identity, role boundaries, required capabilities, and read-only posture | `.apm/agents/apple-code-reviewer.agent.md` | Vendor adapters under `dist/` |
| Evidence-first, actionable review workflow and twelve-phase completion | `.apm/skills/review-apple-code/SKILL.md` | `references/core-review-checklist.md` |
| Severity definitions and required labels | `.apm/skills/review-apple-code/references/severity-labels-routing.md` | Report template consumes the definitions |
| Dot-prefixed folder default exclusion and real-defect exceptions | `.apm/skills/review-apple-code/references/core-review-checklist.md` | Agent delegates to the primary Skill |
| Phase 1 scope | `.apm/skills/review-apple-code/SKILL.md` | `core-review-checklist.md` provides detailed prompts |
| Phase 2 architecture | `.apm/skills/review-apple-code/references/core-review-checklist.md` | Primary Skill invokes the checklist |
| Phase 3 code quality | `.apm/skills/review-apple-code/references/core-review-checklist.md` | Primary Skill invokes the checklist |
| Phase 4 defects and logic | `.apm/skills/inspect-swift-correctness/SKILL.md` | `references/swift-correctness-checklist.md` |
| Phase 5 security | `.apm/skills/assess-apple-security-privacy/SKILL.md` | `references/security-privacy-checklist.md` |
| Phase 6 performance and scalability | `.apm/skills/assess-apple-runtime-quality/SKILL.md` | `references/runtime-quality-checklist.md` |
| Phase 7 error handling and observability | `.apm/skills/assess-apple-runtime-quality/SKILL.md` | `references/runtime-quality-checklist.md` |
| Phase 8 tests | `.apm/skills/verify-apple-build-tests/SKILL.md` | `references/build-test-matrix.md` |
| Phase 9 dependencies and configuration | `.apm/skills/verify-apple-build-tests/SKILL.md` | `references/build-test-matrix.md` |
| Phase 10 documentation impact | `.apm/skills/review-apple-code/references/severity-labels-routing.md` | Primary Skill invokes routing |
| Phase 11 finding validation and de-duplication | `.apm/skills/review-apple-code/SKILL.md` | No second validation checklist retained |
| Phase 12 final report | `.apm/skills/review-apple-code/assets/review-report-template.md` | Primary Skill requires exact use |
| README, CHANGELOG, REVIEW, TODO, CHECKLIST routing | `.apm/skills/review-apple-code/references/severity-labels-routing.md` | Report template records counts |
| CHECKLIST fields and placeholder-only values | `.apm/skills/review-apple-code/references/severity-labels-routing.md` | None |
| `MOBILE_IMPLEMENTATION_LEDGER.md` repository note | `.apm/skills/review-apple-code/references/repository-overrides.md` | Loaded only when the named file exists |
| Source environment lacks authoritative Xcode validation | `.apm/skills/verify-apple-build-tests/SKILL.md` | Detector and repository override refine the environment |
| Optional static and wiki checks | `.apm/skills/review-apple-code/references/repository-overrides.md` | Loaded only when commands exist and scope applies |
| Cancelled CI may represent timeout failure | `.apm/skills/verify-apple-build-tests/SKILL.md` | Repository override preserves source-specific rationale |
| Executive summary, counts, findings, recommendation, and handoff fields | `.apm/skills/review-apple-code/assets/review-report-template.md` | `tests/report-contract.yml` validates the shape |

## Official-Spec Additions

The supplied drafts were broad review SOPs with limited Apple-specific depth. The following capabilities were added from official Apple and Swift guidance so the named role can perform Apple-platform review rather than generic review only:

- Swift strict concurrency, actor isolation, task cancellation, continuations, `Sendable`, ARC, and interoperability review.
- SwiftUI, UIKit, and AppKit lifecycle, state ownership, navigation, adaptive layout, localization, and accessibility review.
- Keychain, ATS, entitlements, permissions, privacy manifests, required-reason APIs, third-party SDK declarations, and App Store risk review.
- Responsiveness, energy, memory and resource lifetime, retry, logging, telemetry, and measurement review.
- Xcode and SwiftPM capability detection, test matrix, signing-input boundaries, dependency review, CI interpretation, and release-evidence limits.

These additions live in domain Skills and focused official-source files so they can be updated independently without expanding the Agent body.
