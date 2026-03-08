#!/usr/bin/env python3
"""Build pattern cluster, maturity, and conflict overlays.

Publisher surfaces only Sophia-audited pattern materials as bounded,
review-facing overlays. This layer does not mutate canonical identities,
graph edges, precedents, closures, or truth artifacts.
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


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    return action if action in {"docket", "watch", "suppressed", "rejected"} else "watch"


def _targets(rec: dict[str, Any]) -> list[str]:
    return sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])


def _validate_outputs(pattern_dashboard: dict[str, Any], pattern_registry: dict[str, Any], pattern_watchlist: dict[str, Any], pattern_annotations: dict[str, Any]) -> None:
    if not isinstance(pattern_dashboard.get("entries"), list):
        raise ValueError("pattern_dashboard.entries must be a list")
    if not isinstance(pattern_registry.get("entries"), list):
        raise ValueError("pattern_registry.entries must be a list")
    if not isinstance(pattern_watchlist.get("entries"), list):
        raise ValueError("pattern_watchlist.entries must be a list")
    if not isinstance(pattern_annotations.get("annotations"), list):
        raise ValueError("pattern_annotations.annotations must be a list")


def build_pattern_overlays(
    pattern_audit: dict[str, Any],
    pattern_recommendations: dict[str, Any],
    pattern_cluster_map: dict[str, Any],
    pattern_maturity_map: dict[str, Any],
    cross_case_relationship_map: dict[str, Any],
    pattern_conflict_report: dict[str, Any],
    investigation_dashboard: dict[str, Any],
    authority_gate_dashboard: dict[str, Any],
    review_packet_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "pattern_audit": _extract_required_provenance("pattern_audit", pattern_audit),
        "pattern_recommendations": _extract_required_provenance("pattern_recommendations", pattern_recommendations),
        "pattern_cluster_map": _extract_required_provenance("pattern_cluster_map", pattern_cluster_map),
        "pattern_maturity_map": _extract_required_provenance("pattern_maturity_map", pattern_maturity_map),
        "cross_case_relationship_map": _extract_required_provenance("cross_case_relationship_map", cross_case_relationship_map),
        "pattern_conflict_report": _extract_required_provenance("pattern_conflict_report", pattern_conflict_report),
    }
    for name, artifact in {
        "investigation_dashboard": investigation_dashboard,
        "authority_gate_dashboard": authority_gate_dashboard,
        "review_packet_dashboard": review_packet_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(pattern_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(pattern_recommendations.get("recommendations")) if isinstance(r, dict)]
    clusters = [e for e in as_list(pattern_cluster_map.get("entries")) if isinstance(e, dict)]
    maturities = [e for e in as_list(pattern_maturity_map.get("entries")) if isinstance(e, dict)]
    relationships = [e for e in as_list(cross_case_relationship_map.get("entries")) if isinstance(e, dict)]
    conflicts = [e for e in as_list(pattern_conflict_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    cluster_by_review = _index_by_key(clusters, "reviewId")
    maturity_by_review = _index_by_key(maturities, "reviewId")
    relationship_by_review = _index_by_key(relationships, "reviewId")
    conflict_by_review = _index_by_key(conflicts, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)
        cluster = cluster_by_review.get(review_id, {})
        maturity = maturity_by_review.get(review_id, {})
        relation = relationship_by_review.get(review_id, {})
        conflict = conflict_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        pattern_cluster = str(cluster.get("patternCluster", rec.get("patternCluster", "unclustered")))
        pattern_maturity = str(maturity.get("patternMaturity", rec.get("patternMaturity", "speculative")))
        cross_case_hints = sorted([x for x in as_list(relation.get("crossCaseRelationshipHints", rec.get("crossCaseRelationshipHints", []))) if isinstance(x, str)])
        conflict_markers = sorted([x for x in as_list(conflict.get("conflictMarkers", rec.get("conflictMarkers", []))) if isinstance(x, str)])
        pattern_audit_state = str(audit.get("patternAuditState", rec.get("patternAuditState", "none")))
        linked_target_ids = _targets(rec)

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "patternCluster": pattern_cluster,
                "patternMaturity": pattern_maturity,
                "crossCaseRelationshipHints": cross_case_hints,
                "conflictMarkers": conflict_markers,
                "patternAuditState": pattern_audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            dashboard_entries.append(entry)
            registry_entries.append({**entry, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "patternCluster": pattern_cluster,
                    "patternMaturity": pattern_maturity,
                    "crossCaseRelationshipHints": cross_case_hints,
                    "conflictMarkers": conflict_markers,
                    "patternAuditState": pattern_audit_state,
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
                "patternCluster": pattern_cluster,
                "patternMaturity": pattern_maturity,
                "crossCaseRelationshipHints": cross_case_hints,
                "conflictMarkers": conflict_markers,
                "patternAuditState": pattern_audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticAccusation": True,
                "noAutomaticGraphMutation": True,
                "noAutomaticPrecedentMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    pattern_dashboard = {
        "generatedAt": generated_at,
        "patternProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    pattern_registry = {
        "generatedAt": generated_at,
        "patternProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    pattern_watchlist = {
        "generatedAt": generated_at,
        "patternProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    pattern_annotations = {
        "generatedAt": generated_at,
        "patternProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticAccusation": True,
        "noAutomaticGraphMutation": True,
        "noAutomaticPrecedentMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(pattern_dashboard, pattern_registry, pattern_watchlist, pattern_annotations)
    return pattern_dashboard, pattern_registry, pattern_watchlist, pattern_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern-audit", type=Path, default=Path("bridge/pattern_audit.json"))
    parser.add_argument("--pattern-recommendations", type=Path, default=Path("bridge/pattern_recommendations.json"))
    parser.add_argument("--pattern-cluster-map", type=Path, default=Path("bridge/pattern_cluster_map.json"))
    parser.add_argument("--pattern-maturity-map", type=Path, default=Path("bridge/pattern_maturity_map.json"))
    parser.add_argument("--cross-case-relationship-map", type=Path, default=Path("bridge/cross_case_relationship_map.json"))
    parser.add_argument("--pattern-conflict-report", type=Path, default=Path("bridge/pattern_conflict_report.json"))
    parser.add_argument("--pattern-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--investigation-dashboard", type=Path, default=Path("registry/investigation_dashboard.json"))
    parser.add_argument("--authority-gate-dashboard", type=Path, default=Path("registry/authority_gate_dashboard.json"))
    parser.add_argument("--review-packet-dashboard", type=Path, default=Path("registry/review_packet_dashboard.json"))

    parser.add_argument("--out-pattern-dashboard", type=Path, default=Path("registry/pattern_dashboard.json"))
    parser.add_argument("--out-pattern-registry", type=Path, default=Path("registry/pattern_registry.json"))
    parser.add_argument("--out-pattern-watchlist", type=Path, default=Path("registry/pattern_watchlist.json"))
    parser.add_argument("--out-pattern-annotations", type=Path, default=Path("registry/pattern_annotations.json"))

    args = parser.parse_args()

    if args.pattern_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --pattern-snapshot is no longer supported. Use canonical pattern artifacts.")
        return 2

    try:
        outputs = build_pattern_overlays(
            load_required_json(args.pattern_audit),
            load_required_json(args.pattern_recommendations),
            load_required_json(args.pattern_cluster_map),
            load_required_json(args.pattern_maturity_map),
            load_required_json(args.cross_case_relationship_map),
            load_required_json(args.pattern_conflict_report),
            load_required_json(args.investigation_dashboard),
            load_required_json(args.authority_gate_dashboard),
            load_required_json(args.review_packet_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_pattern_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_pattern_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_pattern_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_pattern_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_pattern_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote pattern dashboard: {args.out_pattern_dashboard}")
    print(f"[OK] Wrote pattern registry: {args.out_pattern_registry}")
    print(f"[OK] Wrote pattern watchlist: {args.out_pattern_watchlist}")
    print(f"[OK] Wrote pattern annotations: {args.out_pattern_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
