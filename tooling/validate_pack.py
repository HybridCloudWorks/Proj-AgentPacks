#!/usr/bin/env python3
"""Validate an agent pack against agent-pack-prompt v2.2 and write its VALIDATION_REPORT.md.

Shared across every pack in this repository. Checks are grouped by kind so the report never
presents an unexecuted check as passed:
  structural       files, manifest fields, frontmatter, naming, stale content, content references,
                   cross-file consistency
  executable       the pack's own unit tests, `apm compile --validate`, optional `apm install`
  not established  live client behaviour; always listed, never claimed

Usage: python tooling/validate_pack.py <pack-folder> [--install-check] [--no-report]
Exit 0 when no check failed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

APM_FIELDS = {"$schema", "name", "version", "description", "author", "license", "homepage", "repository",
              "keywords", "target", "targets", "type", "scripts", "includes", "dependencies",
              "devDependencies", "compilation", "policy", "registries", "marketplace"}
APM_TARGETS = {"copilot", "claude", "codex", "gemini", "kiro", "cursor", "opencode", "windsurf",
               "antigravity", "agent-skills", "grok-build", "hermes"}
AGENT_DIRS = {"copilot": ".github/agents", "claude": ".claude/agents", "codex": ".codex/agents", "kiro": ".kiro/agents"}
REQUIRED = ["apm.yml", "DESCRIPTION.md", "README.md", "LICENSE", "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md",
            "docs", "compatibility", "examples", "templates", "hooks/README.md", "tests",
            ".apm/agents", ".apm/skills", ".apm/instructions", ".apm/prompts"]
STALE = ["targets", "claude-code", "gemini-cli", "github-copilot", "openai-codex", "instructions", "prompts"]
SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
INSTALLED_FORBIDDEN = [
    (r"`shared/|\bshared/(hooks|tooling|examples|instructions|prompts|templates|docs)\b", "shared/ folder does not exist after install"),
    (r"installed repository root", "assumes a repository-root install"),
    (r"(?<![\w-])targets/", "hand-built targets are gone"),
    (r"(?i)\b(read|reads|use|uses|consult|see|load|open)\b[^.\n]{0,60}\b(CLAUDE\.md|AGENTS\.md|GEMINI\.md|copilot-instructions\.md)", "tells the model to read a repository context file the pack does not install"),
    (r"\.github/hooks", "repository hook path"),
    (r"\bINSTALL\.md\b", "removed file"),
    (r"\bdocs/[A-Za-z_]+\.md", "pack docs are not installed"),
    (r"\btests/[\w.-]+\.(yml|yaml|md|json)", "pack tests are not installed"),
    (r"\btemplates/[\w.-]+\.(md|py)", "pack templates are not installed"),
]
PACK_DOC_FORBIDDEN = [
    (r"(?<![\w-])targets/", "hand-built targets are gone"),
    (r"`shared/|\bshared/(hooks|tooling|examples|instructions|prompts|templates|docs)\b", "shared/ folder does not exist"),
    (r"four vendor|generated targets|28-section", "describes the old layout"),
    (r"\bINSTALL\.md\b", "removed file"),
    (r"(?<![.\w/`])(instructions|prompts)/(?=[\w.-]+\.(md|yml))", "instructions and prompts live under .apm/"),
]
NOT_ESTABLISHED = [
    "Agents appear and run in the VS Code agent pane for Claude Code, Codex, and GitHub Copilot.",
    "A user-profile install (Code Workflow installer, or `apm install -g`) behaves identically on Windows and macOS.",
    "Kiro and Antigravity IDE behaviour, and Gemini CLI behaviour, on a live install.",
    "Model behaviour of the agents when actually invoked; tests cover helper code and contracts only.",
    "Hook behaviour: hooks ship as helper scripts and samples; no native hook was installed or exercised.",
]


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, str]] = []

    def add(self, kind: str, check: str, ok: bool | None, detail: str = "") -> None:
        status = "skipped" if ok is None else ("pass" if ok else "FAIL")
        self.rows.append((kind, check, status, detail))

    def failures(self) -> list[tuple[str, str, str, str]]:
        return [r for r in self.rows if r[2] == "FAIL"]


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.DOTALL)
    if not m:
        return {}, text
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            fields[km.group(1)] = km.group(2).strip().strip("\"'")
    return fields, m.group(2)


def simple_yaml(path: Path) -> dict[str, object]:
    """Enough YAML for apm.yml: scalars, inline lists, and block lists of scalars."""
    data: dict[str, object] = {}
    key: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\s*-\s+", line) and key is not None:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(line.split("-", 1)[1].strip().strip("\"'"))
            continue
        m = re.match(r"^([A-Za-z_$][\w-]*):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                data[key] = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
            elif value:
                data[key] = value.strip("\"'")
            else:
                data[key] = []
    return data


def structural(root: Path, rep: Report) -> dict[str, object]:
    for rel in REQUIRED:
        rep.add("structural", f"required artifact {rel}", (root / rel).exists())
    for rel in STALE:
        rep.add("structural", f"no stale folder {rel}/", not (root / rel).exists())
    cache = [p for p in list(root.rglob("__pycache__")) + list(root.rglob("*.pyc")) if p.parts[len(root.parts)] not in ("tests", "tooling")]
    rep.add("structural", "no __pycache__ or .pyc outside tests/ and tooling/", not cache, ", ".join(str(p.relative_to(root)) for p in cache[:3]))
    rep.add("structural", "no archives at pack root", not any(root.glob("*.zip")))
    rep.add("structural", "no native hook JSON for APM to deploy",
            not any((root / "hooks").glob("*.json")) and not (root / ".apm" / "hooks").exists(),
            "native hooks would carry repository-relative commands; hooks ship as helper scripts and samples")
    for rel in ("tooling/validate_pack.py", "tooling/build_pack.py"):
        rep.add("structural", f"no per-pack copy of {rel} (shared tooling lives at the repository root)", not (root / rel).exists())

    manifest = simple_yaml(root / "apm.yml")
    unknown = sorted(set(manifest) - APM_FIELDS)
    rep.add("structural", "apm.yml uses only APM-defined fields", not unknown, f"unknown: {unknown}" if unknown else "")
    rep.add("structural", "apm.yml has name and version", bool(manifest.get("name")) and bool(manifest.get("version")))
    rep.add("structural", "apm.yml version is semantic", bool(re.match(r"^\d+\.\d+\.\d+", str(manifest.get("version", "")))))
    rep.add("structural", "apm.yml name equals the pack folder name without -pack", manifest.get("name") == root.name.removesuffix("-pack"), f"{manifest.get('name')} vs {root.name}")
    targets = manifest.get("targets") or []
    bad = sorted(set(targets) - APM_TARGETS) if isinstance(targets, list) else ["not a list"]
    rep.add("structural", "apm.yml targets are valid APM targets", bool(targets) and not bad, f"targets: {targets}")

    agents = sorted((root / ".apm" / "agents").glob("*.agent.md"))
    rep.add("structural", "at least one agent", bool(agents))
    primaries = 0
    names: list[str] = []
    for path in agents:
        fm, body = frontmatter(path)
        name = fm.get("name", "")
        names.append(name)
        stem = path.name[: -len(".agent.md")]
        rep.add("structural", f"agent {stem}: name and description present", bool(name) and bool(fm.get("description")))
        rep.add("structural", f"agent {stem}: file name equals name", name == stem)
        rep.add("structural", f"agent {stem}: no tools field (declared in compatibility/tool-permissions.yml)", "tools" not in fm)
        rep.add("structural", f"agent {stem}: description within 1024 characters", len(fm.get("description", "")) <= 1024)
        rep.add("structural", f"agent {stem}: body within 300 lines", len(body.splitlines()) <= 300)
        if fm.get("user-invocable", "true").lower() != "false":
            primaries += 1
    rep.add("structural", "exactly one user-invocable primary agent", primaries == 1, f"user-invocable agents: {primaries}")

    perm_path = root / "compatibility" / "tool-permissions.yml"
    if perm_path.is_file():
        declared = set(re.findall(r"^  ([a-z0-9_-]+):\s*$", perm_path.read_text(encoding="utf-8"), re.M))
        rep.add("structural", "tool-permissions.yml covers every agent", declared == set(names), f"missing: {sorted(set(names) - declared)}")
    else:
        rep.add("structural", "tool-permissions.yml present", False)

    skills = sorted(p for p in (root / ".apm" / "skills").iterdir() if p.is_dir())
    rep.add("structural", "at least one skill", bool(skills))
    for skill in skills:
        fm, _ = frontmatter(skill / "SKILL.md") if (skill / "SKILL.md").is_file() else ({}, "")
        rep.add("structural", f"skill {skill.name}: SKILL.md with name equal to folder", fm.get("name") == skill.name and bool(SLUG.match(skill.name)))
        rep.add("structural", f"skill {skill.name}: description within 1024 characters", 0 < len(fm.get("description", "")) <= 1024)
    instructions = sorted((root / ".apm" / "instructions").glob("*.instructions.md"))
    for path in instructions:
        fm, _ = frontmatter(path)
        rep.add("structural", f"instruction {path.name}: description and applyTo", bool(fm.get("description")) and bool(fm.get("applyTo")))
    prompts = sorted((root / ".apm" / "prompts").glob("*.prompt.md"))
    for path in prompts:
        fm, _ = frontmatter(path)
        rep.add("structural", f"prompt {path.name}: description", bool(fm.get("description")))
    prompt_path = root / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md"
    prompt_text = prompt_path.read_text(encoding="utf-8", errors="replace") if prompt_path.is_file() else ""
    rep.add("structural", "authoring prompt is version 2.2 or later", bool(re.search(r"Prompt version 2\.[2-9]|Prompt version [3-9]", prompt_text)))
    return {"manifest": manifest, "agents": names, "skills": [s.name for s in skills],
            "prompts": len(prompts), "instructions": len(instructions)}


def content_scan(root: Path, rep: Report) -> None:
    """Installed content may reference only what is installed with it; pack docs may not describe the old layout."""
    for path in sorted((root / ".apm").rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [f"{reason}: {m.group(0)}" for pattern, reason in INSTALLED_FORBIDDEN for m in [re.search(pattern, text)] if m]
        rep.add("structural", f"installed content {path.relative_to(root).as_posix()}: references only installed things", not hits, "; ".join(hits))
    docs = [root / "README.md", root / "DESCRIPTION.md", root / "hooks" / "README.md"]
    docs += sorted((root / "docs").glob("*.md")) + sorted((root / "compatibility").glob("*.yml"))
    for path in docs:
        if not path.is_file() or path.name == "DESIGN_DECISIONS.md":
            continue  # a decision log may describe the layouts it replaced
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [f"{reason}: {m.group(0)}" for pattern, reason in PACK_DOC_FORBIDDEN for m in [re.search(pattern, text)] if m]
        rep.add("structural", f"pack doc {path.relative_to(root).as_posix()}: describes the current layout", not hits, "; ".join(hits))


def _strings(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for k, v in value.items() for s in ([k] if isinstance(k, str) else []) + _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    return []


def consistency(root: Path, rep: Report, info: dict[str, object]) -> None:
    """tests/*.yml and the contract instruction must agree with the real agents, skills and prompts.
    Test metadata comes in several legacy schemas, so the checks work on the strings they contain."""
    skills = set(info["skills"])  # type: ignore[arg-type]
    prompts = {p.name for p in (root / ".apm" / "prompts").glob("*.prompt.md")}

    def load(rel: str):
        path = root / rel
        if not path.is_file():
            rep.add("structural", f"{rel} present", False)
            return None
        text = path.read_text(encoding="utf-8")
        try:
            import yaml  # type: ignore
            return yaml.safe_load(text)
        except ImportError:
            try:
                return json.loads(text)
            except json.JSONDecodeError as exc:
                rep.add("structural", f"{rel} parses (PyYAML not installed, JSON fallback)", False, str(exc))
                return None
        except Exception as exc:  # yaml.YAMLError
            rep.add("structural", f"{rel} is valid YAML", False, str(exc)[:160])
            return None

    cov = load("tests/skill-coverage.yml")
    if isinstance(cov, dict) and isinstance(cov.get("skills"), dict):
        listed = set(cov["skills"])
        rep.add("structural", "tests/skill-coverage.yml lists exactly the shipped skills", listed == skills,
                f"missing: {sorted(skills - listed)[:5]} extra: {sorted(listed - skills)[:5]}")
        empty = [k for k, v in cov["skills"].items() if not (isinstance(v, dict) and v.get("activation"))]
        rep.add("structural", "tests/skill-coverage.yml has an activation statement for every skill", not empty, ", ".join(empty[:5]))
    elif cov is not None:
        rep.add("structural", "tests/skill-coverage.yml has the expected shape", False, "expected a skills mapping")
    for rel in ("tests/capability-coverage.yml", "tests/trigger-cases.yml"):
        data = load(rel)
        if data is None:
            continue
        strings = _strings(data)
        unknown = sorted({s for s in strings if re.match(r"^[a-z0-9]+(-[a-z0-9]+)+$", s) and s in skills} ^ {s for s in strings if s in skills})
        bad = sorted({s for s in strings if s.endswith(".prompt.md")} - prompts)
        rep.add("structural", f"{rel} prompt files exist", not bad, ", ".join(bad))
        if isinstance(data, dict) and "requirements" in data:
            reqs = data["requirements"]
            rep.add("structural", f"{rel} names every skill exactly once",
                    sorted(r.get("skill") for r in reqs) == sorted(skills), f"{len(reqs)} requirements for {len(skills)} skills")

    rc = load("tests/report-contract.yml")
    contract = next(iter((root / ".apm" / "instructions").glob("*contract*.instructions.md")), None)
    rep.add("structural", "an always-on contract instruction exists (.apm/instructions/*contract*.instructions.md)", contract is not None)
    if isinstance(rc, dict) and contract:
        raw = contract.read_text(encoding="utf-8")
        text = raw.lower().replace("-", "").replace("_", "").replace(" ", "")
        expected = [s for k, v in rc.items() if isinstance(v, list) for s in v if isinstance(s, str) and len(s) <= 48]
        missing = [s for s in expected if s.lower().replace("_", "").replace("-", "").replace(" ", "") not in text]
        rep.add("structural", "contract instruction states every short value listed in report-contract.yml", not missing, ", ".join(missing[:6]))
        fallback = rc.get("fallback")
        if isinstance(fallback, str):
            rep.add("structural", "contract instruction states the fallback sentence", fallback in raw)
        defined = {s for v in rc.values() if isinstance(v, list) for s in v if isinstance(s, str)}
        status_like = set()
        for path in (root / ".apm").rglob("*.md"):
            status_like |= set(re.findall(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b", path.read_text(encoding="utf-8", errors="replace")))
        status_words = {"READY", "VERIFIED", "BLOCKED", "COMPLETE", "COMPLETED", "REQUIRED", "ANALYSIS", "PREPARED", "APPROVED",
                        "FAILED", "PASSED", "PENDING", "PARTIAL", "SKIPPED", "REVIEW", "MERGE", "DECISION", "VERIFY"}
        status_like = {s for s in status_like if set(s.split("_")) & status_words}
        undefined = sorted(status_like - defined)
        rep.add("structural", "status names used in installed content are defined in report-contract.yml", not undefined, ", ".join(undefined[:6]))


def executable(root: Path, rep: Report, info: dict[str, object], install_check: bool) -> None:
    tests = root / "tests"
    if any(tests.glob("test_*.py")):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        proc = subprocess.run([sys.executable, "-I", "-B", "-m", "unittest", "discover", "-s", "tests"],
                              cwd=root, capture_output=True, text=True, env=env)
        tail = (proc.stderr or proc.stdout).strip().splitlines()[-1:] or [""]
        rep.add("executable", "pack unit tests (python -m unittest discover -s tests)", proc.returncode == 0, tail[0])
    else:
        rep.add("executable", "pack unit tests", None, "no test_*.py in tests/")

    apm = shutil.which("apm")
    if not apm:
        rep.add("executable", "apm compile --validate", None, "apm CLI not on PATH")
        rep.add("executable", "apm install into a scratch project", None, "apm CLI not on PATH")
        return
    proc = subprocess.run([apm, "compile", "--validate"], cwd=root, capture_output=True, text=True)
    rep.add("executable", "apm compile --validate", proc.returncode == 0,
            next((l.strip() for l in proc.stdout.splitlines() if "primitives" in l), proc.stderr.strip()[-200:]))
    if not install_check:
        rep.add("executable", "apm install into a scratch project", None, "run with --install-check")
        return
    manifest = info["manifest"]
    assert isinstance(manifest, dict)
    targets = [t for t in manifest.get("targets", []) if t in APM_TARGETS]
    agent_names = info["agents"]
    assert isinstance(agent_names, list)
    with tempfile.TemporaryDirectory(prefix="pack-install-") as tmp:
        subprocess.run(["git", "init", "-q"], cwd=tmp, capture_output=True)
        proc = subprocess.run([apm, "install", "--target", ",".join(targets), str(root)], cwd=tmp, capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        ok = proc.returncode == 0 and "installation failed" not in out.lower()
        rep.add("executable", f"apm install --target {','.join(targets)} succeeds", ok, "" if ok else out.strip()[-300:])
        generated = [p for p in Path(tmp).rglob("*") if p.is_file() and not ({"apm_modules", ".git"} & set(p.parts))]
        for target, folder in AGENT_DIRS.items():
            if target in targets:
                count = len([p for p in generated if folder in p.as_posix()])
                rep.add("executable", f"{target}: {len(agent_names)} agents generated", count == len(agent_names), f"found {count}")
        hooks = [p for p in generated if "hooks" in p.parts or p.name in ("settings.json", "apm-hooks.json")]
        rep.add("executable", "no hook files generated", not hooks, ", ".join(p.name for p in hooks[:5]))
        rules = len([p for p in generated if ".claude/rules" in p.as_posix()])
        rep.add("executable", "claude: instructions generated as rules", rules == info["instructions"], f"found {rules}")
        text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in generated if p.suffix in (".md", ".toml"))
        hits = [f"{reason}: {m.group(0)}" for pattern, reason in INSTALLED_FORBIDDEN for m in [re.search(pattern, text)] if m]
        rep.add("executable", "generated vendor files reference only installed things", not hits, "; ".join(hits))


def prompt_version(root: Path) -> str:
    path = root / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md"
    m = re.search(r"Prompt version ([0-9]+(?:\.[0-9]+)?)", path.read_text(encoding="utf-8", errors="replace")) if path.is_file() else None
    return m.group(1) if m else "unknown"


def render(root: Path, rep: Report, info: dict[str, object]) -> str:
    manifest = info["manifest"]
    assert isinstance(manifest, dict)
    fails = rep.failures()
    passed = sum(r[2] == "pass" for r in rep.rows)
    skipped = sum(r[2] == "skipped" for r in rep.rows)
    lines = ["# VALIDATION_REPORT", "",
             f"Pack: {manifest.get('name')} {manifest.get('version')}",
             f"Standard: agent-pack-prompt v{prompt_version(root)}",
             f"Validated: {dt.date.today().isoformat()}",
             f"Status: {'PASS' if not fails else 'FAIL'}", "",
             f"Checks: {len(rep.rows)}  Passed: {passed}  Failed: {len(fails)}  Skipped: {skipped}", "",
             "## Scope", "",
             f"{len(info['agents'])} agents, {len(info['skills'])} skills, {info['instructions']} instruction files, "  # type: ignore[arg-type]
             f"{info['prompts']} prompts; targets {', '.join(manifest.get('targets', []))}.", "",
             "## Failed checks", ""]
    lines += [f"- {c}: {d}" for _, c, _, d in fails] or ["- None"]
    lines += ["", "## Not established", ""] + [f"- {n}" for n in NOT_ESTABLISHED]
    lines += ["", "## Check inventory", "", "| Kind | Check | Result | Detail |", "|---|---|---|---|"]
    lines += [f"| {k} | {c} | {s} | {d.replace('|', '/')} |" for k, c, s, d in rep.rows]
    return "\n".join(lines) + "\n"


def validate(root: Path, install_check: bool, write_report: bool) -> tuple[Report, dict[str, object]]:
    rep = Report()
    info = structural(root, rep)
    content_scan(root, rep)
    consistency(root, rep, info)
    executable(root, rep, info, install_check)
    if write_report:
        (root / "VALIDATION_REPORT.md").write_text(render(root, rep, info), encoding="utf-8")
    return rep, info


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pack", help="pack folder")
    parser.add_argument("--install-check", action="store_true", help="also run apm install into a scratch project")
    parser.add_argument("--no-report", action="store_true", help="do not write VALIDATION_REPORT.md")
    args = parser.parse_args()
    root = Path(args.pack).resolve()
    if not (root / "apm.yml").is_file():
        print(f"not a pack (no apm.yml): {root}")
        return 2
    rep, _ = validate(root, args.install_check, not args.no_report)
    fails = rep.failures()
    skipped = sum(r[2] == "skipped" for r in rep.rows)
    print(f"{root.name}: {'PASS' if not fails else 'FAIL'}: {len(rep.rows)} checks, {len(fails)} failures, {skipped} skipped")
    for _, check, _, detail in fails:
        print(f"  FAIL {check}: {detail}")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
