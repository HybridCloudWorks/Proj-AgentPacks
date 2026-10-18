---
description: "Safety rules for scripts and runbooks that call gcloud, bq, gcloud storage, gsutil or kubectl: explicit scope, validated syntax, previews and no hidden mutations."
applyTo: "**/*.sh,**/*.bash,**/*.ps1,**/*.psm1"
---

# Google Cloud command-line script instructions

These rules apply only to scripts that call Google Cloud or Kubernetes command-line tools.

- Validate the exact leaf command and flags with `gcloud help <command>` (or the tool's own help) before writing or running it; command syntax recalled from memory is often wrong.
- Pass `--project`, and `--region`, `--zone` or `--location`, explicitly on every resource command; never rely on the active configuration. Add `--quiet` so the command cannot block on a prompt.
- Reduce output with `--filter`, `--format="json(field,...)"` and `--limit`; never print secret values, access tokens or full IAM policies into logs.
- Keep read-only discovery and mutations in separate, clearly named steps. Mutating steps (create, update, delete, IAM bindings, API enablement, billing, organization policy, KMS, deployments) require Level 2 approval under the `google-cloud-architect-contract` instruction and must use a preview such as `--dry-run`, `--validate-only` or `kubectl diff` when the command supports it.
- Use the gcp-estate-discovery skill to classify a command by approval level before running it; its classifier never executes the command.
