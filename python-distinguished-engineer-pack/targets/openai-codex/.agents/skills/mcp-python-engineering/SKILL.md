---
name: mcp-python-engineering
description: Implement and review Python MCP servers/clients with protocol, transport, schema, identity and tool boundaries. Use when python MCP resource, prompt, tool, transport, protocol test or supply-chain review is requested.
---

# Mcp Python Engineering

## Activation and scope

Python MCP resource, prompt, tool, transport, protocol test or supply-chain review is requested. Do not claim tool annotations or prompt instructions enforce permissions; never auto-register a remote service.

## Inputs and dependencies

- Inputs: Pinned MCP/SDK versions, consumers, transport, identity/tenancy, operations and data classification.
- Dependencies: Approved SDK/docs for exact version and local protocol-test harness.
- Owner: the primary Python Distinguished Engineer; use a specialist only when its isolated evidence helps the task.

## Workflow

1. Classify application-selected resources, user-selected prompts and model-invoked tools. Specify input/output schemas, bounds, effects, idempotency, timeout/retry policy, cost and audit needs for every tool.
2. Separate protocol/transport from domain adapters. Keep stdio logs off protocol stdout; for remote transports validate current auth, origin/host protections, token audience and per-tool authorization.
3. Validate arguments independently of model intent. Resolve tenant/resource scope from authenticated context, not supplied claims; distinguish read and consequential operations and enforce approval outside the model.
4. Test initialization/capability negotiation, list/call/read flows, malformed arguments, unauthorized resource, timeout/cancellation, structured errors, injection, tool abuse and oversized results. Pin and review third-party servers before connecting.

## Output and validation

Protocol contract and implementation/test evidence, authz matrix, redaction/telemetry and rollback plan. Record exact checks run, observed failures and unavailable evidence. A draft, static check or local mock does not establish live behavior.

## Failure and guardrails

SDK/protocol mismatch, arbitrary file/URL/query tool, unapproved server, missing authz or protocol contamination. Preserve existing user work; stop only the dependent operation when a material input or required approval is missing, and continue useful authorized work. A specialist cannot self-approve or expand the assignment.

## Workflow connection

Within the complete pack, the optional `build-mcp-server.prompt.md` recipe connects this Skill to the primary workflow. This Skill is self-contained when installed individually; no external prompt or specialist is required. Consult shared instruction, handoff and completion contracts when the full pack is available.
