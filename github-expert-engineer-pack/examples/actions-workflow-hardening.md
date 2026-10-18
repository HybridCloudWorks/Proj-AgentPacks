# Worked example: moving a deploy workflow to OIDC and least privilege

Prompt: `harden-actions-workflow.prompt.md`. Skills applied: github-expert-orchestration, github-actions-workflows-and-security, github-ci-cd-and-deployment-environments, github-security-and-supply-chain.

The organization, repository, account and role names are fictional. Commit SHAs for pinned actions are shown as `<sha …>`; the real patch carries the resolved 40-character values.

## Request

> Harden `.github/workflows/deploy.yml` in `example-org/payments-api`. It uses AWS access keys from repository secrets. Move it to OIDC and least privilege. Prepare the change; don't push.

## 1. Orient

The actor is a repository admin, so the repository's workflow settings can be read:

```text
gh api repos/example-org/payments-api/actions/permissions/workflow
{"default_workflow_permissions": "write", "can_approve_pull_request_reviews": false}

gh api repos/example-org/payments-api/environments --jq '.environments[] | {name, rules: [.protection_rules[].type]}'
{"name": "production", "rules": ["required_reviewers", "branch_policy"]}
{"name": "staging", "rules": ["branch_policy"]}
```

## 2. Read the workflow end to end

```yaml
name: deploy
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      reason:
        description: Why are you deploying?
        required: true
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-1
      - run: echo "Deploy reason: ${{ github.event.inputs.reason }}"
      - uses: example-tools/ecs-deploy@v3
        with:
          cluster: payments-prod
          service: payments-api
```

What the read turned up:

1. Long-lived AWS keys are stored as repository secrets and readable by every job in every workflow of the repository.
2. The `deploy` job has no `environment`, so the `production` required reviewers never gate it. Every push to `main` deploys straight away.
3. There is no `permissions` key, so the job inherits the repository default `write` token.
4. `github.event.inputs.reason` is expanded inside a `run:` script. Anyone who can dispatch the workflow can inject shell.
5. Every action is referenced by a mutable tag, and one of them is a third-party deploy action.
6. There is no `concurrency` group, so two pushes in quick succession run overlapping deploys.

## 3. Resolve action pins

```text
gh api repos/actions/checkout/git/ref/tags/v4.2.2 --jq '.object | {type, sha}'
```

If `type` is `tag` (an annotated tag), dereference it with `gh api repos/actions/checkout/git/tags/<sha> --jq .object.sha` to get the commit. The same was done for `aws-actions/configure-aws-credentials` and `example-tools/ecs-deploy`. The resolved SHAs and their tags go into the PR description so the reviewer can check them.

## 4. Local patch

```yaml
name: deploy
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      reason:
        description: Why are you deploying?
        required: true
permissions: {}
concurrency:
  group: deploy-production
  cancel-in-progress: false
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    timeout-minutes: 30
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@<sha of v4.2.2> # v4.2.2
        with:
          persist-credentials: false
      - uses: aws-actions/configure-aws-credentials@<sha of the pinned v4 release> # v4.x.y
        with:
          role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
          aws-region: eu-west-1
      - name: Record deploy reason
        env:
          DEPLOY_REASON: ${{ github.event.inputs.reason }}
        run: echo "Deploy reason: $DEPLOY_REASON"
      - uses: example-tools/ecs-deploy@<sha of v3.1.0> # v3.1.0
        with:
          cluster: payments-prod
          service: payments-api
```

`cancel-in-progress: false` queues a second deploy instead of killing one halfway through. `id-token: write` appears only on the job that exchanges the token. `AWS_DEPLOY_ROLE_ARN` is an environment variable on `production`, not a secret: the ARN is not sensitive, and scoping it to the environment keeps other jobs from assuming the role.

## 5. Validate locally

```text
actionlint .github/workflows/deploy.yml
(exit 0, no output)
python -c "import sys, yaml; yaml.safe_load(open(sys.argv[1]))" .github/workflows/deploy.yml
(exit 0)
```

actionlint run on the original file had reported the injection: `"github.event.inputs.reason" is potentially untrusted. avoid using it directly in inline scripts`.

## 6. Handoffs (changes outside this repository's files)

Each item is written up with `templates/handoff.md`:

1. **Cloud identity owner**: create the IAM role with the GitHub OIDC provider `token.actions.githubusercontent.com` as the federated principal, and this trust condition:

   ```json
   "Condition": {
     "StringEquals": {
       "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
       "token.actions.githubusercontent.com:sub": "repo:example-org/payments-api:environment:production"
     }
   }
   ```

   Give the role the same ECS deploy permissions the current access key has, and nothing more.
