#!/usr/bin/env python3
"""Validate atlas timeline structure and consistency."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))

    for key in ("timeRange", "nodes", "edges", "events"):
        if key not in data:
            errors.append(f"Missing top-level key: {key}")

    if errors:
        return errors

    start = parse_date(data["timeRange"]["start"])
    end = parse_date(data["timeRange"]["end"])
    if start > end:
        errors.append("timeRange.start must be <= timeRange.end")

    nodes = data["nodes"]
    edges = data["edges"]
    events = data["events"]

    for node_id, node_meta in nodes.items():
        try:
            parse_date(node_meta["appearanceDate"])
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Invalid node appearanceDate for {node_id}: {exc}")

    for edge_id, edge_meta in edges.items():
        try:
            parse_date(edge_meta["appearanceDate"])
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Invalid edge appearanceDate for {edge_id}: {exc}")

    last_key = None
    for i, ev in enumerate(events):
        key = (ev.get("date"), ev.get("type"), ev.get("id"))
        if last_key and key < last_key:
            errors.append("Events must be sorted by (date, type, id)")
            break
        last_key = key

        try:
            parse_date(ev["date"])
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Invalid event date at index {i}: {exc}")

        ev_type = ev.get("type")
        ev_id = ev.get("id")
        if ev_type == "node-appear" and ev_id not in nodes:
            errors.append(f"Event references unknown node id: {ev_id}")
        if ev_type == "edge-appear" and ev_id not in edges:
            errors.append(f"Event references unknown edge id: {ev_id}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timeline", type=Path)
    args = parser.parse_args()

    errs = validate(args.timeline)
    if errs:
        print("[ERROR] Timeline validation failed:")
        for e in errs:
            print(f"  - {e}")
        return 1
    print(f"[OK] Timeline validated: {args.timeline}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
