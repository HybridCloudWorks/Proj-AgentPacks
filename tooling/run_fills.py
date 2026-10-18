#!/usr/bin/env python3
"""Run gap fills for several packs, a few at a time, and publish each one that passes as a pull request.

Each pack runs `generate_pack.py fill <pack>`; its output goes to staging/<name>-fill.log. A pack whose engine
checks pass is published with `generate_pack.py publish`, which opens a pull request on pack/<name>-fill.
A pack that fails is left in staging for review and is not published.

Usage: python tooling/run_fills.py [--parallel 4] [--no-publish] <pack> [<pack> ...]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ENGINE = REPO / "tooling" / "generate_pack.py"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("packs", nargs="+")
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--no-publish", action="store_true")
    args = parser.parse_args()
    (REPO / "staging").mkdir(exist_ok=True)
    queue = list(args.packs)
    running: dict[str, tuple[subprocess.Popen, object, float]] = {}
    results: dict[str, dict] = {}
    while queue or running:
        while queue and len(running) < args.parallel:
            pack = queue.pop(0)
            name = pack.removesuffix("/").removesuffix("-pack")
            log = open(REPO / "staging" / f"{name}-fill.log", "w", encoding="utf-8")
            proc = subprocess.Popen([sys.executable, str(ENGINE), "fill", pack], cwd=REPO, stdout=log, stderr=subprocess.STDOUT, text=True)
            running[pack] = (proc, log, time.time())
            print(f"{time.strftime('%H:%M:%S')} started {pack}", flush=True)
        for pack, (proc, log, started) in list(running.items()):
            if proc.poll() is None:
                continue
            log.close()
            del running[pack]
            name = pack.removesuffix("/").removesuffix("-pack")
            ws = REPO / "staging" / f"{name}-fill"
            check = json.loads((ws / "check.json").read_text(encoding="utf-8")) if (ws / "check.json").is_file() else {}
            gen = json.loads((ws / "generation-log.json").read_text(encoding="utf-8")) if (ws / "generation-log.json").is_file() else {}
            claude = gen.get("claude", {}) if isinstance(gen.get("claude"), dict) else {}
            result = {"status": check.get("status", "FAIL"), "minutes": round((time.time() - started) / 60, 1),
                      "turns": claude.get("num_turns"), "cost_usd": round(claude.get("total_cost_usd") or 0, 2),
                      "added": len(check.get("added_files", [])), "pr": ""}
            if result["status"] == "PASS" and not args.no_publish:
                pub = subprocess.run([sys.executable, str(ENGINE), "publish", str(ws)], cwd=REPO, capture_output=True, text=True)
                result["pr"] = (pub.stdout.strip().splitlines() or [pub.stderr.strip()])[-1]
            results[pack] = result
            print(f"{time.strftime('%H:%M:%S')} finished {pack}: {result}", flush=True)
        time.sleep(15)
    print("\nSUMMARY")
    for pack, r in results.items():
        print(f"{r['status']:5} {pack:42} {r['minutes']:>5} min  {r['turns']} turns  USD {r['cost_usd']}  +{r['added']} files  {r['pr']}")
    total = sum(r["cost_usd"] for r in results.values())
    print(f"total USD {round(total, 2)} across {len(results)} packs; {sum(r['status'] == 'PASS' for r in results.values())} passed")
    return 0 if all(r["status"] == "PASS" for r in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
