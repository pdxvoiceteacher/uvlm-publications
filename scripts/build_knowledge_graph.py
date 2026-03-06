#!/usr/bin/env python3
"""Generate a publication knowledge graph from metadata relations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def slug_from_doi_suffix(doi_suffix: str) -> str:
    parts = doi_suffix.split(".")
    if len(parts) < 4:
        raise ValueError(f"Invalid DOI suffix format: {doi_suffix}")
    return parts[2]


def target_from_relation_doi(doi: str) -> str:
    suffix = doi.split("/", 1)[1] if "/" in doi else doi
    parts = suffix.split(".")
    return parts[2] if len(parts) >= 4 else suffix


def build_graph(publications_index: dict, papers_dir: Path) -> dict:
    nodes = []
    edges = []

    for doi_suffix, record in sorted(publications_index.items()):
        slug = slug_from_doi_suffix(doi_suffix)
        metadata_path = papers_dir / slug / "metadata.yaml"
        if not metadata_path.exists():
            continue

        metadata = read_yaml(metadata_path)
        nodes.append(
            {
                "id": slug,
                "doi_suffix": doi_suffix,
                "title": metadata.get("title", record.get("title")),
                "type": metadata.get("type", record.get("type")),
                "date": metadata.get("publication_date", record.get("date")),
            }
        )

        for rel in metadata.get("relations", []):
            edges.append(
                {
                    "from": slug,
                    "to": target_from_relation_doi(rel.get("doi", "")),
                    "relation_type": rel.get("type", "related"),
                    "doi": rel.get("doi", ""),
                }
            )

    return {"nodes": nodes, "edges": edges}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--publications-index",
        type=Path,
        default=Path("registry/publications.json"),
        help="Path to registry/publications.json",
    )
    parser.add_argument("--papers-dir", type=Path, default=Path("papers"), help="Path to papers directory")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("registry/knowledge_graph.json"),
        help="Knowledge graph output path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    publications_index = read_json(args.publications_index)
    graph = build_graph(publications_index, args.papers_dir)
    args.output.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Wrote knowledge graph to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
