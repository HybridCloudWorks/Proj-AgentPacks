# Worked example: a security posture audit that cannot be verified

Prompt: `audit-security-posture.prompt.md`. Skills applied: github-expert-orchestration, github-security-and-supply-chain, github-actions-workflows-and-security, github-audit-evidence-and-compliance.

This example ends unverified. The local findings are real, but the evidence the decision depends on (feature enablement and alert state) cannot be read with the actor's access. The organization, repository and dates are fictional.

## Request

> Audit the GitHub security posture of `example-org/payments-api`. We need evidence for our SOC 2 auditor next week.

## 1. Orient

The actor uses a fine-grained token with repository `Contents`, `Metadata`, `Actions` and `Pull requests` read. It has no `Administration`, `Code scanning alerts`, `Secret scanning alerts` or `Dependabot alerts` permission. Nobody suspects a current secret exposure, so containment is not needed first.

## 2. Local inventory

| Control | Local evidence |
|---|---|
| Security policy | `SECURITY.md` present; points reporters to private vulnerability reporting |
| Code scanning | `.github/workflows/codeql.yml`: advanced setup, matrix `language: [javascript-typescript]`, on push and PR to `main` plus a weekly schedule |
| Languages in the repository | TypeScript in `src/`; Python in `services/reconciler/` (`pyproject.toml`), deployed by `.github/workflows/deploy-reconciler.yml` |
| Dependabot | `.github/dependabot.yml`: one `npm` entry for `/`; no `pip`, no `github-actions` |
| Dependency review | no `actions/dependency-review-action` in any workflow |
| Action references | `git grep -nE "uses: [^./][^@]+@v[0-9]" .github/workflows` finds 7 tag references, 3 of them to third-party actions |

## 3. Remote reads

```text
gh api repos/example-org/payments-api --jq '.security_and_analysis'
null
```

GitHub returns `security_and_analysis` only to repository admins and organization owners or security managers. A `null` here says nothing about whether secret scanning or push protection is on.

```text
gh api "repos/example-org/payments-api/code-scanning/alerts?state=open&per_page=1"
gh: Resource not accessible by personal access token (HTTP 403)
gh api "repos/example-org/payments-api/secret-scanning/alerts?state=open&per_page=1"
gh: Resource not accessible by personal access token (HTTP 403)
gh api "repos/example-org/payments-api/dependabot/alerts?state=open&per_page=1"
gh: Resource not accessible by personal access token (HTTP 403)
```

The calls stopped at the first 403. Retrying with other endpoints would not change the token's permissions.

What the token can read:

```text
gh run list --repo example-org/payments-api --workflow codeql.yml --limit 5 --json event,conclusion,createdAt
5 runs, all "success"; the latest is a "schedule" run on 2026-10-13

gh api repos/example-org/payments-api/rules/branches/main --jq '[.[].type]'
["deletion", "non_fast_forward", "pull_request", "required_status_checks"]
```

No `code_scanning` rule applies to `main`, so code scanning results do not gate merges.

## 4. Evidence ledger (abridged)

The ledger follows `templates/evidence-ledger.md`. Rows that could not be observed carry the ledger's not-verified label there. In the report below they move to Skipped checks.

| # | Statement | Label | Source |
|---|---|---|---|
| E1 | CodeQL workflow runs successfully on a schedule | CONFIRMED | `gh run list --workflow codeql.yml` |
| E2 | CodeQL analyzes JavaScript and TypeScript only | CONFIRMED | `codeql.yml` matrix |
| E3 | The Python service is production code | CONFIRMED | `deploy-reconciler.yml` deploys `services/reconciler` |
| E4 | No code scanning merge gate on `main` | CONFIRMED | `GET /repos/.../rules/branches/main` |
| E5 | Secret scanning and push protection enabled | not verified | `security_and_analysis` returned `null` |
| E6 | Open code scanning, secret scanning and Dependabot alerts | not verified | HTTP 403 on all three endpoints |

## Completion report

### Scope

