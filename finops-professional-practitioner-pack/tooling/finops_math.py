"""Deterministic FinOps arithmetic for the hook runner, examples and tests. Standard library only.

Usage: python tooling/finops_math.py per-day 2026-02=28000 2026-03=31000
       python tooling/finops_math.py savings --list 1.00 --contracted 0.95 --effective 0.70
"""
from __future__ import annotations

import argparse
import calendar
import csv
import json
import statistics
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, Mapping, Sequence

COST_COLUMNS = ("BilledCost", "EffectiveCost", "ListCost", "ContractedCost")
FOCUS_MARKERS = {"BilledCost", "EffectiveCost", "ListCost", "ContractedCost", "ChargeCategory", "ChargePeriodStart",
                 "BillingAccountId", "ServiceCategory"}
NATIVE_MARKERS = {
    "aws-cur": {"line_item_unblended_cost", "lineItem/UnblendedCost", "line_item_usage_account_id"},
    "azure-cost-details": {"costInBillingCurrency", "CostInBillingCurrency", "PreTaxCost", "billingAccountId"},
    "gcp-billing-export": {"cost_at_list", "billing_account_id", "usage_start_time"},
}
PLACEHOLDER_TAG_VALUES = {"", "unknown", "none", "n/a", "na", "tbd", "null", "unassigned"}


def days_in_month(month: str) -> int:
    year, number = (int(part) for part in month.split("-"))
    return calendar.monthrange(year, number)[1]


def cost_per_day(monthly_totals: Mapping[str, float]) -> dict[str, float]:
    """Monthly totals keyed YYYY-MM, divided by the days in each month."""
    return {month: total / days_in_month(month) for month, total in monthly_totals.items()}


def month_over_month(previous: tuple[str, float], current: tuple[str, float]) -> dict[str, float]:
    """Raw and day-normalized change between two months, as fractions."""
    (previous_month, previous_total), (current_month, current_total) = previous, current
    if previous_total <= 0:
        raise ValueError("previous total must be positive")
    raw = current_total / previous_total - 1
    normalized = (current_total / days_in_month(current_month)) / (previous_total / days_in_month(previous_month)) - 1
    return {"raw_change": raw, "normalized_change": normalized}


def savings_breakdown(list_cost, contracted_cost, effective_cost) -> dict:
    """Split rate savings into negotiated (List - Contracted) and commitment (Contracted - Effective) parts."""
    if min(list_cost, contracted_cost, effective_cost) < 0:
        raise ValueError("costs must be non-negative")
    return {"negotiated": list_cost - contracted_cost, "commitment": contracted_cost - effective_cost,
            "total": list_cost - effective_cost}


def effective_savings_rate(contracted_cost, effective_cost):
    if contracted_cost <= 0:
        raise ValueError("contracted cost must be positive")
    return (contracted_cost - effective_cost) / contracted_cost


def commitment_utilization(used_cost, unused_cost):
    total = used_cost + unused_cost
    if total <= 0:
        raise ValueError("no commitment cost in the window")
    return used_cost / total


def coverage(covered_cost, eligible_cost):
    if eligible_cost <= 0:
        raise ValueError("eligible cost must be positive")
    return covered_cost / eligible_cost


def detect_anomaly(series: Sequence[float], threshold: float = 3.5, season: int = 7, min_history: int = 28,
                   min_delta: float = 0.0) -> dict | None:
    """Score the last value against earlier values at the same seasonal position (same weekday for daily data).

    Median and median absolute deviation keep one earlier spike from widening the band. Returns None when there
    is too little history or the change is within the threshold or below min_delta.
    """
    values = [float(v) for v in series]
    if len(values) < min_history + 1:
        return None
    observed = values[-1]
    peers = values[-1 - season::-season]
    if len(peers) < 3:
        return None
    expected = statistics.median(peers)
    spread = 1.4826 * statistics.median(abs(p - expected) for p in peers)
    if spread == 0:
        spread = max(abs(expected) * 0.01, 1e-9)  # flat history: treat one percent of the level as one unit
    delta = observed - expected
    score = delta / spread
    if abs(score) < threshold or abs(delta) < min_delta:
        return None
    return {"observed": observed, "expected": expected, "delta": delta, "score": score,
            "direction": "spike" if delta > 0 else "drop"}


