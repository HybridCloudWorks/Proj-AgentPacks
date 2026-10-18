# Infrastructure Pull Request Review

When a pull request changes infrastructure-as-code, configuration management, deployment automation, platform manifests, or CI/CD, use the repository Skill at `.github/skills/review-infrastructure-pr/SKILL.md`.

Review changed lines semantically rather than performing a smell test. Trace cross-tool inputs, identities, targets, state or ownership, generated artifacts, deployment order, failure behavior, and existing-environment effects. Apply only the technology Skills present in the change. Report concrete, line-anchored defects or material evidence gaps; do not emit generic best practices, praise, diff narration, or unsupported product behavior.

Treat Copilot review as advisory. Required checks, rulesets, protected environments, CODEOWNERS, and accountable human approval remain authoritative.
