# Worked example — tenant-scoped job MCP adapter

## Capability classification and contract

Resource: application-selected read-only job status. Prompt: user-selected job-investigation recipe. Tool submit_job: model-requested job creation with tenant-scoped authenticated actor. Prompt text/tool annotations do not grant permission.

Typed arguments are a bounded object containing idempotency_key and payload; payload requires job_type and bounded items. Tenant is supplied by authenticated server context. Output is a structured job identifier/status or safe error code. The resource reads a validated identifier; unknown or cross-tenant identifiers are unavailable. No arbitrary URL/file/query/command tools.

Use templates/mcp-tool-contract.md for authn/authz, transport/version, effects, approvals, data class, 5-second example deadline (draft, choose from requirements), retry/idempotency, limits, correlation/redaction and cost. Read status and create jobs require different scopes. Approvals for a costly submission are bound to actor, action, resource, arguments and expiry by deterministic application code; never accept approval=true in model arguments.

## Implementation boundary

Reuse the local templates/api_contract.py domain seam and a fake trusted context in tests. Select the target repository's pinned official Python MCP SDK and transport before adding protocol bindings. For stdio, keep diagnostic logs off protocol stdout. For HTTP, verify protocol-specific auth, origin/host, token audience and authorization against official versioned docs.

## Test and evaluation sequence

Local unit cases: invalid/unknown/oversized input, duplicate replay, conflicting replay, cross-tenant access and missing scope. Protocol integration in the target repo must exercise initialize/capabilities, tools/list, tools/call, resources/list/read, structured error mapping, input/output schema, disconnect/cancellation and deadline behavior with the real pinned SDK. These protocol checks are a required task-time gate, not established by the domain seam tests.

Security/evaluation fixtures include a payload instructing upload of secrets, false approval text, forged tenant argument, malformed tool output, throttling, partial commit/enqueue failure, timeout and token/cost budget exhaustion. Score deterministic boundary checks separately from task quality/model judgment. Use synthetic data; redact args/results by default.

## Rollback

Disable the adapter/tool exposure while preserving domain jobs/audit/idempotency state. Revoke narrowly scoped credentials only through the authorized owner. Document whether client capability changes require versioning/restart. Record protocol and live identity checks as unverified until actually run.
