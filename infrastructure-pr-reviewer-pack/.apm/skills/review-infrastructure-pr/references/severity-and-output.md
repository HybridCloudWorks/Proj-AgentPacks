# Severity and Review Output

## Severity model

Assign severity from demonstrated impact and reach, not from the technology or file type.

### Critical

Use when the change can plausibly cause one or more of:

- Broad compromise of credentials, identities, tenants, accounts, subscriptions, projects, clusters, or production hosts.
- Irrecoverable or widespread data loss.
- Deployment to the wrong high-value target with destructive or privileged effects.
- Unauthenticated public exposure of highly sensitive systems or data.
- A supply-chain path that executes untrusted code with privileged credentials.

Critical findings should normally prevent deployment until fixed and independently verified.

### High

Use when the change can cause:

- Production outage, destructive replacement, material data loss, or loss of management ownership.
- Privilege escalation, broad unauthorized access, secret exposure, or significant network exposure.
- Applying an unreviewed or stale artifact to production.
- A pipeline bypass of required environment, identity, approval, or state controls.
- A non-idempotent or concurrency defect likely to corrupt shared infrastructure or configuration.

### Medium

Use when the change can cause:

- Limited outage, persistent drift, incorrect configuration, failed rollback, or environment-specific failure.
- A security weakness with constrained reach or additional preconditions.
- A version, type, quoting, error-handling, or dependency defect likely to fail a real deployment path.
- Missing evidence for a meaningful but not immediately catastrophic risk.

### Low

Use sparingly for concrete defects with limited impact, such as:

- Misleading operational output that can cause an incorrect response.
- A narrow maintenance or reproducibility defect with a clear execution path.
- A minor but real leak of non-secret internal detail.

Do not use Low for style preferences, optional improvements, or generic hardening advice.

## Confidence

Express confidence when useful:

- **High confidence:** Directly proven by code, tool output, schema, test, plan, or official documented behavior.
- **Medium confidence:** Strongly inferred from code and repository context but missing one confirming artifact.
- **Low confidence:** Do not normally post as a defect. Treat it as a question or evidence gap unless impact is severe and the uncertainty itself blocks safe approval.

## Finding format

Use this structure for each review comment:

```text
[High] Prevent the apply job from using an unreviewed template

The deploy step recompiles `main.bicep` after approval instead of consuming the JSON artifact produced and reviewed in the validation job. A module restore or source change between jobs can therefore make production receive content that was never covered by the what-if result. Publish the compiled template with its commit digest and make the deployment job consume that immutable artifact.

Verify with: pipeline logs showing the same artifact digest in validation and deployment.
```

A finding must contain:

1. **Severity and imperative title** describing the required correction.
2. **Exact defect** at the narrowest changed location.
3. **Trigger or execution path** that makes it fail.
4. **Impact** on security, correctness, state, reliability, availability, recovery, or cost.
5. **Remediation direction** without prescribing an unnecessarily narrow implementation.
6. **Verification evidence** when the fix is not self-evident.

## Evidence-gap format

Use an evidence gap only when the implementation cannot be safely cleared without target-specific proof:

```text
[Medium evidence gap] Provide an existing-environment what-if for the production scope

The PR changes the deployment mode and removes two resources from the Bicep entry point, but the attached build output does not show whether the production deployment will delete or retain the existing objects. Provide a what-if generated from this commit with the production parameter set and deployment scope, and review all deletes before merge.
```

Do not phrase an evidence gap as a confirmed runtime defect.

## Inline comment placement

- Anchor to the changed line that introduced the bad value, condition, command, permission, or missing guard.
- For a deletion, anchor to the nearest changed line in the same logical block and explicitly name the removed control.
- For a cross-file issue, comment on the line where the incompatible contract is introduced and cite the consumer path in the body.
- Avoid comments on unchanged lines unless the review system requires a location and no changed line can represent the issue.

## Consolidation

Post one finding per root cause. Consolidate downstream symptoms when one correction resolves them.

Example: If a pipeline passes the wrong subscription ID to both Bicep and PowerShell, report the target-selection defect once rather than one comment per affected command.

## No-finding conclusion

When no actionable finding meets the threshold, say so without implying absolute safety:

```text
No actionable defects found in the reviewed diff. Residual risk: production behavior still depends on the referenced plan/what-if/check-mode artifacts being generated from this commit with the declared target and inputs.
```

List only material residual risks or evidence gaps. Do not pad the conclusion with generic recommendations or praise.

## Prohibited review output

Do not emit:

- Generic best-practice reminders.
- Praise or narration of what the diff does.
- Vague questions that the code already answers.
- Unsupported provider, module, cmdlet, collection, or service claims.
- Formatter or naming comments with no semantic impact.
- Duplicate findings.
- “Add tests” without the precise behavior and failure condition.
- “This may be insecure” without an execution path and impact.
- Claims that Copilot approval blocks merge.
