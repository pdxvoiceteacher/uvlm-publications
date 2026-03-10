#!/usr/bin/env python3
"""Build successor-delta and renewal-braiding overlays.

Publisher surfaces only Sophia-audited successor-delta materials; it does not
declare new epochs, canonize successor orders, or authorize institutional transition.
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
    "successor-braid-active",
    "successor-plurality-recovery",
    "successor-capture-risk",
    "successor-transition-coupled",
    "successor-trust-degraded",
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


def _atlas_classes(braid_class: str, plurality_class: str, coupling_class: str, capture_risk: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if braid_class in {"active", "braided", "emergent", "bounded"}:
        out.append("successor-braid-active")
    if plurality_class in {"recovery", "preserved", "bounded"}:
        out.append("successor-plurality-recovery")
    if capture_risk in {"high", "elevated", "critical"}:
        out.append("successor-capture-risk")
    if coupling_class in {"coupled", "aligned", "bounded"}:
        out.append("successor-transition-coupled")
    if trust_degraded:
        out.append("successor-trust-degraded")
    return out


def build_successor_delta_overlays(
    successor_delta_audit: dict[str, Any],
    successor_delta_recommendations: dict[str, Any],
    renewal_braid_map: dict[str, Any],
    successor_delta_seed_report: dict[str, Any],
    plurality_recovery_registry_bridge: dict[str, Any],
    transition_coupling_report: dict[str, Any],
    terrace_health_dashboard: dict[str, Any],
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
        "successor_delta_audit": _extract_required_provenance("successor_delta_audit", successor_delta_audit),
        "successor_delta_recommendations": _extract_required_provenance("successor_delta_recommendations", successor_delta_recommendations),
        "renewal_braid_map": _extract_required_provenance("renewal_braid_map", renewal_braid_map),
        "successor_delta_seed_report": _extract_required_provenance("successor_delta_seed_report", successor_delta_seed_report),
        "plurality_recovery_registry": _extract_required_provenance("plurality_recovery_registry", plurality_recovery_registry_bridge),
        "transition_coupling_report": _extract_required_provenance("transition_coupling_report", transition_coupling_report),
    }

    for name, artifact in {
        "terrace_health_dashboard": terrace_health_dashboard,
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

    audits = [e for e in as_list(successor_delta_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(successor_delta_recommendations.get("recommendations")) if isinstance(e, dict)]
    braid_entries = [e for e in as_list(renewal_braid_map.get("entries")) if isinstance(e, dict)]
    seed_entries = [e for e in as_list(successor_delta_seed_report.get("entries")) if isinstance(e, dict)]
    plurality_entries = [e for e in as_list(plurality_recovery_registry_bridge.get("entries")) if isinstance(e, dict)]
    coupling_entries = [e for e in as_list(transition_coupling_report.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    braid_by = _index_by_key(braid_entries, "reviewId")
    seed_by = _index_by_key(seed_entries, "reviewId")
    plurality_by = _index_by_key(plurality_entries, "reviewId")
    coupling_by = _index_by_key(coupling_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        br = braid_by.get(review_id, {})
        sd = seed_by.get(review_id, {})
        pr = plurality_by.get(review_id, {})
        cp = coupling_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        successor_status = str(br.get("successorStatus", rec.get("successorStatus", "monitor")))
        braid_class = str(br.get("braidClass", rec.get("braidClass", "bounded"))).lower()
        successor_seed_class = str(sd.get("successorSeedClass", rec.get("successorSeedClass", "bounded"))).lower()
        plurality_class = str(pr.get("pluralityClass", rec.get("pluralityClass", "bounded"))).lower()
        transition_coupling_class = str(cp.get("transitionCouplingClass", rec.get("transitionCouplingClass", "bounded"))).lower()
        trust_repair = str(cp.get("trustRepair", rec.get("trustRepair", "bounded"))).lower()
        memory_reactivation = str(cp.get("memoryReactivation", rec.get("memoryReactivation", "bounded"))).lower()
        successor_capture_risk = str(cp.get("successorCaptureRisk", rec.get("successorCaptureRisk", "bounded"))).lower()
        coupling_score = _to_float(cp.get("couplingScore", rec.get("couplingScore", 0.0)))
        provenance_markers = [str(v) for v in as_list(cp.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(cp.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(
            braid_class,
            plurality_class,
            transition_coupling_class,
            successor_capture_risk,
            trust_degraded,
        )

        base = {
            "reviewId": review_id,
            "successorStatus": successor_status,
            "braidClass": braid_class,
            "successorSeedClass": successor_seed_class,
            "pluralityClass": plurality_class,
            "transitionCouplingClass": transition_coupling_class,
            "trustRepair": trust_repair,
            "memoryReactivation": memory_reactivation,
            "successorCaptureRisk": successor_capture_risk,
            "couplingScore": coupling_score,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "successorDeltaAuditState": str(au.get("successorDeltaAuditState", rec.get("successorDeltaAuditState", "none"))),
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
            "noRankingOfSuccessorOrdersCivilizationsInstitutionsCommunities": True,
            "successorVisibilityNotEpochAuthority": True,
            "noTheoryCompetitionClosure": True,
            "noNewAgeConfirmedPresentation": True,
        })

    shared = {
        "generatedAt": generated_at,
        "successorDeltaProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfSuccessorOrdersCivilizationsInstitutionsCommunities": True,
        "successorVisibilityNotEpochAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noNewAgeConfirmedPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsSuccessorDeltaMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    renewal_braid_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    successor_delta_registry = {**shared, "entries": sorted(registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    plurality_recovery_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    transition_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (renewal_braid_dashboard, "entries"),
        (successor_delta_registry, "entries"),
        (plurality_recovery_watchlist, "entries"),
        (transition_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return renewal_braid_dashboard, successor_delta_registry, plurality_recovery_watchlist, transition_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--successor-delta-audit", type=Path, default=Path("bridge/successor_delta_audit.json"))
    p.add_argument("--successor-delta-recommendations", type=Path, default=Path("bridge/successor_delta_recommendations.json"))
    p.add_argument("--renewal-braid-map", type=Path, default=Path("bridge/renewal_braid_map.json"))
    p.add_argument("--successor-delta-seed-report", type=Path, default=Path("bridge/successor_delta_seed_report.json"))
    p.add_argument("--plurality-recovery-registry", type=Path, default=Path("bridge/plurality_recovery_registry.json"))
    p.add_argument("--transition-coupling-report", type=Path, default=Path("bridge/transition_coupling_report.json"))

    p.add_argument("--terrace-health-dashboard", type=Path, default=Path("registry/terrace_health_dashboard.json"))
    p.add_argument("--epoch-dashboard", type=Path, default=Path("registry/epoch_dashboard.json"))
    p.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    p.add_argument("--knowledge-river-dashboard", type=Path, default=Path("registry/knowledge_river_dashboard.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    p.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-renewal-braid-dashboard", type=Path, default=Path("registry/renewal_braid_dashboard.json"))
    p.add_argument("--out-successor-delta-registry", type=Path, default=Path("registry/successor_delta_registry.json"))
    p.add_argument("--out-plurality-recovery-watchlist", type=Path, default=Path("registry/plurality_recovery_watchlist.json"))
    p.add_argument("--out-transition-annotations", type=Path, default=Path("registry/transition_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_successor_delta_overlays(
            load_required_json(args.successor_delta_audit),
            load_required_json(args.successor_delta_recommendations),
            load_required_json(args.renewal_braid_map),
            load_required_json(args.successor_delta_seed_report),
            load_required_json(args.plurality_recovery_registry),
            load_required_json(args.transition_coupling_report),
            load_required_json(args.terrace_health_dashboard),
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
        args.out_renewal_braid_dashboard,
        args.out_successor_delta_registry,
        args.out_plurality_recovery_watchlist,
        args.out_transition_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_renewal_braid_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_successor_delta_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_plurality_recovery_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_transition_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote renewal braid dashboard: {args.out_renewal_braid_dashboard}")
    print(f"[OK] Wrote successor delta registry: {args.out_successor_delta_registry}")
    print(f"[OK] Wrote plurality recovery watchlist: {args.out_plurality_recovery_watchlist}")
    print(f"[OK] Wrote transition annotations: {args.out_transition_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
