#!/usr/bin/env python3
"""Safe local Codex lifecycle hook for orchestration audit and completion guards."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True)
    args = parser.parse_args()
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        event = {"raw_input_invalid": True, "raw_input": raw[:1000]}
    root = Path(event.get("cwd") or Path.cwd()).resolve()
    audit = root / ".agentic" / "audit"
    audit.mkdir(parents=True, exist_ok=True)
    record = {"recorded_at": datetime.now(timezone.utc).isoformat(), "event_argument": args.event, "event": event}
    with (audit / "codex-events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    if args.event == "Stop":
        if event.get("stop_hook_active"):
            print("{}")
            return 0
        active = root / ".agentic" / "active-workflow.json"
        if active.is_file():
            try:
                active_data = json.loads(active.read_text(encoding="utf-8"))
                workflow_id = active_data["workflow_id"]
                state_path = root / ".agentic" / "workflows" / workflow_id / "WORKFLOW.json"
                state = json.loads(state_path.read_text(encoding="utf-8"))
                validator = root / "tooling" / "workflow.py"
                if state.get("enforce_stop", False) and state.get("status") != "completed" and validator.is_file():
                    result = subprocess.run([sys.executable, str(validator), "validate", "--root", str(root), "--workflow", workflow_id], capture_output=True, text=True)
                    if result.returncode != 0:
                        print(json.dumps({"decision": "block", "reason": f"Workflow {workflow_id} is not complete. Continue until required Codex subagent handoffs are validated."}))
                        return 0
            except (OSError, KeyError, json.JSONDecodeError):
                pass
    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
