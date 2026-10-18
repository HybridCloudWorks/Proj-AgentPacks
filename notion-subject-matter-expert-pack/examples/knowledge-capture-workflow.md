# Worked example: a release-cadence decision captured as a record

Synthetic scenario; the workspace, pages and people are invented.

Request: "We just agreed to move from weekly to fortnightly releases. Write it up as a decision record in Notion with the options we discussed."

1. Extract. From the conversation: the decision (fortnightly releases from the next quarter), the three options discussed (stay weekly, fortnightly, continuous deployment behind flags), the reasons (QA capacity, customer change fatigue), the trade-offs (slower hotfix path), and two follow-ups (update the release checklist, tell support). No decision makers were named.
2. Classify. One decision record. The checklist update is a separate how-to change, noted as a follow-up rather than mixed in.
3. Search. notion-knowledge-curation searches for "release cadence" and "release decision" and finds a Decisions database and an older record, "Decision: weekly releases", status Accepted.
4. Destination. The Decisions database. The agent fetches it: data source identified, properties Decision (title), Status (Proposed, Accepted, Superseded, Rejected), Decided on (date), Decision makers (person), Area (select: Delivery, Product, Platform).
5. Draft. Context, options with benefits and costs, decision, rationale, consequences including the slower hotfix path, follow-through. Decision makers left empty because nobody was named; the draft says so.
6. Approval. Creating the new entry is Level 1: the user asked for it in this database. Changing the old record's status to Superseded edits a page the user did not name, so the agent asks once: "Mark 'Decision: weekly releases' as Superseded and link it to the new record?" The user agrees.
7. Write and verify. The agent creates the entry, updates the old record's status and adds a "Superseded by" link, then fetches both pages and confirms properties, parent and links.
8. Discoverability. The release process hub page would benefit from a link; it was not named, so the agent proposes the edit instead of making it.

Report: COMPLETE_VERIFIED for the two writes, with both URLs; follow-ups list the hub link proposal, the checklist update and the empty decision-makers property; `notifications_and_automations` notes that no people were mentioned and that database automations could not be inspected.
