# Worked example: security and privacy review of a sign-in change

Synthetic fixture. The app, domain, paths, commit hashes and command output are illustrative. They show the workflow and the report format; they are not observed results. `harbor.example.com` is a reserved example domain.

- Prompt: `review-apple-security-privacy.prompt.md`
- Skills: `review-apple-code`, `assess-apple-security-privacy`, `verify-apple-build-tests`
- Outcome: Changes requested

## Request

"Security review of PR #219 in Harbor before we merge it: passwordless sign-in with magic links."

Harbor is an account-based notes app for iOS 17.0 and later. The pull request adds an email magic-link sign-in. It changes the URL handler, the session store, the entitlements and Info.plist.

## How the review ran

1. **Scope.** Base `71b0c3e`, head `2fa94d8`. Changed files: `Harbor/App/HarborApp.swift`, `Harbor/Auth/DeepLinkRouter.swift` (new), `Harbor/Auth/SessionStore.swift`, `Harbor/Harbor.entitlements`, `Harbor/Info.plist` and `HarborTests/DeepLinkRouterTests.swift` (new).

2. **Assets, actors and boundaries.** `assess-apple-security-privacy` starts with an inventory:

   | Item | Detail |
   |---|---|
   | Assets | The refresh token, the one-time magic-link token, the user's notes |
   | Actors | The user, other apps on the device, any web page the user visits, anyone who can send the user a link |
   | Entry points | The new `harbor` custom URL scheme and universal links for `harbor.example.com` |
   | Sinks | `SessionStore.signIn(magicToken:)`, `SessionStore.persist(_:)`, the unified log |

3. **Source-to-sink traces.** Every finding below has a traced path; no attack class was reported from a pattern alone.
   - URL, then `.onOpenURL`, then `logger.info(... privacy: .public)`, then the unified log (ACR-003).
   - URL, then `DeepLinkRouter.handle(_:)`, then `signIn(magicToken:)`, which replaces the current session (ACR-001).
   - Sign-in response, then `persist(_:)`, then `UserDefaults` (ACR-002).

4. **Official sources.** Before writing about Keychain accessibility and Associated Domains, the reviewer loaded the Skill's `references/official-sources.md` and used the Keychain Services and Entitlements pages it lists.

5. **Evidence the client cannot give.** Whether the backend binds magic-link tokens to a request, expires them or allows them once could not be inspected. The report treats this as an evidence limit and does not assume the server compensates for a client gap.

6. **Configuration checks.** `verify-apple-build-tests` linted the two property lists and ran the new test class only, the narrowest useful command.

7. **Examined and not reported.** The Associated Domains entitlement lists one domain, `applinks:harbor.example.com`, which is least privilege. `PrivacyInfo.xcprivacy` did not change, and the change adds no data type, SDK or tracking.

The reviewer returned this report. The magic-link token never appears in it.

---

# Apple Code Review Report

## Executive Summary

- Overall code health: The sign-in flow works for the happy path, but any link can sign the user into another account, the refresh token moved out of the Keychain, and full sign-in URLs are logged publicly.
- Highest-risk findings: ACR-001 (High), ACR-002 (High).
- Release readiness: Not ready to merge. The fixes are engineering work with no human blockers.
- Evidence limitations: The backend's token rules and the site association file served by `harbor.example.com` could not be inspected. Universal-link routing was not tested on a device.

## Review Scope

- Review target: PR #219 "Magic-link sign-in", base `71b0c3e`, head `2fa94d8`.
- Files and components reviewed: `Harbor/App/HarborApp.swift`, `Harbor/Auth/DeepLinkRouter.swift` (new), `Harbor/Auth/SessionStore.swift`, `Harbor/Harbor.entitlements`, `Harbor/Info.plist`, `HarborTests/DeepLinkRouterTests.swift` (new); `Harbor/Auth/KeychainTokenStore.swift` and `Harbor/Auth/SignInCoordinator.swift` read for context.
- Technologies and platforms: Swift, SwiftUI `onOpenURL`, Keychain Services, unified logging, Associated Domains; iOS 17.0 and later.
- Change type: Security (new authentication path).
- Primary risk areas: Untrusted URLs reaching authentication, token storage, sensitive logging.
- Constraints and exclusions: Read-only review. The backend and the site association file are outside the repository.
- Not verifiable from available context: Server-side token binding, expiry and single use; universal-link behavior on a device.

## Findings Summary

`Critical: 0 | High: 2 | Medium: 1 | Low: 0`

## Detailed Findings

### ACR-001 - Any app or web page can sign the user into a different account through the custom URL scheme

