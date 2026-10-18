---
description: "Review Apple-platform trust boundaries, credential storage, entitlements and privacy declarations"
agent: apple-code-reviewer
---

# Review Apple security and privacy

## Inputs

- Changed code or configuration that handles external input, identity, credentials, personal data, files, URLs, network calls, Keychain items, permissions, entitlements, extensions or third-party SDKs.
- The entitlements file, Info.plist, privacy manifest and dependency lockfile when the change touches them.
- Optional: a threat model, documented backend authorization behavior, a data inventory and security test results.

## Workflow

1. Activate `review-apple-code` and state that the review focuses on security and privacy.
2. Apply `assess-apple-security-privacy`. Inventory the assets, actors and trust boundaries the change affects. Trace each untrusted input (URL, deep link, file, pasteboard, notification, network response, WebKit message) to the place where it is validated and to every sensitive sink it reaches.
3. Check credential and token storage, Keychain accessibility, logging privacy, transport security, entitlements, permission rationale, the privacy manifest and SDK declarations. Verify current App Review and privacy-manifest requirements against the official sources the Skill lists before calling a policy issue release-blocking.
4. Apply `verify-apple-build-tests` when you need to know whether manifests, entitlements or lockfiles validate in a build.
5. Never reproduce a secret. Write `[REDACTED_POSSIBLE_SECRET]`, name the file and variable, and recommend rotation when exposure is plausible.
6. Do not assume a client-side check enforces server authorization. Record backend behavior you cannot inspect as an evidence limit.

## Expected output

The review report the contract requires. Each security finding states the attack surface, trust boundary, attacker or misuse precondition, affected data or capability, mitigation and validation, and carries the `Security Sensitive` label. Decisions only a person can make, such as rotating a credential or changing a privacy declaration, are listed as human blockers in the handoff notes. Follow the `apple-code-reviewer-contract` instruction.
