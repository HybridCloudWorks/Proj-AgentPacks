"""Build the canonical Microsoft Certified Trainer pack and four vendor targets."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
APM = ROOT / ".apm"
AGENTS = APM / "agents"
SKILLS = APM / "skills"
TARGETS = ROOT / "targets"
DIST = ROOT / "dist"

AGENT_FILES = [
    "microsoft-certified-trainer.agent.md",
    "microsoft-course-architect.agent.md",
    "microsoft-lab-demo-engineer.agent.md",
    "microsoft-courseware-engineer.agent.md",
    "microsoft-copilot-learning-reviewer.agent.md",
]
SKILL_NAMES = [
    "mct-courseware-governance", "microsoft-learn-curriculum-mapping", "learning-objectives-and-assessment",
    "course-architecture-and-syllabus", "instructor-led-facilitation", "trainer-preparation-and-rehearsal",
    "microsoft-365-copilot-instruction", "microsoft-365-apps-workflows", "copilot-prompting-and-knowledge-checks",
    "copilot-studio-course-labs", "microsoft-designer-and-visual-content", "powerpoint-courseware-engineering",
    "lab-and-demo-engineering", "git-and-github-course-delivery", "azure-and-cloud-lab-handoff",
    "course-evaluation-and-feedback", "training-content-maintenance", "trainer-automation-and-tools",
]
INSTRUCTIONS = [
    "mct.instructions.md", "curriculum.instructions.md", "delivery.instructions.md",
    "courseware.instructions.md", "copilot.instructions.md", "security-and-privacy.instructions.md",
]
PROMPTS = [
    "ingest-mct-courseware.prompt.md", "map-learn-content.prompt.md", "design-course.prompt.md",
    "build-one-day-agenda.prompt.md", "prepare-instructor-guide.prompt.md", "create-interactive-lab.prompt.md",
    "rehearse-demo.prompt.md", "engineer-powerpoint-deck.prompt.md", "create-knowledge-checks.prompt.md",
    "create-copilot-studio-workshop.prompt.md", "refresh-from-change-log.prompt.md", "evaluate-session.prompt.md",
]
EXAMPLES = [
    "ms-4018-course-map.md", "one-day-agenda.md", "copilot-demo-runbook.md", "copilot-studio-lab.md",
    "interactive-powerpoint-session.md", "azure-github-handoff.md", "session-evaluation.md", "refresh-from-change-log.md",
]


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_skill(name: str, destination_root: Path) -> None:
    source = SKILLS / name
    destination = destination_root / name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def copy_skills(destination_root: Path) -> None:
    for name in SKILL_NAMES:
        copy_skill(name, destination_root)


def copy_shared(destination_root: Path) -> None:
    for directory, names in (("instructions", INSTRUCTIONS), ("prompts", PROMPTS), ("examples", EXAMPLES)):
        for name in names:
            copy_file(ROOT / directory / name, destination_root / directory / name)


def copy_agents(destination_root: Path, extension: str = ".agent.md") -> None:
    for name in AGENT_FILES:
        target_name = name if extension == ".agent.md" else name.replace(".agent.md", extension)
        copy_file(AGENTS / name, destination_root / target_name)


def source_description(source: Path) -> str:
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return source.stem.replace("-", " ").title()


def copy_claude_agents(destination_root: Path) -> None:
    tool_sets = {
        "microsoft-certified-trainer.agent.md": "Read, Grep, Glob, Edit, Write, Bash, WebFetch, WebSearch, Task",
        "microsoft-course-architect.agent.md": "Read, Grep, Glob, WebFetch, WebSearch",
        "microsoft-lab-demo-engineer.agent.md": "Read, Grep, Glob, Edit, Write, Bash, WebFetch, WebSearch",
        "microsoft-courseware-engineer.agent.md": "Read, Grep, Glob, Edit, Write, Bash, WebFetch, WebSearch",
        "microsoft-copilot-learning-reviewer.agent.md": "Read, Grep, Glob, Edit, Write, WebFetch, WebSearch",
    }
    for name in AGENT_FILES:
        source = AGENTS / name
        stem = name.removesuffix(".agent.md")
        content = (
            "---\n"
            f"name: {stem}\n"
            f"description: {source_description(source)}\n"
            f"tools: {tool_sets[name]}\n"
            "---\n\n"
            f"{agent_body(source)}\n"
        )
        write(destination_root / f"{stem}.md", content)


def copy_gemini_agents(destination_root: Path) -> None:
    tool_sets = {
        "microsoft-certified-trainer.agent.md": ["read_file", "grep_search", "run_shell_command", "write_file", "replace", "google_web_search"],
        "microsoft-course-architect.agent.md": ["read_file", "grep_search", "google_web_search"],
        "microsoft-lab-demo-engineer.agent.md": ["read_file", "grep_search", "run_shell_command", "write_file", "replace", "google_web_search"],
        "microsoft-courseware-engineer.agent.md": ["read_file", "grep_search", "run_shell_command", "write_file", "replace", "google_web_search"],
        "microsoft-copilot-learning-reviewer.agent.md": ["read_file", "grep_search", "write_file", "replace", "google_web_search"],
    }
    for name in AGENT_FILES:
        source = AGENTS / name
        stem = name.removesuffix(".agent.md")
        lines = ["---", f"name: {stem}", f"description: {source_description(source)}", "kind: local", "tools:"]
        lines.extend(f"  - {tool}" for tool in tool_sets[name])
        lines.extend(["---", "", agent_body(source), ""])
        write(destination_root / f"{stem}.md", "\n".join(lines))


def copy_templates(destination_root: Path) -> None:
    for path in (ROOT / "templates").glob("*"):
        if path.is_file():
            copy_file(path, destination_root / "templates" / path.name)


def copy_shared_hooks(destination_root: Path) -> None:
    for name in ("README.md", "pre-trainer-session.ps1", "pre-trainer-session.sh", "post-trainer-session.ps1", "post-trainer-session.sh"):
        copy_file(ROOT / "hooks" / name, destination_root / "hooks" / name)


def write_install(target: Path, instructions: str) -> None:
    write(target / "INSTALL.md", f"# Install\n\n{instructions}\n")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def agent_body(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text.strip()


def build_codex_agents(destination: Path) -> None:
    for name in AGENT_FILES:
        source = AGENTS / name
        stem = name.removesuffix(".agent.md")
        body = agent_body(source).replace('"""', '\\"\\"\\"')
        description = stem.replace("-", " ").title() + " specialist for Microsoft training"
        content = (
            f'name = "{stem}"\n'
            f'description = "{description}"\n'
            'sandbox_mode = "workspace-write"\n'
            'approval_policy = "on-request"\n\n'
            f'developer_instructions = """\n{body}\n"""\n'
        )
        write(destination / f"{stem}.toml", content)


