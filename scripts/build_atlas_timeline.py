#!/usr/bin/env python3
"""Build deterministic atlas timeline artifact from knowledge graph + catalog."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Invalid ISO date: {value}") from exc


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def publication_dates_from_catalog(catalog: list[dict]) -> dict[str, dt.date]:
    result: dict[str, dt.date] = {}
    for item in catalog:
        doi = item.get("doi", "")
        if isinstance(doi, str) and "/" in doi and doi != "pending":
            suffix = doi.split("/", 1)[1]
        else:
            url = item.get("url", "")
            slug = url.rstrip("/").split("/")[-1] if isinstance(url, str) and url else ""
            kind = item.get("type", "paper")
            suffix = f"uvlm.{kind}.{slug}.v1" if slug else ""
        date_value = item.get("date")
        if not isinstance(date_value, str) or not date_value:
            raise ValueError(f"Missing date in catalog entry: {item}")
        if suffix:
            result[suffix] = parse_date(date_value)
    return result


def derive_node_dates(graph: dict, pub_dates: dict[str, dt.date]) -> dict[str, dt.date]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    node_map = {n["id"]: n for n in nodes}

    node_dates: dict[str, dt.date] = {}

    for node in nodes:
        node_id = node["id"]
        if node.get("class") == "publication":
            suffix = node.get("doi_suffix")
            if not isinstance(suffix, str) or suffix not in pub_dates:
                raise ValueError(f"Publication node cannot be matched to date: {node_id} ({suffix})")
            node_dates[node_id] = pub_dates[suffix]

    changed = True
    while changed:
        changed = False
        for node in nodes:
            node_id = node["id"]
            if node_id in node_dates:
                continue

            connected_dates: list[dt.date] = []
            for edge in edges:
                if edge.get("source") == node_id and edge.get("target") in node_dates:
                    connected_dates.append(node_dates[edge["target"]])
                elif edge.get("target") == node_id and edge.get("source") in node_dates:
                    connected_dates.append(node_dates[edge["source"]])

            if connected_dates:
                node_dates[node_id] = min(connected_dates)
                changed = True

    for node in nodes:
        if node["id"] not in node_dates:
            raise ValueError(f"Could not derive appearance date for node: {node['id']}")

    # Validate edge references
    for edge in edges:
        if edge.get("source") not in node_map or edge.get("target") not in node_map:
            raise ValueError(f"Malformed edge references non-existent node: {edge}")

    return node_dates


def edge_id(edge: dict) -> str:
    return f"{edge['source']}->{edge['target']}:{edge['type']}"


def build_timeline(graph: dict, node_dates: dict[str, dt.date]) -> dict:
    edges = graph.get("edges", [])

    edge_dates: dict[str, dt.date] = {}
    for edge in edges:
        source_date = node_dates[edge["source"]]
        target_date = node_dates[edge["target"]]
        edge_dates[edge_id(edge)] = max(source_date, target_date)

    events: list[dict] = []
    for node_id, date_value in node_dates.items():
        events.append({"date": date_value.isoformat(), "type": "node-appear", "id": node_id})
    for eid, date_value in edge_dates.items():
        events.append({"date": date_value.isoformat(), "type": "edge-appear", "id": eid})

    type_order = {"node-appear": 0, "edge-appear": 1}
    events.sort(key=lambda e: (e["date"], type_order.get(e["type"], 99), e["id"]))

    start = min(node_dates.values()).isoformat()
    end = max(node_dates.values()).isoformat()

    return {
        "timeRange": {"start": start, "end": end},
        "nodes": {k: {"appearanceDate": v.isoformat()} for k, v in sorted(node_dates.items())},
        "edges": {k: {"appearanceDate": v.isoformat()} for k, v in sorted(edge_dates.items())},
        "events": events,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=Path("registry/knowledge_graph.json"))
    parser.add_argument("--catalog", type=Path, default=Path("registry/catalog.json"))
    parser.add_argument("--output", type=Path, default=Path("registry/atlas_timeline.json"))
    args = parser.parse_args()

    if not args.graph.exists():
        raise SystemExit(f"Graph file missing: {args.graph}")
    if not args.catalog.exists():
        raise SystemExit(f"Catalog file missing: {args.catalog}")

    graph = load_json(args.graph)
    catalog = load_json(args.catalog)

    if not isinstance(catalog, list):
        raise SystemExit("Catalog must be a JSON array")

    pub_dates = publication_dates_from_catalog(catalog)
    node_dates = derive_node_dates(graph, pub_dates)
    timeline = build_timeline(graph, node_dates)

    args.output.write_text(json.dumps(timeline, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Wrote atlas timeline: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
