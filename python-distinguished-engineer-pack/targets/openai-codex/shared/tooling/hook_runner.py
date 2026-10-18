"""Copilot JSON hooks and manual preflight; no repository code is executed."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import sys
import tomllib
from completion_contract import validate_completion

MAX_BYTES = 262144


def preflight(root: Path) -> dict[str, object]:
    path = root / "pyproject.toml"
    names = [name for name in ("pyproject.toml", "uv.lock", "poetry.lock", "Pipfile.lock", "requirements.txt") if (root / name).is_file()]
    result: dict[str, object] = {"metadata": names, "requires_python": None}
    if path.is_file():
        if path.is_symlink() or path.resolve().parent != root.resolve() or path.stat().st_size > MAX_BYTES:
            result["error"] = "metadata file outside allowed scope or size"
        else:
            try:
                parsed = tomllib.loads(path.read_text(encoding="utf-8"))
                requirement = parsed.get("project", {}).get("requires-python")
                result["requires_python"] = requirement if isinstance(requirement, str) and len(requirement) <= 100 and re.fullmatch(r"[0-9<>=!~.,* ]+", requirement) else None
            except (OSError, ValueError, AttributeError):
                result["error"] = "metadata could not be parsed"
    return result


def handle(event: str, payload: object) -> dict[str, object]:
    if not isinstance(payload, dict) or not isinstance(payload.get("cwd"), str):
        raise ValueError("invalid hook payload")
    root = Path(payload["cwd"]).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("invalid workspace")
    if event == "sessionStart":
        info = preflight(root)
        # Only fixed metadata names and a bounded version expression; never prompts or contents.
        session = payload.get("sessionId")
        session = session if isinstance(session, str) and re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", session) else None
        return {"additionalContext": "Python preflight: " + json.dumps(info) + ". Optional completion JSON for this run uses session_id=" + json.dumps(session) + ". Inspect repository instructions and use relevant Python Skills."}
    report = root / ".github" / "python-engineering" / "completion.json"
    if not report.exists():
        return {}
    errors: list[str] = []
    try:
        if not report.resolve().is_relative_to(root) or report.stat().st_size > MAX_BYTES:
            raise ValueError("invalid report boundary")
        value = json.loads(report.read_text(encoding="utf-8"))
        errors = validate_completion(value)
        if not isinstance(value, dict) or not payload.get("sessionId") or value.get("session_id") != payload["sessionId"]:
            errors.append("completion report belongs to another session")
    except (OSError, ValueError):
        errors = ["completion report unreadable or outside bounds"]
    if errors and not payload.get("stop_hook_active", False):
        return {"decision": "block", "reason": "Correct the local completion evidence or report unverified completion. Contract errors: " + "; ".join(errors)}
    if errors:
        return {"decision": "allow", "reason": "Completion remains unverified; correction bounded to one retry."}
    return {"decision": "allow"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("event", choices=["sessionStart", "agentStop", "preflight", "completion"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        if args.event == "preflight":
            print(json.dumps(preflight(args.root.resolve())))
            return 0
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
