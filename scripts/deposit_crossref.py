#!/usr/bin/env python3
"""Deposit Crossref XML and update DOI registry."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests
import yaml

CROSSREF_TEST_ENDPOINT = "https://test.crossref.org/servlet/deposit"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True, help="Path to metadata.yaml")
    parser.add_argument("--xml", type=Path, required=True, help="Path to Crossref XML file")
    parser.add_argument("--registry", type=Path, default=Path("registry/dois.json"), help="Path to DOI registry")
    parser.add_argument("--endpoint", default=CROSSREF_TEST_ENDPOINT, help="Crossref deposit endpoint")
    parser.add_argument("--simulate", action="store_true", help="Skip API request and simulate successful deposit")
    return parser.parse_args()


def load_required_env() -> tuple[str, str, str]:
    username = os.getenv("CROSSREF_USERNAME")
    password = os.getenv("CROSSREF_PASSWORD")
    doi_prefix = os.getenv("DOI_PREFIX")

    if not all([username, password, doi_prefix]):
        missing = [
            name
            for name, value in (
                ("CROSSREF_USERNAME", username),
                ("CROSSREF_PASSWORD", password),
                ("DOI_PREFIX", doi_prefix),
            )
            if not value
        ]
        raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")

    return username, password, doi_prefix


def update_registry(registry_path: Path, metadata: dict, doi: str) -> None:
    registry = {}
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))

    registry[metadata["doi_suffix"]] = {
        "doi": doi,
        "title": metadata["title"],
        "version": metadata.get("version", "v1"),
        "date": metadata["publication_date"],
    }

    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()

    try:
        username, password, doi_prefix = load_required_env()
    except EnvironmentError as exc:
        print(f"[ERROR] {exc}")
        return 1

    metadata = yaml.safe_load(args.metadata.read_text(encoding="utf-8"))
    target_doi = f"{doi_prefix}/{metadata['doi_suffix']}"

    if args.simulate:
        print(f"[SIMULATE] Deposit skipped. Would mint DOI: {target_doi}")
        update_registry(args.registry, metadata, target_doi)
        return 0

    files = {"fname": (args.xml.name, args.xml.read_bytes(), "application/xml")}
    response = requests.post(args.endpoint, auth=(username, password), files=files, timeout=60)

    if response.status_code >= 300:
        print(f"[ERROR] Crossref deposit failed: HTTP {response.status_code}\n{response.text}")
        return 1

    print("[OK] Crossref deposit accepted")
    update_registry(args.registry, metadata, target_doi)
    print(f"[OK] Registry updated: {args.registry}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
