#!/usr/bin/env python3
"""Generate Crossref deposit XML from a publication metadata YAML file."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

DOI_SUFFIX_PATTERN = re.compile(r"^uvlm\.(paper|dataset|software)\.[a-z0-9-]+\.v[0-9]+$")


def add_relations(journal_article: ET.Element, relations: list[dict]) -> None:
    if not relations:
        return

    program = ET.SubElement(
        journal_article,
        "program",
        {
            "xmlns:rel": "http://www.crossref.org/relations.xsd",
            "name": "relations",
        },
    )
    rel_program = ET.SubElement(program, "rel:program")

    for relation in relations:
        related_item = ET.SubElement(rel_program, "rel:related_item")
        relation_node = ET.SubElement(
            related_item,
            "rel:intra_work_relation",
            {
                "relationship-type": relation["type"],
                "identifier-type": "doi",
            },
        )
        relation_node.text = relation["doi"]


def build_xml(metadata: dict, doi_prefix: str, depositor_email: str, batch_id: str) -> ET.Element:
    if not DOI_SUFFIX_PATTERN.match(metadata["doi_suffix"]):
        raise ValueError(f"Invalid DOI suffix format: {metadata['doi_suffix']}")

    now = dt.datetime.utcnow()
    root = ET.Element(
        "doi_batch",
        {
            "version": "4.4.2",
            "xmlns": "http://www.crossref.org/schema/4.4.2",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.crossref.org/schema/4.4.2 http://www.crossref.org/schemas/crossref4.4.2.xsd",
        },
    )

    head = ET.SubElement(root, "head")
    ET.SubElement(head, "doi_batch_id").text = batch_id
    ET.SubElement(head, "timestamp").text = now.strftime("%Y%m%d%H%M%S")
    depositor = ET.SubElement(head, "depositor")
    ET.SubElement(depositor, "depositor_name").text = metadata.get("publisher", "UVLM")
    ET.SubElement(depositor, "email_address").text = depositor_email
    ET.SubElement(head, "registrant").text = metadata.get("publisher", "Ultra Verba Lux Mentis")

    body = ET.SubElement(root, "body")
    journal = ET.SubElement(body, "journal")

    journal_metadata = ET.SubElement(journal, "journal_metadata")
    ET.SubElement(journal_metadata, "full_title").text = metadata.get("publisher", "Ultra Verba Lux Mentis")
    ET.SubElement(journal_metadata, "abbrev_title").text = "UVLM"
    ET.SubElement(journal_metadata, "issn", media_type="electronic").text = "0000-0000"

    journal_issue = ET.SubElement(journal, "journal_issue")
    publication_date = ET.SubElement(journal_issue, "publication_date", media_type="online")
    date_value = dt.date.fromisoformat(metadata["publication_date"])
    ET.SubElement(publication_date, "year").text = str(date_value.year)
    ET.SubElement(publication_date, "month").text = f"{date_value.month:02d}"
    ET.SubElement(publication_date, "day").text = f"{date_value.day:02d}"

    journal_article = ET.SubElement(journal, "journal_article", publication_type="full_text")
    titles = ET.SubElement(journal_article, "titles")
    ET.SubElement(titles, "title").text = metadata["title"]

    contributors = ET.SubElement(journal_article, "contributors")
    for index, author in enumerate(metadata.get("authors", []), start=1):
        full_name = author.get("name", "").strip()
        parts = full_name.split()
        given = parts[0] if parts else ""
        surname = " ".join(parts[1:]) if len(parts) > 1 else given

        person = ET.SubElement(
            contributors,
            "person_name",
            contributor_role="author",
            sequence="first" if index == 1 else "additional",
        )
        ET.SubElement(person, "given_name").text = given
        ET.SubElement(person, "surname").text = surname
        ET.SubElement(person, "ORCID").text = f"https://orcid.org/{author['orcid']}"

    pub_date = ET.SubElement(journal_article, "publication_date", media_type="online")
    ET.SubElement(pub_date, "year").text = str(date_value.year)
    ET.SubElement(pub_date, "month").text = f"{date_value.month:02d}"
    ET.SubElement(pub_date, "day").text = f"{date_value.day:02d}"

    if metadata.get("abstract"):
        abstract = ET.SubElement(journal_article, "jats:abstract")
        abstract.set("xmlns:jats", "http://www.ncbi.nlm.nih.gov/JATS1")
        ET.SubElement(abstract, "jats:p").text = metadata["abstract"]

    add_relations(journal_article, metadata.get("relations", []))

    doi_data = ET.SubElement(journal_article, "doi_data")
    ET.SubElement(doi_data, "doi").text = f"{doi_prefix}/{metadata['doi_suffix']}"
    ET.SubElement(doi_data, "resource").text = metadata["url"]

    return root


def indent(element: ET.Element, level: int = 0) -> None:
    whitespace = "\n" + level * "  "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = whitespace + "  "
        for child in element:
            indent(child, level + 1)
        if not element.tail or not element.tail.strip():
            element.tail = whitespace
    elif level and (not element.tail or not element.tail.strip()):
        element.tail = whitespace


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path, help="Path to metadata.yaml")
    parser.add_argument("--doi-prefix", required=True, help="DOI prefix, e.g. 10.1234")
    parser.add_argument("--depositor-email", required=True, help="Crossref depositor email")
    parser.add_argument("--batch-id", default="uvlm-batch", help="Crossref batch ID")
    parser.add_argument("--output", type=Path, default=Path("crossref_deposit.xml"), help="Output XML file path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = yaml.safe_load(args.metadata.read_text(encoding="utf-8"))

    root = build_xml(metadata, args.doi_prefix, args.depositor_email, args.batch_id)
    indent(root)
    ET.ElementTree(root).write(args.output, encoding="utf-8", xml_declaration=True)
    print(f"Generated {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
