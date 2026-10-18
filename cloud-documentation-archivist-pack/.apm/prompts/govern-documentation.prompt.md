---
description: "Set the documentation contract, ownership, templates, taxonomy and lifecycle rules for a documentation repository or knowledge base"
agent: cloud-documentation-archivist
---

# Govern a documentation repository or knowledge base

## Inputs

- The repository, document root or knowledge base in scope, and its existing conventions.
- Its owners and reviewers, its continuous-integration and documentation tooling, and any external mirrors such as a wiki, portal or Notion workspace.
- The problems that prompted the request: stale pages, duplicates, missing owners, or pages nobody can find.

## Workflow

1. Apply repository-and-project-doc-governance.
   - Inventory the document roots, templates, generated outputs, navigation, owners, review metadata, links, automation and mirrors.
   - Classify each source as authoritative, generated, archival, or not to be edited.
   - Define a lightweight documentation contract: naming, location, frontmatter, required sections, owner, reviewer, last-reviewed date, status, version, deprecation and link policy.
   - Match the existing conventions before introducing new folders or root files.
2. Apply knowledge-base-and-taxonomy. Build the taxonomy around the readers' vocabulary, product boundaries, tasks, lifecycle and ownership. Keep categories shallow. Record aliases and acronyms. Separate evergreen reference, time-bound guidance, incident evidence, decisions, drafts and archives, and deprecate duplicate pages instead of leaving competing answers.
3. Apply templates-and-content-models to adapt or create templates that carry the contract's required fields. Keep native GitHub issue and pull request templates apart from writing templates.
4. Apply documentation-hooks-and-automation to propose checks that enforce the contract. Automate repetitive checks; leave editorial judgment to people.
5. When the structure changes, update references, navigation, CI checks, redirects, templates and contributor guidance together. Deliver this as a plan unless the user authorized the edits.

Do not change external mirrors or connectors without explicit authorization.

## Expected output

The inventory, the documentation contract, the taxonomy, template changes, proposed automation, and a change plan with an owner and sequence.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report.
