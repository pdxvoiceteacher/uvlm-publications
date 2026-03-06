#!/usr/bin/env python3
"""Export deterministic symbolic bridge input from graph + constellation artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

CONCEPT_REL_TYPES = {"contains", "dependsOn", "refines", "extends", "contrastsWith"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def edge_id(edge: dict[str, Any]) -> str:
    return f"{edge['source']}->{edge['target']}:{edge['type']}"


def sort_key_id(item: dict[str, Any]) -> tuple:
    return (item.get("id", ""),)


def sort_key_edge(item: dict[str, Any]) -> tuple:
    return (item.get("source", ""), item.get("target", ""), item.get("type", ""))


def build_bundle(graph: dict[str, Any], constellations: dict[str, Any]) -> dict[str, Any]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    concept_nodes = [
        {
            "id": node["id"],
            "value": node.get("value", ""),
            "appearanceDate": node.get("appearanceDate"),
        }
        for node in nodes
        if node.get("class") == "concept" and isinstance(node.get("id"), str)
    ]
    concept_nodes.sort(key=sort_key_id)

    concept_relations = [
        {
            "id": edge_id(edge),
            "source": edge["source"],
            "target": edge["target"],
            "type": edge["type"],
        }
        for edge in edges
        if edge.get("type") in CONCEPT_REL_TYPES
    ]
    concept_relations.sort(key=sort_key_edge)

    publication_concept_edges = [
        {
            "id": edge_id(edge),
            "source": edge["source"],
            "target": edge["target"],
            "type": edge["type"],
        }
        for edge in edges
        if edge.get("type") == "mentionsConcept"
    ]
    publication_concept_edges.sort(key=sort_key_edge)

    concept_hierarchy = [
        {
            "id": edge_id(edge),
            "source": edge["source"],
            "target": edge["target"],
            "type": edge["type"],
        }
        for edge in edges
        if edge.get("type") == "contains"
    ]
    concept_hierarchy.sort(key=sort_key_edge)

    constellation_items = []
    for c in constellations.get("constellations", []):
        if not isinstance(c, dict):
            continue
        constellation_items.append(
            {
                "id": c.get("id"),
                "title": c.get("title"),
                "seedConcepts": sorted(c.get("seedConcepts", [])),
                "memberNodeIds": sorted(c.get("memberNodeIds", [])),
                "memberEdgeIds": sorted(c.get("memberEdgeIds", [])),
                "stats": c.get("stats", {}),
                "explanation": c.get("explanation", {}),
            }
        )
    constellation_items.sort(key=sort_key_id)

    return {
        "generatedAt": dt.date.today().isoformat(),
        "sourceArtifacts": {
            "knowledgeGraph": "registry/knowledge_graph.json",
            "constellations": "registry/constellations.json",
        },
        "conceptNodes": concept_nodes,
        "conceptRelations": concept_relations,
        "publicationConceptEdges": publication_concept_edges,
        "conceptHierarchy": concept_hierarchy,
        "constellations": constellation_items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=Path("registry/knowledge_graph.json"))
    parser.add_argument("--constellations", type=Path, default=Path("registry/constellations.json"))
    parser.add_argument("--output", type=Path, default=Path("bridge/symbolic_input.json"))
    args = parser.parse_args()

    graph = load_json(args.graph)
    constellations = load_json(args.constellations)

    bundle = build_bundle(graph, constellations)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Wrote symbolic bridge input: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
