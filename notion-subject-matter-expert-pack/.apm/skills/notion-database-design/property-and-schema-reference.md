# Property and schema reference

Property types, view types, formula functions and automation options evolve and some depend on the plan. Check the current Notion interface or formula reference before promising a capability.

## Choosing a property type

| Need | Use | Avoid |
|---|---|---|
| Workflow stage with groups such as not started, in progress, done | Status | Select, which has no stage groups |
| One category from a short fixed list | Select | Free text that drifts |
| Several labels | Multi-select | One select with combined values |
| Link to a record that lives elsewhere | Relation | Copying the other record's name into text |
| A value computed from other properties | Formula | Manually maintained duplicates |
| A value summarized from related records | Rollup over a relation | Hand-updated counts |
| Accountability | Person | Names typed as text |
| Deadline or period | Date, with end date for ranges | Two separate text dates |
| A stable reference people quote | Unique ID with a prefix | Titles used as identifiers |
| Who changed what and when | Created by, created time, last edited by, last edited time | Manual "updated" fields |

Keep the title property meaningful on its own: "Renew vendor contract for payroll" rather than "Contract".

## Relation patterns

- One-to-many: Projects to Tasks. Relation on Tasks pointing at Projects, shown on both sides, with a rollup on Projects counting open tasks.
- Many-to-many: Documents to Topics. Two-way relation; each side lists the other.
- Self-relation: Tasks to Tasks for parent and sub-items, or "Blocked by" and "Blocking" for dependencies used by timeline views.
- Junction database: when the link itself carries data (a person's role on a project, an allocation percentage), model the link as its own database with two relations.

## Formula notes

Formulas reference properties with `prop("Name")`. Useful building blocks include `if` and `ifs`, `and`, `or`, `not`, `empty`, `today` and `now`, `dateBetween`, `dateAdd`, `formatDate`, `format`, `let`, and list functions such as `map`, `filter` and `length` over relations. Examples:

- Overdue flag: `if(not empty(prop("Due")) and prop("Due") < today() and prop("Status") != "Done", "Overdue", "")`
- Days open: `dateBetween(now(), prop("Created time"), "days")`
- Open related tasks: `prop("Tasks").filter(current.prop("Status") != "Done").length()`

Test each branch, including empty dates and empty relations, against real entries.

## Choosing a view

| Job | View |
|---|---|
| Move work through stages | Board grouped by status |
| Plan across time with dependencies | Timeline |
| See dated items by day or month | Calendar |
| Scan and edit many fields | Table, with a saved filter per audience |
| Browse visual items | Gallery |
| Read a simple list | List |
| Summarize counts or trends | Chart |
| Collect requests from people outside the database | Form |

Name views by purpose ("My open tasks", "This sprint", "Needs review"), not by type.

## Schema-change risk matrix

| Change | Typical effect | Risk | Safe procedure |
|---|---|---|---|
| Add property or view | Visible to all users of the database | Low | Add, explain its purpose in the description |
| Add select option | New value appears | Low | Add with the owner's agreement |
| Rename property | Notion-internal references usually follow; API scripts, imports, MCP prompts and external filters that use the name break | Medium | Find external users of the name first; coordinate the rename |
| Rename or remove an option in use | Entries lose or change their value | High | Migrate entries to the new value, then retire the old one |
| Change property type | Values that do not fit the new type can be lost | High | Duplicate or export first; add a new property, migrate, verify, retire the old |
| Delete property | Values gone from entries; formulas, rollups, filters and automations depending on it break | High | Retire instead: hide from views, note it in the description, delete later with owner approval |
| Change or remove a relation | Rollups and the other database's view of the link change | High | Map dependents on both sides first |
| Change a formula | Every view, filter and sort using it changes | Medium | Test on sample entries before saving |
| Add or change an automation | Acts without supervision; may notify or edit at scale | High | Describe trigger, action and notifications; start narrow; approval required |

## Starter blueprints

Adapt these to what the user's team actually tracks; do not create unused properties.

- Tasks: Name (title), Status, Priority (select), Owner (person), Due (date), Project (relation), Blocked by (self-relation), Estimate (number or select), ID (unique ID).
- Projects: Name, Status, Lead (person), Dates (date range), Tasks (relation), Open tasks (rollup), Goal (text), Spec (relation or URL).
- Decisions: Decision (title), Status (proposed, accepted, superseded, rejected), Decided on (date), Decision makers (person), Area (select), Impact (select), Supersedes (self-relation).
- Documents or wiki: Title, Type (how-to, reference, explainer, policy, FAQ), Owner (person), Tags (multi-select), Review by (date), Status (draft, current, outdated).
- Meetings: Title, Date, Type (decision, status, planning, retrospective, one-to-one, external), Attendees (person), Project (relation), Decisions (relation), Follow-ups (relation to Tasks).
