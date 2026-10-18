---
name: secure-python-engineering
description: Assess and repair Python security boundaries, identity, secrets, data handling and supply chain. Use when security review or a Python change affects authentication, input/output, execution, storage or dependencies.
---

# Secure Python Engineering

## Activation and scope

Security review or a Python change affects authentication, input/output, execution, storage or dependencies. Read-only security specialist gets no shell/edit tools by default; primary runs approved diagnostics.

## Inputs and dependencies

- Inputs: Changed code/callers, assets/actors/trust boundaries, configured controls and available diagnostics.
- Dependencies: Repository security scanners/policy and representative sanitized fixtures.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Threat-model actors, assets, data paths and blast radius; trace authentication, authorization/tenant scope, sessions, validation and error disclosure.
2. Review SQL/template/command injection, SSRF/redirects, paths/imports, unsafe YAML/pickle/XML, eval/exec, archives/temp files, races, TLS, cryptography and randomness. An occurrence is a review lead, not automatic proof.
3. Inspect dependency/index integrity, build plugins, container provenance, Action permissions/pinning and untrusted PR secret exposure; follow approved SBOM/vulnerability workflows.
4. Check data minimization, retention, logs/traces and secret handling. Return located findings with confidence, exploit/failure scenario, severity, business impact, remediation and validation; leave code unchanged on a review-only assignment.

## Output and validation

Evidence-based findings or requested remediation with negative tests, residual risk and approval gaps. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Unreproducible vulnerability claim, sensitive evidence disclosure, unknown dependency provenance or unavailable production controls. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `review-python-pull-request.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
