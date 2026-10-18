---
name: agent-evaluation
description: Evaluate agent outcomes and tool-use process with datasets, deterministic checks, rubrics and human review. Use when agent behavior, release gates, prompt/tool changes or reliability/safety evaluation is requested.
---

# Agent Evaluation

## Activation and scope

Agent behavior, release gates, prompt/tool changes or reliability/safety evaluation is requested. Do not run cost-bearing provider evaluations without scoped authorization.

## Inputs and dependencies

- Inputs: Task distribution, dataset provenance, expected/prohibited behavior, tool policy, budgets and approved thresholds.
- Dependencies: Versioned isolated evaluator, deterministic assertions and optional approved model judge.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Define scenario, purpose, input, preconditions, expected/prohibited outcomes, expected tools/approval, scoring, threshold owner/version and evidence.
2. Measure outcome correctness/usability/grounding/policy/failure/latency/cost and process intent/tool choice/arguments/output use/provenance/scope/termination/recovery.
3. Include ambiguity/conflict, missing dependencies, invalid/malformed input, timeout/cancellation, auth failures, injection/exfiltration, approval bypass, cost exhaustion, duplicates, recovery/rollback and cross-user memory cases.
4. Keep deterministic, statistical, model-judged and human assessments separate; version prompts/tools/models/datasets and prevent test-set leakage. Label unapproved thresholds as draft and require human adjudication for subjective or consequential release decisions.

## Output and validation

Evaluation plan/results with scenario failures, scoring provenance, budgets, human-review gaps and release recommendation. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Unapproved external judge/data, arbitrary threshold presented as policy, judge-only correctness or benchmark overgeneralization. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `evaluate-agent.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
