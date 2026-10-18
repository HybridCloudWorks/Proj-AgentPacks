# Worked example: a customer renewal call

Synthetic scenario; the customer, figures and pages are invented.

Request: "Prep for Thursday's renewal call with Northwind: an internal pre-read for the account team and an agenda we can send them."

1. Frame. Purpose: agree renewal scope. Sixty minutes, 14:00 Europe/London. Attendees: two from the account team, three from the customer. Documents go in the Meetings database.
2. Context. notion-meeting-materials searches for the customer and finds the account page, last quarter's review notes, an open support escalation and a pricing guidance page. The agent fetches all four and notes that the account page was last edited five months ago.
3. Pre-read. Titled "INTERNAL - Northwind renewal pre-read - 2026-10-22" and opening with "Internal only. Do not forward to external participants." It covers usage trends and the escalation with citations, the pricing position from the guidance page, options for the renewal, and questions to agree internally. A short section of general negotiation practice is labeled as general knowledge. The stale account page is flagged.
4. Agenda. Objective, five timed items totalling 55 minutes plus five for next steps, decisions needed, an empty action-items section, and resources the customer can open. It contains no pricing position, no assessment of the customer, and no mention of the pre-read.
5. Linking. The pre-read links to the agenda. The agenda does not link to or name the pre-read, because its title would leak to the customer.
6. Check. The pre-publication check on the agenda finds one problem: a line copied from the review notes reading "internal only: renewal at risk". The agent removes it. Because this is an external, commercially sensitive meeting, it asks notion-governance-reviewer to review the agenda; the reviewer finds nothing blocking and notes that it cannot see who the Meetings database is shared with.
7. Write. Both pages are created in the Meetings database with Date and Type set. The Attendees person property is left empty because setting it notifies people and the user did not ask for that.
8. Verify. Both pages fetched; titles, properties and the one-way link confirmed.

Report: COMPLETE_VERIFIED for creation, with URLs. `permissions_and_sharing_impact`: none changed; sharing the agenda with the customer remains the user's Level 2 decision. `independent_review`: the reviewer's findings and its blind spot on database sharing.
