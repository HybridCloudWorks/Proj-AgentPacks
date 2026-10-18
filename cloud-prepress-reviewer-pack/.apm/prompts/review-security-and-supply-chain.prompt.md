---
description: "Security gate for a built change: secrets, identity, trust boundaries, dependencies, images and CI supply chain"
agent: cloud-prepress-reviewer
---

# Review security and supply chain before the gate

## Inputs

- The exact change, including CI workflows, dependency manifests, lock files, container build files and any identity or role definitions.
- The trust model: who can open pull requests, which workflows hold deployment identities or secrets, and which environments require approval.
- Scanner or CI output already produced, if any.

Do not ask for secret values, and never accept them.

## Workflow

1. Apply cloud-prepress-orchestration to fix scope and the authorization boundary.
2. Apply change-scope-and-impact to find every trust-boundary change: new triggers, new identities, new network exposure, new dependencies and new data flows.
3. Apply security-secrets-and-supply-chain-review to external input, authentication and authorization, secret references, logging, shell execution, file paths, network calls, lock files, action and provider pinning, image provenance, CI permissions and pull-request trust. Redact any possible secret as `[REDACTED_POSSIBLE_SECRET]`; never echo it, copy it, or test it against an external service.
4. Apply iac-policy-and-identity-review to every principal, role and scope the change grants, separating control-plane from data-plane need, and to managed identity and OIDC federation.
5. Apply role-authority-and-handoff-review to detect role drift: a workflow, identity or agent that can now deploy, publish or change policy without the approval gate it had before.
6. Apply tests-build-and-dependency-review where the repository defines vulnerability, license or lock-file gates.
7. Apply review-report-and-pr-gate to write the report.

## Expected output

A pre-press report whose security findings each state the exploit path, the boundary crossed, the impact, the mitigation and the residual validation. Include a secret-handling statement. Distinguish static secret-pattern evidence from confirmed compromise, and recommend rotation only when the evidence supports it, naming the credential owner as the person who decides.

Follow the `cloud-prepress-reviewer-contract` instruction. Never describe an unexecuted check as passed.