def segment_anomalies(segments: Mapping[str, Sequence[float]], **options) -> dict[str, dict]:
    """Run detect_anomaly per segment; a rise and a fall elsewhere can cancel out in the total."""
    results = {name: detect_anomaly(series, **options) for name, series in segments.items()}
    return {name: result for name, result in results.items() if result}


def classify_billing_header(headers: Iterable[str]) -> dict:
    """Identify an export schema from its column names. Only known column names are ever returned."""
    names = {h.strip().lstrip("\ufeff") for h in headers}
    focus_hits = names & FOCUS_MARKERS
    if len(focus_hits) >= 3:
        schema = "focus"
    else:
        schema = next((label for label, markers in NATIVE_MARKERS.items() if names & markers), "unknown")
    return {"schema": schema, "focus_cost_columns": [c for c in COST_COLUMNS if c in names]}


def _decimal(text: str | None) -> Decimal:
    if text is None or text.strip() == "":
        return Decimal(0)
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"not a number: {text[:20]!r}") from exc


def load_focus_csv(path: Path) -> list[dict]:
    """Read a FOCUS-shaped CSV; cost columns become Decimal so sums match invoices to the cent."""
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for column in COST_COLUMNS:
            if column in row:
                row[column] = _decimal(row[column])
    return rows


def regular(row: Mapping) -> bool:
    return not row.get("ChargeClass")


def total(rows: Iterable[Mapping], column: str, *, regular_only: bool = False,
          charge_categories: set[str] | None = None) -> Decimal:
    return sum((r[column] for r in rows
                if (not regular_only or regular(r))
                and (charge_categories is None or r.get("ChargeCategory") in charge_categories)), Decimal(0))


def invoice_totals(rows: Iterable[Mapping]) -> dict[str, Decimal]:
    """BilledCost per InvoiceId, the figure that must match the invoice document."""
    totals: dict[str, Decimal] = {}
    for row in rows:
        totals[row.get("InvoiceId") or ""] = totals.get(row.get("InvoiceId") or "", Decimal(0)) + row["BilledCost"]
    return totals


def untagged_share(rows: Iterable[Mapping], key: str, column: str = "EffectiveCost") -> Decimal:
    """Share of regular usage cost whose Tags lack a usable value for key. Placeholders count as untagged."""
    base = [r for r in rows if r.get("ChargeCategory") == "Usage" and regular(r)]
    overall = sum((r[column] for r in base), Decimal(0))
    if overall == 0:
        return Decimal(0)
    missing = Decimal(0)
    for row in base:
        try:
            tags = json.loads(row.get("Tags") or "{}")
        except json.JSONDecodeError:
            tags = {}
        value = tags.get(key) if isinstance(tags, dict) else None
        if not isinstance(value, str) or value.strip().lower() in PLACEHOLDER_TAG_VALUES:
            missing += row[column]
    return missing / overall


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    per_day = sub.add_parser("per-day", help="cost per day for YYYY-MM=total pairs")
    per_day.add_argument("pairs", nargs="+")
    savings = sub.add_parser("savings", help="split rate savings into negotiated and commitment parts")
    for name in ("list", "contracted", "effective"):
        savings.add_argument(f"--{name}", required=True)
    args = parser.parse_args()
    try:
        if args.command == "per-day":
            totals = {pair.split("=", 1)[0]: float(pair.split("=", 1)[1]) for pair in args.pairs}
            print(json.dumps(cost_per_day(totals)))
        else:
            parts = savings_breakdown(_decimal(args.list), _decimal(args.contracted), _decimal(args.effective))
            print(json.dumps({k: str(v) for k, v in parts.items()}))
        return 0
    except (ValueError, IndexError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
