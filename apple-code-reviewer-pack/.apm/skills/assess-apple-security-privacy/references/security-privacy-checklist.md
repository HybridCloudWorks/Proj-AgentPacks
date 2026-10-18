# Apple Security and Privacy Checklist

## Input and Routing Boundaries

- Validate custom URL schemes, universal links, app links, document imports, intents, widgets, share extensions, notifications, and pasteboard content.
- Canonicalize and constrain file paths; prevent traversal, unsafe bookmarks, or security-scoped resource misuse.
- Validate decoded and deserialized data before state mutation or privileged action.
- Treat WebKit messages, JavaScript bridges, navigation actions, redirects, and downloaded files as untrusted.

## Identity and Authorization

- Revalidate authorization at the server or owning privileged boundary.
- Handle account switching, logout, token expiry, revoked access, and stale cached identity.
- Avoid using device possession, biometrics, or local flags as a substitute for remote authorization.
- Bind sensitive operations to the intended account, resource, and current session.

## Secrets and Sensitive Data

- No secrets, private keys, tokens, credentials, or production identifiers in source, fixtures, logs, crash metadata, screenshots, or build settings.
- Keychain item class, accessibility, access group, synchronizability, and deletion behavior match the threat model.
- Sensitive files use appropriate protection, backup exclusion, and lifecycle deletion.
- Clipboard, notification previews, widgets, app switcher snapshots, caches, and temporary files do not expose protected data.
- Unified logging uses privacy annotations and avoids sensitive interpolation.

## Networking

- ATS exceptions are narrow, justified, and not used to normalize insecure transport.
- Trust evaluation does not disable certificate or hostname validation.
- Redirects, cookies, caches, credentials, and background sessions preserve account and data boundaries.
- Request construction prevents injection and sends only required data.
- Retry and replay behavior does not duplicate sensitive or non-idempotent operations.

## Platform Permissions and Entitlements

- Entitlements, app groups, keychain groups, associated domains, extensions, background modes, and sandbox exceptions use least privilege.
- Permission usage descriptions accurately explain user-visible purpose.
- Denied, restricted, limited, provisional, and revoked states are handled safely.
- Sensitive capability access is contextual, not requested prematurely, and remains functional when denied where possible.

## Privacy

- `PrivacyInfo.xcprivacy` and third-party SDK manifests cover collected data and required-reason API use applicable to the shipped binary.
- App Store privacy answers, in-app behavior, SDK behavior, and policy disclosures remain consistent.
- Data minimization, purpose limitation, retention, deletion, export, and account deletion behavior match requirements.
- Tracking and cross-app or cross-site use has the required consent and declarations.
- Children, health, financial, location, biometric, contacts, photos, and other sensitive classes receive risk-proportionate handling.

## Supply Chain

- Review new or updated package sources, resolved versions, binary targets, plugins, build scripts, and transitive behavior.
- Prefer pinned, reviewable dependencies and verify checksums or signatures supported by the build system.
- Treat package plugins and build scripts as code execution during build.