def make_targets() -> None:
    if TARGETS.exists():
        shutil.rmtree(TARGETS)
    TARGETS.mkdir(parents=True, exist_ok=True)

    copilot = TARGETS / "github-copilot"
    copy_file(ROOT / "DESCRIPTION.md", copilot / "DESCRIPTION.md")
    copy_agents(copilot / ".github" / "agents")
    copy_skills(copilot / ".github" / "skills")
    copy_skills(copilot / ".agents" / "skills")
    copy_shared(copilot / ".github")
    copy_templates(copilot)
    copy_file(ROOT / "copilot-instructions.md", copilot / ".github" / "copilot-instructions.md")
    copy_file(ROOT / "AGENT-PACK-README.md", copilot / ".github" / "AGENT-PACK-README.md")
    copy_file(ROOT / "hooks" / "microsoft-certified-trainer.json", copilot / ".github" / "hooks" / "microsoft-certified-trainer.json")
    for name in ("pre-trainer-session.ps1", "pre-trainer-session.sh", "post-trainer-session.ps1", "post-trainer-session.sh"):
        copy_file(ROOT / "hooks" / name, copilot / ".github" / "hooks" / "scripts" / name)
    write_install(copilot, "Copy `.github/` and `.agents/skills/` into the target repository. Use the primary trainer agent directly; specialists are optional.")

    claude = TARGETS / "claude-code"
    copy_file(ROOT / "DESCRIPTION.md", claude / "DESCRIPTION.md")
    copy_claude_agents(claude / ".claude" / "agents")
    copy_skills(claude / ".claude" / "skills")
    copy_shared(claude / "shared")
    copy_shared_hooks(claude / "shared")
    copy_templates(claude)
    copy_file(ROOT / "copilot-instructions.md", claude / "CLAUDE.md")
    write_install(claude, "Copy `.claude/agents` and `.claude/skills` into the project. Keep shared instructions, prompts, examples, and templates available to the session.")

    codex = TARGETS / "openai-codex"
    copy_file(ROOT / "DESCRIPTION.md", codex / "DESCRIPTION.md")
    build_codex_agents(codex / ".codex" / "agents")
    copy_skills(codex / ".agents" / "skills")
    copy_shared(codex / "shared")
    copy_shared_hooks(codex / "shared")
    copy_templates(codex)
    copy_file(ROOT / "copilot-instructions.md", codex / "AGENTS.md")
    write_install(codex, "Copy `.codex/agents` and `.agents/skills` into the project or Codex configuration. Review approval policy before enabling mutations.")

    gemini = TARGETS / "gemini-cli"
    copy_file(ROOT / "DESCRIPTION.md", gemini / "DESCRIPTION.md")
    copy_gemini_agents(gemini / ".gemini" / "agents")
    copy_skills(gemini / ".agents" / "skills")
    copy_shared(gemini / "shared")
    copy_shared_hooks(gemini / "shared")
    copy_templates(gemini)
    copy_file(ROOT / "copilot-instructions.md", gemini / "GEMINI.md")
    write_install(gemini, "Copy `.gemini/agents` and `.agents/skills` into the project. Use shared instructions, prompts, examples, and templates as session context.")


