# UI and Accessibility Checklist

## SwiftUI

- Correct ownership among `@State`, bindings, environment, observation, and reference models.
- Stable identity in lists, navigation destinations, and conditional view trees.
- Side effects placed in lifecycle-aware tasks or commands rather than body evaluation.
- `.task` cancellation and repeated execution across identity changes.
- Navigation path consistency, deep-link restoration, modal ownership, and dismissal.
- State changes from correct isolation and no blocking work on the main actor.
- Preview-only assumptions not required at runtime.

## UIKit and AppKit

- View or window controller containment and appearance lifecycle.
- Reusable cells and supplementary views reset all state and cancel asynchronous work.
- Delegates, data sources, observers, and callbacks have correct ownership and cleanup.
- Layout updates occur on the correct thread and do not create constraint conflicts.
- Scene, window, document, background, restoration, and termination behavior.
- AppKit responder chain, first responder, menu and command validation, and multiwindow behavior where applicable.

## Navigation and Presentation

- No duplicate presentation, stale destination, inaccessible dismissal, or impossible back-stack state.
- Deep links validate input and land in a coherent authenticated state.
- Sheets, popovers, alerts, split views, tabs, and platform-specific presentations adapt to device and window context.
- Unsaved data, cancellation, retry, and destructive confirmation behavior are explicit.

## Adaptive UI and Localization

- Dynamic Type does not truncate critical content or disable controls.
- Layout supports declared orientations, window resizing, size classes, and safe areas.
- Localized text can expand; concatenation does not break grammar or translation.
- Locale-aware formatting is used for dates, numbers, currency, measurement, and names.
- Right-to-left layout and mirrored navigation semantics are preserved where supported.
- Keyboard, pointer, focus, hardware keyboard, and alternate input are considered for target platforms.

## Accessibility

- Every actionable element has an accurate label, value, trait, hint only when useful, and discoverable action.
- Custom controls expose semantics equivalent to native controls.
- Reading and focus order follow task flow; related content is grouped without hiding necessary children.
- State changes and errors are announced when users would otherwise miss them.
- Accessibility identifiers are stable for tests but are not substituted for user-facing labels.
- Meaning is not conveyed by color, sound, position, or motion alone.
- Contrast, target size, Dynamic Type, reduced motion, reduced transparency, and increased contrast are respected when applicable.
- Images distinguish decorative content from meaningful alternatives.
- Timed interactions provide an accessible alternative when required.

## UI Tests

- Assert user-observable behavior, not private implementation structure.
- Use stable semantic queries and deterministic setup.
- Cover critical navigation, error recovery, permission denial, localization, Dynamic Type, and accessibility behavior appropriate to risk.
