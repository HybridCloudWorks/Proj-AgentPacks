# Worked example: extract subnets into a module and key them by zone, with no recreation

Prompt: `refactor-terraform-module.prompt.md`. Skills: terraform-modules-and-refactoring, terraform-core-and-style, terraform-testing-and-validation.

This is a synthetic walkthrough. Names, account details and versions are illustrative. Commands and outputs show what the agent would run and see; they are not results recorded by this pack's validation. Plan excerpts are trimmed to addresses and actions.

## Request

> Move the private subnets in `envs/network` into a reusable `modules/network` child module, and key them by availability zone instead of list position. Nothing in production may be recreated. You can edit, list state addresses and run plans in staging and prod with the `network-plan-readonly` role. Do not apply.

## 1. Establish the contract

| Fact | Where it came from | Value |
|---|---|---|
| Terraform | `required_version`, `terraform version` | `~> 1.9` required; 1.9.8 installed |
| Provider | `.terraform.lock.hcl` | `hashicorp/aws` 5.x, with checksums for linux_amd64 and darwin_arm64 |
| Backend | `backend.tf` plus `staging.s3.tfbackend` and `prod.s3.tfbackend` | S3, keys `network/staging.tfstate` and `network/prod.tfstate` |
| Environments | `staging.tfvars`, `prod.tfvars` | staging lists 2 zones, prod lists 3, both in a, b, c order |
| Authorization | the user | edit; `terraform state list` and `terraform plan` in staging and prod; no apply, no state commands |

The current configuration uses positional `count`:

```hcl
resource "aws_subnet" "private" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.main.id
  availability_zone = var.private_subnets[count.index].az
  cidr_block        = var.private_subnets[count.index].cidr
}

resource "aws_route_table_association" "private" {
  count          = length(var.private_subnets)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
```

Removing a zone from the middle of the list would shift every later index and force replacement. That is the reason for the change.

## 2. Map addresses before editing

`terraform state list` (addresses only, no values) in each environment, filtered to the two resource types:

| Current address | New address | staging | prod |
|---|---|---|---|
| `aws_subnet.private[0]` | `module.network.aws_subnet.private["eu-west-1a"]` | present | present |
| `aws_subnet.private[1]` | `module.network.aws_subnet.private["eu-west-1b"]` | present | present |
| `aws_subnet.private[2]` | `module.network.aws_subnet.private["eu-west-1c"]` | absent | present |
| `aws_route_table_association.private[0]` | `module.network.aws_route_table_association.private["eu-west-1a"]` | present | present |
| `aws_route_table_association.private[1]` | `module.network.aws_route_table_association.private["eu-west-1b"]` | present | present |
| `aws_route_table_association.private[2]` | `module.network.aws_route_table_association.private["eu-west-1c"]` | absent | present |

`moved` blocks cannot use variables, so this static map is only correct because both variable files list zones in the same order. In staging the index-2 blocks find no object and do nothing.

## 3. Edit

The child module declares its provider requirement and takes no provider configuration:

```hcl
# modules/network/versions.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

# modules/network/subnets.tf
resource "aws_subnet" "private" {
  for_each          = var.private_subnets
  vpc_id            = var.vpc_id
  availability_zone = each.key
  cidr_block        = each.value.cidr
}

resource "aws_route_table_association" "private" {
  for_each       = aws_subnet.private
  subnet_id      = each.value.id
  route_table_id = var.route_table_id
}
```

`var.private_subnets` is typed `map(object({ cidr = string }))` with a description and a validation that keys look like zone names. The root keeps its list variable, so no variable file changes, and converts it at the call:

```hcl
module "network" {
  source          = "../../modules/network"
  vpc_id          = aws_vpc.main.id
  route_table_id  = aws_route_table.private.id
  private_subnets = { for s in var.private_subnets : s.az => { cidr = s.cidr } }
}
```

`envs/network/moves.tf` received one `moved` block per subnet row of the map, for example:

```hcl
moved {
  from = aws_subnet.private[0]
  to   = module.network.aws_subnet.private["eu-west-1a"]
}
```

## 4. First plan: the review catches a destroy

Staging, after `terraform init -backend-config=staging.s3.tfbackend`:

```text
  # aws_subnet.private[0] has moved to module.network.aws_subnet.private["eu-west-1a"]
  # aws_subnet.private[1] has moved to module.network.aws_subnet.private["eu-west-1b"]

  # aws_route_table_association.private[0] will be destroyed
  # (because aws_route_table_association.private[0] is not in configuration)
  # aws_route_table_association.private[1] will be destroyed
  # module.network.aws_route_table_association.private["eu-west-1a"] will be created
  # module.network.aws_route_table_association.private["eu-west-1b"] will be created

Plan: 2 to add, 0 to change, 2 to destroy.
```

