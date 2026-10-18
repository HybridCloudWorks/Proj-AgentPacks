# Design Decisions

## Broad trigger, narrow Skills

Terraform and Terraform-based IaC should route to this Agent broadly. Detailed procedures remain in nine Skills so a normal HCL edit does not load HCP Stacks, policy conversion, provider Go, and AVM certification guidance at once.

## Main Terraform first

The pack prioritizes Terraform language, modules, state, tests, CI/CD, and plan safety. HCP Terraform/Enterprise, Stacks, policy, provider development, and AVM are included because the supplied sources and user request identify them as high-value adjacent HCL products. Individual provider-specific cloud recipes were not promoted to separate Skills.

## State is a first-class boundary

S3 and Azure Storage are treated as distinct backend choices with locking, access, versioning/recovery, identity, migration, and sensitivity considerations. HCP Terraform state is treated as a workspace-controlled product boundary, not as a synonym for local CLI workspaces.

## Version-sensitive material

Terraform Search, mock providers, Stacks syntax, tfpolicy, provider framework behavior, AVM requirements, and backend locking details can change. Skills route to current official documentation and require checking the installed version before making exact claims.

## Source versus additions

The Agent, core style, modules, state, Stacks, tests, policies, provider development, CI/CD, and AVM content are source-derived and consolidated. The explicit routing/evidence contract and the pack-level gap closure around backend/security/state safety are editorial additions needed to make the expert complete and portable.
