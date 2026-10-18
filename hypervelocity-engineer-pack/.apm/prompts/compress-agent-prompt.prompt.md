---
description: "Rewrite a prompt, agent profile or workflow instruction for fewer tokens and less ambiguity without dropping constraints"
agent: hypervelocity-engineer
---

# Compress an agent prompt

## Inputs

- The prompt text or file path, and the model, agent or workflow that consumes it.
- Behavior it must preserve: constraints, evidence requirements, approval boundaries and output format.
- Known problems, such as retries, misread scope or inconsistent output.

## Workflow

1. Apply `prompt-token-efficiency`: objective first, required context before optional, one term per concept, measurable constraints, procedures moved to Skills, dynamic data kept out of the static prompt.
2. Run its ambiguity audit: defined nouns, clear antecedents, explicit scope and time range, precedence for conflicts, testable success criteria, and explicit stop and approval conditions.
3. If the text is a GitHub Agentic Workflow body, apply `workflow-lifecycle-and-release` to recompile and validate after the change. If the user wants measured savings, apply `optimize-agentic-workflow` instead of estimating.

## Expected output

The compressed prompt, the constraints preserved, the duplication removed, remaining ambiguity, the safety behavior that must stay explicit, and length before and after labeled measured or estimated. The file is edited only when the user asks. Follow the `hypervelocity-engineer-contract` instruction for the completion report.
