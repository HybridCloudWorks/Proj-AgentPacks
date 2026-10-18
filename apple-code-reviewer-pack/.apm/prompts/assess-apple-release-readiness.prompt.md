---
description: "Assess whether an Apple-platform release candidate has the evidence it needs to ship"
agent: apple-code-reviewer
---

# Assess Apple release readiness

## Inputs

- The release candidate: a branch, tag or commit, and the commit range since the last release.
- The distribution context the user names, such as App Store, TestFlight or direct distribution.
- Evidence for the release configuration: macOS CI runs, test result bundles, archive logs, and the release notes or changelog for the range.
- Changes in the range to entitlements, Info.plist, privacy manifests, deployment targets, signing inputs and dependencies.

## Workflow

1. Activate `review-apple-code` with the change type set to release review, scoped to the commit range.
2. Apply `verify-apple-build-tests` to the release configuration: toolchain detection, CI conclusions for the candidate commit, cancelled or timed-out jobs, test coverage of the changed behavior, deployment targets, configuration inputs and dependency changes.
3. Apply `assess-apple-security-privacy` to entitlement, privacy-manifest, permission, SDK and credential changes in the range, and check current App Review and privacy requirements against its official sources.
4. Apply `inspect-swift-correctness`, `assess-apple-ui-accessibility` and `assess-apple-runtime-quality` only to changes in the range that reach their areas. State which parts of the range you did not review.
5. Never sign, archive, upload, publish or change release settings. Never infer release readiness from reading source alone.

## Expected output

The review report the contract requires, with a release recommendation from the four allowed values. Recommend Approved or Approved with comments only when release-configuration build and test results were observed for the candidate commit. When they are missing, say exactly what must run, where it must run and who owns it. Documentation Impact names the changelog entries the range needs. Follow the `apple-code-reviewer-contract` instruction.
