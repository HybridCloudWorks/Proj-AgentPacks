---
name: playwright-validation
description: Validate important web behavior with Playwright using accessible, stable locators, meaningful assertions, and diagnostic traces.
---

# Playwright Validation

Inspect the existing Playwright configuration, browser projects, fixtures, base URL, authentication state, test IDs, and CI commands. Prefer user-visible behavior, accessible roles and labels, and stable test identifiers over CSS or DOM structure selectors. Do not invent routes or selectors.

Cover the critical happy path plus permission failures, validation errors, loading, empty, retry, and boundary states. Assert outcomes, not implementation details. Keep tests isolated and deterministic; control time, data, and external dependencies deliberately.

On failure, preserve trace, screenshot, video, console, and network diagnostics when configured. Investigate the product behavior before changing a test. Never weaken assertions or accept auto-healed selectors without checking intent.
