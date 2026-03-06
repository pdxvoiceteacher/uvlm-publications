#!/usr/bin/env python3
"""Build a deterministic UVLM knowledge graph from catalog metadata and declared paper relations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

PUBLICATION_RELATION_TYPES = {"cites", "isVersionOf", "isPartOf", "isReferencedBy"}
CONCEPT_RELATION_TYPES = {"contains", "dependsOn", "refines", "extends", "contrastsWith"}


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
    existing = nodes.get(node["id"])
    if existing is None:
        nodes[node["id"]] = node
        return

    merged = dict(existing)
    for key, value in node.items():
        if key not in merged or merged[key] in (None, "", []):
            merged[key] = value
    nodes[node["id"]] = merged


def add_edge(edges: dict[str, dict], edge: dict) -> None:
    key = f"{edge['source']}|{edge['type']}|{edge['target']}"
    edges[key] = edge


def add_concept_node(nodes: dict[str, dict], concept: str) -> str:
    c_id = concept_id(concept)
    add_node(nodes, {"id": c_id, "class": "concept", "value": concept})
    return c_id


def normalize_doi_suffix(entry: dict) -> str:
    doi = entry.get("doi", "pending")
    if doi != "pending" and "/" in doi:
        return suffix_from_doi(doi)
    url = entry.get("url", "")
    slug = url.rstrip("/").split("/")[-1] if url else "unknown"
    return f"uvlm.{entry.get('type', 'paper')}.{slug}.v1"


def metadata_by_suffix(papers_dir: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for metadata_path in sorted(papers_dir.glob("*/metadata.yaml")):
        metadata = read_yaml(metadata_path)
        suffix = metadata.get("doi_suffix")
        if isinstance(suffix, str) and suffix:
            result[suffix] = metadata
    return result


def publication_object(doi_suffix: str, catalog_entry: dict | None, metadata: dict | None, doi_hint: str | None = None) -> dict:
    doi_value = doi_hint
    if catalog_entry:
        doi_value = catalog_entry.get("doi")
    if not isinstance(doi_value, str) or not doi_value:
        doi_value = f"pending/{doi_suffix}"

    title = (metadata or {}).get("title") or (catalog_entry or {}).get("title") or doi_suffix
    abstract = (metadata or {}).get("abstract") or (catalog_entry or {}).get("abstract") or "No abstract available."
    date = (metadata or {}).get("publication_date") or (catalog_entry or {}).get("date")
    if not date:
        date = "1900-01-01"

    url = (metadata or {}).get("url") or (catalog_entry or {}).get("url")
    if not url:
        url = f"https://doi.org/{doi_value}" if doi_value != "pending" else f"https://ultraverbaluxmentis.org/publications/{slug_from_doi_suffix(doi_suffix)}"

    authors = [a.get("name") for a in (metadata or {}).get("authors", []) if isinstance(a, dict) and a.get("name")]
    if not authors:
        authors = [a for a in (catalog_entry or {}).get("authors", []) if isinstance(a, str) and a]

    keywords = [k for k in (metadata or {}).get("keywords", []) if isinstance(k, str) and k]
    if not keywords:
        keywords = [k for k in (catalog_entry or {}).get("keywords", []) if isinstance(k, str) and k]

    concepts = [c for c in (metadata or {}).get("concepts", []) if isinstance(c, str) and c]
    series = (metadata or {}).get("series") or (catalog_entry or {}).get("series")
    pub_type = (metadata or {}).get("type") or (catalog_entry or {}).get("type") or "paper"

    return {
        "id": publication_id(doi_suffix),
        "class": "publication",
        "title": title,
        "doi": doi_value,
        "doi_suffix": doi_suffix,
        "date": date,
        "url": url,
        "abstract": abstract,
        "authors": authors,
        "keywords": keywords,
        "concepts": concepts,
        "series": series,
        "type": pub_type,
        "publication_type": pub_type,
    }


def build_graph(catalog: list[dict], papers_dir: Path) -> dict:
    nodes: dict[str, dict] = {}
    edges: dict[str, dict] = {}

    catalog_map: dict[str, dict] = {}
    for entry in catalog:
        catalog_map[normalize_doi_suffix(entry)] = entry

    metadata_map = metadata_by_suffix(papers_dir)

    for doi_suffix in sorted(set(catalog_map) | set(metadata_map)):
        entry = catalog_map.get(doi_suffix)
        metadata = metadata_map.get(doi_suffix)
        pub = publication_object(doi_suffix, entry, metadata)
        pub_id = pub["id"]
        add_node(nodes, pub)

        series_name = pub.get("series")
        if series_name:
            s_id = series_id(series_name)
            add_node(nodes, {"id": s_id, "class": "series", "name": series_name})
            add_edge(edges, {"source": pub_id, "target": s_id, "type": "publishedIn"})

        for author in pub.get("authors", []):
            a_id = author_id(author)
            add_node(nodes, {"id": a_id, "class": "author", "name": author})
            add_edge(edges, {"source": pub_id, "target": a_id, "type": "authoredBy"})

        for keyword in pub.get("keywords", []):
            k_id = keyword_id(keyword)
            add_node(nodes, {"id": k_id, "class": "keyword", "value": keyword})
            add_edge(edges, {"source": pub_id, "target": k_id, "type": "taggedWith"})

        for concept in pub.get("concepts", []):
            c_id = add_concept_node(nodes, concept)
            add_edge(edges, {"source": pub_id, "target": c_id, "type": "mentionsConcept"})

        metadata = metadata or {}
        for concept_relation in metadata.get("concept_relations", []):
            source_concept = concept_relation.get("source", "")
            target_concept = concept_relation.get("target", "")
            relation_type = concept_relation.get("type")
            if not source_concept or not target_concept or relation_type not in CONCEPT_RELATION_TYPES:
                continue

            source_id = add_concept_node(nodes, source_concept)
            target_id = add_concept_node(nodes, target_concept)
            add_edge(edges, {"source": source_id, "target": target_id, "type": relation_type})

        for rel in metadata.get("relations", []):
            rel_type = rel.get("type")
            rel_doi = rel.get("doi", "")
            if rel_type not in PUBLICATION_RELATION_TYPES or not rel_doi:
                continue

            target_suffix = suffix_from_doi(rel_doi)
            target_pub = publication_object(
                target_suffix,
                catalog_map.get(target_suffix),
                metadata_map.get(target_suffix),
                doi_hint=rel_doi,
            )
            target_id = target_pub["id"]
            if target_id == pub_id:
                continue
            add_node(nodes, target_pub)
            add_edge(edges, {"source": pub_id, "target": target_id, "type": rel_type, "doi": rel_doi})

        previous_doi = metadata.get("previous_doi")
        if previous_doi:
            target_suffix = suffix_from_doi(previous_doi)
            target_pub = publication_object(
                target_suffix,
                catalog_map.get(target_suffix),
                metadata_map.get(target_suffix),
                doi_hint=previous_doi,
            )
            target_id = target_pub["id"]
            add_node(nodes, target_pub)
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
