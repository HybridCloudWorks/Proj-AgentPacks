---
description: "Review a Cloudflare-related change: Worker code, Wrangler config, Terraform or Pulumi, rules or policies"
agent: cloudflare-subject-matter-expert
argument-hint: "[diff, branch, plan or export]"
---

# Review a Cloudflare change

## Inputs

The exact diff, base and head, plan output or exported configuration, the repository's instructions and the acceptance criteria.

## Workflow

Keep the review read-only. Apply cloudflare-workers-development for Worker code and configuration, cloudflare-iac-and-api-automation for Terraform, Pulumi, API scripts and CI, and the product skill for any rule or policy. Delegate security-relevant parts to `cloudflare-security-reviewer`. Run only local, credential-free checks. Do not post comments, approve or merge.

## Expected output

Prioritized located findings with severity, evidence, impact, recommended change and blocking flag; checks actually run with environment labels; review limits; and a CHANGES_REQUIRED or ANALYSIS_ONLY status under the `cloudflare-subject-matter-expert-contract` instruction.