- **Severity:** High
- **Label:** Confirmed Issue; Security Sensitive
- **File:** `Harbor/Auth/DeepLinkRouter.swift`; `Harbor/Info.plist`
- **Location:** `DeepLinkRouter.handle(_:)`; the `CFBundleURLTypes` entry for the `harbor` scheme
- **Category:** Security and Privacy
- **Confidence:** High for the client path; Medium for exploitability, which depends on backend token binding
- **Description:** The handler accepts a sign-in token from any URL whose path is `/auth/magic`, checks neither scheme nor host, and signs in at once, replacing any current session. The new `harbor` custom scheme reaches the same handler. Any app or web page can open a custom-scheme URL, whereas a universal link can come only from the associated domain. Attack surface: the custom URL scheme. Trust boundary: links from outside the app into authentication. Precondition: the attacker requests a magic link for their own account and gets the victim to open it through the custom scheme. Affected: the victim's session and every note they write afterwards.
- **Evidence:** `guard let components = URLComponents(url: url, resolvingAgainstBaseURL: false), components.path == "/auth/magic", let token = ...` with no check of `url.scheme` or `url.host`; `CFBundleURLSchemes` contains `harbor`; `signIn(magicToken:)` calls `sessionStore.replace(_:)` without asking.
- **Trigger or reproduction:** While signed in to account A, open `harbor://anything/auth/magic?token=<token issued for account B>` from a web page.
- **Expected behavior:** Magic links work only as universal links from `harbor.example.com`, only for a sign-in this device requested, and never switch accounts silently.
- **Observed or likely behavior:** The app signs in to account B without prompting. Notes the victim writes next sync to the attacker's account.
- **Impact:** Login cross-site request forgery: the victim's new notes are disclosed to the attacker.
- **Recommendation:** Restrict the route, and bind each link to a request this device started.
- **Suggested fix:** In `handle(_:)`, require `url.scheme == "https"` and `url.host == "harbor.example.com"`, and keep the custom scheme away from the sign-in route. When the user requests a link, store a random nonce in the Keychain and send it with the request; accept the link only when its `nonce` matches, then delete the stored nonce. Route the result through `SignInCoordinator`, which already asks before switching accounts and shows errors.
- **Validation needed:** New `DeepLinkRouterTests` cases: a custom-scheme URL is rejected, a wrong host is rejected, a missing or mismatched nonce is rejected, and an existing session triggers the switch prompt. The backend owner confirms tokens are single-use, short-lived and bound to the nonce; the client check does not replace server enforcement.
- **Risk if unfixed:** One link can silently move a user's future notes into someone else's account.

### ACR-002 - The refresh token moved from the Keychain to UserDefaults

- **Severity:** High
- **Label:** Confirmed Issue; Security Sensitive
- **File:** `Harbor/Auth/SessionStore.swift`
- **Location:** `SessionStore.persist(_:)`
- **Category:** Security and Privacy
- **Confidence:** High
- **Description:** The diff replaces the call to `KeychainTokenStore.save(_:)` with `UserDefaults.standard.set(session.refreshToken, forKey: "refreshToken")`. Defaults are a property list in the app container and are included in device backups, so the long-lived refresh token can be restored onto another device and read from an unencrypted backup or a copied container. Attack surface: local storage and backups. Trust boundary: the device and its backups. Precondition: access to an unencrypted backup or the app container. Affected: the account's refresh token.
- **Evidence:** Removed line `try KeychainTokenStore.save(session.refreshToken)`; added line `UserDefaults.standard.set(session.refreshToken, forKey: "refreshToken")`. `KeychainTokenStore` still exists and saves with a this-device-only accessibility class.
- **Trigger or reproduction:** Any sign-in on a build that contains this change.
- **Expected behavior:** The refresh token stays in the Keychain with a this-device-only accessibility class, as before the change.
- **Observed or likely behavior:** The token is stored in the preferences property list and travels with backups.
- **Impact:** Session takeover from a backup or container copy; regression of an existing control.
- **Recommendation:** Restore Keychain storage and clear the defaults key.
- **Suggested fix:** Revert to `KeychainTokenStore.save(_:)`. On launch, call `UserDefaults.standard.removeObject(forKey: "refreshToken")` so values written by any build that carried this change are removed.
- **Validation needed:** A unit test asserting that after `persist(_:)` the defaults key is nil and `KeychainTokenStore.load()` returns the token. On a device, confirm the session survives an app restart.
- **Risk if unfixed:** Every signed-in user's refresh token is exposed in backups.

### ACR-003 - Full sign-in URLs, including the token, are logged without redaction

- **Severity:** Medium
- **Label:** Confirmed Issue; Security Sensitive
- **File:** `Harbor/App/HarborApp.swift`
- **Location:** The `.onOpenURL` closure in `HarborApp.body`
- **Category:** Security and Privacy
- **Confidence:** High
- **Description:** `logger.info("Opened URL: \(url.absoluteString, privacy: .public)")` writes the whole URL, including the token in its query, to the unified log. The `.public` annotation overrides the default redaction of interpolated strings. Attack surface: device logs. Trust boundary: the app and the system log, sysdiagnose archives and support bundles. Precondition: access to device logs, such as a connected Mac or a shared diagnostic archive. Affected: magic-link tokens.
- **Evidence:** The quoted log line, with `privacy: .public` on the interpolation.
- **Trigger or reproduction:** Open any magic link.
- **Expected behavior:** Logs record the route and the outcome, never the token.
- **Observed or likely behavior:** The token appears in plain text in the device log.
- **Impact:** Token replay within its validity window when logs are shared.
- **Recommendation:** Log only the path.
- **Suggested fix:** `logger.info("Opened URL path: \(url.path, privacy: .public)")`, or remove the line.
- **Validation needed:** Open a magic link on a device and confirm in Console that no query string is logged. Not run in this review.
- **Risk if unfixed:** Tokens leak through routine support diagnostics.

