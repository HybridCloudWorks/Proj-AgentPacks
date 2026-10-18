# Worked example: UI and accessibility review

Synthetic fixture. The app, paths, commit hashes and CI results are illustrative. They show the workflow and the report format; they are not observed results.

- Prompt: `review-apple-ui-accessibility.prompt.md`
- Skills: `review-apple-code`, `assess-apple-ui-accessibility`, `inspect-swift-correctness`, `verify-apple-build-tests`
- Outcome: Changes requested

## Request

"Please review the accessibility of PR #305 in Pantry. CI is green."

Pantry is a SwiftUI recipe app for iPhone and iPad, iOS 17.0 and later. The pull request adds a star rating to recipes, redesigns the ingredient rows and restyles the filter chips. It links a design specification for colors and spacing.

## How the review ran

1. **Scope.** Base `8a17d42`, head `c3d9f10`. Changed: `Pantry/Recipes/StarRatingControl.swift` (new), `Pantry/Recipes/IngredientRow.swift`, `Pantry/Recipes/RecipeFilterBar.swift` and `PantryUITests/RecipeDetailUITests.swift`.

2. **CI evidence instead of a local rerun.** The detector on the reviewer's macOS host reported `can_run_xcodebuild: yes`. Before relying on "CI is green", `verify-apple-build-tests` checked that the passing runs belong to the head commit (`gh pr checks 305`, then `gh run view` with `headSha`). They do, so the reviewer did not repeat the suite locally. It also found that `ci.yml` runs UI tests on an iPhone simulator only, so nothing exercised iPad layouts.

3. **What VoiceOver gets from each new control.** `assess-apple-ui-accessibility` read each changed control for label, value, traits, actions and focus order:

   ```swift
   HStack(spacing: 4) {
       ForEach(1...5, id: \.self) { value in
           Image(systemName: value <= rating ? "star.fill" : "star")
               .foregroundStyle(.orange)
               .onTapGesture { rating = value }
       }
   }
   ```

   Five separate images, no value and no button or adjustable trait. That became ACR-001. The filter chips use the same tap-gesture pattern with selection shown only by color (ACR-003).

4. **Dynamic Type.** `IngredientRow` combines `.lineLimit(1)` with `.frame(height: 44)`. At accessibility text sizes the ingredient name truncates and clips (ACR-002).

5. **State behind the view.** `inspect-swift-correctness` confirmed that the `@Binding var rating` writes back to the recipe model on the main actor. No finding.

6. **Examined and not reported.** Orange stars instead of the accent color, and the 4-point spacing, follow the linked design specification. Visual preference is not a finding. Two of the three findings share a pattern, but the review covered only the changed files and did not search the rest of the app.

The reviewer returned this report.

---

# Apple Code Review Report

## Executive Summary

- Overall code health: The new UI works by touch, but the rating control and filter chips are hard to use with VoiceOver, and ingredient names truncate at large text sizes.
- Highest-risk findings: ACR-001, ACR-002 and ACR-003 (all Medium).
- Release readiness: Not ready to merge. All fixes are engineering work.
- Evidence limitations: No VoiceOver or Dynamic Type check was run on a device. CI runs UI tests on iPhone only.

## Review Scope

- Review target: PR #305 "Recipe ratings and ingredient redesign", base `8a17d42`, head `c3d9f10`.
- Files and components reviewed: `Pantry/Recipes/StarRatingControl.swift` (new), `Pantry/Recipes/IngredientRow.swift`, `Pantry/Recipes/RecipeFilterBar.swift`, `PantryUITests/RecipeDetailUITests.swift`; `Pantry/Recipes/RecipeDetailView.swift` read for context.
- Technologies and platforms: SwiftUI, XCUITest; iPhone and iPad, iOS 17.0 and later.
- Change type: Feature with a UI focus.
- Primary risk areas: Custom-control semantics, Dynamic Type, color-only state.
- Constraints and exclusions: Read-only. Visual design follows the linked specification and was not judged.
- Not verifiable from available context: VoiceOver behavior on a device; iPad layouts, which CI does not test.

## Findings Summary

`Critical: 0 | High: 0 | Medium: 3 | Low: 0`

## Detailed Findings

### ACR-001 - The star rating is not exposed to VoiceOver as one adjustable control

