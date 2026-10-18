# Terraform Expert Engineer Pack

Portable Agent/Skill package for Terraform and HCL-based infrastructure engineering. It covers ordinary Terraform configuration and module work plus the high-value products and workflows that surround it: remote state, S3 and Azure Storage backends, HCP Terraform/Enterprise, Terraform Stacks, policy, tests, provider development, CI/CD, and Azure Verified Modules.

## Primary downloads

- terraform-expert-engineer-pack.zip - complete source and generated vendor files.
- terraform-expert-engineer-canonical.zip - APM-friendly canonical source.
- terraform-expert-engineer-prompt.zip - reusable authoring prompt.
- terraform-expert-engineer-validation.zip - uppercase VALIDATION_REPORT.md.

Also generated: vendor packages generated at build time and one individual skill.zip archive per Skill, collected in terraform-expert-engineer-skills.zip.

## Build and validate

    python tooling/build_pack.py
    python tooling/validate_pack.py --write-report

The build is deterministic. Static validation does not prove a live Terraform plan, HCP Terraform run, cloud API call, state lock, policy enforcement, provider acceptance test, AVM certification, or production safety.

## Design boundary

The supplied sources include duplicate agents, duplicate AVM guidance, overlapping Terraform style and testing material, policy author/test agents, Terraform Stacks examples, import/search examples, provider scaffolding, CI references, and cloud-specific Terraform guidance. The pack preserves the distinct capabilities, folds examples into focused procedures, and avoids creating low-value Skills for each individual attachment.
