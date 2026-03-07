#!/usr/bin/env python3
"""Compute SHA-256 content hash for paper.pdf and write it into metadata.yaml."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import yaml


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def update_metadata_hash(metadata_path: Path, paper_path: Path) -> str:
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    hash_value = sha256_file(paper_path)
    metadata["content_hash"] = hash_value
    metadata_path.write_text(yaml.safe_dump(metadata, sort_keys=False), encoding="utf-8")
    return hash_value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path, help="Path to metadata.yaml")
    parser.add_argument("--paper", type=Path, help="Path to paper.pdf (default: sibling paper.pdf)")
    args = parser.parse_args()

    paper_path = args.paper if args.paper else args.metadata.parent / "paper.pdf"
    if not args.metadata.exists() or not paper_path.exists():
        print(f"[ERROR] Missing metadata or paper file: {args.metadata}, {paper_path}")
        return 1

    hash_value = update_metadata_hash(args.metadata, paper_path)
    print(f"[OK] Updated content_hash in {args.metadata}: {hash_value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
