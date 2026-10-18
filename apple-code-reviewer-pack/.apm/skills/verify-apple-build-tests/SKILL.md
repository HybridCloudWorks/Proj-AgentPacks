---
name: verify-apple-build-tests
description: Verify the build, test, dependency, configuration, signing-input, and CI evidence for Apple-platform changes. Use when reviewing Xcode projects or workspaces, Swift packages, schemes, build settings, XCTest or Swift Testing, XCUITest, dependency locks, entitlements, Info.plist, privacy manifests, xcconfig, CI workflows, archives, or release readiness; do not claim Apple app validation when macOS and the required Xcode toolchain are unavailable.
---

# Objective

Establish what can actually be built and tested in the current environment, evaluate whether changed behavior has risk-proportionate coverage, and identify configuration or dependency failures before merge or release.

# Inputs

Required: repository root plus the changed Xcode, SwiftPM, dependency, configuration, test, or CI files relevant to the review.

Optional: intended schemes, destinations, Xcode and Swift versions, macOS CI logs, test result bundles, signing ownership, and release requirements.

# Workflow

1. Run the bundled `scripts/detect_apple_toolchain.py` from this Skill directory as `python3 scripts/detect_apple_toolchain.py --root <repository> --format markdown`.
2. Identify project type, targets, schemes, packages, dependency managers, tests, CI providers, deployment targets, and required credentials or signing inputs.
3. Select only commands supported by the detected environment and repository.
4. Run the narrowest non-destructive validation first; capture exact command, exit status, and relevant output.
5. Review unit, integration, UI, accessibility, regression, negative-path, concurrency, security, migration, and performance tests applicable to the change.
6. Review dependencies, lockfiles, package plugins, binary targets, build phases, scripts, generated code, and version constraints.
7. Review build settings, xcconfig layering, Info.plist, entitlements, privacy manifests, capabilities, deployment targets, environment inputs, and placeholder validation.
8. Inspect CI conclusions, cancellations, timeouts, skipped jobs, matrix gaps, flaky retries, and artifact or archive evidence.
9. Return verified results, failed results, unavailable validation, missing tests, configuration dependencies, and release impact.

LOAD `references/build-test-matrix.md` to select commands and coverage by repository type.

LOAD `references/official-sources.md` before asserting current Xcode, SwiftPM, testing, signing, privacy, or App Store requirements.

# Output Contract

Return the detected toolchain, commands actually run, verified passes, observed failures, unavailable validation, missing or weak tests, dependency and configuration findings, CI evidence, release impact, and the exact validation still required on macOS or protected infrastructure.

# Environment Rules

- Xcode app targets, simulator and device tests, signing, archives, and XCUITest require macOS with compatible Xcode and project dependencies.
- Linux Swift can validate only compatible pure Swift packages; it does not prove an iOS, macOS, watchOS, tvOS, or visionOS target builds.
- Do not install dependencies, change resolved versions, accept licenses, unlock keychains, or access credentials during read-only review without explicit approval.
- A cancelled CI run may indicate timeout or infrastructure failure; inspect it rather than treating it as passed or irrelevant.

# Test Finding Contract

For each missing or weak test include test type, scenario, setup, action, expected assertion, why it matters, and the defect or regression it would catch.

# Configuration Finding Contract

Include variable, setting, entitlement, capability, package, certificate reference, or placeholder name; source; consumer; expected format without a value; validation; and ownership.

# Ownership Boundaries

- This Skill owns proof of buildability, test execution, dependency resolution, configuration completeness, signing-input discovery, CI interpretation, and release evidence.
- `inspect-swift-correctness` owns language-level behavior found while interpreting compiler or test failures.
- `assess-apple-security-privacy` owns security and privacy impact in entitlements, manifests, dependencies, and signing configuration.
- `assess-apple-runtime-quality` owns measured runtime impact; this Skill owns whether performance evidence and tests exist and ran.

# Stop Conditions

State insufficient evidence when required schemes, generated projects, private dependencies, credentials, signing assets, simulators, devices, backend services, or CI logs are inaccessible. Never infer release readiness from source inspection alone.
