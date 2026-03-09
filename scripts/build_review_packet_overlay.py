#!/usr/bin/env python3
"""Build human review packet and uncertainty synthesis overlays.

Publisher surfaces only Sophia-audited review packets and uncertainty disclosures
as bounded, review-facing artifacts. This layer does not auto-accuse, auto-
publish, or mutate canonical truth artifacts.
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


def _normalized_action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    if action not in {"docket", "watch", "suppressed", "rejected"}:
        return "watch"
    return action


def _normalized_targets(rec: dict[str, Any]) -> list[str]:
    return sorted([target for target in as_list(rec.get("linkedTargetIds")) if isinstance(target, str)])


def _validate_output_contracts(
    review_packet_dashboard: dict[str, Any],
    review_packet_registry: dict[str, Any],
    uncertainty_watchlist: dict[str, Any],
    review_packet_annotations: dict[str, Any],
) -> None:
    if not isinstance(review_packet_dashboard.get("entries"), list):
        raise ValueError("review_packet_dashboard.entries must be a list")
    if not isinstance(review_packet_registry.get("entries"), list):
        raise ValueError("review_packet_registry.entries must be a list")
    if not isinstance(uncertainty_watchlist.get("entries"), list):
        raise ValueError("uncertainty_watchlist.entries must be a list")
    if not isinstance(review_packet_annotations.get("annotations"), list):
        raise ValueError("review_packet_annotations.annotations must be a list")


def build_review_packet_overlays(
    review_packet_audit: dict[str, Any],
    review_packet_recommendations: dict[str, Any],
    review_packet_map: dict[str, Any],
    review_packet_summary: dict[str, Any],
    narrative_synthesis_map: dict[str, Any],
    uncertainty_disclosure_report: dict[str, Any],
    investigation_dashboard: dict[str, Any],
    public_record_dashboard: dict[str, Any],
    authority_gate_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "review_packet_audit": _extract_required_provenance("review_packet_audit", review_packet_audit),
        "review_packet_recommendations": _extract_required_provenance("review_packet_recommendations", review_packet_recommendations),
        "review_packet_map": _extract_required_provenance("review_packet_map", review_packet_map),
        "review_packet_summary": _extract_required_provenance("review_packet_summary", review_packet_summary),
        "narrative_synthesis_map": _extract_required_provenance("narrative_synthesis_map", narrative_synthesis_map),
        "uncertainty_disclosure_report": _extract_required_provenance("uncertainty_disclosure_report", uncertainty_disclosure_report),
    }
    for optional_name, artifact in {
        "investigation_dashboard": investigation_dashboard,
        "public_record_dashboard": public_record_dashboard,
        "authority_gate_dashboard": authority_gate_dashboard,
    }.items():
        optional = _extract_optional_provenance(optional_name, artifact)
        if optional:
            provenances[optional_name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(review_packet_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(review_packet_recommendations.get("recommendations")) if isinstance(r, dict)]
    packet_map_entries = [e for e in as_list(review_packet_map.get("entries")) if isinstance(e, dict)]
    packet_summary_entries = [e for e in as_list(review_packet_summary.get("entries")) if isinstance(e, dict)]
    narrative_entries = [e for e in as_list(narrative_synthesis_map.get("entries")) if isinstance(e, dict)]
    uncertainty_entries = [e for e in as_list(uncertainty_disclosure_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    packet_map_by_review = _index_by_key(packet_map_entries, "reviewId")
    packet_summary_by_review = _index_by_key(packet_summary_entries, "reviewId")
    narrative_by_review = _index_by_key(narrative_entries, "reviewId")
    uncertainty_by_review = _index_by_key(uncertainty_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _normalized_action(rec)
        packet_map_entry = packet_map_by_review.get(review_id, {})
        summary_entry = packet_summary_by_review.get(review_id, {})
        narrative_entry = narrative_by_review.get(review_id, {})
        uncertainty_entry = uncertainty_by_review.get(review_id, {})
        audit_entry = audit_by_review.get(review_id, {})

        packet_status = str(packet_map_entry.get("packetStatus", rec.get("packetStatus", "pending-review")))
        maturity_ceiling = str(summary_entry.get("maturityCeiling", rec.get("maturityCeiling", "bounded-review")))
        ambiguity_level = str(summary_entry.get("ambiguityLevel", rec.get("ambiguityLevel", "medium")))
        uncertainty_disclosures = sorted([x for x in as_list(uncertainty_entry.get("uncertaintyDisclosures", rec.get("uncertaintyDisclosures", []))) if isinstance(x, str)])
        excluded_conclusions = sorted([x for x in as_list(narrative_entry.get("excludedConclusions", rec.get("excludedConclusions", []))) if isinstance(x, str)])
        synthesis_status = str(narrative_entry.get("synthesisStatus", rec.get("synthesisStatus", "bounded")))
        packet_audit_state = str(audit_entry.get("reviewPacketAuditState", rec.get("reviewPacketAuditState", "none")))
        linked_target_ids = _normalized_targets(rec)

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "packetStatus": packet_status,
                "maturityCeiling": maturity_ceiling,
                "ambiguityLevel": ambiguity_level,
                "uncertaintyDisclosures": uncertainty_disclosures,
                "excludedConclusions": excluded_conclusions,
                "synthesisStatus": synthesis_status,
                "reviewPacketAuditState": packet_audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            dashboard_entries.append(entry)
            registry_entries.append(
                {
                    "reviewId": review_id,
                    "packetStatus": packet_status,
                    "maturityCeiling": maturity_ceiling,
                    "ambiguityLevel": ambiguity_level,
                    "uncertaintyDisclosures": uncertainty_disclosures,
                    "excludedConclusions": excluded_conclusions,
                    "synthesisStatus": synthesis_status,
                    "reviewPacketAuditState": packet_audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "updatedAt": generated_at,
                }
            )

        if action == "watch":
            watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "packetStatus": packet_status,
                    "maturityCeiling": maturity_ceiling,
                    "ambiguityLevel": ambiguity_level,
                    "uncertaintyDisclosures": uncertainty_disclosures,
                    "excludedConclusions": excluded_conclusions,
                    "synthesisStatus": synthesis_status,
                    "reviewPacketAuditState": packet_audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        annotation_entries.append(
            {
                "reviewId": review_id,
                "targetPublisherAction": action,
                "packetStatus": packet_status,
                "maturityCeiling": maturity_ceiling,
                "ambiguityLevel": ambiguity_level,
                "uncertaintyDisclosures": uncertainty_disclosures,
                "excludedConclusions": excluded_conclusions,
                "synthesisStatus": synthesis_status,
                "reviewPacketAuditState": packet_audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticAccusation": True,
                "noAutomaticPublication": True,
                "noAutomaticIdentityMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    review_packet_dashboard = {
        "generatedAt": generated_at,
        "reviewPacketProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    review_packet_registry = {
        "generatedAt": generated_at,
        "reviewPacketProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    uncertainty_watchlist = {
        "generatedAt": generated_at,
        "reviewPacketProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    review_packet_annotations = {
        "generatedAt": generated_at,
        "reviewPacketProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticAccusation": True,
        "noAutomaticPublication": True,
        "noAutomaticIdentityMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_output_contracts(
        review_packet_dashboard,
        review_packet_registry,
        uncertainty_watchlist,
        review_packet_annotations,
    )

    return review_packet_dashboard, review_packet_registry, uncertainty_watchlist, review_packet_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-packet-audit", type=Path, default=Path("bridge/review_packet_audit.json"))
    parser.add_argument("--review-packet-recommendations", type=Path, default=Path("bridge/review_packet_recommendations.json"))
    parser.add_argument("--review-packet-map", type=Path, default=Path("bridge/review_packet_map.json"))
    parser.add_argument("--review-packet-summary", type=Path, default=Path("bridge/review_packet_summary.json"))
    parser.add_argument("--narrative-synthesis-map", type=Path, default=Path("bridge/narrative_synthesis_map.json"))
    parser.add_argument("--uncertainty-disclosure-report", type=Path, default=Path("bridge/uncertainty_disclosure_report.json"))
    parser.add_argument("--review-packet-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--investigation-dashboard", type=Path, default=Path("registry/investigation_dashboard.json"))
    parser.add_argument("--public-record-dashboard", type=Path, default=Path("registry/public_record_dashboard.json"))
    parser.add_argument("--authority-gate-dashboard", type=Path, default=Path("registry/authority_gate_dashboard.json"))

    parser.add_argument("--out-review-packet-dashboard", type=Path, default=Path("registry/review_packet_dashboard.json"))
    parser.add_argument("--out-review-packet-registry", type=Path, default=Path("registry/review_packet_registry.json"))
    parser.add_argument("--out-uncertainty-watchlist", type=Path, default=Path("registry/uncertainty_watchlist.json"))
    parser.add_argument("--out-review-packet-annotations", type=Path, default=Path("registry/review_packet_annotations.json"))

    args = parser.parse_args()

    if args.review_packet_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --review-packet-snapshot is no longer supported. Use canonical review-packet artifacts.")
        return 2

    try:
        outputs = build_review_packet_overlays(
            load_required_json(args.review_packet_audit),
            load_required_json(args.review_packet_recommendations),
            load_required_json(args.review_packet_map),
            load_required_json(args.review_packet_summary),
            load_required_json(args.narrative_synthesis_map),
            load_required_json(args.uncertainty_disclosure_report),
            load_required_json(args.investigation_dashboard),
            load_required_json(args.public_record_dashboard),
            load_required_json(args.authority_gate_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_review_packet_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_review_packet_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_uncertainty_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_review_packet_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_review_packet_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_review_packet_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_uncertainty_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_review_packet_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote review packet dashboard: {args.out_review_packet_dashboard}")
    print(f"[OK] Wrote review packet registry: {args.out_review_packet_registry}")
    print(f"[OK] Wrote uncertainty watchlist: {args.out_uncertainty_watchlist}")
    print(f"[OK] Wrote review packet annotations: {args.out_review_packet_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
