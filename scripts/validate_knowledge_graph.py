#!/usr/bin/env python3
"""Validate knowledge graph artifact against expected shape and classes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALLOWED_NODE_CLASSES = {"publication", "author", "keyword", "series", "concept"}
ALLOWED_EDGE_TYPES = {
    "authoredBy",
    "taggedWith",
    "publishedIn",
    "mentionsConcept",
    "cites",
    "isVersionOf",
    "isPartOf",
    "isReferencedBy",
}


def validate_graph(path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        return ["Graph root must be an object"]

    nodes = data.get("nodes")
    edges = data.get("edges")

    if not isinstance(nodes, list):
        errors.append("`nodes` must be an array")
        nodes = []
    if not isinstance(edges, list):
        errors.append("`edges` must be an array")
        edges = []

    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"nodes[{index}] must be an object")
            continue

        node_id = node.get("id")
        node_class = node.get("class")
        if not isinstance(node_id, str) or not node_id:
            errors.append(f"nodes[{index}].id must be a non-empty string")
        elif node_id in node_ids:
            errors.append(f"nodes[{index}].id duplicates existing node: {node_id}")
        else:
            node_ids.add(node_id)

        if node_class not in ALLOWED_NODE_CLASSES:
            errors.append(f"nodes[{index}].class must be one of {sorted(ALLOWED_NODE_CLASSES)}")

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edges[{index}] must be an object")
            continue

        source = edge.get("source")
        target = edge.get("target")
        edge_type = edge.get("type")

        if not isinstance(source, str) or not source:
            errors.append(f"edges[{index}].source must be a non-empty string")
        if not isinstance(target, str) or not target:
            errors.append(f"edges[{index}].target must be a non-empty string")
        if edge_type not in ALLOWED_EDGE_TYPES:
            errors.append(f"edges[{index}].type must be one of {sorted(ALLOWED_EDGE_TYPES)}")

        if isinstance(source, str) and source and source not in node_ids:
            errors.append(f"edges[{index}].source does not exist in nodes: {source}")
        if isinstance(target, str) and target and target not in node_ids:
            errors.append(f"edges[{index}].target does not exist in nodes: {target}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path, help="Path to knowledge_graph.json")
    args = parser.parse_args()

    errors = validate_graph(args.graph)
    if errors:
        print("[ERROR] Knowledge graph validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"[OK] Knowledge graph validated: {args.graph}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
