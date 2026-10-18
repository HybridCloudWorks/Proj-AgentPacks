# Worked example: is a release ready to promote to production?

Prompt: `assess-release-readiness.prompt.md`. Skills applied: github-expert-orchestration, github-releases-packages-and-artifacts, github-ci-cd-and-deployment-environments, github-audit-evidence-and-compliance.

The organization, repository, digests and run IDs are fictional; digests are shortened.

## Request

> Is `payments-api` v2.4.0 ready to promote from staging to production?

Assessment only. Promoting, deploying, retagging and changing environment settings were not authorized.

## 1. Tag, release and source commit

```text
git rev-parse v2.4.0^{commit}
9e3f1c7…
gh release view v2.4.0 --repo example-org/payments-api --json tagName,isDraft,isPrerelease,publishedAt,assets --jq '{tagName,isDraft,isPrerelease,publishedAt,assets:[.assets[].name]}'
{"tagName": "v2.4.0", "isDraft": false, "isPrerelease": false, "publishedAt": "2026-10-15T13:02:11Z", "assets": ["sbom.spdx.json"]}
```

## 2. Build run and artifact digest

```text
gh run list --repo example-org/payments-api --workflow release.yml --commit 9e3f1c7 --json databaseId,event,conclusion
[{"databaseId": 11902215530, "event": "push", "conclusion": "success"}]
gh run download 11902215530 --repo example-org/payments-api -n image-digest -D ./evidence
cat ./evidence/image-digest.txt
sha256:4f0c…e21a
```

## 3. Provenance

```text
gh attestation verify oci://ghcr.io/example-org/payments-api@sha256:4f0c…e21a --owner example-org
✓ Verification succeeded!
  predicate type: https://slsa.dev/provenance/v1
  signer workflow: example-org/payments-api/.github/workflows/release.yml@refs/tags/v2.4.0
```

So the image digest was built by `release.yml` from the tag.

## 4. Staging received that digest

```text
gh api "repos/example-org/payments-api/deployments?environment=staging&per_page=1" --jq '.[0] | {id, sha, ref, created_at}'
{"id": 2209871, "sha": "9e3f1c7…", "ref": "v2.4.0", "created_at": "2026-10-15T13:20:40Z"}
gh api repos/example-org/payments-api/deployments/2209871/statuses --jq '.[0].state'
"success"
gh run view 11902391044 --repo example-org/payments-api --log | grep -m1 "image:"
deploy-staging  Deploy  image: ghcr.io/example-org/payments-api@sha256:4f0c…e21a
```

## 5. The production path

`.github/workflows/deploy-production.yml` runs on `workflow_dispatch` with a `version` input:

```yaml
jobs:
  deploy:
    environment: production
    steps:
      - uses: actions/checkout@<pinned sha> # v4.2.2
        with: { ref: "${{ inputs.version }}" }
      - run: docker build -t ghcr.io/example-org/payments-api:${{ inputs.version }} .
      - run: docker push ghcr.io/example-org/payments-api:${{ inputs.version }}
      - run: ./deploy.sh production ghcr.io/example-org/payments-api:${{ inputs.version }}
```

Production rebuilds the image from source and deploys it by tag. It does not promote the attested digest that staging ran. It also expands `inputs.version` straight into `run:` scripts, which is script injection for anyone who can dispatch the workflow. The production image would be a different, unattested build, and rollback would rebuild an old tag rather than redeploy a known digest.

## 6. Production environment protection

```text
gh api repos/example-org/payments-api/environments/production --jq '{rules: [.protection_rules[].type], deployment_branch_policy}'
{"rules": ["branch_policy"], "deployment_branch_policy": {"protected_branches": false, "custom_branch_policies": true}}
gh api repos/example-org/payments-api/environments/production/deployment-branch-policies --jq '.branch_policies[] | {name, type}'
{"name": "main", "type": "branch"}
{"name": "v*", "type": "tag"}
```

Production has no required reviewers. Any `v*` tag can deploy to it, so the tag protection matters:

```text
gh api "repos/example-org/payments-api/rulesets?includes_parents=true" --jq '.[] | select(.target == "tag") | {id, name, enforcement}'
{"id": 91, "name": "release-tags", "enforcement": "disabled"}
```

