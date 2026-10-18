# Microsoft Certified Trainer Pack

This pack turns official Microsoft sources and trainer-owned customizations into an evidence-aware teaching workflow. It is designed for an authorized MCT with access to Microsoft Learn, Microsoft Official Curriculum, and—where permitted—the Learning Download Center.

## Primary deliverables

- `DESCRIPTION.md` — concise pack identity and scope.
- `.apm/` — canonical agents and 18 focused Skills.
- `PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md` — reusable authoring standard used for this pack.
- `dist/` — four AI-specific packages, canonical source, validation bundle, full pack, and one `skill.zip` per Skill.
- `VALIDATION_REPORT.md` — uppercase static validation report.

## Use model

Use `microsoft-certified-trainer` for end-to-end work. It can inspect sources, research official Microsoft documentation, author course assets, and run local checks without specialists. Invoke specialists when a focused review or parallel workstream is useful; they share the same source and reporting contract.

The pack intentionally hands off specialized live work to existing Azure Architect and GitHub Expert packs. The handoff packet includes objectives, prerequisites, environment assumptions, permissions, cost and data boundaries, acceptance evidence, rollback/cleanup, and the exact question for the partner agent.

## Source and safety boundary

Supplied MCT courseware is treated as reference material with provenance and change-log tracking. The agent does not reproduce restricted Microsoft courseware wholesale, infer redistribution rights, or claim live tenant behavior. Product features, UI, licensing, rollout, and Designer availability are verified against current Microsoft sources when material.

## Build and validate

From this directory, use the bundled Python runtime or another Python 3.11+ interpreter:

```powershell
python tooling\build_pack.py
python tooling\validate_pack.py --write-report
python tooling\validate_pack.py
```

Static validation proves structure, parity, frontmatter, scripts, tests, and archive integrity. It does not prove MCT authorization, tenant access, courseware license terms, live Copilot behavior, Copilot Studio publication, cloud deployment, or classroom learning outcomes.

