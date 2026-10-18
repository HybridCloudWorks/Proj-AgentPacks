# Evidence record

The result that the `verify-infrastructure-evidence` Skill returns to `review-infrastructure-pr` (its Output Contract). One record per review. It feeds the report's Coverage and Evidence and Evidence Gaps sections; it does not create findings by itself.

## Environment

- Repository root:
- Head SHA checked out:
- Downloads permitted: <no (default) | yes, granted by the user for: ...>
- Tools available: <name and version for each tool the checks used>
- Host limits: <no cloud credentials, no cluster access, no network, and so on>

## Checks executed

Result values follow `references/evidence-matrix.md`: pass, fail, skip, not applicable.

| Check | Class | Command | Tool version | Scope | Result | What the result establishes |
|---|---|---|---|---|---|---|
| | local static, dependency-resolving, remote read, target simulation | | | files or directories | | the narrow claim only, such as "parses" or "compiles" |

## Checks skipped

| Check | Exact reason | What remains unverified |
|---|---|---|
| | tool not installed, download not permitted, would contact a target, would execute untrusted code | |

## Artifact integrity

One row per plan, what-if, render, check-mode diff, test result or CI log the author supplied.

| Artifact | Commit | Inputs and parameters | Target and scope | Identity | State, inventory or lock | Tool version | Consumed by deployment? | Integrity verdict |
|---|---|---|---|---|---|---|---|---|
| | matches head? | | | | | | same artifact, or rebuilt? | valid evidence, stale, wrong target, unverifiable |

## Material gaps

For each gap, the precise artifact needed: what it is, which commit, inputs, target and identity it must use, and which risk it clears.

## Limitations

What these checks cannot establish for this change: lifecycle, authorization, target correctness, existing-environment behavior, admission or runtime behavior.
