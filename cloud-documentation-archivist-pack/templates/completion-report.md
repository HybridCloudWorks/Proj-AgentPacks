# Documentation completion report

- Recommendation: [DOCUMENTATION_READY / REVIEW_REQUIRED / CHANGES_REQUIRED / BLOCKED_ON_SOURCE_OR_OWNER / NOT_VERIFIED]
- Date: YYYY-MM-DD
- Request: [The request in one sentence]
- Workflow: [Prompt or Skills applied]

## Scope and audience

[Reader and the task or decision they need the content for. Document types and Diátaxis mode. Files in scope and explicit exclusions.]

## Source and evidence

| Claim or section | Source (path, URL, or record) | Version or date | Evidence label |
| --- | --- | --- | --- |
| [Claim] | [Source] | [Version or date] | [observed / supplied / inferred / not verified] |

## Content decision

[Mode and template chosen and why. What was created, changed, superseded or left alone. Files changed.]

## Validation

| Check | Method or command | Result | Notes |
| --- | --- | --- | --- |
| [Check] | [Tool, command, or manual] | [passed / failed / skipped / not run] | [Reason when skipped or not run] |

### Findings

| id | severity | source | impact | remediation | verification |
| --- | --- | --- | --- | --- | --- |
| [F1] | [High / Medium / Low] | [file:line or record] | [Reader or system impact] | [Fix and who makes it] | [How the fix will be confirmed] |

Delete the findings table when there are none, and say so in one line.

## Limitations

[Everything not verified, assumptions, unresolved source conflicts, renderer differences, and external actions that were not taken.]

## Ownership and next review

- Owner: [Accountable person or team]
- Reviewer or decider: [Who must act next]
- Document status: [Draft / Proposed / Active / Deprecated]
- Next review: [YYYY-MM-DD or the event that triggers review]
- Handoff: [Decision or action requested, or "None"]

---

Choosing the recommendation:

- DOCUMENTATION_READY: content is complete, local checks ran and passed, every claim is traced, and an owner and next review are set. Any remaining limits are stated and do not affect the correctness of the content.
- REVIEW_REQUIRED: content is complete and locally valid but needs a named person to accept, approve or confirm it before use.
- CHANGES_REQUIRED: a review found defects that must be fixed before the documents can be relied on.
- BLOCKED_ON_SOURCE_OR_OWNER: work cannot finish because an authoritative source, owner, destination or authorization is missing.
- NOT_VERIFIED: content exists, but key claims or procedures could not be checked against their source or a live system.

Never record an unexecuted check as passed.
