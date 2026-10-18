# Worked example: runtime-quality review of a thumbnail grid

Synthetic fixture. The app, paths, commit hashes and command output are illustrative. They show the workflow and the report format; they are not observed results. This example shows the evidence threshold at work: plausible risks without measurements become measurement suggestions, not findings.

- Prompt: `review-apple-runtime-quality.prompt.md`
- Skills: `review-apple-code`, `assess-apple-runtime-quality`, `inspect-swift-correctness`, `verify-apple-build-tests`
- Outcome: Approved with comments

## Request

"Can you check the thumbnail grid PR (#77) for performance problems before I merge? It feels smooth on my iPad Pro."

Driftwood is a photo-journal app for iPhone and iPad, iOS 17.0 and later. The pull request shows each journal entry's photo as a thumbnail in a `LazyVGrid`.

## How the review ran

1. **Frequency and scale first.** `assess-apple-runtime-quality` needs a frequency and scale model before judging cost. The pull request description gives the scale (journals of up to 2,000 entries). From the code: 160 x 160 point cells, about 20 to 30 visible at once, and a thumbnail load per cell as it appears during scrolling.

2. **Trace the work.**

   ```swift
   actor ThumbnailLoader {
       private let cache: NSCache<NSString, UIImage> = {
           let cache = NSCache<NSString, UIImage>()
           cache.countLimit = 300
           return cache
       }()

       func thumbnail(for entry: JournalEntry, size: CGSize) async throws -> UIImage {
           let key = entry.id.uuidString as NSString
           if let cached = cache.object(forKey: key) { return cached }
           let data = try await store.imageData(for: entry.id)
           try Task.checkCancellation()
           guard let image = UIImage(data: data)?.preparingThumbnail(of: size) else {
               throw ThumbnailError.decodeFailed
           }
           cache.setObject(image, forKey: key)
           return image
       }
   }
   ```

   The cell starts the load with `.task(id: entry.id)` and logs failures in its `catch`.

3. **Apply the evidence threshold to each candidate.**

   | Candidate | Threshold met? | Outcome |
   |---|---|---|
   | Decoding and downsampling | Expensive work on a latency-sensitive path, but off the main actor. Because it runs inside the actor, decodes are serialized; no measurement shows a problem. | Measurement suggestion |
   | Cache memory | Bounded by `countLimit = 300`, and `NSCache` evicts under memory pressure. Scale model: 320 x 320 pixels x 4 bytes is about 0.4 MB per thumbnail at 2x, so about 120 MB when full. Plausible pressure on older iPads, not measured. | Measurement suggestion |
   | Error logging per cell | High-volume error logs on a hot path when the image store is unavailable | ACR-001, Low |
   | Work after a cell scrolls away | `.task(id:)` cancels it and the loader checks cancellation before decoding | Verified, no finding |

4. **Correctness behind the runtime path.** `inspect-swift-correctness` confirmed that loader state is actor-isolated, that a cancelled load never reaches the cache, and that `.task(id:)` restarts when a reused cell shows a different entry. No finding.

5. **Evidence.** `verify-apple-build-tests` ran the new test class, then the full suite. Simulator timings say nothing about device performance, so the report claims none, and no Instruments trace was available.

The reviewer returned this report.

---

# Apple Code Review Report

## Executive Summary

- Overall code health: Good. Decoding is off the main actor, cancellation is handled, the cache is bounded, and the new loader has focused tests.
- Highest-risk findings: ACR-001 (Low).
- Release readiness: Ready to merge. On-device memory and fill latency are unmeasured, and two measurements are suggested.
- Evidence limitations: No device, Instruments trace or MetricKit data. Simulator test results do not establish performance.

## Review Scope

- Review target: PR #77 "Thumbnail grid", base `0c6e1aa`, head `f3b8d20`.
- Files and components reviewed: `Driftwood/Journal/EntryGrid.swift` (new, contains `ThumbnailCell`), `Driftwood/Journal/ThumbnailLoader.swift` (new), `DriftwoodTests/ThumbnailLoaderTests.swift` (new); `Driftwood/Storage/ImageStore.swift` read for context.
- Technologies and platforms: SwiftUI `LazyVGrid` and `.task(id:)`, Swift actors, `NSCache`, `UIImage.preparingThumbnail(of:)`, unified logging; iPhone and iPad, iOS 17.0 and later.
- Change type: Feature with a performance focus.
- Primary risk areas: Decode cost while scrolling, cache memory, cancellation, log volume.
- Constraints and exclusions: Read-only. The review focused on runtime behavior; UI semantics were not reviewed.
- Not verifiable from available context: Memory footprint and fill latency on the oldest supported iPad; behavior with 2,000 entries on a device.

## Findings Summary

`Critical: 0 | High: 0 | Medium: 0 | Low: 1`

## Detailed Findings

### ACR-001 - Every failed thumbnail load logs at error level

