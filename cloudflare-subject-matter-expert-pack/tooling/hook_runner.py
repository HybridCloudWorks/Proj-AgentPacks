"""Hook and manual helper for the Cloudflare Subject Matter Expert pack.

Events
  sessionStart  read host JSON on stdin; return bounded additionalContext from a Cloudflare preflight
  agentStop     read host JSON on stdin; validate an optional completion report for this session
  preflight     manual: print the preflight for --root
  completion    manual: validate the report at --report

No repository code is executed and nothing is sent over the network. The preflight passes only fixed
finding codes and counts to the model, never names or values taken from repository files.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True  # never leave __pycache__ inside installed skill folders
sys.path[:0] =[str(Path(__file__).resolve().parent), str(PACK_ROOT / ".apm" / "skills" / "cloudflare-workers-development" / "scripts")]
from completion_contract import validate_completion  # noqa: E402
from wrangler_check import check_project  # noqa: E402

MAX_BYTES = 262144
MAX_TF_FILES = 200
MAX_TF_DEPTH = 4
SKIP_DIRS = {"node_modules", "vendor", "dist", "build"}
REPORT_PATH = Path(".cloudflare-sme") / "completion.json"
SESSION = re.compile(r"[A-Za-z0-9_.:-]{1,128}")
PROVIDER_LOCK = re.compile(r'provider\s+"registry\.terraform\.io/cloudflare/cloudflare"\s*\{\s*version\s*=\s*"(\d+\.\d+\.\d+)"')


def _tf_files(root: Path):
    """Yield .tf files at most MAX_TF_DEPTH folders deep, skipping dependency and VCS folders."""
    for folder, dirs, files in os.walk(root):
        depth = len(Path(folder).relative_to(root).parts)
        dirs[:] = [] if depth >= MAX_TF_DEPTH else [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            if name.endswith(".tf"):
                yield Path(folder) / name


def _terraform(root: Path) -> dict[str, object]:
    uses_provider = False
    for count, path in enumerate(_tf_files(root)):
        if count >= MAX_TF_FILES:
            break
        if path.is_symlink() or path.stat().st_size > MAX_BYTES:
            continue
        if "cloudflare/cloudflare" in path.read_text(encoding="utf-8", errors="replace"):
            uses_provider = True
            break
    version = None
    lock = root / ".terraform.lock.hcl"
    if lock.is_file() and not lock.is_symlink() and lock.stat().st_size <= MAX_BYTES:
        match = PROVIDER_LOCK.search(lock.read_text(encoding="utf-8", errors="replace"))
        version = match.group(1) if match else None
    return {"cloudflare_provider": uses_provider, "locked_provider_version": version}


def preflight(root: Path) -> dict[str, object]:
    root = root.resolve()
    wrangler = check_project(root)
    levels = Counter(f["level"] for f in wrangler["findings"])
    return {
        "wrangler_config": wrangler["config"],
        "compatibility_date": wrangler.get("compatibility_date"),
        "finding_counts": {level: levels.get(level, 0) for level in ("error", "warn", "info")},
        "finding_codes": sorted({f["code"] for f in wrangler["findings"]}),
        "binding_counts": {kind: len(names) for kind, names in wrangler["bindings"].items()},
        "environment_count": len(wrangler["environments"]),
        "terraform": _terraform(root),
    }


def handle(event: str, payload: object) -> dict[str, object]:
    if not isinstance(payload, dict) or not isinstance(payload.get("cwd"), str):
        raise ValueError("invalid hook payload")
    root = Path(payload["cwd"]).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("invalid workspace")
    session = payload.get("sessionId")
    session = session if isinstance(session, str) and SESSION.fullmatch(session) else None
    if event == "sessionStart":
        info = preflight(root)
        if not info["wrangler_config"] and not info["terraform"]["cloudflare_provider"]:
            return {}
        return {"additionalContext": "Cloudflare preflight: " + json.dumps(info, sort_keys=True)
                + ". Optional completion JSON for this run uses session_id=" + json.dumps(session)
                + ". Load the relevant Cloudflare skills; account writes need explicit Level 2 approval."}
    report = root / REPORT_PATH
    if not report.exists():
        return {}
    errors: list[str]
    try:
        if report.is_symlink() or not report.resolve().is_relative_to(root) or report.stat().st_size > MAX_BYTES:
            raise ValueError("invalid report boundary")
        value = json.loads(report.read_text(encoding="utf-8"))
        errors = validate_completion(value)
        if not isinstance(value, dict) or not session or value.get("session_id") != session:
            errors.append("completion report belongs to another session")
    except (OSError, ValueError):
        errors = ["completion report unreadable or outside bounds"]
    if errors and not payload.get("stop_hook_active", False):
        return {"decision": "block", "reason": "Correct the completion report or report the work as unverified. Contract errors: " + "; ".join(errors)}
    if errors:
        return {"decision": "allow", "reason": "Completion remains unverified; correction was limited to one retry."}
    return {"decision": "allow"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("event", choices=["sessionStart", "agentStop", "preflight", "completion"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        if args.event == "preflight":
            print(json.dumps(preflight(args.root), indent=2))
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
