---
name: cloud-prepress-orchestration
description: Orchestrates the evidence-first review between implementation and pull request or deployment, selecting only the review domains required by the changed artifact.
---

# Cloud Pre-Press Orchestration

This is the entry Skill for a built change that is not yet approved for PR merge or deployment. Establish the target, baseline, changed files, implementation intent, environment, deployment scope, evidence available, and authorization boundary before detailed review.

Route only the needed Skills. Typical sequence: scope → architecture/ADR → code/IaC/security → tests/build → preview/policy → operations/rollback/cost → report/gate. Run independent static checks in parallel; serialize anything requiring shared state or live read-only access.

The reviewer is read-only by default. It may inspect files, diffs, tests, generated artifacts, local tool output, and explicitly authorized read-only cloud evidence. It must not apply, deploy, delete, force-unlock state, change RBAC/policy, rotate secrets, or publish a PR. A missing check is `not-verified`, not a pass.

Stop and classify blockers when requirements, ownership, authorization, plan/what-if evidence, rollback, or required inputs are missing. Do not manufacture findings from generic preferences.
