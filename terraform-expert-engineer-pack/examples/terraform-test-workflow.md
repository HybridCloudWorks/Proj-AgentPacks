# Worked example: mocked unit tests and a gated integration test for a bucket module

Prompt: `add-terraform-tests.prompt.md`. Skills: terraform-testing-and-validation, terraform-core-and-style.

This is a synthetic walkthrough. Names and versions are illustrative. Commands and outputs show what the agent would run and see; they are not results recorded by this pack's validation. Part of the outcome is unverified: the integration test is written but not run.

## Request

> Add tests to `modules/log-bucket`. I want fast checks that need no AWS credentials, and an integration test we can run later. Don't put credentials anywhere.

## 1. Establish the contract

| Fact | Value |
|---|---|
| Module interface | `name` (string, validated against S3 naming), `versioning_enabled` (bool, default true), `kms_key_arn` (string, default null), `expiration_rules` (map of objects, default `{}`); outputs `bucket_name` and `bucket_arn` |
| Module `required_version` | `>= 1.5` |
| CLI that runs tests | 1.9.8 locally; CI pins the same version |
| Provider | `hashicorp/aws` 5.x, locked |
| Authorization | write tests and run anything that needs no credentials; no AWS account was offered |

`mock_provider` needs a newer Terraform than the module's floor of 1.5. The module's `required_version` stays as it is, because raising it would break consumers for the sake of tests. The CLI that runs the tests is pinned to 1.9.8 instead.

## 2. Choose the level per behaviour

| Behaviour | Level | Why |
|---|---|---|
| Versioning defaults to enabled | plan, mocked | configuration logic only |
| Invalid bucket name rejected | plan, mocked, `expect_failures` | variable validation |
| SSE-S3 when no KMS key; SSE-KMS when given | plan, mocked | conditional logic |
| One lifecycle rule per `expiration_rules` key | plan, mocked | `for_each` keys |
| `bucket_arn` output is wired to the bucket | apply, mocked | computed values exist only after apply; a mocked apply creates nothing |
| Real bucket is versioned and encrypted | apply, real AWS | provider and API behaviour cannot be mocked |

## 3. Unit tests

```hcl
# modules/log-bucket/tests/unit.tftest.hcl
mock_provider "aws" {
  mock_resource "aws_s3_bucket" {
    defaults = {
      arn = "arn:aws:s3:::example-logs"
    }
  }
}

variables {
  name = "example-logs"
}

run "versioning_defaults_to_enabled" {
  command = plan

  assert {
    condition     = aws_s3_bucket_versioning.this.versioning_configuration[0].status == "Enabled"
    error_message = "Versioning must be enabled unless the caller turns it off."
  }
}

run "rejects_invalid_bucket_name" {
  command = plan

  variables {
    name = "Example_Logs"
  }

  expect_failures = [var.name]
}

run "bucket_arn_output_is_wired" {
  command = apply

  assert {
    condition     = startswith(output.bucket_arn, "arn:aws:s3:::")
    error_message = "bucket_arn must come from the bucket's ARN."
  }
}
```

The encryption and lifecycle scenarios come after these, follow the same pattern, and are left out here.

## 4. First run: the mock hid the shape

At first the provider was mocked with a bare `mock_provider "aws" {}` and no `mock_resource` block. The first run:

```text
tests/unit.tftest.hcl... in progress
  run "versioning_defaults_to_enabled"... pass
  run "rejects_invalid_bucket_name"... pass
  run "bucket_arn_output_is_wired"... fail
╷
│ Error: Test assertion failed
│
│   on tests/unit.tftest.hcl line 31, in run "bucket_arn_output_is_wired":
│   31:     condition     = startswith(output.bucket_arn, "arn:aws:s3:::")
│     ├────────────────
│     │ output.bucket_arn is "x7k2p9qa"
│
│ bucket_arn must come from the bucket's ARN.
╵
  run "uses_sse_s3_without_kms_key"... pass
  run "one_rule_per_expiration_key"... pass
tests/unit.tftest.hcl... tearing down
tests/unit.tftest.hcl... fail

Failure! 4 passed, 1 failed.
```

