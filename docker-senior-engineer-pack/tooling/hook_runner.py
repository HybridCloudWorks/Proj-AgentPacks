"""Hook events and manual helpers for the Docker Senior Engineer pack.

Reads files only. It never runs docker, builds, pulls or executes repository code, and it never puts
file contents into the context it returns: only counts, rule identifiers and severities.

Events read a JSON payload on stdin: sessionStart (inventory and static-check summary) and agentStop
(optional completion report check). Manual commands: preflight --root, completion --report, lint --root.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path

# Isolated interpreters (python -I) do not add the script's folder to sys.path; the helpers live beside this file.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from completion_contract import validate_completion  # noqa: E402
from container_lint import discover, lint_paths, summarize  # noqa: E402

MAX_BYTES = 262144
REPORT = Path(".docker-engineering") / "completion.json"
SESSION = re.compile(r"[A-Za-z0-9_.:-]{1,128}")


def preflight(root: Path) -> dict[str, object]:
    files = discover(root)
    findings = lint_paths(root, files)
    return {
        "dockerfiles": len(files["dockerfile"]),  # type: ignore[arg-type]
        "compose_files": len(files["compose"]),  # type: ignore[arg-type]
        "bake_files": len(files["bake"]),  # type: ignore[arg-type]
        "ignore_files": len(files["ignore"]),  # type: ignore[arg-type]
        "inventory_truncated": files["truncated"],
        "static_findings": summarize(findings),
    }


def _session(payload: dict[str, object]) -> str | None:
    value = payload.get("sessionId", payload.get("session_id"))
    return value if isinstance(value, str) and SESSION.fullmatch(value) else None


def handle(event: str, payload: object) -> dict[str, object]:
    if not isinstance(payload, dict) or not isinstance(payload.get("cwd"), str):
        raise ValueError("invalid hook payload")
    root = Path(payload["cwd"]).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("invalid workspace")
    session = _session(payload)
    if event == "sessionStart":
        info = preflight(root)
        return {"additionalContext": "Docker preflight (static, file inventory only): " + json.dumps(info)
                + ". Confirm the engine context before any Docker command. Optional completion JSON for this run uses session_id="
                + json.dumps(session) + "."}
    report = root / REPORT
    if not report.exists():
        return {}
    errors: list[str] = []
    try:
        if report.is_symlink() or not report.resolve().is_relative_to(root) or report.stat().st_size > MAX_BYTES:
            raise ValueError("invalid report boundary")
        value = json.loads(report.read_text(encoding="utf-8"))
        errors = validate_completion(value)
        if not isinstance(value, dict) or session is None or value.get("session_id") != session:
            errors.append("completion report belongs to another session")
    except (OSError, ValueError):
        errors = ["completion report unreadable or outside bounds"]
    retried = bool(payload.get("stop_hook_active", payload.get("stopHookActive", False)))
    if errors and not retried:
        return {"decision": "block", "reason": "Correct the completion evidence or report the work as unverified. Contract errors: " + "; ".join(errors)}
    if errors:
        return {"decision": "allow", "reason": "Completion remains unverified; correction is bounded to one retry."}
    return {"decision": "allow"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("event", choices=["sessionStart", "agentStop", "preflight", "completion", "lint"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        if args.event == "preflight":
            print(json.dumps(preflight(args.root.resolve())))
            return 0
        if args.event == "lint":
            root = args.root.resolve()
            findings = lint_paths(root, discover(root))
            print(json.dumps({"findings": [asdict(f) for f in findings], "summary": summarize(findings)}, indent=2))
            return int(any(f.severity in ("Blocker", "High") for f in findings))
        if args.event == "completion":
            if args.report is None or args.report.stat().st_size > MAX_BYTES:
                raise ValueError("invalid report")
            errors = validate_completion(json.loads(args.report.read_text(encoding="utf-8")))
            print(json.dumps({"valid": not errors, "errors": errors}))
            return int(bool(errors))
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("payload too large")
        print(json.dumps(handle(args.event, json.loads(raw))))
        return 0
    except (OSError, ValueError, TypeError):
        print(json.dumps({"error": "invalid hook input or unavailable local file"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
