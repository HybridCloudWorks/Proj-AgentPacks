# Prompt inventory

Ten prompts in `.apm/prompts/`, one per primary workflow of the `github-expert-engineer` agent. Each prompt states its inputs, the workflow and the Skills it applies, and the expected output, and each ends by following the always-on `github-expert-engineer-contract` instruction. Prompts are installed content, so they name only Skills and the contract instruction. They never point at `docs/`, `tests/`, `templates/`, `hooks/` or `tools/` paths. Helper scripts are mentioned only by function ("when the installer has made them available").

Every prompt starts with `github-expert-orchestration`, so that Skill is left out of the Skills column below.

| Prompt | Workflow | Skills applied | Expected output | Worked example |
|---|---|---|---|---|
| review-pull-request.prompt.md | Review a PR, including Copilot-authored or Copilot-reviewed changes | github-pull-requests-and-code-review, github-branch-protection-and-rulesets, github-copilot-engineering, github-review-automation-and-hooks | Review report with located findings, AI suggestions kept separate, gates checked on the current head SHA | `examples/copilot-pull-request-review.md` |
| diagnose-actions-failure.prompt.md | Diagnose a workflow that did not run, stayed queued, was skipped or failed | github-actions-debugging-and-troubleshooting, github-api-cli-and-mcp-operations, github-actions-workflows-and-security | Failure class, commands with redacted log lines, confirmed cause or ranked hypotheses, local remediation | `examples/actions-run-diagnosis.md` |
| harden-actions-workflow.prompt.md | Author or harden a workflow: permissions, pins, OIDC, triggers | github-actions-workflows-and-security, github-ci-cd-and-deployment-environments, github-security-and-supply-chain | Local workflow diff, findings, validation actually run, handoff for cloud trust and secret removal | `examples/actions-workflow-hardening.md` |
| review-repository-governance.prompt.md | Assess org and repo governance, or plan a ruleset or settings change | github-platform-administration, github-repository-lifecycle-and-governance, github-documentation-and-repository-contracts, github-branch-protection-and-rulesets | Assessment report; for a change, the before-state, policy diff, impact matrix, rollout, rollback and read-back, blocked on the owner | `examples/org-ruleset-change-plan.md` |
| audit-security-posture.prompt.md | Audit security features and supply-chain controls | github-security-and-supply-chain, github-actions-workflows-and-security, github-audit-evidence-and-compliance | Controls labeled by verification level, ranked findings, next evidence request | `examples/security-posture-audit.md` |
| query-github-activity.prompt.md | Query PRs, issues, discussions, labels, Projects and workflows read-only | github-api-cli-and-mcp-operations, github-issues-discussions-and-projects | Schema-first results, triage proposal for a maintainer, injection checks on automations that read issue text | `examples/issue-triage-query.md` |
| assess-release-readiness.prompt.md | Trace a release from commit to deployment | github-releases-packages-and-artifacts, github-ci-cd-and-deployment-environments, github-audit-evidence-and-compliance | Provenance chain, environment protection state, findings, rollback target | `examples/release-readiness-review.md` |
| review-copilot-setup.prompt.md | Review Copilot instructions, agents, skills, MCP and review settings | github-copilot-engineering, github-documentation-and-repository-contracts, github-api-cli-and-mcp-operations | Per-surface configuration evidence, findings, unreadable settings, optional local edits | none |
| design-github-integration.prompt.md | Design or audit a GitHub App, token, OAuth or webhook integration | github-apps-tokens-and-webhooks, github-api-cli-and-mcp-operations | Permission matrix, threat model, rollback and verification plan | none |
| plan-migration-or-recovery.prompt.md | Plan a migration, backup, restore or DR exercise | github-migrations-backups-and-recovery, github-branch-protection-and-rulesets, github-security-and-supply-chain, github-audit-evidence-and-compliance | Scope inventory, phase plan, lossy-conversion register, restore test, post-migration checks | none |

## Templates the workflows produce

| Template | Produced by |
|---|---|
| `templates/completion-report.md` | Every prompt |
| `templates/handoff.md` | Any prompt whose next step belongs to another owner, most often harden-actions-workflow, review-repository-governance and audit-security-posture |
| `templates/evidence-ledger.md` | audit-security-posture, assess-release-readiness, plan-migration-or-recovery |
| `templates/governance-change-plan.md` | review-repository-governance |
| `templates/integration-permission-matrix.md` | design-github-integration |
| `templates/migration-recovery-plan.md` | plan-migration-or-recovery |

## Skill coverage

Every Skill is applied by at least one prompt.

| Skill | Prompts |
|---|---|
| github-expert-orchestration | all ten |
| github-pull-requests-and-code-review | review-pull-request |
| github-branch-protection-and-rulesets | review-pull-request, review-repository-governance, plan-migration-or-recovery |
| github-copilot-engineering | review-pull-request, review-copilot-setup |
| github-review-automation-and-hooks | review-pull-request |
| github-actions-debugging-and-troubleshooting | diagnose-actions-failure |
| github-actions-workflows-and-security | diagnose-actions-failure, harden-actions-workflow, audit-security-posture |
| github-api-cli-and-mcp-operations | diagnose-actions-failure, query-github-activity, review-copilot-setup, design-github-integration |
| github-ci-cd-and-deployment-environments | harden-actions-workflow, assess-release-readiness |
| github-security-and-supply-chain | harden-actions-workflow, audit-security-posture, plan-migration-or-recovery |
| github-platform-administration | review-repository-governance |
| github-repository-lifecycle-and-governance | review-repository-governance |
| github-documentation-and-repository-contracts | review-repository-governance, review-copilot-setup |
| github-audit-evidence-and-compliance | audit-security-posture, assess-release-readiness, plan-migration-or-recovery |
| github-issues-discussions-and-projects | query-github-activity |
| github-releases-packages-and-artifacts | assess-release-readiness |
| github-apps-tokens-and-webhooks | design-github-integration |
| github-migrations-backups-and-recovery | plan-migration-or-recovery |

`tests/capability-coverage.yml` and `tests/trigger-cases.yml` reference these prompts by file name, and the shared validator checks that each referenced file exists.

## How the prompts install

Each prompt carries two frontmatter keys: `description` and `agent: github-expert-engineer`.

- GitHub Copilot honours `agent`. Claude Code installs prompts as commands and drops `agent` with a warning (observed with APM 0.33.0).
- At user scope (`apm install -g`), Copilot receives prompts and instructions. Codex receives no prompts, so Codex users invoke the agent directly.
- The verified vendor facts this pack relies on do not record what APM generates from prompts for Gemini CLI or Kiro. The validator's install check scans every generated file for references to uninstalled content, but it does not assert prompt output for those two targets.
