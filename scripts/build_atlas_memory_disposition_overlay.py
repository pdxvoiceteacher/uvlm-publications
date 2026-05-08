#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DISPOSITION_SCHEMA = "atlas.memory_disposition_packet.v1"
REGISTRY_SCHEMA = "atlas.memory_disposition_registry.v1"
QUEUE_SCHEMA = "atlas.memory_review_queue.v1"
ANNOTATIONS_SCHEMA = "atlas.memory_disposition_annotations.v1"
NON_AUTHORITATIVE_STATUSES = {
    "pending_human_review",
    "retrieval_candidate",
    "quarantine",
    "reject",
    "needs_more_evidence",
    "ltm_candidate_review_required",
}
ANNOTATION_STATUSES = {"quarantine", "reject", "needs_more_evidence"}


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _require_false(payload: dict[str, Any], key: str) -> None:
    if payload.get(key) is not False:
        raise ValueError(f"{key} must remain false")


def _validate_disposition(packet: dict[str, Any]) -> None:
    if packet.get("schema") != DISPOSITION_SCHEMA:
        raise ValueError(f"schema must be {DISPOSITION_SCHEMA}")
    disposition = packet.get("disposition")
    if not isinstance(disposition, dict):
        raise ValueError("disposition must be an object")
    status = disposition.get("status")
    if status not in NON_AUTHORITATIVE_STATUSES:
        raise ValueError(f"Unsupported disposition status: {status}")

    authority = packet.get("authority_boundary")
    if not isinstance(authority, dict):
        raise ValueError("authority_boundary must be an object")
    for key in (
        "memory_write_authorized",
        "prior_canonized",
        "truth_certified",
        "deployment_authorized",
        "publisher_finalized",
        "canonical_publication_mutated",
    ):
        _require_false(authority, key)


def build_overlay_outputs(
    packet: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _validate_disposition(packet)
    disposition = packet["disposition"]
    status = disposition["status"]

    base_entry = {
        "dispositionId": packet["disposition_id"],
        "memoryIntentId": packet["memory_intent_id"],
        "status": status,
        "allowedUse": disposition["allowed_use"],
        "retentionBand": disposition["retention_band"],
        "sensitivityClass": disposition["sensitivity_class"],
        "reasonCodes": list(disposition.get("reason_codes", [])),
        "requiresHumanReview": packet["review_requirements"]["requires_human_review"],
        "sourcePacketSchema": packet["source_packet_schema"],
    }

    registry = {
        "schema": REGISTRY_SCHEMA,
        "entries": [base_entry],
        "nonAuthoritativeOnly": True,
        "noMemoryIndexMutation": True,
        "noCanonicalPublicationMutation": True,
        "noDoiRegistryMutation": True,
    }

    queue_entries = []
    if status in {
        "ltm_candidate_review_required",
        "pending_human_review",
        "retrieval_candidate",
    }:
        queue_entries.append(
            {
                **base_entry,
                "queueReason": "ltm_review_required"
                if status == "ltm_candidate_review_required"
                else "human_review_required",
            }
        )
    review_queue = {
        "schema": QUEUE_SCHEMA,
        "entries": queue_entries,
        "ltmCandidatesRequireHumanReview": True,
        "noMemoryIndexMutation": True,
    }

    annotation_entries = []
    if status in ANNOTATION_STATUSES:
        annotation_entries.append({**base_entry, "annotationType": "watchlist"})
    annotations = {
        "schema": ANNOTATIONS_SCHEMA,
        "entries": annotation_entries,
        "watchlistOnly": True,
        "noCanonicalPublicationMutation": True,
        "noDoiRegistryMutation": True,
    }

    return registry, review_queue, annotations


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build review-facing Atlas memory disposition overlays."
    )
    parser.add_argument(
        "--atlas-memory-disposition-packet",
        type=Path,
        default=Path("bridge/atlas_memory_disposition_packet.json"),
    )
    parser.add_argument(
        "--out-disposition-registry",
        type=Path,
        default=Path("registry/atlas_memory_disposition_registry.json"),
    )
    parser.add_argument(
        "--out-review-queue",
        type=Path,
        default=Path("registry/atlas_memory_review_queue.json"),
    )
    parser.add_argument(
        "--out-annotations",
        type=Path,
        default=Path("registry/atlas_memory_disposition_annotations.json"),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    packet = _read_json(args.atlas_memory_disposition_packet)
    registry, review_queue, annotations = build_overlay_outputs(packet)
    _write_json(args.out_disposition_registry, registry)
    _write_json(args.out_review_queue, review_queue)
    _write_json(args.out_annotations, annotations)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
