# Worked example: a configuration reference generated from a schema

Synthetic scenario. `envctl` is an illustrative internal CLI, and its schema, paths and pull request numbers are invented.

Prompt used: `document-reference.prompt.md`.

## Request

"Document every key in envctl's `environment.yaml` for the 2.4 release." The request comes from the Platform team, which owns `envctl`.

## Sources

| Source | Role |
| --- | --- |
| `schema/environment.schema.json` at tag `v2.4.0` | Authoritative structure, types, required keys, enums and defaults |
| `internal/config/load.go` at `v2.4.0` | How defaults are applied, plus validation the schema cannot express |
| Pull request #512 thread, supplied | A maintainer's clarification of `drift_check.mode` |
| `make docs-schema` | The repository's existing target that renders the schema to Markdown tables |

## Applying technical-reference-and-api-docs

1. `make docs-schema` rendered 27 properties into a table: name, type, required, default, allowed values and schema description.
2. Review of the generated output against the code:
   - `tags_inherit` and `drift_check.mode` had no schema description. Their descriptions were written from `load.go` (lines 88 to 104) and match the maintainer's explanation in #512. An upstream schema fix is listed as a follow-up. No issue was filed, because filing one is an external write.
   - The schema gives `log_retention_days` a default of 30, and `load.go` applies the schema default without overriding it, so the documented default is correct.
   - `load.go` also rejects a `network.cidr` that overlaps `10.0.0.0/16`, which the schema cannot express. The constraint was added to that row, with the source line cited.
   - The allowed `region` values depend on which regions are enabled for the account. The row says so and links to the account's region settings instead of listing values that would go stale.
3. The page is organized as the file is: top-level keys, then `network`, `drift_check` and `tags` sections. A link to the "Create an environment" how-to replaces the procedural text the old page had.
4. **docs-security-privacy-and-redaction.** Example files use `ACCOUNT_ID` and `example-env` as placeholders. No real account or CIDR from production appears.

## Completion report

Recommendation: **DOCUMENTATION_READY**

### Scope and audience

A reference for every key in `environment.yaml` as of envctl 2.4.0, for platform engineers and service teams who write environment files. Earlier versions are out of scope.

### Source and evidence

| Claim or section | Source | Version or date | Evidence label |
| --- | --- | --- | --- |
| Keys, types, required, enums, defaults | `schema/environment.schema.json` | `v2.4.0` | observed |
| Default application and the CIDR constraint | `internal/config/load.go` | `v2.4.0` | observed |
| `drift_check.mode` semantics | PR #512 maintainer comment, matched against `load.go` | 2026-10-11 | observed |
| `region` values are environment-dependent | `load.go` region lookup | `v2.4.0` | observed |

### Content decision

Replaced `docs/reference/environment-file.md` with the generated-then-reviewed reference (27 keys). Added `examples/environment.minimal.yaml` and `examples/environment.full.yaml`. Moved the procedural content to a link to the existing how-to guide.

### Validation

| Check | Method or command | Result | Notes |
| --- | --- | --- | --- |
| Generated table matches the schema | `make docs-schema`, then a diff against the page | passed | 27 of 27 properties present |
| Examples are valid | `envctl config validate --file examples/environment.minimal.yaml` and `--file examples/environment.full.yaml` with envctl 2.4.0 installed locally | passed | Exit code 0 for both; the command is read-only |
| Structure, placeholders, secret-like values | `hooks/post-documentation.sh docs/reference/environment-file.md` | passed | |
| Relative links (9) | Manual resolution | passed | |
| External link to the provider's region list | — | not run | Network access not authorized; it is further reading only |

There are no findings.

### Limitations

The external region-list link was not checked. Behaviour before 2.4.0 is not documented. The two missing schema descriptions are fixed on the page but not yet upstream.

### Ownership and next review

- Owner: Platform team
- Reviewer or decider: none required
- Document status: Active
- Next review: the envctl 2.5.0 release, or 2027-01-18, whichever comes first
- Handoff: none. Optional follow-up: add the two descriptions to the schema so the next generation needs no manual fill
