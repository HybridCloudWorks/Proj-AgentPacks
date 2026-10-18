---
description: "Interpret a captured Terraform plan, Bicep what-if or azd preview against the reviewed change and intended scope"
agent: cloud-prepress-reviewer
---

# Review a captured deployment preview

## Inputs

- The captured preview output, as text or JSON: Terraform plan, Bicep or ARM what-if, or `azd provision --preview`.
- The exact command and flags, the commit it was captured at, and who authorized it.
- The intended environment, tenant, subscription, region, resource group or management group scope, state backend and deployment identity.
- The names (not values) of the parameter and variable files the preview used.
- The diff the preview is meant to represent.

If no preview is supplied, ask whether the operator authorizes a read-only preview at a named scope. Without that authorization, do not run one: record preview evidence as `not-verified`.

## Workflow

1. Apply deployment-preview-and-environment-review to confirm that the preview ran against the intended tenant, subscription, scope, backend and identity at the reviewed commit, and that secrets were passed as references.
2. Apply change-scope-and-impact to map every previewed change back to the diff. A change the diff does not explain is drift or a wrong target until shown otherwise.
3. Apply iac-policy-and-identity-review to every delete, replace, role assignment, policy assignment, exemption, network exposure or lifecycle change in the preview.
4. Apply azure-evidence-and-mcp-review to label the evidence: `preview-verified` covers only what the captured preview shows; `live-read-verified` requires an authorized read-only query; record source and retrieval date for any change-type or API semantics the conclusion depends on.
5. Apply review-report-and-pr-gate to write the report.

Account for state lock risk whenever a plan runs against shared state. Never run apply, deploy, force-unlock, import or any mutation to resolve a preview question.

## Expected output

A pre-press report whose tests, build and preview status gives the create, modify, delete, replace and no-change counts, the commit and scope captured, each unexplained change, policy denials and permission errors. Findings tie each risky previewed change to a file and line. A preview is evidence of the captured preview only; it is not proof of a successful deployment or of live policy compliance.

Follow the `cloud-prepress-reviewer-contract` instruction. Never describe an unexecuted check as passed.
