# Worked example: release readiness blocked by missing evidence

Synthetic fixture. The app, package, paths, commit hashes, CI runs and command output are illustrative. They show the workflow and the report format; they are not observed results. This example shows a Blocked outcome: nothing could be built or tested, and the reviewer says so instead of inferring readiness.

- Prompts: `assess-apple-release-readiness.prompt.md`, with the build and CI steps of `verify-apple-build-and-ci.prompt.md`
- Skills: `review-apple-code`, `verify-apple-build-tests`, `assess-apple-security-privacy`, `inspect-swift-correctness`
- Outcome: Blocked

## Request

"Is `release/3.2.0` of Tidewater ready to submit to the App Store? CI keeps getting cancelled. It's probably just flaky."

Tidewater is an iOS tide-chart app with a widget extension. The previous release was tagged `v3.1.0`.

## How the review ran

1. **Scope is the range.** `review-apple-code` set the change type to release review for `v3.1.0..release/3.2.0`: 37 commits, head `a41e9c0`. The feature commits in the range were each merged through a reviewed pull request (#401 to #433), so this review covered release configuration and evidence and listed the feature code as an exclusion.

2. **Toolchain.** The reviewer worked in a Linux container with no Swift toolchain. The detector printed:

   ```text
   ## Capabilities

   - can_inspect_source: yes
   - can_run_xcodebuild: no
   - can_run_swift_package_commands: no
   - can_run_apple_ui_tests: no
   - can_validate_signing_or_archive: no

   ## Limitations

   - Apple app builds, simulator/device tests, signing, archives, and XCUITest are not authoritative without macOS and Xcode.
   - No Swift toolchain was detected; Swift build and test commands are unavailable.
   ```

   The Linux-environment repository override applied: no build, test, signing or archive claim of any kind. The repository has no `tools/check-swift-static.py`.

3. **Cancelled CI is not neutral.** The user called the cancellations flaky. Following the cancelled-CI repository override, the reviewer opened the runs instead of discounting them. All three `release.yml` runs for the branch stopped at exactly 30 minutes, during package resolution, with the runner's maximum-execution-time message. The last successful release run, for `v3.1.0`, took 41 minutes. Reading `.github/workflows/release.yml` was justified because release behavior is in scope; the diff showed the timeout lowered from 60 to 30 minutes. That became ACR-001.

4. **Secret handling.** `Config/Shared.xcconfig` gained a literal map-service key. The reviewer wrote it as `[REDACTED_POSSIBLE_SECRET]` in notes and report, and recorded only the file and variable name. Whether to rotate it depends on how the key is restricted, which only its owner knows, so the finding carries `Human Blocker`.

5. **Supported risk, not missing evidence.** The ChartKit upgrade crosses a major version and has never been built, because every CI run was cancelled first. Missing evidence is not itself a defect, so ACR-003 states the supported risk (a source-breaking major upgrade with unchanged call sites) and labels it `Requires Validation`.

6. **Decisions only people can make.** Raising the deployment target from iOS 16.0 to 17.0 drops users who cannot upgrade. No decision record or changelog entry mentions it, and an engineer cannot decide support policy, so ACR-004 is a `Human Blocker`.

7. **Not activated.** `assess-apple-ui-accessibility` and `assess-apple-runtime-quality` were not activated. The release-configuration changes do not reach their areas, and the feature code was excluded. The report says so.

The reviewer returned this report.

---

# Apple Code Review Report

## Executive Summary

- Overall code health: Not established. No build or test result exists for the release candidate.
- Highest-risk findings: ACR-001 (High), ACR-002 (Medium, human blocker), ACR-004 (Medium, human blocker).
- Release readiness: Not established. Blocked on missing build and test evidence and on two owner decisions.
- Evidence limitations: No macOS, Xcode or Swift toolchain in this environment. Every release CI run for the candidate was cancelled before building. No archive, App Store Connect or device access. The feature commits were excluded because each was reviewed in its own pull request.

## Review Scope

- Review target: Release candidate `release/3.2.0`, head `a41e9c0`, compared with tag `v3.1.0` at `5be0d13` (37 commits).
- Files and components reviewed: `.github/workflows/release.yml`, `Config/Shared.xcconfig`, `Tidewater/Info.plist`, `Tidewater.xcodeproj/project.pbxproj` (deployment targets and package references), `Tidewater.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`, `CHANGELOG.md`; `Tidewater/Charts/TideChartView.swift` and `Tidewater/Maps/MapTileClient.swift` read for context.
- Technologies and platforms: Xcode project with Swift Package Manager dependencies, xcconfig layering, GitHub Actions; iOS app and widget extension.
- Change type: Release.
- Primary risk areas: Release CI, committed credentials, a major dependency upgrade, the supported-OS change.
- Constraints and exclusions: Read-only. No signing, archiving, uploading or release-setting changes. Feature code excluded as stated above. `.github/` inspected because release behavior is in scope.
- Not verifiable from available context: Whether the app and widget build against ChartKit 5.0.0; any test result; archive and signing; whether the map key is restricted; whether dropping iOS 16 was approved.

## Findings Summary

`Critical: 0 | High: 1 | Medium: 3 | Low: 0`

## Detailed Findings

### ACR-001 - The release job's time limit is shorter than the job, so every run is cancelled

- **Severity:** High
- **Label:** Confirmed Issue
- **File:** `.github/workflows/release.yml`
- **Location:** Job `build-and-test`, `timeout-minutes: 30`, changed in commit `c19f2e7`
- **Category:** Dependencies and Configuration
- **Confidence:** High
- **Description:** Commit `c19f2e7` lowered the job's time limit from 60 to 30 minutes. The last successful release run took 41 minutes, and the ChartKit upgrade adds package-resolution time. All three release runs for the candidate were cancelled at the limit, before any build or test step ran.
- **Evidence:** Runs 7712, 7724 and 7731 for `release/3.2.0`: conclusion cancelled, duration 30m 0s, last step "Resolve Swift packages", log line "has exceeded the maximum execution time of 30 minutes". Run 7409 for `v3.1.0`: success, 41m 12s.
- **Trigger or reproduction:** Any run of `release.yml`.
- **Expected behavior:** The release job finishes build, tests and archive within its time limit.
- **Observed or likely behavior:** Every run is cancelled, and no build, test or archive evidence exists for the candidate.
- **Impact:** The release cannot be validated. Reading the cancellations as flakiness hides the fact that nothing was tested.
- **Recommendation:** Restore a limit above the observed duration.
- **Suggested fix:** Set `timeout-minutes: 60`. If a shorter limit is wanted, cache package resolution first and measure before lowering it.
- **Validation needed:** A completed `release.yml` run for the fixed head, with build, test and archive steps succeeding.
- **Risk if unfixed:** The team ships without CI evidence, or keeps re-running a job that cannot finish.

### ACR-002 - A map-service key is committed in a tracked configuration file

- **Severity:** Medium
- **Label:** Confirmed Issue; Security Sensitive; Human Blocker
- **File:** `Config/Shared.xcconfig`
- **Location:** `MAPS_API_KEY`, added in commit `8d3a0f2`
- **Category:** Security and Privacy
- **Confidence:** High that a literal value is committed; Low on impact, which depends on how the key is restricted
- **Description:** A literal key was committed to a tracked xcconfig file and flows into Info.plist as `MapsAPIKey`. Its value is shown here as `[REDACTED_POSSIBLE_SECRET]`. A key shipped inside an app bundle can be extracted anyway, so the risk depends on whether the provider restricts it to the app's bundle identifier, which cannot be determined from the repository. Attack surface: repository history and the shipped bundle. Trust boundary: repository readers and app users on one side, the map-provider account on the other. Precondition: read access to the repository or the bundle. Affected: the map account's quota and billing.
- **Evidence:** `MAPS_API_KEY = [REDACTED_POSSIBLE_SECRET]` in `Config/Shared.xcconfig`; `MapsAPIKey = $(MAPS_API_KEY)` in `Tidewater/Info.plist`; `MapTileClient` reads `MapsAPIKey`.
- **Trigger or reproduction:** Anyone with repository access, now or through history.
- **Expected behavior:** Key values come from a CI secret or an untracked configuration file; the repository holds only the variable name.
- **Observed or likely behavior:** The value is in a tracked file and in git history.
- **Impact:** Possible quota abuse or charges against the map account if the key is unrestricted.
- **Recommendation:** Remove the value from tracked files; the key owner decides whether to rotate or restrict it.
- **Suggested fix:** Replace the line with `#include? "Secrets.xcconfig"`, keep `MAPS_API_KEY` in an untracked `Config/Secrets.xcconfig` that CI writes from a secret, and add that file to `.gitignore`.
- **Validation needed:** The release build in CI reads the key from the secret; `git grep MAPS_API_KEY` shows only the variable name; the key owner records the rotation or restriction decision.
- **Risk if unfixed:** A usable key stays in repository history.

### ACR-003 - ChartKit moves to a new major version that has never been built

- **Severity:** Medium
- **Label:** Requires Validation; Potential Risk
- **File:** `Tidewater.xcodeproj/project.pbxproj`; `Tidewater.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`; `Tidewater/Charts/TideChartView.swift`
- **Location:** `XCRemoteSwiftPackageReference "ChartKit"` (minimum version 4.2.0 to 5.0.0); the `LineSeries(points:)` and `ChartAxis.time(_:)` call sites in `TideChartView`
- **Category:** Dependencies and Configuration
- **Confidence:** Medium
- **Description:** The range moves ChartKit across a major version, which may contain source-breaking changes. No commit in the range touches the call sites, and no build has completed with the new version because of ACR-001. Whether the app compiles and draws tide charts as before is unknown.
- **Evidence:** The `Package.resolved` diff changes ChartKit's version and revision; the requirement in `project.pbxproj` changes to 5.0.0; `git log v3.1.0..release/3.2.0 -- Tidewater/Charts/TideChartView.swift` is empty.
- **Trigger or reproduction:** Building the app or the widget against ChartKit 5.0.0.
- **Expected behavior:** The app and widget build, and tide charts render as in 3.1.0.
- **Observed or likely behavior:** Unknown; no build evidence exists.
- **Impact:** A build failure, or changed rendering on the app's main screen and in the widget.
- **Recommendation:** Build and test on macOS before release.
- **Suggested fix:** None until a build result exists. If the build fails, update the call sites to the 5.0.0 API in a separate change.
- **Validation needed:** On macOS with the Xcode version `release.yml` selects: build the `Tidewater` scheme and the widget extension, run the unit and UI tests, compare the tide chart with the 3.1.0 screenshot baseline, and check whether the resolved ChartKit package ships a privacy manifest.
- **Risk if unfixed:** A broken or visibly different main chart reaches users.

### ACR-004 - The minimum iOS version was raised without a recorded decision

- **Severity:** Medium
- **Label:** Human Blocker; Configuration Dependency
- **File:** `Tidewater.xcodeproj/project.pbxproj`
- **Location:** `IPHONEOS_DEPLOYMENT_TARGET` for targets `Tidewater` and `TidewaterWidgets`, commit `e7a4c88`
- **Category:** Dependencies and Configuration
- **Confidence:** High that the setting changed; whether it was approved is unknown
- **Description:** The deployment target rose from iOS 16.0 to iOS 17.0 for the app and the widget. Users whose devices cannot run iOS 17 stop receiving updates. Neither the commit message nor the 3.2.0 changelog mentions it, and no decision record was found.
- **Evidence:** Four `IPHONEOS_DEPLOYMENT_TARGET = 16.0;` lines become `17.0;` (Debug and Release, both targets); the 3.2.0 section of `CHANGELOG.md` has no platform entry.
- **Trigger or reproduction:** Releasing 3.2.0.
- **Expected behavior:** A change to supported OS versions is approved by the product owner and announced in the release notes.
- **Observed or likely behavior:** iOS 16 support is dropped without notice.
- **Impact:** Some users lose updates without warning.
- **Recommendation:** The product owner confirms or reverts the change.
- **Suggested fix:** If confirmed, add changelog and release-notes entries. If not, restore 16.0 and check the range for APIs that need iOS 17.
- **Validation needed:** The owner's decision is recorded. If reverted, the app builds on macOS with the iOS 16.0 target.
- **Risk if unfixed:** An unplanned loss of a user segment.

## Category Results

### Architecture

Not reviewed. The feature commits in the range were reviewed in their own pull requests; this review covers release configuration and evidence.

### Code Quality

Not reviewed, for the same reason.

### Correctness and Logic

Limited to the ChartKit call sites, covered by ACR-003. Without a build, `inspect-swift-correctness` could not confirm them against the 5.0.0 API.

### UI and Accessibility

Not reviewed. No UI test has run for the candidate, and the feature code is excluded.

### Security and Privacy

ACR-002. Entitlements and `PrivacyInfo.xcprivacy` did not change in the range. Whether ChartKit 5.0.0 ships its own privacy manifest could not be checked, because packages were not resolved here; that check is part of the validation for ACR-003.

### Performance and Energy

Not reviewed. No traces were supplied, and the feature code is excluded.

### Error Handling and Observability

Not reviewed, for the same reason.

### Tests

No build or test ran anywhere for the candidate commit. Commands run in the Linux container:

| Command | Exit | Result |
|---|---|---|
| `python3 scripts/detect_apple_toolchain.py --root /workspace/tidewater --format markdown` (from the `verify-apple-build-tests` Skill directory) | 0 | Linux; every Apple capability `no` |
| `git rev-list --count v3.1.0..release/3.2.0` | 0 | 37 |
| `git diff --stat v3.1.0..release/3.2.0` | 0 | 64 files changed |
| `git diff v3.1.0..release/3.2.0 -- .github/workflows/release.yml Config Tidewater/Info.plist Tidewater.xcodeproj CHANGELOG.md` | 0 | The changes described in ACR-001 to ACR-004 |
| `gh run list --workflow release.yml --branch release/3.2.0 --limit 5` | 0 | Runs 7712, 7724, 7731: cancelled |
| `gh run view 7731 --log` | 0 | Stopped at the 30-minute limit during "Resolve Swift packages" |
| `gh run view 7409 --json conclusion,createdAt,updatedAt` | 0 | `v3.1.0` release run: success, 41m 12s |

Nothing in this table is a build or test pass.

### Dependencies and Configuration

ACR-001, ACR-003 and ACR-004. The xcconfig change is reported under Security and Privacy as ACR-002.

## Documentation Impact

- `README.md` updates: After the fix for ACR-002, document `Config/Secrets.xcconfig` and the `MAPS_API_KEY` CI secret in the configuration section.
- `CHANGELOG.md` entries: If ACR-004 is confirmed, add "Requires iOS 17 or later." to the 3.2.0 section.
- `REVIEW.md` human blockers: Rotation or restriction of the map key (owner: map-provider account owner; finding ACR-002; blocks release). Whether 3.2.0 drops iOS 16 (owner: product owner; finding ACR-004; blocks release).
- `TODO.md` engineering actions: Restore the release time limit (ACR-001); move the key to a CI secret and ignore `Config/Secrets.xcconfig` (ACR-002); build and test against ChartKit 5.0.0 on macOS (ACR-003).
- `CHECKLIST.md` input entries:

  | Variable Name | Purpose | Required | Source | Consumer | Expected Format | Validation Status | Notes |
  |---|---|---|---|---|---|---|---|
  | `MAPS_API_KEY` | Authenticates map-tile requests | Yes, for builds that show maps | CI secret written to `Config/Secrets.xcconfig` (proposed) | `Tidewater/Info.plist` `MapsAPIKey`, then `MapTileClient` | `XXXXXXXXXX0000000000XXXXXXXXXX` (length unconfirmed) | Not validated | Treat the committed value as exposed until the owner confirms its restrictions; never commit a value |

## Merge or Release Recommendation

**Blocked.** No build, test or archive result exists for `a41e9c0`: every release run was cancelled by ACR-001, and this environment cannot build Apple targets. Two decisions only people can make are open (ACR-002 and ACR-004). Nothing in this review is a pass, and readiness cannot be judged until release CI completes on macOS.

## Engineer Handoff Notes

- Current state: Nothing has been built or tested for the candidate. Release CI cancels at 30 minutes, and this review ran without any Apple toolchain.
- Highest risks: ACR-001 (no release evidence possible), ACR-003 (unbuilt major upgrade).
- Required fixes: ACR-001 and the engineering part of ACR-002; ACR-003 needs a build result before any fix can be decided.
- Suggested work order: ACR-001 first, because no other validation can run until it is fixed; then the ACR-002 configuration change; then one release run, whose result settles ACR-003; ACR-002 rotation and ACR-004 proceed in parallel with their owners.
- Validation requirements: A completed `release.yml` run for the fixed head on macOS with the Xcode version it selects (build, unit and UI tests, archive), owned by the release engineer; a tide-chart comparison with 3.1.0; recorded decisions for ACR-002 and ACR-004. The reviewer runs none of these, and none of them is signing or upload.
- Human blockers: Map-key rotation or restriction (map-provider account owner); iOS 16 support decision (product owner).
- Configuration dependencies: `MAPS_API_KEY`; `IPHONEOS_DEPLOYMENT_TARGET` for both targets.
