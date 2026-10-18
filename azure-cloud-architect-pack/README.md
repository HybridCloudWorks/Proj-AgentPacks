# Azure Cloud Architect Pack

Portable Agent/Skill package for the full Azure cloud-architecture lifecycle. This pack is broader than the Azure Expert Designer: it designs and reviews Azure foundations and workloads, supports controlled deployment and operations, and routes detailed Draw.io production to the separate diagram capability when needed.

## Primary downloads

- `dist/azure-cloud-architect-pack.zip` — complete source, targets, tests, hooks, tooling, and archives.
- `dist/azure-cloud-architect-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/azure-cloud-architect-prompt.zip` — reusable pack-authoring prompt.
- `dist/azure-cloud-architect-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `azure-cloud-architect-skills.zip`.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
```

Validation is static and non-mutating. It does not prove a live Azure tenant, subscription, deployment, Entra/RBAC/Policy authorization, quota, regional availability, cost, security posture, or recovery result.

## MCP and official evidence

When the host supports it, prefer Microsoft Learn, Azure Architecture Center, CAF, WAF, AVM, and the official Azure MCP Server for current Azure documentation, resource guidance, best practices, and read-only evidence. Use Azure MCP tools only within explicit authorization and least-privilege boundaries. MCP availability is an integration capability, not a reason to bypass approvals.

## Optional hook

`hooks/architecture-review.ps1` checks a proposed handoff directory for the required REQ, TOPOLOGY, CONSTRAINTS, and ADR artifacts. It is opt-in and non-mutating; it does not deploy or call Azure.
