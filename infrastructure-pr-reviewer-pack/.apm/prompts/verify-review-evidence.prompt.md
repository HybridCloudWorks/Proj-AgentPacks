---
description: "Run safe, non-deploying checks and judge whether attached plans, previews, renders and CI logs belong to the reviewed commit, target and inputs"
agent: infrastructure-pr-reviewer
---

# Verify review evidence

## Inputs

- Repository root, base and head revisions, and the changed technologies.
- Attached plans, what-if results, compiled or rendered output, test, policy or scan results, CI logs and deployment records.
- Whether dependency downloads are permitted. Assume they are not unless the user says so.

## Workflow

1. Apply the `verify-infrastructure-evidence` Skill. Classify each proposed check as local static, dependency-resolving, remote read, target simulation or mutating execution.
2. From that Skill, run `python scripts/run_review_checks.py --help` once, then `python scripts/run_review_checks.py <repository-root>` for the supported local checks. Pass `--allow-downloads` only when the user has permitted dependency retrieval.
3. Record every check as pass, fail, skip or not applicable, with command, tool version, scope and the relevant output.
4. For each attached artifact, verify commit, inputs, target, identity, state or inventory, dependency lock, tool version and whether deployment consumes that same artifact, using that Skill's `references/evidence-matrix.md`.
5. Interpret passes narrowly. Syntax, lint, compile, render or an empty-state plan does not establish lifecycle, authorization, target or existing-environment safety.
6. Return results to the `review-infrastructure-pr` Skill, which writes the report and decides whether any failed check is a finding.

Never run apply, deploy, destroy, import, state mutation, target-side Ansible, privileged cluster operations, Terraform or OpenTofu tests that can create resources, or untrusted workflows.

## Expected output

The review report in the structure of the `review-infrastructure-pr` Skill's `assets/review-report-template.md`. Coverage and Evidence lists checks executed, checks skipped with the exact reason, and the integrity assessment of each artifact. Evidence Gaps names each missing artifact precisely. A skipped check or absent artifact is never a confirmed defect.

Follow the `infrastructure-pr-reviewer-contract` instruction. Never describe an unexecuted check as passed.
