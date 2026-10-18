# AWS Cloud Architect Pack

Portable Agent/Skill package for the full AWS cloud-architecture lifecycle. This pack is broader than the AWS Expert Designer: it designs and reviews AWS foundations and workloads, supports controlled deployment and operations, and routes Draw.io visualization to the separate diagram capability when needed.

## Primary downloads

- `dist/aws-cloud-architect-pack.zip` — complete source, targets, tests, hooks, tooling, and archives.
- `dist/aws-cloud-architect-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/aws-cloud-architect-prompt.zip` — reusable pack-authoring prompt.
- `dist/aws-cloud-architect-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `aws-cloud-architect-skills.zip`.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
```

Validation is static and non-mutating. It does not prove a live AWS account, deployment, IAM authorization, service quota, regional availability, cost, security posture, or recovery result.

## MCP and official evidence

When the host supports it, prefer the official AWS Knowledge MCP Server for current AWS documentation, API references, architecture guidance, agent skills, and Region availability. Use the AWS MCP Server/Agent Toolkit or specialized MCP servers only within explicit authorization and least-privilege boundaries. MCP availability is an integration capability, not a reason to bypass approvals.

## Optional hook

`hooks/architecture-review.ps1` checks a proposed handoff directory for the required REQ, TOPOLOGY, CONSTRAINTS, and ADR artifacts. It is opt-in and non-mutating; it does not deploy or call AWS.
