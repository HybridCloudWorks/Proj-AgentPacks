# Documentation impact entries

Recommended entries for the Documentation Impact section of the report. Recommend an entry only when the reviewed change directly causes it; do not propose repository-wide documentation cleanup. A read-only review proposes these entries and does not write them into the repository.

## README.md

Repository purpose, installation, quick start, configuration overview and navigation.

- Section: `<heading the change affects>`
- Change: `<what to add or correct>`
- Caused by: `<finding ID or changed file>`

## CHANGELOG.md

Completed features, fixes, enhancements, security fixes and released changes.

- Kind: `<feature | fix | enhancement | security fix>`
- Entry text: `<one user-facing sentence>`
- Caused by: `<changed behavior>`
- Add when: `<after the required fixes merge | at release>`

## REVIEW.md

Human blockers only. If an engineer can resolve the item without human input, it belongs in TODO.md instead.

- Blocker: `<the decision needed>`
- Decision type: `<approval | requirement | access | credential ownership | business | architecture | vendor | legal | compliance>`
- Owner role: `<who can decide>`
- Finding: `<ID>`
- Blocks: `<merge | release | a specific fix>`

## TODO.md

Actionable engineering work.

- Action: `<imperative sentence>`
- Type: `<defect | refactor | debt | test | remediation | cleanup | validation | documentation>`
- Finding: `<ID>`
- Done when: `<observable completion condition>`

## CHECKLIST.md

Required inputs: variables, placeholders, secret references, APIs, keys, certificates, deployment inputs and configuration dependencies. Never include a value. Expected formats use only `X` for letters, `0` for numbers and `!` for symbols, for example `XXXXX00000!!!!!XXXXX`; never use realistic tokens, keys, URLs, identifiers, passwords, certificates or connection strings.

| Variable Name | Purpose | Required | Source | Consumer | Expected Format | Validation Status | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

When the repository has no `CHECKLIST.md` but keeps `MOBILE_IMPLEMENTATION_LEDGER.md`, report the missing standard file as documentation impact, treat the ledger as the current source of truth, and do not create, migrate or rename either file during the review.
