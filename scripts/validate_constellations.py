#!/usr/bin/env python3
"""Validate registry/constellations.json against knowledge graph references."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        dt.date.fromisoformat(value)
        return "T" not in value
    except Exception:  # noqa: BLE001
        return False


def canonical_edge_id(edge: dict[str, Any]) -> str:
    return f"{edge.get('source')}->{edge.get('target')}:{edge.get('type')}"


def validate_schema(doc: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft7Validator(schema)
    errs = []
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "<root>"
        errs.append(f"schema.{loc}: {err.message}")
    return errs


def build_graph_index(graph: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    nodes_raw = graph.get("nodes", [])
    edges_raw = graph.get("edges", [])

    nodes: dict[str, dict[str, Any]] = {}
    for node in nodes_raw:
        if isinstance(node, dict) and isinstance(node.get("id"), str):
            nodes[node["id"]] = node

    edges: dict[str, dict[str, Any]] = {}
    for edge in edges_raw:
        if isinstance(edge, dict):
            cid = canonical_edge_id(edge)
            edges[cid] = edge

    return nodes, edges


def validate_top_level(doc: Any, strict: bool) -> tuple[list[str], list[str], list[dict[str, Any]], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(doc, dict):
        return ["Constellations root must be a JSON object"], warnings, [], {}

    for key in ("generatedAt", "method", "constellations"):
        if key not in doc:
            errors.append(f"Missing top-level key: {key}")

    if errors:
        return errors, warnings, [], {}

    if not parse_iso_date(doc.get("generatedAt")):
        errors.append("generatedAt must be an ISO date string (YYYY-MM-DD)")

    method = doc.get("method")
    if not isinstance(method, dict):
        errors.append("method must be an object")
        method = {}
    else:
        if not isinstance(method.get("name"), str) or not method.get("name").strip():
            errors.append("method.name must be a non-empty string")
        if not isinstance(method.get("version"), str) or not method.get("version").strip():
            errors.append("method.version must be a non-empty string")

    constellations = doc.get("constellations")
    if not isinstance(constellations, list):
        errors.append("constellations must be an array")
        constellations = []

    if len(constellations) == 0:
        if strict:
            errors.append("constellations must not be empty in --strict mode")
        else:
            warnings.append("constellations array is empty")

    return errors, warnings, constellations, method


def validate_stats(constellation: dict[str, Any], graph_nodes: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    cid = constellation.get("id", "<unknown>")

    stats = constellation.get("stats")
    if not isinstance(stats, dict):
        return [f"stats must be object in {cid}"]

    required = ("publicationCount", "conceptCount", "authorCount", "seriesCount")
    for key in required:
        if not isinstance(stats.get(key), int) or stats.get(key) < 0:
            errors.append(f"stats.{key} must be a non-negative integer in {cid}")

    member_node_ids = constellation.get("memberNodeIds", [])
    if not isinstance(member_node_ids, list):
        return errors

    actual = {"publication": 0, "concept": 0, "author": 0, "series": 0}
    for nid in member_node_ids:
        node = graph_nodes.get(nid)
        if not node:
            continue
        klass = node.get("class")
        if klass in actual:
            actual[klass] += 1

    if isinstance(stats.get("publicationCount"), int) and stats["publicationCount"] != actual["publication"]:
        errors.append(
            f"stats.publicationCount={stats['publicationCount']} does not match actual value {actual['publication']} in {cid}"
        )
    if isinstance(stats.get("conceptCount"), int) and stats["conceptCount"] != actual["concept"]:
        errors.append(
            f"stats.conceptCount={stats['conceptCount']} does not match actual value {actual['concept']} in {cid}"
        )
    if isinstance(stats.get("authorCount"), int) and stats["authorCount"] != actual["author"]:
        errors.append(
            f"stats.authorCount={stats['authorCount']} does not match actual value {actual['author']} in {cid}"
        )
    if isinstance(stats.get("seriesCount"), int) and stats["seriesCount"] != actual["series"]:
        errors.append(
            f"stats.seriesCount={stats['seriesCount']} does not match actual value {actual['series']} in {cid}"
        )

    return errors


def validate_constellation(
    constellation: Any,
    graph_nodes: dict[str, dict[str, Any]],
    graph_edges: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []

    if not isinstance(constellation, dict):
        return ["constellation entry must be object"]

    cid = constellation.get("id")
    if not isinstance(cid, str) or not cid.strip():
        return ["constellation.id must be a non-empty string"]

    if not isinstance(constellation.get("title"), str) or not constellation.get("title").strip():
        errors.append(f"title must be a non-empty string in {cid}")

    seed_concepts = constellation.get("seedConcepts")
    if not isinstance(seed_concepts, list) or not seed_concepts:
        errors.append(f"seedConcepts must be a non-empty list in {cid}")
        seed_concepts = []
    elif len(seed_concepts) != len(set(seed_concepts)):
        errors.append(f"seedConcepts contains duplicates in {cid}")

    member_node_ids = constellation.get("memberNodeIds")
    if not isinstance(member_node_ids, list) or not member_node_ids:
        errors.append(f"memberNodeIds must be a non-empty list in {cid}")
        member_node_ids = []
    else:
        if len(member_node_ids) != len(set(member_node_ids)):
            errors.append(f"duplicate memberNodeIds in {cid}")

    member_edge_ids = constellation.get("memberEdgeIds")
    if not isinstance(member_edge_ids, list):
        errors.append(f"memberEdgeIds must be a list in {cid}")
        member_edge_ids = []
    else:
        if len(member_edge_ids) != len(set(member_edge_ids)):
            errors.append(f"duplicate memberEdgeIds in {cid}")

    for nid in member_node_ids:
        if not isinstance(nid, str) or not nid:
            errors.append(f"memberNodeIds entries must be non-empty strings in {cid}")
            continue
        if nid not in graph_nodes:
            errors.append(f"unknown memberNodeId {nid} in {cid}")

    member_node_set = set([nid for nid in member_node_ids if isinstance(nid, str)])

    for sid in seed_concepts:
        if not isinstance(sid, str) or not sid:
            errors.append(f"seedConcepts entries must be non-empty strings in {cid}")
            continue
        node = graph_nodes.get(sid)
        if node is None:
            errors.append(f"seed concept {sid} does not exist in graph for {cid}")
            continue
        if node.get("class") != "concept":
            errors.append(f"seed concept {sid} is not class=concept in {cid}")
        if sid not in member_node_set:
            errors.append(f"seed concept {sid} is not included in memberNodeIds for {cid}")

    has_member_concept = any(graph_nodes.get(nid, {}).get("class") == "concept" for nid in member_node_ids)
    if not has_member_concept:
        errors.append(f"{cid} must include at least one concept in memberNodeIds")

    for eid in member_edge_ids:
        if not isinstance(eid, str) or not eid:
            errors.append(f"memberEdgeIds entries must be non-empty strings in {cid}")
            continue
        edge = graph_edges.get(eid)
        if edge is None:
            errors.append(f"unknown memberEdgeId {eid} in {cid}")
            continue

        source = edge.get("source")
        target = edge.get("target")
        if source not in member_node_set or target not in member_node_set:
            errors.append(
                f"member edge endpoints must be included in memberNodeIds for {cid}: {eid}"
            )

    stats = constellation.get("stats")
    if not isinstance(stats, dict):
        errors.append(f"stats must be object in {cid}")

    explanation = constellation.get("explanation")
    if not isinstance(explanation, dict):
        errors.append(f"explanation must be object in {cid}")
    else:
        primary = explanation.get("primarySignals")
        if not isinstance(primary, list) or len(primary) == 0:
            errors.append(f"explanation.primarySignals must be a non-empty list in {cid}")
        elif not all(isinstance(x, str) and x.strip() for x in primary):
            errors.append(f"explanation.primarySignals must contain non-empty strings in {cid}")

    errors.extend(validate_stats(constellation, graph_nodes))

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("constellations", nargs="?", type=Path, help="Path to constellations JSON")
    parser.add_argument("graph", nargs="?", type=Path, help="Path to knowledge graph JSON")
    parser.add_argument("--constellations", dest="constellations_opt", type=Path)
    parser.add_argument("--graph", dest="graph_opt", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--schema", type=Path, default=Path("schemas/constellations_schema.json"))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    const_path = args.constellations_opt or args.constellations
    graph_path = args.graph_opt or args.graph or Path("registry/knowledge_graph.json")

    if const_path is None:
        parser.error("constellations path required (positional or --constellations)")

    const_doc = load_json(const_path)
    graph_doc = load_json(graph_path)
    graph_nodes, graph_edges = build_graph_index(graph_doc)

    errors = validate_schema(const_doc, args.schema)
    top_errors, warnings, constellations, method = validate_top_level(const_doc, strict=args.strict)
    errors.extend(top_errors)

    seen_ids: set[str] = set()
    last_id = ""
    for i, constellation in enumerate(constellations):
        c_errors = validate_constellation(constellation, graph_nodes, graph_edges)
        errors.extend(c_errors)

        cid = constellation.get("id") if isinstance(constellation, dict) else None
        if isinstance(cid, str) and cid:
            if cid in seen_ids:
                errors.append(f"duplicate constellation id: {cid}")
            seen_ids.add(cid)
            if last_id and cid < last_id:
                errors.append("constellations must be sorted by id")
            last_id = cid
        else:
            errors.append(f"constellations[{i}] has invalid or missing id")

    if errors:
        print(f"{const_path.name} is invalid")
        for err in errors:
            print(f"ERROR: {err}")
        for warn in warnings:
            print(f"WARNING: {warn}")
        return 1

    print(f"{const_path.name} is valid")
    print(f"constellations: {len(constellations)}")
    print(f"graph nodes indexed: {len(graph_nodes)}")
    print(f"graph edges indexed: {len(graph_edges)}")
    if isinstance(method, dict):
        print(f"method: {method.get('name')} {method.get('version')}")
    for warn in warnings:
        print(f"WARNING: {warn}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
