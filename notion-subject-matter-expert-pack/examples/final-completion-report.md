# Worked completion report

Synthetic report for the knowledge-capture example. Field names follow `tests/report-contract.yml`.

Status: COMPLETE_VERIFIED

Outcome: the fortnightly release decision is recorded in the Decisions database and the previous weekly-release decision is marked superseded.

| Criterion | Status | Evidence |
|---|---|---|
| Decision record has context, options, decision, rationale and consequences | passed | Fetched page shows all five sections |
| Properties use existing schema values | passed | Fetched entry: Status Accepted, Area Delivery |
| Previous decision linked and superseded | passed | Fetched old record: Status Superseded, link to the new record |

| Action | Target | Location | URL |
|---|---|---|---|
| created | Decision: move to fortnightly releases | Decisions database | (page URL from the create result) |
| updated | Decision: weekly releases | Decisions database | (page URL from the fetch result) |

- Placement and links: both records in the Decisions database, linked to each other; release process hub link proposed, not made.
- Sources: this conversation (2026-10-18); the earlier decision record.
- Decisions: decision makers left empty because none were named.
- Permissions and sharing impact: none; both pages inherit the database's sharing.
- Schema impact: none.
- Data sensitivity: internal; no personal data or credentials.
- Notifications and automations: no mentions or person properties set; database automations could not be inspected through the connector.
- Checks: fetch of both pages, passed; pre-publication draft check (command, exit code 0), passed.
- Independent review: not requested; internal records in an existing database.
- Unverified: none.
- Remaining risks: an automation on the database could have notified followers; the user was told.
- Rollback: move the new record to Trash and restore the old record's status from page history.
- Follow-ups: hub link, release checklist update, decision makers.

Had the connector been unavailable, the same report would carry status PREPARED_NOT_VERIFIED, the drafts, and the sentence: "The Notion work is prepared, but it is not verified in the workspace."
