# Container change completion report

Field names match `tests/report-contract.yml`; the binding rules are in the always-on `docker-senior-engineer-contract` instruction. A machine-readable report can be checked with `hooks/post-docker-engineering.sh <report.json>`.

Status: COMPLETE_VERIFIED | IMPLEMENTATION_PREPARED_NOT_VERIFIED | ANALYSIS_ONLY | CHANGES_REQUIRED | BLOCKED_ON_HUMAN_DECISION

Outcome:

| Criterion (id) | Status (passed, failed, unverified) | Evidence level (static, local build, local runtime, scan, live) | Evidence |
|---|---|---|---|
| | | | |

Files changed:

Decisions:

Image impact (base, size before and after, stages, layers):

Runtime contract impact (user and UID, ports, entrypoint and signals, health, writable paths, volumes, environment, resources):

Security review:

Supply chain impact (pins and digests, SBOM, provenance, signatures, scanner and database date):

Platform compatibility (architectures; engine, Buildx and Compose versions; consumers):

Operational impact:

| Check command | Exit code | Status | Environment (context, builder, platform, versions) | Evidence |
|---|---|---|---|---|
| | | | | |

Unverified items:

Remaining risks:

Rollback:

Follow-ups:

COMPLETE_VERIFIED needs at least one criterion, every criterion and check passed with executed evidence, and no unverified item. Otherwise choose the matching status, and when required validation is unavailable end with: "Container change is prepared, but completion is not verified."
