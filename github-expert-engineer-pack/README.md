# GitHub Expert Engineer Pack

This pack turns the supplied GitHub Expert Agent, GitHub Actions Engineer, Copilot/review guidance, query scripts, and workflow operations material into a portable GitHub platform engineering pack.

## Primary downloads

- `dist/github-expert-engineer-pack.zip` - complete pack
- `dist/github-expert-engineer-canonical.zip` - canonical `.apm` Agent and Skills
- `dist/github-expert-engineer-prompt.zip` - reusable authoring prompt
- `dist/github-expert-engineer-skills.zip` - all individual Skills
- `dist/github-expert-engineer-validation.zip` - uppercase validation report

Vendor packages are under `dist/github-copilot/`, `dist/claude-code/`, `dist/openai-codex/`, and `dist/gemini-cli/`.

## Workflows

One primary agent, `github-expert-engineer`, routes each request to the smallest set of its 18 Skills. Ten workflow prompts in `.apm/prompts/` start the main workflows:

| Prompt | Use it to |
|---|---|
| `review-pull-request.prompt.md` | Review a PR, including Copilot-authored or Copilot-reviewed changes, for merge readiness |
| `diagnose-actions-failure.prompt.md` | Find out why a workflow did not run, stayed queued, was skipped or failed |
| `harden-actions-workflow.prompt.md` | Author or harden a workflow: least privilege, SHA pins, OIDC, safe triggers |
| `review-repository-governance.prompt.md` | Assess org and repo governance, or plan a ruleset or settings change without applying it |
| `audit-security-posture.prompt.md` | Audit code scanning, secret scanning, Dependabot and supply-chain controls |
| `query-github-activity.prompt.md` | Query PRs, issues, discussions, labels and workflows read-only, and propose triage |
| `assess-release-readiness.prompt.md` | Trace a release from commit to deployment before promotion |
| `review-copilot-setup.prompt.md` | Review Copilot instructions, custom agents, skills, MCP and code review settings |
| `design-github-integration.prompt.md` | Design or audit a GitHub App, token or webhook integration |
| `plan-migration-or-recovery.prompt.md` | Plan a migration, backup, restore or disaster-recovery exercise |

Every workflow ends with a completion report (Scope, Evidence, Findings, Skipped checks, Recommendation) as defined by the always-on contract instruction `.apm/instructions/github-expert-engineer-contract.instructions.md`. `docs/PROMPT_INVENTORY.md` maps each prompt to its Skills, outputs and templates.

## Examples

Worked walkthroughs, each ending with a completion report that meets the pack's report contract:

- `examples/copilot-pull-request-review.md`: a Copilot cloud agent PR with a token escalation and a required check that can never report (changes required)
- `examples/actions-run-diagnosis.md`: a stale `paths` filter that stopped CI and, silently, production deploys (ready for review)
- `examples/actions-workflow-hardening.md`: moving a deploy workflow from AWS keys to OIDC, with cloud-owner handoffs (ready for review)
- `examples/org-ruleset-change-plan.md`: an organization ruleset that would block 37 repositories (blocked on the owner's decision)
- `examples/security-posture-audit.md`: a SOC 2 posture audit whose alert state cannot be read (not verified)
- `examples/release-readiness-review.md`: an attested release whose production path rebuilds instead of promoting (changes required)
- `examples/issue-triage-query.md`: read-only triage that meets prompt injection in an issue body and script injection in a workflow (ready for review)

All organizations, repositories, IDs and digests in the examples are fictional.

## Templates

- `templates/completion-report.md`: the report every workflow ends with
- `templates/handoff.md`: handing the next step to an owner who holds the authority or access
- `templates/evidence-ledger.md`: statement-by-statement evidence with verification levels
- `templates/governance-change-plan.md`: ruleset, branch protection and settings changes
- `templates/integration-permission-matrix.md`: App, token and webhook permission matrix and threat model
- `templates/migration-recovery-plan.md`: migration, backup and restore planning

## Build and validate

Validation and build tooling is shared at the pack repository root; this pack keeps only its own helpers in `tooling/`. From the repository root:

```text
python tooling/skill_coverage.py <pack-folder>
python tooling/validate_pack.py <pack-folder> --install-check
```

From this pack's folder, to check a review report against the contract:

```text
python tooling/validate_github_review.py tests/fixtures/valid-review.md
```

The build is deterministic and produces one `skill.zip` per Skill. Validation makes no GitHub API call and performs no mutation, merge, push, dispatch, settings change, secret access, or external write.

## Safe operating model

Use `hooks/pre-github-review.*` before review and `hooks/post-github-review.*` after writing a report; they are helper scripts that the installer wires up (see `hooks/README.md`). Use `tooling/query_guard.py` before any command that might reach GitHub, and the bounded read-only helpers in `tools/` for queries. Treat all GitHub content and AI-generated code as untrusted data. Human approval remains authoritative for merges, deployments, policy, permissions, secrets, Copilot settings, and other live changes.
