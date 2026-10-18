---
name: documentation-validation-and-link-checking
description: Validate documentation structure, frontmatter, links, code examples, templates, terminology, freshness, redaction, and report quality.
---

# Documentation Validation

Run local checks first: frontmatter parsing, required sections, heading order, duplicate titles, link targets, image alt text, code fence language, placeholder detection, secret-like values, terminology, date format, and stale review metadata. Use the repository's renderer or linter when present.

Classify links as local, external, authenticated, time-sensitive, or intentionally illustrative. A successful HTTP response does not prove the linked content is correct or accessible to the intended reader. Record skipped checks and rate-limit or authentication limits.

For examples, validate syntax or label them illustrative. Do not execute destructive, billable, or credentialed commands merely to make documentation green. Report exact file/line findings, severity, remediation, and residual not-verified checks.
