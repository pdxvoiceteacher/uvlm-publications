#!/usr/bin/env python3
"""Build meta-cognition overlays.

Publisher surfaces only Sophia-audited meta-cognition materials.
The system may evaluate architecture but cannot autonomously modify core safety
constraints without human approval.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

REQUIRED_PROVENANCE_KEYS = ("schemaVersion", "producerCommits", "sourceMode")
IMMUTABLE_CONSTRAINTS = [
    "evidence maturity gating",
    "provenance requirements",
    "sanction suppression rules",
    "agency humility protocol",
    "non-coercion forecasting rule",
    "human authority over value judgments",
]


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
    if not isinstance(prov.get("schemaVersion"), str) or not str(prov.get("schemaVersion")).strip():
        raise ValueError(f"{name} provenance.schemaVersion must be a non-empty string")
    commits = prov.get("producerCommits")
    if not isinstance(commits, list) or not commits or not all(isinstance(v, str) and v.strip() for v in commits):
        raise ValueError(f"{name} provenance.producerCommits must be a non-empty list of non-empty strings")
    if not isinstance(prov.get("sourceMode"), str) or not str(prov.get("sourceMode")).strip():
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


def _to_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError:
            return default
    return default


def _validate_outputs(meta_dashboard: dict[str, Any], reasoning_performance_registry: dict[str, Any], meta_watchlist: dict[str, Any], meta_annotations: dict[str, Any]) -> None:
    if not isinstance(meta_dashboard.get("entries"), list):
        raise ValueError("meta_dashboard.entries must be a list")
    if not isinstance(reasoning_performance_registry.get("entries"), list):
        raise ValueError("reasoning_performance_registry.entries must be a list")
    if not isinstance(meta_watchlist.get("entries"), list):
        raise ValueError("meta_watchlist.entries must be a list")
    if not isinstance(meta_annotations.get("annotations"), list):
        raise ValueError("meta_annotations.annotations must be a list")
    for payload in (meta_dashboard, reasoning_performance_registry, meta_watchlist, meta_annotations):
        json.dumps(payload)


def build_meta_cognition_overlays(
    meta_cognition_audit: dict[str, Any],
    meta_cognition_recommendations: dict[str, Any],
    reasoning_efficiency_report: dict[str, Any],
    pattern_donor_reliability_report: dict[str, Any],
    governance_constraint_performance_report: dict[str, Any],
    discovery_productivity_report: dict[str, Any],
    value_dashboard: dict[str, Any],
    responsibility_dashboard: dict[str, Any],
    system_forecast_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "meta_cognition_audit": _extract_required_provenance("meta_cognition_audit", meta_cognition_audit),
        "meta_cognition_recommendations": _extract_required_provenance("meta_cognition_recommendations", meta_cognition_recommendations),
        "reasoning_efficiency_report": _extract_required_provenance("reasoning_efficiency_report", reasoning_efficiency_report),
        "pattern_donor_reliability_report": _extract_required_provenance("pattern_donor_reliability_report", pattern_donor_reliability_report),
        "governance_constraint_performance_report": _extract_required_provenance("governance_constraint_performance_report", governance_constraint_performance_report),
        "discovery_productivity_report": _extract_required_provenance("discovery_productivity_report", discovery_productivity_report),
    }
    for name, artifact in {
        "value_dashboard": value_dashboard,
        "responsibility_dashboard": responsibility_dashboard,
        "system_forecast_dashboard": system_forecast_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(meta_cognition_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(meta_cognition_recommendations.get("recommendations")) if isinstance(e, dict)]
    reasoning_entries = [e for e in as_list(reasoning_efficiency_report.get("entries")) if isinstance(e, dict)]
    donor_entries = [e for e in as_list(pattern_donor_reliability_report.get("entries")) if isinstance(e, dict)]
    governance_entries = [e for e in as_list(governance_constraint_performance_report.get("entries")) if isinstance(e, dict)]
    discovery_entries = [e for e in as_list(discovery_productivity_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    reasoning_by_review = _index_by_key(reasoning_entries, "reviewId")
    donor_by_review = _index_by_key(donor_entries, "reviewId")
    governance_by_review = _index_by_key(governance_entries, "reviewId")
    discovery_by_review = _index_by_key(discovery_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        reasoning = reasoning_by_review.get(review_id, {})
        donor = donor_by_review.get(review_id, {})
        governance = governance_by_review.get(review_id, {})
        discovery = discovery_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        reasoning_efficiency = _to_float(reasoning.get("reasoningEfficiency", rec.get("reasoningEfficiency", 0.0)))
        pattern_donor_reliability = str(donor.get("patternDonorReliability", rec.get("patternDonorReliability", "unknown")))
        governance_constraint_performance = str(governance.get("governanceConstraintPerformance", rec.get("governanceConstraintPerformance", "bounded")))
        discovery_productivity = _to_float(discovery.get("discoveryProductivity", rec.get("discoveryProductivity", 0.0)))
        meta_audit_state = str(audit.get("metaCognitionAuditState", rec.get("metaCognitionAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "reasoningEfficiency": reasoning_efficiency,
            "patternDonorReliability": pattern_donor_reliability,
            "governanceConstraintPerformance": governance_constraint_performance,
            "discoveryProductivity": discovery_productivity,
            "metaCognitionAuditState": meta_audit_state,
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
            "noAutonomousSafetyConstraintModification": True,
            "humanApprovalRequiredForStructuralChanges": True,
            "immutableSafetyConstraints": IMMUTABLE_CONSTRAINTS,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    meta_dashboard = {
        "generatedAt": generated_at,
        "metaCognitionProtocol": True,
        "nonCanonical": True,
        "noAutonomousSafetyConstraintModification": True,
        "humanApprovalRequiredForStructuralChanges": True,
        "immutableSafetyConstraints": IMMUTABLE_CONSTRAINTS,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    reasoning_performance_registry = {
        "generatedAt": generated_at,
        "metaCognitionProtocol": True,
        "nonCanonical": True,
        "noAutonomousSafetyConstraintModification": True,
        "humanApprovalRequiredForStructuralChanges": True,
        "immutableSafetyConstraints": IMMUTABLE_CONSTRAINTS,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    meta_watchlist = {
        "generatedAt": generated_at,
        "metaCognitionProtocol": True,
        "nonCanonical": True,
        "noAutonomousSafetyConstraintModification": True,
        "humanApprovalRequiredForStructuralChanges": True,
        "immutableSafetyConstraints": IMMUTABLE_CONSTRAINTS,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    meta_annotations = {
        "generatedAt": generated_at,
        "metaCognitionProtocol": True,
        "nonCanonical": True,
        "noAutonomousSafetyConstraintModification": True,
        "humanApprovalRequiredForStructuralChanges": True,
        "immutableSafetyConstraints": IMMUTABLE_CONSTRAINTS,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(meta_dashboard, reasoning_performance_registry, meta_watchlist, meta_annotations)
    return meta_dashboard, reasoning_performance_registry, meta_watchlist, meta_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--meta-cognition-audit", type=Path, default=Path("bridge/meta_cognition_audit.json"))
    parser.add_argument("--meta-cognition-recommendations", type=Path, default=Path("bridge/meta_cognition_recommendations.json"))
    parser.add_argument("--reasoning-efficiency-report", type=Path, default=Path("bridge/reasoning_efficiency_report.json"))
    parser.add_argument("--pattern-donor-reliability-report", type=Path, default=Path("bridge/pattern_donor_reliability_report.json"))
    parser.add_argument("--governance-constraint-performance-report", type=Path, default=Path("bridge/governance_constraint_performance_report.json"))
    parser.add_argument("--discovery-productivity-report", type=Path, default=Path("bridge/discovery_productivity_report.json"))

    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))
    parser.add_argument("--responsibility-dashboard", type=Path, default=Path("registry/responsibility_dashboard.json"))
    parser.add_argument("--system-forecast-dashboard", type=Path, default=Path("registry/system_forecast_dashboard.json"))

    parser.add_argument("--out-meta-dashboard", type=Path, default=Path("registry/meta_dashboard.json"))
    parser.add_argument("--out-reasoning-performance-registry", type=Path, default=Path("registry/reasoning_performance_registry.json"))
    parser.add_argument("--out-meta-watchlist", type=Path, default=Path("registry/meta_watchlist.json"))
    parser.add_argument("--out-meta-annotations", type=Path, default=Path("registry/meta_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_meta_cognition_overlays(
            load_required_json(args.meta_cognition_audit),
            load_required_json(args.meta_cognition_recommendations),
            load_required_json(args.reasoning_efficiency_report),
            load_required_json(args.pattern_donor_reliability_report),
            load_required_json(args.governance_constraint_performance_report),
            load_required_json(args.discovery_productivity_report),
            load_required_json(args.value_dashboard),
            load_required_json(args.responsibility_dashboard),
            load_required_json(args.system_forecast_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_meta_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_reasoning_performance_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_meta_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_meta_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_meta_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_reasoning_performance_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_meta_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_meta_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote meta dashboard: {args.out_meta_dashboard}")
    print(f"[OK] Wrote reasoning performance registry: {args.out_reasoning_performance_registry}")
    print(f"[OK] Wrote meta watchlist: {args.out_meta_watchlist}")
    print(f"[OK] Wrote meta annotations: {args.out_meta_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
