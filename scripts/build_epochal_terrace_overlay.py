#!/usr/bin/env python3
"""Build epochal terrace and plateau stability overlays.

Publisher surfaces only Sophia-audited epochal terrace materials; it does not
declare permanent epochs, canonize social orders, or authorize institutional
consolidation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from canonical_integrity_manifest import evaluate_manifest_pair, load_manifest

REQUIRED_PROVENANCE_KEYS = ("schemaVersion", "producerCommits", "sourceMode")
RESETTABLE_ATLAS_CLASSES = [
    "terrace-stable",
    "terrace-watch",
    "plateau-bounded",
    "erosion-risk",
    "terrace-trust-degraded",
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


def _index_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        key_value = row.get(key)
        if isinstance(key_value, str):
            out[key_value] = row
    return out


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    return action if action in {"docket", "watch", "suppressed", "suppress", "rejected"} else "watch"


def _atlas_classes(terrace_status: str, plateau_class: str, erosion_risk: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if terrace_status in {"stable", "bounded", "monitor"}:
        out.append("terrace-stable")
    if terrace_status in {"watch", "fragile"}:
        out.append("terrace-watch")
    if plateau_class in {"bounded", "stable", "plural"}:
        out.append("plateau-bounded")
    if erosion_risk in {"high", "elevated", "critical"}:
        out.append("erosion-risk")
    if trust_degraded:
        out.append("terrace-trust-degraded")
    return out


def build_epochal_terrace_overlays(
    epochal_terrace_audit: dict[str, Any],
    epochal_terrace_recommendations: dict[str, Any],
    epochal_terrace_map: dict[str, Any],
    stability_plateau_report: dict[str, Any],
    institutional_sedimentation_registry: dict[str, Any],
    terrace_erosion_risk_report: dict[str, Any],
    delta_dashboard: dict[str, Any],
    knowledge_river_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    trust_surface_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "epochal_terrace_audit": _extract_required_provenance("epochal_terrace_audit", epochal_terrace_audit),
        "epochal_terrace_recommendations": _extract_required_provenance("epochal_terrace_recommendations", epochal_terrace_recommendations),
        "epochal_terrace_map": _extract_required_provenance("epochal_terrace_map", epochal_terrace_map),
        "stability_plateau_report": _extract_required_provenance("stability_plateau_report", stability_plateau_report),
        "institutional_sedimentation_registry": _extract_required_provenance("institutional_sedimentation_registry", institutional_sedimentation_registry),
        "terrace_erosion_risk_report": _extract_required_provenance("terrace_erosion_risk_report", terrace_erosion_risk_report),
    }

    for name, artifact in {
        "delta_dashboard": delta_dashboard,
        "knowledge_river_dashboard": knowledge_river_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "trust_surface_dashboard": trust_surface_dashboard,
        "value_dashboard": value_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    provenance_summary = _build_provenance_summary(provenances)
    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [entry for entry in as_list(epochal_terrace_audit.get("audits")) if isinstance(entry, dict)]
    recommendations = [entry for entry in as_list(epochal_terrace_recommendations.get("recommendations")) if isinstance(entry, dict)]
    terrace_entries = [entry for entry in as_list(epochal_terrace_map.get("entries")) if isinstance(entry, dict)]
    plateau_entries = [entry for entry in as_list(stability_plateau_report.get("entries")) if isinstance(entry, dict)]
    sediment_entries = [entry for entry in as_list(institutional_sedimentation_registry.get("entries")) if isinstance(entry, dict)]
    erosion_entries = [entry for entry in as_list(terrace_erosion_risk_report.get("entries")) if isinstance(entry, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    terrace_by = _index_by_key(terrace_entries, "reviewId")
    plateau_by = _index_by_key(plateau_entries, "reviewId")
    sediment_by = _index_by_key(sediment_entries, "reviewId")
    erosion_by = _index_by_key(erosion_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recommendations, key=lambda row: str(row.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        terrace = terrace_by.get(review_id, {})
        plateau = plateau_by.get(review_id, {})
        sediment = sediment_by.get(review_id, {})
        erosion = erosion_by.get(review_id, {})
        audit = audit_by.get(review_id, {})

        terrace_status = str(terrace.get("terraceStatus", rec.get("terraceStatus", "monitor")))
        terrace_class = str(terrace.get("terraceClass", rec.get("terraceClass", "bounded")))
        plateau_class = str(plateau.get("plateauClass", rec.get("plateauClass", "bounded")))
        sediment_class = str(sediment.get("sedimentClass", rec.get("sedimentClass", "bounded")))
        plurality_retention = str(plateau.get("pluralityRetention", rec.get("pluralityRetention", "bounded")))
        trust_surface_stability = str(plateau.get("trustSurfaceStability", rec.get("trustSurfaceStability", "bounded")))
        erosion_risk = str(erosion.get("erosionRisk", rec.get("erosionRisk", "bounded"))).lower()
        institutional_embedment = _to_float(sediment.get("institutionalEmbedment", rec.get("institutionalEmbedment", 0.0)))
        provenance_markers = [str(v) for v in as_list(erosion.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(erosion.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))

        base = {
            "reviewId": review_id,
            "terraceStatus": terrace_status,
            "terraceClass": terrace_class,
            "plateauClass": plateau_class,
            "sedimentClass": sediment_class,
            "pluralityRetention": plurality_retention,
            "trustSurfaceStability": trust_surface_stability,
            "erosionRisk": erosion_risk,
            "institutionalEmbedment": institutional_embedment,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": _atlas_classes(terrace_status, plateau_class, erosion_risk, trust_degraded),
            "epochalTerraceAuditState": str(audit.get("epochalTerraceAuditState", rec.get("epochalTerraceAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({**base, "status": "watch", "queuedAt": generated_at})

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "noCanonMutation": True,
            "noDeploymentExecution": True,
            "noGovernanceRightMutation": True,
            "noRankingOfCivilizationsCommunitiesInstitutionsTraditions": True,
            "terraceStabilityNotTruthAuthority": True,
            "noTheoryCompetitionClosure": True,
            "noEpochConfirmedForeverPresentation": True,
        })

    shared = {
        "generatedAt": generated_at,
        "epochalTerraceProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfCivilizationsCommunitiesInstitutionsTraditions": True,
        "terraceStabilityNotTruthAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noEpochConfirmedForeverPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsTerraceMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": provenance_summary,
        **integrity_status,
    }

    epoch_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda row: str(row.get("reviewId", "")))}
    plateau_registry = {**shared, "entries": sorted(registry_entries, key=lambda row: str(row.get("reviewId", "")))}
    terrace_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda row: str(row.get("reviewId", "")))}
    epoch_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda row: str(row.get("reviewId", "")))}

    for payload, key in (
        (epoch_dashboard, "entries"),
        (plateau_registry, "entries"),
        (terrace_watchlist, "entries"),
        (epoch_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for field in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(field), bool):
                raise ValueError(f"{field} must be a boolean")

    return epoch_dashboard, plateau_registry, terrace_watchlist, epoch_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochal-terrace-audit", type=Path, default=Path("bridge/epochal_terrace_audit.json"))
    parser.add_argument("--epochal-terrace-recommendations", type=Path, default=Path("bridge/epochal_terrace_recommendations.json"))
    parser.add_argument("--epochal-terrace-map", type=Path, default=Path("bridge/epochal_terrace_map.json"))
    parser.add_argument("--stability-plateau-report", type=Path, default=Path("bridge/stability_plateau_report.json"))
    parser.add_argument("--institutional-sedimentation-registry", type=Path, default=Path("bridge/institutional_sedimentation_registry.json"))
    parser.add_argument("--terrace-erosion-risk-report", type=Path, default=Path("bridge/terrace_erosion_risk_report.json"))

    parser.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    parser.add_argument("--knowledge-river-dashboard", type=Path, default=Path("registry/knowledge_river_dashboard.json"))
    parser.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    parser.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    parser.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-epoch-dashboard", type=Path, default=Path("registry/epoch_dashboard.json"))
    parser.add_argument("--out-plateau-registry", type=Path, default=Path("registry/plateau_registry.json"))
    parser.add_argument("--out-terrace-watchlist", type=Path, default=Path("registry/terrace_watchlist.json"))
    parser.add_argument("--out-epoch-annotations", type=Path, default=Path("registry/epoch_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_epochal_terrace_overlays(
            load_required_json(args.epochal_terrace_audit),
            load_required_json(args.epochal_terrace_recommendations),
            load_required_json(args.epochal_terrace_map),
            load_required_json(args.stability_plateau_report),
            load_required_json(args.institutional_sedimentation_registry),
            load_required_json(args.terrace_erosion_risk_report),
            load_required_json(args.delta_dashboard),
            load_required_json(args.knowledge_river_dashboard),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.commons_sovereignty_dashboard),
            load_required_json(args.trust_surface_dashboard),
            load_required_json(args.value_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    for out in (
        args.out_epoch_dashboard,
        args.out_plateau_registry,
        args.out_terrace_watchlist,
        args.out_epoch_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_epoch_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_plateau_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_terrace_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_epoch_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote epoch dashboard: {args.out_epoch_dashboard}")
    print(f"[OK] Wrote plateau registry: {args.out_plateau_registry}")
    print(f"[OK] Wrote terrace watchlist: {args.out_terrace_watchlist}")
    print(f"[OK] Wrote epoch annotations: {args.out_epoch_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
