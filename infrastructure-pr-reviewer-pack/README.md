# Infrastructure PR Reviewer Pack

A portable, evidence-driven review pack for infrastructure-as-code, configuration management, deployment automation, platform manifests, and CI/CD pull requests.

The canonical source is vendor-neutral. GitHub Copilot receives additional code-review setup collateral because the supplied source package was designed for Copilot pull-request review. Claude Code, OpenAI Codex, and Gemini CLI receive native Agent and Skill layouts with equivalent review semantics.

## Canonical architecture

```text
infrastructure-pr-reviewer
└── review-infrastructure-pr
    ├── review-terraform-opentofu
    ├── review-bicep-arm
    ├── review-powershell-automation
    ├── review-ansible-automation
    ├── review-cicd-deployment
    ├── review-kubernetes-packaging
    └── verify-infrastructure-evidence
```

The orchestration Skill owns the complete changed-line review protocol, universal gates, severity model, de-duplication, and final output. Technology Skills load only when their stack appears in the change. The evidence Skill owns non-deploying static checks and interpretation of plan, preview, render, test, policy, and CI evidence.

## Build

```bash
python3 tooling/build_pack.py
```

The build validates the source, generates all targets, packages every Skill, tests bundled scripts, verifies ZIP structure, and writes `dist/VALIDATION_REPORT.md`.

## APM

`apm.yml` and `.apm/` are the authored package. Run `apm install` in an environment with Microsoft APM to generate `apm.lock.yaml`, deploy supported primitives, and audit drift. Commit the generated lockfile after dependency resolution.

## Safety posture

The reviewer is read-only by default. It may inspect repository and pull-request evidence and run explicitly safe, non-deploying checks. It must not edit files, apply infrastructure, invoke target-side configuration, acquire production credentials, or claim approval authority.

## Distribution

- Complete package: `dist/infrastructure-pr-reviewer-pack.zip`
- Combined Skill archives: `dist/infrastructure-pr-reviewer-skills.zip`
- Native targets: `dist/`
- Individual Skills: `dist/skills/<skill-name>/skill.zip`
- Validation record: `dist/VALIDATION_REPORT.md`
