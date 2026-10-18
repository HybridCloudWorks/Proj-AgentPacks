#!/usr/bin/env python3
"""Reliability arithmetic for architecture work: error budgets, composite availability and RTO/RPO fit.

Offline and deterministic; it never calls a cloud API. Percentages are given as 99.9, not 0.999.
  python availability.py budget --slo 99.9 --days 30
  python availability.py compose --serial 99.95 99.99 --parallel 99.5x2
  python availability.py dr-check --rpo-minutes 15 --rto-minutes 60 --backup-interval-minutes 5 --restore-minutes 40
Exit 0 on success (dr-check: objectives met), 1 when dr-check finds a gap, 2 on invalid input.
"""
from __future__ import annotations

import argparse
import json
import sys

MINUTES_PER_DAY = 24 * 60


def _fraction(percent: float) -> float:
    if not 0 < percent <= 100:
        raise ValueError(f"availability {percent} must be in (0, 100]")
    return percent / 100


def error_budget_minutes(slo_percent: float, days: float) -> float:
    if days <= 0:
        raise ValueError("window must be positive")
    return (1 - _fraction(slo_percent)) * days * MINUTES_PER_DAY


def parallel(percent: float, replicas: int) -> float:
    """Availability of independent redundant replicas where any one can serve."""
    if replicas < 1:
        raise ValueError("replicas must be at least 1")
    return (1 - (1 - _fraction(percent)) ** replicas) * 100


def serial(percents: list[float]) -> float:
    """Availability of components that must all be up."""
    result = 1.0
    for value in percents:
        result *= _fraction(value)
    return result * 100


def parse_parallel(spec: str) -> float:
    value, _, count = spec.lower().partition("x")
    if not count:
        raise ValueError(f"parallel spec {spec!r} must look like 99.5x2")
    return parallel(float(value), int(count))


def dr_check(rpo_minutes: float, rto_minutes: float, restore_minutes: float,
             backup_interval_minutes: float | None = None, replication_lag_minutes: float | None = None,
             detection_minutes: float = 0) -> dict[str, object]:
    if backup_interval_minutes is None and replication_lag_minutes is None:
        raise ValueError("give a backup interval or a replication lag")
    candidates = [v for v in (backup_interval_minutes, replication_lag_minutes) if v is not None]
    if any(v < 0 for v in candidates + [rpo_minutes, rto_minutes, restore_minutes, detection_minutes]):
        raise ValueError("durations cannot be negative")
    worst_data_loss = min(candidates)  # the better of the two protection mechanisms bounds data loss
    recovery_time = detection_minutes + restore_minutes
    return {
        "worst_case_data_loss_minutes": worst_data_loss,
        "recovery_time_minutes": recovery_time,
        "rpo_margin_minutes": rpo_minutes - worst_data_loss,
        "rto_margin_minutes": rto_minutes - recovery_time,
        "meets_rpo": worst_data_loss <= rpo_minutes,
        "meets_rto": recovery_time <= rto_minutes,
        "note": "Margins come from design inputs; only a measured restore test verifies them.",
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    budget = sub.add_parser("budget")
    budget.add_argument("--slo", type=float, required=True)
    budget.add_argument("--days", type=float, default=30)
    compose = sub.add_parser("compose")
    compose.add_argument("--serial", type=float, nargs="*", default=[])
    compose.add_argument("--parallel", nargs="*", default=[], help="replicated components as AVAILABILITYxCOUNT")
    dr = sub.add_parser("dr-check")
    dr.add_argument("--rpo-minutes", type=float, required=True)
    dr.add_argument("--rto-minutes", type=float, required=True)
    dr.add_argument("--restore-minutes", type=float, required=True)
    dr.add_argument("--backup-interval-minutes", type=float)
    dr.add_argument("--replication-lag-minutes", type=float)
    dr.add_argument("--detection-minutes", type=float, default=0)
    args = parser.parse_args(argv)
    try:
        if args.command == "budget":
            minutes = error_budget_minutes(args.slo, args.days)
            print(json.dumps({"slo_percent": args.slo, "window_days": args.days, "allowed_downtime_minutes": round(minutes, 3)}))
            return 0
        if args.command == "compose":
            parts = list(args.serial) + [parse_parallel(spec) for spec in args.parallel]
            if not parts:
                raise ValueError("give at least one --serial or --parallel component")
            print(json.dumps({"components_percent": [round(p, 6) for p in parts], "composite_percent": round(serial(parts), 6)}))
            return 0
        result = dr_check(args.rpo_minutes, args.rto_minutes, args.restore_minutes,
                          args.backup_interval_minutes, args.replication_lag_minutes, args.detection_minutes)
        print(json.dumps(result))
        return 0 if result["meets_rpo"] and result["meets_rto"] else 1
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
