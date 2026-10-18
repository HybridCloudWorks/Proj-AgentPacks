# Worked example: review an Apple pull request

Synthetic fixture. The app, paths, commit hashes, CI runs and command output are illustrative. They show the workflow and the report format; they are not observed results.

- Prompt: `review-apple-pull-request.prompt.md`
- Skills: `review-apple-code`, `inspect-swift-correctness`, `assess-apple-runtime-quality`, `assess-apple-ui-accessibility`, `verify-apple-build-tests`
- Outcome: Changes requested

## Request

"Review PR #482 in Fieldbook and tell me whether it can merge."

Fieldbook is a SwiftUI iOS app with an iOS 17.0 deployment target. The pull request syncs the user's saved searches to their account so they appear on every device.

## How the review ran

1. **Scope first.** The reviewer resolved base `4f1c2ab` on `main` and head `9d07e3e` with `git merge-base` and `git diff --stat`, read the pull-request description, and recorded four changed files. The build settings give Swift 6 language mode. No crash logs or traces were supplied, so the scope lists them as unavailable before any finding is written.

2. **Toolchain.** `verify-apple-build-tests` ran its bundled detector on the reviewer's macOS host: `can_run_xcodebuild: yes`. The reviewer read `.github/workflows/ci.yml` only to copy the scheme and simulator destination instead of guessing them; no CI file changed in the pull request.

3. **Architecture.** The new `SavedSearchStore` actor owns the upload queue, and the main-actor `SearchViewModel` owns presentation state. This matches the existing `NotesStore` pattern, so no architecture concern was recorded.

4. **Routing.** Only the Skills the diff reaches were activated:

   | Changed file | Skill |
   |---|---|
   | `Fieldbook/Search/SavedSearchStore.swift` (new) | `inspect-swift-correctness` |
   | `Fieldbook/Search/SearchViewModel.swift` | `inspect-swift-correctness`, `assess-apple-runtime-quality` |
   | `Fieldbook/Search/SavedSearchList.swift` | `assess-apple-ui-accessibility` |
   | `FieldbookTests/SavedSearchStoreTests.swift` | `verify-apple-build-tests` |

   `assess-apple-security-privacy` was not activated. The upload reuses the existing authenticated `APIClient`, and the change adds no credential, storage, permission or entitlement. The report says so under Security and Privacy.

5. **Actor state across a suspension point.** `inspect-swift-correctness` traced `sync()`:

   ```swift
   func sync() async throws {
       guard !pending.isEmpty else { return }
       try await api.upload(pending)   // the actor can run enqueue(_:) here
       pending.removeAll()             // removes items that were never uploaded
   }
   ```

   Actors are reentrant, so a save made during the upload is appended and then removed. That became ACR-001.

6. **One root cause, two Skills.** `inspect-swift-correctness` found that each `.onAppear` starts another unstructured `Task` without cancelling the last one. `assess-apple-runtime-quality` independently found repeated uploads on every tab switch. Both describe one root cause, so the report has one finding, ACR-002, that cites both consequences.

7. **Examined and not reported.** `SavedSearch` holds only value types and is `Sendable`, so calling the actor from the main-actor view model is correctly isolated. The name `startSync()` is a style preference, not a risk.

8. **Validation.** The reviewer ran the narrowest discovery command, then the full test command the CI uses, and checked that the CI run belonged to the head commit.

The reviewer returned this report.

---

# Apple Code Review Report

## Executive Summary

- Overall code health: The feature is well structured and the existing suite passes, but the sync queue can lose saved searches and each appearance of the list starts another sync.
- Highest-risk findings: ACR-001 (High), ACR-002 (Medium).
- Release readiness: Not ready to merge. The required fixes are engineering work with no human blockers.
- Evidence limitations: No test exercises enqueue during a sync. Whether the upload endpoint is idempotent was not inspected. Nothing was run on a physical device.

## Review Scope

