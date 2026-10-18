# Re-review reconciliation

The record that the `review-infrastructure-pr` Skill's Re-review rules require on a new push: rebuild the ledger against the new head, verify earlier findings against the code rather than resolved conversations, review all newly changed lines, and do not repeat findings whose root cause is fixed. Summarize it in the report's Coverage and Evidence section.

## Revisions

- Base SHA:
- Previously reviewed head:
- New head:
- Ledger rebuilt for: <full PR diff base...new head>
- Lines changed since the previous review: <n added, n deleted>

## Earlier findings and gaps

Status values: fixed, partially fixed, not fixed, superseded (the code it anchored to no longer exists and the root cause is gone or moved).

| ID | Previous severity | Status at new head | Evidence at new head | Carried forward as |
|---|---|---|---|---|
| F-01 | | | `<path>:<line>`, or the regenerated artifact and its commit | closed, F-01 (unchanged ID), or new ID if the root cause changed |

An author reply, a resolved conversation or a green pipeline is not evidence on its own. Cite the code or the regenerated artifact.

## Evidence regenerated

| Artifact | Previous commit | New commit | Still valid? |
|---|---|---|---|
| | | | evidence from an older commit, other inputs or another target no longer counts |

## Newly changed lines

| Location | Introduced by | Disposition |
|---|---|---|
| | fix for F-nn, or unrelated change | verified, finding, evidence gap, not applicable |

## Result

- Open findings carried forward:
- New findings:
- Disposition at the new head:
