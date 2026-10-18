# Worked example: audit AI-generated Apple code

Synthetic fixture. The package, paths, commit hashes and command output are illustrative. They show the workflow and the report format; they are not observed results.

- Prompt: `audit-ai-generated-apple-code.prompt.md`
- Skills: `review-apple-code`, `inspect-swift-correctness`, `verify-apple-build-tests`, `assess-apple-security-privacy`, `assess-apple-runtime-quality`
- Outcome: Changes requested

## Request

"A coding assistant wrote CSV export for LedgerKit. It says everything builds and all tests pass. Audit it before I open a pull request."

LedgerKit is a Foundation-only Swift package declaring `.iOS(.v16)` and `.macOS(.v13)`; the Ledger iOS and macOS apps in the same repository depend on it. The assistant's summary made five claims: "builds cleanly", "all tests pass", "handles all edge cases, including special characters", "thread-safe and fast through concurrent processing", and "works on iOS and macOS".

## How the review ran

1. **Claims become scope.** `review-apple-code` recorded the change type as an audit of AI-generated code and listed each claim as unverified before any analysis.

2. **Toolchain.** The reviewer worked in a Linux dev container. The detector reported `can_run_swift_package_commands: yes` and `can_run_xcodebuild: no`. The Linux-environment repository override therefore applied: no claim about Xcode, the app targets or Apple's Foundation. The repository has no `tools/check-swift-static.py`, so the optional static check was not run.

3. **Package validation without changing the tree.** LedgerKit has no dependencies, so there was nothing to resolve. The reviewer recorded `git status --porcelain` before and after `swift build` and `swift test`, and the tree stayed clean.

4. **Routing.**

   | Area | Skill | Why |
   |---|---|---|
   | `CSVExporter.swift` logic and concurrency | `inspect-swift-correctness` | New Swift behavior with a task group and `@unchecked Sendable` |
   | Build, tests and the "tests pass" claim | `verify-apple-build-tests` | Claims about builds and tests |
   | Export writes user data to a file | `assess-apple-security-privacy` | File output of personal financial data |
   | "Fast through concurrent processing" | `assess-apple-runtime-quality` | Performance claim |

   `assess-apple-ui-accessibility` was not activated, because no UI code was generated.

5. **Suppressed compiler checks.** `inspect-swift-correctness` gives extra attention to `@unchecked Sendable`, because it turns off the diagnostic that would catch the generated pattern:

   ```swift
   final class CSVExporter: @unchecked Sendable {
       private var rows: [String] = []

       func export(_ records: [ExpenseRecord]) async -> String {
           rows = [Self.header]
           await withTaskGroup(of: Void.self) { group in
               for record in records {
                   group.addTask { self.rows.append(self.makeRow(record)) }
               }
           }
           return rows.joined(separator: "\n")
       }
   }
   ```

6. **Nearby patterns.** The generated `dateString(_:)` duplicates `DayFormatting.isoDay(_:)`, which `JSONExporter` already uses. The duplicate omits the locale, calendar and time zone the existing helper pins, so the duplication is a correctness risk and is reported (ACR-003). Duplication alone would not have been.

7. **Examined and not reported.** `csv.data(using: .utf8)!` looks like a risky force unwrap, but encoding a Swift `String` as UTF-8 does not fail, so it is not a finding. Merchant names and notes are typed by the user in this app, and the repository has no import path, so spreadsheet formula injection has no external source here; it was considered and not reported.

The reviewer returned this report.

---

# Apple Code Review Report

## Executive Summary

- Overall code health: The generated exporter compiles and its single test passes on Linux, but it races on shared state, writes malformed CSV for ordinary merchant names, and formats dates using the device calendar.
- Highest-risk findings: ACR-001 (High), ACR-002 (High).
- Release readiness: Not ready for a pull request. All fixes are engineering work.
- Evidence limitations: Linux only. Apple's Foundation, the iOS and macOS app targets, and Xcode were not available, so nothing about them was built or tested.

## Review Scope

- Review target: Branch `feature/csv-export`, head `b7e2d41`, against `main` at `e03a9c5`.
- Files and components reviewed: `Sources/LedgerKit/Export/CSVExporter.swift` (new), `Tests/LedgerKitTests/CSVExporterTests.swift` (new); `Sources/LedgerKit/Model/ExpenseRecord.swift`, `Sources/LedgerKit/Formatting/DayFormatting.swift` and `Sources/LedgerKit/Export/JSONExporter.swift` read for context.
- Technologies and platforms: Swift package with Foundation only; platforms iOS 16 and macOS 13; consumed by the Ledger apps.
- Change type: Audit of AI-generated code. Generator claims checked:
  - "Builds cleanly": observed for the package on Linux (`swift build`, exit 0); the app targets were not built.
  - "All tests pass": observed, but weak (`swift test`, exit 0, one test that asserts only the header row).
  - "Handles all edge cases, including special characters": contradicted by ACR-002.
  - "Thread-safe and fast through concurrent processing": thread safety contradicted by ACR-001; no measurement supports "fast".
  - "Works on iOS and macOS": not verifiable here.
