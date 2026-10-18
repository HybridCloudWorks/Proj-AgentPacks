# Conditional Repository Overrides Preserved from the Source Draft

Load this file only when the repository contains the named files, commands, or conditions. These are not universal Apple-review rules.

## Input Inventory Routing

When `CHECKLIST.md` does not exist but `MOBILE_IMPLEMENTATION_LEDGER.md` does:

- Report the missing standard inventory file as documentation impact.
- Respect the ledger as the repository's current source of truth.
- Do not create, migrate, or rename the file during a read-only review.
- Route any change proposal as engineering work or a human decision according to repository ownership.

## Linux Review Environment

When the current environment is Linux without Swift or Xcode:

- Do not claim `swift test`, `xcodebuild`, XCTest, XCUITest, simulator, device, signing, archive, or App Store validation ran.
- If `tools/check-swift-static.py` exists, it may be run as non-destructive static validation.
- If the repository contains a wiki build and `tools/check-wiki-links.py`, run them only when the reviewed change affects that path.
- Treat macOS CI as the authority for Apple app build and test claims.

## Cancelled CI

A cancelled CI run is not automatically neutral. Inspect whether a step hit `timeout-minutes`, exhausted resources, was superseded, or was manually cancelled. A timeout can carry the same release risk as an explicit failure.

## Dot-Folder Rationale

The source draft recorded historical examples of a dead release workflow and a wiki-publish injection surface under `.github/`. Treat these as rationale for the exception to blanket exclusion, not as verified current findings. Inspect `.github/` when CI, release, secrets, or supply-chain behavior is relevant.
