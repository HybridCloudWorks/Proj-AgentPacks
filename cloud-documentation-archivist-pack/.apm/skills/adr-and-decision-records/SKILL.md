---
name: adr-and-decision-records
description: Author and maintain concise Architecture Decision Records and decision logs with alternatives, consequences, traceability, status, and supersession.
---

# ADR and Decision Records

Write one significant decision per record. Include identifier, title, status, date, deciders, context and problem, forces or requirements, options with honest trade-offs, decision, consequences, risks, follow-ups, and links to evidence.

Store records where the repository convention says; otherwise use `docs/decisions/` or `docs/adr/` with stable numbering. Never edit the decision of an Accepted ADR. Supersede it with a new record and link both directions. Preserve Proposed, Accepted, Rejected, Deprecated, and Superseded status meaning.

Keep depth proportional to the decision. Do not invent concrete versions or costs. Separate architectural rationale from implementation detail and link to requirements, diagrams, plans, and runbooks.
