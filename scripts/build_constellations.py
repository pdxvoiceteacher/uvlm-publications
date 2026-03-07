#!/usr/bin/env python3
"""Build deterministic research constellations from the knowledge graph."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import defaultdict, deque
from pathlib import Path

CONCEPT_REL_TYPES = {"contains", "dependsOn", "refines", "extends", "contrastsWith"}
PUB_REL_TYPES = {"cites", "isReferencedBy", "isPartOf", "isVersionOf"}
STRONG = {"mentionsConcept", *CONCEPT_REL_TYPES}
MEDIUM = set(PUB_REL_TYPES)
WEAK = {"publishedIn", "authoredBy"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def edge_id(edge: dict) -> str:
    return f"{edge['source']}->{edge['target']}:{edge['type']}"


def slugify(value: str) -> str:
    return value.strip().lower().replace(" ", "-")


def projection_components(nodes: dict[str, dict], edges: list[dict]) -> list[set[str]]:
    projection_ids = {nid for nid, node in nodes.items() if node.get("class") in {"concept", "publication"}}
    adjacency: dict[str, set[str]] = {nid: set() for nid in projection_ids}

    for edge in edges:
        t = edge.get("type")
        s = edge.get("source")
        d = edge.get("target")
        if s in projection_ids and d in projection_ids and t in (STRONG | MEDIUM):
            adjacency[s].add(d)
            adjacency[d].add(s)

    seen: set[str] = set()
    components: list[set[str]] = []
    for start in sorted(adjacency):
        if start in seen:
            continue
        q = deque([start])
        seen.add(start)
        comp = {start}
        while q:
            cur = q.popleft()
            for nxt in sorted(adjacency[cur]):
                if nxt in seen:
                    continue
                seen.add(nxt)
                comp.add(nxt)
                q.append(nxt)
        components.append(comp)

    return components


def choose_seed_concept(component: set[str], nodes: dict[str, dict], edges: list[dict]) -> str | None:
    concepts = sorted([nid for nid in component if nodes.get(nid, {}).get("class") == "concept"])
    if not concepts:
        return None

    degree = {c: 0 for c in concepts}
    for edge in edges:
        if edge.get("source") in degree and edge.get("target") in component:
            degree[edge["source"]] += 1
        if edge.get("target") in degree and edge.get("source") in component:
            degree[edge["target"]] += 1

    return sorted(concepts, key=lambda cid: (-degree[cid], cid))[0]


def constellation_title(seed_concept_id: str | None, component: set[str], nodes: dict[str, dict]) -> tuple[str, str]:
    if seed_concept_id:
        value = nodes.get(seed_concept_id, {}).get("value", seed_concept_id.split(":", 1)[1])
        base = f"{value} Core"
        return f"constellation:{slugify(value)}-core", base

    pubs = sorted([nid for nid in component if nodes.get(nid, {}).get("class") == "publication"])
    if pubs:
        suffix = pubs[0].split("publication:", 1)[1]
        return f"constellation:{slugify(suffix)}-cluster", f"{suffix} Cluster"

    first = sorted(component)[0]
    return f"constellation:{slugify(first)}-cluster", "Research Cluster"


def primary_signals(component_edges: list[dict]) -> list[str]:
    types = {e.get("type") for e in component_edges}
    signals: list[str] = []
    if "mentionsConcept" in types:
        signals.append("shared concept mentions")
    if CONCEPT_REL_TYPES & types:
        signals.append("concept relation topology")
    if PUB_REL_TYPES & types:
        signals.append("publication reference linkage")
    if "publishedIn" in types:
        signals.append("shared series context")
    if "authoredBy" in types:
        signals.append("shared authorship")
    return signals or ["topological connectivity"]


def build_constellations(graph: dict) -> dict:
    nodes = {node["id"]: node for node in graph.get("nodes", [])}
    edges = graph.get("edges", [])

    components = [c for c in projection_components(nodes, edges) if len(c) > 1]
    constellations: list[dict] = []

    for component in sorted(components, key=lambda c: sorted(c)[0]):
        member_nodes = set(component)
        # pull weak context nodes (authors/series) connected to component nodes
        for edge in edges:
            s, t = edge.get("source"), edge.get("target")
            et = edge.get("type")
            if et not in WEAK:
                continue
            if s in component and t in nodes:
                member_nodes.add(t)
            if t in component and s in nodes:
                member_nodes.add(s)

        member_edges = []
        for edge in edges:
            if edge.get("source") in member_nodes and edge.get("target") in member_nodes:
                member_edges.append(edge)

        seed = choose_seed_concept(component, nodes, edges)
        cid, title = constellation_title(seed, component, nodes)

        counts = defaultdict(int)
        for node_id in member_nodes:
            cls = nodes.get(node_id, {}).get("class", "unknown")
            counts[cls] += 1

        constellation = {
            "id": cid,
            "title": title,
            "seedConcepts": [seed] if seed else [],
            "memberNodeIds": sorted(member_nodes),
            "memberEdgeIds": sorted({edge_id(e) for e in member_edges}),
            "stats": {
                "publicationCount": counts["publication"],
                "conceptCount": counts["concept"],
                "authorCount": counts["author"],
                "seriesCount": counts["series"],
            },
            "explanation": {
                "primarySignals": primary_signals(member_edges)
            }
        }
        constellations.append(constellation)

    return {
        "generatedAt": dt.date.today().isoformat(),
        "method": {
            "name": "deterministic-topology-clustering",
            "version": "v1",
            "notes": "Connected components on publication+concept projection with deterministic weak-context expansion"
        },
        "constellations": sorted(constellations, key=lambda c: c["id"])
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=Path("registry/knowledge_graph.json"))
    parser.add_argument("--catalog", type=Path, default=Path("registry/catalog.json"))
    parser.add_argument("--output", type=Path, default=Path("registry/constellations.json"))
    args = parser.parse_args()

    graph = read_json(args.graph)
    _ = read_json(args.catalog)  # reserved for future weighting/titles
    result = build_constellations(graph)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Wrote constellations: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