## Category Results

### Architecture

`DeepLinkRouter` calls `SessionStore` directly instead of the existing `SignInCoordinator`, which owns sign-in errors and account-switch confirmation. That bypass is why ACR-001 has no confirmation step, so it is covered there rather than reported again.

### Code Quality

No separate finding.

### Correctness and Logic

The router's `Task { try await session.signIn(magicToken: token) }` discards sign-in errors, so a failed link does nothing visible. Routing through `SignInCoordinator`, part of the fix for ACR-001, restores the existing error presentation, so this is not reported separately.

### UI and Accessibility

Not applicable. No view changed apart from the URL handler.

### Security and Privacy

ACR-001, ACR-002 and ACR-003. The Associated Domains entitlement is limited to `harbor.example.com`. The privacy manifest did not change, and the change adds no data type, SDK or tracking. The site association file served by the domain and the backend's token rules could not be inspected.

### Performance and Energy

Not applicable. No frequent path changed.

### Error Handling and Observability

The log line is covered by ACR-003, and discarded sign-in errors are covered under Correctness and Logic.

### Tests

Commands run on the macOS host:

| Command | Exit | Result |
|---|---|---|
| `python3 scripts/detect_apple_toolchain.py --root ~/src/harbor --format markdown` (from the `verify-apple-build-tests` Skill directory) | 0 | macOS; `can_run_xcodebuild: yes` |
| `plutil -lint Harbor/Info.plist Harbor/Harbor.entitlements` | 0 | Both files OK |
| `xcodebuild test -project Harbor.xcodeproj -scheme Harbor -destination 'platform=iOS Simulator,name=iPhone 15' -only-testing:HarborTests/DeepLinkRouterTests` | 0 | 4 tests, 0 failures |

The four new tests cover only valid `https` links. The full suite was not run locally. Missing tests:

| Type | Scenario | Setup | Action | Expected assertion | Why it matters | Catches |
|---|---|---|---|---|---|---|
| Security unit | Custom-scheme sign-in | Router with a fake session | Handle a `harbor://` sign-in URL | No sign-in attempted | Blocks the cross-account path | ACR-001 |
| Security unit | Nonce mismatch | Stored nonce differs from the link's | Handle the link | No sign-in attempted | Binds links to this device's request | ACR-001 |
| Unit | Token storage | Fake session | `persist(_:)` | Defaults key is nil; Keychain returns the token | Prevents the storage regression returning | ACR-002 |

### Dependencies and Configuration

Info.plist adds `CFBundleURLTypes` with the `harbor` scheme, and the entitlements add Associated Domains; both lint cleanly. Universal links also depend on the domain serving its site association file, an input owned outside the repository and listed under `CHECKLIST.md` below.

## Documentation Impact

- `README.md` updates: Explain how to test magic links in development: universal links need the associated domain to serve its site association file, and after ACR-001 the custom scheme no longer opens the sign-in route.
- `CHANGELOG.md` entries: After the fixes merge: "Added passwordless sign-in with magic links."
- `REVIEW.md` human blockers: None. Confirming the backend token rules is a validation request to the backend owner, tracked in `TODO.md`.
- `TODO.md` engineering actions: Fix ACR-001, ACR-002 and ACR-003; add the three tests above; ask the backend owner to confirm single-use, expiry and nonce binding.
- `CHECKLIST.md` input entries:

  | Variable Name | Purpose | Required | Source | Consumer | Expected Format | Validation Status | Notes |
  |---|---|---|---|---|---|---|---|
  | `com.apple.developer.associated-domains` | Lets iOS route magic links from the web domain to the app | Yes | `Harbor/Harbor.entitlements` | iOS universal-link routing and `DeepLinkRouter` | `XXXXXXXX!XXXXXX!XXXXXXX!XXX` | Not validated: the site association file was not inspected | The domain must serve a site association file that lists the app |

## Merge or Release Recommendation

**Changes requested.** Two High findings, a cross-account sign-in path and a token-storage regression, have clear engineering fixes. No human decision is pending; the backend confirmation is a validation step.

## Engineer Handoff Notes

- Current state: Head `2fa94d8` lints cleanly and its four new tests pass on the simulator. The full suite was not run locally. Three security findings are open.
- Highest risks: ACR-001 (cross-account sign-in), ACR-002 (refresh token in backups).
- Required fixes: ACR-001, ACR-002, ACR-003.
- Suggested work order: ACR-002 first, because it is a small revert that removes an exposure on every sign-in; then ACR-003; then ACR-001, which needs the nonce flow and the coordinator change.
- Validation requirements: The three new tests and the full `xcodebuild test` suite pass on macOS; on a device, a universal link signs in and a custom-scheme link does not; Console shows no token; the backend owner confirms the token rules.
- Human blockers: None.
- Configuration dependencies: `com.apple.developer.associated-domains` and the site association file served by `harbor.example.com`.
