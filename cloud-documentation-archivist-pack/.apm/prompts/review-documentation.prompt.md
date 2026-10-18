---
description: "Review existing documentation for accuracy, structure, links, freshness, editorial quality and exposure of sensitive data"
agent: cloud-documentation-archivist
---

# Review documentation

## Inputs

- The files, folder or pull request diff in scope, and what the review should focus on.
- The implementation or authoritative source to compare the documents against.
- The repository's renderer, linter or link checker, if it has one.
- Whether the user wants findings only or also asked for fixes.

## Workflow

1. Apply documentation-hooks-and-automation. Take a bounded, read-only inventory of the document root, then run the post-write checks on the files in scope: structure, frontmatter, links, placeholders, secret-like values, evidence labels, owner, status and next review. Use the repository's own tooling when it exists. If a check cannot run, do it by hand or record it as not run.
2. Apply documentation-validation-and-link-checking. Run local checks first. Classify links as local, external, authenticated, time-sensitive or illustrative. Validate examples, or label them illustrative. Record every skipped check and why it was skipped.
3. Apply docs-security-privacy-and-redaction to look for secrets, personal and customer data, internal hostnames and identifiers, unsafe commands and unsupported security claims. If a committed value might be a live credential, the owner must rotate it; editing the text does not contain it.
4. Apply diataxis-content-design to find pages that mix modes, and documentation-style-and-editorial-quality for clarity, heading hierarchy, alt text and terminology. Do not raise findings that are only about style preference.
5. Apply repository-and-project-doc-governance to compare each document with its implementation or source. A recent edit does not make a page current.

Stay read-only unless the user asked for fixes. Do not run destructive, billable or credentialed commands to test examples.

## Expected output

Findings, each with id, severity, source (file and line), impact, remediation and verification; the checks that ran and their results; and the checks that were skipped and why.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report. Use CHANGES_REQUIRED when any finding must be fixed before the documents can be relied on.
