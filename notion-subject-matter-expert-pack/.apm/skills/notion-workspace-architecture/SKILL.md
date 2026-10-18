---
name: notion-workspace-architecture
description: Design, restructure and audit how a Notion workspace is organized and governed - teamspaces, page hierarchy, wikis and hub pages, naming and tagging, sharing and permission models, content lifecycle, migrations and workspace health. Use when a user asks where content should live, how to organize or reorganize a workspace or teamspace, who can see what, how to consolidate or migrate pages into Notion, or why content is hard to find, stale, duplicated or over-shared.
---

# Notion Workspace Architecture

## Purpose and activation

Give a workspace a structure people can navigate, permission boundaries that match its audiences, and a lifecycle that keeps content current. Activate for structure proposals, teamspace design, reorganizations, migrations from other tools, sharing reviews and workspace health audits.

## Scope and exclusions

- In scope: teamspaces and top-level pages, page trees and depth, wiki pages and verification, hub and index pages, linked database views used as navigation, naming conventions, tag vocabularies, the sharing model (members, groups, guests, public web links), ownership and review cadence, archive rules, audits, restructure and migration plans.
- Out of scope: property-level database modeling (use notion-database-design), writing page content (use notion-knowledge-curation), plan purchases and billing, identity-provider configuration such as SSO or SCIM (advise only; an administrator acts in the admin console), and legal retention decisions.

## Inputs

- The goal or the pain point, in the user's words.
- Teams and audiences, including any external guests.
- The current structure: teamspaces, top-level pages and main databases, fetched or described by the user.
- Sensitivity of the content and any rules about who may see it.
- The workspace plan and the user's role; teamspace types, permission groups, audit logs and verified pages vary by plan.
- For migrations: the source tool, volume, deadline and what must survive (links, comments, history, permissions).

## Dependencies and tools

- The host's Notion connector for search and fetch. Move, update and archive tools are used only for approved changes.
- workspace-design-reference.md in this skill folder: organizing patterns, hub outline, naming and tagging rules, permission summary, audit checklist, change-list format and migration notes.
- Most connectors cannot read sharing settings, member lists, teamspace settings or audit logs. Ask the user or an administrator for that evidence instead of assuming it.

## Workflow

1. Inventory. Map teamspaces, top-level pages, major databases and hub pages. Sample deep trees rather than fetching everything. Record owners, last-edited dates and what the connector cannot see.
2. Diagnose. Look for findability problems (vague or duplicate titles, trees deeper than about four levels, pages no hub links to), missing owners, stale pages, the same information kept in several places instead of one database with linked views, team knowledge sitting in personal pages, and permission sprawl (many pages shared one by one, guests on broad trees, public links).
3. Design. Choose an organizing principle (by team, by function, by lifecycle, or a hybrid) and write it down. Align teamspace and top-level boundaries with permission boundaries so inheritance does the work. Define hub pages, a small controlled tag vocabulary, naming conventions, owners and a review cadence. Decide where each shared database lives and where its linked views appear.
4. Plan changes. Produce a change list: each line names the page, the action (create hub, move, merge, rename, archive), the new parent, the permission effect, link impact, the owner who must agree, and the undo path. Order it: create hubs, move, relink, then archive. Pilot one area before the rest.
5. Execute only what is approved. Moves and archives are Level 2 because they change who can see content or remove it from view. Stop the batch at the first unexpected result.
6. Verify. Fetch moved pages and confirm their parent. Fetch hub pages and confirm their links resolve. Re-run the relevant audit items.
7. Report with the contract's completion report, including the permission effect of every move.

## Output

A structure proposal as an outline tree, the tag vocabulary and naming rules, governance rules (owners, review cadence, verification, archive), a change list with risk and undo for each line, or audit findings with severity and location.

## Validation

- Every proposed teamspace and top-level page has an owner and a stated audience.
- Every audit finding names a page, database or teamspace and the evidence for it.
- After execution, every moved page is fetched under its expected parent and every hub link resolves.
- Pre-publication check for anything shared outward: no credentials, no internal-only markers, no unfilled placeholders, and every mention points at a URL taken from a fetched result.

## Failure handling and escalation

- Partial visibility: report audit coverage as partial and list what was not visible. Never conclude that no other pages exist.
- A move or archive fails mid-batch: stop, report which steps completed, and give the restore steps (move back, restore from Trash, page history).
- Conflicting owners or audiences: report BLOCKED_ON_HUMAN_DECISION with the options and their consequences.
- Migration fidelity gaps (lost comments, flattened permissions, broken internal links): list them per source before the import runs.

## Permissions and guardrails

- Reading for an audit stays within the assigned scope. Report sensitive findings by location and category; do not paste the sensitive content into the report.
- Never change sharing, remove guests or disable public links to "fix" a finding without explicit approval of that exact change.
- Moving pages, archiving, changing permissions, inviting guests and publishing to the web are Level 2.
- Large reorganizations notify page followers and change URLs people bookmarked; say so in the change list.

## Workflow connection

The primary `notion-subject-matter-expert` agent uses this skill for design and audit work; `notion-governance-reviewer` uses it for independent exposure reviews. The pack's design and audit prompts call it. Installed alone, it is self-contained: treat reads as safe, treat moves, archives and sharing changes as needing the user's explicit approval, and verify every change by fetching. With the full pack installed, the `notion-subject-matter-expert-contract` instruction supplies the approval levels, handoff rules and completion report.
