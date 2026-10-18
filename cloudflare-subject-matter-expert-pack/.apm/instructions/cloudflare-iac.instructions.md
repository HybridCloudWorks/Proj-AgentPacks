---
description: "Rules for Terraform and Pulumi code that configures Cloudflare: provider pinning, resource naming, state imports, ruleset ownership, drift and token scope."
applyTo: "**/*.tf,**/*.tfvars,**/Pulumi*.yaml"
---

# Cloudflare infrastructure as code

These rules apply only where the file configures the `cloudflare/cloudflare` provider or a Pulumi Cloudflare package; ignore them otherwise.

- Respect the pinned provider version and lock file. Look up resource and attribute names in the documentation for that exact version; major versions renamed resources and changed attribute shapes, and a rename needs a state move or `moved` block, not a destroy and create.
- A single ruleset per zone and phase owns its whole rule list. Know whether Terraform, another tool or the dashboard owns each ruleset before changing it; mixed ownership causes rules to be overwritten.
- Existing objects are imported before they are managed. Never let a plan create a duplicate DNS record, zone setting or Access application that already exists.
- Never put API tokens, tunnel secrets or service-token secrets in `.tf`, `.tfvars` or state outputs; mark sensitive variables and source them from the environment or a secret manager. Scope the deploying token to the accounts, zones and permission groups the code manages.
- Review `terraform plan` or `pulumi preview` output for deletions, replacements and in-place changes to security, DNS and Zero Trust resources before any apply. Apply, import and destroy are Level 2 actions under the contract.
- Use the cloudflare-iac-and-api-automation skill for the full procedure, drift handling and ruleset guard.