2. **Repository admin**: create the `production` environment variable `AWS_DEPLOY_ROLE_ARN`.
3. **After the first successful OIDC deploy, in this order**: the cloud identity owner deactivates the old access key; the repository admin deletes `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`; the default workflow permission is changed to `read` as a separate governance change.
4. **Team notice**: with the job bound to `production`, every push to `main` now waits for a required reviewer. That is the intended gate, but it changes how the team works.

## Completion report

### Scope

`.github/workflows/deploy.yml` in `example-org/payments-api`, hardened as a local patch. Repository workflow settings and environments were read. Nothing was pushed, dispatched or changed in AWS or in repository settings.

### Evidence

- CONFIRMED: the repository default workflow token permission is `write` (`GET /repos/example-org/payments-api/actions/permissions/workflow`).
- CONFIRMED: `production` has required reviewers and a branch policy; `deploy.yml` never references it.
- CONFIRMED: the original workflow uses `secrets.AWS_ACCESS_KEY_ID` and `secrets.AWS_SECRET_ACCESS_KEY`, tag-referenced actions, and an inline expansion of `github.event.inputs.reason`.
- CONFIRMED: actionlint flags the inline expansion in the original file and reports nothing on the patch; the patch parses as YAML.
- HYPOTHESIS: the new role's trust condition matches the token's `sub` claim for environment-bound jobs. This is settled only by a live assume-role.

### Findings

#### ACT-1 · High · Long-lived cloud keys stored as repository secrets

- evidence: the `configure-aws-credentials` step in the original `deploy.yml` uses `aws-access-key-id` and `aws-secret-access-key` from repository secrets.
- impact: any workflow or job in the repository can read the keys, and they stay valid until someone rotates them.
- remediation: assume a role via OIDC (patched), then deactivate the keys and delete the secrets after cutover (handoff 3).
- verification: the first deploy run's log shows `Assuming role with OIDC`, CloudTrail shows `AssumeRoleWithWebIdentity` from the run, and the old key shows no use afterwards.

#### ACT-2 · High · Deploy job bypasses the protected production environment

- evidence: the `deploy` job in the original file has no `environment` key, while `production` has `required_reviewers`.
- impact: every push to `main` deploys to production without the required reviewer, which makes the environment protection decorative.
- remediation: set `environment: production` on the job (patched).
- verification: the next run shows "Waiting for review" on `production`, and the deployment record lists the approving reviewer.

#### ACT-3 · Medium · Job inherits a write token by default

- evidence: there is no `permissions` key, and the repository default is `write`.
- impact: every step, including third-party actions, gets a write token for repository contents and more.
- remediation: workflow-level `permissions: {}` and job-level `contents: read` plus `id-token: write` (patched). Changing the repository default to `read` is a separate governance change.
- verification: the "GITHUB_TOKEN Permissions" block in the job's set-up log lists `Contents: read` and `IdToken: write` only.

#### ACT-4 · Medium · Script injection from a dispatch input

- evidence: `run: echo "Deploy reason: ${{ github.event.inputs.reason }}"`, flagged by actionlint.
- impact: anyone who can dispatch the workflow can run arbitrary shell in a job that holds deploy credentials.
- remediation: pass the input through `env` and quote the variable (patched).
- verification: actionlint is clean, and a dispatch with a reason containing `$(id)` prints it literally.

#### ACT-5 · Medium · Actions referenced by mutable tags

- evidence: `actions/checkout@v4`, `aws-actions/configure-aws-credentials@v4` and `example-tools/ecs-deploy@v3`.
- impact: a moved or compromised tag changes the code that runs with deploy credentials.
- remediation: pin full commit SHAs with version comments (patched), and add the `github-actions` ecosystem to Dependabot so the pins get update PRs.
- verification: `git grep -nE "uses: [^@]+@v[0-9]" .github/workflows/deploy.yml` returns nothing.

#### ACT-6 · Low · Overlapping deploys possible

- evidence: no `concurrency` key in the original file.
- impact: two quick pushes can run interleaved deploys to the same service.
- remediation: `concurrency: deploy-production` with `cancel-in-progress: false` (patched).
- verification: a second run shows as pending while the first is in progress.

### Skipped checks

- Live OIDC assume-role and deployment: not verified. The IAM role does not exist yet (handoff 1), and dispatching or deploying was not authorized.
- Review of the `example-tools/ecs-deploy` source at the pinned SHA: not done. The trust decision about that action belongs to the platform team.
- Other workflows' use of the AWS secrets: `git grep` found none, but secrets used by workflows on other branches were not checked.

### Recommendation

READY_FOR_REVIEW

- Rationale: all six findings are fixed in a local patch that passes static validation. What is left is outside the repository files and goes through the handoffs.
- Owner: `payments-api` maintainers for the patch; the cloud identity owner for the role; a repository admin for the variable and, later, removing the secrets.
- Next safe action: the user authorizes pushing the branch and opening a PR. The role is created before the PR merges, because the first post-merge deploy needs it.
