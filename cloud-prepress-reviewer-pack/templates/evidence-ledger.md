# Evidence ledger: <change title>

The detailed evidence record that azure-evidence-and-mcp-review keeps for drift-prone or gate-deciding claims. Summarize it in the report's evidence ledger section; keep this full ledger beside the report when a claim depends on a version, an API, a limit, a policy effect or a retrieved document.

## Labels

Use exactly one label per row.

| Label | Use it when |
|---|---|
| observed | Seen directly in the diff, a repository file, or local tool output at the reviewed commit. |
| inferred | Reasoned from observed evidence, but not itself observed. |
| designed | Stated in a design, plan, runbook or ADR; not executed or rehearsed. |
| structurally-validated | A local static check ran and passed: build, compile, format, validate, lint, schema. |
| preview-verified | Shown by a captured what-if, plan or azd preview at the reviewed commit and intended scope. |
| live-read-verified | Returned by an authorized read-only query of live state, at a named scope and time. |
| accepted-risk | A named owner accepted the risk, with scope and expiry recorded. |
| not-verified | Needed for the conclusion but not obtained. Say what would obtain it. |

A source document does not prove the repository follows it. A static review does not prove live policy compliance. A preview does not prove a deployment succeeded.

## Ledger

| # | Claim | Label | Source | Retrieved or captured | Scope | Version or API | Confidence |
|---|---|---|---|---|---|---|---|
| E1 | <the specific claim the review relies on> | <label> | <file and line, command, CI run, or document title> | <date and time, or commit> | <tenant, subscription, scope, or repository path> | <tool, provider, API or document version> | <high, medium, low, with reason> |

## Live and MCP queries

Record every live read-only query, or record that none ran.

| Query | Tool | Authorized by | Scope | Time | Result summary |
|---|---|---|---|---|---|
| <what was asked> | <Azure MCP tool or CLI command> | <person, and where they said so> | <exact scope> | <time> | <summary, with identifiers redacted where sensitive> |

No natural-language convenience may widen the scope beyond what was authorized, cross a tenant or subscription boundary, or read secret values.
