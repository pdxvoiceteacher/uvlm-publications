#!/usr/bin/env python3
"""Validate registry/constellations.json against knowledge graph references."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def parse_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        dt.date.fromisoformat(value)
        return True
    except Exception:  # noqa: BLE001
        return False


def validate(const_path: Path, graph_path: Path) -> list[str]:
    errors: list[str] = []
    const = json.loads(const_path.read_text(encoding="utf-8"))
    graph = json.loads(graph_path.read_text(encoding="utf-8"))

    node_ids = {n.get("id") for n in graph.get("nodes", []) if isinstance(n, dict) and isinstance(n.get("id"), str)}
    edge_ids = {
        f"{e.get('source')}->{e.get('target')}:{e.get('type')}"
        for e in graph.get("edges", [])
        if isinstance(e, dict)
    }

    if not isinstance(const, dict):
        return ["Constellations root must be object"]

    if not parse_date(const.get("generatedAt")):
        errors.append("generatedAt must be ISO date string")

    method = const.get("method")
    if not isinstance(method, dict):
        errors.append("method must be an object")
    else:
        if not isinstance(method.get("name"), str) or not method.get("name"):
            errors.append("method.name must be non-empty string")
        if not isinstance(method.get("version"), str) or not method.get("version"):
            errors.append("method.version must be non-empty string")

    constellations = const.get("constellations")
    if not isinstance(constellations, list):
        errors.append("constellations must be an array")
        return errors

    seen_ids: set[str] = set()
    last_id = None
    for i, item in enumerate(constellations):
        if not isinstance(item, dict):
            errors.append(f"constellations[{i}] must be object")
            continue
        cid = item.get("id")
        if not isinstance(cid, str) or not cid:
            errors.append(f"constellations[{i}].id must be non-empty string")
            continue
        if cid in seen_ids:
            errors.append(f"duplicate constellation id: {cid}")
        seen_ids.add(cid)
        if last_id and cid < last_id:
            errors.append("constellations must be sorted by id")
        last_id = cid

        if not isinstance(item.get("title"), str) or not item.get("title"):
            errors.append(f"{cid} title must be non-empty string")

        members = item.get("memberNodeIds")
        if not isinstance(members, list) or not members:
            errors.append(f"{cid} memberNodeIds must be non-empty list")
            members = []
        if len(set(members)) != len(members):
            errors.append(f"{cid} memberNodeIds has duplicates")
        if members != sorted(members):
            errors.append(f"{cid} memberNodeIds must be sorted")

        for nid in members:
            if nid not in node_ids:
                errors.append(f"{cid} references unknown node id: {nid}")

        medges = item.get("memberEdgeIds")
        if not isinstance(medges, list):
            errors.append(f"{cid} memberEdgeIds must be list")
            medges = []
        if len(set(medges)) != len(medges):
            errors.append(f"{cid} memberEdgeIds has duplicates")
        if medges != sorted(medges):
            errors.append(f"{cid} memberEdgeIds must be sorted")
        for eid in medges:
            if eid not in edge_ids:
                errors.append(f"{cid} references unknown edge id: {eid}")

        stats = item.get("stats")
        if not isinstance(stats, dict):
            errors.append(f"{cid} stats must be object")
        else:
            for key in ("publicationCount", "conceptCount", "authorCount", "seriesCount"):
                if not isinstance(stats.get(key), int) or stats.get(key) < 0:
                    errors.append(f"{cid} stats.{key} must be non-negative integer")

        if isinstance(stats, dict):
            # practical consistency check
            class_counts = {"publication": 0, "concept": 0, "author": 0, "series": 0}
            for nid in members:
                if nid.startswith("publication:"):
                    class_counts["publication"] += 1
                if nid.startswith("concept:"):
                    class_counts["concept"] += 1
                if nid.startswith("author:"):
                    class_counts["author"] += 1
                if nid.startswith("series:"):
                    class_counts["series"] += 1
            if stats.get("publicationCount") != class_counts["publication"]:
                errors.append(f"{cid} publicationCount does not match members")
            if stats.get("conceptCount") != class_counts["concept"]:
                errors.append(f"{cid} conceptCount does not match members")

        explanation = item.get("explanation")
        if not isinstance(explanation, dict):
            errors.append(f"{cid} explanation must be object")
        else:
            ps = explanation.get("primarySignals")
            if not isinstance(ps, list) or not all(isinstance(x, str) and x for x in ps):
                errors.append(f"{cid} explanation.primarySignals must be list[str]")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("constellations", type=Path)
    parser.add_argument("--graph", type=Path, default=Path("registry/knowledge_graph.json"))
    args = parser.parse_args()

    errs = validate(args.constellations, args.graph)
    if errs:
        print("[ERROR] Constellations validation failed:")
        for err in errs:
            print(f"  - {err}")
        return 1

    print(f"[OK] Constellations validated: {args.constellations}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
