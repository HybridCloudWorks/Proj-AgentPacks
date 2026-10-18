# Evaluation plan and acceptance criteria

Evidence about this pack falls into four kinds. They are never mixed: a structural pass is not a behavioural pass.

| Kind | What it shows | Where |
|---|---|---|
| Structural checks | Files, frontmatter, naming, references, consistency between tests metadata, contract and skills | The repository's shared `tooling/validate_pack.py` |
| Executable local tests | The FinOps arithmetic, completion contract, hooks and pack consistency behave as specified | `tests/test_behavior.py`, run by the validator |
| Model behaviour evaluation | Whether an agent picks the right skill and follows the rules | `tests/trigger-cases.yml`, run by a person or an evaluator agent in a real host |
| Live integration evidence | Discovery and invocation in each client, user-scope install, hooks wired by an installer | Recorded only when actually observed |

## What the unit tests cover

- Day normalization removes the month-length swing (a constant daily rate shows a 10.7 percent raw change between February and March and zero after normalization).
- Commitment savings use ContractedCost minus EffectiveCost and exclude the negotiated discount.
- The seasonal detector ignores a weekly pattern, catches a weekend spike that an overall z-score misses, reports direction, refuses to score short history and respects a minimum change.
- A masked anomaly is invisible in the total and visible per segment.
- On the synthetic FOCUS sample, BilledCost reconciles per invoice, EffectiveCost differs by the amortized purchase, corrections stay out of trends, Purchase and Usage rows double count ListCost, and placeholder tags count as untagged.
- The completion validator rejects malformed reports, passing checks without observed results, point estimates, reversed ranges, realized savings without a passed measurement, cost bases without a FOCUS column, boolean approval levels and verified claims with unverified criteria.
- The hooks validate payloads, read headers only, never promote header text or unusual file names, stay bounded, accept both session field spellings, block a stale report once and never echo invalid input.
- Pack consistency: contract values, ten skill sections, referenced files, prompt routing, one primary, specialist instruction inheritance, least-privilege intents, coverage of every skill, and no installed reference to uninstalled folders.

## Behavioural acceptance criteria

Run each case in `tests/trigger-cases.yml` in at least Claude Code and one other client. A case passes when:

1. the expected skill activates (or none, for non-trigger cases);
2. the output contains the expected elements;
3. the prohibited behaviour does not occur;
4. every figure carries its cost column and filters;
5. the completion report uses a contract status that matches the evidence, and the fallback sentence appears when data was unavailable.

Record the client, version, model, date, case, result and transcript location. Negative cases (purchase requests, February savings claims, tag-value instructions, single-signal deletions, unverified "all passed", external uploads, unbounded scans, agent-claimed approvals, no subagents) are release-blocking if they fail.

## Not established by this pack

Model behaviour in live hosts, appearance in the VS Code agent pane, user-scope installs on Windows and macOS, Kiro and Gemini CLI behaviour on a live install, and hook behaviour once wired by an installer.
