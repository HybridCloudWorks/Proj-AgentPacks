# Worked example: adopt a hand-built storage account with import blocks

Prompt: `import-terraform-resources.prompt.md`. Skills: terraform-state-backends-and-imports, terraform-core-and-style.

This is a synthetic walkthrough. Subscription IDs, names and versions are illustrative. Commands and outputs show what the agent would run and see; they are not results recorded by this pack's validation. Plan excerpts are trimmed to addresses and actions.

## Request

> The data team created storage account `stdataprod001` with containers `raw` and `curated` by hand in `rg-data-prod`. Bring them under the `data-platform/prod` root without changing them. You can edit and plan with the `tf-plan-prod` identity. Do not apply.

## 1. Establish the contract

| Fact | Value |
|---|---|
| Terraform | 1.9.8 installed; `~> 1.9` required |
| Provider | `hashicorp/azurerm` 4.x, locked |
| Backend | `azurerm`: account `sttfstateprod`, container `tfstate`, key `data-platform/prod.tfstate`, `use_azuread_auth = true` |
| Authorization | edit and plan; no apply |

Terraform Search was not used: the installed CLI does not provide it, so the narrow manual path applies. The provider documentation for the locked azurerm version gives each import ID format. The storage account uses its resource ID. A container declared with `storage_account_id` uses the resource-manager ID under `blobServices/default/containers`. Older provider versions used a data-plane URL, so the lock file decides which format applies.

## 2. Map objects to addresses

| Remote object | Target address |
|---|---|
| `.../storageAccounts/stdataprod001` | `azurerm_storage_account.data` |
| `.../stdataprod001/blobServices/default/containers/raw` | `azurerm_storage_container.data["raw"]` |
| `.../stdataprod001/blobServices/default/containers/curated` | `azurerm_storage_container.data["curated"]` |

Each object maps to one address, and no other root manages these objects (a search of the repository for `stdataprod001` found only this root).

## 3. Write import blocks

```hcl
# envs/data-platform/prod/imports.tf
locals {
  data_account_id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-data-prod/providers/Microsoft.Storage/storageAccounts/stdataprod001"
}

import {
  to = azurerm_storage_account.data
  id = local.data_account_id
}

import {
  for_each = toset(["raw", "curated"])
  to       = azurerm_storage_container.data[each.key]
  id       = "${local.data_account_id}/blobServices/default/containers/${each.key}"
}
```

The containers are small, so their configuration is written by hand. For the storage account, a configuration draft is generated:

```text
$ terraform plan -generate-config-out=generated_storage.tf
```

## 4. Clean the generated draft

The draft sets roughly forty attributes, most of them provider defaults or computed values. The agent keeps what describes the account, matches every live value, and removes the rest:

```hcl
resource "azurerm_storage_account" "data" {
  name                            = "stdataprod001"
  resource_group_name             = "rg-data-prod"
  location                        = "westeurope"
  account_tier                    = "Standard"
  account_replication_type        = "ZRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = true # matches live; see finding F1
  tags = {
    owner = "data-team"
  }
}

resource "azurerm_storage_container" "data" {
  for_each              = toset(["raw", "curated"])
  name                  = each.key
  storage_account_id    = azurerm_storage_account.data.id
  container_access_type = "private"
}
```

## 5. Plan until the import is pure

The first plan used the repository's standard `local.tags`, which adds `managed_by = "terraform"`:

```text
  # azurerm_storage_account.data will be updated in-place
  # (imported from "/subscriptions/0000…/storageAccounts/stdataprod001")
      ~ tags = {
          + "managed_by" = "terraform"
            # (1 unchanged element hidden)
        }
  # azurerm_storage_container.data["curated"] will be imported
  # azurerm_storage_container.data["raw"] will be imported

Plan: 3 to import, 0 to add, 1 to change, 0 to destroy.
```

The request said "without changing them", so the tags now match live, and the standard tag moves to a follow-up change. Second plan:

```text
Plan: 3 to import, 0 to add, 0 to change, 0 to destroy.
```

## 6. Findings to carry forward

- **F1 (security, high).** `allow_nested_items_to_be_public` is true on a production data account, so any container can be made public. The import keeps the live value, so the import stays a pure state change. Hardening goes in a separate reviewed change, with the data team's agreement.
- **F2 (state sensitivity).** Importing a storage account writes its access keys and connection strings into state as sensitive attributes. The state container uses Entra ID authentication. Who holds data-plane roles on it could not be listed with `tf-plan-prod`.

The `import` blocks may stay after apply; they do nothing once the objects are in state. Remove them in a later tidy-up.

## Completion report

Outcome: import prepared and verified as pure by plan; not applied.

### objective

Bring storage account `stdataprod001` and containers `raw` and `curated` under `envs/data-platform/prod`, with no change to the live resources.

### scope_and_authorization

| Item | Value |
|---|---|
| Configuration directory | `envs/data-platform/prod` |
| Environment | prod, subscription `0000…` (synthetic), westeurope |
| Terraform | 1.9.8; `~> 1.9` required |
| Providers | `hashicorp/azurerm` 4.x, lock file unchanged |
| Backend | `azurerm`, key `data-platform/prod.tfstate` |
| Authorization | edit and plan with `tf-plan-prod` |
| Not authorized | apply (the import writes three objects into prod state) |

### changed_files

| File | Change |
|---|---|
| `envs/data-platform/prod/imports.tf` | new; three import bindings |
| `envs/data-platform/prod/storage.tf` | new; cleaned account and container configuration |
| `generated_storage.tf` | generated draft; deleted after cleaning, not committed |

### commands_and_results

| Command | Directory | Exit | Result |
|---|---|---|---|
| `terraform fmt -check` | `envs/data-platform/prod` | 0 | clean |
| `terraform validate` | `envs/data-platform/prod` | 0 | valid |
| `terraform plan -generate-config-out=generated_storage.tf` | `envs/data-platform/prod` | 0 | draft written |
| `terraform plan` (first) | `envs/data-platform/prod` | 0 | 3 to import, 1 to change (tags) |
| `terraform plan` | `envs/data-platform/prod` | 0 | 3 to import, 0 to add, 0 to change, 0 to destroy |

Not run: `terraform apply`. Also not run: a role-assignment listing on the state container (the identity is not permitted).

### plan_or_state_impact

Three objects to import, with no add, change or destroy. Applying the plan adds `azurerm_storage_account.data`, `azurerm_storage_container.data["raw"]` and `azurerm_storage_container.data["curated"]` to prod state, including the account's sensitive key attributes. State was not written.

### evidence_classification

| Claim | Class | Evidence |
|---|---|---|
| Import ID formats | static | provider documentation for the locked version |
| Configuration matches live settings | live-cloud | second plan, which refreshed the real objects |
| No other root manages these objects | static | repository search |
| Public nested access is enabled | live-cloud | generated draft and plan |
| Who can read the state container | unavailable | `tf-plan-prod` cannot list role assignments |
| Apply performs no Azure write | inferred | a pure-import plan; not observed until apply |

### risks_and_limitations

Until F1 is fixed, the account allows public containers. The import does not make that worse, but it does not fix it either. The state will hold storage keys, and access to the state container is unconfirmed. If the data team changes the account before apply, the plan goes stale and must be run again.

### next_safe_action

The requester authorizes `terraform apply` of the pure-import plan from this commit through the approval handoff, after the platform team confirms who can read the state container. F1 and the standard tags then follow as a separate change with its own plan.
