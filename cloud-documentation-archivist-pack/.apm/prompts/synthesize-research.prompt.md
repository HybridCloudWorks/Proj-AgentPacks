---
description: "Turn cloud research, vendor documentation, incidents and repository evidence into a cited brief or comparison with a source ledger"
agent: cloud-documentation-archivist
---

# Synthesize research into a cited brief

## Inputs

- The question, the audience, and the decision or action the brief supports.
- A date boundary and the confidence the reader needs.
- The sources the user supplied or allows. Use web access only when the host provides it and the user has authorized it for this task.
- Where the brief will live, if it is to become durable knowledge.

## Workflow

1. Apply research-synthesis-and-source-traceability.
   - Keep a source ledger. For each source record the title, URL or path, publisher, version or date, accessed date, the claim it supports, its limitations, and whether it is current.
   - Prefer primary vendor documentation, standards, source code and observed evidence. Use secondary sources to find leads and label them secondary.
   - Label every statement as fact, inference, recommendation, unresolved conflict or not verified.
   - Check region, plan and version constraints, and tell similar product names apart.
   - Keep material disagreements visible instead of averaging them away.
2. Apply documentation-style-and-editorial-quality. Lead with the answer, synthesize rather than paste, and put each claim's citation next to it.
3. Apply docs-security-privacy-and-redaction. Leave out private conversation content, customer data, and internal details the audience should not see.
4. If the brief is to be filed as durable knowledge, apply knowledge-base-and-taxonomy to add its metadata, owner, status and next review date.

Do not send the brief, or any research material, to an external system without authorization.

## Expected output

A brief or comparison with each claim cited next to it, the source ledger, a list of conflicts and of statements that could not be verified, and a recommendation labelled as one.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report. If sources could not be checked for currency, say so under Limitations.
