# Worked example: convert a cross-resource Sentinel policy to tfpolicy

Prompt: `author-terraform-policy.prompt.md`. Skills: terraform-policy-and-governance, terraform-cloud-and-stacks.

This is a synthetic walkthrough. The organization, policy set and file names are illustrative. Commands and outputs show what the agent would run and see; they are not results recorded by this pack's validation. Part of the outcome is unverified: the tfpolicy tests are written but not run, and one behaviour needs a decision from the policy owner.

## Request

> Convert our Sentinel policy `s3-buckets-encrypted` to tfpolicy, and test the cross-resource part. Keep it advisory for now.

## 1. Establish the contract

| Fact | Value |
|---|---|
| Current policy | `policies/sentinel/s3-buckets-encrypted.sentinel`, with five Sentinel test cases |
| Where it is enforced | HCP Terraform policy set `aws-baseline`, connected to `policies/sentinel` through VCS. `sentinel.hcl` sets `enforcement_level = "advisory"` |
| Local runners | Sentinel CLI installed; no tfpolicy runner on PATH. The repository's CI job for its two existing tfpolicy policies pins a runner, and its version is recorded in that job |
| Authorization | write the converted policy and tests on a branch; do not change the policy set or its enforcement |

## 2. Classify the original

The rule is: every managed S3 bucket being created or updated must have an `aws_s3_bucket_server_side_encryption_configuration` that refers to it.

- Input surface: the plan (bucket changes) and the configuration (references).
- Kind: a graph or reference rule, not a direct attribute rule.
- Stage: post-plan, advisory.

Excerpt of the original:

```sentinel
import "tfplan/v2" as tfplan
import "tfconfig/v2" as tfconfig

# Managed buckets being created or updated
buckets = filter tfplan.resource_changes as _, rc {
	rc.type is "aws_s3_bucket" and
	rc.mode is "managed" and
	(rc.change.actions contains "create" or rc.change.actions contains "update")
}

# Encryption configurations as written in configuration
encryption_configs = filter tfconfig.resources as _, r {
	r.type is "aws_s3_bucket_server_side_encryption_configuration"
}

# ...a bucket passes when an encryption configuration's config.bucket.references
# names it, after the module-qualified address is rebuilt. Trimmed here.
```

`sentinel test` on the original passes all five cases. That is the baseline the conversion must match.

## 3. Map constructs and flag what does not translate

| Sentinel construct | Converted approach | Equivalent? |
|---|---|---|
| Filter `resource_changes` by type, mode and create or update | Rule scoped to managed `aws_s3_bucket`, with operation handling for create and update | Yes, if the installed runner names operations the same way; check in CI |
| `config.bucket.references` (configuration metadata) | Match on the planned `bucket` value of each encryption configuration | **No.** References are configuration metadata. The converted rule compares values |
| Rebuilding the module-qualified address from `module_address` | Not needed when matching values | Approximation. It also matches a configuration in another module that happens to target the same bucket name, which Sentinel would not |
| A new bucket whose name is computed (for example from `random_id`) | The value is unknown at plan time | **No.** Sentinel passes through the reference. The converted rule cannot decide |

The last row changes behaviour, and the agent does not choose silently. The draft treats an unknown bucket name as an advisory failure, with the message "Encryption for this bucket cannot be confirmed until its name is known; set the name explicitly or reference it from the encryption configuration." The policy owner must accept that, or choose to pass it.

## 4. Tests

The converted policy and its tests follow the structure of the repository's two existing tfpolicy policies. The agent did not copy syntax from elsewhere.

| Case | Input | Expected |
|---|---|---|
| pass | bucket with a matching encryption configuration | pass |
| fail | bucket with no encryption configuration | fail, with the remediation message |
| boundary | encryption configuration targets a different bucket | fail |
| operation-aware | bucket being deleted; bucket with a tag-only update | delete ignored; update evaluated |
| missing data | bucket name unknown at plan time | advisory failure (pending the owner's decision) |
| module | bucket and encryption in the same child module | pass |

The mocks are synthetic plans built for these cases. No plan data was downloaded from HCP Terraform.

## 5. Enforcement map

| Rule | Stage | Enforced by | Can override |
|---|---|---|---|
| `s3-buckets-encrypted` (Sentinel, current) | post-plan | policy set `aws-baseline`, advisory | not applicable: advisory never blocks |
| `s3-buckets-encrypted` (tfpolicy, draft) | post-plan, or CI-only until it is attached | the repository's tfpolicy CI job | not attached to any workspace yet |

Making either policy mandatory, editing `enforcement_level` in `sentinel.hcl`, or replacing the Sentinel policy in the policy set is an enforcement change. The agent asks before any of them.

## Completion report

Outcome: conversion drafted, with two non-equivalences flagged and one behaviour waiting on the owner. tfpolicy tests not run.

### objective

Convert `s3-buckets-encrypted` from Sentinel to tfpolicy, and test the cross-resource behaviour, keeping enforcement advisory.

### scope_and_authorization

| Item | Value |
|---|---|
| Configuration directories | `policies/sentinel`, `policies/tfpolicy` |
| Environment | HCP Terraform organization `example-org`, policy set `aws-baseline` (not accessed) |
| Runners | Sentinel CLI installed locally; tfpolicy runner only in CI |
| Authorization | write the converted policy and tests on branch `policy/s3-encryption-tfpolicy` |
| Not authorized | changing the policy set, its enforcement level or its workspace attachments |

### changed_files

| File | Change |
|---|---|
| `policies/tfpolicy/s3-buckets-encrypted.policy.hcl` | new; converted rule |
| `policies/tfpolicy/s3-buckets-encrypted.policytest.hcl` | new; six cases |
| `policies/tfpolicy/mocks/s3-buckets-encrypted/` | new; synthetic plan mocks |
| `policies/tfpolicy/CONVERSION_NOTES.md` | new; the construct table and the open decision |

### commands_and_results

| Command | Directory | Exit | Result |
|---|---|---|---|
| `sentinel test s3-buckets-encrypted.sentinel` | `policies/sentinel` | 0 | 5 passed (baseline) |

Not run: the tfpolicy tests, because no runner is installed locally and pushing to trigger CI was not authorized. Not checked: whether the draft parses under the runner version CI pins.

### plan_or_state_impact

None. No Terraform plan or state was touched, and the policy set was not modified.

### evidence_classification

| Claim | Class | Evidence |
|---|---|---|
| The original's behaviour on its five cases | local | `sentinel test` |
| Which constructs do not translate | static | reading both policy models against the original |
| The converted policy passes its six cases | unavailable | runner not installed; CI not triggered |
| The draft's syntax is valid for the pinned runner | unavailable | not parsed by any runner |
| The current enforcement is advisory | static | `policies/sentinel/sentinel.hcl` |
| HCP Terraform applies `sentinel.hcl` as committed | inferred | the policy set's VCS connection was not checked in HCP Terraform |

### risks_and_limitations

The value-based match is looser than Sentinel's reference match across modules, and stricter for computed names. Neither difference is visible until real plans run through it. If the owner chooses to pass unknown names, unencrypted buckets with computed names get through without notice.

### next_safe_action

The policy owner decides how unknown bucket names are handled. The requester then pushes the branch, so the repository's tfpolicy CI job parses and runs the six cases. Any change to the `aws-baseline` policy set comes after that, through an approval handoff.
