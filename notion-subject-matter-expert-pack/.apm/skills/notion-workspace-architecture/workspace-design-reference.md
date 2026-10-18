# Workspace design reference

Notion's feature names, permission labels and plan limits change. Confirm them in the current Notion interface or help center for the user's plan before quoting them as fact.

## Organizing patterns

| Pattern | Top level looks like | Works when | Watch for |
|---|---|---|---|
| By team | One teamspace per team, plus a company-wide space | Teams own distinct knowledge and permissions follow teams | Cross-team projects scattered across spaces |
| By function | Handbook, Projects, Docs, Meetings, Decisions | Small organizations, shared ways of working | Permission boundaries that do not match functions |
| By lifecycle | Active, Reference, Archive | Project-heavy work that ends and goes quiet | Reference material buried in old project trees |
| Hybrid | Team spaces holding shared databases, viewed from company hubs | Most growing organizations | Two places claiming to be the source of truth |

Prefer one shared database per kind of record (projects, tasks, decisions, documents, meetings) with linked, filtered views on team pages, over a separate copy per team.

## Hub page outline

1. One sentence on what this area is for and who owns it.
2. Start here: the three to five pages a newcomer needs.
3. Sections by task the reader wants to do, each with links or a linked database view.
4. Recently updated: a linked view sorted by last edited.
5. How to contribute: where new pages go, which template to use, who reviews.

## Naming and tagging

- Titles name the subject and the kind of page: "How to rotate the API signing key", "Decision: adopt quarterly planning", "Billing FAQ".
- Put dates in titles only for dated artifacts (meetings, weekly reports), in ISO order (2026-10-18) so they sort.
- Keep a controlled tag vocabulary of roughly ten to thirty values per database, with an owner. Merge synonyms; retire tags that nobody filters by.
- Avoid encoding status or owner in titles; use properties.

## Permission summary

- Access is inherited from the parent page or teamspace unless a page is shared differently. A move changes what a page inherits.
- Typical page access levels: full access, can edit, can edit content (databases), can comment, can view. Labels and availability vary by plan.
- Members, groups and guests are different principals. Guests on a high page in the tree can see everything under it.
- Public web sharing exposes the page and, depending on settings, its sub-pages to anyone with the link and possibly search engines.
- Integrations and connectors see only the pages that were shared with them, and everything below those pages.

## Lifecycle

- Every hub and every shared database has a named owner.
- Wiki pages can carry verification with an owner and an expiry; use it for policy and procedure pages.
- Review cadence by type: policies and procedures quarterly, reference pages twice a year, project pages at project close.
- Archive by moving to a clearly named archive area or marking a status property, not by deleting. Trash restores are time-limited and depend on the plan.

## Audit checklist

- Structure: depth, duplicates, orphans (pages no hub or database links to), empty pages, personal pages holding team knowledge.
- Freshness: pages not edited for longer than their review cadence, expired verifications, owners who left.
- Exposure: public links, guests with broad access, pages shared individually outside the teamspace model, sensitive titles in broadly visible areas.
- Databases: duplicate databases for the same records, unused properties, views nobody owns.
- Record each finding with location, evidence, severity, impact, recommended change and whether it blocks the user's goal.

## Change-list format

| # | Page or database | Action | New parent | Permission effect | Links affected | Owner sign-off | Undo |
|---|---|---|---|---|---|---|---|

Order: create hubs, move, relink, archive. Pilot one area, verify, then continue.

## Migration notes

- Inventory the source first: spaces, page counts, attachments, internal links, comments, permissions.
- Notion's importers and Markdown or CSV imports usually preserve text and basic structure. Comments, page history, fine-grained permissions, macros and some internal links often do not survive. Test with a representative sample before the full import.
- Import into a staging area that only the migration team can see, fix links and structure, then move into place.
- Keep the source read-only during the cutover window and record the mapping from old locations to new pages.
