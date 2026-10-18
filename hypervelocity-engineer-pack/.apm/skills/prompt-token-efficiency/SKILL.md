---
name: prompt-token-efficiency
description: Rewrite prompts and agent instructions for minimal tokens, maximal clarity, low ambiguity, stable terminology, and testable output without removing safety or task-critical context.
---

# Prompt Token Efficiency

Optimize for reliable model execution, not human literary style. Preserve intent, constraints, evidence requirements, approval boundaries, and output quality.

## Compression rules

- State the objective first.
- Put required context before optional context.
- Remove pleasantries, repetition, narrative framing, and decorative examples.
- Use one stable term per concept and explicit measurable constraints.
- Prefer atomic imperative statements and compact tables.
- Replace vague words with acceptance tests, limits, or decision criteria.
- Keep specialized procedures in Skills and dynamic data outside the static prompt.

## Ambiguity audit

Before finalizing, check that every noun is defined, every pronoun has a clear antecedent, scope and time range are explicit, conflicts have precedence, and success criteria are testable. Verify that the shorter prompt still states what must not happen and when to stop or ask for approval.

## Output

Return the compressed prompt, a concise list of preserved constraints, removed duplication, unresolved ambiguity, and any safety behavior that must remain explicit. A shorter prompt is not an optimization if it increases retries, unsafe tool calls, or output rework.
