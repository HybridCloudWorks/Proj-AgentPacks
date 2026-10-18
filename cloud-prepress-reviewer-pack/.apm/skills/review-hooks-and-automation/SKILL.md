---
name: review-hooks-and-automation
description: Uses the pack's pre-review and post-review hooks plus deterministic inventory and report validators to make recurring review checks consistent and non-mutating.
---

# Review Hooks and Automation

Use `hooks/pre-review.ps1` or `hooks/pre-review.sh` before analysis to inventory the diff, classify changed paths, identify likely sensitive files, and report available local validation commands. Use `hooks/post-review.ps1` or `hooks/post-review.sh` after writing the report to validate its schema, finding evidence, recommendation, and redaction rules.

The helpers are advisory gates, not deployment engines. They may read the repository and local files, but they must not apply infrastructure, query live Azure without an explicit read-only mode, modify source, publish artifacts, or delete data. A skipped tool is recorded as skipped.

Extend the tools only when a repeated, observable check justifies automation. Keep policy thresholds and path exclusions visible in the report; never hide failures to make a gate pass.
