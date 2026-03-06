#!/usr/bin/env python3
"""Build a deterministic UVLM knowledge graph from catalog metadata and declared paper relations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

PUBLICATION_RELATION_TYPES = {"cites", "isVersionOf", "isPartOf", "isReferencedBy"}


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Metadata file must contain a YAML object: {path}")
    return data


def slug_from_doi_suffix(doi_suffix: str) -> str:
    parts = doi_suffix.split(".")
    if len(parts) < 4:
        raise ValueError(f"Invalid DOI suffix format: {doi_suffix}")
    return parts[2]


def suffix_from_doi(doi: str) -> str:
    return doi.split("/", 1)[1] if "/" in doi else doi


def slugify(value: str) -> str:
    return value.strip().lower().replace(" ", "-")


def publication_id(doi_suffix: str) -> str:
    return f"publication:{doi_suffix}"


def author_id(name: str) -> str:
    return f"author:{slugify(name)}"


def keyword_id(keyword: str) -> str:
    return f"keyword:{slugify(keyword)}"


def series_id(series: str) -> str:
    return f"series:{slugify(series)}"


def concept_id(concept: str) -> str:
    return f"concept:{slugify(concept)}"


def relation_target_publication_id(doi: str) -> str:
    return publication_id(suffix_from_doi(doi))


def add_node(nodes: dict[str, dict], node: dict) -> None:
    nodes[node["id"]] = node


def add_edge(edges: dict[str, dict], edge: dict) -> None:
    key = f"{edge['source']}|{edge['type']}|{edge['target']}"
    edges[key] = edge


def build_graph(catalog: list[dict], papers_dir: Path) -> dict:
    nodes: dict[str, dict] = {}
    edges: dict[str, dict] = {}

    for entry in sorted(catalog, key=lambda item: item.get("title", "")):
        doi = entry.get("doi", "pending")
        doi_suffix = suffix_from_doi(doi) if doi != "pending" and "/" in doi else None
        if not doi_suffix:
            url = entry.get("url", "")
            slug = url.rstrip("/").split("/")[-1] if url else "unknown"
            doi_suffix = f"uvlm.{entry.get('type', 'paper')}.{slug}.v1"

        pub_id = publication_id(doi_suffix)
        add_node(
            nodes,
            {
                "id": pub_id,
                "class": "publication",
                "title": entry.get("title"),
                "doi": doi,
                "doi_suffix": doi_suffix,
                "date": entry.get("date"),
                "url": entry.get("url"),
                "publication_type": entry.get("type"),
            },
        )

        series_name = entry.get("series")
        if series_name:
            s_id = series_id(series_name)
            add_node(nodes, {"id": s_id, "class": "series", "name": series_name})
            add_edge(edges, {"source": pub_id, "target": s_id, "type": "publishedIn"})

        for author in entry.get("authors", []):
            if not author:
                continue
            a_id = author_id(author)
            add_node(nodes, {"id": a_id, "class": "author", "name": author})
            add_edge(edges, {"source": pub_id, "target": a_id, "type": "authoredBy"})

        for keyword in entry.get("keywords", []):
            if not keyword:
                continue
            k_id = keyword_id(keyword)
            add_node(nodes, {"id": k_id, "class": "keyword", "value": keyword})
            add_edge(edges, {"source": pub_id, "target": k_id, "type": "taggedWith"})

        slug = slug_from_doi_suffix(doi_suffix)
        metadata_path = papers_dir / slug / "metadata.yaml"
        if not metadata_path.exists():
            continue

        metadata = read_yaml(metadata_path)

        for concept in metadata.get("concepts", []):
            if not concept:
                continue
            c_id = concept_id(concept)
            add_node(nodes, {"id": c_id, "class": "concept", "value": concept})
            add_edge(edges, {"source": pub_id, "target": c_id, "type": "mentionsConcept"})

        for rel in metadata.get("relations", []):
            rel_type = rel.get("type")
            rel_doi = rel.get("doi", "")
            if rel_type not in PUBLICATION_RELATION_TYPES or not rel_doi:
                continue

            target_id = relation_target_publication_id(rel_doi)
            add_node(
                nodes,
                {
                    "id": target_id,
                    "class": "publication",
                    "title": None,
                    "doi": rel_doi,
                    "doi_suffix": suffix_from_doi(rel_doi),
                    "date": None,
                    "url": None,
                    "publication_type": None,
                },
            )
            add_edge(edges, {"source": pub_id, "target": target_id, "type": rel_type, "doi": rel_doi})

        previous_doi = metadata.get("previous_doi")
        if previous_doi:
            target_id = relation_target_publication_id(previous_doi)
            add_node(
                nodes,
                {
                    "id": target_id,
                    "class": "publication",
                    "title": None,
                    "doi": previous_doi,
                    "doi_suffix": suffix_from_doi(previous_doi),
                    "date": None,
                    "url": None,
                    "publication_type": None,
                },
            )
            add_edge(edges, {"source": pub_id, "target": target_id, "type": "isVersionOf", "doi": previous_doi})

    return {
        "nodes": [nodes[key] for key in sorted(nodes)],
        "edges": [edges[key] for key in sorted(edges)],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=Path("registry/catalog.json"), help="Path to catalog JSON")
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
    catalog_data = read_json(args.catalog)
    if not isinstance(catalog_data, list):
        raise ValueError("Catalog must be a JSON array")

    graph = build_graph(catalog_data, args.papers_dir)
    args.output.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Wrote knowledge graph to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
