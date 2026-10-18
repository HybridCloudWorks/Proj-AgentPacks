---
name: python-language-engineering
description: Implement and review Python semantics, module boundaries, resource lifetime, and compatible public interfaces. Use when a Python implementation, defect, library interface, or version-sensitive change needs hands-on work.
---

# Python Language Engineering

## Activation and scope

A Python implementation, defect, library interface, or version-sensitive change needs hands-on work. Do not use to redesign unrelated modules or replace repository style tools.

## Inputs and dependencies

- Inputs: Relevant code and callers, acceptance criteria, supported interpreter range, CI commands.
- Dependencies: Repository interpreter and standard library; existing formatter, linter, tests.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Resolve requires-python against CI matrices, container images and deployment runtimes; record conflicts before selecting syntax.
2. Trace object lifetime, mutability, scope, iterator exhaustion, descriptors or decorators, imports and public interfaces. Prefer cohesive modules and composition; use advanced object-model features only for a demonstrated need.
3. Keep I/O out of import initialization. Use context managers and explicit ownership for files, clients, locks and generators. Preserve exception causes and return contracts; do not hide errors behind successful-looking defaults.
4. Cover mutable defaults, shared global state, circular imports, datetime timezone and encoding assumptions, serialization boundaries, and accidental quadratic work. Use threads/processes only after identifying CPU versus I/O work.

## Output and validation

Focused patch or located review findings; compatibility decision, tests, cleanup behavior and interface impact. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Unknown minimum interpreter, changed public contract, import side effects, resource leaks or unreproduced defect. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `implement-feature.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. Consult shared instruction, handoff and completion contracts when the full pack is available.