The GitHub security and supply-chain controls of `example-org/payments-api`, for SOC 2 evidence. Read-only local inventory plus the API reads the actor's token allows. No settings, alerts or credentials were touched.

### Evidence

- CONFIRMED: `SECURITY.md` is present and refers to private vulnerability reporting.
- CONFIRMED: the CodeQL advanced-setup workflow analyzes `javascript-typescript` only and ran successfully five times, most recently on 2026-10-13.
- CONFIRMED: `services/reconciler/` is Python and is deployed by `deploy-reconciler.yml`.
- CONFIRMED: `dependabot.yml` configures `npm` only.
- CONFIRMED: the effective rules on `main` include no code scanning rule.
- CONFIRMED: 3 third-party actions are referenced by mutable tags.
- INFERRED: Python vulnerabilities in the reconciler are not covered by code scanning, from the matrix and the repository contents.

### Findings

#### SEC-1 · Medium · Code scanning skips the production Python service

- evidence: the `language` matrix in `.github/workflows/codeql.yml` (`javascript-typescript` only); `services/reconciler/pyproject.toml`; `deploy-reconciler.yml`.
- impact: injection and deserialization flaws in a deployed service go undetected. An auditor reading "CodeQL enabled" would overstate coverage.
- remediation: add `python` to the matrix, or move to default setup, which detects languages; the security owner chooses.
- verification: the next CodeQL run lists a `python` analysis, and `gh api repos/example-org/payments-api/code-scanning/analyses` (with alert read permission) shows it.

#### SEC-2 · Medium · Dependabot version updates cover npm only

- evidence: `.github/dependabot.yml` has one `npm` entry; there are no `pip` or `github-actions` entries.
- impact: Python dependencies and action versions drift without update PRs. If actions are pinned to SHAs later, the pins will never be refreshed.
- remediation: add `pip` (directory `/services/reconciler`) and `github-actions` (directory `/`) entries.
- verification: update PRs for both ecosystems appear after the next scheduled run. Version updates are separate from Dependabot alerts, whose state is still unread.

#### SEC-3 · Low · Code scanning results do not gate merges

- evidence: the effective rules on `main` are `deletion`, `non_fast_forward`, `pull_request` and `required_status_checks`, with no `code_scanning` rule.
- impact: a PR that introduces a high-severity alert can merge.
- remediation: add a "require code scanning results" rule through a governance change (`review-repository-governance.prompt.md`).
- verification: the rules endpoint lists a `code_scanning` rule for `main`.

#### SEC-4 · Low · Third-party actions referenced by mutable tags

- evidence: 3 third-party `uses:` references with `@v` tags in `.github/workflows/`.
- impact: a moved or compromised tag changes the code that runs in CI.
- remediation: pin to full commit SHAs with version comments, together with the `github-actions` Dependabot entry recommended above.
- verification: the `git grep` in section 2 returns only first-party references.

### Skipped checks

- Secret scanning, push protection and private vulnerability reporting enablement: not verified, because `security_and_analysis` is visible only to admins and security managers.
- Open code scanning, secret scanning and Dependabot alerts, with their counts, severities and ages: not verified (HTTP 403 on all three endpoints).
- Artifact attestations for releases: not checked in this pass.
- Organization-level security configurations that may apply to the repository: not readable with this token.

### Recommendation

NOT_VERIFIED

- Rationale: the four findings are confirmed and worth fixing. But a SOC 2 posture statement depends on feature enablement and alert state, and none of that could be read. Calling the posture good or bad from workflow files alone would overstate the evidence.
- Owner: the `example-org` security manager, or a repository admin for `payments-api`.
- Next safe action: a security manager runs these read-only commands and returns counts and states only (no alert payloads): `gh api repos/example-org/payments-api --jq .security_and_analysis`, then the three alert endpoints with `state=open`, summarized by severity and age. An alternative is a short-lived token with read-only `Administration`, `Code scanning alerts`, `Secret scanning alerts` and `Dependabot alerts` permissions on this one repository.
