# Worked example: pre-review inventory and post-review report validation

Prompt: `.apm/prompts/validate-review-report.prompt.md`, wrapped around `.apm/prompts/review-before-pr.prompt.md`. Outcome: `READY_FOR_PR`.

Skills applied: review-hooks-and-automation, cloud-prepress-orchestration, change-scope-and-impact, code-defect-and-quality-review, tests-build-and-dependency-review, documentation-inputs-and-repository-contracts, review-report-and-pr-gate.

The repository and paths are fictional. `$PACK_HOME` stands for the folder where the installer placed the pack's helper scripts; APM itself does not deploy them.

## Request

> Review `fix/csv-formula-escape` before I open the PR. Run the pre-review inventory first and validate the report before you hand it over. Put the report in `../reviews/billing-exports/fix-csv-formula-escape/`.

## 1. Pre-review inventory (review-hooks-and-automation)

```text
$ bash "$PACK_HOME/hooks/pre-review.sh" . ../reviews/billing-exports/fix-csv-formula-escape/inventory.json
Cloud Pre-Press pre-review inventory: .
Read-only: no Azure, deployment, state, policy, identity, or PR mutation.
{
  "repository": "/home/dev/src/billing-exports",
  "status_entries": [],
  "changed_files": [],
  "risk_flags": [],
  "available_tools": {
    "git": true,
    "az": false,
    "azd": false,
    "terraform": false,
    "bicep": false,
    "docker": true
  },
  "mutation_performed": false
}
```

The inventory found no changed files. That does not mean the branch is empty. The helper compares the working tree with `HEAD`, and this branch is committed with a clean tree. The reviewer records the gap and resolves the actual diff against the base, as change-scope-and-impact requires:

```text
$ git diff --name-status main...fix/csv-formula-escape
M       CHANGELOG.md
M       src/exports/csv_writer.py
M       tests/test_csv_writer.py
```

The report states the inventory's result and why it differs, instead of quietly replacing it.

## 2. Review the change

The fix neutralizes spreadsheet formula injection in invoice exports:

```python
 8  _FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")
 9  _TEXT_COLUMNS = ("customer_name", "memo", "reference")
...
12  def _neutralize(value: str) -> str:
13      """Prefix an apostrophe so spreadsheet apps treat the cell as text, not a formula."""
14      return "'" + value if value.startswith(_FORMULA_PREFIXES) else value
...
34      for row in rows:
35          record = row.as_dict()
36          for column in _TEXT_COLUMNS:
37              record[column] = _neutralize(record[column])
38          writer.writerow(record)
```

The reviewer traces the cases that commonly break such a fix:

- **Empty or missing values.** `InvoiceRow.as_dict()` in `src/exports/models.py`, unchanged but inspected for this reason, returns `""` for missing text fields, and `"".startswith(...)` is false. No error.
- **Negative amounts.** `amount` is not in `_TEXT_COLUMNS`, so `-12.50` is written unchanged. `test_negative_amount_is_not_prefixed` asserts it.
- **Prefix coverage.** The six prefixes match the characters spreadsheet apps treat as formula starts, including tab and carriage return.

One gap concerns consumers, not code. The `README.md` names the finance reconciliation importer as a consumer of this export. A memo such as `-refund` now arrives as `'-refund`, and `CHANGELOG.md` does not say so. Under documentation-inputs-and-repository-contracts that is a finding, because it changes how a consumer must parse the file. It is Low and does not block the PR.

```text
$ python -m pytest -q
..................                                           [100%]
18 passed in 0.61s
$ ruff check .
All checks passed!
```

## 3. Post-review validation, first attempt

The reviewer writes the report and runs the post-review helper:

```text
$ bash "$PACK_HOME/hooks/post-review.sh" ../reviews/billing-exports/fix-csv-formula-escape/REVIEW.md
Cloud Pre-Press post-review report validation: ../reviews/billing-exports/fix-csv-formula-escape/REVIEW.md
FAIL: expected exactly one recommendation, found: ['READY_FOR_PR', 'READY_FOR_DEPLOYMENT_REVIEW']
FAIL: duplicate finding ID
$ echo $?
1
```

The order of the listed values can vary between runs. Two sentences in the draft caused both failures:

- The handoff said "Address F1 in a follow-up", which repeats the ID already in the findings table.
- The recommendation reason said "Not READY_FOR_DEPLOYMENT_REVIEW: this repository has no deployment step", which names a second recommendation.

The reviewer corrects the report text and leaves the validator alone. The handoff now refers to "the Low changelog finding", and the reason no longer names another recommendation.

## 4. Post-review validation, second attempt

```text
$ bash "$PACK_HOME/hooks/post-review.sh" ../reviews/billing-exports/fix-csv-formula-escape/REVIEW.md
Cloud Pre-Press post-review report validation: ../reviews/billing-exports/fix-csv-formula-escape/REVIEW.md
PASS: ../reviews/billing-exports/fix-csv-formula-escape/REVIEW.md
```

