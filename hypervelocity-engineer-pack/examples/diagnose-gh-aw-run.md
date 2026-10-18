# Worked example: digest workflow that stopped producing output

Prompt: `.apm/prompts/diagnose-gh-aw-run.prompt.md`. Skills applied: `agentic-workflows`, `workflow-observability-and-evaluation`, `workflow-lifecycle-and-release`, `agent-governance-and-guardrails`. Repository, run IDs, commits and figures are illustrative.

## Request

> `weekly-pr-digest` hasn't created its digest issue for two weeks. Run 9123456789 is the latest. Find out why, and fix it if the fix is small. You can trigger one manual run to confirm.

Authorized: read logs and audit data, edit the workflow locally, one confirming `gh aw run`. Not yet authorized: push or pull request (asked for in step 5).

## 1. Route

`agentic-workflows` selects the debug and audit route. The identity check applies: this is `gh aw`, not the Copilot CLI. The confirming run uses `gh aw run`, not `gh workflow run`.

## 2. Collect evidence

```text
gh aw logs weekly-pr-digest
gh aw audit 9123456789 --json
```

| Evidence | Value | Label |
|---|---|---|
| Last eight runs | six succeeded up to 2026-09-28; 2026-10-05 and 2026-10-12 failed | observed |
| Failed runs end at | agent step, `timeout-minutes: 15` reached | observed |
| Tool calls in run 9123456789 | 46, of which 29 were denied | observed |
| Denied calls | all `web-fetch` requests to `api.deps.dev`, blocked by the network policy | observed |
| First denial | 2 minutes into the agent step | observed |
| Safe outputs emitted | none (no `create-issue`) | observed |
| Body change | commit `4f1c2e9` (2026-10-01) added "look up each dependency's release notes on deps.dev" | observed in `git log -p` |

Step summaries and the audit JSON are kept with the diagnosis; the final chat answer of the run is not used as evidence.

## 3. Hypotheses

| Hypothesis | Test | Result |
|---|---|---|
| Source and lock drift | `gh aw compile weekly-pr-digest` at `4f1c2e9` produces no lock diff | ruled out |
| Engine credential expired | agent step authenticated and made 46 tool calls | ruled out |
| GitHub API rate limit | no 403 or 429 responses in logs | ruled out |
| Denied fetch retried until timeout | 29 denials to one domain, starting after the body change | confirmed |

Root cause: the body change asks for data from a domain the network policy blocks. The prompt has no stop rule for denied calls, so the agent retried until the timeout. The change compiled cleanly because a compiler cannot know that a sentence in the body needs a new domain.

## 4. Options

`agent-governance-and-guardrails` and the tool-denial rule in `optimize-agentic-workflow` both say to stop the repeated forbidden call, not to widen the policy automatically.

| Option | Change | Governance effect | Decision |
|---|---|---|---|
| A | Remove the deps.dev lookup; link each dependency PR's own release notes instead | narrows behavior | chosen as the small fix |
| B | Add `api.deps.dev` to the network allowlist | widens egress; owner approval needed | offered, not applied |
| C | Deterministic pre-step fetches deps.dev data to a file the agent reads | new egress step; needs review | proposed as follow-up |

Option A also adds one line to the body: "If a tool call is denied, do not retry it; note the missing data in the digest."

## 5. Fix, validate, confirm

```text
gh aw compile weekly-pr-digest
gh aw validate
```

Both exited 0. The lock diff shows no change to permissions, tools, network or safe outputs.

Pushing is an external write, so the agent asked: "The fix is ready locally. May I push branch `fix/digest-denied-fetch` and open a pull request?" The user agreed. Pull request #231 was opened, a maintainer reviewed and merged it, and the agent then used the authorized run:

```text
gh aw run weekly-pr-digest
gh aw logs weekly-pr-digest
gh aw audit 9134567890 --json
```

Run 9134567890 completed in 3 minutes 40 seconds with 11 tool calls, none denied, and created issue #232 "[digest] Week of 2026-10-13".

## Completion report

Outcome: root cause confirmed and fixed; one authorized live run succeeded.

**objective**: Find why `weekly-pr-digest` stopped creating its digest issue and apply a small fix.

**scope-and-authorization**: Log and audit reads, local edits and one `gh aw run` were authorized in the request. Push and pull request were asked for and approved during the task. Option B (wider network allowlist) was not authorized and was not applied.

**actions-and-changed-files**: Edited the body of `.github/workflows/weekly-pr-digest.md` (removed the deps.dev lookup, added a no-retry rule for denied calls). Regenerated `.github/workflows/weekly-pr-digest.lock.yml`. Pushed `fix/digest-denied-fetch` and opened pull request #231, which a maintainer merged. Triggered run 9134567890.

**evidence**:
- Observed: two failed runs ending at the timeout; 29 denied `web-fetch` calls to `api.deps.dev`; the body change in `4f1c2e9`; no lock drift; the confirming run's 11 calls, 0 denials, and issue #232.
- Inferred: the denial loop caused the timeout. The timing and counts support this, but the engine's internal retry reasoning is not visible.
- Unavailable: none material.

**validation**:

| Check | Command | Result |
|---|---|---|
| Compile | `gh aw compile weekly-pr-digest` | passed |
| Validate | `gh aw validate` | passed |
| Lock capability delta | manual diff review | passed: no change |
| Live confirmation | `gh aw run weekly-pr-digest`, then `gh aw audit 9134567890 --json` | passed: issue #232 created, 0 denials |

**risks-and-limitations**: One successful run is a single sample; the next scheduled run on 2026-10-19 is the second. The digest no longer includes deps.dev release notes. Permissions, safe outputs (`create-issue` only), secrets and network are unchanged. Live proof covers one dispatch run, not the schedule trigger.

**next-safe-action**: The owner decides whether option C is worth a reviewed egress step. The agent checks `gh aw logs weekly-pr-digest` after the 2026-10-19 scheduled run if asked.
