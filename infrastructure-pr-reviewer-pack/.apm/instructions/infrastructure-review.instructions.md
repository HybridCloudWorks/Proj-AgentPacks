---
description: Apply evidence-driven infrastructure and automation pull-request review rules to relevant files.
applyTo: "**/*.tf,**/*.tfvars,**/*.tftest.hcl,**/.terraform.lock.hcl,**/*.bicep,**/*.bicepparam,**/azuredeploy*.json,**/*.ps1,**/*.psm1,**/*.psd1,**/ansible/**/*.yml,**/ansible/**/*.yaml,**/playbooks/**/*.yml,**/playbooks/**/*.yaml,**/roles/**/*.yml,**/roles/**/*.yaml,.github/workflows/**/*.yml,.github/workflows/**/*.yaml,**/azure-pipelines*.yml,**/azure-pipelines*.yaml,**/pipelines/**/*.yml,**/pipelines/**/*.yaml,**/*.sh,**/*.bash,**/Chart.yaml,**/values*.yaml,**/kustomization.yaml,**/kustomization.yml"
---

# Infrastructure and Automation PR Review

- Use the repository skill at `.github/skills/review-infrastructure-pr/SKILL.md` for pull-request review.
- Review every changed line internally; comment only on concrete, actionable defects or material evidence gaps.
- Detect the technologies present and apply only the relevant adapters. Do not force Terraform conventions onto Bicep, PowerShell, Ansible, pipelines, or Kubernetes.
- Reconstruct the full execution chain across templates, scripts, inventories, workflows, artifacts, identities, and targets.
- Verify target selection, idempotency, ownership, lifecycle, security, failure propagation, retry, rollback, concurrency, and artifact integrity.
- Review existing-environment behavior, not only clean deployment.
- Treat passing syntax, lint, compilation, plan, what-if, or check-mode output as evidence rather than proof.
- Anchor each finding to the narrowest changed line and explain the trigger, impact, remediation direction, and verification evidence.
- Do not emit style-only comments, generic best practices, praise, diff narration, or speculative product behavior.
