---
name: review-powershell-automation
description: Review PowerShell scripts, modules, manifests, DSC, and PowerShell pipeline steps for runtime compatibility, parameter contracts, native command failures, idempotency, quoting, object flow, concurrency, credentials, retries, and tests. Use when a PR changes .ps1, .psm1, .psd1, PowerShell deployment wrappers, or callers that depend on their output. Do not execute deployment scripts merely to validate them.
---

# Objective

Determine whether PowerShell automation fails correctly, preserves typed contracts, remains idempotent and target-safe, and avoids leaking sensitive data across streams, processes, or artifacts.

## Inputs

- Supported PowerShell editions and platforms, module manifests, callers, working directory, identity, environment, and native tools.
- Changed parameters, public functions, output objects, external commands, API calls, retries, cleanup, and tests.
- Parser, PSScriptAnalyzer, Pester, and mocked failure-path evidence when available.

## Workflow

1. Establish actual host, edition, platform, invocation mode, module dependencies, exported functions, working directory, identity, and caller expectations.
2. Review parameter types, validation, defaults, null/empty/scalar/array behavior, path handling, secure values, and backward compatibility.
3. Trace terminating and non-terminating errors, catch/finally behavior, native exit codes, `$LASTEXITCODE`, `Start-Process`, forced success, and pipeline exit status.
4. Review current-state checks, rerun behavior, destructive guards, partial-failure recovery, cleanup, temporary resources, and `ShouldProcess` boundaries where required.
5. Review quoting, interpolation, argument arrays, literal paths, regex, constructed commands, remote execution, JSON depth, encoding, and injection boundaries.
6. Review success/error/warning/verbose/debug/information streams, structured output, secret exposure, transcripts, cached contexts, and concurrent-run collisions.
7. Review API status, pagination, bounded retry, timeout, idempotency, download trust, parser/analyzer results, and Pester coverage of failure paths.
8. Return confirmed findings and evidence gaps to `review-infrastructure-pr`.

## Decision Rules

- A required cmdlet that can emit non-terminating errors must be converted into a failing path when correctness depends on it.
- Native command success must be established from the actual process exit status, not console text.
- `-WhatIf` is not proof that every native or external side effect participates in the guard.
- Prefer typed objects and direct invocation over formatted text and constructed command strings.

## Output Contract

Return technology-specific findings and evidence gaps to `review-infrastructure-pr` with an anchor, trigger, affected target, impact, remediation, and verification evidence. Do not repeat universal gates or create another final report.

## Validation and Stop Conditions

Use `references/review-checklist.md`; verify uncertain semantics through `references/official-sources.md`. Stop when decisive target state, identity, versions, generated output, or safe access is unavailable. Never mutate targets or expose sensitive values.

## Resources

- Read `references/review-checklist.md` for the complete technology adapter.
- Read `references/official-sources.md` when behavior is version-specific, uncertain, or current verification is required.