- Review target: PR #482 "Sync saved searches", base `4f1c2ab`, head `9d07e3e`.
- Files and components reviewed: `Fieldbook/Search/SavedSearchStore.swift` (new), `Fieldbook/Search/SearchViewModel.swift`, `Fieldbook/Search/SavedSearchList.swift`, `FieldbookTests/SavedSearchStoreTests.swift`; `Fieldbook/Search/SearchTab.swift` and `Fieldbook/Networking/APIClient.swift` read for context.
- Technologies and platforms: Swift 6 language mode, SwiftUI, Swift concurrency (actor, unstructured `Task`), XCTest; iOS 17.0 and later.
- Change type: Feature.
- Primary risk areas: Actor state across suspension points, task lifetime, list identity.
- Constraints and exclusions: Read-only review. `.github/workflows/ci.yml` read only to copy the scheme and destination. The server API was not reviewed.
- Not verifiable from available context: Whether `POST /v1/saved-searches` is idempotent; behavior on physical devices and slow networks.

## Findings Summary

`Critical: 0 | High: 1 | Medium: 2 | Low: 1`

## Detailed Findings

### ACR-001 - Saved searches added during an upload are dropped from the sync queue

- **Severity:** High
- **Label:** Confirmed Issue
- **File:** `Fieldbook/Search/SavedSearchStore.swift`
- **Location:** `SavedSearchStore.sync()`, lines 41-46
- **Category:** Correctness and Logic
- **Confidence:** High
- **Description:** `sync()` uploads `pending`, suspends at `await api.upload(_:)`, then calls `pending.removeAll()`. The actor is reentrant, so `enqueue(_:)` can run during the suspension, and whatever it appends is removed without having been uploaded.
- **Evidence:** `try await api.upload(pending)` followed by `pending.removeAll()`. `SearchViewModel.save(_:)` calls `enqueue(_:)` on every save with no check for an in-flight sync.
- **Trigger or reproduction:** Save a search, then save another before the first upload completes. A slow network makes this common.
- **Expected behavior:** Every saved search stays in `pending` until an upload that contains it succeeds.
- **Observed or likely behavior:** The second search is removed from `pending` and never uploaded. It exists only on the device that created it.
- **Impact:** Silent loss of user data from sync. The user sees the search locally and assumes it synced.
- **Recommendation:** Remove only the items that were part of the uploaded batch.
- **Suggested fix:** Take `let batch = pending` before the `await`, upload `batch`, then remove only those items: `let uploaded = Set(batch.map(\.id)); pending.removeAll { uploaded.contains($0.id) }`.
- **Validation needed:** A unit test with a fake `SavedSearchAPI` whose `upload` suspends on a continuation the test controls: start `sync()`, enqueue a second search during the suspension, resume, and assert the second search is still pending. Rerun the full test command.
- **Risk if unfixed:** Users with more than one device intermittently lose saved searches, with no error and no log.

### ACR-002 - Each appearance of the list starts another sync task and repeats the upload

- **Severity:** Medium
- **Label:** Confirmed Issue; Requires Validation
- **File:** `Fieldbook/Search/SearchViewModel.swift`; `Fieldbook/Search/SavedSearchList.swift`
- **Location:** `SearchViewModel.startSync()`; the `.onAppear` modifier in `SavedSearchList.body`
- **Category:** Correctness and Logic (runtime impact merged from Performance and Energy)
- **Confidence:** High for the duplicate tasks; Medium for duplicate server records
- **Description:** `.onAppear` calls `startSync()`, which assigns a new unstructured `Task` to `syncTask` without cancelling the previous one, and nothing cancels it when the view disappears. Switching tabs twice during a slow upload leaves two `sync()` calls interleaved on the actor, and both upload the same pending items.
- **Evidence:** `syncTask = Task { try? await store.sync(); await refresh() }` with no `syncTask?.cancel()` and no `.onDisappear`. `SearchTab` hosts the list in a `TabView`, so `onAppear` runs on every tab switch.
- **Trigger or reproduction:** With saved searches pending and a slow network, switch away from the Search tab and back.
- **Expected behavior:** At most one sync in flight, tied to the lifetime of the screen that started it.
- **Observed or likely behavior:** Two or more concurrent uploads of the same batch; extra network and radio time on a frequent interaction; duplicate server records if the endpoint is not idempotent.
- **Impact:** Wasted network and energy, and possible duplicate saved searches on the user's other devices.
- **Recommendation:** Make sync single-flight and let SwiftUI own its lifetime.
- **Suggested fix:** Replace `.onAppear { viewModel.startSync() }` with `.task { await viewModel.sync() }`, which SwiftUI cancels when the view disappears, and have `SavedSearchStore` hold the in-flight sync task and return its result when `sync()` is called again before it finishes.
- **Validation needed:** A unit test that calls `sync()` twice concurrently against the suspending fake and asserts one upload. Ask the backend owner whether the upload endpoint is idempotent.
- **Risk if unfixed:** Duplicate uploads grow with tab switching. Once ACR-001 is fixed, this becomes the main sync defect.

