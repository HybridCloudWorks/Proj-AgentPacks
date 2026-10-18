---
description: "Review SwiftUI, UIKit or AppKit changes for state, navigation, layout, localization and accessibility defects"
agent: apple-code-reviewer
---

# Review Apple UI and accessibility

## Inputs

- The changed views, view controllers, scenes or windows, with the state owners and navigation they depend on.
- Supported platforms, minimum OS versions, and the device, size-class or window ranges the app declares.
- Optional: product or design requirements, localization resources, accessibility identifiers, UI tests and screenshots.

## Workflow

1. Activate `review-apple-code` and state that the review focuses on UI behavior and accessibility.
2. Apply `assess-apple-ui-accessibility`. Trace initial load, updates, dismissal, background and foreground transitions, and repeated presentation. Check SwiftUI identity and state ownership, UIKit or AppKit lifecycle and reuse, navigation consistency, Dynamic Type and localized layout, and the label, value, traits, actions and focus order of every control the change adds or alters.
3. Bring in `inspect-swift-correctness` when the defect sits in state or concurrency code behind the view, and `assess-apple-security-privacy` when the change touches permission prompts, secure text entry or screens that show sensitive data.
4. Report only behavior you can tie to code, requirements or tests. Visual preference is not a finding. When design requirements or supported device ranges are missing, record that as an evidence limit.

## Expected output

The review report the contract requires. Each UI finding names the affected platform and OS range, the interaction that triggers it, what the user experiences, its accessibility impact, and how to validate the fix: a UI test that uses semantic queries, or a manual VoiceOver, Dynamic Type or keyboard check that you list as not yet run. Follow the `apple-code-reviewer-contract` instruction.
