# State address map

Use before changing resource addresses (a refactor, a `count` to `for_each` conversion, extraction into a module) or adopting existing objects (import). Each object in state, and each remote object being imported, must map to exactly one address. Fill this in before editing configuration, then confirm every row against a plan.

## Context

| Item | Value |
|---|---|
| Configuration directory | |
| Environments covered | |
| Source of current addresses (`terraform state list`, plan, or static reading) | |
| Terraform and provider versions | |

## Refactor moves

| Current address | New address | Mechanism (`moved` block or `state mv`) | Present in environments | Plan shows |
|---|---|---|---|---|

Rules:

- `moved` blocks are static. They cannot use variables, so a list-index to map-key mapping holds only if every environment's variable files produce the same order.
- A `moved` block whose `from` address is absent in an environment does nothing there.
- Keep historical `moved` blocks, and chain new ones after them. Removing a `moved` block breaks every user who has not yet crossed it.
- `state mv` is for exceptional state-only work, with a backup, this map, the state lock and an approval handoff.

## Import bindings

| Remote object (type and ID, redacted where needed) | Target address | ID format confirmed for the locked provider version | Configuration (generated draft or hand-written) | Plan shows |
|---|---|---|---|---|

Rules:

- Prefer `import` blocks. CLI `terraform import` writes state at once and authors no configuration.
- Treat generated configuration and Terraform Search output as drafts. Clean them before review.
- Keep the first apply a pure import: match live settings, and propose hardening as a separate change.
- Note sensitive attributes the import brings into state.

## Consumer impact

| Consumer (root, registry consumer, other repository) | Affected? | Action needed |
|---|---|---|

Release label for a published module: patch, minor or breaking. Base the label on consumer and state behaviour, not diff size, and give the reason.

## Plan confirmation

| Environment | Plan summary | Unexpected rows | Date |
|---|---|---|---|
