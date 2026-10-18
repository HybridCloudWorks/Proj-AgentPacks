# Changed-line coverage ledger

The internal ledger that the `review-infrastructure-pr` Skill builds before writing any finding (workflow step 2 and `references/review-protocol.md` section 2). Start from the output of `scripts/change_manifest.py --base <base> --head <head> --format markdown`; build the same rows by hand from the full diff when the script cannot run.

The ledger is working material. Summarize it in the report's Coverage and Evidence section; do not paste it into review comments.

## Header

- Repository:
- Base SHA:
- Head SHA:
- Manifest source: <change_manifest.py output, or "hand-built from diff">
- Changed files: <n>   Added lines: <n>   Deleted lines: <n>

## Rows

One row per added or deleted line. Group adjacent lines only when they form one inseparable expression, object, task or command.

| # | Location | Semantic change | Technology | Upstream inputs | Downstream effects | Target | Ownership (before → after) | Lifecycle effect | Failure modes | Evidence | Disposition |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `<path>:<old or new line>` | | | | | | | create, update, replace, delete, adopt, detach, move, restart or no-op | null, empty, malformed, duplicate, partial, retry, cancel, concurrent | | verified, finding F-nn, evidence gap, not applicable |

## File-level changes without textual lines

| Path | Change | What it can alter | Disposition |
|---|---|---|---|
| | rename, mode change or binary | resource identity, state address, include path, executable bit, artifact provenance | |

## Closing checks

- [ ] Every row has a disposition. A file that parsed, or a neighboring block that was reviewed, does not cover a line.
- [ ] Every deletion names the control, check, permission or guarantee it removes, and whether another line replaces it.
- [ ] Every rename states whether it changes only source layout or also a deployed identity.
- [ ] Every generated artifact is explained by a source change and is the one the pipeline consumes.
- [ ] Inspected / total is the number reported in Coverage and Evidence.