### ACR-003 - Saved-search rows use the name as identity, and names are not unique

- **Severity:** Medium
- **Label:** Confirmed Issue
- **File:** `Fieldbook/Search/SavedSearchList.swift`
- **Location:** `ForEach(viewModel.searches, id: \.name)` in `SavedSearchList.body`
- **Category:** UI and Accessibility
- **Confidence:** High
- **Description:** SwiftUI requires identifiers to be unique within a `ForEach`. `SavedSearch` already conforms to `Identifiable` with a `UUID`, but the list keys rows by `name`, and `SavedSearchStore.add(_:)` accepts duplicate names.
- **Evidence:** `id: \.name` in the `ForEach`; no uniqueness check in `add(_:)` or in the save sheet.
- **Trigger or reproduction:** Save two searches named "Trailheads", then pin, rename or delete one of them. iOS 17.0 and later, iPhone and iPad.
- **Expected behavior:** Each row keeps its own state and animation, and the row the user acts on is the row that changes.
- **Observed or likely behavior:** SwiftUI warns at runtime that the ID occurs more than once and the result is undefined. Rows can show each other's content, and per-row state can attach to the wrong row.
- **Impact:** Users act on one row and see another change. VoiceOver focus can land on the wrong row after an update.
- **Recommendation:** Use the model's stable identifier.
- **Suggested fix:** `ForEach(viewModel.searches)`, which uses `SavedSearch.id`.
- **Validation needed:** A UI test that creates two searches with the same name, deletes the second, and asserts the first remains with its own subtitle. A manual VoiceOver pass over the list, not run in this review.
- **Risk if unfixed:** Intermittent wrong-row behavior that is hard to reproduce from bug reports.

### ACR-004 - Sync failures are discarded without a log or user signal

- **Severity:** Low
- **Label:** Recommended Improvement
- **File:** `Fieldbook/Search/SearchViewModel.swift`
- **Location:** `try? await store.sync()` in `startSync()`
- **Category:** Error Handling and Observability
- **Confidence:** High
- **Description:** `try?` discards every sync error. Pending items survive a failed upload, so the next sync retries them, but nothing records that a sync failed or why.
- **Evidence:** `try? await store.sync()`; the view model has no `Logger` call and no error state.
- **Trigger or reproduction:** Any upload failure: offline, expired session or server error.
- **Expected behavior:** Failures are logged with a stable event name and safe context, and persistent failure is visible to the user.
- **Observed or likely behavior:** Silent failure. Support cannot tell a sync that never ran from one that failed.
- **Impact:** Slower diagnosis of sync problems; users are not told their searches are not syncing.
- **Recommendation:** Catch the error, log it and expose a sync status.
- **Suggested fix:** Replace `try?` with `do`/`catch`; in the catch, set a `syncState` the list can show and log a stable event name with the existing sync `Logger`, leaving interpolated values at the default private level.
- **Validation needed:** A unit test asserting `syncState` is `.failed` after a throwing fake. Check that log output contains no saved-search names.
- **Risk if unfixed:** Sync failures go unnoticed until users report missing searches.

## Category Results

