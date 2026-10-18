---
name: python-static-typing
description: Design precise Python interfaces and resolve static typing errors while keeping runtime validation explicit. Use when public API typing, model boundaries, checker errors, stub quality, or modernization is in scope.
---

# Python Static Typing

## Activation and scope

Public API typing, model boundaries, checker errors, stub quality, or modernization is in scope. Avoid repository-wide strictness expansion during a narrow feature.

## Inputs and dependencies

- Inputs: Checker configuration/version, failing diagnostics, interface consumers, interpreter support.
- Dependencies: Configured checker and existing runtime boundary validator.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Reproduce the configured checker diagnostics with the repository command; preserve strictness, plugins and excludes unless a justified change is requested.
2. Use Protocol for behavioral seams, generics for relationships, precise nullable/state models and typed structures. Check callable sync/async contracts and variance at library boundaries.
3. Narrow object-valued input before use. Prefer resolving errors over Any, casts or ignores; for a necessary suppression record the exact diagnostic, reason, scope and follow-up.
4. Validate requests, environment configuration, messages, database assumptions and model/tool output at runtime separately. Type annotations and casts do not validate external data.

## Output and validation

Typed interface or targeted diagnostic fix, checker evidence, runtime-validation coverage and suppression ledger. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Unsupported syntax, missing third-party stubs, checker-version disagreement or typing-only fix that leaves unsafe runtime input. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `implement-python-feature.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
