#!/usr/bin/env python3
"""Deposit Crossref XML and update DOI registries with audit logging."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import yaml

CROSSREF_TEST_ENDPOINT = "https://test.crossref.org/servlet/deposit"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True, help="Path to metadata.yaml")
    parser.add_argument("--xml", type=Path, required=True, help="Path to Crossref XML file")
    parser.add_argument("--registry", type=Path, default=Path("registry/dois.json"), help="Path to DOI slug registry")
    parser.add_argument(
        "--publications-index",
        type=Path,
        default=Path("registry/publications.json"),
        help="Path to global DOI-suffix publication index",
    )
    parser.add_argument("--deposits-dir", type=Path, default=Path("registry/deposits"), help="Path to deposit logs")
    parser.add_argument("--endpoint", default=CROSSREF_TEST_ENDPOINT, help="Crossref deposit endpoint")
    parser.add_argument("--dry-run", action="store_true", help="Validate payload and log attempt without minting DOI")
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


def validate_xml(xml_path: Path) -> None:
    ET.parse(xml_path)


def update_slug_registry(registry_path: Path, metadata: dict, doi: str, status: str) -> None:
    registry = {}
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))

    key = metadata["doi_suffix"].split(".")[2]
    registry[key] = {
        "doi": doi,
        "status": status,
        "title": metadata["title"],
        "version": metadata.get("version", "v1"),
        "date": metadata["publication_date"],
    }

    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


def update_publications_index(index_path: Path, metadata: dict, doi: str, status: str) -> None:
    index = {}
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))

    key = metadata["doi_suffix"]
    index[key] = {
        "title": metadata["title"],
        "doi": doi,
        "type": metadata["type"],
        "date": metadata["publication_date"],
        "status": status,
    }

    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")


def write_deposit_log(deposits_dir: Path, metadata: dict, doi: str, status: str, detail: str) -> Path:
    deposits_dir.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    deposit_id = str(uuid.uuid4())
    slug = metadata["doi_suffix"].split(".")[2]
    log_path = deposits_dir / f"{metadata['publication_date']}_{slug}.json"

    payload = {
        "deposit_id": deposit_id,
        "timestamp": timestamp,
        "status": status,
        "doi": doi,
        "detail": detail,
    }
    log_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return log_path


def write_indexes(args: argparse.Namespace, metadata: dict, doi: str, status: str) -> None:
    update_slug_registry(args.registry, metadata, doi, status)
    update_publications_index(args.publications_index, metadata, doi, status)


def main() -> int:
    args = parse_args()

    try:
        username, password, doi_prefix = load_required_env()
    except EnvironmentError as exc:
        print(f"[ERROR] {exc}")
        return 1

    metadata = yaml.safe_load(args.metadata.read_text(encoding="utf-8"))
    target_doi = f"{doi_prefix}/{metadata['doi_suffix']}"

    try:
        validate_xml(args.xml)
    except ET.ParseError as exc:
        print(f"[ERROR] Invalid XML document: {exc}")
        write_indexes(args, metadata, target_doi, "failed")
        write_deposit_log(args.deposits_dir, metadata, target_doi, "failed", f"XML parse failure: {exc}")
        return 1

    if args.dry_run:
        print(f"[DRY-RUN] Deposit validation completed for DOI: {target_doi}")
        write_indexes(args, metadata, target_doi, "pending")
        log_path = write_deposit_log(args.deposits_dir, metadata, target_doi, "pending", "Dry-run validation only")
        print(f"[OK] Dry-run log written: {log_path}")
        return 0

    files = {"fname": (args.xml.name, args.xml.read_bytes(), "application/xml")}
    response = requests.post(args.endpoint, auth=(username, password), files=files, timeout=60)

    if response.status_code >= 300:
        detail = f"Crossref deposit failed: HTTP {response.status_code}"
        print(f"[ERROR] {detail}\n{response.text}")
        write_indexes(args, metadata, target_doi, "failed")
        write_deposit_log(args.deposits_dir, metadata, target_doi, "failed", detail)
        return 1

    print("[OK] Crossref deposit accepted")
    write_indexes(args, metadata, target_doi, "registered")
    log_path = write_deposit_log(args.deposits_dir, metadata, target_doi, "registered", "Crossref accepted deposit")
    print(f"[OK] Registries updated: {args.registry}, {args.publications_index}")
    print(f"[OK] Deposit log written: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
