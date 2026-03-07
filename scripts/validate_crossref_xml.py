#!/usr/bin/env python3
"""Validate generated Crossref XML for well-formedness and required structure."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REQUIRED_TAGS = [
    "doi_batch",
    "head",
    "body",
    "journal",
    "journal_article",
    "doi_data",
    "doi",
    "resource",
]


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def find_first(root: ET.Element, wanted: str) -> ET.Element | None:
    for node in root.iter():
        if local_name(node.tag) == wanted:
            return node
    return None


def validate(xml_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as exc:
        return [f"XML is not well-formed: {exc}"]

    for tag in REQUIRED_TAGS:
        if find_first(root, tag) is None:
            errors.append(f"Missing required tag: {tag}")

    doi_node = find_first(root, "doi")
    if doi_node is not None and not (doi_node.text or "").strip():
        errors.append("DOI node is present but empty")

    resource_node = find_first(root, "resource")
    if resource_node is not None:
        resource_text = (resource_node.text or "").strip()
        if not resource_text:
            errors.append("Resource node is present but empty")
        elif not resource_text.startswith("https://"):
            errors.append("Resource URL must start with https://")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path, help="Path to Crossref XML file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate(args.xml)

    if errors:
        print("[ERROR] Crossref XML validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"[OK] Crossref XML validated: {args.xml}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
