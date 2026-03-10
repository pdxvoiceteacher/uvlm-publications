#!/usr/bin/env python3
"""Build terrace erosion and renewal corridor overlays.

Publisher surfaces only Sophia-audited terrace erosion and renewal materials;
it does not declare epoch collapse, canonize successor systems, or authorize
institutional transition.
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
    "erosion-watch",
    "renewal-corridor",
    "orthodoxy-pressure",
    "plurality-recovery",
    "erosion-trust-degraded",
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
    if not isinstance(prov.get("schemaVersion"), str) or not str(prov.get("schemaVersion", "")).strip():
        raise ValueError(f"{name} provenance.schemaVersion must be a non-empty string")
    commits = prov.get("producerCommits")
    if not isinstance(commits, list) or not commits or not all(isinstance(v, str) and v.strip() for v in commits):
        raise ValueError(f"{name} provenance.producerCommits must be a non-empty list of non-empty strings")
    if not isinstance(prov.get("sourceMode"), str) or not str(prov.get("sourceMode", "")).strip():
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
    commits: list[str] = []
    schema_versions: dict[str, str] = {}
    source_modes: dict[str, str] = {}
    for name, prov in provenances.items():
        schema_versions[name] = str(prov.get("schemaVersion"))
        source_modes[name] = str(prov.get("sourceMode"))
        for c in prov.get("producerCommits", []):
            if c not in commits:
                commits.append(c)
    return {
        "schemaVersions": schema_versions,
        "producerCommits": commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": any(v.lower() == "fixture" for v in source_modes.values()),
    }


def _index_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        k = row.get(key)
        if isinstance(k, str):
            out[k] = row
    return out


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    return action if action in {"docket", "watch", "suppressed", "suppress", "rejected"} else "watch"


def _atlas_classes(erosion_class: str, orthodoxy_class: str, renewal_class: str, plurality: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if erosion_class in {"elevated", "high", "critical", "watch"}:
        out.append("erosion-watch")
    if renewal_class in {"active", "emergent", "bounded"}:
        out.append("renewal-corridor")
    if orthodoxy_class in {"high", "rigid", "captured", "elevated"}:
        out.append("orthodoxy-pressure")
    if plurality in {"recovery", "preserved", "repairing"}:
        out.append("plurality-recovery")
    if trust_degraded:
        out.append("erosion-trust-degraded")
    return out


def build_terrace_erosion_overlays(
    terrace_erosion_audit: dict[str, Any],
    terrace_erosion_recommendations: dict[str, Any],
    terrace_erosion_map: dict[str, Any],
    orthodoxy_pressure_report: dict[str, Any],
    renewal_corridor_registry_bridge: dict[str, Any],
    epochal_transition_forecast: dict[str, Any],
    epoch_dashboard: dict[str, Any],
    delta_dashboard: dict[str, Any],
    knowledge_river_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    trust_surface_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "terrace_erosion_audit": _extract_required_provenance("terrace_erosion_audit", terrace_erosion_audit),
        "terrace_erosion_recommendations": _extract_required_provenance("terrace_erosion_recommendations", terrace_erosion_recommendations),
        "terrace_erosion_map": _extract_required_provenance("terrace_erosion_map", terrace_erosion_map),
        "orthodoxy_pressure_report": _extract_required_provenance("orthodoxy_pressure_report", orthodoxy_pressure_report),
        "renewal_corridor_registry": _extract_required_provenance("renewal_corridor_registry", renewal_corridor_registry_bridge),
        "epochal_transition_forecast": _extract_required_provenance("epochal_transition_forecast", epochal_transition_forecast),
    }

    for name, artifact in {
        "epoch_dashboard": epoch_dashboard,
        "delta_dashboard": delta_dashboard,
        "knowledge_river_dashboard": knowledge_river_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "trust_surface_dashboard": trust_surface_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [e for e in as_list(terrace_erosion_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(terrace_erosion_recommendations.get("recommendations")) if isinstance(e, dict)]
    erosion_entries = [e for e in as_list(terrace_erosion_map.get("entries")) if isinstance(e, dict)]
    orth_entries = [e for e in as_list(orthodoxy_pressure_report.get("entries")) if isinstance(e, dict)]
    renew_entries = [e for e in as_list(renewal_corridor_registry_bridge.get("entries")) if isinstance(e, dict)]
    forecast_entries = [e for e in as_list(epochal_transition_forecast.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    erosion_by = _index_by_key(erosion_entries, "reviewId")
    orth_by = _index_by_key(orth_entries, "reviewId")
    renew_by = _index_by_key(renew_entries, "reviewId")
    forecast_by = _index_by_key(forecast_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    renewal_registry_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        er = erosion_by.get(review_id, {})
        op = orth_by.get(review_id, {})
        rn = renew_by.get(review_id, {})
        fc = forecast_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        erosion_status = str(er.get("erosionStatus", rec.get("erosionStatus", "monitor")))
        erosion_class = str(er.get("erosionClass", rec.get("erosionClass", "bounded"))).lower()
        orthodoxy_class = str(op.get("orthodoxyClass", rec.get("orthodoxyClass", "bounded"))).lower()
        renewal_class = str(rn.get("renewalClass", rec.get("renewalClass", "bounded"))).lower()
        plurality_collapse_recovery = str(fc.get("pluralityCollapseRecovery", rec.get("pluralityCollapseRecovery", "bounded"))).lower()
        trust_erosion = str(fc.get("trustErosion", rec.get("trustErosion", "bounded"))).lower()
        memory_reactivation = str(fc.get("memoryReactivation", rec.get("memoryReactivation", "bounded"))).lower()
        phase_transition_likelihood = _to_float(fc.get("phaseTransitionLikelihood", rec.get("phaseTransitionLikelihood", 0.0)))
        provenance_markers = [str(v) for v in as_list(fc.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(fc.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(erosion_class, orthodoxy_class, renewal_class, plurality_collapse_recovery, trust_degraded)

        base = {
            "reviewId": review_id,
            "erosionStatus": erosion_status,
            "erosionClass": erosion_class,
            "orthodoxyClass": orthodoxy_class,
            "renewalClass": renewal_class,
            "pluralityCollapseRecovery": plurality_collapse_recovery,
            "trustErosion": trust_erosion,
            "memoryReactivation": memory_reactivation,
            "phaseTransitionLikelihood": phase_transition_likelihood,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "terraceErosionAuditState": str(au.get("terraceErosionAuditState", rec.get("terraceErosionAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            renewal_registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({**base, "status": "watch", "queuedAt": generated_at})

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "noCanonMutation": True,
            "noDeploymentExecution": True,
            "noGovernanceRightMutation": True,
            "noRankingOfCivilizationsInstitutionsSuccessorOrders": True,
            "erosionNotCollapseCertainty": True,
            "noNewAgeConfirmedPresentation": True,
            "noTheoryCompetitionClosure": True,
        })

    shared = {
        "generatedAt": generated_at,
        "terraceErosionProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfCivilizationsInstitutionsSuccessorOrders": True,
        "erosionNotCollapseCertainty": True,
        "noNewAgeConfirmedPresentation": True,
        "noTheoryCompetitionClosure": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsErosionRenewalMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    terrace_health_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    orthodoxy_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    renewal_corridor_registry = {**shared, "entries": sorted(renewal_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    epoch_transition_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (terrace_health_dashboard, "entries"),
        (orthodoxy_watchlist, "entries"),
        (renewal_corridor_registry, "entries"),
        (epoch_transition_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for k in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(k), bool):
                raise ValueError(f"{k} must be a boolean")

    return terrace_health_dashboard, orthodoxy_watchlist, renewal_corridor_registry, epoch_transition_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--terrace-erosion-audit", type=Path, default=Path("bridge/terrace_erosion_audit.json"))
    p.add_argument("--terrace-erosion-recommendations", type=Path, default=Path("bridge/terrace_erosion_recommendations.json"))
    p.add_argument("--terrace-erosion-map", type=Path, default=Path("bridge/terrace_erosion_map.json"))
    p.add_argument("--orthodoxy-pressure-report", type=Path, default=Path("bridge/orthodoxy_pressure_report.json"))
    p.add_argument("--renewal-corridor-registry", type=Path, default=Path("bridge/renewal_corridor_registry.json"))
    p.add_argument("--epochal-transition-forecast", type=Path, default=Path("bridge/epochal_transition_forecast.json"))

    p.add_argument("--epoch-dashboard", type=Path, default=Path("registry/epoch_dashboard.json"))
    p.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    p.add_argument("--knowledge-river-dashboard", type=Path, default=Path("registry/knowledge_river_dashboard.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    p.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-terrace-health-dashboard", type=Path, default=Path("registry/terrace_health_dashboard.json"))
    p.add_argument("--out-orthodoxy-watchlist", type=Path, default=Path("registry/orthodoxy_watchlist.json"))
    p.add_argument("--out-renewal-corridor-registry", type=Path, default=Path("registry/renewal_corridor_registry.json"))
    p.add_argument("--out-epoch-transition-annotations", type=Path, default=Path("registry/epoch_transition_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_terrace_erosion_overlays(
            load_required_json(args.terrace_erosion_audit),
            load_required_json(args.terrace_erosion_recommendations),
            load_required_json(args.terrace_erosion_map),
            load_required_json(args.orthodoxy_pressure_report),
            load_required_json(args.renewal_corridor_registry),
            load_required_json(args.epochal_transition_forecast),
            load_required_json(args.epoch_dashboard),
            load_required_json(args.delta_dashboard),
            load_required_json(args.knowledge_river_dashboard),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.commons_sovereignty_dashboard),
            load_required_json(args.trust_surface_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    for out in (
        args.out_terrace_health_dashboard,
        args.out_orthodoxy_watchlist,
        args.out_renewal_corridor_registry,
        args.out_epoch_transition_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_terrace_health_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_orthodoxy_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_renewal_corridor_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_epoch_transition_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote terrace health dashboard: {args.out_terrace_health_dashboard}")
    print(f"[OK] Wrote orthodoxy watchlist: {args.out_orthodoxy_watchlist}")
    print(f"[OK] Wrote renewal corridor registry: {args.out_renewal_corridor_registry}")
    print(f"[OK] Wrote epoch transition annotations: {args.out_epoch_transition_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
