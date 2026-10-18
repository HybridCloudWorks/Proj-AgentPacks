---
name: terraform-core-and-style
description: Author, review, and validate ordinary Terraform and HCL configuration, provider requirements, dependency locks, variables, outputs, expressions, and secure style.
---

# Terraform Core and HCL Style

Use this Skill for ordinary Terraform configuration, HCL review, provider declarations, version constraints, dependency locks, resource expressions, variables, outputs, and local validation.

## Establish the contract

- Determine Terraform CLI version, provider versions, module sources, root versus child module, execution mode, backend, and expected cloud.
- Read repository-specific style, security, policy, and CI instructions before editing.
- Keep Terraform source UTF-8 and run terraform fmt on changed configuration.
- Keep one clear terraform block per module when repository style permits, with required_version and required_providers.
- Declare provider source addresses and intentional version constraints; commit .terraform.lock.hcl for root configurations.
- Use lower snake_case names, nouns for resources, typed and described variables, described outputs, and precise validation where it improves the interface.
- Prefer for_each with stable keys for collections; use count only for genuinely positional or conditional instances.
- Keep provider configuration in the root module; child modules declare requirements and use configuration_aliases only when needed.

## Security and review

Keep credentials out of HCL, tfvars, state, plans, logs, and version control. Mark sensitive variables and outputs accurately. Review dynamic blocks, null and unknown values, lifecycle rules, replace behavior, provider aliases, and data sources for unintended access.

Run terraform init -backend=false for reusable-module validation when backend access is not required, then terraform validate. Use terraform plan with real variables and an authorized backend when contextual values, data sources, or state matter. Record what each check does not prove.

## Troubleshooting

Classify errors as syntax, initialization/provider installation, configuration type, dependency graph, backend/state, provider API, or policy. Reduce to a minimal reproducer, inspect the exact installed Terraform/provider version, and avoid solving a state or provider problem by broadening permissions or deleting state.
