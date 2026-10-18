# Worked example: a deployment how-to from a "beginner guide" request

Synthetic scenario. The service, team, paths and log content are illustrative.

Prompts used: `plan-documentation.prompt.md`, then `write-tutorial-or-how-to.prompt.md`.

## Request

The Orders Platform engineering manager asks: "Write a beginner guide to deploying orders-api for new team members." The output goes to a branch in the service repository. Nobody asked for anything to be published.

## Orientation

documentation-archivist-orchestration's six questions, answered from the repository and the request:

| Question | Answer |
| --- | --- |
| Reader | An engineer new to the Orders team who already uses git, pull requests and the CI system |
| Task | Get a merged change to staging, then through the production approval gate |
| Authoritative source | `.github/workflows/deploy.yml`, the pipeline as code. `docs/deploy.md` is older and contradicts it |
| Document type | How-to. "Beginner" describes how well the reader knows this service, not their engineering skill. There is no sandbox for a learning journey, so a tutorial would promise something the environment cannot deliver |
| Location and owner | `docs/how-to/deploy-orders-api.md`, owned by the Orders Platform team |
| Evidence and freshness | A sanitized staging run log from 2026-10-14, supplied by the service owner. Review whenever the pipeline file changes |

Skills loaded for the writing: diataxis-content-design, tutorials-and-how-to-guides, templates-and-content-models, docs-security-privacy-and-redaction, documentation-style-and-editorial-quality and documentation-validation-and-link-checking. No others.

## Reconciling the sources

- `deploy.yml` runs `build`, then `deploy-staging` automatically on every merge to `main`, then `deploy-production`. `deploy-production` uses the `production` environment, which needs an approval from the `orders-release` group. A manual trigger with a `ref` input redeploys an earlier tag.
- `docs/deploy.md` was last edited in 2024. It tells readers to run `make deploy-prod` from a laptop. That `Makefile` target still exists. It calls the cloud CLI with the operator's own credentials and skips the approval gate.

The pipeline file governs, so the guide documents only the pipeline path. Whether the `Makefile` bypass should exist is a governance decision for the owner, not something the guide gets to settle, so it is raised as finding F1.

## Writing the guide

Template: `templates/how-to.md`. Kept sections: goal and scope, prerequisites, procedure, troubleshooting, rollback and cleanup, and verification limits.

Procedure as written:

1. Merge the reviewed pull request to `main`. Expected result: a `deploy` run starts.
2. Watch `deploy-staging` finish, then call `GET https://STAGING_HOST/healthz`. Expected result, labelled illustrative: `{"status":"ok","version":"RELEASE_TAG"}`.
3. **Approval gate.** The run pauses at `deploy-production`. A member of `orders-release` approves it in the environment gate after confirming the change window.
4. Run the same health check against `PRODUCTION_HOST`.

Rollback: trigger the workflow manually with `ref` set to the previous release tag. A rollback goes through the same approval gate. Redeploying does not reverse database migrations, so the guide links to the migration runbook instead of describing reversal steps.

Redaction: the supplied log contained the staging hostname and a CI run URL that included the organization name. The hostname became `STAGING_HOST` and the URL was removed. The log held no credentials.

## Completion report

Recommendation: **REVIEW_REQUIRED**

### Scope and audience

How-to guide for engineers new to orders-api who already know git and CI. In scope: deploying a merged change through staging and production with the existing pipeline. Out of scope: first-time access requests, database migration reversal, and the `Makefile` deployment path.

### Source and evidence

| Claim or section | Source | Version or date | Evidence label |
| --- | --- | --- | --- |
| Pipeline stages and approval gate | `.github/workflows/deploy.yml` | commit on `main`, 2026-10-17 | observed |
| Approver group `orders-release` | `production` environment settings, as described by the owner | 2026-10-17 | supplied |
| Staging steps 1 and 2 behave as written | Sanitized staging run log | 2026-10-14 | supplied (run by the service owner, not this session) |
| Production steps 3 and 4, and rollback | No run evidence | — | not verified |

### Content decision

Classified as a how-to, not a tutorial; the reason is recorded under Orientation. Created `docs/how-to/deploy-orders-api.md` from the how-to template. `docs/deploy.md` was left untouched until the owner decides on F1.

### Validation

| Check | Method or command | Result | Notes |
| --- | --- | --- | --- |
| Structure, placeholders, secret-like values | `hooks/post-documentation.sh docs/how-to/deploy-orders-api.md` | passed | Output `PASS` |
| Relative links (3) | Manual resolution against the branch | passed | |
| CI run-history link | — | not run | Needs sign-in; classified as authenticated |
| Steps 1 and 2 | Compared with the supplied staging log | passed | Comparison only; no deployment run by this session |
| Steps 3 and 4, and rollback | — | not run | No authorization or evidence for a production run |

| id | severity | source | impact | remediation | verification |
| --- | --- | --- | --- | --- | --- |
| F1 | Medium | `Makefile:41` (`deploy-prod`), `docs/deploy.md:12` | A documented path deploys to production without the approval gate, and new readers of the old page will follow it | Owner decides whether to remove the target. Then mark `docs/deploy.md` deprecated with a link to the new guide | Owner records the decision; the old page shows a deprecation notice pointing to the guide |

### Limitations

The production steps and rollback are written from the pipeline definition and have not been exercised. The guide's Verification limits section says so. Approver group membership was supplied by the owner and was not inspected.

### Ownership and next review

- Owner: Orders Platform team
- Reviewer or decider: Orders service owner, who must confirm steps 3 and 4 and decide F1
- Document status: Draft
- Next review: the next change to `deploy.yml`, or 2027-01-18, whichever comes first
- Handoff: confirm the production steps on the next release, then set the status to Active
