#!/usr/bin/env python3
"""Build civilizational delta and paradigm transition overlays.

Publisher surfaces only Sophia-audited civilizational delta materials; it does
not authorize epoch declarations, canon formation, governance transition, or
civilizational ranking.
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
    "delta-convergent",
    "delta-branching",
    "delta-capture-risk",
    "delta-plurality-preserved",
    "delta-trust-degraded",
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


def _atlas_classes(convergence_class: str, plurality_preservation: str, capture_risk: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if convergence_class in {"aligned", "convergent", "bounded"}:
        out.append("delta-convergent")
    if convergence_class in {"branching", "divergent", "uncertain"}:
        out.append("delta-branching")
    if capture_risk in {"high", "elevated", "critical"}:
        out.append("delta-capture-risk")
    if plurality_preservation in {"preserved", "high", "bounded"}:
        out.append("delta-plurality-preserved")
    if trust_degraded:
        out.append("delta-trust-degraded")
    return out


def build_civilizational_delta_overlays(
    civilizational_delta_audit: dict[str, Any],
    civilizational_delta_recommendations: dict[str, Any],
    delta_seed_map: dict[str, Any],
    paradigm_convergence_report: dict[str, Any],
    epistemic_reorganization_signal: dict[str, Any],
    civilizational_delta_forecast: dict[str, Any],
    knowledge_river_dashboard: dict[str, Any],
    discovery_navigation_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    trust_surface_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "civilizational_delta_audit": _extract_required_provenance("civilizational_delta_audit", civilizational_delta_audit),
        "civilizational_delta_recommendations": _extract_required_provenance("civilizational_delta_recommendations", civilizational_delta_recommendations),
        "delta_seed_map": _extract_required_provenance("delta_seed_map", delta_seed_map),
        "paradigm_convergence_report": _extract_required_provenance("paradigm_convergence_report", paradigm_convergence_report),
        "epistemic_reorganization_signal": _extract_required_provenance("epistemic_reorganization_signal", epistemic_reorganization_signal),
        "civilizational_delta_forecast": _extract_required_provenance("civilizational_delta_forecast", civilizational_delta_forecast),
    }

    for name, artifact in {
        "knowledge_river_dashboard": knowledge_river_dashboard,
        "discovery_navigation_dashboard": discovery_navigation_dashboard,
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

    audits = [entry for entry in as_list(civilizational_delta_audit.get("audits")) if isinstance(entry, dict)]
    recommendations = [entry for entry in as_list(civilizational_delta_recommendations.get("recommendations")) if isinstance(entry, dict)]
    seed_entries = [entry for entry in as_list(delta_seed_map.get("entries")) if isinstance(entry, dict)]
    convergence_entries = [entry for entry in as_list(paradigm_convergence_report.get("entries")) if isinstance(entry, dict)]
    reorg_entries = [entry for entry in as_list(epistemic_reorganization_signal.get("entries")) if isinstance(entry, dict)]
    forecast_entries = [entry for entry in as_list(civilizational_delta_forecast.get("entries")) if isinstance(entry, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    seed_by = _index_by_key(seed_entries, "reviewId")
    convergence_by = _index_by_key(convergence_entries, "reviewId")
    reorg_by = _index_by_key(reorg_entries, "reviewId")
    forecast_by = _index_by_key(forecast_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recommendations, key=lambda row: str(row.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        seed = seed_by.get(review_id, {})
        conv = convergence_by.get(review_id, {})
        reorg = reorg_by.get(review_id, {})
        fore = forecast_by.get(review_id, {})
        audit = audit_by.get(review_id, {})

        delta_status = str(seed.get("deltaStatus", rec.get("deltaStatus", "monitor")))
        delta_seed_class = str(seed.get("deltaSeedClass", rec.get("deltaSeedClass", "bounded")))
        convergence_class = str(conv.get("convergenceClass", rec.get("convergenceClass", "bounded")))
        reorganization_class = str(reorg.get("reorganizationClass", rec.get("reorganizationClass", "bounded")))
        river_braiding_density = _to_float(conv.get("riverBraidingDensity", rec.get("riverBraidingDensity", 0.0)))
        memory_support = str(fore.get("memorySupport", rec.get("memorySupport", "bounded")))
        distributary_potential = str(fore.get("distributaryPotential", rec.get("distributaryPotential", "bounded")))
        trust_surface_stability = str(fore.get("trustSurfaceStability", rec.get("trustSurfaceStability", "bounded")))
        plurality_preservation = str(fore.get("pluralityPreservation", rec.get("pluralityPreservation", "bounded")))
        capture_risk = str(fore.get("captureRisk", rec.get("captureRisk", "bounded"))).lower()
        provenance_markers = [str(v) for v in as_list(fore.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(fore.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))

        base = {
            "reviewId": review_id,
            "deltaStatus": delta_status,
            "deltaSeedClass": delta_seed_class,
            "convergenceClass": convergence_class,
            "reorganizationClass": reorganization_class,
            "riverBraidingDensity": river_braiding_density,
            "memorySupport": memory_support,
            "distributaryPotential": distributary_potential,
            "trustSurfaceStability": trust_surface_stability,
            "pluralityPreservation": plurality_preservation,
            "captureRisk": capture_risk,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": _atlas_classes(convergence_class, plurality_preservation, capture_risk, trust_degraded),
            "deltaAuditState": str(audit.get("civilizationalDeltaAuditState", rec.get("civilizationalDeltaAuditState", "none"))),
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
            "noRankingOfPersonsCommunitiesInstitutionsCivilizations": True,
            "deltaMaturityNotTruthAuthority": True,
            "noTheoryCompetitionClosure": True,
            "noEpochConfirmedPresentation": True,
        })

    shared = {
        "generatedAt": generated_at,
        "civilizationalDeltaProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfPersonsCommunitiesInstitutionsCivilizations": True,
        "deltaMaturityNotTruthAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noEpochConfirmedPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsDeltaMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": provenance_summary,
        **integrity_status,
    }

    delta_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda row: str(row.get("reviewId", "")))}
    paradigm_transition_registry = {**shared, "entries": sorted(registry_entries, key=lambda row: str(row.get("reviewId", "")))}
    epoch_shift_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda row: str(row.get("reviewId", "")))}
    delta_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda row: str(row.get("reviewId", "")))}

    for payload, key in (
        (delta_dashboard, "entries"),
        (paradigm_transition_registry, "entries"),
        (epoch_shift_watchlist, "entries"),
        (delta_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for field in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(field), bool):
                raise ValueError(f"{field} must be a boolean")

    return delta_dashboard, paradigm_transition_registry, epoch_shift_watchlist, delta_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--civilizational-delta-audit", type=Path, default=Path("bridge/civilizational_delta_audit.json"))
    parser.add_argument("--civilizational-delta-recommendations", type=Path, default=Path("bridge/civilizational_delta_recommendations.json"))
    parser.add_argument("--delta-seed-map", type=Path, default=Path("bridge/delta_seed_map.json"))
    parser.add_argument("--paradigm-convergence-report", type=Path, default=Path("bridge/paradigm_convergence_report.json"))
    parser.add_argument("--epistemic-reorganization-signal", type=Path, default=Path("bridge/epistemic_reorganization_signal.json"))
    parser.add_argument("--civilizational-delta-forecast", type=Path, default=Path("bridge/civilizational_delta_forecast.json"))

    parser.add_argument("--knowledge-river-dashboard", type=Path, default=Path("registry/knowledge_river_dashboard.json"))
    parser.add_argument("--discovery-navigation-dashboard", type=Path, default=Path("registry/discovery_navigation_dashboard.json"))
    parser.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    parser.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    parser.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    parser.add_argument("--out-paradigm-transition-registry", type=Path, default=Path("registry/paradigm_transition_registry.json"))
    parser.add_argument("--out-epoch-shift-watchlist", type=Path, default=Path("registry/epoch_shift_watchlist.json"))
    parser.add_argument("--out-delta-annotations", type=Path, default=Path("registry/delta_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_civilizational_delta_overlays(
            load_required_json(args.civilizational_delta_audit),
            load_required_json(args.civilizational_delta_recommendations),
            load_required_json(args.delta_seed_map),
            load_required_json(args.paradigm_convergence_report),
            load_required_json(args.epistemic_reorganization_signal),
            load_required_json(args.civilizational_delta_forecast),
            load_required_json(args.knowledge_river_dashboard),
            load_required_json(args.discovery_navigation_dashboard),
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
        args.out_delta_dashboard,
        args.out_paradigm_transition_registry,
        args.out_epoch_shift_watchlist,
        args.out_delta_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_delta_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_paradigm_transition_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_epoch_shift_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_delta_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote delta dashboard: {args.out_delta_dashboard}")
    print(f"[OK] Wrote paradigm transition registry: {args.out_paradigm_transition_registry}")
    print(f"[OK] Wrote epoch shift watchlist: {args.out_epoch_shift_watchlist}")
    print(f"[OK] Wrote delta annotations: {args.out_delta_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
