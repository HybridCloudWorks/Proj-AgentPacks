---
description: "Review a Google Cloud design or estate against the Well-Architected Framework"
agent: google-cloud-architect
---

# Review a Google Cloud architecture

## Inputs

The design documents, diagrams, infrastructure code or plan output to review, or the exact organization, folder or project to inspect and the identity to use. Ask which pillars and requirements matter most if the user has not said.

## Workflow

Apply gcp-well-architected-review. Gather evidence from the supplied material; for a live estate use gcp-estate-discovery or delegate to gcp-estate-inspector under a read-only identity. Delegate the security pillar to gcp-security-reviewer when an independent review is wanted. Keep the review read-only: do not fix, apply or post anything.

## Expected output

Prioritized findings in the contract's finding format, a per-pillar summary, the evidence and commands behind each finding, items that could not be assessed and why, and a remediation roadmap. Apply the `google-cloud-architect-contract` instruction; asking for a review is not asking for fixes.