The validator checks five headings, one recommendation, duplicate IDs and secret-like values, and nothing more. Under review-report-and-pr-gate the reviewer then reads the report against the rest of the contract: all twelve sections are present, the single finding carries all nine fields, every evidence row has a contract label, and the skipped checks are listed. The PASS proves the report's shape. It is not evidence that the change is safe.

## Completion report

### Scope and inputs

| Item | Value |
|---|---|
| Repository and refs | `billing-exports`, base `main`, head `fix/csv-formula-escape` at `c81d0e4` |
| Change intent | Neutralize spreadsheet formula injection in invoice CSV exports |
| Change class | application |
| Target environment | Not applicable; no infrastructure in the diff |
| Requirements and design | Work item: exported text cells must not execute as formulas |
| Owner | Change: billing team. Export consumer: finance reconciliation. |
| Authorization boundary | Read-only review. Local `pytest`, `ruff` and the pack's helpers authorized. No live access, no source edits, no pull request actions. |
| Report location | `../reviews/billing-exports/fix-csv-formula-escape/REVIEW.md` |

### Changed paths and methods

| Path | Change class | Review method |
|---|---|---|
| `src/exports/csv_writer.py` | application | Read in full; traced empty, negative-amount and prefix cases |
| `tests/test_csv_writer.py` | tests | Mapped each test to a case; ran the suite |
| `CHANGELOG.md` | documentation | Checked consumer-visible behavior is described |

Paths inspected outside the diff, and why:

- `src/exports/models.py`: what `as_dict()` returns for missing text fields.
- `README.md`: the export's consumers.

### Evidence ledger

| Evidence | Label | Source, command or capture | Bound to |
|---|---|---|---|
| Inventory reported no changed files on a committed branch | observed | `hooks/pre-review.sh`, `inventory.json` | working tree at `c81d0e4` |
| Three changed files | observed | `git diff --name-status main...fix/csv-formula-escape` | `c81d0e4` |
| Unit tests pass | observed | `python -m pytest -q`, exit 0, 18 passed | `c81d0e4` |
| Lint passes | structurally-validated | `ruff check .`, exit 0 | `c81d0e4` |
| Report shape | structurally-validated | `hooks/post-review.sh`, PASS on the second run | this report |
| Behavior in the finance importer | not-verified | Importer is outside this repository | not bound |

### Findings

#### Changelog does not tell export consumers about the apostrophe prefix

| id | severity | status | file | line |
|---|---|---|---|---|
| F1 | Low | confirmed | `CHANGELOG.md` | 7 |

- **scenario:** A memo such as `-refund` is now exported as `'-refund`. The changelog entry says only "Fixed CSV formula injection in invoice exports".
- **impact:** The finance reconciliation importer may store or match the prefixed value without anyone expecting it.
- **recommendation:** Add a sentence naming the affected columns and the leading apostrophe, and tell the importer's owner.
- **verification:** The changelog entry names `customer_name`, `memo` and `reference` and the prefix rule.

### Skipped checks and limits

| Check | Why skipped or limited | Effect on the recommendation |
|---|---|---|
| Inventory changed-file list | The helper compares with `HEAD`; the branch is committed, so it listed nothing | Diff resolved against `main` instead |
| Consumer integration | The finance importer is outside this repository | Consumer handling not verified; covered by the Low finding |

### Architecture and ADR status

No architecture artifact or ADR applies to the export format. Nothing is contradicted.

### Security, IaC, policy and identity status

- The change closes a formula-injection path for the three free-text columns. Numeric columns are untouched.
- No infrastructure, identity, policy or dependency change.

Secret handling: the diff was searched for key, token and connection-string patterns. Nothing matched and nothing was redacted, and no secret value appears in this report.

### Tests, build and preview status

| Check | Command or source | Result | Label |
|---|---|---|---|
| Unit tests | `python -m pytest -q` | exit 0, 18 passed | observed |
| Lint | `ruff check .` | exit 0 | structurally-validated |
| Report validation | `hooks/post-review.sh` | PASS on the second run | structurally-validated |

Preview change counts: no preview; the change contains no infrastructure.

### Operations, rollback, cost and inputs

- Observability and ownership: no change to logging or alerts.
- Rollback boundary: revert the merge. Files already exported with the prefix stay prefixed, so consumers may see both forms. Label: designed.
- Cost: no change.
- New required inputs: none.

### Unresolved risks and human blockers

| Item | Type | Owner | Needed to clear |
|---|---|---|---|
| Importer handling of prefixed values | open risk | finance reconciliation owner | Confirmation, or an importer change |

No human blocker.

### Recommendation

READY_FOR_PR

The fix is correct for the cases traced, it is tested, and nothing blocks it. The only finding is a Low documentation follow-up. This review does not approve or merge the pull request.

### Engineer handoff

- Next actor: the change author, then the pull request approver.
- Actions, in order: add the consumer note for the Low changelog finding; open the pull request with this report attached; tell the finance reconciliation owner about the prefix.
- Evidence the next actor receives: this report, `inventory.json`, and the test and lint output above.
- Re-review trigger: new commits to `src/exports/`.
- Not done by this review: no source edits, no pull request opened, no consumer testing.
