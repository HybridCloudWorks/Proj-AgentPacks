---
description: "Create or update reference documentation for an API, CLI, configuration file, schema, resource or error catalogue"
agent: cloud-documentation-archivist
---

# Document a technical reference

## Inputs

- The interface in scope: endpoints, commands, configuration keys, schema properties, resource types or error codes.
- Its source of truth and version: an OpenAPI or JSON schema, CLI help output, source code, or vendor documentation with a version or date.
- The versions and availability (region, plan or edition) the reference covers.
- The existing reference layout and any generator the repository already uses.

## Workflow

1. Apply technical-reference-and-api-docs. Organize the page the way the product is organized. For each item, record its syntax, type, whether it is required, default, allowed values, constraints, side effects, permissions, errors, idempotency, version or availability, and a minimal example. When a schema is reliable, generate from it, then review the output for omissions and misleading defaults.
2. Apply diataxis-content-design to keep the page neutral reference. Link procedures to how-to guides instead of writing them inline.
3. Apply templates-and-content-models to choose the reference or API template.
4. Apply docs-security-privacy-and-redaction to every request, response and configuration example.
5. Apply documentation-validation-and-link-checking. Validate examples against the schema or with a read-only local command; otherwise label them illustrative. Check anchors and links.

Never invent a field, response, limit, SKU or behaviour. When a fact is uncertain or depends on the environment, mark it and give the source version and date.

## Expected output

The reference pages; the source version and how the content was produced (generated, hand-written or mixed); the items whose behaviour is uncertain; and the validation results.

Follow the `cloud-documentation-archivist-contract` instruction and end with its completion report.
