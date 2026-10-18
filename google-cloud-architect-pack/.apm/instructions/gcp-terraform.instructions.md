---
description: "Guardrails for Google Cloud Terraform and OpenTofu: identity, exposure, encryption, labels, deletion protection, provider pinning and plan-only validation."
applyTo: "**/*.tf,**/*.tfvars,**/*.tf.json,**/*.tftest.hcl"
---

# Google Cloud Terraform instructions

When a change touches Google Cloud infrastructure code, apply gcp-iac-validation and the skill for the affected domain (gcp-network-design, gcp-identity-access, gcp-security-controls, gcp-gke-platform, gcp-serverless-apps).

- Identity: attach user-managed service accounts with the narrowest predefined role on the narrowest resource. Do not create `google_service_account_key` resources or commit key files; use Workload Identity Federation, attached service accounts or impersonation. Prefer `_member` or `_binding` resources over authoritative `_policy` resources unless the module owns the whole policy, and say which.
- Exposure: no `allUsers` or `allAuthenticatedUsers` bindings, public IPs on databases or VMs, `0.0.0.0/0` ingress firewall rules or unrestricted Cloud Run ingress unless a requirement names it; route public traffic through a load balancer with Cloud Armor.
- Data: keep `deletion_protection = true` on stateful resources, state CMEK requirements explicitly, and set backup and point-in-time recovery where the data has an RPO.
- Hygiene: pin provider and module versions, label every resource with environment, application, owner and cost centre, use typed and described variables, and keep secrets out of variables, state outputs and plan logs.
- Validation: run `terraform fmt -check` and `terraform validate`; run `terraform plan` only against a target the user named with the identity the user provided. Never run `apply`, `destroy`, `import`, `state rm`, `state mv` or `force-unlock` without Level 2 approval under the `google-cloud-architect-contract` instruction. A clean plan is not proof that IAM, quotas or organization policies will allow the apply.
