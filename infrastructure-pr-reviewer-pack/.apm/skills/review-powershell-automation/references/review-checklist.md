# PowerShell Review Adapter

Apply this adapter to `.ps1`, `.psm1`, `.psd1`, PowerShell-based pipeline steps, Desired State Configuration, and scripts that orchestrate cloud, infrastructure, packaging, or deployment tools.

## 1. Runtime and calling context

Identify:

- Supported PowerShell editions and versions.
- Windows, Linux, and macOS assumptions.
- Module manifest, exported functions, required modules, and dependency versions.
- Calling pipeline, working directory, execution policy, identity, environment variables, and native tools.
- Whether the file is dot-sourced, imported as a module, invoked as a script, or run in a child process.

Review behavior under the actual host and shell. Windows PowerShell and PowerShell 7 can differ in module availability, encoding, native command behavior, and platform APIs.

## 2. Parameters and contracts

Verify:

- Parameters have correct types, mandatory rules, validation, aliases, defaults, and pipeline-binding behavior.
- Secure values do not use plaintext defaults or unsafe conversions.
- Empty strings, nulls, empty arrays, scalar-versus-array inputs, and wildcard characters behave intentionally.
- Paths are resolved safely and do not depend on an unexpected current directory.
- Public functions and module exports remain backward compatible for callers.
- Objects are passed as objects where possible rather than flattened to fragile text.

Do not require advanced-function features mechanically. Require them when the script's contract, safety, or pipeline behavior depends on them.

## 3. Error handling and native commands

Scrutinize:

- `try`/`catch` blocks around operations that can emit non-terminating errors without `-ErrorAction Stop` or equivalent handling.
- Native command invocations whose exit status is not checked or propagated.
- `$LASTEXITCODE` being overwritten before inspection.
- `Start-Process` without `-Wait`, `-PassThru`, or exit-code verification when completion matters.
- `continue`, empty catches, broad catches, `SilentlyContinue`, and warning-only failures that allow a pipeline to succeed.
- Pipeline commands that write an error but still exit zero.
- Cleanup in `finally` that masks the original failure.

A script must fail the calling job when a required deployment or configuration action fails.

## 4. Idempotency and current-state checks

Verify:

- Create operations distinguish absent, present, and partially configured states.
- Append operations do not duplicate entries on rerun.
- Updates compare the intended and actual values accurately.
- Deletes or resets are scoped to the intended object.
- Retry after partial failure does not create duplicates or repeat irreversible actions.
- Temporary files, mounts, sessions, locks, and credentials are cleaned up safely.
- `SupportsShouldProcess`, `-WhatIf`, or `-Confirm` is used where the repository contract requires interactive or operator-safe destructive behavior.

`-WhatIf` support is not proof of safety; verify that every destructive side effect participates and that native commands are not executed outside the guard.

## 5. Quoting, interpolation, and injection

Verify:

- User-controlled values are not inserted into `Invoke-Expression`, script blocks, command strings, Azure DevOps logging commands, or shell invocations unsafely.
- Native arguments preserve whitespace, quotes, wildcard characters, newlines, and special characters.
- Paths use appropriate joining and literal-path semantics.
- Here-strings, expandable strings, and subexpressions do not expose secrets or alter JSON/YAML unexpectedly.
- Regex input is escaped when treated literally.
- Remote commands and encoded commands have a clear trust boundary.

Prefer argument arrays, typed objects, splatting, and direct cmdlet invocation over constructed command strings.

## 6. Output streams and object flow

Review all output streams:

- Success output used by callers.
- Error output and exit status.
- Warning, verbose, debug, information, and host output.
- Progress output in noninteractive jobs.

Verify:

- Diagnostic text is not mixed into machine-readable JSON or object output.
- Secrets are not written to any stream or transcript.
- Functions return stable object shapes and types.
- `Write-Host` is not used where a caller needs structured output.
- `ConvertTo-Json` depth and encoding preserve nested deployment data.
- Downstream tools receive the exact intended value rather than formatted display text.

## 7. Scopes, state, and concurrency

Verify:

- Variables do not leak through global, script, or module scope unexpectedly.
- Parallel jobs, runspaces, or pipeline matrix runs do not collide on files, resource names, ports, or shared CLI context.
- Current subscription, tenant, account, Kubernetes context, or working directory is set and verified explicitly.
- Imported modules and profiles cannot silently alter behavior in CI; use clean profiles where appropriate.
- Cached credentials and contexts are not reused across environments.
- Locks and temporary state survive or recover from cancellation correctly.

## 8. Credentials and sensitive data

Verify:

- No plaintext secrets, tokens, certificates, private keys, or connection strings in source, defaults, logs, history, transcripts, files, or command lines.
- `SecureString` and `PSCredential` are not converted to plaintext without a tightly controlled need and lifetime.
- Secret values are not serialized into CLIXML or artifacts that cross trust boundaries unexpectedly.
- Debug or verbose output cannot reveal headers, tokens, request bodies, or environment variables.
- Cloud login uses the intended identity and verifies tenant or subscription context.

## 9. External APIs, retries, and timeouts

Verify:

- REST calls validate status, content type, pagination, throttling, and partial results.
- Retries are bounded and limited to transient failures.
- Non-idempotent POST or create calls use idempotency controls or current-state checks.
- Polling loops have timeouts, backoff, and clear terminal states.
- TLS validation is not disabled.
- Downloads use trusted sources and integrity verification where supported.

## 10. Validation and tests

Use, when available:

- PowerShell parser validation for all changed scripts.
- PSScriptAnalyzer with repository configuration.
- Pester tests for functions, parameter validation, object output, and failure paths.
- Mocked native commands and API calls, including nonzero exit codes, timeouts, partial responses, and retries.
- Platform-specific CI for every supported host.

Do not execute deployment scripts merely to test parsing. Tests must isolate side effects or use disposable targets.
