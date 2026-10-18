# Tool and Permission Matrix

| Capability | Default use | Allowed without additional approval | Approval required |
|---|---|---|---|
| Read/search repository | Discover facts and evidence | Yes, within approved workspace | No |
| Local non-destructive commands | Typecheck, lint, tests, inventory, pack validation | Yes, when isolated and expected | Shared or costly environment |
| Edit local files | Implement scoped changes and reports | Yes, in approved workspace | Substantial overwrite or destructive deletion |
| Web search/fetch | Verify official current docs | Yes, with source attribution | Uploading source or private data |
| GitHub/MCP read | Inspect issues, PRs, checks, metadata | Yes when authenticated scope is already approved | Broad/unclear access or external upload |
| Git commit | Local checkpoint | Follow user/repository authorization | If policy requires approval |
| Push, merge, approve, release, dispatch | External delivery mutation | No | Yes |
| Cloud deploy/apply or IAM change | Shared or production mutation | No | Yes |
| Install package, MCP server, skill, executable | Supply-chain mutation | No for unverified artifacts | Yes |
| Send message, ticket, email, publish | External communication | No | Yes |

Command guard tools are deny-by-default for known delivery and destructive commands. They do not replace host permissions or human review.
