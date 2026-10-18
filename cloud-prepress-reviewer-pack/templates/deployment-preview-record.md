# Deployment preview record: <change title>

The record deployment-preview-and-environment-review keeps for each Terraform plan, Bicep or ARM what-if, or `azd provision --preview` the review relies on. One record per preview. Its counts and conclusions feed the report's tests, build and preview status section.

## Target and authorization

| Item | Value |
|---|---|
| Tool and command | `<exact command and flags>` |
| Who ran it | <operator, CI job and run ID, or the reviewer> |
| Authorized by | <person, where they said so, and the scope they authorized; or "captured by CI, no reviewer access"> |
| Commit | `<commit>`; matches reviewed head: <yes or no> |
| Environment | <environment name> |
| Tenant and subscription | <placeholder or alias; never a secret> |
| Region | <region> |
| Deployment scope | <resource group, subscription, management group or tenant> |
| State backend | <backend and key, for Terraform; "not applicable" otherwise> |
| Deployment identity | <identity name and its role at that scope, with evidence label> |
| Parameter and variable files | <file names only; values are not recorded> |
| Secrets passed as references | <yes, or the finding raised> |

## Change counts

| Create | Modify | Delete | Replace | No change | Ignored or unsupported |
|---|---|---|---|---|---|
| <n> | <n> | <n> | <n> | <n> | <n> |

## Changes that need attention

| Resource or address | Change type | Explained by the diff | Concern |
|---|---|---|---|
| <address or resource ID alias> | <create, modify, delete, replace, move> | <file and line, or "no"> | <replacement of stateful resource, unexplained drift, exposure, role or policy change, known preview noise> |

## Errors and limits

- Policy denials: <none, or the policy, assignment scope and effect>
- Permission errors: <none, or the missing action and scope>
- State lock: <not applicable, acquired and released, or lock risk observed>
- Preview limits: <for example, values unknown until apply, nested deployments the preview could not expand, resources outside the preview's scope>

## Gates after the preview

| Gate | Owner | Status |
|---|---|---|
| <deployment approval, change window, post-deployment verification> | <owner> | <pending or recorded> |

## Hard stops

This record never authorizes `terraform apply`, `azd up`, `azd deploy`, `azd down`, ARM create, update or delete, force-unlock, import, or any resource, RBAC, policy or secret change. A preview is evidence of the captured preview, not proof of a successful deployment.