## 7. Rollback target

```text
gh api "repos/example-org/payments-api/deployments?environment=production&per_page=1" --jq '.[0] | {ref, sha, created_at}'
{"ref": "v2.3.2", "sha": "41aa0d2…", "created_at": "2026-09-29T10:05:12Z"}
gh api orgs/example-org/packages/container/payments-api --jq .visibility
"private"
```

The v2.3.2 image is still in the registry, but because production deploys by tag rather than digest, the exact image that production runs today is not recorded in GitHub.

## Completion report

### Scope

Promotion readiness of `example-org/payments-api` v2.4.0 from staging to production: tag, release, build run, digest, attestation, staging deployment, production workflow, environment protection, tag protection and rollback target. Read-only; nothing was promoted.

### Evidence

- CONFIRMED: tag v2.4.0 points to `9e3f1c7`; the release is published and not a prerelease.
- CONFIRMED: run 11902215530 (`release.yml`, push of the tag) succeeded and produced digest `sha256:4f0c…e21a`.
- CONFIRMED: `gh attestation verify` succeeded for that digest, with SLSA provenance v1 signed by `release.yml@refs/tags/v2.4.0`.
- CONFIRMED: staging deployment 2209871 for `9e3f1c7` succeeded, and the staging job log shows the attested digest.
- CONFIRMED: `deploy-production.yml` rebuilds the image from source and deploys by tag.
- CONFIRMED: the `production` environment has only a branch policy (`main`, tags `v*`) and no required reviewers.
- CONFIRMED: the tag ruleset 91 `release-tags` is disabled.
- CONFIRMED: the last production deployment is v2.3.2 (`41aa0d2`); the package is private.

### Findings

#### ACT-1 · High · Production rebuilds instead of promoting the attested digest

- evidence: the `docker build` and `docker push` steps in `deploy-production.yml`; the deploy step uses `:${{ inputs.version }}`, not a digest.
- impact: production would run an image that was never tested in staging and has no attestation, and a rollback cannot reproduce the previous image exactly.
- remediation: change the production job to take a digest (or read it from the release run's artifact), verify it with `gh attestation verify`, and deploy `image@sha256:…` with no build step. Pass the input through `env` instead of expanding `${{ inputs.version }}` inside `run:`. Record the digest in the deployment payload.
- verification: a staging-then-production dry run in a non-production copy shows the same digest in both job logs, with no build step in the production job.

#### GH-1 · High · Production deploys need no reviewer

- evidence: `protection_rules` for `production` contains only `branch_policy`.
- impact: anyone who can dispatch the workflow can deploy any `main` commit or `v*` tag to production without a second person.
- remediation: a repository admin adds required reviewers (the release managers team), turns on "prevent self-review", and optionally sets a wait timer.
- verification: `gh api repos/example-org/payments-api/environments/production --jq '[.protection_rules[].type]'` includes `required_reviewers`.

#### GH-2 · Medium · Tags that can deploy to production are unprotected

- evidence: the `production` branch policy allows tags `v*`; the only tag ruleset (91) is disabled.
- impact: anyone with write access can create or move a `v*` tag onto unreviewed code and deploy it.
- remediation: enable a tag ruleset on `v*` that restricts creation, update and deletion to the release managers. This is an organization governance change.
- verification: `GET /repos/example-org/payments-api/rulesets?includes_parents=true` shows an active tag ruleset covering `v*`.

### Skipped checks

- What production actually runs today: not verified, because production deploys by tag and the cluster is outside GitHub.
- Tag signature on v2.4.0: not checked, because no signing policy was supplied.
- Contents of `sbom.spdx.json`: present, not reviewed.
- A dry run of a digest-based promotion: not run, because deploying was not authorized.

### Recommendation

CHANGES_REQUIRED

- Rationale: v2.4.0 itself is well evidenced up to staging. The production path would not deploy that artifact, and nothing stops an unreviewed deploy, so promotion now would break the provenance chain the release established.
- Owner: the release manager for the promotion path; a repository admin for the production reviewers; an organization owner for the tag ruleset.
- Next safe action: hold the promotion. Fix the promotion path and add production reviewers first, then re-run this assessment against the same digest. The tag ruleset can follow as a governance change.
