#!/usr/bin/env python3
"""Build new-delta stabilization and fragmented-renewal reversion overlays.

Publisher surfaces only Sophia-audited post-crossing stabilization materials;
it does not declare new epochs, certify successor governance, or authorize
institutional succession.
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
    "stabilization-reviewable",
    "reversion-fragmented",
    "resilience-conditional",
    "plurality-retained",
    "post-crossing-trust-degraded",
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


def _atlas_classes(stabilization_class: str, reversion_class: str, resilience_class: str, plurality_retention: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if stabilization_class in {"durable", "reviewable", "bounded", "conditional", "stabilizing"}:
        out.append("stabilization-reviewable")
    if reversion_class in {"fragmented", "scatter", "erosive", "regressive", "elevated"}:
        out.append("reversion-fragmented")
    if resilience_class in {"conditional", "guarded", "bounded", "recovering", "stressed"}:
        out.append("resilience-conditional")
    if plurality_retention in {"retained", "preserved", "bounded", "recovering"}:
        out.append("plurality-retained")
    if trust_degraded:
        out.append("post-crossing-trust-degraded")
    return out


def build_new_delta_stabilization_overlays(
    new_delta_stabilization_audit: dict[str, Any],
    new_delta_stabilization_recommendations: dict[str, Any],
    new_delta_stabilization_map: dict[str, Any],
    fragmented_renewal_reversion_report: dict[str, Any],
    crossing_resilience_scorecard: dict[str, Any],
    post_crossing_governance_gate: dict[str, Any],
    successor_crossing_dashboard: dict[str, Any],
    false_future_decay_watchlist: dict[str, Any],
    delta_gate_registry: dict[str, Any],
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
        "new_delta_stabilization_audit": _extract_required_provenance("new_delta_stabilization_audit", new_delta_stabilization_audit),
        "new_delta_stabilization_recommendations": _extract_required_provenance("new_delta_stabilization_recommendations", new_delta_stabilization_recommendations),
        "new_delta_stabilization_map": _extract_required_provenance("new_delta_stabilization_map", new_delta_stabilization_map),
        "fragmented_renewal_reversion_report": _extract_required_provenance("fragmented_renewal_reversion_report", fragmented_renewal_reversion_report),
        "crossing_resilience_scorecard": _extract_required_provenance("crossing_resilience_scorecard", crossing_resilience_scorecard),
        "post_crossing_governance_gate": _extract_required_provenance("post_crossing_governance_gate", post_crossing_governance_gate),
    }

    for name, artifact in {
        "successor_crossing_dashboard": successor_crossing_dashboard,
        "false_future_decay_watchlist": false_future_decay_watchlist,
        "delta_gate_registry": delta_gate_registry,
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

    audits = [e for e in as_list(new_delta_stabilization_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(new_delta_stabilization_recommendations.get("recommendations")) if isinstance(e, dict)]
    stabilization_entries = [e for e in as_list(new_delta_stabilization_map.get("entries")) if isinstance(e, dict)]
    reversion_entries = [e for e in as_list(fragmented_renewal_reversion_report.get("entries")) if isinstance(e, dict)]
    resilience_entries = [e for e in as_list(crossing_resilience_scorecard.get("entries")) if isinstance(e, dict)]
    gate_entries = [e for e in as_list(post_crossing_governance_gate.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    stabilization_by = _index_by_key(stabilization_entries, "reviewId")
    reversion_by = _index_by_key(reversion_entries, "reviewId")
    resilience_by = _index_by_key(resilience_entries, "reviewId")
    gate_by = _index_by_key(gate_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    resilience_registry_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        st = stabilization_by.get(review_id, {})
        rv = reversion_by.get(review_id, {})
        rs = resilience_by.get(review_id, {})
        ga = gate_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        stabilization_status = str(st.get("stabilizationStatus", rec.get("stabilizationStatus", "under_review")))
        stabilization_class = str(st.get("stabilizationClass", rec.get("stabilizationClass", "bounded"))).lower()
        reversion_class = str(rv.get("reversionClass", rec.get("reversionClass", "bounded"))).lower()
        resilience_class = str(rs.get("resilienceClass", rec.get("resilienceClass", "conditional"))).lower()
        gate_status = str(ga.get("gateStatus", rec.get("gateStatus", "review"))).lower()
        trust_legibility = str(rs.get("trustLegibility", rec.get("trustLegibility", "bounded"))).lower()
        memory_continuity = str(rs.get("memoryContinuity", rec.get("memoryContinuity", "bounded"))).lower()
        plurality_retention = str(rs.get("pluralityRetention", rec.get("pluralityRetention", "bounded"))).lower()
        renewal_scatter = _to_float(rv.get("renewalScatter", rec.get("renewalScatter", 0.0)))
        provenance_markers = [str(v) for v in as_list(rs.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(rs.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(stabilization_class, reversion_class, resilience_class, plurality_retention, trust_degraded)

        base = {
            "reviewId": review_id,
            "stabilizationStatus": stabilization_status,
            "stabilizationClass": stabilization_class,
            "reversionClass": reversion_class,
            "resilienceClass": resilience_class,
            "gateStatus": gate_status,
            "trustLegibility": trust_legibility,
            "memoryContinuity": memory_continuity,
            "pluralityRetention": plurality_retention,
            "renewalScatter": renewal_scatter,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "stabilizationAuditState": str(au.get("stabilizationAuditState", rec.get("stabilizationAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            resilience_registry_entries.append({**base, "updatedAt": generated_at})

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
                "stabilizationVisibilityNotLegitimateAuthority": True,
                "noTheoryCompetitionClosure": True,
                "noNewAgeConfirmedOrFutureSecuredPermanentlyPresentation": True,
            }
        )

    shared = {
        "generatedAt": generated_at,
        "newDeltaStabilizationProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions": True,
        "stabilizationVisibilityNotLegitimateAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noNewAgeConfirmedOrFutureSecuredPermanentlyPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsPostCrossingStabilizationMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    new_delta_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    reversion_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    crossing_resilience_registry = {**shared, "entries": sorted(resilience_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    post_crossing_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (new_delta_dashboard, "entries"),
        (reversion_watchlist, "entries"),
        (crossing_resilience_registry, "entries"),
        (post_crossing_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return new_delta_dashboard, reversion_watchlist, crossing_resilience_registry, post_crossing_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--new-delta-stabilization-audit", type=Path, default=Path("bridge/new_delta_stabilization_audit.json"))
    p.add_argument("--new-delta-stabilization-recommendations", type=Path, default=Path("bridge/new_delta_stabilization_recommendations.json"))
    p.add_argument("--new-delta-stabilization-map", type=Path, default=Path("bridge/new_delta_stabilization_map.json"))
    p.add_argument("--fragmented-renewal-reversion-report", type=Path, default=Path("bridge/fragmented_renewal_reversion_report.json"))
    p.add_argument("--crossing-resilience-scorecard", type=Path, default=Path("bridge/crossing_resilience_scorecard.json"))
    p.add_argument("--post-crossing-governance-gate", type=Path, default=Path("bridge/post_crossing_governance_gate.json"))

    p.add_argument("--successor-crossing-dashboard", type=Path, default=Path("registry/successor_crossing_dashboard.json"))
    p.add_argument("--false-future-decay-watchlist", type=Path, default=Path("registry/false_future_decay_watchlist.json"))
    p.add_argument("--delta-gate-registry", type=Path, default=Path("registry/delta_gate_registry.json"))
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

    p.add_argument("--out-new-delta-dashboard", type=Path, default=Path("registry/new_delta_dashboard.json"))
    p.add_argument("--out-reversion-watchlist", type=Path, default=Path("registry/reversion_watchlist.json"))
    p.add_argument("--out-crossing-resilience-registry", type=Path, default=Path("registry/crossing_resilience_registry.json"))
    p.add_argument("--out-post-crossing-annotations", type=Path, default=Path("registry/post_crossing_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_new_delta_stabilization_overlays(
            load_required_json(args.new_delta_stabilization_audit),
            load_required_json(args.new_delta_stabilization_recommendations),
            load_required_json(args.new_delta_stabilization_map),
            load_required_json(args.fragmented_renewal_reversion_report),
            load_required_json(args.crossing_resilience_scorecard),
            load_required_json(args.post_crossing_governance_gate),
            load_required_json(args.successor_crossing_dashboard),
            load_required_json(args.false_future_decay_watchlist),
            load_required_json(args.delta_gate_registry),
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
        args.out_new_delta_dashboard,
        args.out_reversion_watchlist,
        args.out_crossing_resilience_registry,
        args.out_post_crossing_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_new_delta_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_reversion_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_crossing_resilience_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_post_crossing_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote new delta dashboard: {args.out_new_delta_dashboard}")
    print(f"[OK] Wrote reversion watchlist: {args.out_reversion_watchlist}")
    print(f"[OK] Wrote crossing resilience registry: {args.out_crossing_resilience_registry}")
    print(f"[OK] Wrote post crossing annotations: {args.out_post_crossing_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
