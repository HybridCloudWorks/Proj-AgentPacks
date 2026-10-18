---
description: "Review a CI/CD or deployment-wrapper change for trust boundary, identity, target selection, conditions, concurrency and artifact provenance"
agent: infrastructure-pr-reviewer
---

# Review a deployment pipeline change

Use this workflow when a pull request changes GitHub Actions, Azure Pipelines or other CI/CD definitions, reusable workflows or templates, or the Bash, Python, Make or task-runner wrappers that validate, preview, approve, deploy, clean up or roll back infrastructure.

## Inputs

- The diff with base and head revisions, including every reusable workflow, template or wrapper the changed pipeline calls.
- Events, filters, environments, approvals, runner types, permissions, identities, service connections and federated-credential claims, as far as the repository shows them.
- CI logs, artifact digests and environment-approval records, when supplied.

## Workflow

1. Apply the `review-infrastructure-pr` Skill and build full changed-line coverage.
2. Apply `review-cicd-deployment`: map each event to the jobs it starts, establish the trust boundary for forks, pull requests, branches, tags, schedules and manual dispatch, and confirm pull-request code cannot reach privileged secrets, trusted self-hosted runners or production.
3. Trace every changed condition through boolean, string, null, empty, skipped, cancelled and failure semantics. Confirm target and environment are explicit and validated before credentials are acquired.
4. Follow the artifact from build through scan, preview, approval and deployment. The artifact approved must be the artifact deployed.
5. Review concurrency groups, cancellation, stale or delayed runs, retries, timeouts and cleanup against the real shared target.
6. Activate the technology Skill for each tool the pipeline invokes, such as `review-terraform-opentofu` for plan and apply jobs or `review-bicep-arm` for what-if and deployment steps.
7. Apply `verify-infrastructure-evidence` for workflow lint or ShellCheck where installed. Never run the workflow or wrapper to validate it.

Stay read-only. Do not trigger workflows, re-run jobs, approve environments or change repository settings.

## Expected output

The review report in the structure of the `review-infrastructure-pr` Skill's `assets/review-report-template.md`, with the event-to-job trust map summarized in Review Scope and the artifact chain recorded in Coverage and Evidence. When a control depends on repository settings the reviewer cannot see, such as protected environments or required checks, record it under Handoff as a configuration dependency, using the `review-infrastructure-pr` Skill's `assets/repository-enforcement-checklist.md`.

Follow the `infrastructure-pr-reviewer-contract` instruction. Never describe an unexecuted check as passed.
