---
name: security-secrets-and-supply-chain-review
description: Reviews changed code and infrastructure for trust-boundary failures, secret exposure, identity misuse, insecure defaults, dependency risk, and supply-chain weaknesses.
---

# Security, Secrets, and Supply Chain Review

Inspect user-controlled and external inputs, authentication, authorization, secret references, tokens, keys, certificates, logging, shell execution, file paths, network calls, data boundaries, dependency changes, lock files, action/provider pinning, image provenance, and policy bypasses.

Redact possible secrets as `[REDACTED_POSSIBLE_SECRET]`; never echo, copy, or validate a secret by sending it externally. Distinguish static secret-pattern evidence from a confirmed credential compromise; recommend rotation only when evidence supports it.

Check least privilege at the actual scope and operation: control-plane versus data-plane roles, managed identities/OIDC, CI permissions, pull-request trust, private endpoints, encryption, and production exposure. Report exploit path, boundary, impact, mitigation, and residual validation.
