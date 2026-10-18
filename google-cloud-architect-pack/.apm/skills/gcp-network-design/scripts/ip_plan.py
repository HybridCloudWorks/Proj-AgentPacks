#!/usr/bin/env python3
"""Check a Google Cloud IP plan offline: overlaps, address classes, subnet headroom and GKE capacity.

Reads a JSON plan and never calls a cloud API. Usage: python ip_plan.py plan.json
Exit 0 when the plan has no errors, 1 when it has errors, 2 when the input cannot be read.

Plan shape:
  {"reserved": [{"name": "on-prem", "cidr": "10.0.0.0/12"}],
   "allow_overlap": [["dev-pods", "test-pods"]],
   "subnets": [{"name": "prod-usc1", "region": "us-central1", "cidr": "10.16.0.0/20",
                "expected_hosts": 200,
                "secondary": [{"name": "prod-pods", "cidr": "10.32.0.0/16"},
                              {"name": "prod-services", "cidr": "10.48.0.0/20"}],
                "gke": {"pods_range": "prod-pods", "services_range": "prod-services",
                        "max_pods_per_node": 48, "max_nodes": 300, "expected_services": 400},
                "serverless": {"max_instances": 100}}]}
"""
from __future__ import annotations

import ipaddress
import json
import sys
from pathlib import Path

RESERVED_PER_PRIMARY_RANGE = 4  # network, gateway, second-to-last and broadcast addresses
HEADROOM_WARNING = 0.8
PRIVATE_CLASSES = [
    (ipaddress.ip_network("10.0.0.0/8"), "RFC 1918"),
    (ipaddress.ip_network("172.16.0.0/12"), "RFC 1918"),
    (ipaddress.ip_network("192.168.0.0/16"), "RFC 1918"),
    (ipaddress.ip_network("100.64.0.0/10"), "RFC 6598"),
    (ipaddress.ip_network("240.0.0.0/4"), "Class E"),
]


def address_class(net: ipaddress.IPv4Network) -> str:
    for block, label in PRIVATE_CLASSES:
        if net.subnet_of(block):
            return label
    return "public"


def pod_block_size(max_pods_per_node: int) -> int:
    """GKE gives each node a Pod range of twice its maximum Pods, rounded up to a power of two."""
    size = 1
    while size < 2 * max_pods_per_node:
        size *= 2
    return size


def check_plan(plan: object) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []
    summary: list[dict[str, object]] = []
    if not isinstance(plan, dict) or not isinstance(plan.get("subnets"), list):
        return {"errors": ["plan must be an object with a subnets list"], "warnings": [], "notes": [], "subnets": []}

    ranges: list[tuple[str, ipaddress.IPv4Network]] = []

    def parse(name: str, cidr: object) -> ipaddress.IPv4Network | None:
        try:
            net = ipaddress.ip_network(str(cidr), strict=True)
        except ValueError as exc:
            errors.append(f"{name}: invalid CIDR {cidr!r} ({exc})")
            return None
        if not isinstance(net, ipaddress.IPv4Network):
            notes.append(f"{name}: IPv6 range not checked for capacity")
            return None
        if any(existing == name for existing, _ in ranges):
            errors.append(f"{name}: duplicate range name")
        ranges.append((name, net))
        label = address_class(net)
        if label == "public":
            warnings.append(f"{name}: {net} is publicly routable; confirm privately used public addressing is intended")
        elif label != "RFC 1918":
            notes.append(f"{name}: {net} is {label}; confirm every connected system and service supports it")
        return net

    for item in plan.get("reserved", []) or []:
        if isinstance(item, dict):
            parse(str(item.get("name", "reserved")), item.get("cidr"))

    for subnet in plan["subnets"]:
        if not isinstance(subnet, dict) or not subnet.get("name"):
            errors.append("every subnet needs a name")
            continue
        name = str(subnet["name"])
        primary = parse(name, subnet.get("cidr"))
        secondaries: dict[str, ipaddress.IPv4Network] = {}
        for sec in subnet.get("secondary", []) or []:
            if isinstance(sec, dict) and sec.get("name"):
                net = parse(str(sec["name"]), sec.get("cidr"))
                if net is not None:
                    secondaries[str(sec["name"])] = net
        row: dict[str, object] = {"name": name, "region": subnet.get("region")}
        demand = int(subnet.get("expected_hosts", 0) or 0)

        gke = subnet.get("gke")
        if isinstance(gke, dict):
            max_pods = int(gke.get("max_pods_per_node", 110))
            max_nodes = int(gke.get("max_nodes", 0))
            demand += max_nodes
            if not 8 <= max_pods <= 256:
                errors.append(f"{name}: max_pods_per_node {max_pods} is outside 8-256")
            pods = secondaries.get(str(gke.get("pods_range")))
            services = secondaries.get(str(gke.get("services_range")))
            if pods is None:
                errors.append(f"{name}: GKE pods_range {gke.get('pods_range')!r} is not a secondary range of this subnet")
            else:
                block = pod_block_size(max_pods)
                capacity = pods.num_addresses // block
                row.update(pod_block=f"/{32 - block.bit_length() + 1}", node_capacity_from_pod_range=capacity)
                if capacity < max_nodes:
                    errors.append(f"{name}: Pod range {pods} fits {capacity} nodes at {max_pods} Pods per node; plan needs {max_nodes}")
            if services is None:
                errors.append(f"{name}: GKE services_range {gke.get('services_range')!r} is not a secondary range of this subnet")
            elif int(gke.get("expected_services", 0)) > services.num_addresses:
                errors.append(f"{name}: Service range {services} holds {services.num_addresses} addresses; plan needs {gke.get('expected_services')}")

        serverless = subnet.get("serverless")
        if isinstance(serverless, dict):
            demand += 2 * int(serverless.get("max_instances", 0))  # Direct VPC egress uses about two addresses per instance

        if primary is not None:
            usable = primary.num_addresses - RESERVED_PER_PRIMARY_RANGE
            row.update(primary_usable=usable, primary_demand=demand)
            if demand > usable:
                errors.append(f"{name}: primary range {primary} has {usable} usable addresses; plan needs {demand}")
            elif demand > HEADROOM_WARNING * usable:
                warnings.append(f"{name}: primary range {primary} is over {int(HEADROOM_WARNING * 100)}% allocated ({demand}/{usable})")
        summary.append(row)

    allowed = {frozenset(map(str, pair)) for pair in plan.get("allow_overlap", []) or [] if isinstance(pair, list) and len(pair) == 2}
    for i, (name_a, net_a) in enumerate(ranges):
        for name_b, net_b in ranges[i + 1:]:
            if net_a.overlaps(net_b):
                message = f"overlap: {name_a} {net_a} and {name_b} {net_b}"
                if frozenset((name_a, name_b)) in allowed:
                    warnings.append(message + " (allowed by plan; the two must never be connected)")
                else:
                    errors.append(message)

    return {"errors": errors, "warnings": warnings, "notes": notes, "subnets": summary}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(json.dumps({"error": "usage: ip_plan.py plan.json"}))
        return 2
    try:
        plan = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": f"cannot read plan: {type(exc).__name__}"}))
        return 2
    result = check_plan(plan)
    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
