#!/usr/bin/env python3
"""Build successor-crossing and false-future-decay overlays.

Publisher surfaces only Sophia-audited successor-crossing materials; it does not
declare new epochs, certify futures, or authorize institutional succession.
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
    "crossing-threshold-review",
    "decay-coherence-loss",
    "viability-conditional",
    "plurality-retained",
    "crossing-trust-degraded",
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


def _atlas_classes(crossing_class: str, decay_class: str, gate_status: str, plurality_retention: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if crossing_class in {"threshold", "review", "bounded", "conditional"}:
        out.append("crossing-threshold-review")
    if decay_class in {"drift", "erosive", "collapse", "coherence-loss", "elevated"}:
        out.append("decay-coherence-loss")
    if gate_status in {"review", "pending", "guarded", "bounded", "blocked"}:
        out.append("viability-conditional")
    if plurality_retention in {"retained", "preserved", "bounded", "recovering"}:
        out.append("plurality-retained")
    if trust_degraded:
        out.append("crossing-trust-degraded")
    return out


def build_successor_crossing_overlays(
    successor_crossing_audit: dict[str, Any],
    successor_crossing_recommendations: dict[str, Any],
    successor_crossing_map: dict[str, Any],
    false_future_decay_report: dict[str, Any],
    delta_crossing_gate: dict[str, Any],
    future_viability_forecast: dict[str, Any],
    successor_maturation_dashboard: dict[str, Any],
    false_future_watchlist: dict[str, Any],
    plurality_retention_registry: dict[str, Any],
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
        "successor_crossing_audit": _extract_required_provenance("successor_crossing_audit", successor_crossing_audit),
        "successor_crossing_recommendations": _extract_required_provenance("successor_crossing_recommendations", successor_crossing_recommendations),
        "successor_crossing_map": _extract_required_provenance("successor_crossing_map", successor_crossing_map),
        "false_future_decay_report": _extract_required_provenance("false_future_decay_report", false_future_decay_report),
        "delta_crossing_gate": _extract_required_provenance("delta_crossing_gate", delta_crossing_gate),
        "future_viability_forecast": _extract_required_provenance("future_viability_forecast", future_viability_forecast),
    }

    for name, artifact in {
        "successor_maturation_dashboard": successor_maturation_dashboard,
        "false_future_watchlist": false_future_watchlist,
        "plurality_retention_registry": plurality_retention_registry,
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

    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [e for e in as_list(successor_crossing_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(successor_crossing_recommendations.get("recommendations")) if isinstance(e, dict)]
    crossing_entries = [e for e in as_list(successor_crossing_map.get("entries")) if isinstance(e, dict)]
    decay_entries = [e for e in as_list(false_future_decay_report.get("entries")) if isinstance(e, dict)]
    gate_entries = [e for e in as_list(delta_crossing_gate.get("entries")) if isinstance(e, dict)]
    viability_entries = [e for e in as_list(future_viability_forecast.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    crossing_by = _index_by_key(crossing_entries, "reviewId")
    decay_by = _index_by_key(decay_entries, "reviewId")
    gate_by = _index_by_key(gate_entries, "reviewId")
    viability_by = _index_by_key(viability_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    gate_registry_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        cr = crossing_by.get(review_id, {})
        de = decay_by.get(review_id, {})
        ga = gate_by.get(review_id, {})
        vi = viability_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        crossing_status = str(cr.get("crossingStatus", rec.get("crossingStatus", "under_review")))
        crossing_class = str(cr.get("crossingClass", rec.get("crossingClass", "bounded"))).lower()
        decay_class = str(de.get("decayClass", rec.get("decayClass", "bounded"))).lower()
        gate_status = str(ga.get("gateStatus", rec.get("gateStatus", "review"))).lower()
        viability_score = _to_float(vi.get("viabilityScore", rec.get("viabilityScore", 0.0)))
        trust_legibility = str(vi.get("trustLegibility", rec.get("trustLegibility", "bounded"))).lower()
        memory_continuity = str(vi.get("memoryContinuity", rec.get("memoryContinuity", "bounded"))).lower()
        plurality_retention = str(vi.get("pluralityRetention", rec.get("pluralityRetention", "bounded"))).lower()
        capture_exposure = str(de.get("captureExposure", rec.get("captureExposure", "bounded"))).lower()
        provenance_markers = [str(v) for v in as_list(vi.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(vi.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(crossing_class, decay_class, gate_status, plurality_retention, trust_degraded)

        base = {
            "reviewId": review_id,
            "crossingStatus": crossing_status,
            "crossingClass": crossing_class,
            "decayClass": decay_class,
            "gateStatus": gate_status,
            "viabilityScore": viability_score,
            "trustLegibility": trust_legibility,
            "memoryContinuity": memory_continuity,
            "pluralityRetention": plurality_retention,
            "captureExposure": capture_exposure,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "crossingAuditState": str(au.get("crossingAuditState", rec.get("crossingAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            gate_registry_entries.append({**base, "updatedAt": generated_at})

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
                "crossingVisibilityNotLegitimateAuthority": True,
                "noTheoryCompetitionClosure": True,
                "noNewAgeConfirmedOrFutureSecuredPresentation": True,
            }
        )

    shared = {
        "generatedAt": generated_at,
        "successorCrossingProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions": True,
        "crossingVisibilityNotLegitimateAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noNewAgeConfirmedOrFutureSecuredPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsSuccessorCrossingMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    successor_crossing_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    false_future_decay_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    delta_gate_registry = {**shared, "entries": sorted(gate_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    future_crossing_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (successor_crossing_dashboard, "entries"),
        (false_future_decay_watchlist, "entries"),
        (delta_gate_registry, "entries"),
        (future_crossing_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return successor_crossing_dashboard, false_future_decay_watchlist, delta_gate_registry, future_crossing_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--successor-crossing-audit", type=Path, default=Path("bridge/successor_crossing_audit.json"))
    p.add_argument("--successor-crossing-recommendations", type=Path, default=Path("bridge/successor_crossing_recommendations.json"))
    p.add_argument("--successor-crossing-map", type=Path, default=Path("bridge/successor_crossing_map.json"))
    p.add_argument("--false-future-decay-report", type=Path, default=Path("bridge/false_future_decay_report.json"))
    p.add_argument("--delta-crossing-gate", type=Path, default=Path("bridge/delta_crossing_gate.json"))
    p.add_argument("--future-viability-forecast", type=Path, default=Path("bridge/future_viability_forecast.json"))

    p.add_argument("--successor-maturation-dashboard", type=Path, default=Path("registry/successor_maturation_dashboard.json"))
    p.add_argument("--false-future-watchlist", type=Path, default=Path("registry/false_future_watchlist.json"))
    p.add_argument("--plurality-retention-registry", type=Path, default=Path("registry/plurality_retention_registry.json"))
    p.add_argument("--renewal-braid-dashboard", type=Path, default=Path("registry/renewal_braid_dashboard.json"))
    p.add_argument("--terrace-health-dashboard", type=Path, default=Path("registry/terrace_health_dashboard.json"))
    p.add_argument("--epoch-dashboard", type=Path, default=Path("registry/epoch_dashboard.json"))
    p.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    p.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-successor-crossing-dashboard", type=Path, default=Path("registry/successor_crossing_dashboard.json"))
    p.add_argument("--out-false-future-decay-watchlist", type=Path, default=Path("registry/false_future_decay_watchlist.json"))
    p.add_argument("--out-delta-gate-registry", type=Path, default=Path("registry/delta_gate_registry.json"))
    p.add_argument("--out-future-crossing-annotations", type=Path, default=Path("registry/future_crossing_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_successor_crossing_overlays(
            load_required_json(args.successor_crossing_audit),
            load_required_json(args.successor_crossing_recommendations),
            load_required_json(args.successor_crossing_map),
            load_required_json(args.false_future_decay_report),
            load_required_json(args.delta_crossing_gate),
            load_required_json(args.future_viability_forecast),
            load_required_json(args.successor_maturation_dashboard),
            load_required_json(args.false_future_watchlist),
            load_required_json(args.plurality_retention_registry),
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
        args.out_successor_crossing_dashboard,
        args.out_false_future_decay_watchlist,
        args.out_delta_gate_registry,
        args.out_future_crossing_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_successor_crossing_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_false_future_decay_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_delta_gate_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_future_crossing_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote successor crossing dashboard: {args.out_successor_crossing_dashboard}")
    print(f"[OK] Wrote false future decay watchlist: {args.out_false_future_decay_watchlist}")
    print(f"[OK] Wrote delta gate registry: {args.out_delta_gate_registry}")
    print(f"[OK] Wrote future crossing annotations: {args.out_future_crossing_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
