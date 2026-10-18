---
name: python-cli-automation
description: Build Python CLI and subprocess automation with explicit arguments, exit codes and safe filesystem behavior. Use when cLI command, background automation, file processing or subprocess integration is requested.
---

# Python Cli Automation

## Activation and scope

CLI command, background automation, file processing or subprocess integration is requested. Do not treat shell access as permission to publish, delete or contact external systems.

## Inputs and dependencies

- Inputs: CLI framework, argument contract, execution identities, target paths, expected side effects and shell/platform.
- Dependencies: Repository CLI/runtime and identified executable dependencies.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Define arguments/help, configuration precedence, stdout/stderr and exit codes; preserve noninteractive use and structured output consumers.
2. Resolve and constrain paths to authorized targets; prevent traversal, symlink escape and unsafe archive extraction. Use private temporary directories with deterministic cleanup.
3. Invoke known executables with argument arrays and shell=False where possible; bound time/output and handle interruption without orphan processes.
4. Provide dry-run and idempotency for consequential automation; separate discovery from mutation. Test hostile arguments, missing executable, permission denied, timeout, cancellation and partial output.

## Output and validation

CLI or automation patch with documented usage, exit behavior, side-effect scope and regression evidence. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

Ambiguous delete target, shell injection, unexpected executable identity, secret output or unsafe recovery. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `implement-python-feature.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. With the full pack installed, the `python-engineering-contract` instruction supplies the approval, handoff and completion rules.
