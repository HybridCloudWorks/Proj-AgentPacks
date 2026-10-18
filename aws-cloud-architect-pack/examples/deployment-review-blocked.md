# Worked example: blocked production change (deploy, SCP edit and stack deletion)

Workflow: `review-deployment-plan.prompt.md`. Skills applied: `aws-iac-deployment-and-lifecycle`, `aws-security-identity-and-compliance`, `aws-resilience-dr-and-migration`, `aws-operations-observability-and-troubleshooting`, `aws-caf-landing-zones-and-governance`, `aws-docs-mcp-and-evidence`.

This example shows a **blocked** outcome. The names are fictional.

## Request

> Our CDK refactor is ready. Deploy `OrdersStack-prod` now, update the Prod OU SCP so ap-southeast-2 is allowed, and delete the old `OrdersLegacy-prod` stack. Just do it, we're late.

## What was supplied

| Evidence | Label |
|---|---|
| `cdk diff OrdersStack-prod` output, pasted by the user | observed (as supplied; not re-run) |
| The SCP JSON before and after, from the user's pull request | observed |
| `aws cloudformation describe-stacks` and `list-imports` output for `OrdersLegacy-prod`, pasted by the user | observed (as supplied) |
| Deployment identity or pipeline run in this session | none |

The message gives no target account ID, no rollback plan and no approver. "Just do it" is urgency, not scoped authorization. The request also contains three separate mutations, and each needs its own approval.

## Review

`aws-iac-deployment-and-lifecycle` classified every change in the diff. Other skills added their findings.

### Finding 1: critical, production database would be destroyed and recreated

The diff shows:

```text
[-] AWS::RDS::DBCluster OrdersDbCluster1A2B3C4D destroy
[+] AWS::RDS::DBCluster DataOrdersDbCluster9F8E7D6C
[-] AWS::RDS::DBInstance OrdersDbClusterWriter5E6F7A8B destroy
[+] AWS::RDS::DBInstance DataOrdersDbClusterWriterC1D2E3F4
```

The refactor moved the cluster construct inside a new `Data` construct. That changed its construct path, and therefore its logical ID. CloudFormation will create a new, empty cluster and remove the existing one. The construct uses the CDK default removal policy for database clusters, so a final snapshot would be taken, but the application would switch to an empty database. Every order written between the snapshot and a manual restore would be at risk.

`aws-resilience-dr-and-migration` adds two points. No pre-change snapshot has been confirmed. Restoring from the final snapshot is not a rollback either, because it creates a new cluster endpoint and needs an application configuration change.

**Required fix.** Keep the original logical IDs by overriding them on the underlying `CfnDBCluster` and `CfnDBInstance` resources, or move the construct back to its original path. Then re-run `cdk diff` and confirm it shows no destroy or add for any `AWS::RDS::*` resource.

### Finding 2: high, database security group widened

`aws-security-identity-and-compliance` found this in the diff: ingress on port 5432 changes from the application security group to the CIDR `10.0.0.0/8`. That range includes every on-premises and hub-connected network.

**Required fix.** Restore the security-group reference.

### Finding 3: high, the SCP edit targets a Control Tower-managed policy and widens data residency

The policy being edited is named `aws-guardrails-RgnDeny7`. That prefix is the one Control Tower uses for its managed SCPs (name observed; Control Tower ownership inferred).

`aws-caf-landing-zones-and-governance` explains the problem. Editing a managed SCP directly creates landing-zone drift. The Region change belongs in the Control Tower landing-zone Region settings, made by the platform team. Separately, ap-southeast-2 adds a new data-residency jurisdiction, which needs the data-protection owner's sign-off. There is no evidence the change was tested on the Policy-Staging OU.

### Finding 4: high, deleting the legacy stack would fail, and parts of it are unresolved

From the supplied output:

- Termination protection is enabled on `OrdersLegacy-prod`.
- Its export `OrdersLegacy-QueueArn` is imported by `BillingStack-prod`. CloudFormation will not delete a stack whose exports are still imported, so the delete would fail even with termination protection off.
- The S3 bucket `orders-legacy-exports` has a Retain deletion policy. It would survive the delete with no owning stack, no lifecycle management and no clear owner.

**Required fix.** Migrate `BillingStack-prod` off the import. Assign an owner and a lifecycle policy to the bucket. Only then disable termination protection, as a separately approved change.

