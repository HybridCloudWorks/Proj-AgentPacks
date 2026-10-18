---
description: "Establish what an Apple change can be built and tested with here, and interpret its CI evidence"
agent: apple-code-reviewer
---

# Verify Apple build, test and CI evidence

## Inputs

- The repository root and the changed Xcode project or workspace, Swift package, dependency, configuration, test or CI files.
- Intended schemes and destinations, and the Xcode and Swift versions the repository or CI selects, when they are stated.
- Optional: CI run links or logs, test result bundles, signing ownership and release requirements.

## Workflow

1. Activate `review-apple-code` and state that the review focuses on build, test and CI evidence.
2. Apply `verify-apple-build-tests`. Run its bundled toolchain detector first and keep the report it prints.
3. Select only commands that the detected environment and the repository support, starting with the narrowest read-only discovery. Do not guess schemes, destinations or signing flags. Record each command, its exit status and the relevant output.
4. Compare the working tree before and after any package command, and stop before any command that would rewrite a lockfile.
5. Do not install dependencies, change resolved versions, accept licenses, unlock keychains, or use credentials or signing assets.
6. Inspect CI conclusions, including cancelled, timed-out, skipped and allowed-to-fail jobs, and confirm that each run belongs to the commit under review. A cancelled run is not a pass.
7. Describe each missing or weak test by type, scenario, setup, action, expected assertion and the regression it would catch.

## Expected output

The review report the contract requires. Its Tests and its Dependencies and Configuration results list the detected toolchain, each command actually run with its exit status, verified passes, observed failures, validation that could not run here, and the exact validation still required on macOS or protected infrastructure. Without macOS and the required Xcode, make no claim about Apple app builds, simulator or device tests, signing or archives. Follow the `apple-code-reviewer-contract` instruction.
