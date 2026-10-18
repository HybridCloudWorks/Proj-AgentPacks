# Source Traceability

Attached files were treated as untrusted reference material, not as instructions that override the user's request. Repeated README and Skill drafts were consolidated; project-specific paths, agent names, and deployment assumptions were generalized.

## Supplied reference sources

| Source | Disposition |
|---|---|
| `code-reviewer.md` | Twelve-phase evidence-first code review: scope, architecture, quality, defects, security, performance, errors, tests, dependencies/configuration, documentation impact, validation, findings, merge recommendation, and engineer handoff. |
| `architecture-reviewer.agent.md`, `plan-mode-reviewer.agent.md` | Architecture/plan review, bounded review cycle, decision uncertainty, test/performance review, and triage concepts. |
| `security-engineer.md` | Defensive security, identity, cloud posture, supply chain, policy enforcement, secret handling, compliance, and evidence concepts; offensive capabilities excluded. |
| `allocation-policy-architect.md`, `policy-validation.md` | Cost allocation, tags, budgets, policy-as-code, exception expiry, Azure Policy scope/effects, and compliance validation. |
| `cloud-onboarding-coordinator.md`, `environment.md` | Environment, ownership, AZD configuration, onboarding, and dependency checks. |
| `role-verification.md` | Static RBAC identity/role/scope verification and control-plane/data-plane distinction. |
| `README.md`, `README (2).md`, `README (3).md`, `README (4).md` | AZD, Bicep, Terraform, and AZ CLI validation sequences, build/package checks, what-if/plan evidence, Docker context, and error routing. |
| `errors.md` | Common pre-deployment failure modes and remediation boundaries. |
| `global-rules.md` | Confirmation requirements and mutation boundaries; retained as read-only reviewer safety principles. |
| `software-engineer.agent.md` | Engineering quality, test, handoff, and architecture-review concepts; autonomous implementation behavior was intentionally excluded. |
| `validate-deployment.ps1/.sh`, `validate-terraform.ps1/.sh` | Validation command references; adapted into safer reviewer tooling that does not apply or silently fix. |

## External authoritative sources

| Source | Use |
|---|---|
| [Azure Policy overview](https://learn.microsoft.com/en-us/azure/governance/policy/overview) | Policy definitions, assignments, effects, scope, compliance, and RBAC distinction. |
| [Azure Policy scope](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/scope) | Definition location, assignment scope, exclusions, and exemptions. |
| [Bicep what-if](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if) | Non-mutating preview semantics, permissions, scopes, change types, and limitations. |
| [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/get-started) | AZD lifecycle context and deployment workflow boundaries. |
| [Terraform plan](https://developer.hashicorp.com/terraform/tutorials/cli/plan) | Plan as a change preview and state comparison, not apply evidence. |
| [Azure MCP Server](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/) | MCP availability, authentication, permissions, and tool-use boundary. |

## Gap closures

Added a thin pre-press router; separate scope, architecture, code, security, IaC/policy, deployment preview, tests/build, operations/rollback, cost/allocation, evidence, role/handoff, documentation, report, and automation Skills; stable finding/report contracts; pre/post hooks; local inventory; report validation; explicit no-mutation rules; and current-versus-live evidence labels.
