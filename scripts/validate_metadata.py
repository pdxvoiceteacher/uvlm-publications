#!/usr/bin/env python3
"""Validate publication metadata files against the publication JSON schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


DEFAULT_SCHEMA_PATH = Path("schemas/publication_schema.json")
DEFAULT_PAPERS_DIR = Path("papers")


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Metadata file {path} must contain a YAML object at the top level.")
    return data


def load_schema(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def discover_metadata_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(path.glob("*/metadata.yaml"))


def validate_files(metadata_files: list[Path], schema: dict) -> int:
    validator = Draft202012Validator(schema)
    has_errors = False

    for metadata_file in metadata_files:
        try:
            metadata = load_yaml(metadata_file)
        except Exception as exc:  # noqa: BLE001
            has_errors = True
            print(f"[ERROR] Could not read {metadata_file}: {exc}")
            continue

        errors = sorted(validator.iter_errors(metadata), key=lambda e: e.path)
        if not errors:
            print(f"[OK] {metadata_file}")
            continue

        has_errors = True
        print(f"[ERROR] {metadata_file} failed validation:")
        for err in errors:
            location = ".".join(str(item) for item in err.path) or "<root>"
            print(f"  - {location}: {err.message}")

    return 1 if has_errors else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to JSON schema (default: schemas/publication_schema.json)",
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=DEFAULT_PAPERS_DIR,
        help="Metadata file or papers directory to validate (default: papers)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.schema.exists():
        print(f"[ERROR] Schema file not found: {args.schema}")
        return 1

    metadata_files = discover_metadata_files(args.path)
    if not metadata_files:
        print(f"[ERROR] No metadata.yaml files found under: {args.path}")
        return 1

    schema = load_schema(args.schema)
    return validate_files(metadata_files, schema)


if __name__ == "__main__":
    sys.exit(main())
