# Source Traceability

Attached documents were treated as untrusted reference material, not as instructions that override the user's request. Duplicate agent and Skill drafts were consolidated; the user request defines the full-lifecycle Azure Cloud Architect scope and deliverable contract.

## Supplied Azure Architect sources

| Source | Disposition |
|---|---|
| `azure-architect.agent.md`, `azure-architect.md`, `azure-architect (2).md` | Core Azure architecture mission, WAF/CAF alignment, hybrid connectivity, identity, networking, resilience, cost, and `REQ`/`TOPOLOGY`/`CONSTRAINTS`/`ADR` handoff. |
| `azure-certified-architect.agent.md` | AZ-305/AZ-104 domain coverage normalized into current framework-aware Skills; certification percentages are not treated as a live product contract. |
| `AVM (to know).md`, `AVM (to know) 2.md` | AVM Terraform module design, provider/version, interface, testing, documentation, and composition concerns; current AVM specifications take precedence where the attachment has drifted. |
| `Azure Standardization Expert/alz-architect.md` | Management-group, subscription, resource-group placement, naming, tags, reserved names, lifecycle boundaries, and “do not rename live resources” rules. |
| `Azure Standardization Expert/alz-orchestrator.md` | Cross-domain decomposition, design → IaC → pipeline → validation → documentation sequencing, read-only diagnostics, and approval gates. Repository-specific HCW paths were not copied as universal facts. |
| `Azure Standardization Expert/iac-repo-standardizer.md` and duplicates | Additive IaC repository standardization, OIDC/bootstrap identity, remote state, validation, policy, documentation, and ALZ-readiness controls. |
| `lz-plan.md`, `lz-review.md`, `lz-change-reviewer.md`, `lz-diagnose.md` | Plan/review/diagnose workflow shapes; project-specific agent names and paths were generalized. |
| `SKILL*.md` | Repeated/tag-hygiene references consolidated; duplicates were not copied. |

## External authoritative sources

| Source | Use |
|---|---|
| [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/) | Five pillars, workload guidance, design principles, trade-offs, review boundaries, and service/workload guides. |
| [Cloud Adoption Framework for Azure](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/) | Strategy, Plan, Ready, Migrate, Modernize, Cloud-native, Govern, Secure, and Manage adoption framing. |
| [What is an Azure landing zone?](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/) | Platform/application landing zones, management-group hierarchy, centralized capabilities, accelerators, and governance inheritance. |
| [Management groups](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-management-groups) | Current hierarchy depth, flatness, policy-scope, subscription placement, and privileged management guidance. |
| [Azure MCP Server documentation](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/) | Official MCP capability, clients, authentication/permissions, and tool-reference boundary. |
| [Bicep what-if](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if) | Non-mutating preview, validation levels, scopes, limitations, and change interpretation. |
| [Deployment stacks](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks) | Managed-resource lifecycle and explicit detach/delete behavior. |
| [AVM Terraform composition](https://azure.github.io/Azure-Verified-Modules/contributing/terraform/composition/) and [TFFR3 provider requirements](https://azure.github.io/Azure-Verified-Modules/spec/TFFR3/) | Current AVM Terraform direction, AzAPI-first requirement, narrow AzureRM exception, version pinning, and module composition. |

## Editorial additions

Gap closures include explicit tenant → management group → subscription → resource group → resource boundaries; ALZ platform/application separation; AVM/AzAPI drift handling; deployment what-if and stack safety; OIDC/bootstrap and remote-state guardrails; current Azure MCP evidence workflow; lifecycle operations and diagnosis; diagram routing without duplicating the Azure Expert Designer; and static-versus-rendered-versus-live evidence labels.
