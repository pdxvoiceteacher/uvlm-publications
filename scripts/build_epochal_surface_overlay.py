#!/usr/bin/env python3
"""Build epochal-surface emergence and reopened-experiment overlays.

Publisher surfaces only Sophia-audited epochal-surface materials; it does not
declare new epochs, certify settled futures, or authorize institutional
succession.
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
    "epochal-surface-reviewable",
    "habitable-plateau-conditional",
    "experiment-reopened",
    "plurality-durable",
    "epochal-surface-trust-degraded",
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


def _atlas_classes(surface_class: str, plateau_class: str, experiment_class: str, plurality_durability: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if surface_class in {"emergent", "reviewable", "bounded", "conditional", "living"}:
        out.append("epochal-surface-reviewable")
    if plateau_class in {"habitable", "conditional", "guarded", "bounded", "forming"}:
        out.append("habitable-plateau-conditional")
    if experiment_class in {"reopened", "active", "experimental", "recovering", "bounded"}:
        out.append("experiment-reopened")
    if plurality_durability in {"durable", "retained", "preserved", "bounded", "recovering"}:
        out.append("plurality-durable")
    if trust_degraded:
        out.append("epochal-surface-trust-degraded")
    return out


def build_epochal_surface_overlays(
    epochal_surface_audit: dict[str, Any],
    epochal_surface_recommendations: dict[str, Any],
    epochal_surface_map: dict[str, Any],
    habitable_plateau_report: dict[str, Any],
    reopened_experiment_registry: dict[str, Any],
    surface_emergence_gate: dict[str, Any],
    terrace_seed_dashboard: dict[str, Any],
    repluralization_watchlist: dict[str, Any],
    sedimentation_readiness_registry: dict[str, Any],
    new_delta_dashboard: dict[str, Any],
    successor_crossing_dashboard: dict[str, Any],
    successor_maturation_dashboard: dict[str, Any],
    renewal_braid_dashboard: dict[str, Any],
    terrace_health_dashboard: dict[str, Any],
    epoch_dashboard: dict[str, Any],
    delta_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    trust_surface_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    provenances: dict[str, dict[str, Any]] = {
        "epochal_surface_audit": _extract_required_provenance("epochal_surface_audit", epochal_surface_audit),
        "epochal_surface_recommendations": _extract_required_provenance("epochal_surface_recommendations", epochal_surface_recommendations),
        "epochal_surface_map": _extract_required_provenance("epochal_surface_map", epochal_surface_map),
        "habitable_plateau_report": _extract_required_provenance("habitable_plateau_report", habitable_plateau_report),
        "reopened_experiment_registry": _extract_required_provenance("reopened_experiment_registry", reopened_experiment_registry),
        "surface_emergence_gate": _extract_required_provenance("surface_emergence_gate", surface_emergence_gate),
    }

    for name, artifact in {
        "terrace_seed_dashboard": terrace_seed_dashboard,
        "repluralization_watchlist": repluralization_watchlist,
        "sedimentation_readiness_registry": sedimentation_readiness_registry,
        "new_delta_dashboard": new_delta_dashboard,
        "successor_crossing_dashboard": successor_crossing_dashboard,
        "successor_maturation_dashboard": successor_maturation_dashboard,
        "renewal_braid_dashboard": renewal_braid_dashboard,
        "terrace_health_dashboard": terrace_health_dashboard,
        "epoch_dashboard": epoch_dashboard,
        "delta_dashboard": delta_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "trust_surface_dashboard": trust_surface_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    integrity_status = evaluate_manifest_pair(
        bridge_canonical_integrity_manifest,
        registry_canonical_integrity_manifest,
    )

    audits = [e for e in as_list(epochal_surface_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(epochal_surface_recommendations.get("recommendations")) if isinstance(e, dict)]
    surface_entries = [e for e in as_list(epochal_surface_map.get("entries")) if isinstance(e, dict)]
    plateau_entries = [e for e in as_list(habitable_plateau_report.get("entries")) if isinstance(e, dict)]
    experiment_entries = [e for e in as_list(reopened_experiment_registry.get("entries")) if isinstance(e, dict)]
    gate_entries = [e for e in as_list(surface_emergence_gate.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    surface_by = _index_by_key(surface_entries, "reviewId")
    plateau_by = _index_by_key(plateau_entries, "reviewId")
    experiment_by = _index_by_key(experiment_entries, "reviewId")
    gate_by = _index_by_key(gate_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    plateau_registry_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        su = surface_by.get(review_id, {})
        pl = plateau_by.get(review_id, {})
        ex = experiment_by.get(review_id, {})
        ga = gate_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        surface_status = str(su.get("surfaceStatus", rec.get("surfaceStatus", "under_review")))
        surface_class = str(su.get("surfaceClass", rec.get("surfaceClass", "bounded"))).lower()
        plateau_class = str(pl.get("plateauClass", rec.get("plateauClass", "bounded"))).lower()
        experiment_class = str(ex.get("experimentClass", rec.get("experimentClass", "bounded"))).lower()
        gate_status = str(ga.get("gateStatus", rec.get("gateStatus", "review"))).lower()
        trust_stability = str(pl.get("trustStability", rec.get("trustStability", "bounded"))).lower()
        memory_teachability = str(pl.get("memoryTeachability", rec.get("memoryTeachability", "bounded"))).lower()
        plurality_durability = str(pl.get("pluralityDurability", rec.get("pluralityDurability", "bounded"))).lower()
        experimentation_recovery = _to_float(ex.get("experimentationRecovery", rec.get("experimentationRecovery", 0.0)))
        provenance_markers = [str(v) for v in as_list(pl.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(pl.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(surface_class, plateau_class, experiment_class, plurality_durability, trust_degraded)

        base = {
            "reviewId": review_id,
            "surfaceStatus": surface_status,
            "surfaceClass": surface_class,
            "plateauClass": plateau_class,
            "experimentClass": experiment_class,
            "gateStatus": gate_status,
            "trustStability": trust_stability,
            "memoryTeachability": memory_teachability,
            "pluralityDurability": plurality_durability,
            "experimentationRecovery": experimentation_recovery,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "epochalSurfaceAuditState": str(au.get("epochalSurfaceAuditState", rec.get("epochalSurfaceAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            plateau_registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({**base, "status": "watch", "queuedAt": generated_at})

        annotation_entries.append(
            {
                **base,
                "targetPublisherAction": action,
                "noCanonMutation": True,
                "noDeploymentExecution": True,
                "noGovernanceRightMutation": True,
                "noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions": True,
                "surfaceVisibilityNotSettledAuthority": True,
                "noTheoryCompetitionClosure": True,
                "noNewAgeFormedOrFutureSecuredPermanentlyPresentation": True,
            }
        )

    shared = {
        "generatedAt": generated_at,
        "epochalSurfaceProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions": True,
        "surfaceVisibilityNotSettledAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noNewAgeFormedOrFutureSecuredPermanentlyPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsEpochalSurfaceMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    epochal_surface_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    reopened_experiment_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    habitable_plateau_registry = {**shared, "entries": sorted(plateau_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    epochal_surface_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (epochal_surface_dashboard, "entries"),
        (reopened_experiment_watchlist, "entries"),
        (habitable_plateau_registry, "entries"),
        (epochal_surface_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return epochal_surface_dashboard, reopened_experiment_watchlist, habitable_plateau_registry, epochal_surface_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--epochal-surface-audit", type=Path, default=Path("bridge/epochal_surface_audit.json"))
    p.add_argument("--epochal-surface-recommendations", type=Path, default=Path("bridge/epochal_surface_recommendations.json"))
    p.add_argument("--epochal-surface-map", type=Path, default=Path("bridge/epochal_surface_map.json"))
    p.add_argument("--habitable-plateau-report", type=Path, default=Path("bridge/habitable_plateau_report.json"))
    p.add_argument("--reopened-experiment-registry", type=Path, default=Path("bridge/reopened_experiment_registry.json"))
    p.add_argument("--surface-emergence-gate", type=Path, default=Path("bridge/surface_emergence_gate.json"))

    p.add_argument("--terrace-seed-dashboard", type=Path, default=Path("registry/terrace_seed_dashboard.json"))
    p.add_argument("--repluralization-watchlist", type=Path, default=Path("registry/repluralization_watchlist.json"))
    p.add_argument("--sedimentation-readiness-registry", type=Path, default=Path("registry/sedimentation_readiness_registry.json"))
    p.add_argument("--new-delta-dashboard", type=Path, default=Path("registry/new_delta_dashboard.json"))
    p.add_argument("--successor-crossing-dashboard", type=Path, default=Path("registry/successor_crossing_dashboard.json"))
    p.add_argument("--successor-maturation-dashboard", type=Path, default=Path("registry/successor_maturation_dashboard.json"))
    p.add_argument("--renewal-braid-dashboard", type=Path, default=Path("registry/renewal_braid_dashboard.json"))
    p.add_argument("--terrace-health-dashboard", type=Path, default=Path("registry/terrace_health_dashboard.json"))
    p.add_argument("--epoch-dashboard", type=Path, default=Path("registry/epoch_dashboard.json"))
    p.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    p.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-epochal-surface-dashboard", type=Path, default=Path("registry/epochal_surface_dashboard.json"))
    p.add_argument("--out-reopened-experiment-watchlist", type=Path, default=Path("registry/reopened_experiment_watchlist.json"))
    p.add_argument("--out-habitable-plateau-registry", type=Path, default=Path("registry/habitable_plateau_registry.json"))
    p.add_argument("--out-epochal-surface-annotations", type=Path, default=Path("registry/epochal_surface_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_epochal_surface_overlays(
            load_required_json(args.epochal_surface_audit),
            load_required_json(args.epochal_surface_recommendations),
            load_required_json(args.epochal_surface_map),
            load_required_json(args.habitable_plateau_report),
            load_required_json(args.reopened_experiment_registry),
            load_required_json(args.surface_emergence_gate),
            load_required_json(args.terrace_seed_dashboard),
            load_required_json(args.repluralization_watchlist),
            load_required_json(args.sedimentation_readiness_registry),
            load_required_json(args.new_delta_dashboard),
            load_required_json(args.successor_crossing_dashboard),
            load_required_json(args.successor_maturation_dashboard),
            load_required_json(args.renewal_braid_dashboard),
            load_required_json(args.terrace_health_dashboard),
            load_required_json(args.epoch_dashboard),
            load_required_json(args.delta_dashboard),
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
        args.out_epochal_surface_dashboard,
        args.out_reopened_experiment_watchlist,
        args.out_habitable_plateau_registry,
        args.out_epochal_surface_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_epochal_surface_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_reopened_experiment_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_habitable_plateau_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_epochal_surface_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote epochal surface dashboard: {args.out_epochal_surface_dashboard}")
    print(f"[OK] Wrote reopened experiment watchlist: {args.out_reopened_experiment_watchlist}")
    print(f"[OK] Wrote habitable plateau registry: {args.out_habitable_plateau_registry}")
    print(f"[OK] Wrote epochal surface annotations: {args.out_epochal_surface_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