def add_tree(archive: zipfile.ZipFile, source: Path, prefix: str = "") -> None:
    if source.is_file():
        archive.write(source, prefix + source.name)
        return
    if not source.exists():
        return
    for path in source.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            archive.write(path, prefix + path.relative_to(source).as_posix())


def zip_path(source: Path, destination: Path, prefix: str = "") -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        add_tree(archive, source, prefix)


def make_archives() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "skills").mkdir(parents=True, exist_ok=True)
    for vendor in ("github-copilot", "claude-code", "openai-codex", "gemini-cli"):
        zip_path(TARGETS / vendor, DIST / f"{vendor}-microsoft-certified-trainer.zip")
    zip_path(APM, DIST / "microsoft-certified-trainer-canonical.zip")
    zip_path(ROOT / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md", DIST / "microsoft-certified-trainer-prompt.zip")
    for name in SKILL_NAMES:
        zip_path(SKILLS / name, DIST / "skills" / name / "skill.zip")
    zip_path(SKILLS, DIST / "microsoft-certified-trainer-skills.zip")

    validation_zip = DIST / "microsoft-certified-trainer-validation.zip"
    with zipfile.ZipFile(validation_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in (ROOT / "VALIDATION_REPORT.md", ROOT / "tooling" / "validate_pack.py"):
            if path.exists():
                archive.write(path, path.relative_to(ROOT).as_posix())
        add_tree(archive, ROOT / "tests", "tests/")

    full_files = [
        "DESCRIPTION.md", "README.md", "AGENT-PACK-README.md", "copilot-instructions.md",
        "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md", "LICENSE", "apm.yml", "VALIDATION_REPORT.md",
    ]
    full_dirs = [".apm", "compatibility", "docs", "examples", "hooks", "instructions", "prompts", "targets", "templates", "tests", "tooling"]
    full_zip = DIST / "microsoft-certified-trainer-full-pack.zip"
    with zipfile.ZipFile(full_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in full_files:
            if (ROOT / name).exists():
                archive.write(ROOT / name, name)
        for name in full_dirs:
            add_tree(archive, ROOT / name, name + "/")


def main() -> None:
    make_targets()
    make_archives()
    print(f"Built {len(AGENT_FILES)} agents, {len(SKILL_NAMES)} skills, four vendor targets, and archives in {DIST}")


if __name__ == "__main__":
    main()
