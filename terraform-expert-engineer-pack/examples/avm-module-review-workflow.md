# Worked example: review a Key Vault wrapper that claims AVM compliance

Prompt: `review-terraform-avm-module.prompt.md`. Skills: azure-verified-modules, terraform-core-and-style, terraform-modules-and-refactoring.

This is a synthetic walkthrough. The module, its inputs and its version numbers are illustrative. Commands and outputs show what the agent would run and see; they are not results recorded by this pack's validation. This is a review-only task, so no files change.

## Request

> Our `modules/key-vault` wrapper says "AVM compliant" in its README. Review it before we publish it to the private registry. Findings only.

## 1. Establish the contract

| Fact | Value |
|---|---|
| Module | `modules/key-vault`, commit `4e1d9b2` |
| Goal | consume the AVM Key Vault module correctly through an internal wrapper |
| AVM specification | not retrieved: this session has no web access. Rows that depend on its exact wording are marked "unable to verify" |
| Repository instructions | `CONTRIBUTING.md` asks for examples and a changelog for every module |
| Authorization | review only; local checks |

## 2. What the agent read

```hcl
# modules/key-vault/main.tf (excerpt)
provider "azurerm" {
  features {}
}

module "vault" {
  source = "git::https://github.com/Azure/terraform-azurerm-avm-res-keyvault-vault.git?ref=main"
  count  = var.enabled ? 1 : 0

  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  tenant_id           = var.tenant_id
}

# modules/key-vault/terraform.tf
terraform {
  required_version = ">= 1.5"
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
}

# modules/key-vault/outputs.tf
output "key_vault" {
  value = module.vault
}

# modules/key-vault/variables.tf (excerpt)
variable "secret_values" {
  type        = map(string)
  description = "Secrets to create in the vault, keyed by secret name."
}
```

## 3. Local checks

```text
$ terraform fmt -check -recursive        (exit 0)
$ terraform init -backend=false          (exit 0; fetched the Git module at ref=main)
$ terraform validate                     (exit 0) Success! The configuration is valid.
```

`init` fetched whatever commit `main` points at today. A rerun tomorrow could fetch different code, which is itself part of finding R1.

## 4. Requirement table

| Area | Requirement as checked | Result | Evidence | Remediation |
|---|---|---|---|---|
| Module sources | AVM module from the Terraform Registry with a pinned version | **fail** (R1) | `main.tf:6`, Git source at `ref=main` | `source = "Azure/avm-res-keyvault-vault/azurerm"` with an exact `version` the team has reviewed |
| Terraform and provider constraints | `required_providers` with source and compatible constraints | **fail** (R2) | `terraform.tf:4`, azurerm has no version constraint | add a constraint compatible with the pinned AVM module's own requirement |
| Permitted providers | only providers the current specification permits | unable to verify | specification not retrieved | check against the current specification |
| Provider configuration | none in the child module | **fail** (R3) | `main.tf:1` | remove the block; the caller passes the provider |
| Switches | no blanket `enabled` switch | **fail** (R4) | `main.tf:7`, `count = var.enabled ? 1 : 0` | remove; a caller that does not want a vault omits the module call |
| Outputs | no whole-module outputs | **fail** (R5) | `outputs.tf:2`, `value = module.vault` | output the specific attributes consumers use, such as the vault's resource ID and URI |
| Sensitive values | sensitive inputs marked | **fail** (R6) | `variables.tf`: `secret_values` lacks `sensitive = true` | mark it sensitive |
| Naming | lower snake_case | pass | all identifiers | none |
| Collections | stable `for_each` keys | pass | role assignments use `toset(var.admin_object_ids)` | none |
| Variables | precise types and descriptions | pass | every variable is typed and described | none |
| Lifecycle | no unreviewed `ignore_changes` | pass | none present | none |
| Layout | file names and ordering per current style | unable to verify | specification not retrieved; `terraform fmt` passes | check against the current specification |
| Optional resources | feature toggles for newly introduced optional resources | not applicable | no optional resources are introduced | none |
| Documentation | examples, changelog, upgrade notes | **fail** (R7) | `examples/basic` present; no `CHANGELOG.md` | add a changelog, as `CONTRIBUTING.md` requires |
| Tests | tests appropriate to the release process | **fail** (R8) | no `tests/` directory | add plan-mode tests of the wrapper's interface |

R1, R3 and R4 block publication. R1 makes builds non-reproducible. R3 breaks provider aliasing for callers. R4 turns a later removal of the switch into a state address change (`module.vault[0]` to `module.vault`) for every consumer, which needs a `moved` block when it is fixed.

## 5. Outside AVM style

| Concern | Status | Evidence class |
|---|---|---|
| Terraform correctness | `validate` passes; no plan was run | local |
| Provider API behaviour | not exercised | unavailable |
| Security posture (network access, purge protection) | defaults come from whichever AVM module version is fetched; not reviewed | unavailable |
| Official AVM certification | not established. This is an internal wrapper, not an AVM module, so "AVM compliant" in the README overstates it. "Built on the AVM Key Vault module" is accurate once R1 is fixed | static |

## Completion report

Outcome: review complete. Eight findings, three of which block publication; two requirements could not be verified without the current specification.

### objective

Review `modules/key-vault` against AVM requirements before it is published to the private registry.

### scope_and_authorization

| Item | Value |
|---|---|
| Configuration directory | `modules/key-vault` at commit `4e1d9b2` |
| Environment | none; review only |
| Terraform | local CLI satisfies `>= 1.5` |
| Providers | `hashicorp/azurerm`, unconstrained (finding R2) |
| Backend | none (module) |
| Authorization | findings only; local checks |
| Not authorized | edits, publishing |

### changed_files

None. This was a review.

### commands_and_results

| Command | Directory | Exit | Result |
|---|---|---|---|
| `terraform fmt -check -recursive` | `modules/key-vault` | 0 | clean |
| `terraform init -backend=false` | `modules/key-vault` | 0 | Git module fetched at `ref=main` |
| `terraform validate` | `modules/key-vault` | 0 | valid |

Not run: `terraform plan` (no target subscription in scope); retrieval of the AVM specification (no web access).

### plan_or_state_impact

None. No plan, no state.

### evidence_classification

| Claim | Class | Evidence |
|---|---|---|
| R1 to R8 | static | file and line references above |
| The module is valid Terraform | local | `validate` |
| Provider and layout rows that depend on the specification | unavailable | specification not retrieved |
| The fetched AVM module's defaults are secure | unavailable | not reviewed; the version is not pinned |
| The module is AVM-certified | unavailable | never established by a local review |

### risks_and_limitations

The table covers the Skill's high-value checks, not the whole AVM specification. The two "unable to verify" rows may hide further failures. Fixing R4 changes consumer state addresses, so the fix needs a `moved` block. Callers that set `enabled` must also change, so the release is breaking.

### next_safe_action

The module owner decides which findings to fix. Then the agent re-reviews with the current AVM specification retrieved, and plans the wrapper's example against a sandbox subscription before the module is published.
