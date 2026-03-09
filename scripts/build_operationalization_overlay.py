#!/usr/bin/env python3
"""Build operationalization boundary and maturity overlays.

Publisher surfaces only Sophia-audited operationalization materials; it does
not authorize deployment, implementation, or institutional control.
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
    operational_maturity_dashboard: dict[str, Any],
    deployment_boundary_registry: dict[str, Any],
    translation_risk_watchlist: dict[str, Any],
    operationalization_annotations: dict[str, Any],
) -> None:
    if not isinstance(operational_maturity_dashboard.get("entries"), list):
        raise ValueError("operational_maturity_dashboard.entries must be a list")
    if not isinstance(deployment_boundary_registry.get("entries"), list):
        raise ValueError("deployment_boundary_registry.entries must be a list")
    if not isinstance(translation_risk_watchlist.get("entries"), list):
        raise ValueError("translation_risk_watchlist.entries must be a list")
    if not isinstance(operationalization_annotations.get("annotations"), list):
        raise ValueError("operationalization_annotations.annotations must be a list")

    for payload in (
        operational_maturity_dashboard,
        deployment_boundary_registry,
        translation_risk_watchlist,
        operationalization_annotations,
    ):
        for key in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(key), bool):
                raise ValueError(f"{key} must be a boolean")
        json.dumps(payload)


def build_operationalization_overlays(
    operationalization_audit: dict[str, Any],
    operationalization_recommendations: dict[str, Any],
    operational_maturity_map: dict[str, Any],
    deployment_boundary_report: dict[str, Any],
    translation_risk_register: dict[str, Any],
    operationalization_gate: dict[str, Any],
    knowledge_topology_dashboard: dict[str, Any],
    emergent_domain_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "operationalization_audit": _extract_required_provenance("operationalization_audit", operationalization_audit),
        "operationalization_recommendations": _extract_required_provenance("operationalization_recommendations", operationalization_recommendations),
        "operational_maturity_map": _extract_required_provenance("operational_maturity_map", operational_maturity_map),
        "deployment_boundary_report": _extract_required_provenance("deployment_boundary_report", deployment_boundary_report),
        "translation_risk_register": _extract_required_provenance("translation_risk_register", translation_risk_register),
        "operationalization_gate": _extract_required_provenance("operationalization_gate", operationalization_gate),
    }
    for name, artifact in {
        "knowledge_topology_dashboard": knowledge_topology_dashboard,
        "emergent_domain_dashboard": emergent_domain_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "value_dashboard": value_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    provenance_summary = _build_provenance_summary(provenances)
    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [entry for entry in as_list(operationalization_audit.get("audits")) if isinstance(entry, dict)]
    recommendations = [entry for entry in as_list(operationalization_recommendations.get("recommendations")) if isinstance(entry, dict)]
    maturity_entries = [entry for entry in as_list(operational_maturity_map.get("entries")) if isinstance(entry, dict)]
    boundary_entries = [entry for entry in as_list(deployment_boundary_report.get("entries")) if isinstance(entry, dict)]
    risk_entries = [entry for entry in as_list(translation_risk_register.get("entries")) if isinstance(entry, dict)]
    gate_entries = [entry for entry in as_list(operationalization_gate.get("entries")) if isinstance(entry, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    maturity_by_review = _index_by_key(maturity_entries, "reviewId")
    boundary_by_review = _index_by_key(boundary_entries, "reviewId")
    risk_by_review = _index_by_key(risk_entries, "reviewId")
    gate_by_review = _index_by_key(gate_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recommendations, key=lambda row: str(row.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        maturity = maturity_by_review.get(review_id, {})
        boundary = boundary_by_review.get(review_id, {})
        risk = risk_by_review.get(review_id, {})
        gate = gate_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        operational_status = str(maturity.get("operationalStatus", rec.get("operationalStatus", "monitor")))
        maturity_class = str(maturity.get("maturityClass", rec.get("maturityClass", "bounded")))
        deployment_readiness = str(boundary.get("deploymentReadiness", rec.get("deploymentReadiness", "bounded")))
        dead_zone_adjacency = str(boundary.get("deadZoneAdjacency", rec.get("deadZoneAdjacency", "bounded")))
        translation_risk = str(risk.get("translationRisk", rec.get("translationRisk", "bounded")))
        required_safeguards = sorted([str(v) for v in as_list(gate.get("requiredSafeguards", rec.get("requiredSafeguards", []))) if str(v).strip()])
        commons_review_requirement = str(gate.get("commonsReviewRequirement", rec.get("commonsReviewRequirement", "required")))
        readiness_score = _to_float(maturity.get("readinessScore", rec.get("readinessScore", 0.0)))
        translation_risk_score = _to_float(risk.get("translationRiskScore", rec.get("translationRiskScore", 0.0)))
        audit_state = str(audit.get("operationalizationAuditState", rec.get("operationalizationAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "operationalStatus": operational_status,
            "maturityClass": maturity_class,
            "deploymentReadiness": deployment_readiness,
            "deadZoneAdjacency": dead_zone_adjacency,
            "translationRisk": translation_risk,
            "requiredSafeguards": required_safeguards,
            "commonsReviewRequirement": commons_review_requirement,
            "readinessScore": readiness_score,
            "translationRiskScore": translation_risk_score,
            "operationalizationAuditState": audit_state,
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
            "noDeploymentExecution": True,
            "noPolicyEnactment": True,
            "noGovernanceRightsMutation": True,
            "noCanonClosure": True,
            "noRankingOfPersonsCommunitiesInstitutions": True,
            "scientificMaturityNotOperationalControlLicense": True,
            "notes": rec.get("notes", ""),
        })

    shared = {
        "generatedAt": generated_at,
        "operationalizationProtocol": True,
        "nonCanonical": True,
        "noDeploymentExecution": True,
        "noPolicyEnactment": True,
        "noGovernanceRightsMutation": True,
        "noCanonClosure": True,
        "noRankingOfPersonsCommunitiesInstitutions": True,
        "scientificMaturityNotOperationalControlLicense": True,
        "provenance": provenance_summary,
        **integrity_status,
    }

    operational_maturity_dashboard = {
        **shared,
        "entries": sorted(dashboard_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    deployment_boundary_registry = {
        **shared,
        "entries": sorted(registry_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    translation_risk_watchlist = {
        **shared,
        "entries": sorted(watch_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    operationalization_annotations = {
        **shared,
        "annotations": sorted(annotation_entries, key=lambda row: str(row.get("reviewId", ""))),
    }

    _validate_outputs(
        operational_maturity_dashboard,
        deployment_boundary_registry,
        translation_risk_watchlist,
        operationalization_annotations,
    )
    return (
        operational_maturity_dashboard,
        deployment_boundary_registry,
        translation_risk_watchlist,
        operationalization_annotations,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operationalization-audit", type=Path, default=Path("bridge/operationalization_audit.json"))
    parser.add_argument("--operationalization-recommendations", type=Path, default=Path("bridge/operationalization_recommendations.json"))
    parser.add_argument("--operational-maturity-map", type=Path, default=Path("bridge/operational_maturity_map.json"))
    parser.add_argument("--deployment-boundary-report", type=Path, default=Path("bridge/deployment_boundary_report.json"))
    parser.add_argument("--translation-risk-register", type=Path, default=Path("bridge/translation_risk_register.json"))
    parser.add_argument("--operationalization-gate", type=Path, default=Path("bridge/operationalization_gate.json"))

    parser.add_argument("--knowledge-topology-dashboard", type=Path, default=Path("registry/knowledge_topology_dashboard.json"))
    parser.add_argument("--emergent-domain-dashboard", type=Path, default=Path("registry/emergent_domain_dashboard.json"))
    parser.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    parser.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-operational-maturity-dashboard", type=Path, default=Path("registry/operational_maturity_dashboard.json"))
    parser.add_argument("--out-deployment-boundary-registry", type=Path, default=Path("registry/deployment_boundary_registry.json"))
    parser.add_argument("--out-translation-risk-watchlist", type=Path, default=Path("registry/translation_risk_watchlist.json"))
    parser.add_argument("--out-operationalization-annotations", type=Path, default=Path("registry/operationalization_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_operationalization_overlays(
            load_required_json(args.operationalization_audit),
            load_required_json(args.operationalization_recommendations),
            load_required_json(args.operational_maturity_map),
            load_required_json(args.deployment_boundary_report),
            load_required_json(args.translation_risk_register),
            load_required_json(args.operationalization_gate),
            load_required_json(args.knowledge_topology_dashboard),
            load_required_json(args.emergent_domain_dashboard),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.commons_sovereignty_dashboard),
            load_required_json(args.value_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_operational_maturity_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_deployment_boundary_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_translation_risk_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_operationalization_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_operational_maturity_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_deployment_boundary_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_translation_risk_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_operationalization_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote operational maturity dashboard: {args.out_operational_maturity_dashboard}")
    print(f"[OK] Wrote deployment boundary registry: {args.out_deployment_boundary_registry}")
    print(f"[OK] Wrote translation risk watchlist: {args.out_translation_risk_watchlist}")
    print(f"[OK] Wrote operationalization annotations: {args.out_operationalization_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
