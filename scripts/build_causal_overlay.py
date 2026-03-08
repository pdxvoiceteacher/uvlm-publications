#!/usr/bin/env python3
"""Build causal hypothesis and mechanism-separation overlays."""

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


def _validate_outputs(causal_dashboard: dict[str, Any], mechanism_registry: dict[str, Any], causal_watchlist: dict[str, Any], causal_annotations: dict[str, Any]) -> None:
    if not isinstance(causal_dashboard.get("entries"), list):
        raise ValueError("causal_dashboard.entries must be a list")
    if not isinstance(mechanism_registry.get("entries"), list):
        raise ValueError("mechanism_registry.entries must be a list")
    if not isinstance(causal_watchlist.get("entries"), list):
        raise ValueError("causal_watchlist.entries must be a list")
    if not isinstance(causal_annotations.get("annotations"), list):
        raise ValueError("causal_annotations.annotations must be a list")


def build_causal_overlays(
    causal_audit: dict[str, Any],
    causal_recommendations: dict[str, Any],
    causal_bundle_map: dict[str, Any],
    mechanism_candidate_map: dict[str, Any],
    mechanism_separation_report: dict[str, Any],
    causal_conflict_report: dict[str, Any],
    pattern_timeline_dashboard: dict[str, Any],
    environment_integrity_dashboard: dict[str, Any],
    authority_gate_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "causal_audit": _extract_required_provenance("causal_audit", causal_audit),
        "causal_recommendations": _extract_required_provenance("causal_recommendations", causal_recommendations),
        "causal_bundle_map": _extract_required_provenance("causal_bundle_map", causal_bundle_map),
        "mechanism_candidate_map": _extract_required_provenance("mechanism_candidate_map", mechanism_candidate_map),
        "mechanism_separation_report": _extract_required_provenance("mechanism_separation_report", mechanism_separation_report),
        "causal_conflict_report": _extract_required_provenance("causal_conflict_report", causal_conflict_report),
    }
    for name, artifact in {
        "pattern_timeline_dashboard": pattern_timeline_dashboard,
        "environment_integrity_dashboard": environment_integrity_dashboard,
        "authority_gate_dashboard": authority_gate_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(causal_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(causal_recommendations.get("recommendations")) if isinstance(r, dict)]
    bundles = [e for e in as_list(causal_bundle_map.get("entries")) if isinstance(e, dict)]
    mechanisms = [e for e in as_list(mechanism_candidate_map.get("entries")) if isinstance(e, dict)]
    separations = [e for e in as_list(mechanism_separation_report.get("entries")) if isinstance(e, dict)]
    conflicts = [e for e in as_list(causal_conflict_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    bundle_by_review = _index_by_key(bundles, "reviewId")
    mechanism_by_review = _index_by_key(mechanisms, "reviewId")
    separation_by_review = _index_by_key(separations, "reviewId")
    conflict_by_review = _index_by_key(conflicts, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    mechanism_registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        bundle = bundle_by_review.get(review_id, {})
        mechanism = mechanism_by_review.get(review_id, {})
        separation = separation_by_review.get(review_id, {})
        conflict = conflict_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        causal_bundle_type = str(bundle.get("causalBundleType", rec.get("causalBundleType", "unknown-bundle")))
        mechanism_candidates = sorted([x for x in as_list(mechanism.get("mechanismCandidates", rec.get("mechanismCandidates", []))) if isinstance(x, str)])
        explanatory_gap = str(separation.get("explanatoryGap", rec.get("explanatoryGap", "high")))
        prohibited_conclusions = sorted([x for x in as_list(separation.get("prohibitedConclusions", rec.get("prohibitedConclusions", []))) if isinstance(x, str)])
        causal_conflict_state = str(conflict.get("causalConflictState", rec.get("causalConflictState", "none")))
        causal_audit_state = str(audit.get("causalAuditState", rec.get("causalAuditState", "none")))
        linked_target_ids = _targets(rec)

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "causalBundleType": causal_bundle_type,
                "mechanismCandidates": mechanism_candidates,
                "explanatoryGap": explanatory_gap,
                "prohibitedConclusions": prohibited_conclusions,
                "causalConflictState": causal_conflict_state,
                "causalAuditState": causal_audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            dashboard_entries.append(entry)
            mechanism_registry_entries.append({**entry, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "causalBundleType": causal_bundle_type,
                    "mechanismCandidates": mechanism_candidates,
                    "explanatoryGap": explanatory_gap,
                    "prohibitedConclusions": prohibited_conclusions,
                    "causalConflictState": causal_conflict_state,
                    "causalAuditState": causal_audit_state,
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
                "causalBundleType": causal_bundle_type,
                "mechanismCandidates": mechanism_candidates,
                "explanatoryGap": explanatory_gap,
                "prohibitedConclusions": prohibited_conclusions,
                "causalConflictState": causal_conflict_state,
                "causalAuditState": causal_audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticAccusation": True,
                "noAutomaticAttribution": True,
                "noAutomaticGraphMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    causal_dashboard = {
        "generatedAt": generated_at,
        "causalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    mechanism_registry = {
        "generatedAt": generated_at,
        "causalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(mechanism_registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    causal_watchlist = {
        "generatedAt": generated_at,
        "causalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    causal_annotations = {
        "generatedAt": generated_at,
        "causalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticAccusation": True,
        "noAutomaticAttribution": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(causal_dashboard, mechanism_registry, causal_watchlist, causal_annotations)
    return causal_dashboard, mechanism_registry, causal_watchlist, causal_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--causal-audit", type=Path, default=Path("bridge/causal_audit.json"))
    parser.add_argument("--causal-recommendations", type=Path, default=Path("bridge/causal_recommendations.json"))
    parser.add_argument("--causal-bundle-map", type=Path, default=Path("bridge/causal_bundle_map.json"))
    parser.add_argument("--mechanism-candidate-map", type=Path, default=Path("bridge/mechanism_candidate_map.json"))
    parser.add_argument("--mechanism-separation-report", type=Path, default=Path("bridge/mechanism_separation_report.json"))
    parser.add_argument("--causal-conflict-report", type=Path, default=Path("bridge/causal_conflict_report.json"))
    parser.add_argument("--causal-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--pattern-timeline-dashboard", type=Path, default=Path("registry/pattern_timeline_dashboard.json"))
    parser.add_argument("--environment-integrity-dashboard", type=Path, default=Path("registry/environment_integrity_dashboard.json"))
    parser.add_argument("--authority-gate-dashboard", type=Path, default=Path("registry/authority_gate_dashboard.json"))

    parser.add_argument("--out-causal-dashboard", type=Path, default=Path("registry/causal_dashboard.json"))
    parser.add_argument("--out-mechanism-registry", type=Path, default=Path("registry/mechanism_registry.json"))
    parser.add_argument("--out-causal-watchlist", type=Path, default=Path("registry/causal_watchlist.json"))
    parser.add_argument("--out-causal-annotations", type=Path, default=Path("registry/causal_annotations.json"))

    args = parser.parse_args()

    if args.causal_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --causal-snapshot is no longer supported. Use canonical causal artifacts.")
        return 2

    try:
        outputs = build_causal_overlays(
            load_required_json(args.causal_audit),
            load_required_json(args.causal_recommendations),
            load_required_json(args.causal_bundle_map),
            load_required_json(args.mechanism_candidate_map),
            load_required_json(args.mechanism_separation_report),
            load_required_json(args.causal_conflict_report),
            load_required_json(args.pattern_timeline_dashboard),
            load_required_json(args.environment_integrity_dashboard),
            load_required_json(args.authority_gate_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_causal_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_mechanism_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_causal_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_causal_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_causal_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_mechanism_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_causal_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_causal_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote causal dashboard: {args.out_causal_dashboard}")
    print(f"[OK] Wrote mechanism registry: {args.out_mechanism_registry}")
    print(f"[OK] Wrote causal watchlist: {args.out_causal_watchlist}")
    print(f"[OK] Wrote causal annotations: {args.out_causal_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