- **Severity:** Medium
- **Label:** Confirmed Issue
- **File:** `Pantry/Recipes/StarRatingControl.swift`
- **Location:** `StarRatingControl.body`
- **Category:** UI and Accessibility
- **Confidence:** High
- **Description:** The control is five `Image` views, each with an `onTapGesture`. VoiceOver reaches five separate images that have no rating value and no button or adjustable trait, so users cannot tell the current rating or that the stars can be changed. Affects iPhone and iPad, iOS 17.0 and later.
- **Evidence:** The `HStack` of `Image(systemName:)` views with `.onTapGesture`, quoted in the walkthrough; no accessibility modifiers in the file.
- **Trigger or reproduction:** With VoiceOver on, open a recipe and move to the rating.
- **Expected behavior:** One element labelled "Rating" with a value such as "3 of 5 stars", adjusted by swiping up or down.
- **Observed or likely behavior:** Five images in a row with no value, read one by one.
- **Impact:** VoiceOver users cannot learn or reliably set a recipe's rating.
- **Recommendation:** Expose the control as one adjustable element.
- **Suggested fix:** Add `.accessibilityElement(children: .ignore)`, `.accessibilityLabel("Rating")`, a localized `.accessibilityValue` such as "3 of 5 stars", and `.accessibilityAdjustableAction` that raises or lowers `rating` within 1 to 5.
- **Validation needed:** A UI test that finds the element by its "Rating" label and asserts its value; a manual VoiceOver check on iPhone and iPad, not run in this review.
- **Risk if unfixed:** A new feature ships unusable for VoiceOver users.

### ACR-002 - Ingredient names truncate and clip at accessibility text sizes

- **Severity:** Medium
- **Label:** Confirmed Issue
- **File:** `Pantry/Recipes/IngredientRow.swift`
- **Location:** `IngredientRow.body`
- **Category:** UI and Accessibility
- **Confidence:** High
- **Description:** The row sets `.lineLimit(1)` on the ingredient name and a fixed `.frame(height: 44)` on the row. At the larger accessibility text sizes the name no longer fits on one line, so it truncates, and the fixed height clips the text. Affects iPhone and iPad, iOS 17.0 and later.
- **Evidence:** `Text(ingredient.name).font(.body).lineLimit(1)` inside an `HStack` with `.frame(height: 44)`. Before this change the row had neither modifier.
- **Trigger or reproduction:** Set Larger Text to an accessibility size and open a recipe with long ingredient names.
- **Expected behavior:** The full ingredient name is readable at every supported text size.
- **Observed or likely behavior:** Names such as "Gluten-free soy sauce" are cut short and clipped.
- **Impact:** Users who rely on large text cannot read ingredients, including allergen-relevant ones.
- **Recommendation:** Let the row grow and wrap.
- **Suggested fix:** Replace `.frame(height: 44)` with `.frame(minHeight: 44)`, remove `.lineLimit(1)`, and switch the row to a `VStack` when `dynamicTypeSize.isAccessibilitySize` is true.
- **Validation needed:** A UI test launched with `-UIPreferredContentSizeCategoryName UICTContentSizeCategoryAccessibilityXXXL` that asserts the full ingredient name is shown; previews at accessibility sizes.
- **Risk if unfixed:** A regression for large-text users in a screen they use for every recipe.

### ACR-003 - Filter chips show selection by color only and are not buttons

- **Severity:** Medium
- **Label:** Confirmed Issue
- **File:** `Pantry/Recipes/RecipeFilterBar.swift`
- **Location:** `FilterChip.body`
- **Category:** UI and Accessibility
- **Confidence:** High
- **Description:** Each chip is a `Text` with `.onTapGesture`, and selection is shown only by its background color. VoiceOver does not announce the chip as a button or report whether it is selected, and users who cannot tell the colors apart get no other cue. Affects iPhone and iPad, iOS 17.0 and later.
- **Evidence:** `.background(isSelected ? Color.accentColor : Color(.secondarySystemBackground), in: Capsule())` and `.onTapGesture { toggle(filter) }`; no accessibility traits and no non-color indicator.
- **Trigger or reproduction:** With VoiceOver on, or with grayscale enabled, select a filter.
- **Expected behavior:** Each chip is announced as a button with its selected state, and selection is visible without color.
- **Observed or likely behavior:** VoiceOver reads only the title, and selected and unselected chips differ only in color.
- **Impact:** Users cannot tell which filters are active.
- **Recommendation:** Use a button and add a non-color cue.
- **Suggested fix:** Wrap the chip in a `Button`, add `.accessibilityAddTraits(isSelected ? .isSelected : [])`, and show a checkmark in selected chips.
- **Validation needed:** A UI test asserting that the selected chip reports its selected state; a manual VoiceOver and grayscale check, not run in this review.
- **Risk if unfixed:** Filtered results look wrong to users who cannot see which filters are on.

