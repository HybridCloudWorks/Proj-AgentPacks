---
name: secure-agent-engineering
description: Assess prompt injection, tool abuse, memory poisoning, isolation, privacy and responsible AI in Python agents. Use when agent, retrieval, browser, model output, MCP or durable-memory boundaries are in scope.
---

# Secure Agent Engineering

## Activation and scope

Agent, retrieval, browser, model output, MCP or durable-memory boundaries are in scope. Do not send confidential prompts/source/customer data to unapproved evaluators.

## Inputs and dependencies

- Inputs: Prompt/tool/retrieval/memory flows, identities/tenancy, oversight, data policy and misuse scenarios.
- Dependencies: Application policy enforcement layer and sanitized security/evaluation fixtures.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Map instruction/data boundaries; treat retrieved documents, browser text, tool results, skills and model-generated code as untrusted.
2. Enforce authorization, approval and budgets in deterministic boundaries; narrow tools to domains/files/records/actions. Prevent confused-deputy use and cross-tenant context.
3. Review purpose/disclosure, data minimization/expiry/deletion, grounding/provenance, contestability, accessible escalation, human oversight, fairness and monitored feedback.
4. Test exfiltration, injection, malformed results, poisoned memory, denial of service, approval bypass and excessive autonomy. Use protected-characteristic data only for a documented lawful approved purpose with privacy/fairness controls; require human judgment for consequential decisions.

## Output and validation

Threat model, misuse findings, executable negative-case plan, responsible-AI constraints and release/escalation recommendation. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Policy enforced only by model prose, missing tenant isolation, retained secrets or unsafe fallback. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `evaluate-agent.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
