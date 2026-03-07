#!/usr/bin/env python3
"""Build public-record intake, entity-graph, and custody overlays.

This script surfaces Sophia-audited public-record mapping materials as bounded,
review-facing non-canonical artifacts. It does not mutate identities, claims,
queues, or canonical truth artifacts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

REQUIRED_PROVENANCE_KEYS = ("schemaVersion", "producerCommits", "sourceMode")


def load_required_json(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"Missing required canonical artifact: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in required canonical artifact {path}: {exc}") from exc


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _index_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        k = row.get(key)
        if isinstance(k, str):
            out[k] = row
    return out


def _extract_required_provenance(name: str, artifact: dict[str, Any]) -> dict[str, Any]:
    prov = artifact.get("provenance")
    if not isinstance(prov, dict):
        raise ValueError(f"{name} missing required provenance metadata")
    for key in REQUIRED_PROVENANCE_KEYS:
        if key not in prov:
            raise ValueError(f"{name} provenance missing required field: {key}")
    if not isinstance(prov.get("schemaVersion"), str):
        raise ValueError(f"{name} provenance.schemaVersion must be a string")
    if not isinstance(prov.get("producerCommits"), list) or not all(isinstance(v, str) for v in prov.get("producerCommits", [])):
        raise ValueError(f"{name} provenance.producerCommits must be a list of strings")
    if not isinstance(prov.get("sourceMode"), str):
        raise ValueError(f"{name} provenance.sourceMode must be a string")
    return prov


def _extract_optional_provenance(name: str, artifact: dict[str, Any]) -> dict[str, Any] | None:
    prov = artifact.get("provenance")
    if not isinstance(prov, dict) or not isinstance(prov.get("schemaVersions"), dict):
        return None
    return {
        "schemaVersion": str(prov.get("schemaVersions", {}).get(name, "composite")),
        "producerCommits": [str(v) for v in as_list(prov.get("producerCommits")) if isinstance(v, str)],
        "sourceMode": "fixture" if bool(prov.get("derivedFromFixtures")) else "live",
    }


def _build_provenance_summary(provenances: dict[str, dict[str, Any]]) -> dict[str, Any]:
    producer_commits: list[str] = []
    schema_versions: dict[str, str] = {}
    source_modes: dict[str, str] = {}
    for artifact_name, prov in provenances.items():
        schema_versions[artifact_name] = str(prov.get("schemaVersion"))
        source_modes[artifact_name] = str(prov.get("sourceMode"))
        for commit in prov.get("producerCommits", []):
            if commit not in producer_commits:
                producer_commits.append(commit)
    derived_from_fixtures = any(mode.lower() == "fixture" for mode in source_modes.values())
    return {
        "schemaVersions": schema_versions,
        "producerCommits": producer_commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": derived_from_fixtures,
    }


def build_public_record_overlays(
    public_record_audit: dict[str, Any],
    public_record_recommendations: dict[str, Any],
    public_record_intake_map: dict[str, Any],
    entity_graph_map: dict[str, Any],
    relationship_edge_map: dict[str, Any],
    chain_of_custody_report: dict[str, Any],
    verification_dashboard: dict[str, Any],
    claim_type_registry: dict[str, Any],
    entity_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "public_record_audit": _extract_required_provenance("public_record_audit", public_record_audit),
        "public_record_recommendations": _extract_required_provenance("public_record_recommendations", public_record_recommendations),
        "public_record_intake_map": _extract_required_provenance("public_record_intake_map", public_record_intake_map),
        "entity_graph_map": _extract_required_provenance("entity_graph_map", entity_graph_map),
        "relationship_edge_map": _extract_required_provenance("relationship_edge_map", relationship_edge_map),
        "chain_of_custody_report": _extract_required_provenance("chain_of_custody_report", chain_of_custody_report),
    }
    for optional_name, artifact in {
        "verification_dashboard": verification_dashboard,
        "claim_type_registry": claim_type_registry,
        "entity_watchlist": entity_watchlist,
    }.items():
        optional = _extract_optional_provenance(optional_name, artifact)
        if optional:
            provenances[optional_name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(public_record_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(public_record_recommendations.get("recommendations")) if isinstance(r, dict)]
    intake_entries = [e for e in as_list(public_record_intake_map.get("entries")) if isinstance(e, dict)]
    graph_entries = [e for e in as_list(entity_graph_map.get("entries")) if isinstance(e, dict)]
    relationship_entries = [e for e in as_list(relationship_edge_map.get("entries")) if isinstance(e, dict)]
    custody_entries = [e for e in as_list(chain_of_custody_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    intake_by_review = _index_by_key(intake_entries, "reviewId")
    graph_by_review = _index_by_key(graph_entries, "reviewId")
    relationship_by_review = _index_by_key(relationship_entries, "reviewId")
    custody_by_review = _index_by_key(custody_entries, "reviewId")

    public_record_entries: list[dict[str, Any]] = []
    entity_graph_entries: list[dict[str, Any]] = []
    relationship_watch_entries: list[dict[str, Any]] = []
    custody_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        audit = audit_by_review.get(review_id, {})
        intake = intake_by_review.get(review_id, {})
        graph = graph_by_review.get(review_id, {})
        relationship = relationship_by_review.get(review_id, {})
        custody = custody_by_review.get(review_id, {})

        record_type = str(intake.get("recordType", rec.get("recordType", "unknown")))
        machine_readability_score = float(intake.get("machineReadabilityScore", rec.get("machineReadabilityScore", 0.0)))
        entity_graph_status = str(graph.get("entityGraphStatus", rec.get("entityGraphStatus", "pending")))
        relationship_ambiguity = str(relationship.get("relationshipAmbiguity", rec.get("relationshipAmbiguity", "medium")))
        custody_integrity_score = float(custody.get("custodyIntegrityScore", rec.get("custodyIntegrityScore", 0.0)))
        custody_state = str(custody.get("custodyState", rec.get("custodyState", "unverified")))
        linked_target_ids = sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])
        audit_state = str(audit.get("publicRecordAuditState", rec.get("publicRecordAuditState", "none")))

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "recordType": record_type,
                "machineReadabilityScore": machine_readability_score,
                "entityGraphStatus": entity_graph_status,
                "relationshipAmbiguity": relationship_ambiguity,
                "custodyIntegrityScore": custody_integrity_score,
                "custodyState": custody_state,
                "publicRecordAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            public_record_entries.append(entry)
            entity_graph_entries.append(entry.copy())

        if action == "watch":
            relationship_watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "recordType": record_type,
                    "machineReadabilityScore": machine_readability_score,
                    "entityGraphStatus": entity_graph_status,
                    "relationshipAmbiguity": relationship_ambiguity,
                    "custodyIntegrityScore": custody_integrity_score,
                    "custodyState": custody_state,
                    "publicRecordAuditState": audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        custody_annotations.append(
            {
                "reviewId": review_id,
                "targetPublisherAction": action,
                "recordType": record_type,
                "machineReadabilityScore": machine_readability_score,
                "entityGraphStatus": entity_graph_status,
                "relationshipAmbiguity": relationship_ambiguity,
                "custodyIntegrityScore": custody_integrity_score,
                "custodyState": custody_state,
                "publicRecordAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticAccusation": True,
                "noAutomaticGraphHardening": True,
                "noAutomaticIdentityMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    public_record_dashboard = {
        "generatedAt": generated_at,
        "publicRecordProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(public_record_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    entity_graph_registry = {
        "generatedAt": generated_at,
        "publicRecordProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(entity_graph_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    relationship_watchlist = {
        "generatedAt": generated_at,
        "publicRecordProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(relationship_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    chain_of_custody_annotations = {
        "generatedAt": generated_at,
        "publicRecordProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticAccusation": True,
        "noAutomaticGraphHardening": True,
        "noAutomaticIdentityMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(custody_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return public_record_dashboard, entity_graph_registry, relationship_watchlist, chain_of_custody_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-record-audit", type=Path, default=Path("bridge/public_record_audit.json"))
    parser.add_argument("--public-record-recommendations", type=Path, default=Path("bridge/public_record_recommendations.json"))
    parser.add_argument("--public-record-intake-map", type=Path, default=Path("bridge/public_record_intake_map.json"))
    parser.add_argument("--entity-graph-map", type=Path, default=Path("bridge/entity_graph_map.json"))
    parser.add_argument("--relationship-edge-map", type=Path, default=Path("bridge/relationship_edge_map.json"))
    parser.add_argument("--chain-of-custody-report", type=Path, default=Path("bridge/chain_of_custody_report.json"))
    parser.add_argument("--public-record-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--verification-dashboard", type=Path, default=Path("registry/verification_dashboard.json"))
    parser.add_argument("--claim-type-registry", type=Path, default=Path("registry/claim_type_registry.json"))
    parser.add_argument("--entity-watchlist", type=Path, default=Path("registry/entity_watchlist.json"))

    parser.add_argument("--out-public-record-dashboard", type=Path, default=Path("registry/public_record_dashboard.json"))
    parser.add_argument("--out-entity-graph-registry", type=Path, default=Path("registry/entity_graph_registry.json"))
    parser.add_argument("--out-relationship-watchlist", type=Path, default=Path("registry/relationship_watchlist.json"))
    parser.add_argument("--out-chain-of-custody-annotations", type=Path, default=Path("registry/chain_of_custody_annotations.json"))

    args = parser.parse_args()

    if args.public_record_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --public-record-snapshot is no longer supported. Use canonical public-record artifacts.")
        return 2

    try:
        outputs = build_public_record_overlays(
            load_required_json(args.public_record_audit),
            load_required_json(args.public_record_recommendations),
            load_required_json(args.public_record_intake_map),
            load_required_json(args.entity_graph_map),
            load_required_json(args.relationship_edge_map),
            load_required_json(args.chain_of_custody_report),
            load_required_json(args.verification_dashboard),
            load_required_json(args.claim_type_registry),
            load_required_json(args.entity_watchlist),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_public_record_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_entity_graph_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_relationship_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_chain_of_custody_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote public-record dashboard: {args.out_public_record_dashboard}")
    print(f"[OK] Wrote entity-graph registry: {args.out_entity_graph_registry}")
    print(f"[OK] Wrote relationship watchlist: {args.out_relationship_watchlist}")
    print(f"[OK] Wrote chain-of-custody annotations: {args.out_chain_of_custody_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
