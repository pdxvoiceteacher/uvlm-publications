#!/usr/bin/env python3
"""Build discovery navigation and corridor overlays.

Publisher surfaces only Sophia-audited discovery-navigation materials; it does
not authorize autonomous pursuit, deployment, canonization, or institutional control.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from canonical_integrity_manifest import evaluate_manifest_pair, load_manifest

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
        key_value = row.get(key)
        if isinstance(key_value, str):
            out[key_value] = row
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
    commits = prov.get("producerCommits")
    if not isinstance(commits, list) or not commits or not all(isinstance(v, str) and v.strip() for v in commits):
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
    return sorted([target for target in as_list(rec.get("linkedTargetIds")) if isinstance(target, str)])


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


def _validate_outputs(
    discovery_navigation_dashboard: dict[str, Any],
    discovery_corridor_registry: dict[str, Any],
    discovery_risk_watchlist: dict[str, Any],
    discovery_annotations: dict[str, Any],
) -> None:
    if not isinstance(discovery_navigation_dashboard.get("entries"), list):
        raise ValueError("discovery_navigation_dashboard.entries must be a list")
    if not isinstance(discovery_corridor_registry.get("entries"), list):
        raise ValueError("discovery_corridor_registry.entries must be a list")
    if not isinstance(discovery_risk_watchlist.get("entries"), list):
        raise ValueError("discovery_risk_watchlist.entries must be a list")
    if not isinstance(discovery_annotations.get("annotations"), list):
        raise ValueError("discovery_annotations.annotations must be a list")

    for payload in (
        discovery_navigation_dashboard,
        discovery_corridor_registry,
        discovery_risk_watchlist,
        discovery_annotations,
    ):
        for key in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(key), bool):
                raise ValueError(f"{key} must be a boolean")
        json.dumps(payload)


def build_discovery_navigation_overlays(
    discovery_navigation_audit: dict[str, Any],
    discovery_navigation_recommendations: dict[str, Any],
    discovery_vector_field: dict[str, Any],
    cross_domain_bridge_map: dict[str, Any],
    entropy_reduction_corridor: dict[str, Any],
    discovery_navigation_report: dict[str, Any],
    knowledge_topology_dashboard: dict[str, Any],
    operational_maturity_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "discovery_navigation_audit": _extract_required_provenance("discovery_navigation_audit", discovery_navigation_audit),
        "discovery_navigation_recommendations": _extract_required_provenance("discovery_navigation_recommendations", discovery_navigation_recommendations),
        "discovery_vector_field": _extract_required_provenance("discovery_vector_field", discovery_vector_field),
        "cross_domain_bridge_map": _extract_required_provenance("cross_domain_bridge_map", cross_domain_bridge_map),
        "entropy_reduction_corridor": _extract_required_provenance("entropy_reduction_corridor", entropy_reduction_corridor),
        "discovery_navigation_report": _extract_required_provenance("discovery_navigation_report", discovery_navigation_report),
    }

    for name, artifact in {
        "knowledge_topology_dashboard": knowledge_topology_dashboard,
        "operational_maturity_dashboard": operational_maturity_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "value_dashboard": value_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    provenance_summary = _build_provenance_summary(provenances)
    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [entry for entry in as_list(discovery_navigation_audit.get("audits")) if isinstance(entry, dict)]
    recommendations = [entry for entry in as_list(discovery_navigation_recommendations.get("recommendations")) if isinstance(entry, dict)]
    vector_entries = [entry for entry in as_list(discovery_vector_field.get("entries")) if isinstance(entry, dict)]
    bridge_entries = [entry for entry in as_list(cross_domain_bridge_map.get("entries")) if isinstance(entry, dict)]
    corridor_entries = [entry for entry in as_list(entropy_reduction_corridor.get("entries")) if isinstance(entry, dict)]
    report_entries = [entry for entry in as_list(discovery_navigation_report.get("entries")) if isinstance(entry, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    vector_by_review = _index_by_key(vector_entries, "reviewId")
    bridge_by_review = _index_by_key(bridge_entries, "reviewId")
    corridor_by_review = _index_by_key(corridor_entries, "reviewId")
    report_by_review = _index_by_key(report_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recommendations, key=lambda row: str(row.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        vector = vector_by_review.get(review_id, {})
        bridge = bridge_by_review.get(review_id, {})
        corridor = corridor_by_review.get(review_id, {})
        report = report_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        discovery_status = str(vector.get("discoveryStatus", rec.get("discoveryStatus", "monitor")))
        vector_class = str(vector.get("vectorClass", rec.get("vectorClass", "bounded")))
        bridge_maturity = str(bridge.get("bridgeMaturity", rec.get("bridgeMaturity", "bounded")))
        corridor_class = str(corridor.get("corridorClass", rec.get("corridorClass", "bounded")))
        dead_zone_adjacency = str(corridor.get("deadZoneAdjacency", rec.get("deadZoneAdjacency", "bounded")))
        memory_support = str(report.get("memorySupport", rec.get("memorySupport", "bounded")))
        commons_review_requirement = str(report.get("commonsReviewRequirement", rec.get("commonsReviewRequirement", "required")))
        altruistic_corridor_score = _to_float(corridor.get("altruisticCorridorScore", rec.get("altruisticCorridorScore", 0.0)))
        consent_feedback_friction = str(report.get("consentFeedbackFriction", rec.get("consentFeedbackFriction", "bounded")))
        multiscale_support_class = str(report.get("multiscaleSupportClass", rec.get("multiscaleSupportClass", "bounded")))
        conformity_penalty = _to_float(corridor.get("conformityPenalty", rec.get("conformityPenalty", 0.0)))
        repair_corridor_flag = bool(corridor.get("repairCorridorFlag", rec.get("repairCorridorFlag", False)))
        distortion_risk_class = str(report.get("distortionRiskClass", rec.get("distortionRiskClass", "bounded")))
        river_seed_potential = str(corridor.get("riverSeedPotential", rec.get("riverSeedPotential", "bounded")))
        river_formation_signal = str(corridor.get("riverFormationSignal", rec.get("riverFormationSignal", "emergent")))
        corridor_weaving_score = _to_float(corridor.get("corridorWeavingScore", rec.get("corridorWeavingScore", 0.0)))
        corridor_score = _to_float(corridor.get("corridorScore", rec.get("corridorScore", 0.0)))
        bridge_confidence = _to_float(bridge.get("bridgeConfidence", rec.get("bridgeConfidence", 0.0)))
        audit_state = str(audit.get("discoveryNavigationAuditState", rec.get("discoveryNavigationAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "discoveryStatus": discovery_status,
            "vectorClass": vector_class,
            "bridgeMaturity": bridge_maturity,
            "corridorClass": corridor_class,
            "deadZoneAdjacency": dead_zone_adjacency,
            "memorySupport": memory_support,
            "commonsReviewRequirement": commons_review_requirement,
            "altruisticCorridorScore": altruistic_corridor_score,
            "consentFeedbackFriction": consent_feedback_friction,
            "multiscaleSupportClass": multiscale_support_class,
            "conformityPenalty": conformity_penalty,
            "repairCorridorFlag": repair_corridor_flag,
            "distortionRiskClass": distortion_risk_class,
            "riverSeedPotential": river_seed_potential,
            "riverFormationSignal": river_formation_signal,
            "corridorWeavingScore": corridor_weaving_score,
            "corridorScore": corridor_score,
            "bridgeConfidence": bridge_confidence,
            "discoveryNavigationAuditState": audit_state,
            "linkedTargetIds": linked_target_ids,
        }

        if action == "docket":
            dashboard_entries.append({**base, "humanReviewFlag": bool(rec.get("humanReviewFlag", True)), "queuedAt": generated_at})
            registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({
                **base,
                "status": "watch",
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "observational": True,
                "nonCanonical": True,
                "queuedAt": generated_at,
            })

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "noAutonomousResearchExecution": True,
            "noDeploymentExecution": True,
            "noGovernanceRightsMutation": True,
            "noCanonClosure": True,
            "noRankingOfCommunitiesOrInstitutions": True,
            "corridorPriorityNotTruthAuthority": True,
            "antiDistortionSafeguardsRequired": True,
            "notes": rec.get("notes", ""),
        })

    shared = {
        "generatedAt": generated_at,
        "discoveryNavigationProtocol": True,
        "nonCanonical": True,
        "noAutonomousResearchExecution": True,
        "noDeploymentExecution": True,
        "noGovernanceRightsMutation": True,
        "noCanonClosure": True,
        "noRankingOfCommunitiesOrInstitutions": True,
        "corridorPriorityNotTruthAuthority": True,
        "provenance": provenance_summary,
        **integrity_status,
    }

    discovery_navigation_dashboard = {
        **shared,
        "entries": sorted(dashboard_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    discovery_corridor_registry = {
        **shared,
        "entries": sorted(registry_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    discovery_risk_watchlist = {
        **shared,
        "entries": sorted(watch_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    discovery_annotations = {
        **shared,
        "annotations": sorted(annotation_entries, key=lambda row: str(row.get("reviewId", ""))),
    }

    _validate_outputs(
        discovery_navigation_dashboard,
        discovery_corridor_registry,
        discovery_risk_watchlist,
        discovery_annotations,
    )
    return (
        discovery_navigation_dashboard,
        discovery_corridor_registry,
        discovery_risk_watchlist,
        discovery_annotations,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discovery-navigation-audit", type=Path, default=Path("bridge/discovery_navigation_audit.json"))
    parser.add_argument("--discovery-navigation-recommendations", type=Path, default=Path("bridge/discovery_navigation_recommendations.json"))
    parser.add_argument("--discovery-vector-field", type=Path, default=Path("bridge/discovery_vector_field.json"))
    parser.add_argument("--cross-domain-bridge-map", type=Path, default=Path("bridge/cross_domain_bridge_map.json"))
    parser.add_argument("--entropy-reduction-corridor", type=Path, default=Path("bridge/entropy_reduction_corridor.json"))
    parser.add_argument("--discovery-navigation-report", type=Path, default=Path("bridge/discovery_navigation_report.json"))

    parser.add_argument("--knowledge-topology-dashboard", type=Path, default=Path("registry/knowledge_topology_dashboard.json"))
    parser.add_argument("--operational-maturity-dashboard", type=Path, default=Path("registry/operational_maturity_dashboard.json"))
    parser.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    parser.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-discovery-navigation-dashboard", type=Path, default=Path("registry/discovery_navigation_dashboard.json"))
    parser.add_argument("--out-discovery-corridor-registry", type=Path, default=Path("registry/discovery_corridor_registry.json"))
    parser.add_argument("--out-discovery-risk-watchlist", type=Path, default=Path("registry/discovery_risk_watchlist.json"))
    parser.add_argument("--out-discovery-annotations", type=Path, default=Path("registry/discovery_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_discovery_navigation_overlays(
            load_required_json(args.discovery_navigation_audit),
            load_required_json(args.discovery_navigation_recommendations),
            load_required_json(args.discovery_vector_field),
            load_required_json(args.cross_domain_bridge_map),
            load_required_json(args.entropy_reduction_corridor),
            load_required_json(args.discovery_navigation_report),
            load_required_json(args.knowledge_topology_dashboard),
            load_required_json(args.operational_maturity_dashboard),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.commons_sovereignty_dashboard),
            load_required_json(args.value_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_discovery_navigation_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_discovery_corridor_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_discovery_risk_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_discovery_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_discovery_navigation_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_discovery_corridor_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_discovery_risk_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_discovery_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote discovery navigation dashboard: {args.out_discovery_navigation_dashboard}")
    print(f"[OK] Wrote discovery corridor registry: {args.out_discovery_corridor_registry}")
    print(f"[OK] Wrote discovery risk watchlist: {args.out_discovery_risk_watchlist}")
    print(f"[OK] Wrote discovery annotations: {args.out_discovery_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
