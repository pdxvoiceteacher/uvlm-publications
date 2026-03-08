#!/usr/bin/env python3
"""Build responsibility, support, and intervention-boundary overlays.

Publisher surfaces only Sophia-audited responsibility/support materials; no
automatic sanctioning, coercion, or moral classification occurs from this layer.
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

    schema_version = prov.get("schemaVersion")
    if not isinstance(schema_version, str) or not schema_version.strip():
        raise ValueError(f"{name} provenance.schemaVersion must be a non-empty string")
    producer_commits = prov.get("producerCommits")
    if not isinstance(producer_commits, list) or not producer_commits or not all(isinstance(v, str) and v.strip() for v in producer_commits):
        raise ValueError(f"{name} provenance.producerCommits must be a non-empty list of non-empty strings")
    source_mode = prov.get("sourceMode")
    if not isinstance(source_mode, str) or not source_mode.strip():
        raise ValueError(f"{name} provenance.sourceMode must be a non-empty string")
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
    return {
        "schemaVersions": schema_versions,
        "producerCommits": producer_commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": any(mode.lower() == "fixture" for mode in source_modes.values()),
    }


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    return action if action in {"docket", "watch", "suppressed", "rejected"} else "watch"


def _targets(rec: dict[str, Any]) -> list[str]:
    return sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])


def _validate_outputs(responsibility_dashboard: dict[str, Any], support_registry: dict[str, Any], intervention_watchlist: dict[str, Any], responsibility_annotations: dict[str, Any]) -> None:
    if not isinstance(responsibility_dashboard.get("entries"), list):
        raise ValueError("responsibility_dashboard.entries must be a list")
    if not isinstance(support_registry.get("entries"), list):
        raise ValueError("support_registry.entries must be a list")
    if not isinstance(intervention_watchlist.get("entries"), list):
        raise ValueError("intervention_watchlist.entries must be a list")
    if not isinstance(responsibility_annotations.get("annotations"), list):
        raise ValueError("responsibility_annotations.annotations must be a list")
    for payload in (responsibility_dashboard, support_registry, intervention_watchlist, responsibility_annotations):
        json.dumps(payload)


def build_responsibility_overlays(
    responsibility_audit: dict[str, Any],
    responsibility_recommendations: dict[str, Any],
    responsibility_mode_map: dict[str, Any],
    support_pathway_map: dict[str, Any],
    intervention_boundary_report: dict[str, Any],
    sanction_suppression_gate: dict[str, Any],
    agency_mode_dashboard: dict[str, Any],
    theory_dashboard: dict[str, Any],
    experiment_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "responsibility_audit": _extract_required_provenance("responsibility_audit", responsibility_audit),
        "responsibility_recommendations": _extract_required_provenance("responsibility_recommendations", responsibility_recommendations),
        "responsibility_mode_map": _extract_required_provenance("responsibility_mode_map", responsibility_mode_map),
        "support_pathway_map": _extract_required_provenance("support_pathway_map", support_pathway_map),
        "intervention_boundary_report": _extract_required_provenance("intervention_boundary_report", intervention_boundary_report),
        "sanction_suppression_gate": _extract_required_provenance("sanction_suppression_gate", sanction_suppression_gate),
    }
    for name, artifact in {
        "agency_mode_dashboard": agency_mode_dashboard,
        "theory_dashboard": theory_dashboard,
        "experiment_dashboard": experiment_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(responsibility_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(responsibility_recommendations.get("recommendations")) if isinstance(e, dict)]
    modes = [e for e in as_list(responsibility_mode_map.get("entries")) if isinstance(e, dict)]
    supports = [e for e in as_list(support_pathway_map.get("entries")) if isinstance(e, dict)]
    boundaries = [e for e in as_list(intervention_boundary_report.get("entries")) if isinstance(e, dict)]
    sanctions = [e for e in as_list(sanction_suppression_gate.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    mode_by_review = _index_by_key(modes, "reviewId")
    support_by_review = _index_by_key(supports, "reviewId")
    boundary_by_review = _index_by_key(boundaries, "reviewId")
    sanction_by_review = _index_by_key(sanctions, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        mode = mode_by_review.get(review_id, {})
        support = support_by_review.get(review_id, {})
        boundary = boundary_by_review.get(review_id, {})
        sanction = sanction_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        responsibility_status = str(mode.get("responsibilityStatus", rec.get("responsibilityStatus", "under-review")))
        support_pathway = str(support.get("supportPathway", rec.get("supportPathway", "monitor")))
        consent_requirement = str(boundary.get("consentRequirement", rec.get("consentRequirement", "required")))
        coercion_ceiling = str(boundary.get("coercionCeiling", rec.get("coercionCeiling", "strict")))
        sanction_suppression_state = str(sanction.get("sanctionSuppressionState", rec.get("sanctionSuppressionState", "enabled")))
        intervention_boundary_state = str(boundary.get("interventionBoundaryState", rec.get("interventionBoundaryState", "bounded")))
        responsibility_audit_state = str(audit.get("responsibilityAuditState", rec.get("responsibilityAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "responsibilityStatus": responsibility_status,
            "supportPathway": support_pathway,
            "consentRequirement": consent_requirement,
            "coercionCeiling": coercion_ceiling,
            "sanctionSuppressionState": sanction_suppression_state,
            "interventionBoundaryState": intervention_boundary_state,
            "responsibilityAuditState": responsibility_audit_state,
            "linkedTargetIds": linked_target_ids,
        }

        if action == "docket":
            dashboard_entries.append({**base, "humanReviewFlag": bool(rec.get("humanReviewFlag", True)), "queuedAt": generated_at})
            registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({
                **base,
                "status": "watch",
                "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                "observational": True,
                "nonCanonical": True,
                "queuedAt": generated_at,
            })

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "noAutomaticSanctioning": True,
            "noAutomaticCoercion": True,
            "noAutomaticMoralClassification": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    responsibility_dashboard = {
        "generatedAt": generated_at,
        "responsibilityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    support_registry = {
        "generatedAt": generated_at,
        "responsibilityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    intervention_watchlist = {
        "generatedAt": generated_at,
        "responsibilityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    responsibility_annotations = {
        "generatedAt": generated_at,
        "responsibilityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticSanctioning": True,
        "noAutomaticCoercion": True,
        "noAutomaticMoralClassification": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(responsibility_dashboard, support_registry, intervention_watchlist, responsibility_annotations)
    return responsibility_dashboard, support_registry, intervention_watchlist, responsibility_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--responsibility-audit", type=Path, default=Path("bridge/responsibility_audit.json"))
    parser.add_argument("--responsibility-recommendations", type=Path, default=Path("bridge/responsibility_recommendations.json"))
    parser.add_argument("--responsibility-mode-map", type=Path, default=Path("bridge/responsibility_mode_map.json"))
    parser.add_argument("--support-pathway-map", type=Path, default=Path("bridge/support_pathway_map.json"))
    parser.add_argument("--intervention-boundary-report", type=Path, default=Path("bridge/intervention_boundary_report.json"))
    parser.add_argument("--sanction-suppression-gate", type=Path, default=Path("bridge/sanction_suppression_gate.json"))

    parser.add_argument("--agency-mode-dashboard", type=Path, default=Path("registry/agency_mode_dashboard.json"))
    parser.add_argument("--theory-dashboard", type=Path, default=Path("registry/theory_dashboard.json"))
    parser.add_argument("--experiment-dashboard", type=Path, default=Path("registry/experiment_dashboard.json"))

    parser.add_argument("--out-responsibility-dashboard", type=Path, default=Path("registry/responsibility_dashboard.json"))
    parser.add_argument("--out-support-registry", type=Path, default=Path("registry/support_registry.json"))
    parser.add_argument("--out-intervention-watchlist", type=Path, default=Path("registry/intervention_watchlist.json"))
    parser.add_argument("--out-responsibility-annotations", type=Path, default=Path("registry/responsibility_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_responsibility_overlays(
            load_required_json(args.responsibility_audit),
            load_required_json(args.responsibility_recommendations),
            load_required_json(args.responsibility_mode_map),
            load_required_json(args.support_pathway_map),
            load_required_json(args.intervention_boundary_report),
            load_required_json(args.sanction_suppression_gate),
            load_required_json(args.agency_mode_dashboard),
            load_required_json(args.theory_dashboard),
            load_required_json(args.experiment_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_responsibility_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_support_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_intervention_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_responsibility_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_responsibility_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_support_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_intervention_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_responsibility_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote responsibility dashboard: {args.out_responsibility_dashboard}")
    print(f"[OK] Wrote support registry: {args.out_support_registry}")
    print(f"[OK] Wrote intervention watchlist: {args.out_intervention_watchlist}")
    print(f"[OK] Wrote responsibility annotations: {args.out_responsibility_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
