# Cloud Pre-Press Reviewer Pack

Portable Agent/Skill package for the review boundary between implementation/build completion and pull-request or deployment approval. It consolidates the supplied code reviewer, architecture reviewer, security engineer, allocation/policy, onboarding, validation, role-verification, plan-review, error, and repository-contract references into a thin reviewer Agent with focused Skills.

## Primary downloads

- `dist/cloud-prepress-reviewer-pack.zip` — complete source, vendor targets, hooks, tools, tests, and archives.
- `dist/cloud-prepress-reviewer-canonical.zip` — APM-friendly canonical Agent and Skills.
- `dist/cloud-prepress-reviewer-prompt.zip` — reusable pack-authoring prompt.
- `dist/cloud-prepress-reviewer-validation.zip` — uppercase `VALIDATION_REPORT.md`.

The distribution also includes vendor packages generated at build time and one validated `skill.zip` archive for every Skill, collected in `cloud-prepress-reviewer-skills.zip`.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
```

Use `hooks/pre-review.*` before analysis and `hooks/post-review.*` after the report is written. The hooks and tools are non-mutating. They do not prove a live Azure deployment, policy compliance, plan/apply result, cost estimate, recovery result, or PR approval.

## Review boundary

This pack reviews the built result. It does not implement fixes, replace architecture design, run deployment commands, or merge/publish a PR. It returns a recommendation and a handoff that another authorized actor can act on.

## Official evidence

Prefer current Microsoft Learn, Azure Policy, Bicep/ARM, Azure Developer CLI, Terraform/AVM, and official Azure MCP evidence. Use current documentation for version-sensitive behavior, API versions, policy effects, limits, provider/module requirements, and preview semantics. Record sources and retrieval dates when claims materially affect the gate.
