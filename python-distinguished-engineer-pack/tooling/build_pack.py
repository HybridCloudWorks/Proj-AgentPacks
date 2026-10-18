"""Rebuild only this pack's generated targets, catalog and deterministic archives."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "compatibility" / "capability-map.yml"
SKIP = {"__pycache__", ".pytest_cache", ".git", "dist"}
VENDORS = ("github-copilot", "claude-code", "openai-codex", "gemini-cli")


def read_manifest() -> dict:
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def copy(source: Path, target: Path) -> None:
    if not source.is_file() or source.is_symlink():
        raise ValueError("Source is missing or symbolic: " + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def files_under(path: Path) -> list[Path]:
    return sorted(p for p in path.rglob("*") if p.is_file() and not any(s in SKIP for s in p.relative_to(path).parts))


def clear_generated(name: str) -> Path:
    target = ROOT / name
    if name not in {"targets", "dist"} or target.is_symlink() or target.resolve().parent != ROOT.resolve():
        raise ValueError("Invalid generated-output boundary")
    if target.exists():
        if any(p.is_symlink() for p in target.rglob("*")):
            raise ValueError("Refusing generated output containing symlinks")
        shutil.rmtree(target)
    target.mkdir()
    return target


def frontmatter(path: Path) -> tuple[dict, str]:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError("Missing frontmatter: " + str(path))
    return yaml.safe_load(parts[1]), parts[2].strip()


def source_files(manifest: dict) -> list[Path]:
    result = [ROOT / name for name in manifest["root_files"] if (ROOT / name).is_file()]
    for directory in manifest["source_dirs"]:
        result.extend(files_under(ROOT / directory))
    return sorted(set(result))


def generate_targets(manifest: dict) -> None:
    targets = clear_generated("targets")
    for vendor in VENDORS:
        target = targets / vendor
        if vendor == "github-copilot":
            agent_dir, skill_dir, shared = ".github/agents", ".github/skills", target / ".github"
        elif vendor == "claude-code":
            agent_dir, skill_dir, shared = ".claude/agents", ".claude/skills", target / "shared"
        elif vendor == "openai-codex":
            agent_dir, skill_dir, shared = ".codex/agents", ".agents/skills", target / "shared"
        else:
            agent_dir, skill_dir, shared = ".gemini/agents", ".agents/skills", target / "shared"
        for agent in manifest["agents"]:
            name = agent["name"]
            canonical = ROOT / ".apm/agents" / (name + ".agent.md")
            header, body = frontmatter(canonical)
            if vendor == "github-copilot":
                copy(canonical, target / agent_dir / canonical.name)
            elif vendor == "openai-codex":
                # Current custom-agent files inherit parent permissions and MCP configuration.
                text = "name = " + json.dumps(name) + "\ndescription = " + json.dumps(agent["description"]) + "\ndeveloper_instructions = " + json.dumps(body) + "\n"
                write(target / agent_dir / (name + ".toml"), text)
            else:
                header = {"name": name, "description": agent["description"]}
                if vendor == "claude-code":
                    header["tools"] = agent["claude_tools"]
                else:
                    header["kind"] = "local"
                    header["tools"] = agent["gemini_tools"]
                    header["max_turns"] = 20
                write(target / agent_dir / (name + ".md"), "---\n" + yaml.safe_dump(header, sort_keys=False).strip() + "\n---\n\n" + body)
        for skill in manifest["skills"]:
            source = ROOT / ".apm/skills" / skill["name"]
            for file in files_under(source):
                copy(file, target / skill_dir / skill["name"] / file.relative_to(source))
        for group in ("instructions", "prompts", "examples"):
            for file in files_under(ROOT / group):
                copy(file, shared / group / file.relative_to(ROOT / group))
        # Preserve root-relative contracts referenced by primary and specialist instructions.
        for directory in ("docs", "templates", "tests"):
            for file in files_under(ROOT / directory):
                copy(file, target / directory / file.relative_to(ROOT / directory))
        copy(ROOT / "DESCRIPTION.md", target / "DESCRIPTION.md")
        copy(ROOT / "tests/report-contract.yml", target / "tests/report-contract.yml")
        copy(ROOT / "compatibility/compatibility-matrix.yml", target / "compatibility/compatibility-matrix.yml")
        if vendor == "github-copilot":
            copy(ROOT / "copilot-instructions.md", shared / "copilot-instructions.md")
            write(shared / "AGENT-PACK-README.md", "# Python Distinguished Engineer\n\nStart with python-distinguished-engineer; specialists are optional. See INSTALL.md, docs/AGENT_INVENTORY.md and root contracts. Native prompts/Skills/hooks depend on host surface support.")
            copy(ROOT / "hooks/python-engineering.json", shared / "hooks/python-engineering.json")
            for name in ("hook_runner.py", "completion_contract.py"):
                copy(ROOT / "tooling" / name, shared / "hooks/scripts" / name)
            install = "Copy the .github, docs, templates, tests and compatibility folders, merging with existing files after review. Do not overwrite existing repository instructions. Python 3.11+ is required for optional hooks; no dependency install is performed. Primary is user-invocable; four specialists have user-invocable false. Verify the client lists/discovers profiles and supports agent delegation. Prompt availability varies by surface. Hooks are local metadata/evidence checks, not authorization enforcement."
        else:
            context = {"claude-code": "CLAUDE.md", "openai-codex": "AGENTS.md", "gemini-cli": "GEMINI.md"}[vendor]
            copy(ROOT / "copilot-instructions.md", target / context)
            for file in files_under(ROOT / "hooks"):
                if file.suffix in {".ps1", ".sh"} or file.name == "README.md":
                    copy(file, shared / "hooks" / file.name)
            for name in ("hook_runner.py", "completion_contract.py"):
                copy(ROOT / "tooling" / name, shared / "tooling" / name)
            install = "Merge the vendor agent/Skill directories and shared, docs, templates, tests, compatibility and context files into an authorized project. Preserve existing context and policy. Use the primary role directly and specialists for bounded tasks; native visibility/delegation differs by client. Shared prompts are task recipes; hooks are manual helpers, not installed native hook configuration. Run python shared/tooling/hook_runner.py preflight --root . or completion --report PATH. Confirm installed tool names and agent discovery; no credentials/MCP/provider/model or live deployment is configured."
            if vendor == "openai-codex":
                install += " Agent TOML files inherit sandbox/approval/MCP from the parent session; enforce read-only execution with the parent host policy. This pack does not override that security configuration."
            if vendor == "gemini-cli":
                install += " Check /agents and the installed client's subagent support before enabling its relevant setting; do not replace existing settings."
        write(target / "INSTALL.md", "# Installation and use\n\n" + install)


def purpose(path: Path) -> str:
    name = path.as_posix()
    if "/skills/" in name:
        return "Operational Python capability and task-specific supporting material."
    if "/agents/" in name:
        return "Primary or optional specialist role with mapped host metadata."
    group = path.parts[0]
    return {"docs": "Design, authority, provenance, integration or maintenance contract.",
            "compatibility": "Explicit capability, source, host and portability metadata.",
            "tests": "Acceptance/trigger/report contracts, fixtures and executable regression evidence.",
            "tooling": "Reproducible build, validation or bounded local helper.",
            "hooks": "Lifecycle activation, deterministic checks and platform wrapper.",
            "instructions": "Shared scoped Python development rules.",
            "prompts": "Reusable task workflow with explicit expected output.",
            "examples": "Worked Python engineering scenario with evidence limits.",
            "templates": "Reusable implementation or handoff/report/tool contract."}.get(group, "Pack identity, installation, source metadata or authoring contract.")


def catalog(manifest: dict) -> None:
    sections = [
        "# Python Distinguished Engineer — complete artifact catalog",
        "## 1. Executive summary\n\nOne user-facing Python technology agent with four optional specialists, eighteen operational Skills and four vendor targets.",
        "## 2. Goals and non-goals\n\nDeliver maintainable enterprise Python and agent systems with explicit criteria and evidence. No universal framework choice, automatic deployment or implied production authorization.",
        "## 3. Assumptions\n\nPython identity comes from the current conversation. Target repository/runtime/SDK/tenant details are task-time inputs.",
        "## 4. Design principles\n\nRepository compatibility, focused implementation, runtime boundaries, bounded resources, useful delegation, evidence and reversible decisions.",
        "## 5. Major architecture decisions\n\nSee docs/DESIGN_DECISIONS.md below.",
        "## 6. Agent inventory\n\nSee docs/AGENT_INVENTORY.md.",
        "## 7. Skill inventory\n\nSee docs/SKILL_INVENTORY.md.",
        "## 8. Prompt inventory\n\nSee docs/PROMPT_INVENTORY.md.",
        "## 9. Shared instruction inventory\n\n" + ", ".join(manifest["instructions"]),
        "## 10. Tool and permission matrix\n\nSee docs/TOOL_PERMISSION_MATRIX.md.",
        "## 11. Approval matrix\n\nSee docs/APPROVAL_MATRIX.md.",
        "## 12. Directory tree\n\n```text\n" + "\n".join(p.relative_to(ROOT).as_posix() for p in source_files(manifest)) + "\n```",
        "## 13. Artifact contents\n\nArtifacts retain their source paths. Targets are generated from the same source and included later. This generated catalog indexes itself here; it is not recursively embedded.",
    ]
    ordered_roots = [ROOT / name for name in manifest["root_files"] if name != "AGENT-PACK-README.md"]
    ordered = [p for p in ordered_roots if p.is_file()]
    ordered += [p for p in source_files(manifest) if p not in ordered_roots and p.name != "AGENT-PACK-README.md"]
    ordered += files_under(ROOT / "targets")
    for file in ordered:
        rel = file.relative_to(ROOT)
        content = file.read_text(encoding="utf-8")
        fence = "`" * max(4, max((len(run) for run in __import__("re").findall(r"`+", content)), default=0) + 1)
        sections.append("### " + rel.as_posix() + "\n\nARTIFACT NAME: " + rel.as_posix() + "\n\nPURPOSE: " + purpose(rel) + "\n\nCONTENT:\n\n" + fence + "\n" + content.rstrip() + "\n" + fence)
    endings = [
        ("14. Example feature workflow", "examples/python-api-feature-workflow.md"),
        ("15. Example API workflow", "examples/python-api-feature-workflow.md"),
        ("16. Example MCP server workflow", "examples/mcp-server-workflow.md"),
        ("17. Example security-review workflow", "examples/security-review-workflow.md"),
        ("18. Example Playwright validation workflow", "examples/playwright-validation-workflow.md"),
        ("19. Example agent-evaluation workflow", "examples/agent-evaluation-workflow.md"),
        ("20. Example final completion report", "examples/final-completion-report.md"),
        ("21. Installation instructions", "README.md"),
        ("22. Usage instructions", "README.md"),
        ("23. Validation checklist", "VALIDATION_REPORT.md"),
        ("24. Governance guidance", "docs/MAINTENANCE.md"),
        ("25. Maintenance guidance", "docs/MAINTENANCE.md"),
        ("26. Versioning guidance", "docs/MAINTENANCE.md"),
        ("27. Known limitations", "docs/MAINTENANCE.md"),
        ("28. Unresolved assumptions", "docs/INTEGRATION_CONTRACT.md"),
    ]
    sections.extend("## " + title + "\n\n" + path + " is included in full in the artifact contents above." for title, path in endings)
    sections.append("## AGENT PACK VALIDATION SUMMARY\n\nAgent: Python Distinguished Engineer. Artifacts: canonical source, identity/authoring/report, docs/compatibility/tests/tooling, Skills/hooks/instructions/prompts/examples/templates, four vendor targets and archive families. Skills: 18. Profiles: 5. Hooks: metadata preflight and bounded completion evidence. Knowledge/integrations: official Python/PyPA/typing/test/OTel/MCP/Playwright/Azure/vendor documentation. Guardrails: scoped approval, version compatibility, authz/tenancy, injection/redaction, cancellation/budgets and honest evidence. Tests: local boundary behavior, hook protocol, reports, manifests, references and archive safety/parity. Genuine gaps: live host/provider/browser/cloud/MCP SDK verification and target organizational inputs; see VALIDATION_REPORT.md.")
    write(ROOT / "AGENT-PACK-README.md", "\n\n".join(sections))


def zip_files(output: Path, mapping: dict[str, Path]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, file in sorted(mapping.items()):
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError("Unsafe archive member")
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if file.suffix == ".sh" else 0o100644) << 16
            archive.writestr(info, file.read_bytes())


def archives(manifest: dict) -> None:
    dist = clear_generated("dist")
    name = manifest["name"]
    for vendor in VENDORS:
        source = ROOT / "targets" / vendor
        zip_files(dist / (vendor + "-" + name + ".zip"), {p.relative_to(source).as_posix(): p for p in files_under(source)})
    canonical = files_under(ROOT / ".apm")
    zip_files(dist / (name + "-canonical.zip"), {p.relative_to(ROOT).as_posix(): p for p in canonical})
    zip_files(dist / (name + "-prompt.zip"), {"PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md": ROOT / "PORTABLE_AGENT_SKILL_PACK_AUTHORING_PROMPT.md"})
    for skill in manifest["skills"]:
        source = ROOT / ".apm/skills" / skill["name"]
        zip_files(dist / "skills" / skill["name"] / "skill.zip", {p.relative_to(source).as_posix(): p for p in files_under(source)})
    skill_archives = {p.relative_to(dist / "skills").as_posix(): p for p in (dist / "skills").rglob("skill.zip")}
    zip_files(dist / (name + "-skills.zip"), skill_archives)
    validation = [ROOT / "VALIDATION_REPORT.md"] + files_under(ROOT / "tests") + files_under(ROOT / "tooling") + files_under(ROOT / "compatibility") + files_under(ROOT / "templates")
    zip_files(dist / (name + "-validation.zip"), {p.relative_to(ROOT).as_posix(): p for p in validation})
    full = source_files(manifest) + files_under(ROOT / "targets")
    zip_files(dist / (name + "-full-pack.zip"), {p.relative_to(ROOT).as_posix(): p for p in full})
    hashes = {p.relative_to(dist).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dist.rglob("*.zip"))}
    write(dist / "SHA256SUMS.txt", "\n".join(digest + "  " + name for name, digest in hashes.items()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archives-only", action="store_true", help="Repack current validated source/targets.")
    args = parser.parse_args()
    manifest = read_manifest()
    if args.archives_only:
        catalog(manifest)
        archives(manifest)
        return 0
    generate_targets(manifest)
    test = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_behavior.py", "-v"], cwd=ROOT, capture_output=True, text=True, timeout=60)
    print(test.stdout + test.stderr)
    if test.returncode:
        return test.returncode
    from validate_pack import BEHAVIOR_FILES, audit, digest, render
    import re
    match = re.search(r"Ran (\d+) tests?", test.stderr)
    behavior = {"command": "python -m unittest discover -s tests -p test_behavior.py -v",
                "exit_code": test.returncode, "test_count": int(match.group(1)) if match else 0,
                "python_version": sys.version.split()[0],
                "source_sha256": {name: digest(ROOT / name) for name in BEHAVIOR_FILES},
                "evidence": [line for line in test.stderr.splitlines() if line.endswith(" ... ok") or line == "OK"]}
    write(ROOT / "tests/behavior-results.json", json.dumps(behavior, indent=2))
    # Ensure installed test evidence is identical to the newly recorded source.
    for vendor in VENDORS:
        copy(ROOT / "tests/behavior-results.json", ROOT / "targets" / vendor / "tests/behavior-results.json")
    # Assemble report/catalog, then validate final archive state and embed that final report.
    write(ROOT / "VALIDATION_REPORT.md", render(audit(ROOT, archives=False)))
    catalog(manifest)
    archives(manifest)
    results = audit(ROOT, archives=True, check_report=False)
    write(ROOT / "VALIDATION_REPORT.md", render(results))
    catalog(manifest)
    archives(manifest)
    final = audit(ROOT, archives=True)
    print("PASS" if not final["failures"] else "FAIL", len(final["checks"]), "checks;", len(final["failures"]), "failures")
    for error in final["failures"]:
        print(error)
    return int(bool(final["failures"]))


if __name__ == "__main__":
    raise SystemExit(main())