### Architecture

No architecture concerns were identified from the available context.

### Code Quality

Names, unit size and structure follow the existing `NotesStore` pattern. No finding.

### Correctness and Logic

ACR-001 and ACR-002. `SavedSearch` contains only value types and is `Sendable`, and calls from the main-actor view model into the actor are correctly isolated.

### UI and Accessibility

ACR-003. Swipe actions use labelled `Button`s, and rows use `.body` text with no fixed heights, so Dynamic Type is unaffected.

### Security and Privacy

Not applicable. The upload uses the existing authenticated `APIClient` and sends only search names and filters the user created. The change adds no credential, storage, permission, entitlement or SDK, so `assess-apple-security-privacy` was not activated.

### Performance and Energy

The repeated uploads are merged into ACR-002. No other work was added to a frequent path.

### Error Handling and Observability

ACR-004.

### Tests

Commands run on the macOS host. The scheme and destination were copied from `.github/workflows/ci.yml`.

| Command | Exit | Result |
|---|---|---|
| `python3 scripts/detect_apple_toolchain.py --root ~/src/fieldbook --format markdown` (from the `verify-apple-build-tests` Skill directory) | 0 | macOS; `can_run_xcodebuild: yes`, `can_run_apple_ui_tests: yes` |
| `xcodebuild -list -json -workspace Fieldbook.xcworkspace` | 0 | Schemes `Fieldbook` and `FieldbookUITests` |
| `xcodebuild test -workspace Fieldbook.xcworkspace -scheme Fieldbook -destination 'platform=iOS Simulator,name=iPhone 15'` | 0 | 212 tests, 0 failures |

CI: `ci.yml` job `build-and-test` succeeded for head `9d07e3e`.

The new `SavedSearchStoreTests` cover enqueue and one successful sync only. Missing tests:

| Type | Scenario | Setup | Action | Expected assertion | Why it matters | Catches |
|---|---|---|---|---|---|---|
| Concurrency unit | Enqueue during upload | Fake API whose `upload` suspends until the test resumes it | Start `sync()`, enqueue a second search, resume | The second search is still pending | Reentrancy is the main risk in the new actor | ACR-001 |
| Concurrency unit | Overlapping syncs | Same fake, two pending items | Call `sync()` twice concurrently | Exactly one upload call | Proves single-flight | ACR-002 |
| UI | Duplicate names | Two searches with the same name | Delete the second | The first row remains with its own subtitle | Guards list identity | ACR-003 |

### Dependencies and Configuration

Not applicable. No project, package, lockfile, entitlement, Info.plist or CI file changed.

## Documentation Impact

- `README.md` updates: None.
- `CHANGELOG.md` entries: After the required fixes merge, under Unreleased: "Saved searches now sync across your devices."
- `REVIEW.md` human blockers: None.
- `TODO.md` engineering actions: Fix ACR-001, ACR-002 and ACR-003; ACR-004 recommended; add the three tests listed under Tests; confirm upload idempotency with the backend owner.
- `CHECKLIST.md` input entries: None. The change adds no configuration input.

## Merge or Release Recommendation

**Changes requested.** ACR-001 silently drops user data from sync, and ACR-002 repeats uploads on a frequent interaction. Both are engineering fixes with clear tests, and no human decision is pending.

## Engineer Handoff Notes

- Current state: Head `9d07e3e` builds, and 212 existing tests pass locally and in CI. The new sync path has no concurrency tests.
- Highest risks: ACR-001 (lost saved searches), ACR-002 (repeated uploads).
- Required fixes: ACR-001, ACR-002, ACR-003. ACR-004 is recommended.
- Suggested work order: ACR-001 first, because the single-flight change in ACR-002 builds on the batch snapshot; then ACR-002 and the two concurrency tests; then ACR-003 and ACR-004.
- Validation requirements: The three new tests pass; rerun the `xcodebuild test` command above on macOS; on a device with a throttled network, confirm that switching tabs does not repeat uploads.
- Human blockers: None.
- Configuration dependencies: None.
