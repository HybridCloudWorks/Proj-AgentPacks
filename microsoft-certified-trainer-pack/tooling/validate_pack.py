"""Static validator for the Microsoft Certified Trainer portable pack."""

from __future__ import annotations

import argparse
import json
import py_compile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AGENTS = [
    "microsoft-certified-trainer.agent.md", "microsoft-course-architect.agent.md",
    "microsoft-lab-demo-engineer.agent.md", "microsoft-courseware-engineer.agent.md",
    "microsoft-copilot-learning-reviewer.agent.md",
]
SKILLS = [
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
VENDORS = {
    "github-copilot": (Path(".github/agents"), Path(".github/skills")),
    "claude-code": (Path(".claude/agents"), Path(".claude/skills")),
    "openai-codex": (Path(".codex/agents"), Path(".agents/skills")),
    "gemini-cli": (Path(".gemini/agents"), Path(".agents/skills")),
}


class Report:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.failed: list[str] = []

    def ok(self, message: str) -> None:
        self.passed.append(message)

    def fail(self, message: str) -> None:
        self.failed.append(message)


def exists(report: Report, path: Path, label: str | None = None) -> bool:
    if path.exists():
        report.ok(label or f"exists: {path.relative_to(ROOT)}")
        return True
    report.fail(label or f"missing: {path.relative_to(ROOT)}")
    return False


def frontmatter_ok(text: str) -> bool:
    return text.startswith("---\n") and "\nname:" in text and "\ndescription:" in text and "\n---" in text


def check_canonical(report: Report) -> None:
    for name in AGENTS:
        path = ROOT / ".apm" / "agents" / name
        if exists(report, path):
            text = path.read_text(encoding="utf-8")
            limit = 150 if name == AGENTS[0] else 100
            if frontmatter_ok(text) and len(text.splitlines()) <= limit:
                report.ok(f"canonical agent contract: {name}")
            else:
                report.fail(f"invalid frontmatter or thin-agent limit: {name}")
    actual = sorted(p.name for p in (ROOT / ".apm" / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    if actual == sorted(SKILLS):
        report.ok("canonical Skills: exactly 18 expected Skills")
    else:
        report.fail(f"canonical Skills mismatch: expected {sorted(SKILLS)}, found {actual}")
    for name in SKILLS:
        path = ROOT / ".apm" / "skills" / name / "SKILL.md"
        if exists(report, path):
            text = path.read_text(encoding="utf-8")
            if frontmatter_ok(text) and len(text) >= 250 and "placeholder" not in text.lower():
                report.ok(f"Skill content: {name}")
            else:
                report.fail(f"Skill content/frontmatter too short or placeholder: {name}")


def check_shared(report: Report) -> None:
    for directory, names in (("instructions", INSTRUCTIONS), ("prompts", PROMPTS), ("examples", EXAMPLES)):
        for name in names:
            path = ROOT / directory / name
            if exists(report, path):
                if len(path.read_text(encoding="utf-8").strip()) >= 80:
                    report.ok(f"shared content: {directory}/{name}")
                else:
                    report.fail(f"shared content too short: {directory}/{name}")
    required = [
        "DESCRIPTION.md", "README.md", "AGENT-PACK-README.md", "copilot-instructions.md",
        "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md", "LICENSE", "apm.yml",
        "docs/DESIGN_DECISIONS.md", "docs/SOURCE_TRACEABILITY.md", "docs/MS-4018_SOURCE_NOTES.md",
        "docs/AGENT_INVENTORY.md", "docs/SKILL_INVENTORY.md", "docs/TOOL_PERMISSION_MATRIX.md",
        "docs/APPROVAL_MATRIX.md", "docs/HANDOFF_CONTRACT.md", "docs/PROMPT_INVENTORY.md",
        "docs/DELIVERABLE_CONTRACT.md", "compatibility/capability-map.yml",
        "compatibility/compatibility-matrix.yml", "compatibility/optional-skills.yml",
        "compatibility/vendor-sources.yml", "tests/capability-coverage.yml", "tests/report-contract.yml",
        "tests/trigger-cases.yml", "tests/fixtures/valid-completion-report.md",
        "templates/course-plan.md", "templates/instructor-guide.md", "templates/lab-runbook.md",
        "templates/demo-runbook.md", "templates/knowledge-checks.yml", "templates/session-evaluation.md",
        "templates/partner-handoff.md",
    ]
    for name in required:
        exists(report, ROOT / name)


def skill_names(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {p.name for p in path.iterdir() if p.is_dir() and (p / "SKILL.md").exists()}


def check_targets(report: Report) -> None:
    for vendor, (agent_rel, skill_rel) in VENDORS.items():
        target = ROOT / "targets" / vendor
        agent_path = target / agent_rel
        skill_path = target / skill_rel
        if agent_path.exists():
            count = len(list(agent_path.glob("*.md"))) + len(list(agent_path.glob("*.toml")))
            if count == len(AGENTS):
                report.ok(f"{vendor}: five agents")
            else:
                report.fail(f"{vendor}: expected five agents, found {count}")
        else:
            report.fail(f"{vendor}: missing agent directory")
        if skill_names(skill_path) == set(SKILLS):
            report.ok(f"{vendor}: 18 Skills")
        else:
            report.fail(f"{vendor}: Skill parity mismatch")
        for path in (target / "DESCRIPTION.md", target / "INSTALL.md"):
            exists(report, path)
        exists(report, target / "templates" / "course-plan.md")
        context_file = {
            "claude-code": "CLAUDE.md",
            "openai-codex": "AGENTS.md",
            "gemini-cli": "GEMINI.md",
        }.get(vendor)
        if context_file:
            exists(report, target / context_file)
            for hook_name in ("README.md", "pre-trainer-session.ps1", "pre-trainer-session.sh", "post-trainer-session.ps1", "post-trainer-session.sh"):
                exists(report, target / "shared" / "hooks" / hook_name)
    copilot = ROOT / "targets" / "github-copilot" / ".github"
    for name in INSTRUCTIONS:
        exists(report, copilot / "instructions" / name)
    for name in PROMPTS:
        exists(report, copilot / "prompts" / name)
    for name in EXAMPLES:
        exists(report, copilot / "examples" / name)
    exists(report, copilot / "copilot-instructions.md")
    exists(report, copilot / "AGENT-PACK-README.md")
    hook_config = copilot / "hooks" / "microsoft-certified-trainer.json"
    if exists(report, hook_config):
        try:
            payload = json.loads(hook_config.read_text(encoding="utf-8"))
            if payload.get("version") == 1 and set(payload.get("hooks", {})) == {"sessionStart", "agentStop"}:
                report.ok("Copilot hook configuration: version 1 with sessionStart and agentStop")
            else:
                report.fail("Copilot hook configuration has unexpected structure")
        except json.JSONDecodeError as exc:
            report.fail(f"Copilot hook configuration is invalid JSON: {exc}")
    for name in ("pre-trainer-session.ps1", "pre-trainer-session.sh", "post-trainer-session.ps1", "post-trainer-session.sh"):
        exists(report, copilot / "hooks" / "scripts" / name)
    if skill_names(ROOT / "targets" / "github-copilot" / ".agents" / "skills") == set(SKILLS):
        report.ok("Copilot compatibility skill mirror")
    else:
        report.fail("Copilot compatibility skill mirror mismatch")


def check_tooling(report: Report) -> None:
    for path in (ROOT / "tooling").glob("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            report.fail(f"Python compile failed: {path.relative_to(ROOT)}: {exc.msg}")
        else:
            report.ok(f"Python compile: {path.relative_to(ROOT)}")
    for name in ("pre-trainer-session.ps1", "pre-trainer-session.sh", "post-trainer-session.ps1", "post-trainer-session.sh", "microsoft-certified-trainer.json"):
        exists(report, ROOT / "hooks" / name)


def check_archives(report: Report) -> None:
    expected = [
        "github-copilot-microsoft-certified-trainer.zip", "claude-code-microsoft-certified-trainer.zip",
        "openai-codex-microsoft-certified-trainer.zip", "gemini-cli-microsoft-certified-trainer.zip",
        "microsoft-certified-trainer-canonical.zip", "microsoft-certified-trainer-prompt.zip",
        "microsoft-certified-trainer-skills.zip", "microsoft-certified-trainer-validation.zip",
        "microsoft-certified-trainer-full-pack.zip",
    ]
    for name in expected:
        path = ROOT / "dist" / name
        if exists(report, path):
            with zipfile.ZipFile(path) as archive:
                if archive.testzip() is None and archive.namelist():
                    report.ok(f"archive integrity: {name}")
                else:
                    report.fail(f"archive empty or corrupt: {name}")
    for name in SKILLS:
        path = ROOT / "dist" / "skills" / name / "skill.zip"
        if exists(report, path):
            with zipfile.ZipFile(path) as archive:
                if any(item.endswith("SKILL.md") for item in archive.namelist()):
                    report.ok(f"individual Skill archive: {name}")
                else:
                    report.fail(f"individual Skill archive missing SKILL.md: {name}")


def render(report: Report) -> str:
    status = "PASS" if not report.failed else "FAIL"
    lines = [
        "# VALIDATION REPORT", "", f"Status: **{status}**", "",
        "This is a static, local pack validation. It verifies source structure, frontmatter, required content, target parity, tooling compilation, hook syntax, tests, templates, and archive integrity. It does not prove MCT authorization, courseware redistribution rights, provider or tenant access, live Copilot behavior, Copilot Studio publication, cloud deployment, browser mutation, model quality, or classroom learning outcomes.", "",
        "## Summary", "", "- Five canonical agents, with a fully capable primary trainer agent.", "- Eighteen focused Skills.", "- Six shared instructions, twelve prompts, eight examples, and seven templates.", "- GitHub Copilot, Claude Code, OpenAI Codex, and Gemini CLI targets.", "- Individual validated `skill.zip` archives.", "", f"Checks passed: {len(report.passed)}", f"Checks failed: {len(report.failed)}", "", "## Passed checks", "",
    ]
    lines.extend(f"- {item}" for item in report.passed)
    lines.extend(["", "## Failed checks", ""])
    lines.extend(f"- {item}" for item in report.failed or ["None"])
    lines.extend(["", "## Evidence boundary", "", "Static validation is not live MCT authorization, courseware license proof, tenant or provider behavior, Copilot Studio publication, cloud deployment, external mutation, or verified learning mastery."])
    return "\n".join(lines) + "\n"


def main() -> int:
    global ROOT
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    ROOT = args.root.resolve()
    report = Report()
    check_canonical(report)
    check_shared(report)
    check_targets(report)
    check_tooling(report)
    check_archives(report)
    if args.write_report:
        (ROOT / "VALIDATION_REPORT.md").write_text(render(report), encoding="utf-8")
    print(render(report))
    return 0 if not report.failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
