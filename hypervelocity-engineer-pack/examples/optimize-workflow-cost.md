# Worked example: daily issue report over its AI-credit limit

Prompt: `.apm/prompts/optimize-workflow-cost.prompt.md`. Skills applied: `optimize-agentic-workflow`, `prompt-token-efficiency`, `workflow-observability-and-evaluation`, `workflow-lifecycle-and-release`. Repository, run IDs and every figure are illustrative.

## Request

> `daily-issue-report` hit the AI-credit limit again (run 9200000001). Cut the cost, but the report has to stay as useful. You can dispatch it twice to compare.

Authorized: read audit data, edit after the plan is approved, two `gh aw run` dispatches. The workflow posts its report with the `create-discussion` safe output.

## 1. Measure first

```text
gh aw audit 9200000001 --json
```

| Field | Value | Label |
|---|---|---|
| Input tokens | 1,284,000 | observed |
| Output tokens | 9,800 | observed |
| Cached tokens | 0 | observed |
| Tool calls | 318: `list_issues` 4, `get_issue` 302, other 12 | observed |
| Duration | 21 minutes | observed |
| Outcome | AI-credit limit reached before `create-discussion` on 3 of the last 7 days | observed in `gh aw logs daily-issue-report` |

## 2. Classify cost and name the drivers

| Area | Share of input tokens | Recurring | Basis |
|---|---|---|---|
| Tool interaction: one `get_issue` per open issue (302) | about 78% | daily | inferred from per-call response sizes in the audit |
| Context assembly: full comment threads for every issue | about 15% | daily | inferred from the same |
| Prompt generation: 1,650-token static instructions after the date and data | about 5%, and no cache hits | daily | observed: cached tokens 0 |

Top three drivers: per-issue fetches, full comment threads, and an unstable prompt prefix. All are recurring; none is one-time setup.

## 3. Plan, approved before editing

Format: `templates/optimization-plan.md`.

| # | Change | Driver | Risk |
|---|---|---|---|
| 1 | Deterministic pre-step runs `gh issue list --state open --json number,title,labels,assignees,createdAt,updatedAt --limit 1000` into a file the agent reads | per-issue fetches | truncation if the limit is too low |
| 2 | Agent fetches full detail only for issues updated in the last 24 hours | comment threads | may miss context on older issues |
| 3 | Stable instructions first, date and data last; instructions compressed with `prompt-token-efficiency` | prompt prefix | a lost constraint |

Explicitly unchanged: model, permissions, daily cadence, and the `create-discussion` safe output. The user approved the plan.

`prompt-token-efficiency` kept every constraint: report sections, the 14-day unassigned rule, the instruction to treat issue text as data, and the no-mention rule. It removed a repeated paragraph on formatting and two decorative examples.

## 4. Evaluation contract, fixed before the change

Task set: the same day's open issues, with both versions dispatched within 30 minutes of each other. Acceptance criteria:

1. Lists every issue updated in the last 24 hours.
2. Per-label counts match `gh issue list`.
3. Flags unassigned issues older than 14 days.
4. Cites no issue number that does not exist.
5. Emits `create-discussion` within the run.
6. Adds no permission and no output.

## 5. Change, compile, compare

```text
gh aw compile daily-issue-report
gh aw validate
```

Both exited 0, and the lock diff adds only the pre-step. Baseline run 9200000101 (current `main`) and candidate run 9200000102 (branch `optimize/issue-report`):

| Criterion | Baseline | Candidate 1 |
|---|---|---|
| 1. Every updated issue listed | met | **failed: 3 missing** |
| 2 to 6 | met | met |

The candidate was cheaper and wrong. The pre-step had been written with `--limit 200`, and the repository has 302 open issues, so the list was truncated. Fewer tokens is not better quality, so the change was revised rather than accepted. The limit was raised to 1000, and the pre-step now fails visibly when the returned count equals the limit. After a recompile, the user authorized one more dispatch (run 9200000103):

| Metric | Baseline 9200000101 | Candidate 2 9200000103 | Label |
|---|---|---|---|
| Criteria met | 6 of 6 | 6 of 6 | observed |
| Input tokens | 1,279,000 | 231,000 | observed |
| Cached tokens | 0 | 1,900 | observed |
| Tool calls | 316 | 21 | observed |
| Duration | 20 minutes | 4.5 minutes | observed |
| Input tokens over seven daily runs | about 8.95 million | about 1.62 million (82% lower) | projected from one pair |

## Completion report

Outcome: cost reduced on one comparable pair with equivalent quality; sustained savings are projected, not yet observed.

**objective**: Bring `daily-issue-report` under its AI-credit limit without making the report less useful.

**scope-and-authorization**: Audit reads, edits after plan approval, and two dispatches were authorized. A third dispatch was asked for and approved after candidate 1 failed. Model, permissions, cadence and safe outputs were not changed.

**actions-and-changed-files**: Edited `.github/workflows/daily-issue-report.md` (added the pre-step, narrowed detail fetches, reordered and compressed instructions). Regenerated `.github/workflows/daily-issue-report.lock.yml`. Runs 9200000101, 9200000102 and 9200000103 dispatched on `main` and `optimize/issue-report`.

**evidence**:
- Observed: baseline audit fields; candidate 1 missing three issues; candidate 2 meeting all six criteria with the token, call and duration figures above.
- Inferred: per-area cost shares, derived from per-call response sizes.
- Unavailable: variance across days; a single pair cannot show it.

**validation**:

| Check | Command or method | Result |
|---|---|---|
| Compile | `gh aw compile daily-issue-report` | passed |
| Validate | `gh aw validate` | passed |
| Acceptance criteria, candidate 1 | criteria 1 to 6 against `gh issue list` | failed: criterion 1 |
| Acceptance criteria, candidate 2 | same | passed: 6 of 6 |
| Lock capability delta | manual diff review | passed: pre-step only |

**risks-and-limitations**: One comparable pair is a small sample. The pre-step's truncation guard stops the run instead of producing a partial report, which is intentional. Permissions are unchanged; the pre-step uses the existing read token. Safe output is still `create-discussion` only. No new secrets or network destinations.

**next-safe-action**: The user reviews and merges `optimize/issue-report`. Then compare seven scheduled runs with `gh aw audit` before treating the savings as achieved. Rollback: revert the source and lock pair together.
