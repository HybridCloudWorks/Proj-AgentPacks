# Worked example: renaming and retyping properties in a shared Projects database

Synthetic scenario; the database and integration are invented.

Request: "In Projects, rename Status to Stage, and change Team from multi-select to select because each project has one owning team."

1. Fetch and map dependents. notion-database-design fetches Projects and the databases related to it. Dependents found: a rollup in Portfolio counting projects by Status, two board views grouped by Status, a formula that flags stalled projects using Status, and a filter on the leadership dashboard. The user mentions a nightly script that exports Projects to a spreadsheet; the agent asks for its property mapping and learns it reads "Status" by name.
2. Classify with the risk matrix.
   - Rename Status to Stage: medium. Views, the formula and the rollup follow the rename inside Notion; the export script breaks.
   - Team multi-select to select: high. Eight of 140 projects have two teams; converting would keep only one value and the choice of which is not controlled.
3. Propose. Rename after the script owner updates the mapping, with both changes landing the same day. For Team, add a new select property "Owning team", fill it for the 132 single-team projects, list the eight dual-team projects for their owners to decide, then hide the old property from views and retire it later. Take a CSV export of Projects first.
4. Approval. The user's request authorized a rename and a retype, but the impact analysis found effects the user had not mentioned (a broken script, eight projects losing data). The agent states them and asks for a fresh decision. The user approves the safer Team plan and defers the rename until the script is updated.
5. Execute and verify. The agent asks the user to take the export (the connector cannot export), adds "Owning team", sets it on the approved list of 132 entries in batches, re-fetches the schema, samples twenty entries and confirms the boards still render. The eight dual-team projects are listed in the report for their owners to decide; nobody is mentioned or notified.

Report: PREPARED_NOT_VERIFIED for the rename (not performed) and verified for the new property, so the overall status is PREPARED_NOT_VERIFIED, with the fallback sentence, `schema_impact` listing every dependent, and rollback steps (remove the new property; the export holds the original values).
