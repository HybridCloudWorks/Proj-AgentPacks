# AWS Cloud Architect Pack

Portable Agent/Skill package for the full AWS cloud-architecture lifecycle. This pack is broader than the AWS Expert Designer: it designs and reviews AWS foundations and workloads, supports controlled deployment and operations, and routes Draw.io visualization to the separate diagram capability when needed.

## Primary downloads

- `dist/aws-cloud-architect-pack.zip` — complete source, targets, tests, hooks, tooling, and archives.
- `dist/aws-cloud-architect-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/aws-cloud-architect-prompt.zip` — reusable pack-authoring prompt.
- `dist/aws-cloud-architect-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The generated distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `aws-cloud-architect-skills.zip`.

## Workflow prompts

There is one prompt per primary workflow in `.apm/prompts/`. Each targets the `aws-cloud-architect` agent and follows the always-on `aws-cloud-architect-contract` instruction.

| Prompt | Use it to |
|---|---|
| `design-aws-workload.prompt.md` | Design a production workload and hand it off |
| `design-aws-landing-zone.prompt.md` | Design multi-account foundations with Control Tower |
| `design-aws-hybrid-network.prompt.md` | Choose and design VPC, hybrid and edge connectivity |
| `plan-aws-migration-and-dr.prompt.md` | Plan migration waves, cutover, rollback and DR from RTO and RPO |
| `review-deployment-plan.prompt.md` | Review a CloudFormation, CDK or Terraform change before it is applied |
| `review-aws-well-architected.prompt.md` | Run a six-pillar review, with CAF perspectives if needed |
| `review-aws-cost.prompt.md` | Find cost drivers and recommend measured optimizations |
| `troubleshoot-aws-incident.prompt.md` | Investigate a production incident with read-only access |
| `verify-aws-evidence.prompt.md` | Verify quotas, Region availability, pricing or behavior and record the evidence |
| `create-aws-architecture-diagram.prompt.md` | Draw an approved design in Draw.io and validate it |

`docs/PROMPT_INVENTORY.md` lists the skills each prompt applies and how APM installs prompts on each host.

## Examples and templates

`examples/` holds worked walkthroughs. Each one ends with a completion report in the contract's twelve-section format:

- `greenfield-workload-design.md`
- `landing-zone-design.md`
- `migration-and-dr-plan.md`
- `deployment-review-blocked.md`: a production change that is refused and blocked
- `incident-troubleshooting.md`
- `architecture-diagram.md`: a diagram that is structurally valid but visually not verified

`templates/` holds the documents the skills produce:

- the handoff set `REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json` and `ADR.md`
- `completion-report.md`
- `well-architected-review.md`

Templates and examples are reference material for people. They are not installed with the agent; the contract instruction carries everything the model needs.

## Build and validate

From the pack repository root:

```text
python tooling/build_pack.py
python tooling/validate_pack.py aws-cloud-architect-pack --install-check
```

Validation is static and non-mutating. It does not prove a live AWS account, deployment, IAM authorization, service quota, regional availability, cost, security posture, or recovery result.

## MCP and official evidence

When the host supports it, prefer the official AWS Knowledge MCP Server for current AWS documentation, API references, architecture guidance, agent skills, and Region availability. Use the AWS MCP Server/Agent Toolkit or specialized MCP servers only within explicit authorization and least-privilege boundaries. MCP availability is an integration capability, not a reason to bypass approvals.

## Optional hook

`hooks/architecture-review.ps1` checks a proposed handoff directory for the required REQ, TOPOLOGY, CONSTRAINTS, and ADR artifacts (`REQ.md`, `TOPOLOGY.json`, `CONSTRAINTS.json`, `ADR.md`). It is opt-in and non-mutating; it does not deploy or call AWS.
