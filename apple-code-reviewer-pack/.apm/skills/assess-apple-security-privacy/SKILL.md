---
name: assess-apple-security-privacy
description: Assess Apple-platform code and configuration for trust-boundary failures, authentication or authorization bypass, secret exposure, unsafe storage or networking, WebKit and deep-link attacks, entitlement misuse, permission problems, privacy-manifest gaps, sensitive logging, and App Store security or privacy risk. Use when changes handle user or external input, identity, credentials, personal data, files, URLs, network calls, Keychain, permissions, entitlements, extensions, or third-party SDKs.
---

# Objective

Trace sensitive data and untrusted input across Apple platform boundaries, identify exploitable or policy-relevant failures, and recommend the smallest effective mitigation without exposing sensitive values.

# Inputs

Required: changed code or configuration that crosses a trust, identity, data, permission, storage, network, extension, or third-party SDK boundary.

Optional: threat model, backend authorization behavior, entitlements, privacy declarations, data inventory, dependency locks, and security test evidence.

# Workflow

1. Inventory assets, actors, data classes, entry points, trust boundaries, permissions, and external systems affected by the change.
2. Trace user, URL, file, pasteboard, notification, network, WebKit, extension, and interprocess inputs to validation and sensitive sinks.
3. Evaluate authentication, authorization, session state, account switching, local-device trust, and privilege boundaries.
4. Evaluate secrets, credentials, tokens, certificates, keys, Keychain accessibility, storage protection, backups, and logs.
5. Evaluate network transport, certificate handling, redirects, URLSession configuration, ATS exceptions, caching, and request construction.
6. Evaluate URL schemes, universal links, deep links, WebKit bridges, file access, path handling, command execution, and deserialization.
7. Evaluate entitlements, sandbox groups, extensions, background modes, permissions, and least privilege.
8. Evaluate data collection, privacy manifests, required-reason APIs, tracking, third-party SDK declarations, retention, deletion, and user disclosure.
9. Evaluate dependency and supply-chain changes visible in the repository.
10. Return attack surface, trust boundary, preconditions, impact, mitigation, validation, and confidence.

LOAD `references/security-privacy-checklist.md` for detailed checks.

LOAD `references/official-sources.md` before making current App Review, privacy-manifest, entitlement, or platform-security claims.

# Secret Handling

Never reproduce actual sensitive values. Replace any suspected value with `[REDACTED_POSSIBLE_SECRET]`, identify the file and variable name without the value, and recommend rotation when exposure is plausible.

# Finding Contract

For each finding state severity, label, attack surface, trust boundary, attacker or misuse precondition, affected data or capability, evidence, impact, mitigation, validation, and confidence.

Do not report theoretical attack names without a reachable source-to-sink path or a clearly missing control at a real boundary.

# Ownership Boundaries

- This Skill owns confidentiality, integrity, authorization, privacy, entitlement, and secret risks.
- `inspect-swift-correctness` owns non-security language and concurrency defects.
- `verify-apple-build-tests` owns whether configuration, manifests, locks, and CI validate successfully.
- `assess-apple-ui-accessibility` owns general UI behavior; this Skill owns sensitive prompts, permission rationale, secure text, and spoofing or phishing surfaces.

# Stop Conditions

State missing evidence when server-side authorization, backend behavior, certificate policy, production entitlements, privacy declarations, or third-party SDK behavior cannot be inspected. Do not assume client-side checks enforce server authorization.
