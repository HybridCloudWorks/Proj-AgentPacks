# Cloud Documentation Archivist Pack

This pack consolidates the supplied Docs & Knowledge Curator, ADR Authoring, Diátaxis guidance, and blog/gist/README/task/workflow templates into a portable documentation expert.

## Primary downloads

- `dist/cloud-documentation-archivist-pack.zip` - complete pack
- `dist/cloud-documentation-archivist-canonical.zip` - canonical Agent and Skills
- `dist/cloud-documentation-archivist-prompt.zip` - reusable authoring prompt
- `dist/cloud-documentation-archivist-skills.zip` - individual Skill bundle
- `dist/cloud-documentation-archivist-validation.zip` - uppercase validation report

Vendor packages are under `dist/github-copilot/`, `dist/claude-code/`, `dist/openai-codex/`, and `dist/gemini-cli/`.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
python tooling/validate_documentation.py templates/README.md
```

The build creates one `skill.zip` per Skill and includes the template library in each vendor target. Validation is static and performs no external publication or connector write.

## Operating model

Use `hooks/pre-documentation.*` before authoring and `hooks/post-documentation.*` after writing. The default behavior is local and read-only. Publishing, PR creation, wiki changes, Notion writes, shared links, and other external mutations require explicit authorization.
