# Technology adapter return

What each technology Skill hands back to `review-infrastructure-pr`. The six adapters (`review-terraform-opentofu`, `review-bicep-arm`, `review-powershell-automation`, `review-ansible-automation`, `review-cicd-deployment`, `review-kubernetes-packaging`) share one Output Contract: findings and evidence gaps with an anchor, trigger, affected target, impact, remediation and verification evidence. They do not repeat the universal gates and do not write a final report.

The orchestration Skill merges returns by root cause, so two adapters that see one defect from both sides produce one finding.

## Header

- Adapter: <Skill name>
- Files and lines covered: <paths and ranges from the coverage ledger>
- Entry points and execution context established: <root module, targetScope, playbook, workflow, chart, script host>
- Decisive semantics verified against: <installed schema, command help, official source from the Skill's references/official-sources.md>
- Stop condition reached: <none, or which one and why>

## Candidate findings

```text
Anchor: <path>:<line>
Trigger: <inputs or event that makes it fail>
Affected target: <environment, scope, host, namespace, state key>
Defect: <what is wrong>
Impact: <what happens>
Remediation: <direction>
Verification: <artifact or check>
Proposed severity and confidence: <for the orchestrator to confirm>
Possible duplicate of: <another adapter's anchor, if the root cause is shared>
```

## Candidate evidence gaps

```text
Risk: <what cannot be cleared>
Artifact needed: <exact artifact, commit, inputs, target, identity>
```

## Verified without finding

Lines or behaviors the adapter checked and cleared, with the evidence that cleared them. These become "verified" rows in the coverage ledger.
