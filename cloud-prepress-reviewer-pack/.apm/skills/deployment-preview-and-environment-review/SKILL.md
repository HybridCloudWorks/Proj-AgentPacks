---
name: deployment-preview-and-environment-review
description: Reviews deployment readiness, environment configuration, authentication, Bicep what-if, Terraform plan, AZD previews, and mutation gates without executing deployment actions.
---

# Deployment Preview and Environment Review

Verify the intended environment, tenant/subscription, region, resource-group or management-group scope, provider, variables, parameter files, backend, deployment identity, and required tools. Check that the preview targets the intended scope and that secrets are references, not values.

Use local validation, `az bicep build`, `terraform fmt/validate`, policy-as-code, tests, `azd provision --preview`, Bicep `validate`/`what-if`, or Terraform `plan` only when the operator explicitly authorizes the needed read-only access. A what-if or plan is evidence of the captured preview, not proof of successful deployment.

Hard-stop on `azd up`, `azd deploy`, `azd down`, `terraform apply`, ARM create/update/delete, force-unlock, import, or resource mutation. Review create/modify/delete/replace counts, unexplained drift, state lock risk, policy denials, missing permissions, and post-preview acceptance gates.
