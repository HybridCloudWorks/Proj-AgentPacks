# github-expert-engineer 1.1.0: artifact catalog

Every file in this pack, with its purpose and location. Contents are in the files themselves.

| ARTIFACT NAME | PURPOSE | LOCATION |
|---|---|---|
| github-expert-engineer.agent.md | Canonical agent: Expert GitHub platform engineer for organization and repository administration, governance, branches, pull requests, reviews, Copilot, Actions, security, releases, APIs, troubleshooting, and evidence-driven automation. | .apm/agents/github-expert-engineer.agent.md |
| github-expert-engineer-contract.instructions.md | Canonical instruction: Approval, handoff and completion-report rules for the github expert engineer pack. Always on; the agents, skills and prompts in this pack refer to it. | .apm/instructions/github-expert-engineer-contract.instructions.md |
| SKILL.md | Canonical skill: Diagnose GitHub Actions workflow discovery, trigger, queue, permission, runner, expression, dependency, artifact, cache, and log failures. | .apm/skills/github-actions-debugging-and-troubleshooting/SKILL.md |
| SKILL.md | Canonical skill: Author and audit GitHub Actions workflows, reusable workflows, composite actions, permissions, action pins, OIDC, expressions, runners, artifacts, caches, and supply-chain controls. | .apm/skills/github-actions-workflows-and-security/SKILL.md |
| SKILL.md | Canonical skill: Use GitHub CLI, REST, GraphQL, GitHub Apps, and MCP safely with narrow scope, pagination, rate-limit awareness, redaction, and mutation gates. | .apm/skills/github-api-cli-and-mcp-operations/SKILL.md |
| SKILL.md | Canonical skill: Design and audit GitHub Apps, fine-grained tokens, OAuth, webhooks, event delivery, permissions, installation scope, and secret-safe integrations. | .apm/skills/github-apps-tokens-and-webhooks/SKILL.md |
| SKILL.md | Canonical skill: Build defensible GitHub audit, incident, compliance, and readiness evidence from local files, API reads, workflow runs, security state, and policy read-backs. | .apm/skills/github-audit-evidence-and-compliance/SKILL.md |
| SKILL.md | Canonical skill: Analyze and design GitHub branch protection, rulesets, required checks, merge queues, bypasses, signed commits, and deployment gates. | .apm/skills/github-branch-protection-and-rulesets/SKILL.md |
| SKILL.md | Canonical skill: Design and review GitHub CI/CD pipelines, environments, approvals, concurrency, deployment protection, release promotion, and rollback boundaries. | .apm/skills/github-ci-cd-and-deployment-environments/SKILL.md |
| SKILL.md | Canonical skill: Configure, use, review, and govern GitHub Copilot code review, cloud agent output, custom agents, instructions, skills, MCP context, and AI-assisted delivery. | .apm/skills/github-copilot-engineering/SKILL.md |
| SKILL.md | Canonical skill: Maintain GitHub documentation, repository instructions, templates, CODEOWNERS, runbooks, and cross-file contracts without duplicating or weakening governance. | .apm/skills/github-documentation-and-repository-contracts/SKILL.md |
| SKILL.md | Canonical skill: Route GitHub platform, administration, Copilot, Actions, review, security, and automation work to the smallest expert Skill with safe evidence boundaries. | .apm/skills/github-expert-orchestration/SKILL.md |
| SKILL.md | Canonical skill: Query, triage, organize, and govern GitHub issues, discussions, labels, milestones, and Projects without confusing collaboration data with instructions. | .apm/skills/github-issues-discussions-and-projects/SKILL.md |
| SKILL.md | Canonical skill: Plan and assess GitHub repository, organization, issue, branch, release, package, Actions, and governance migrations, backup, restore, and disaster recovery. | .apm/skills/github-migrations-backups-and-recovery/SKILL.md |
| SKILL.md | Canonical skill: Administer and assess GitHub enterprises, organizations, teams, repositories, policies, access, billing, and platform settings safely. | .apm/skills/github-platform-administration/SKILL.md |
| SKILL.md | Canonical skill: Review GitHub pull requests, branches, checks, comments, ownership, mergeability, and human or AI review feedback with evidence. | .apm/skills/github-pull-requests-and-code-review/SKILL.md |
| SKILL.md | Canonical skill: Design and audit GitHub releases, tags, packages, artifacts, provenance, retention, immutability, promotion, and rollback workflows. | .apm/skills/github-releases-packages-and-artifacts/SKILL.md |
| SKILL.md | Canonical skill: Design, audit, and improve GitHub repository structure, lifecycle settings, templates, ownership, metadata, and governance contracts. | .apm/skills/github-repository-lifecycle-and-governance/SKILL.md |
| SKILL.md | Canonical skill: Run and design safe pre-review and post-review automation, deterministic inventory, finding validation, mutation guards, and GitHub review handoff tools. | .apm/skills/github-review-automation-and-hooks/SKILL.md |
| SKILL.md | Canonical skill: Audit GitHub security features and software supply-chain controls including CodeQL, secret scanning, Dependabot, advisories, dependency review, attestations, and action trust. | .apm/skills/github-security-and-supply-chain/SKILL.md |
| apm.yml | APM manifest: name, version, targets. | apm.yml |
| capability-map.yml | Vendor compatibility metadata | compatibility/capability-map.yml |
| compatibility-matrix.yml | Vendor compatibility metadata | compatibility/compatibility-matrix.yml |
| optional-skills.yml | Vendor compatibility metadata | compatibility/optional-skills.yml |
| tool-permissions.yml | Vendor compatibility metadata | compatibility/tool-permissions.yml |
| vendor-sources.yml | Vendor compatibility metadata | compatibility/vendor-sources.yml |
| DESCRIPTION.md | What the pack is for and who uses it. | DESCRIPTION.md |
| DESIGN_DECISIONS.md | Pack contract or inventory | docs/DESIGN_DECISIONS.md |
| SOURCE_TRACEABILITY.md | Pack contract or inventory | docs/SOURCE_TRACEABILITY.md |
| post-github-review.ps1 | Hook helper script | hooks/post-github-review.ps1 |
| post-github-review.sh | Hook helper script | hooks/post-github-review.sh |
| pre-github-review.ps1 | Hook helper script | hooks/pre-github-review.ps1 |
| pre-github-review.sh | Hook helper script | hooks/pre-github-review.sh |
| README.md | Hook helper script | hooks/README.md |
| LICENSE | License terms. | LICENSE |
| PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md | The master prompt this pack was built to. | PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md |
| README.md | How to install and use the pack. | README.md |
| capability-coverage.yml | Local test or recorded evidence | tests/capability-coverage.yml |
| REVIEW.md | Local test or recorded evidence | tests/fixtures/REVIEW.md |
| valid-review.md | Local test or recorded evidence | tests/fixtures/valid-review.md |
| report-contract.yml | Local test or recorded evidence | tests/report-contract.yml |
| skill-coverage.yml | Local test or recorded evidence | tests/skill-coverage.yml |
| trigger-cases.yml | Local test or recorded evidence | tests/trigger-cases.yml |
| github_inventory.py | Pack-specific helper code | tooling/github_inventory.py |
| query_guard.py | Pack-specific helper code | tooling/query_guard.py |
| validate_github_review.py | Pack-specific helper code | tooling/validate_github_review.py |
| query-discussions.py | Pack file | tools/query-discussions.py |
| query-discussions.sh | Pack file | tools/query-discussions.sh |
| query-issues.sh | Pack file | tools/query-issues.sh |
| query-labels.sh | Pack file | tools/query-labels.sh |
| query-prs.sh | Pack file | tools/query-prs.sh |
| query-workflows.sh | Pack file | tools/query-workflows.sh |
| VALIDATION_REPORT.md | Executed checks and what remains unverified. | VALIDATION_REPORT.md |

## Build outputs (dist/, not committed)

- copilot-github-expert-engineer.zip: 20 files generated by `apm install --target copilot`
- claude-github-expert-engineer.zip: 20 files generated by `apm install --target claude`
- codex-github-expert-engineer.zip: 19 files generated by `apm install --target codex`
- kiro-github-expert-engineer.zip: 20 files generated by `apm install --target kiro`
- gemini-github-expert-engineer.zip: 18 files generated by `apm install --target gemini`
- agent-skills-github-expert-engineer.zip: 18 files generated by `apm install --target agent-skills`
- github-expert-engineer-canonical.zip, github-expert-engineer-prompt.zip, github-expert-engineer-validation.zip, github-expert-engineer-skills.zip, github-expert-engineer-full-pack.zip, SHA256SUMS.txt
