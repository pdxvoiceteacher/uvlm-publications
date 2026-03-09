#!/usr/bin/env python3
"""Build knowledge river and corridor braiding overlays.

Publisher surfaces only Sophia-audited knowledge-river materials; it does not
authorize canon formation, deployment, institutional control, or prestige hierarchy.
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
    knowledge_river_dashboard: dict[str, Any],
    river_registry: dict[str, Any],
    river_capture_watchlist: dict[str, Any],
    river_annotations: dict[str, Any],
) -> None:
    if not isinstance(knowledge_river_dashboard.get("entries"), list):
        raise ValueError("knowledge_river_dashboard.entries must be a list")
    if not isinstance(river_registry.get("entries"), list):
        raise ValueError("river_registry.entries must be a list")
    if not isinstance(river_capture_watchlist.get("entries"), list):
        raise ValueError("river_capture_watchlist.entries must be a list")
    if not isinstance(river_annotations.get("annotations"), list):
        raise ValueError("river_annotations.annotations must be a list")

    for payload in (knowledge_river_dashboard, river_registry, river_capture_watchlist, river_annotations):
        for key in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(key), bool):
                raise ValueError(f"{key} must be a boolean")
        json.dumps(payload)


def build_knowledge_river_overlays(
    knowledge_river_audit: dict[str, Any],
    knowledge_river_recommendations: dict[str, Any],
    knowledge_river_map: dict[str, Any],
    corridor_braiding_report: dict[str, Any],
    tributary_support_registry: dict[str, Any],
    river_capture_risk_report: dict[str, Any],
    discovery_navigation_dashboard: dict[str, Any],
    knowledge_topology_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "knowledge_river_audit": _extract_required_provenance("knowledge_river_audit", knowledge_river_audit),
        "knowledge_river_recommendations": _extract_required_provenance("knowledge_river_recommendations", knowledge_river_recommendations),
        "knowledge_river_map": _extract_required_provenance("knowledge_river_map", knowledge_river_map),
        "corridor_braiding_report": _extract_required_provenance("corridor_braiding_report", corridor_braiding_report),
        "tributary_support_registry": _extract_required_provenance("tributary_support_registry", tributary_support_registry),
        "river_capture_risk_report": _extract_required_provenance("river_capture_risk_report", river_capture_risk_report),
    }

    for name, artifact in {
        "discovery_navigation_dashboard": discovery_navigation_dashboard,
        "knowledge_topology_dashboard": knowledge_topology_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "value_dashboard": value_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    provenance_summary = _build_provenance_summary(provenances)
    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [entry for entry in as_list(knowledge_river_audit.get("audits")) if isinstance(entry, dict)]
    recommendations = [entry for entry in as_list(knowledge_river_recommendations.get("recommendations")) if isinstance(entry, dict)]
    river_map_entries = [entry for entry in as_list(knowledge_river_map.get("entries")) if isinstance(entry, dict)]
    braid_entries = [entry for entry in as_list(corridor_braiding_report.get("entries")) if isinstance(entry, dict)]
    tributary_entries = [entry for entry in as_list(tributary_support_registry.get("entries")) if isinstance(entry, dict)]
    capture_entries = [entry for entry in as_list(river_capture_risk_report.get("entries")) if isinstance(entry, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    map_by_review = _index_by_key(river_map_entries, "reviewId")
    braid_by_review = _index_by_key(braid_entries, "reviewId")
    tributary_by_review = _index_by_key(tributary_entries, "reviewId")
    capture_by_review = _index_by_key(capture_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recommendations, key=lambda row: str(row.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        river_map = map_by_review.get(review_id, {})
        braid = braid_by_review.get(review_id, {})
        tributary = tributary_by_review.get(review_id, {})
        capture = capture_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        river_status = str(river_map.get("riverStatus", rec.get("riverStatus", "monitor")))
        river_class = str(river_map.get("riverClass", rec.get("riverClass", "bounded")))
        corridor_weaving_score = _to_float(braid.get("corridorWeavingScore", rec.get("corridorWeavingScore", 0.0)))
        braid_stability = str(braid.get("braidStability", rec.get("braidStability", "bounded")))
        tributary_class = str(tributary.get("tributaryClass", rec.get("tributaryClass", "bounded")))
        memory_support = str(tributary.get("memorySupport", rec.get("memorySupport", "bounded")))
        multiscale_validation = str(braid.get("multiscaleValidation", rec.get("multiscaleValidation", "bounded")))
        altruistic_weighting = _to_float(braid.get("altruisticWeighting", rec.get("altruisticWeighting", 0.0)))
        river_capture_risk = str(capture.get("riverCaptureRisk", rec.get("riverCaptureRisk", "bounded")))
        provenance_markers = as_list(capture.get("provenanceMarkers", rec.get("provenanceMarkers", [])))
        canonical_integrity_markers = as_list(capture.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", [])))
        audit_state = str(audit.get("knowledgeRiverAuditState", rec.get("knowledgeRiverAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "riverStatus": river_status,
            "riverClass": river_class,
            "corridorWeavingScore": corridor_weaving_score,
            "braidStability": braid_stability,
            "tributaryClass": tributary_class,
            "memorySupport": memory_support,
            "multiscaleValidation": multiscale_validation,
            "altruisticWeighting": altruistic_weighting,
            "riverCaptureRisk": river_capture_risk,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "knowledgeRiverAuditState": audit_state,
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
            "noCanonMutation": True,
            "noDeploymentExecution": True,
            "noGovernanceRightsMutation": True,
            "noRankingOfPersonsCommunitiesInstitutionsTraditions": True,
            "riverMaturityNotTruthAuthority": True,
            "noTheoryCompetitionClosure": True,
            "notes": rec.get("notes", ""),
        })

    shared = {
        "generatedAt": generated_at,
        "knowledgeRiverProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightsMutation": True,
        "noRankingOfPersonsCommunitiesInstitutionsTraditions": True,
        "riverMaturityNotTruthAuthority": True,
        "noTheoryCompetitionClosure": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsKnowledgeRiverMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "provenance": provenance_summary,
        **integrity_status,
    }

    knowledge_river_dashboard = {
        **shared,
        "entries": sorted(dashboard_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    river_registry = {
        **shared,
        "entries": sorted(registry_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    river_capture_watchlist = {
        **shared,
        "entries": sorted(watch_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    river_annotations = {
        **shared,
        "annotations": sorted(annotation_entries, key=lambda row: str(row.get("reviewId", ""))),
    }

    _validate_outputs(knowledge_river_dashboard, river_registry, river_capture_watchlist, river_annotations)
    return knowledge_river_dashboard, river_registry, river_capture_watchlist, river_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--knowledge-river-audit", type=Path, default=Path("bridge/knowledge_river_audit.json"))
    parser.add_argument("--knowledge-river-recommendations", type=Path, default=Path("bridge/knowledge_river_recommendations.json"))
    parser.add_argument("--knowledge-river-map", type=Path, default=Path("bridge/knowledge_river_map.json"))
    parser.add_argument("--corridor-braiding-report", type=Path, default=Path("bridge/corridor_braiding_report.json"))
    parser.add_argument("--tributary-support-registry", type=Path, default=Path("bridge/tributary_support_registry.json"))
    parser.add_argument("--river-capture-risk-report", type=Path, default=Path("bridge/river_capture_risk_report.json"))

    parser.add_argument("--discovery-navigation-dashboard", type=Path, default=Path("registry/discovery_navigation_dashboard.json"))
    parser.add_argument("--knowledge-topology-dashboard", type=Path, default=Path("registry/knowledge_topology_dashboard.json"))
    parser.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    parser.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-knowledge-river-dashboard", type=Path, default=Path("registry/knowledge_river_dashboard.json"))
    parser.add_argument("--out-river-registry", type=Path, default=Path("registry/river_registry.json"))
    parser.add_argument("--out-river-capture-watchlist", type=Path, default=Path("registry/river_capture_watchlist.json"))
    parser.add_argument("--out-river-annotations", type=Path, default=Path("registry/river_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_knowledge_river_overlays(
            load_required_json(args.knowledge_river_audit),
            load_required_json(args.knowledge_river_recommendations),
            load_required_json(args.knowledge_river_map),
            load_required_json(args.corridor_braiding_report),
            load_required_json(args.tributary_support_registry),
            load_required_json(args.river_capture_risk_report),
            load_required_json(args.discovery_navigation_dashboard),
            load_required_json(args.knowledge_topology_dashboard),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.commons_sovereignty_dashboard),
            load_required_json(args.value_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_knowledge_river_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_river_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_river_capture_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_river_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_knowledge_river_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_river_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_river_capture_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_river_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote knowledge river dashboard: {args.out_knowledge_river_dashboard}")
    print(f"[OK] Wrote river registry: {args.out_river_registry}")
    print(f"[OK] Wrote river capture watchlist: {args.out_river_capture_watchlist}")
    print(f"[OK] Wrote river annotations: {args.out_river_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
