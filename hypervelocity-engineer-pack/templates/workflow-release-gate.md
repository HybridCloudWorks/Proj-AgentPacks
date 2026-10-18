# Workflow release gate

Produced by `workflow-lifecycle-and-release` before a GitHub Agentic Workflow is called production-ready. A workflow that compiles is not ready until every gate is done or explicitly accepted by its owner.

| Item | Value |
|---|---|
| Workflow | |
| Source | `.github/workflows/<name>.md` |
| Generated artifact | `.github/workflows/<name>.lock.yml` |
| Commit | |
| gh-aw extension version | <from `gh extension list`> |
| Repository overlay applied | <`.github/aw/instructions.md` or none> |

## Gates

Status is one of: done, not done (reason), accepted by owner (name), not applicable.

| Gate | Evidence | Status |
|---|---|---|
| Source reviewed | | |
| Generated lock reviewed; no broadened permissions or added tools | | |
| Least-privilege `permissions` | | |
| Safe outputs reviewed: allowlists, maximum counts, sanitization | | |
| Secrets only through the secret mechanism | | |
| Network and MCP allowlists declared | | |
| Runner choice reviewed | | |
| Actions and external references pinned where policy requires | | |
| `gh aw compile` and `gh aw validate` pass | | |
| Representative validation: authorized live run observed through `gh aw logs` | | |
| Rollback or disable instructions written | | |
| Explicit owner for live execution | | |

## Disable and rollback

- Disable: `gh workflow disable <name>.lock.yml`
- Rollback: revert the source and lock pair in one change, then recompile and confirm the lock matches.

## Not established by this gate

<anything verified only structurally, such as behavior on triggers that were not exercised>
