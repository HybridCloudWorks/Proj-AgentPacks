---
description: "Diagnose an Azure deployment, access, network or runtime failure from evidence, separating confirmed cause from hypothesis"
agent: azure-cloud-architect
---

# Troubleshoot an Azure issue

## Inputs

The exact error text, deployment name or correlation ID, affected scope and resources, a timeline, recent changes, pipeline or application logs, what has already been tried, and which read-only queries the user authorizes at which scope.

## Workflow

1. Apply `azure-operations-observability-and-troubleshooting`: locate the failing boundary (bootstrap, authentication, validation, plan, deployment, data plane or post-deployment) from the evidence: error text, deployment operations, Activity Log, resource state, metrics, traces, policy evaluation, network path, identity and role, quota and recent changes. List hypotheses and mark each confirmed, rejected or open with its evidence. Check for partial changes, state locks, orphaned resources, policy effects and regional incidents.
2. Apply `azure-deployment-and-lifecycle` for deployment operations, what-if or plan differences, state locks and rollback impact.
3. Apply `azure-security-identity-and-compliance` when the evidence points at a role, token, federation subject or policy.
4. Apply `azure-networking-hybrid-and-edge` when it points at routing, DNS, private endpoints or inspection.
5. Apply `azure-docs-mcp-and-evidence` to error codes, known limits and service health, and `azure-architecture-handoff-and-adr` when the fix changes a constraint or decision.

Run only read-only queries within the authorized scope. Do not rerun a mutating command, redeploy, delete, repair, force-unlock or start a remediation task. Give the operator the commands instead.

## Expected output

- The confirmed cause, or the leading hypotheses with the evidence still needed.
- The partial-change and impact assessment.
- A proposed fix with the approvals it needs, the operator commands, and a verification step.
- Prevention: the constraint, check, alert or runbook that would have caught it.
- A completion report.

Follow the `azure-cloud-architect-contract` instruction: report every contract section, label evidence, and state what was not verified. Existing authorization applies only within its stated scope.
