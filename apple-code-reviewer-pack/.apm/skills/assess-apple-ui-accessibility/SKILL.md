---
name: assess-apple-ui-accessibility
description: Assess SwiftUI, UIKit, and AppKit changes for lifecycle and state defects, navigation errors, invalid update flow, adaptive-layout failures, localization problems, input and focus issues, and accessibility regressions. Use when reviewing views, view controllers, scenes, windows, navigation, forms, lists, gestures, custom controls, animations, or UI tests; do not use for visual taste or product-design changes unsupported by requirements.
---

# Objective

Determine whether changed Apple UI code presents the correct state, responds to lifecycle and input events safely, adapts across supported environments, and exposes usable accessibility semantics.

# Inputs

Required: changed SwiftUI, UIKit, or AppKit code with its state, navigation, lifecycle, and supported-platform context.

Optional: product requirements, design specifications, localization resources, accessibility identifiers, UI tests, screenshots, and target device or window ranges.

# Workflow

1. Identify UI framework, target platforms, minimum OS versions, state owners, data flow, and navigation ownership.
2. Trace initial load, updates, dismissal, background and foreground transitions, restoration, cancellation, and repeated presentation.
3. Evaluate SwiftUI identity, ownership wrappers, observation, dependency injection, task lifetime, and invalidation.
4. Evaluate UIKit or AppKit containment, appearance and window lifecycle, reuse, delegation, and thread confinement.
5. Evaluate navigation, deep links, sheets, popovers, alerts, tabs, split views, and back-stack consistency.
6. Evaluate layout across supported size classes, window sizes, orientation, Dynamic Type, localization, keyboard, safe areas, and platform conventions.
7. Evaluate controls, labels, values, traits, focus, reading order, actions, grouping, touch or pointer targets, and VoiceOver behavior.
8. Evaluate reduced motion, contrast, color-independent meaning, captions, and alternate input where applicable.
9. Check UI and accessibility tests for the changed behavior.
10. Return only evidence-based findings; do not replace product or visual design judgment.

LOAD `references/ui-accessibility-checklist.md` for detailed framework and accessibility checks.

LOAD `references/official-sources.md` before making version-sensitive API, accessibility, or platform-convention claims.

# Finding Contract

Include affected platform and OS range, lifecycle or interaction trigger, user-visible behavior, accessibility or usability impact, code evidence, correction, validation method, and confidence.

# Ownership Boundaries

- This Skill owns UI state, lifecycle, navigation, layout, interaction, localization, and accessibility semantics.
- `inspect-swift-correctness` owns language-level state, ARC, and concurrency defects behind the UI.
- `assess-apple-runtime-quality` owns measurable rendering, responsiveness, memory, and energy impact.
- `assess-apple-security-privacy` owns permission prompts, sensitive UI, WebKit trust, and privacy disclosure.

# Stop Conditions

State missing evidence when design requirements, supported devices, localization resources, accessibility identifiers, target OS versions, or executable UI tests are unavailable. Do not declare a visual or interaction defect solely from personal preference.
