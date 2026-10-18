# Tool and permission matrix

| Agent | Read/search | Edit | Execute | Browser/network/MCP/Azure/GitHub | Deploy/communication |
|---|---|---|---|---|---|
| Primary | Authorized repo | Scoped product/tests/docs | Reviewed local checks | Exact tools enabled only after target/data/authority are known | Only explicitly authorized exact action |
| Security | Assigned files/evidence | None | None | No direct connectors | None |
| Tests | Assigned files/callers | Tests and fixtures | Isolated reviewed test commands | Approved test target through primary or scoped grant | None |
| Performance | Assigned code/measurements | None | Bounded isolated profiler | Shared/paid runs through explicit approval | None |
| Evaluation | Assigned tool/prompt/fixtures | Eval assets | Local deterministic evaluator | Approved model judge or MCP fixture target only | None |

## Tool contracts

- Read/search: needed for discovery and evidence; allowed authorized repository paths, prohibited secrets/out-of-scope data access. Side effect Level 0; record material paths/evidence, avoid dumping confidential source.
- Edit: needed for scoped implementation/test work; Level 1 in approved workspace. Preserve user changes; public breaking or substantial overwrites require Level 2. Audit final diff.
- Execute: needed for test/build/profile/eval evidence; Level 1 only for reviewed local bounded commands. Shell access bypasses simple file-tool restrictions; use host sandbox/network/identity policy. Record command, environment, exit code and sanitized result.
- Browser: needed for real web-flow behavior; identify domain/account/test data, isolate state and redact artifacts. Production/consequential/upload actions require Level 2. Audit actual assertions and cleanup.
- Network/docs: needed for exact-version authoritative knowledge; no source upload or secrets in queries. Private/external data submission requires Level 2. Record source URL/version/check date.
- MCP: needed only for a documented adapter contract; precise tool identifiers, schemas, identity/data scope and effects. No wildcard third-party grants. Server-side authz and approval apply; audit tool name/status/correlation with redacted arguments.
- Azure/GitHub: distinguish read versus control/data-plane mutation. Exact subscription/repository/resource must be verified. Deployment, permissions, PR writes, merge and releases require Level 2. No live connector is assumed.
- Deployment/communication: absent from default profiles. Add only explicit scoped tools for a user-authorized workflow, with exact target, data, cost, result and recovery evidence.

Copilot primary delegation uses the supported agent alias. Generic test/browser/mcp labels are not valid portable capability grants. Codex inherits parent session security; Claude/Gemini mappings are documented in compatibility metadata.
