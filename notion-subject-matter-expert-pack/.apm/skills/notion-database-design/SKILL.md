---
name: notion-database-design
description: Design and change Notion databases - data sources, property types, relations and rollups, formulas, status workflows, views and filters, templates, buttons, forms and automations - and assess what a schema change breaks before it is made. Use when a user wants a new database or tracker, asks how to model information in Notion, needs a formula, relation, rollup or view, or wants to rename, retype, merge or delete properties in an existing database.
---

# Notion Database Design

## Purpose and activation

Model information so that each database row is one clear thing, each property earns its place, and every audience gets a view that answers its question. Activate for new databases, redesigns, formulas, relations and rollups, view design, templates and automations, and any change to an existing schema.

## Scope and exclusions

- In scope: database and data source structure, property types and option sets, relations (one-way and two-way, self-relations for sub-items and dependencies), rollups, formulas, status workflows, unique IDs, views (table, board, list, calendar, timeline, gallery, chart, form and others the plan offers), filters, sorts and grouping, database templates and buttons, automations, and schema-change impact.
- Out of scope: where the database sits in the workspace and who can open it (notion-workspace-architecture), filling the database with content from a spec (notion-spec-to-tasks), and code that reads or writes the database through the API (notion-api-integration).

## Inputs

- What one row represents, and roughly how many rows to expect.
- The questions people must answer from it, who updates which fields, and which views each audience needs.
- Existing databases on the same subject, fetched with their full schema, and anything that depends on them: relations from other databases, rollups, formulas, linked views, forms, automations, and integrations or scripts that use property names.
- Plan constraints; some view types, automations and actions are plan-dependent.

## Dependencies and tools

- The Notion connector's search, fetch and (for approved changes) database create and update tools. Some connectors cannot edit every schema element or read automations; say what must be done in the Notion interface instead.
- property-and-schema-reference.md in this skill folder: property selection guide, relation patterns, formula notes, view selection, the schema-change risk matrix and starter blueprints.

## Workflow

1. Search before building. If a database for these records already exists, extend it or add a filtered view instead of creating a second one.
2. Fetch the schema and identify the data source to use. A database can hold more than one data source; use the identifier the fetch returns, never a guessed one.
3. Model. Name the title property for the thing itself. Choose types by how the value is used: status for workflow stages, select for one category, multi-select for tags, relation for links to records in another database, person for accountability, date (with end date when it is a range), unique ID for references people quote. Use formulas only for derived values and rollups only over relations. Keep option sets short and owned.
4. Design views for jobs, not for completeness: a board grouped by status for daily work, a timeline for planning, a calendar for dated items, a filtered table per team, a form for intake. Name each view by its purpose.
5. Add templates, buttons and automations only where they remove repeated work. Note every notification they send and every plan dependency.
6. For a change to an existing database, classify each change with the risk matrix, list affected dependents, and write the safe procedure (duplicate or export first, add the new property, migrate values, update dependents, then retire the old property).
7. Apply approved changes, then fetch the schema again and inspect a sample of entries and each changed view.
8. Report schema impact, migrated values, dependents updated and anything left for the user to do in the interface.

## Output

A schema table (property, type, options or formula, purpose, who maintains it), relation diagram in text, view list, template and automation list with their notifications, and for changes a risk-classified change plan with undo steps.

## Validation

- Every property has a stated purpose and maintainer; nothing duplicates data available through a relation or rollup.
- Option values written to entries exactly match the fetched schema.
- Formulas are tested against at least one entry for each branch, including empty values.
- After a change, the re-fetched schema matches the plan and sampled entries kept their values.

## Failure handling and escalation

- Unknown dependents (integrations, automations not visible through the connector): list them as unverified and ask the owner before destructive changes.
- Data loss on retype (multi-select to select, text to number, relation removal): stop and get explicit approval with the export or duplicate taken first.
- The connector cannot perform a change: deliver exact interface steps and report PREPARED_NOT_VERIFIED for that part.

## Permissions and guardrails

- Creating a new database in a location the user named is Level 1.
- Changing an existing database's schema is Level 2: renames, retypes, deletions, removing options in use, and relation, rollup or formula changes. A user's explicit request authorizes that exact change; when impact analysis finds effects the user did not mention, state them and confirm before applying.
- Automations, buttons that notify, webhooks and recurring templates are Level 2; they act later without anyone watching.
- Never delete a property to tidy up; propose retiring it and leave the decision to the owner.

## Workflow connection

The primary `notion-subject-matter-expert` agent uses this skill whenever a task touches database structure; `notion-governance-reviewer` uses its risk matrix in change reviews. notion-spec-to-tasks and notion-knowledge-curation rely on it when the target database is missing or needs a property. Installed alone, it is self-contained: read freely, create new databases only where the user asked, and treat changes to existing schemas as needing explicit approval with an undo path. With the full pack installed, the `notion-subject-matter-expert-contract` instruction supplies the approval levels, handoff rules and completion report.
