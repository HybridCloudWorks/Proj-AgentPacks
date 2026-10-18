#!/usr/bin/env python3
"""Create, discover, and validate Codex agentic workflow state locally."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "compatibility" / "agent-registry.yml"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_registry(path: Path = REGISTRY) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- id:"):
            if current:
                items.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif current and ":" in line and not line.startswith("#"):
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip().strip('"\'')
    if current:
        items.append(current)
    return items


def toml_agent_name(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    match = re.search(r"^name\s*=\s*[\"']([^\"']+)[\"']", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def discover(root: Path, include_user: bool) -> dict:
    locations = [root / ".codex" / "agents"]
    if include_user:
        locations.append(Path(os.environ.get("USERPROFILE", "")) / ".codex" / "agents")
    found: dict[str, list[str]] = {}
    for location in locations:
        if not location.is_dir():
            continue
        for path in sorted(location.glob("*.toml")):
            name = toml_agent_name(path)
            if name:
                found.setdefault(name, []).append(str(path))
    registry = {item["id"]: item for item in parse_registry()}
    records = []
    for item in parse_registry():
        paths = found.get(item["agent_name"], [])
        records.append({
            "id": item["id"],
            "agent_name": item["agent_name"],
            "capability": item.get("capability", ""),
            "available": bool(paths),
            "paths": paths,
            "enabled_by_default": item.get("enabled_by_default", "false").lower() == "true",
        })
    unknown = sorted(name for name in found if name not in registry and name != "codex-agentic-orchestrator")
    return {"generated_at": now(), "root": str(root), "agents": records, "unknown_agents": unknown}


def load_discovery(root: Path) -> dict:
    path = root / ".agentic" / "discovery.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    result = discover(root, include_user=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def selected_nodes(root: Path, mode: str, names: list[str]) -> list[dict]:
    discovery = load_discovery(root)
    available = {item["id"]: item for item in discovery["agents"]}
    if mode == "all":
        requested = [item["id"] for item in discovery["agents"] if item["enabled_by_default"]]
    elif mode == "one":
        requested = names or [item["id"] for item in discovery["agents"] if item["available"]][:1]
    else:
        requested = names
    if not requested:
        raise SystemExit("no agent is available for the requested workflow mode")
    nodes = []
    for name in requested:
        if name not in available:
            nodes.append({"id": name, "agent_name": name, "required": True, "available": False, "status": "blocked"})
        else:
            item = available[name]
            nodes.append({"id": name, "agent_name": item["agent_name"], "required": True, "available": item["available"], "status": "queued" if item["available"] else "blocked"})
    return nodes


def init_workflow(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    workflow_id = args.workflow_id or "wf-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    directory = root / ".agentic" / "workflows" / workflow_id
    if directory.exists():
        raise SystemExit(f"workflow already exists: {workflow_id}")
    nodes = selected_nodes(root, args.mode, [x for x in args.agents.split(",") if x])
    optional = {x for x in args.optional_agents.split(",") if x}
    for node in nodes:
        if args.mode == "all" and not args.require_all:
            node["required"] = bool(node["available"])
            if not node["available"]:
                node["status"] = "skipped_optional"
        if node["id"] in optional:
            node["required"] = False
            if not node["available"]:
                node["status"] = "skipped_optional"
    state = {
        "workflow_id": workflow_id,
        "created_at": now(),
        "updated_at": now(),
        "mode": args.mode,
        "objective": args.objective,
        "enforce_stop": not args.no_enforce_stop,
        "max_parallel": args.max_parallel,
        "nodes": nodes,
        "status": "blocked" if any(n["required"] and not n["available"] for n in nodes) else "queued",
    }
    (directory / "handoffs").mkdir(parents=True)
    (directory / "artifacts").mkdir()
    (directory / "evidence").mkdir()
    (directory / "audit").mkdir()
    (directory / "WORKFLOW.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (directory / "STATUS.md").write_text(f"# {workflow_id}\n\nStatus: **{state['status']}**\n\nObjective: {args.objective}\n\nCreated: {state['created_at']}\n", encoding="utf-8")
    (root / ".agentic" / "active-workflow.json").write_text(json.dumps({"workflow_id": workflow_id, "path": str(directory)}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(state, indent=2))
    return 0


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith("#"):
        return None
    return value.split(" #", 1)[0].strip().strip('"\'')


def handoff_valid(path: Path, node_id: str, workflow_id: str) -> tuple[bool, list[str]]:
    if not path.is_file():
        return False, ["handoff file is missing"]
    text = path.read_text(encoding="utf-8", errors="replace")
    errors = []
    for key in ["workflow_id", "agent_id", "status", "summary", "next_action", "authorization_used"]:
        if not scalar(text, key):
            errors.append(f"missing {key}")
    if scalar(text, "workflow_id") != workflow_id:
        errors.append("workflow_id does not match")
    if scalar(text, "agent_id") != node_id:
        errors.append("agent_id does not match registered node")
    if not re.search(r"^evidence:\s*$", text, re.MULTILINE):
        errors.append("evidence section is missing")
    if scalar(text, "status") == "completed" and not re.search(r"^\s*-\s+path:", text, re.MULTILINE):
        errors.append("completed handoff has no evidence or artifact path")
    return not errors, errors


def validate_workflow(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    directory = root / ".agentic" / "workflows" / args.workflow
    state_path = directory / "WORKFLOW.json"
    if not state_path.is_file():
        print(f"workflow not found: {args.workflow}", file=sys.stderr)
        return 2
    state = json.loads(state_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    results = []
    for node in state.get("nodes", []):
        handoff = directory / "handoffs" / f"{node['id']}.yml"
        if not node.get("available"):
            if node.get("required"):
                errors.append(f"required agent unavailable: {node['id']}")
                node["status"] = "blocked"
            else:
                node["status"] = "skipped_optional"
            results.append({"agent_id": node["id"], "valid": False, "reason": node["status"]})
            continue
        valid, reasons = handoff_valid(handoff, node["id"], state["workflow_id"])
        if valid:
            node["status"] = "completed"
        else:
            node["status"] = "blocked" if node.get("required") else "partial"
            if node.get("required"):
                errors.extend(f"{node['id']}: {reason}" for reason in reasons)
        results.append({"agent_id": node["id"], "valid": valid, "reasons": reasons})
    required = [node for node in state.get("nodes", []) if node.get("required")]
    if errors:
        state["status"] = "blocked"
    elif all(node.get("status") == "completed" for node in required):
        state["status"] = "completed"
    else:
        state["status"] = "partial"
    state["updated_at"] = now()
    state["validation"] = {"validated_at": now(), "errors": errors, "results": results}
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    (directory / "STATUS.md").write_text("# " + state["workflow_id"] + "\n\nStatus: **" + state["status"] + "**\n\n" + "\n".join(f"- {r['agent_id']}: {'valid' if r['valid'] else ', '.join(r.get('reasons', [r.get('reason', 'invalid')]))}" for r in results) + "\n", encoding="utf-8")
    print(json.dumps(state["validation"] | {"workflow_status": state["status"]}, indent=2))
    return 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    discover_parser = sub.add_parser("discover")
    discover_parser.add_argument("--out", default=".agentic/discovery.json")
    discover_parser.add_argument("--no-user", action="store_true")
    init_parser = sub.add_parser("init")
    init_parser.add_argument("--mode", choices=["one", "selected", "all"], required=True)
    init_parser.add_argument("--agents", default="")
    init_parser.add_argument("--optional-agents", default="")
    init_parser.add_argument("--workflow-id")
    init_parser.add_argument("--objective", required=True)
    init_parser.add_argument("--max-parallel", type=int, default=3)
    init_parser.add_argument("--require-all", action="store_true", help="in all mode, block when any registry agent is unavailable")
    init_parser.add_argument("--no-enforce-stop", action="store_true")
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--workflow", required=True)
    status_parser = sub.add_parser("status")
    status_parser.add_argument("--workflow", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.command == "discover":
        output = root / args.out
        result = discover(root, include_user=not args.no_user)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "init":
        return init_workflow(args)
    if args.command == "validate":
        return validate_workflow(args)
    state_path = root / ".agentic" / "workflows" / args.workflow / "WORKFLOW.json"
    if not state_path.is_file():
        print(f"workflow not found: {args.workflow}", file=sys.stderr)
        return 2
    print(state_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
