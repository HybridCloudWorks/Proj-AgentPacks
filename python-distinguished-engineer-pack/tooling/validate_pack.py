#!/usr/bin/env python3
"""Validate this pack against agent-pack-prompt v2 and write VALIDATION_REPORT.md.

Checks are grouped by kind so the report never presents an unexecuted check as passed:
  structural       files, manifest fields, frontmatter, naming, stale content
  executable       the pack's own unit tests, `apm compile --validate`, optional `apm install`
  not established  live client behaviour; always listed, never claimed

Usage: python tooling/validate_pack.py [--install-check] [--no-report]
Exit 0 when no check failed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APM_FIELDS = {"$schema", "name", "version", "description", "author", "license", "homepage", "repository",
              "keywords", "target", "targets", "type", "scripts", "includes", "dependencies",
              "devDependencies", "compilation", "policy", "registries", "marketplace"}
APM_TARGETS = {"copilot", "claude", "codex", "gemini", "kiro", "cursor", "opencode", "windsurf",
               "antigravity", "agent-skills", "grok-build", "hermes"}
AGENT_DIRS = {"copilot": ".github/agents", "claude": ".claude/agents", "codex": ".codex/agents", "kiro": ".kiro/agents"}
REQUIRED = ["apm.yml", "DESCRIPTION.md", "README.md", "LICENSE", "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md",
            "docs", "compatibility", "examples", "templates", "hooks/README.md", "tests", "tooling",
            ".apm/agents", ".apm/skills", ".apm/instructions", ".apm/prompts"]
STALE = ["targets", "claude-code", "gemini-cli", "github-copilot", "openai-codex", "instructions", "prompts"]
SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, str]] = []  # kind, check, status, detail

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


def structural(rep: Report) -> dict[str, object]:
    for rel in REQUIRED:
        rep.add("structural", f"required artifact {rel}", (ROOT / rel).exists())
    for rel in STALE:
        rep.add("structural", f"no stale folder {rel}/", not (ROOT / rel).exists())
    cache = [p for p in list(ROOT.rglob("__pycache__")) + list(ROOT.rglob("*.pyc")) if p.parts[len(ROOT.parts)] not in ("tests", "tooling")]
    rep.add("structural", "no __pycache__ or .pyc outside tests/ and tooling/ (those are git-ignored dev residue)", not cache, ", ".join(str(p.relative_to(ROOT)) for p in cache[:3]))
    rep.add("structural", "no archives at pack root", not any(ROOT.glob("*.zip")))
    rep.add("structural", "no native hook JSON for APM to deploy",
            not any((ROOT / "hooks").glob("*.json")) and not (ROOT / ".apm" / "hooks").exists(),
            "native hooks would carry repository-relative commands; hooks ship as helper scripts and samples")

    manifest = simple_yaml(ROOT / "apm.yml")
    unknown = sorted(set(manifest) - APM_FIELDS)
    rep.add("structural", "apm.yml uses only APM-defined fields", not unknown, f"unknown: {unknown}" if unknown else "")
    rep.add("structural", "apm.yml has name and version", bool(manifest.get("name")) and bool(manifest.get("version")))
    rep.add("structural", "apm.yml version is semantic", bool(re.match(r"^\d+\.\d+\.\d+", str(manifest.get("version", "")))))
    targets = manifest.get("targets") or []
    bad = sorted(set(targets) - APM_TARGETS) if isinstance(targets, list) else ["not a list"]
    rep.add("structural", "apm.yml targets are valid APM targets", bool(targets) and not bad, f"targets: {targets}")

    agents = sorted((ROOT / ".apm" / "agents").glob("*.agent.md"))
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

    perm_path = ROOT / "compatibility" / "tool-permissions.yml"
    if perm_path.is_file():
        declared = set(re.findall(r"^  ([a-z0-9_-]+):\s*$", perm_path.read_text(encoding="utf-8"), re.M))
        rep.add("structural", "tool-permissions.yml covers every agent", declared == set(names), f"missing: {sorted(set(names) - declared)}")
    else:
        rep.add("structural", "tool-permissions.yml present", False)

    skills = sorted(p for p in (ROOT / ".apm" / "skills").iterdir() if p.is_dir())
    rep.add("structural", "at least one skill", bool(skills))
    for skill in skills:
        fm, _ = frontmatter(skill / "SKILL.md") if (skill / "SKILL.md").is_file() else ({}, "")
        rep.add("structural", f"skill {skill.name}: SKILL.md with name equal to folder", fm.get("name") == skill.name and bool(SLUG.match(skill.name)))
        rep.add("structural", f"skill {skill.name}: description within 1024 characters", 0 < len(fm.get("description", "")) <= 1024)
    instructions = sorted((ROOT / ".apm" / "instructions").glob("*.instructions.md"))
    for path in instructions:
        fm, _ = frontmatter(path)
        rep.add("structural", f"instruction {path.name}: description and applyTo", bool(fm.get("description")) and bool(fm.get("applyTo")))
    prompts = sorted((ROOT / ".apm" / "prompts").glob("*.prompt.md"))
    for path in prompts:
        fm, _ = frontmatter(path)
        rep.add("structural", f"prompt {path.name}: description", bool(fm.get("description")))
    prompt_text = (ROOT / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md").read_text(encoding="utf-8", errors="replace")
    rep.add("structural", "authoring prompt is version 2", "Prompt version 2" in prompt_text)
    return {"manifest": manifest, "agents": names, "skills": [s.name for s in skills],
            "prompts": len(prompts), "instructions": len(instructions)}


INSTALLED_FORBIDDEN = [
    (r"`shared/|\bshared/(hooks|tooling|examples|instructions|prompts|templates|docs)\b", "shared/ folder does not exist after install"),
    (r"installed repository root", "assumes a repository-root install"),
    (r"targets/", "hand-built targets are gone"),
    (r"\bCLAUDE\.md\b|\bAGENTS\.md\b|\bGEMINI\.md\b|copilot-instructions\.md", "repository context file is not installed by the pack"),
    (r"\.github/hooks", "repository hook path"),
    (r"\bINSTALL\.md\b", "removed file"),
    (r"\bdocs/[A-Za-z_]+\.md", "pack docs are not installed"),
    (r"\btests/[\w.-]+\.(yml|yaml|md|json)", "pack tests are not installed"),
    (r"\btemplates/[\w.-]+\.(md|py)", "pack templates are not installed"),
]
PACK_DOC_FORBIDDEN = [
    (r"targets/", "hand-built targets are gone"),
    (r"`shared/|\bshared/(hooks|tooling|examples|instructions|prompts|templates|docs)\b", "shared/ folder does not exist"),
    (r"four vendor|generated targets|28-section", "describes the old layout"),
    (r"\bINSTALL\.md\b", "removed file"),
    (r"(?<![.\w/`])(instructions|prompts)/(?=[\w.-]+\.(md|yml))", "instructions and prompts live under .apm/"),
]


def content_scan(rep: Report) -> None:
    """Installed content may reference only what is installed with it; pack docs may not describe the old layout."""
    for path in sorted((ROOT / ".apm").rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [f"{reason}: {m.group(0)}" for pattern, reason in INSTALLED_FORBIDDEN for m in [re.search(pattern, text)] if m]
        rep.add("structural", f"installed content {path.relative_to(ROOT).as_posix()}: references only installed things", not hits, "; ".join(hits))
    docs = [ROOT / "README.md", ROOT / "DESCRIPTION.md", ROOT / "hooks" / "README.md"]
    docs += sorted((ROOT / "docs").glob("*.md")) + sorted((ROOT / "compatibility").glob("*.yml"))
    for path in docs:
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.name == "DESIGN_DECISIONS.md":
            continue  # a decision log may describe the layouts it replaced
        hits = [f"{reason}: {m.group(0)}" for pattern, reason in PACK_DOC_FORBIDDEN for m in [re.search(pattern, text)] if m]
        rep.add("structural", f"pack doc {path.relative_to(ROOT).as_posix()}: describes the current layout", not hits, "; ".join(hits))


def consistency(rep: Report, info: dict[str, object]) -> None:
    """tests/*.yml and the contract instruction must agree with the real agents, skills and prompts."""
    import json
    skills = set(info["skills"])  # type: ignore[arg-type]
    agents = set(info["agents"])  # type: ignore[arg-type]
    prompts = {p.name for p in (ROOT / ".apm" / "prompts").glob("*.prompt.md")}

    def load(rel: str):
        path = ROOT / rel
        if not path.is_file():
            rep.add("structural", f"{rel} present", False)
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rep.add("structural", f"{rel} is valid JSON", False, str(exc))
            return None

    cov = load("tests/capability-coverage.yml")
    if cov:
        reqs = cov.get("requirements", [])
        rep.add("structural", "capability-coverage.yml names every skill exactly once",
                sorted(r.get("skill") for r in reqs) == sorted(skills), f"{len(reqs)} requirements for {len(skills)} skills")
        bad = sorted({r.get("prompt") for r in reqs if r.get("prompt")} - prompts)
        rep.add("structural", "capability-coverage.yml prompts exist", not bad, ", ".join(bad))
        bad = sorted({r.get("agent") for r in reqs if r.get("agent")} - agents)
        rep.add("structural", "capability-coverage.yml agents exist", not bad, ", ".join(bad))
    trig = load("tests/trigger-cases.yml")
    if trig:
        cases = trig.get("cases", [])
        covered = {s for c in cases for s in (c.get("skills") or [])}
        missing = sorted(skills - covered)
        rep.add("structural", "trigger-cases.yml covers every skill", not missing, ", ".join(missing))
        unknown = sorted(covered - skills)
        rep.add("structural", "trigger-cases.yml names only real skills", not unknown, ", ".join(unknown))
        bad = sorted({c.get("prompt") for c in cases if c.get("prompt")} - prompts)
        rep.add("structural", "trigger-cases.yml prompts exist", not bad, ", ".join(bad))
    rc = load("tests/report-contract.yml")
    contract = next(iter((ROOT / ".apm" / "instructions").glob("*contract*.instructions.md")), None)
    rep.add("structural", "an always-on contract instruction exists (.apm/instructions/*contract*.instructions.md)", contract is not None)
    if rc and contract:
        text = contract.read_text(encoding="utf-8").lower().replace("-", "").replace("_", "").replace(" ", "")
        missing = [f for f in rc.get("required_fields", []) + rc.get("statuses", []) + rc.get("severity", [])
                   if f.lower().replace("_", "").replace("-", "") not in text]
        rep.add("structural", "contract instruction states every report field, status and severity from report-contract.yml", not missing, ", ".join(missing))
        rep.add("structural", "contract instruction states the fallback sentence", rc.get("fallback", "") in contract.read_text(encoding="utf-8"))


def executable(rep: Report, info: dict[str, object], install_check: bool) -> None:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run([sys.executable, "-I", "-B", "-m", "unittest", "discover", "-s", "tests"],
                          cwd=ROOT, capture_output=True, text=True, env=env)
    tail = (proc.stderr or proc.stdout).strip().splitlines()[-1:] or [""]
    rep.add("executable", "pack unit tests (python -m unittest discover -s tests)", proc.returncode == 0, tail[0])

    apm = shutil.which("apm")
    if not apm:
        rep.add("executable", "apm compile --validate", None, "apm CLI not on PATH")
        rep.add("executable", "apm install into a scratch project", None, "apm CLI not on PATH")
        return
    proc = subprocess.run([apm, "compile", "--validate"], cwd=ROOT, capture_output=True, text=True)
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
        proc = subprocess.run([apm, "install", "--target", ",".join(targets), str(ROOT)], cwd=tmp, capture_output=True, text=True)
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


NOT_ESTABLISHED = [
    "Agents appear and run in the VS Code agent pane for Claude Code, Codex, and GitHub Copilot.",
    "A user-profile install (Code Workflow installer, or `apm install -g`) behaves identically on Windows and macOS.",
    "Kiro and Gemini CLI behaviour on a live install; neither client was available on the validating machine.",
    "Model behaviour of the five agents when actually invoked; tests cover helper code and contracts only.",
    "Hook behaviour: hooks ship as helper scripts and samples; no native hook was installed or exercised.",
]


def render(rep: Report, info: dict[str, object]) -> str:
    manifest = info["manifest"]
    assert isinstance(manifest, dict)
    fails = rep.failures()
    passed = sum(r[2] == "pass" for r in rep.rows)
    skipped = sum(r[2] == "skipped" for r in rep.rows)
    lines = ["# VALIDATION_REPORT", "",
             f"Pack: {manifest.get('name')} {manifest.get('version')}",
             "Standard: agent-pack-prompt v2",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--install-check", action="store_true", help="also run apm install into a scratch project")
    parser.add_argument("--no-report", action="store_true", help="do not write VALIDATION_REPORT.md")
    args = parser.parse_args()
    rep = Report()
    info = structural(rep)
    content_scan(rep)
    consistency(rep, info)
    executable(rep, info, args.install_check)
    if not args.no_report:
        (ROOT / "VALIDATION_REPORT.md").write_text(render(rep, info), encoding="utf-8")
    fails = rep.failures()
    skipped = sum(r[2] == "skipped" for r in rep.rows)
    print(f"{'PASS' if not fails else 'FAIL'}: {len(rep.rows)} checks, {len(fails)} failures, {skipped} skipped")
    for _, check, _, detail in fails:
        print(f"  FAIL {check}: {detail}")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