### Rollout readiness

`aws-operations-observability-and-troubleshooting`: the pipeline has no stabilization alarm set and no rollback trigger for `OrdersStack-prod`.

`aws-docs-mcp-and-evidence` was not needed. Every finding rests on supplied output and documented CloudFormation behavior, and the CDK version did not affect any of them.

## Response to the user

The architect did not deploy, edit the SCP or delete anything. The session had no deployment identity, and even with one, the request lacked a target, an approver and a rollback plan. The user received the four findings, the fixes, and the three separate approvals still needed:

1. **Deploy `OrdersStack-prod`.** After Findings 1 and 2 are fixed and a re-run diff shows no RDS destroy, approved by the service owner with a confirmed pre-change snapshot.
2. **Add ap-southeast-2.** Through Control Tower Region settings, approved by the platform lead and the data-protection owner after a Policy-Staging test.
3. **Delete `OrdersLegacy-prod`.** After the import is removed and the bucket has an owner, approved by the service owner.

## Completion report

Pack: aws-cloud-architect. Date: 2026-10-18.

Outcome: **blocked.** No change was made. Deploying as diffed would destroy and recreate the production database cluster, and the SCP and deletion requests lack authority and prerequisites.

### scope_and_inputs

Review of `OrdersStack-prod` (CDK), a Prod OU SCP change, and deletion of `OrdersLegacy-prod`. Inputs were the user-supplied diff, the SCP JSON and the stack output (observed as supplied). There was no deployment identity and no explicit, scoped authorization for any mutation.

### business_outcomes_and_requirements

- Ship the refactored orders stack without losing data.
- Enable ap-southeast-2.
- Retire the legacy stack.
- The user's deadline is noted. It does not change the approval requirements.

### source_facts_and_evidence

- RDS destroy-and-add entries in the diff: observed.
- Security-group CIDR change: observed.
- SCP name and diff: observed. Control Tower management of the policy: inferred from the name prefix.
- Termination protection, the export import and the bucket Retain policy: observed.
- Nothing was re-run in an account (not-verified for the current live state).

### framework_alignment

- Reliability and Operational Excellence: the stateful-resource protection gate and the stabilization alarm are both missing.
- Security: network widening, and a governance-control change made outside its owner's process.
- Cost: an orphaned bucket with no lifecycle policy.

### proposed_architecture

Not applicable. The architecture is unchanged. The review proposes no new design, only the fixes listed in Findings 1 to 4.

### assumptions_and_tradeoffs

- The pasted diff matches the commit the pipeline would deploy. That assumption must be confirmed by re-running the diff from the pipeline.
- The user's urgency does not justify accepting data-loss risk.

### implementation_and_operating_implications

- Override the logical IDs or restore the construct path.
- Restore the security-group reference.
- Re-run the diff.
- Take a confirmed snapshot.
- Add a stabilization alarm and a rollback trigger to the pipeline.
- Move the Region change to Control Tower settings.
- Sequence the legacy-stack retirement after the import is removed.

### security_resilience_cost_and_sustainability

- Security: Finding 2 widens database access, and Finding 3 changes a governance control outside its owner's process.
- Resilience: Finding 1 is a production data-loss risk.
- Cost and sustainability: the retained bucket would accrue storage with no owner.

### output_files

| File | Purpose | Check run | Label |
|---|---|---|---|
| None written | The user asked for actions, not files. The findings were returned inline | n/a | n/a |

No REQ, TOPOLOGY, CONSTRAINTS or ADR was produced, because no design decision changed. If the team keeps the new construct structure, an ADR for logical-ID stability is recommended.

### live_or_external_checks

- `cdk diff` re-run, Change Set creation, snapshot confirmation and SCP simulation in Policy-Staging: none executed (not-verified).

### unresolved_risks

- Production database replacement until Finding 1 is fixed (owner: service owner).
- Database security group widening (owner: service owner).
- Control Tower drift and residency risk from the SCP edit (owners: platform lead, data-protection owner).
- Legacy stack dependencies (owner: billing team).

### next_safe_action

The service owner fixes Findings 1 and 2 and re-runs `cdk diff` from the pipeline. The architect then reviews the new diff. Nothing is deployed until a diff without RDS destroy entries and a confirmed snapshot are presented to the approver.
