# AVM requirement review

Use when an Azure Terraform module consumes Azure Verified Modules or is meant to meet AVM requirements. The azure-verified-modules Skill reports each requirement as pass, fail, not applicable or unable to verify. This record keeps those results apart from Terraform correctness, provider behaviour, security posture and official certification.

## Module

| Item | Value |
|---|---|
| Module path or repository | |
| Commit or version reviewed | |
| Goal: consume AVM modules, or meet AVM requirements | |
| AVM specification consulted: URL and retrieval date, or "not retrieved" | |
| Repository instructions read | |
| Review only, or authorized fixes | |

If the specification was not retrieved, every row that depends on its exact wording is "unable to verify". The high-value checks below can still be applied.

## Requirements

| Area | Requirement as checked | Result | Evidence (file:line or command) | Remediation |
|---|---|---|---|---|
| Module sources | AVM modules from the Terraform Registry with pinned versions; no silent substitution of Git or non-AVM modules | | | |
| Terraform and provider constraints | `required_version` and `required_providers` with source and compatible constraints | | | |
| Permitted providers | Only providers the current specification permits for this module | | | |
| Provider configuration | None in child modules beyond supported aliases; the caller passes providers | | | |
| Naming | Lower snake_case | | | |
| Collections | Stable `for_each` keys | | | |
| Variables | Precise types, descriptions, non-sensitive defaults, no unnecessary nullable values | | | |
| Sensitive values | Sensitive inputs and outputs marked accurately | | | |
| Outputs | No whole-resource or whole-module outputs | | | |
| Switches | No blanket `enabled` switch, no `module_depends_on` | | | |
| Lifecycle | No unreviewed `ignore_changes` | | | |
| Layout | `terraform.tf`, variables, locals, outputs and resource ordering per current style; `terraform fmt` | | | |
| Optional resources | Feature toggles for newly introduced optional resources where required | | | |
| Documentation | Module documentation, examples, changelog, upgrade notes | | | |
| Tests | Tests appropriate to the release process | | | |

## Outside AVM style

| Concern | Status | Evidence class |
|---|---|---|
| Terraform correctness (`validate`, plan) | | |
| Provider API behaviour | | |
| Security posture | | |
| Official AVM certification | Never established by a local review | |

## Summary

Counts by result, the blocking failures, and the next safe action.
