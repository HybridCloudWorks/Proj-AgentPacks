# Worked example: a cited brief on CI deployment credentials

Synthetic scenario. Documents, dates and file names are illustrative. Vendor statements are described at the level of detail the supplied exports support, not quoted from live documentation.

Prompt used: `synthesize-research.prompt.md`.

## Request

"Turn this research into a comparison brief. Should production deploys stop using the stored cloud credential and switch to OIDC federation like staging?" The audience is the platform and security leads, who will decide whether to open a decision record.

Web access was not authorized for this session. Only the supplied sources and the repository were used.

## Source ledger

Built from `templates/source-ledger.md` and saved as `research/ci-credentials/source-ledger.md`.

| # | Title | URL or path | Kind | Version or date | Accessed | Relevant claim | Current? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | CI vendor: security hardening with OpenID Connect | `research/ci-credentials/exports/ci-oidc.pdf` | Primary | saved 2026-07-21 | 2026-10-18 | Jobs can request a short-lived identity token; the cloud trust can be conditioned on repository, branch and environment claims | Not verified |
| S2 | Cloud provider: workload identity federation | `research/ci-credentials/exports/cloud-wif.pdf` | Primary | saved 2026-07-21 | 2026-10-18 | The federated credential is exchanged for a short-lived access token; no long-lived secret is stored in CI | Not verified |
| S3 | Internal security standard SEC-STD-12 | `standards/SEC-STD-12.md` | Primary (internal) | v3, 2026-03-04 | 2026-10-18 | CI credentials must be short-lived where the platform supports it | Yes |
| S4 | Staging deploy workflow | `.github/workflows/deploy-staging.yml` | Observed | `main`, 2026-10-17 | 2026-10-18 | Requests `id-token: write` and logs in with federation | Yes |
| S5 | Production deploy workflow | `.github/workflows/deploy-prod.yml` | Observed | `main`, 2026-10-17 | 2026-10-18 | Logs in with the stored credential referenced as `CLOUD_DEPLOY_CREDENTIAL` | Yes |
| S6 | Blog post: "Why we abandoned OIDC for CI" | `research/ci-credentials/exports/blog-2023.html` | Secondary | 2023-02 | 2026-10-18 | Says federated identities cannot be limited to one branch | No |
| S7 | Internal wiki: CI credentials | Supplied page export | Secondary (internal) | 2025-11 | 2026-10-18 | Says both pipelines use stored credentials | No |

Only the reference name of the stored credential (S5) appears. No credential value was read or recorded.

## Conflicts

- **S6 against S1 and S2.** The blog says branch scoping is impossible. Both primary exports, which are newer, describe trust conditions on branch and environment claims. The primary sources govern, and S6 is labelled outdated.
- **S7 against S4.** The wiki says staging uses a stored credential, but the workflow file shows federation. The observed file governs, and the wiki's error is raised as finding F1.

## Brief

Saved as `research/ci-credentials/brief.md`. It leads with the answer:

- **Recommendation:** move production to federation, scoped to the `production` environment claim. Open a decision record with `record-decision.prompt.md`.
- **Facts:** staging already uses federation (S4); production uses a stored long-lived credential (S5); the internal standard asks for short-lived credentials where supported (S3).
- **Facts that may have changed since the exports were saved:** federation removes the stored secret (S1, S2), and trust can be limited to an environment (S1, S2).
- **Inference:** the staging configuration can be reused with a production-scoped condition. Nothing supplied shows this has been tried.
- **Not verified:** whether the production cloud account's policy allows a federated trust to be created. No source covers it.

knowledge-base-and-taxonomy metadata on the brief: owner Platform Security, status Draft, tags `ci`, `identity` and `credentials`, next review 2027-01-18.

## Completion report

Recommendation: **NOT_VERIFIED**

### Scope and audience

A comparison brief for the platform and security leads, supporting the decision on the production deploy credential. Other pipelines and runtime workload identity are out of scope.

### Source and evidence

The source ledger above (S1 to S7). Repository observations are dated 2026-10-17. The two vendor sources are exports saved on 2026-07-21 and were not checked against current documentation.

### Content decision

Wrote a brief with the answer first, every claim labelled, and citations next to the claims. The ledger and the brief sit side by side under `research/ci-credentials/`. Nothing was sent outside the repository.

### Validation

| Check | Method or command | Result | Notes |
| --- | --- | --- | --- |
| Structure and secret scan | `hooks/post-documentation.sh research/ci-credentials/brief.md research/ci-credentials/source-ledger.md` | passed | |
| Every brief claim has a ledger entry | Manual cross-check | passed | 11 claims, all cited |
| Vendor exports are current | — | not run | Web access not authorized |
| Production trust policy allows federation | — | not run | No source available |

| id | severity | source | impact | remediation | verification |
| --- | --- | --- | --- | --- | --- |
| F1 | Low | Internal wiki "CI credentials" (S7) | Readers believe staging still holds a stored credential and may rotate or audit the wrong thing | The wiki owner updates the page and links the brief; editing the wiki is an external write and needs their authorization | The page matches `deploy-staging.yml` |

### Limitations

The vendor statements rest on exports about three months old. The production account's policy was not examined. The recommendation is a recommendation and has not been accepted.

### Ownership and next review

- Owner: Platform Security
- Reviewer or decider: platform lead and security lead
- Document status: Draft
- Next review: after the vendor sources are checked against current documentation, or 2027-01-18
- Handoff: check the currency of S1 and S2, confirm the production account policy, then open the decision record