- **Severity:** Low
- **Label:** Recommended Improvement
- **File:** `Driftwood/Journal/EntryGrid.swift`
- **Location:** The `catch` block of the `.task(id:)` in `ThumbnailCell`
- **Category:** Error Handling and Observability
- **Confidence:** High
- **Description:** Each failed load logs at error level. When the image store is unavailable, for example while original photos are still downloading, every visible and prefetched cell logs again on each scroll pass.
- **Evidence:** `catch { logger.error("thumbnail load failed: \(error)") }` inside a per-cell task; scrolling the grid starts dozens of cell tasks per second.
- **Trigger or reproduction:** Scroll the grid while originals are unavailable.
- **Expected behavior:** One actionable error-level entry per failure condition, with a count; per-item detail at debug level.
- **Observed or likely behavior:** Many identical error-level entries for each scroll.
- **Impact:** Log noise that buries other errors in diagnostic archives, at a small CPU cost.
- **Recommendation:** Log each item's failure at debug level and summarize at error level once, in the loader.
- **Suggested fix:** Move the error-level log into `ThumbnailLoader`, keyed by error domain and code and emitted at most once a minute; keep a `logger.debug` call in the cell.
- **Validation needed:** A unit test showing that 50 failures produce one error-level summary; a Console check while scrolling with the store unavailable, not run in this review.
- **Risk if unfixed:** Real failures are harder to find in field diagnostics.

## Category Results

### Architecture

No architecture concerns were identified from the available context.

### Code Quality

No finding. The loader is small and follows the existing `ImageStore` conventions.

### Correctness and Logic

Verified with `inspect-swift-correctness`: loader state is actor-isolated; `.task(id: entry.id)` cancels when a cell leaves the screen or changes entry; the loader calls `Task.checkCancellation()` after reading and before decoding, so cancelled loads never populate the cache. No finding.

### UI and Accessibility

Not reviewed; outside the requested focus.

### Security and Privacy

Not applicable. Images are local, and the log interpolation keeps its default privacy, so entry identifiers and errors are redacted in release logs.

### Performance and Energy

No finding meets the evidence threshold. Measurement suggestions, with no severity:

1. **Fill latency during fast scrolling.** Decoding runs inside the actor, so thumbnails decode one at a time. Profile a fast scroll through 500 entries with Instruments (Time Profiler and Hangs) on the oldest supported iPad. If visible cells fill slowly, move decoding into a `nonisolated` function and bound the number of concurrent loads.
2. **Cache memory.** The scale model gives about 120 MB for 300 thumbnails at 2x. Measure with the Allocations instrument on the oldest supported iPad. If the footprint is high, set `totalCostLimit` with each thumbnail's pixel bytes as its cost.

### Error Handling and Observability

ACR-001. A failed load shows the placeholder image, which is acceptable feedback to the user.

### Tests

Commands run on the macOS host:

| Command | Exit | Result |
|---|---|---|
| `python3 scripts/detect_apple_toolchain.py --root ~/src/driftwood --format markdown` (from the `verify-apple-build-tests` Skill directory) | 0 | macOS; `can_run_xcodebuild: yes` |
| `xcodebuild test -project Driftwood.xcodeproj -scheme Driftwood -destination 'platform=iOS Simulator,name=iPad (10th generation)' -only-testing:DriftwoodTests/ThumbnailLoaderTests` | 0 | 5 tests, 0 failures |
| `xcodebuild test -project Driftwood.xcodeproj -scheme Driftwood -destination 'platform=iOS Simulator,name=iPad (10th generation)'` | 0 | 148 tests, 0 failures |

The scheme and destination come from the repository's `Makefile` `test` target. The new tests cover a cache hit, a decode failure and cancellation. An optional performance test with `XCTMemoryMetric` over a 500-entry fixture would give a baseline for suggestion 2.

### Dependencies and Configuration

Not applicable. No project, package or configuration file changed.

## Documentation Impact

- `README.md` updates: None.
- `CHANGELOG.md` entries: After merge: "Journal entries show photo thumbnails in a grid."
- `REVIEW.md` human blockers: None.
- `TODO.md` engineering actions: ACR-001; the two measurements under Performance and Energy.
- `CHECKLIST.md` input entries: None.

## Merge or Release Recommendation

**Approved with comments.** No defect meets the evidence threshold, the changed path is tested, and the tests pass. ACR-001 and the two measurements are recommended but not blocking. This approval makes no claim about on-device performance.

## Engineer Handoff Notes

- Current state: Head `f3b8d20` builds, and all 148 tests pass on the iPad simulator. Nothing was profiled on a device.
- Highest risks: Unmeasured memory footprint and fill latency on older iPads.
- Required fixes: None.
- Suggested work order: ACR-001, then measurement 2 (memory), then measurement 1 (latency).
- Validation requirements: Instruments Allocations and Time Profiler runs on the oldest supported iPad with a 500-entry journal; the ACR-001 unit test.
- Human blockers: None.
- Configuration dependencies: None.
