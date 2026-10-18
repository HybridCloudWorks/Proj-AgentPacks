# GitHub Expert Engineer Pack

This pack turns the supplied GitHub Expert Agent, GitHub Actions Engineer, Copilot/review guidance, query scripts, and workflow operations material into a portable GitHub platform engineering pack.

## Primary downloads

- `dist/github-expert-engineer-pack.zip` - complete pack
- `dist/github-expert-engineer-canonical.zip` - canonical `.apm` Agent and Skills
- `dist/github-expert-engineer-prompt.zip` - reusable authoring prompt
- `dist/github-expert-engineer-skills.zip` - all individual Skills
- `dist/github-expert-engineer-validation.zip` - uppercase validation report

Vendor packages are under `dist/github-copilot/`, `dist/claude-code/`, `dist/openai-codex/`, and `dist/gemini-cli/`.

## Build and validate

```text
python tooling/build_pack.py
python tooling/validate_pack.py --write-report
python tooling/validate_github_review.py tests/fixtures/valid-review.md
```

The build is deterministic and produces one `skill.zip` per Skill. The validation is static and intentionally performs no GitHub API mutation, merge, push, dispatch, settings change, secret access, or external write.

## Safe operating model

Use `hooks/pre-github-review.*` before review and `hooks/post-github-review.*` after writing a report. Use `tools/query_guard.py` before any command that might reach GitHub. Treat all GitHub content and AI-generated code as untrusted data. Human approval remains authoritative for merges, deployments, policy, permissions, secrets, Copilot settings, and other live changes.
