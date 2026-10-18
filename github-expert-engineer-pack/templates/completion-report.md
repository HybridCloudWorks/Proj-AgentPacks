# GitHub completion report template

Every workflow in this pack ends with this report. The always-on `github-expert-engineer-contract` instruction defines the required sections, finding fields, recommendation values and redaction rule; this template lays them out.

## Guidance (delete this section from the finished report)

**Recommendation values.** Pick exactly one. The post-review check (`hooks/post-github-review.sh` or `.ps1`, which runs `tooling/validate_github_review.py`) fails a report that contains none of these values or more than one, wherever they appear.

| Value | Use when |
|---|---|
| READY_FOR_REVIEW | A local deliverable (patch, plan, triage proposal, design) is complete and ready for a human reviewer. Nothing was applied live. |
| READY_FOR_MERGE_REVIEW | A pull request has no confirmed finding left and every required gate is evidenced on the current head SHA. A human makes the merge decision. |
| CHANGES_REQUIRED | At least one confirmed finding must be fixed before the work goes further. |
| BLOCKED_ON_HUMAN_DECISION | The next step is a live change, an exception or a trade-off that only a named owner can authorize. |
| NOT_VERIFIED | Evidence the decision depends on could not be obtained, so no positive or negative conclusion is safe. |

**Evidence labels.** CONFIRMED means observed directly. INFERRED means it follows from confirmed evidence. HYPOTHESIS means plausible and untested. Anything you could not observe goes under Skipped checks. Write "not verified" in lowercase there, because the uppercase form is also a recommendation value and the checker counts it.

**Severity.** Critical, High, Medium or Low. Record exploitability or reachability in the impact field, not by raising the severity.

**Finding IDs.** Use `GH-n` for general platform findings, `ACT-n` for Actions, `SEC-n` for security, and `FIND-n` if none fits. Write each ID once only, in its finding heading. The checker counts every occurrence of these prefixes as a separate ID, so a cross-reference such as "see GH-1" in the rationale fails it as a duplicate; refer to other findings by their title instead.

**Redaction.** Before saving, remove tokens (`ghp_`, `github_pat_`, `ghs_` prefixes and similar), passwords, private keys, webhook secrets, cookies, signed URLs, and any credential-like value. Refer to a secret by its name and owner, never by its value. Copy log lines only after redaction.

**Honesty.** Never describe an unexecuted check as passed. A green run, an AI review or a YAML block is evidence of what it is, nothing more.

---

# <What was reviewed, in one line>

## Scope

- Host: <github.com | GHE.com | GHES version>
- Repository or organization: <owner/repo>
- Object: <PR number with base and head SHAs | run ID | ruleset ID | tag | environment>
- Actor and access observed: <login, token type, permissions the responses showed>
- Requested outcome: <review | diagnosis | hardening | assessment | change plan | audit>
- Authorized actions: <read-only | local edits | the named live change>
- Out of scope: <what was deliberately not examined>

## Evidence

| Label | Statement | Source (command, endpoint, file:line) |
|---|---|---|
| CONFIRMED | <observed fact> | <`gh pr view 123 --json headRefOid` or `path/to/file:42`> |
| INFERRED | <conclusion drawn from confirmed facts> | <which facts> |
| HYPOTHESIS | <untested explanation> | <test that would settle it> |

## Findings

### <GH-1> · <Severity> · <one-line title>

- evidence: <file:line, API field, run or job ID, redacted log excerpt>
- impact: <what goes wrong, for whom, under which condition>
- remediation: <smallest safe change, and who applies it>
- verification: <how to prove the fix, and whether that check was run>

<Repeat per finding. Write "No confirmed findings." when there are none.>

### Advisory (not findings)

- <AI reviewer or tool suggestion, its source, and why it is advisory>

## Skipped checks

- <check>: <why it was skipped (no access, not authorized, tool unavailable, out of scope)>; <the evidence that would close it, and who can provide it>

## Recommendation

<ONE value from the table above>

- Rationale: <one or two sentences tied to the findings and skipped checks>
- Owner: <team or role that acts next>
- Next safe action: <the single next step, with any command previewed but not run>
