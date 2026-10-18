# Worked example — Python job assistant evaluation

Task distribution covers status questions, valid job submission, ambiguous scope, invalid input, cross-tenant ID, tool outage, cancellation, duplicate delivery, prompt injection, fabricated approval, budget exhaustion and poisoned memory. Store synthetic cases with purpose/input/preconditions/expected/prohibited behavior, approval expectation, evidence, owner and version.

Deterministic checks verify argument schema, scope, unchanged cross-tenant store, bounded call count, idempotency and termination. Outcome scoring checks task correctness/usability/grounding; process scoring checks tool selection/arguments/output use, approvals, provenance, recovery, latency and cost. Model-judge or human review evaluates explanation quality separately; version the judge prompt and disclose disagreement.

Release thresholds remain draft until a designated owner accepts them. Compare changes against a held-out set with representative error cases; prevent optimization against leaked fixtures. Provider calls require approved data/model/budget and remain unverified in offline pack validation.

Failure example: an agent reports success after the tool returns forbidden. This fails deterministic process/outcome checks regardless of fluent wording. Escalate to primary with trace/tool/result versions and proposed regression. Human release decision is not replaced by a model score.
