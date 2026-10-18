"""Verify canonical contracts, generated targets, local evidence and archive contents."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tomllib
import zipfile

import yaml

ROOT = Path(__file__).resolve().parent.parent
VENDORS = {
    "github-copilot": (".github/agents", ".github/skills", ".agent.md"),
    "claude-code": (".claude/agents", ".claude/skills", ".md"),
    "openai-codex": (".codex/agents", ".agents/skills", ".toml"),
    "gemini-cli": (".gemini/agents", ".agents/skills", ".md"),
}
SKIP = {"__pycache__", ".git", ".pytest_cache"}
BEHAVIOR_FILES = ("tests/test_behavior.py", "tooling/completion_contract.py", "tooling/hook_runner.py", "tooling/validate_python_pack.py", "templates/api_contract.py", "tests/fixtures/valid-completion.json", "tests/fixtures/invalid-completion.json")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fm(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError("Missing YAML frontmatter")
    header = yaml.safe_load(parts[1])
    if not isinstance(header, dict):
        raise ValueError("Invalid frontmatter")
    return header, parts[2]


def paths(directory: Path) -> list[Path]:
    return sorted(p for p in directory.rglob("*") if p.is_file() and not any(s in SKIP for s in p.parts))


def audit(root: Path, archives: bool = True, check_report: bool = True) -> dict:
    result: dict = {"checks": [], "failures": []}
    def expect(ok: bool, label: str) -> None:
        result["checks"].append(label)
        if not ok:
            result["failures"].append(label)
    def load(path: Path):
        try:
            return yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, yaml.YAMLError):
            expect(False, "parse " + str(path.relative_to(root)))
            return {}

    manifest = load(root / "compatibility/capability-map.yml")
    agents, skills = manifest.get("agents", []), manifest.get("skills", [])
    expect(len(agents) == 5 and sum(a.get("user_invocable", False) for a in agents) == 1, "five agents and one user-facing primary")
    expect(len(skills) == 18 and len({s["name"] for s in skills}) == 18, "eighteen unique canonical Skills")
    expected_agents = {a["name"] + ".agent.md" for a in agents}
    expect({p.name for p in (root / ".apm/agents").glob("*")} == expected_agents, "exact canonical agent inventory")
    expect({p.name for p in (root / ".apm/skills").iterdir()} == {s["name"] for s in skills}, "exact canonical Skill directories without legacy seed content")
    for source in manifest.get("root_files", []):
        if source not in {"AGENT-PACK-README.md", "VALIDATION_REPORT.md"} or archives:
            expect((root / source).is_file(), "root artifact " + source)
    for group in manifest.get("source_dirs", []):
        expect((root / group).is_dir() and bool(paths(root / group)), "artifact category " + group)
    for file in paths(root):
        relative = file.relative_to(root)
        if "dist" in relative.parts or "targets" in relative.parts:
            continue
        expect(not file.is_symlink(), "no source symlink " + relative.as_posix())
        if file.suffix in {".yml", ".yaml", ".json"}:
            load(file)
            expect(True, "structured source " + relative.as_posix())
        if file.suffix == ".py":
            try:
                ast.parse(file.read_text(encoding="utf-8"))
                expect(True, "Python syntax " + relative.as_posix())
            except SyntaxError:
                expect(False, "Python syntax " + relative.as_posix())
    for agent in agents:
        header, body = fm(root / ".apm/agents" / (agent["name"] + ".agent.md"))
        expect(header.get("tools") == agent["tools"] and header.get("user-invocable") == agent["user_invocable"], "canonical invocation/tools " + agent["name"])
        expect(len(body.splitlines()) <= 150, "thin profile " + agent["name"])
    for skill in skills:
        name = skill["name"]
        file = root / ".apm/skills" / name / "SKILL.md"
        header, body = fm(file)
        expect(header.get("name") == name and bool(header.get("description")), "Skill discovery " + name)
        expect(all(section in body for section in ("Activation and scope", "Inputs and dependencies", "Workflow", "Output and validation", "Failure and guardrails", "Workflow connection")), "operational Skill contract " + name)
        expect((root / "prompts" / (skill["prompt"] + ".prompt.md")).is_file(), "Skill prompt reference " + name)
        for text in ("microsoft-certified-trainer", "cloud-documentation-archivist", "aws-diagram-architect", "terraform-expert-engineer"):
            expect(text not in body.lower(), "no unrelated persona " + name + " " + text)
    for name in manifest.get("instructions", []):
        header, body = fm(root / "instructions" / name)
        expect(isinstance(header.get("applyTo"), str) and bool(body.strip()), "scoped instruction " + name)
    for name in manifest.get("prompts", []):
        header, body = fm(root / "prompts" / name)
        expect(header.get("agent") == manifest["primary"] and "Expected output" in body, "prompt output/owner " + name)
    for name in manifest.get("examples", []):
        expect((root / "examples" / name).is_file(), "worked example " + name)
    coverage = load(root / "tests/capability-coverage.yml")
    expect({c["skill"] for c in coverage.get("requirements", [])} == {s["name"] for s in skills}, "capability ownership covers all Skills")
    for item in coverage.get("requirements", []):
        expect(item["agent"] in {a["name"] for a in agents} and item["prompt"] in manifest["prompts"], "coverage reference " + item["id"])
    triggers = load(root / "tests/trigger-cases.yml")
    expect({s for c in triggers.get("cases", []) for s in c["skills"]} == {s["name"] for s in skills}, "positive activation coverage")
    expect(len(triggers.get("negative_cases", [])) >= 8, "negative guardrail activation cases")
    for vendor, (agent_dir, skill_dir, extension) in VENDORS.items():
        target = root / "targets" / vendor
        expect({p.name for p in (target / agent_dir).glob("*")} == {a["name"] + extension for a in agents}, "vendor agent inventory " + vendor)
        expect({p.name for p in (target / skill_dir).glob("*")} == {s["name"] for s in skills}, "vendor Skill inventory " + vendor)
        for agent in agents:
            path = target / agent_dir / (agent["name"] + extension)
            try:
                if vendor == "openai-codex":
                    header = tomllib.loads(path.read_text(encoding="utf-8"))
                    expect(not ({"approval_policy", "sandbox_mode"} & set(header)), "Codex parent permission inheritance " + agent["name"])
                    expect(set(header) == {"name", "description", "developer_instructions"}, "Codex custom profile fields " + agent["name"])
                else:
                    header, _ = fm(path)
                    expect(header.get("tools") == agent["tools"] if vendor == "github-copilot" else header.get("tools") == agent["claude_tools"] if vendor == "claude-code" else header.get("tools") == agent["gemini_tools"], "host tool mapping " + vendor + " " + agent["name"])
                expect(header.get("name") == agent["name"] and bool(header.get("description")), "host frontmatter " + vendor + " " + agent["name"])
            except (OSError, ValueError, yaml.YAMLError):
                expect(False, "host parse " + vendor + " " + agent["name"])
        for skill in skills:
            source = root / ".apm/skills" / skill["name"]
            for file in paths(source):
                output = target / skill_dir / skill["name"] / file.relative_to(source)
                expect(output.is_file() and output.read_bytes() == file.read_bytes(), "Skill byte parity " + vendor + " " + skill["name"] + "/" + file.name)
        for contract in ("docs/HANDOFF_CONTRACT.md", "docs/APPROVAL_MATRIX.md", "tests/report-contract.yml", "templates/completion-report.md", "INSTALL.md"):
            expect((target / contract).is_file(), "installed reference " + vendor + " " + contract)
    copilot = root / "targets/github-copilot/.github"
    for directory in ("instructions", "prompts", "examples"):
        for file in paths(root / directory):
            target = copilot / directory / file.relative_to(root / directory)
            expect(target.is_file() and target.read_bytes() == file.read_bytes(), "Copilot shared parity " + directory + "/" + file.name)
    hooks = load(copilot / "hooks/python-engineering.json")
    expect(hooks.get("version") == 1 and set(hooks.get("hooks", {})) == {"sessionStart", "agentStop"}, "native hook lifecycle schema")
    for event, definitions in hooks.get("hooks", {}).items():
        for definition in definitions:
            expect(definition.get("cwd") == "." and 0 < definition.get("timeoutSec", 0) <= 10, "bounded hook " + event)
            expect(".github/hooks/scripts/hook_runner.py " + event in definition.get("bash", "") and ".github/hooks/scripts/hook_runner.py " + event in definition.get("powershell", ""), "cross-platform hook commands " + event)
    for name in ("hook_runner.py", "completion_contract.py"):
        target = copilot / "hooks/scripts" / name
        expect(target.is_file() and target.read_bytes() == (root / "tooling" / name).read_bytes(), "hook dependency parity " + name)
    behavior = load(root / "tests/behavior-results.json")
    expect(behavior.get("exit_code") == 0 and behavior.get("test_count", 0) >= 19, "offline behavior suite executed successfully")
    for name in BEHAVIOR_FILES:
        expect(behavior.get("source_sha256", {}).get(name) == digest(root / name), "behavior evidence fresh " + name)
    if archives:
        dist = root / "dist"
        expected = [manifest["name"] + suffix for suffix in ("-full-pack.zip", "-canonical.zip", "-prompt.zip", "-skills.zip", "-validation.zip")]
        expected += [vendor + "-" + manifest["name"] + ".zip" for vendor in VENDORS]
        expect({p.name for p in dist.glob("*.zip")} == set(expected), "exact archive family inventory")
        for file in sorted(dist.rglob("*.zip")):
            with zipfile.ZipFile(file) as archive:
                names = archive.namelist()
                expect(bool(names) and len(names) == len(set(names)) and archive.testzip() is None, "ZIP integrity " + file.relative_to(dist).as_posix())
                expect(all(not n.startswith("/") and ".." not in PurePosixPath(n).parts and not re.match(r"^[A-Za-z]:", n) and "\\" not in n for n in names), "ZIP path safety " + file.relative_to(dist).as_posix())
                expect(not any("__pycache__" in n or n.endswith(".pyc") for n in names), "ZIP excludes cache " + file.relative_to(dist).as_posix())
                if file.name == "skill.zip":
                    source = root / ".apm/skills" / file.parent.name
                    expect("SKILL.md" in names and {p.relative_to(source).as_posix() for p in paths(source)} == set(names), "individual Skill contents " + file.parent.name)
                    expect(all(archive.read(p.relative_to(source).as_posix()) == p.read_bytes() for p in paths(source)), "individual Skill bytes " + file.parent.name)
                if file.name in {manifest["name"] + "-full-pack.zip", manifest["name"] + "-validation.zip"}:
                    expect("VALIDATION_REPORT.md" in names and (not check_report or archive.read("VALIDATION_REPORT.md") == (root / "VALIDATION_REPORT.md").read_bytes()), "embedded report freshness " + file.name)
                if file.name == manifest["name"] + "-full-pack.zip":
                    for group in manifest["source_dirs"] + ["targets"]:
                        expect(any(n.startswith(group + "/") for n in names), "full-pack category " + group)
                expected_members = None
                if file.name == manifest["name"] + "-full-pack.zip":
                    full_sources = [root / name for name in manifest["root_files"]]
                    for group in manifest["source_dirs"] + ["targets"]:
                        full_sources.extend(paths(root / group))
                    expected_members = {p.relative_to(root).as_posix(): p for p in full_sources}
                elif file.name == manifest["name"] + "-canonical.zip":
                    expected_members = {p.relative_to(root).as_posix(): p for p in paths(root / ".apm")}
                elif file.name == manifest["name"] + "-prompt.zip":
                    expected_members = {"PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md": root / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md"}
                elif file.name == manifest["name"] + "-skills.zip":
                    expected_members = {p.relative_to(dist / "skills").as_posix(): p for p in (dist / "skills").rglob("skill.zip")}
                elif file.name == manifest["name"] + "-validation.zip":
                    validation_sources = [root / "VALIDATION_REPORT.md"]
                    for group in ("tests", "tooling", "compatibility", "templates"):
                        validation_sources.extend(paths(root / group))
                    expected_members = {p.relative_to(root).as_posix(): p for p in validation_sources}
                if expected_members is not None:
                    comparable = {name: path for name, path in expected_members.items() if check_report or name not in {"VALIDATION_REPORT.md", "AGENT-PACK-README.md"}}
                    expect(set(names) == set(expected_members) and all(archive.read(name) == path.read_bytes() for name, path in comparable.items()), "primary/bundle byte parity " + file.name)
                for vendor in VENDORS:
                    if file.name == vendor + "-" + manifest["name"] + ".zip":
                        source = root / "targets" / vendor
                        expect(set(names) == {p.relative_to(source).as_posix() for p in paths(source)} and all(archive.read(p.relative_to(source).as_posix()) == p.read_bytes() for p in paths(source)), "vendor archive parity " + vendor)
        expect(len(list((dist / "skills").glob("*/skill.zip"))) == 18, "eighteen individual Skill archives")
        sums = dist / "SHA256SUMS.txt"
        expect(sums.is_file(), "archive checksum manifest")
        if sums.is_file():
            lines = [line.split("  ", 1) for line in sums.read_text().splitlines()]
            expect(len(lines) == len(list(dist.rglob("*.zip"))) and all((dist / name).is_file() and digest(dist / name) == value for value, name in lines), "all archive SHA256 checksums match")
        catalog = root / "AGENT-PACK-README.md"
        text = catalog.read_text(encoding="utf-8") if catalog.is_file() else ""
        expect(all(title in text for title in ("ARTIFACT NAME:", "PURPOSE:", "CONTENT:", "AGENT PACK VALIDATION SUMMARY", "## 28.")), "ordered full-content artifact catalog")
    return result


def render(result: dict) -> str:
    status = "PASS" if not result["failures"] else "FAIL"
    lines = ["# VALIDATION_REPORT", "", "Agent: Python Distinguished Engineer", "Pack version: 2.0.0", "Validation date: 2026-10-18", "Status: " + status, "", "Checks: " + str(len(result["checks"])), "Failures: " + str(len(result["failures"])), "", "## Verified scope", "", "Canonical five-profile/eighteen-Skill architecture; one Copilot user-facing primary; operational Skills/instructions/prompts/examples; host metadata, references and byte parity; bounded JSON hooks; recorded offline behavioral tests with source hashes; deterministic archive structure/path/integrity/parity/checksums and embedded report freshness.", "", "## Behavior evidence", "", "The build executes python -m unittest discover -s tests -p test_behavior.py -v. tests/behavior-results.json records the observed result and hashes. Tests cover runtime validation, replay conflict/idempotency, tenant/scope isolation, cancellation/deadlines, completion evidence, malformed/stale hook input, bounded retry, redaction and read-only syntax inventory. These are local helper/domain tests.", "", "## Not established", "", "Live discovery/invocation in four vendor clients, actual MCP SDK/protocol initialization, browser sessions, remote auth/role enforcement, cloud deployment, production performance, paid model evaluation quality, organizational release thresholds and APM CLI compilation remain unverified. Manual activation cases in tests/trigger-cases.yml are not reported as executed model behaviors. Role instructions do not create security isolation.", "", "## Failed checks", ""]
    lines += ["- " + s for s in result["failures"]] or ["- None"]
    lines += ["", "## Check inventory", ""] + ["- " + s for s in result["checks"]]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true", help="Write source report; rebuild archives afterwards before final delivery.")
    args = parser.parse_args()
    result = audit(ROOT)
    if args.write_report:
        (ROOT / "VALIDATION_REPORT.md").write_text(render(result), encoding="utf-8")
    print(("PASS" if not result["failures"] else "FAIL") + ": " + str(len(result["checks"])) + " checks, " + str(len(result["failures"])) + " failures")
    print("\n".join(result["failures"]))
    return int(bool(result["failures"]))


if __name__ == "__main__":
    raise SystemExit(main())
