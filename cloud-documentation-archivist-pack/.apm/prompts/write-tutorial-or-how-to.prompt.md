---
description: "Write a tutorial or how-to guide for a cloud, infrastructure, delivery or operations task with safe verification points"
agent: cloud-documentation-archivist
---

# Write a tutorial or how-to guide

## Inputs

- The goal, the reader, and what the reader already knows and can access.
- The procedure's source of truth: scripts, pipeline definitions, infrastructure code, existing guides, or a sanitized record of someone running the steps.
- The environment and platform the guide covers, the permissions each step needs, and any approval, backup or maintenance window.
- The destination folder and its conventions.

## Workflow

1. Apply diataxis-content-design to decide whether the reader is learning (tutorial) or solving a known problem (how-to). Say which mode you chose and why. A "beginner guide" for a competent engineer new to one system is usually a how-to.
2. Apply tutorials-and-how-to-guides.
   - Tutorial: the learner outcome, prerequisites, starting state, sequence, expected result and a clean stopping point.
   - How-to: the goal and assumptions, only the steps that goal needs, decision points, safe commands, expected results, permissions, failure handling, rollback or cleanup, and links to reference.
3. Apply templates-and-content-models to choose the tutorial or how-to template. Replace every placeholder and delete sections that do not apply.
4. Apply docs-security-privacy-and-redaction. Use placeholders for hosts, accounts, subscriptions and keys, and sanitize sample output. Put a visible gate on any destructive or billable step that states the approval or backup it needs.
5. Apply documentation-style-and-editorial-quality: clear headings, uppercase placeholders, and illustrative output labelled as illustrative.
6. Apply documentation-validation-and-link-checking to the changed files.

Do not run deployment, destructive, billable or credentialed commands to prove a step works. Mark a step tested only when there is evidence: the date, the environment and who ran it.

## Expected output

The guide, a list that separates observed steps from untested ones, links to related reference and runbooks, and the files changed.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report. List untested steps under Limitations; never report them as passed.