## Category Results

### Architecture

No architecture concerns were identified from the available context.

### Code Quality

ACR-001 and ACR-003 share a pattern: tap gestures on views that are not buttons. The review covered only the changed files and does not propose an app-wide sweep.

### Correctness and Logic

Verified with `inspect-swift-correctness`: the rating binding writes back to the recipe model on the main actor. No finding.

### UI and Accessibility

ACR-001, ACR-002 and ACR-003. Colors and spacing follow the linked design specification and were not reviewed as preferences.

### Security and Privacy

Not applicable. No data, permission or network change.

### Performance and Energy

Not applicable. No new work on a frequent path.

### Error Handling and Observability

Not applicable. The change has no failure path.

### Tests

Evidence used:

| Source | Result |
|---|---|
| `python3 scripts/detect_apple_toolchain.py --root ~/src/pantry --format markdown` (from the `verify-apple-build-tests` Skill directory), exit 0 | macOS; `can_run_xcodebuild: yes`, `can_run_apple_ui_tests: yes` |
| `gh pr checks 305`, exit 0 | `unit-tests` and `ui-tests` passed |
| `gh run view 5520 --json headSha,conclusion`, exit 0 | `headSha` matches `c3d9f10`; conclusion success |

The suite was not rerun locally because CI results exist for the head commit. `ci.yml` runs UI tests only on an iPhone simulator. The new `testRatingTapUpdatesStars` taps the third star by its identifier and checks the image; it does not check accessibility. Missing tests:

| Type | Scenario | Setup | Action | Expected assertion | Why it matters | Catches |
|---|---|---|---|---|---|---|
| Accessibility UI | Rating value | Recipe rated 3 | Query the element labelled "Rating" | Value is "3 of 5 stars" | The control must expose its state | ACR-001 |
| Accessibility UI | Large text | Launch at the largest accessibility size | Open a recipe with a long ingredient | Full ingredient name shown | Guards against truncation | ACR-002 |
| Accessibility UI | Selected filter | One filter selected | Query the chip | Selected state reported | Selection must not rely on color | ACR-003 |
| UI | iPad layout | iPad simulator destination in `ci.yml` | Run the recipe detail tests | Tests pass on iPad | iPad is a supported platform with no UI coverage | Layout regressions |

### Dependencies and Configuration

Not applicable. No project, package or configuration file changed. The missing iPad destination in `ci.yml` is recorded under Tests.

## Documentation Impact

- `README.md` updates: None.
- `CHANGELOG.md` entries: After the fixes merge: "Rate recipes with up to five stars."
- `REVIEW.md` human blockers: None.
- `TODO.md` engineering actions: Fix ACR-001, ACR-002 and ACR-003; add the four tests above, including an iPad destination in `ci.yml`.
- `CHECKLIST.md` input entries: None.

## Merge or Release Recommendation

**Changes requested.** The new rating control and the restyled filters are hard or impossible to use with VoiceOver, and the ingredient redesign regresses large-text support. All three have small, testable fixes, and no human decision is needed.

## Engineer Handoff Notes

- Current state: Head `c3d9f10` passes unit and UI tests in CI on an iPhone simulator. No accessibility test exists for the changed controls, and nothing ran on iPad.
- Highest risks: ACR-001 (rating unusable with VoiceOver), ACR-002 (truncated ingredients).
- Required fixes: ACR-001, ACR-002, ACR-003.
- Suggested work order: ACR-002 first, because it regresses an existing screen; then ACR-001 and ACR-003, which share a pattern; then the tests and the iPad destination.
- Validation requirements: The four tests pass in CI on iPhone and iPad simulators; a manual VoiceOver pass and an accessibility-size pass on a device.
- Human blockers: None.
- Configuration dependencies: None.