The subnets move, but the associations were moved into the module without `moved` blocks. Destroying and recreating an association detaches the subnet from its route table for the gap between the two calls, which cuts private egress. That blocks the change. The fix is three more `moved` blocks for the association rows. There are no state commands.

Second staging plan:

```text
  # aws_route_table_association.private[0] has moved to module.network.aws_route_table_association.private["eu-west-1a"]
  ...
Plan: 0 to add, 0 to change, 0 to destroy.
```

Prod, after re-initializing with `prod.s3.tfbackend`: six moves, `Plan: 0 to add, 0 to change, 0 to destroy.`

## 5. Test the module's keying

A plan-mode test with a mocked provider proves the keys follow the input map. It needs no credentials:

```hcl
# modules/network/tests/keys.tftest.hcl
mock_provider "aws" {}

variables {
  vpc_id          = "vpc-0example"
  route_table_id  = "rtb-0example"
  private_subnets = {
    "eu-west-1a" = { cidr = "10.0.1.0/24" }
    "eu-west-1b" = { cidr = "10.0.2.0/24" }
  }
}

run "subnets_keyed_by_zone" {
  command = plan

  assert {
    condition     = toset(keys(aws_subnet.private)) == toset(["eu-west-1a", "eu-west-1b"])
    error_message = "Subnets must be keyed by availability zone."
  }
}
```

This proves the configuration logic only. It says nothing about AWS accepting the CIDRs.

## 6. Release label

`modules/network` lives in this repository and has no registry consumers. Its only consumers are the two environments, and both were planned. No version label applies. The `moved` blocks stay in `envs/network/moves.tf` until both environments have applied them. Removing them earlier would turn the moves back into destroy and create.

## Completion report

Outcome: refactor prepared and verified by plan in both environments; not applied.

### objective

Extract the private subnets and their route table associations into `modules/network`, keyed by availability zone, with no resource recreated in staging or prod.

### scope_and_authorization

| Item | Value |
|---|---|
| Configuration directories | `envs/network` (root), `modules/network` (new child) |
| Environments | staging and prod, eu-west-1 |
| Terraform | 1.9.8 installed; `~> 1.9` required |
| Providers | `hashicorp/aws` 5.x from the committed lock file, unchanged |
| Backend | S3, `network/staging.tfstate` and `network/prod.tfstate` |
| Authorization | edit, `state list`, `plan` with `network-plan-readonly`; given by the requester |
| Not authorized | apply in either environment |

### changed_files

| File | Change |
|---|---|
| `modules/network/versions.tf` | new; provider requirement only |
| `modules/network/variables.tf` | new; typed, described, validated inputs |
| `modules/network/subnets.tf` | new; subnets and associations with `for_each` |
| `modules/network/outputs.tf` | new; subnet IDs by zone |
| `modules/network/tests/keys.tftest.hcl` | new; mocked plan-mode test |
| `envs/network/main.tf` | resources replaced by the module call |
| `envs/network/moves.tf` | new; six `moved` blocks |

### commands_and_results

| Command | Directory | Exit | Result |
|---|---|---|---|
| `terraform fmt -check -recursive` | repository root | 0 | no changes needed |
| `terraform init -backend=false` then `terraform validate` | `modules/network` | 0 | valid |
| `terraform test` | `modules/network` | 0 | 1 passed, 0 failed |
| `terraform state list` | `envs/network`, staging and prod | 0 | addresses recorded in the map |
| `terraform plan` (first) | `envs/network`, staging | 0 | 2 to add, 2 to destroy; defect found |
| `terraform plan` | `envs/network`, staging | 0 | 0 to add, 0 to change, 0 to destroy; 4 moved |
| `terraform plan` | `envs/network`, prod | 0 | 0 to add, 0 to change, 0 to destroy; 6 moved |

Not run: `terraform apply` (not authorized).

### plan_or_state_impact

No create, update, replace or destroy in either environment. Staging moves 4 addresses and prod moves 6. State was not written; the moves are recorded only when the plans are applied. No provider or lock-file change. No sensitive values in the affected resources.

### evidence_classification

| Claim | Class | Evidence |
|---|---|---|
| Formatting and configuration are valid | local | `fmt`, `validate` |
| Module keys follow the input map | local | mocked `terraform test` |
| Current addresses per environment | live-cloud | `terraform state list` against each S3 backend |
| Plans are pure moves in both environments | live-cloud | staging and prod plans with refresh |
| Both environments map index to zone identically | static | variable files read side by side |
| Apply records the moves without API calls | inferred | Terraform moves are state-only; not observed until apply |

### risks_and_limitations

The plans are valid only for this commit and the state as read. A change merged in between needs a fresh plan. Any third environment added later must list zones in the same order, or it needs its own `moved` blocks. The mocked test does not exercise AWS.

### next_safe_action

The requester authorizes `terraform apply` in staging with a plan saved from this commit, using the approval handoff. Prod follows only after staging applies cleanly, with its own plan and handoff.
