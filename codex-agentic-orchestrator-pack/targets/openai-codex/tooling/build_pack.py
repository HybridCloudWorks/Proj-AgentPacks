#!/usr/bin/env python3
"""Build the Codex-specific target and deterministic archives."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".apm"
TARGETS = ROOT / "targets"
DIST = ROOT / "dist"


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def zip_dir(source: Path, destination: Path, root_name: str | None = None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    root_name = root_name or source.name
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            arc = Path(root_name) / path.relative_to(source)
            info = zipfile.ZipInfo(str(arc).replace("\\", "/"))
            info.date_time = (2024, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())


AGENT_TEXT = '''name = "codex-agentic-orchestrator"
description = "Codex workflow orchestrator for explicit delegation, durable handoffs, capability-aware selection, bounded concurrency, and truthful completion across one, selected, or all installed custom agents."
sandbox_mode = "workspace-write"
approval_policy = "on-request"
developer_instructions = """
Read repository instructions first. Discover installed `.codex/agents` and create a workflow with `python tooling/workflow.py init` before delegation. Request Codex to use its native subagent workflow for every required specialist action and the exact registered custom agent name. Require each subagent to write `.agentic/workflows/<workflow-id>/handoffs/<agent-id>.yml` using the handoff contract. Missing optional agents are recorded as skipped; missing required agents block. Validate before synthesis. Ask before external writes, destructive commands, deployment, production work, credentials, or permission changes. Report actual invocations, handoff evidence, skipped or blocked nodes, unresolved risks, and the next safe action.
"""
'''


def generate_target() -> Path:
    if TARGETS.exists():
        shutil.rmtree(TARGETS)
    target = TARGETS / "openai-codex"
    copy_tree(CANONICAL / "skills", target / ".agents" / "skills")
    (target / ".codex" / "agents").mkdir(parents=True, exist_ok=True)
    (target / "compatibility").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "DESCRIPTION.md", target / "DESCRIPTION.md")
    shutil.copy2(ROOT / "compatibility" / "agent-registry.yml", target / "compatibility" / "agent-registry.yml")
    shutil.copy2(ROOT / ".codex" / "hooks.json", target / ".codex" / "hooks.json")
    shutil.copy2(ROOT / ".codex" / "config.agentic-orchestrator.toml", target / ".codex" / "config.agentic-orchestrator.toml")
    shutil.copy2(ROOT / "AGENTS.agentic-orchestrator.md", target / "AGENTS.agentic-orchestrator.md")
    copy_tree(ROOT / "tooling", target / "tooling")
    copy_tree(ROOT / "hooks", target / "hooks")
    (target / ".codex" / "agents" / "codex-agentic-orchestrator.toml").write_text(AGENT_TEXT, encoding="utf-8")
    (target / "INSTALL.md").write_text("""# Codex installation

Copy this target into the repository root. Merge `.codex/hooks.json` into the existing project hook configuration and merge `.codex/config.agentic-orchestrator.toml` into `.codex/config.toml`; do not overwrite existing files. Review and trust the project hooks with `/hooks` before enabling them.

Use the `codex-agentic-orchestrator` custom agent from Codex app, CLI, or IDE. Domain agents remain separate: install any combination of the user's domain packs under `.codex/agents` and `.agents/skills`.

The orchestrator records local state under `.agentic/`. It performs no network calls by itself. Review sandbox and approval behavior before allowing delegated subagents to edit files or use external tools.

If the repository already has `AGENTS.md`, merge the supplied `AGENTS.agentic-orchestrator.md` guidance into the relevant section instead of replacing the file.
""", encoding="utf-8")
    return target


def build_archives(target: Path) -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    zip_dir(target, DIST / "openai-codex" / "openai-codex.zip", "openai-codex")
    zip_dir(CANONICAL, DIST / "codex-agentic-orchestrator-canonical.zip", ".apm")
    prompt_dir = DIST / "primary-prompt"
    prompt_dir.mkdir()
    shutil.copy2(ROOT / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md", prompt_dir / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md")
    zip_dir(prompt_dir, DIST / "codex-agentic-orchestrator-prompt.zip", "codex-agentic-orchestrator-prompt")
    shutil.rmtree(prompt_dir)
    for skill in sorted((CANONICAL / "skills").iterdir()):
        if skill.is_dir():
            zip_dir(skill, DIST / "skills" / skill.name / "skill.zip", skill.name)
    bundle = DIST / "skills-bundle"
    for archive in sorted((DIST / "skills").glob("*/skill.zip")):
        destination = bundle / "skills" / archive.parent.name / "skill.zip"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(archive, destination)
    zip_dir(bundle, DIST / "codex-agentic-orchestrator-skills.zip", "codex-agentic-orchestrator-skills")
    shutil.rmtree(bundle)
    report_dir = DIST / "primary-validation"
    report_dir.mkdir()
    shutil.copy2(ROOT / "VALIDATION_REPORT.md", report_dir / "VALIDATION_REPORT.md")
    zip_dir(report_dir, DIST / "codex-agentic-orchestrator-validation.zip", "codex-agentic-orchestrator-validation")
    shutil.rmtree(report_dir)
    full = DIST / "full-pack"
    for item in [".apm", ".codex", "compatibility", "docs", "hooks", "tests", "tooling", "AGENTS.agentic-orchestrator.md", "README.md", "DESCRIPTION.md", "LICENSE", "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md", "VALIDATION_REPORT.md", "apm.yml"]:
        source = ROOT / item
        destination = full / item
        if source.is_dir():
            copy_tree(source, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    copy_tree(TARGETS, full / "targets")
    copy_tree(DIST / "skills", full / "dist" / "skills")
    for name in ["codex-agentic-orchestrator-canonical.zip", "codex-agentic-orchestrator-prompt.zip", "codex-agentic-orchestrator-skills.zip", "codex-agentic-orchestrator-validation.zip"]:
        shutil.copy2(DIST / name, full / "dist" / name)
    (full / "dist" / "openai-codex").mkdir(parents=True, exist_ok=True)
    shutil.copy2(DIST / "openai-codex" / "openai-codex.zip", full / "dist" / "openai-codex" / "openai-codex.zip")
    zip_dir(full, DIST / "codex-agentic-orchestrator-pack.zip", "codex-agentic-orchestrator-pack")
    shutil.rmtree(full)


if __name__ == "__main__":
    target = generate_target()
    build_archives(target)
    print(f"built Codex target and {len(list((DIST / 'skills').glob('*/*.zip')))} Skill archives")
