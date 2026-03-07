#!/usr/bin/env python3
"""Build a machine-readable publication catalog from the global index + metadata files."""

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


def build_catalog(publications_index: dict, papers_dir: Path) -> list[dict]:
    catalog: list[dict] = []

    for doi_suffix, record in sorted(publications_index.items()):
        slug = slug_from_doi_suffix(doi_suffix)
        metadata_path = papers_dir / slug / "metadata.yaml"
        if not metadata_path.exists():
            continue

        metadata = read_yaml(metadata_path)
        entry = {
            "title": metadata.get("title", record.get("title")),
            "doi": record.get("doi", "pending"),
            "authors": [author.get("name") for author in metadata.get("authors", [])],
            "date": metadata.get("publication_date", record.get("date")),
            "url": metadata.get("url"),
            "abstract": metadata.get("abstract", ""),
            "language": metadata.get("language"),
            "keywords": metadata.get("keywords", []),
            "type": metadata.get("type", record.get("type")),
            "series": metadata.get("series"),
        }
        catalog.append(entry)

    return catalog


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--publications-index",
        type=Path,
        default=Path("registry/publications.json"),
        help="Path to registry/publications.json",
    )
    parser.add_argument("--papers-dir", type=Path, default=Path("papers"), help="Path to papers directory")
    parser.add_argument("--output", type=Path, default=Path("registry/catalog.json"), help="Catalog JSON output path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    publications_index = read_json(args.publications_index)
    catalog = build_catalog(publications_index, args.papers_dir)

    args.output.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Wrote catalog with {len(catalog)} entries to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