- Primary risk areas: Concurrency under `@unchecked Sendable`, CSV escaping, date formatting, test adequacy.
- Constraints and exclusions: Read-only audit; no tests were added to reproduce findings. The app targets did not change and were not reviewed.
- Not verifiable from available context: Behavior with Apple's Foundation on iOS and macOS; export time for large ledgers.

## Findings Summary

`Critical: 0 | High: 2 | Medium: 1 | Low: 0`

## Detailed Findings

### ACR-001 - Task-group children append to a shared array without synchronization

- **Severity:** High
- **Label:** Confirmed Issue
- **File:** `Sources/LedgerKit/Export/CSVExporter.swift`
- **Location:** `CSVExporter.export(_:)`, the `withTaskGroup` block; the class declaration `final class CSVExporter: @unchecked Sendable`
- **Category:** Correctness and Logic
- **Confidence:** High
- **Description:** Every child task calls `self.rows.append(_:)` on the same stored array. Child tasks run concurrently, so the appends race. `@unchecked Sendable` removed the compiler diagnostic that would have rejected capturing mutable `self` in the task closures.
- **Evidence:** `group.addTask { self.rows.append(self.makeRow(record)) }`; `private var rows: [String]`; no lock, actor or other synchronization.
- **Trigger or reproduction:** Export more than a few records on a multi-core device. Larger ledgers make it more likely.
- **Expected behavior:** One row per record, in record order, every time.
- **Observed or likely behavior:** Rows in nondeterministic order, lost rows, or a crash when concurrent appends reallocate the array's storage.
- **Impact:** Exported files silently miss or reorder expenses, or the export crashes.
- **Recommendation:** Remove the concurrency. Formatting strings in memory gains nothing from it here.
- **Suggested fix:** Make `CSVExporter` a struct with no stored mutable state, drop `@unchecked Sendable`, and build the output directly: `([Self.header] + records.map(makeRow)).joined(separator: "\n")`.
- **Validation needed:** A unit test that exports 10,000 records and asserts 10,001 lines in input order, run with `swift test --sanitize=thread` here and with the package tests in Xcode on macOS.
- **Risk if unfixed:** Intermittent data loss in exports that no current test detects.

### ACR-002 - Fields are joined without CSV quoting

- **Severity:** High
- **Label:** Confirmed Issue
- **File:** `Sources/LedgerKit/Export/CSVExporter.swift`
- **Location:** `CSVExporter.makeRow(_:)`
- **Category:** Correctness and Logic
- **Confidence:** High
- **Description:** `makeRow` joins the merchant, category and note with commas and never quotes a field that contains a comma, a double quote or a line break.
- **Evidence:** `[day, record.merchant, record.category.name, record.note, amount].joined(separator: ",")`. `merchant` and `note` are free text the user types in `ExpenseEditor`.
- **Trigger or reproduction:** Export a record whose merchant is `Smith, Jones & Co`, or whose note contains a line break.
- **Expected behavior:** Each record is one CSV row of five fields that spreadsheet and accounting software read correctly.
- **Observed or likely behavior:** Extra columns and split rows. Importing the file shifts amounts into the wrong columns.
- **Impact:** Corrupted exports used for expense claims or bookkeeping.
- **Recommendation:** Quote fields as RFC 4180 describes.
- **Suggested fix:** Add `static func escape(_ field: String) -> String` that wraps the field in double quotes, doubling any embedded quote, whenever it contains a comma, a double quote, a carriage return or a line feed. Apply it to every text field.
- **Validation needed:** Unit tests for fields with a comma, a quote and a line break that parse the output back and compare field by field.
- **Risk if unfixed:** Users send corrupted files to third parties and stop trusting the export.

### ACR-003 - Date column follows the device calendar and time zone, duplicating an existing helper

- **Severity:** Medium
- **Label:** Confirmed Issue
- **File:** `Sources/LedgerKit/Export/CSVExporter.swift`
- **Location:** `CSVExporter.dateString(_:)`
- **Category:** Correctness and Logic
- **Confidence:** High
- **Description:** The generated helper creates a `DateFormatter` with `dateFormat = "yyyy-MM-dd"` and sets no locale, calendar or time zone. Apple's `DateFormatter` documentation on fixed-format dates says to use the `en_US_POSIX` locale. Without it, a device using a non-Gregorian calendar writes years in that calendar, and days follow the device time zone instead of the day stored with the record. `DayFormatting.isoDay(_:)` already pins all three settings and is used by `JSONExporter`.
- **Evidence:** `let formatter = DateFormatter(); formatter.dateFormat = "yyyy-MM-dd"` on the per-row path; `DayFormatting.swift` lines 8-15.
- **Trigger or reproduction:** Export on a device set to the Buddhist or Japanese calendar, or export in another time zone a record saved just before midnight.
- **Expected behavior:** The same ISO day as the JSON export, for every record.
- **Observed or likely behavior:** The year 2569 instead of 2026 under the Buddhist calendar; days off by one across time zones.
- **Impact:** Wrong dates in exported records, and CSV and JSON exports that disagree.
- **Recommendation:** Reuse the existing helper.
- **Suggested fix:** Replace `dateString(_:)` with `DayFormatting.isoDay(record.date)`. This also removes one formatter allocation per row.
- **Validation needed:** A unit test that exports a record with a fixed date and compares the date column with `JSONExporter` output; run the package tests on macOS as well, because Linux Foundation is not Apple's Foundation.
- **Risk if unfixed:** Locale-dependent wrong data that only some users see.