The module was right. The mock had generated a random string for the computed `arn`. Giving the computed value a deliberate shape fixed the test:

```text
Success! 5 passed, 0 failed.
```

This test now proves that the output is wired to the bucket's `arn` attribute. It does not prove what AWS returns.

## 5. Integration test, written but not run

```hcl
# modules/log-bucket/tests/integration.tftest.hcl
# Apply mode against real AWS. Run only in the sandbox account, with credentials from
# the environment. terraform test destroys what it created at the end of the file.
provider "aws" {
  region = "eu-west-1"
}

variables {
  name = "tftest-log-bucket-ci"
}

run "creates_versioned_bucket" {
  command = apply

  assert {
    condition     = aws_s3_bucket_versioning.this.versioning_configuration[0].status == "Enabled"
    error_message = "The real bucket is not versioned."
  }
}
```

Running it creates a real bucket, costs a little and needs cleanup. If the teardown fails, a bucket named `tftest-log-bucket-ci` is left behind, and the sandbox owner removes it. The fixed name also means two concurrent runs would collide. The CI job that runs this test must use one concurrency group.

## Completion report

Outcome: unit tests added and passing locally. The integration test is written and not run.

### objective

Add credential-free tests and a later-runnable integration test to `modules/log-bucket`, with no credentials in code.

### scope_and_authorization

| Item | Value |
|---|---|
| Configuration directory | `modules/log-bucket` (child module) |
| Environment | none for unit tests; integration intended for the sandbox account |
| Terraform | 1.9.8 runs the tests; the module still requires `>= 1.5` |
| Providers | `hashicorp/aws` 5.x, lock file unchanged |
| Backend | none (module) |
| Authorization | write tests; run credential-free tests |
| Not authorized | any run against real AWS |

### changed_files

| File | Change |
|---|---|
| `modules/log-bucket/tests/unit.tftest.hcl` | new; five mocked scenarios |
| `modules/log-bucket/tests/integration.tftest.hcl` | new; one apply-mode scenario for the sandbox account |

### commands_and_results

| Command | Directory | Exit | Result |
|---|---|---|---|
| `terraform fmt -check -recursive` | `modules/log-bucket` | 0 | clean |
| `terraform init -backend=false` | `modules/log-bucket` | 0 | providers from the lock file |
| `terraform validate` | `modules/log-bucket` | 0 | valid |
| `terraform test -filter=tests/unit.tftest.hcl` (first) | `modules/log-bucket` | 1 | 4 passed, 1 failed (mock shape) |
| `terraform test -filter=tests/unit.tftest.hcl` | `modules/log-bucket` | 0 | 5 passed, 0 failed |

Not run: `terraform test -filter=tests/integration.tftest.hcl` (no AWS credentials or account authorized).

### plan_or_state_impact

None. The unit tests use mocked providers and create nothing. The integration test was not run, so nothing was created and nothing needs cleanup.

### evidence_classification

| Claim | Class | Evidence |
|---|---|---|
| Defaults, validation, encryption choice and rule keys behave as designed | local | mocked `terraform test`, 5 passed |
| `bucket_arn` is wired to the bucket's `arn` | local | mocked apply; the value is the mock's |
| AWS creates a versioned, encrypted bucket from this module | unavailable | integration test not run |
| Teardown leaves nothing behind | unavailable | not run |

### risks_and_limitations

The mocks prove configuration logic, not the provider schema or the API. A provider upgrade that renames an attribute would surface in `validate`, not in these tests. The integration test's fixed bucket name is safe only with serialized runs.

### next_safe_action

The repository owner decides whether to run the integration test. If so, the owner authorizes credentials for the sandbox account and a cleanup owner, and runs `terraform test -filter=tests/integration.tftest.hcl` there. Separately, the unit tests can be added to CI with terraform-ci-cd-and-quality.