## Category Results

### Architecture

No architecture concerns were identified from the available context.

### Code Quality

The duplicated date helper is covered by ACR-003. Otherwise the generated exporter follows the shape of `JSONExporter`.

### Correctness and Logic

ACR-001, ACR-002 and ACR-003. `csv.data(using: .utf8)!` was examined and not reported, because UTF-8 encoding of a Swift `String` does not fail.

### UI and Accessibility

Not applicable. No UI code was generated.

### Security and Privacy

Reviewed because the export writes personal financial data to a file. The exporter returns `Data`; the existing app share flow, unchanged by this branch, writes and shares it. No secret, sample credential or placeholder key appears in the generated code. Spreadsheet formula injection was considered and not reported, because every text field is typed by the user on their own device and the repository has no import path.

### Performance and Energy

No measurement supports the "fast" claim. The concurrency is removed by the fix for ACR-001, and the per-row formatter by the fix for ACR-003. Export is a user-initiated, one-off action, so no measurement suggestion is needed.

### Error Handling and Observability

`export(_:)` cannot fail and logs nothing. No finding.

### Tests

Commands run in the Linux container:

| Command | Exit | Result |
|---|---|---|
| `python3 scripts/detect_apple_toolchain.py --root /workspace/ledger --format markdown` (from the `verify-apple-build-tests` Skill directory) | 0 | Linux; `can_run_swift_package_commands: yes`; `can_run_xcodebuild: no` |
| `git status --porcelain` | 0 | Clean before package commands |
| `swift package describe` (in `LedgerKit/`) | 0 | Library `LedgerKit`; test target `LedgerKitTests`; no dependencies |
| `swift build` | 0 | Build complete |
| `swift test` | 0 | 1 test, 0 failures |
| `git status --porcelain` | 0 | Still clean; `.build/` is ignored |

The only generated test, `testExportProducesHeader`, exports an empty array and asserts the header line. Missing tests:

| Type | Scenario | Setup | Action | Expected assertion | Why it matters | Catches |
|---|---|---|---|---|---|---|
| Concurrency unit | Large export | 10,000 records | `export(_:)` under `--sanitize=thread` | 10,001 lines in input order, no sanitizer report | The generator claimed thread safety | ACR-001 |
| Unit | Special characters | Merchant with a comma and a quote, note with a line break | Export and parse back | Fields match the input | The generator claimed edge cases were handled | ACR-002 |
| Unit | Date column | Record with a fixed date | Export CSV and JSON | Same ISO day in both | Guards against locale and time-zone drift | ACR-003 |

### Dependencies and Configuration

`Package.swift` did not change. No dependency or configuration input was added.

## Documentation Impact

- `README.md` updates: After the fixes, add `CSVExporter` to the exporter list in `LedgerKit/README.md`.
- `CHANGELOG.md` entries: After the fixes merge: "Added CSV export of expense records."
- `REVIEW.md` human blockers: None.
- `TODO.md` engineering actions: Fix ACR-001, ACR-002 and ACR-003; add the three tests above; run the package tests on macOS.
- `CHECKLIST.md` input entries: None.

## Merge or Release Recommendation

**Changes requested.** Two High defects contradict the generator's claims about edge cases and thread safety. The fixes are small and testable, and no human decision is needed.

## Engineer Handoff Notes

- Current state: The package builds and its single test passes on Linux. Nothing was built or tested on macOS. Three defects are open, and two of the five generator claims are contradicted.
- Highest risks: ACR-001 (lost or reordered rows), ACR-002 (malformed CSV).
- Required fixes: ACR-001, ACR-002, ACR-003.
- Suggested work order: ACR-001 first, because turning the exporter into a pure function simplifies the other two fixes; then ACR-002 and ACR-003; then the three tests.
- Validation requirements: The three tests pass with `swift test --sanitize=thread` in Linux; the package tests pass in Xcode on macOS for iOS and macOS destinations; a manual export from the iOS app opens correctly in a spreadsheet.
- Human blockers: None.
- Configuration dependencies: None.
