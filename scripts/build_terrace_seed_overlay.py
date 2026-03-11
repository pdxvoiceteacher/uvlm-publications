#!/usr/bin/env python3
"""Build terrace-seed formation and experimental repluralization overlays.

Publisher surfaces only Sophia-audited terrace-seed materials; it does not
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
    "terrace-seed-reviewable",
    "repluralization-open",
    "sedimentation-readiness-conditional",
    "plurality-durable",
    "terrace-seed-trust-degraded",
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


def _atlas_classes(seed_class: str, repluralization_class: str, readiness_class: str, plurality_durability: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if seed_class in {"early", "sedimenting", "reviewable", "bounded", "conditional"}:
        out.append("terrace-seed-reviewable")
    if repluralization_class in {"reopened", "experimental", "healthy", "recovering", "bounded"}:
        out.append("repluralization-open")
    if readiness_class in {"conditional", "guarded", "bounded", "forming", "review"}:
        out.append("sedimentation-readiness-conditional")
    if plurality_durability in {"durable", "retained", "preserved", "bounded", "recovering"}:
        out.append("plurality-durable")
    if trust_degraded:
        out.append("terrace-seed-trust-degraded")
    return out


def build_terrace_seed_overlays(
    terrace_seed_audit: dict[str, Any],
    terrace_seed_recommendations: dict[str, Any],
    terrace_seed_map: dict[str, Any],
    experimental_repluralization_report: dict[str, Any],
    sedimentation_readiness_scorecard: dict[str, Any],
    terrace_seed_gate: dict[str, Any],
    new_delta_dashboard: dict[str, Any],
    reversion_watchlist: dict[str, Any],
    crossing_resilience_registry: dict[str, Any],
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
        "terrace_seed_audit": _extract_required_provenance("terrace_seed_audit", terrace_seed_audit),
        "terrace_seed_recommendations": _extract_required_provenance("terrace_seed_recommendations", terrace_seed_recommendations),
        "terrace_seed_map": _extract_required_provenance("terrace_seed_map", terrace_seed_map),
        "experimental_repluralization_report": _extract_required_provenance("experimental_repluralization_report", experimental_repluralization_report),
        "sedimentation_readiness_scorecard": _extract_required_provenance("sedimentation_readiness_scorecard", sedimentation_readiness_scorecard),
        "terrace_seed_gate": _extract_required_provenance("terrace_seed_gate", terrace_seed_gate),
    }

    for name, artifact in {
        "new_delta_dashboard": new_delta_dashboard,
        "reversion_watchlist": reversion_watchlist,
        "crossing_resilience_registry": crossing_resilience_registry,
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

    audits = [e for e in as_list(terrace_seed_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(terrace_seed_recommendations.get("recommendations")) if isinstance(e, dict)]
    seed_entries = [e for e in as_list(terrace_seed_map.get("entries")) if isinstance(e, dict)]
    repluralization_entries = [e for e in as_list(experimental_repluralization_report.get("entries")) if isinstance(e, dict)]
    readiness_entries = [e for e in as_list(sedimentation_readiness_scorecard.get("entries")) if isinstance(e, dict)]
    gate_entries = [e for e in as_list(terrace_seed_gate.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    seed_by = _index_by_key(seed_entries, "reviewId")
    repluralization_by = _index_by_key(repluralization_entries, "reviewId")
    readiness_by = _index_by_key(readiness_entries, "reviewId")
    gate_by = _index_by_key(gate_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    readiness_registry_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        se = seed_by.get(review_id, {})
        rp = repluralization_by.get(review_id, {})
        rd = readiness_by.get(review_id, {})
        ga = gate_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        seed_status = str(se.get("seedStatus", rec.get("seedStatus", "under_review")))
        terrace_seed_class = str(se.get("terraceSeedClass", rec.get("terraceSeedClass", "bounded"))).lower()
        repluralization_class = str(rp.get("repluralizationClass", rec.get("repluralizationClass", "bounded"))).lower()
        readiness_class = str(rd.get("readinessClass", rec.get("readinessClass", "conditional"))).lower()
        gate_status = str(ga.get("gateStatus", rec.get("gateStatus", "review"))).lower()
        trust_stability = str(rd.get("trustStability", rec.get("trustStability", "bounded"))).lower()
        memory_teachability = str(rd.get("memoryTeachability", rec.get("memoryTeachability", "bounded"))).lower()
        plurality_durability = str(rd.get("pluralityDurability", rec.get("pluralityDurability", "bounded"))).lower()
        experimentation_recovery = _to_float(rp.get("experimentationRecovery", rec.get("experimentationRecovery", 0.0)))
        provenance_markers = [str(v) for v in as_list(rd.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(rd.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(terrace_seed_class, repluralization_class, readiness_class, plurality_durability, trust_degraded)

        base = {
            "reviewId": review_id,
            "seedStatus": seed_status,
            "terraceSeedClass": terrace_seed_class,
            "repluralizationClass": repluralization_class,
            "readinessClass": readiness_class,
            "gateStatus": gate_status,
            "trustStability": trust_stability,
            "memoryTeachability": memory_teachability,
            "pluralityDurability": plurality_durability,
            "experimentationRecovery": experimentation_recovery,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "terraceSeedAuditState": str(au.get("terraceSeedAuditState", rec.get("terraceSeedAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            readiness_registry_entries.append({**base, "updatedAt": generated_at})

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
                "seedVisibilityNotSettledAuthority": True,
                "noTheoryCompetitionClosure": True,
                "noNewAgeFormedOrFutureSecuredPermanentlyPresentation": True,
            }
        )

    shared = {
        "generatedAt": generated_at,
        "terraceSeedProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions": True,
        "seedVisibilityNotSettledAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noNewAgeFormedOrFutureSecuredPermanentlyPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsTerraceSeedMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    terrace_seed_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    repluralization_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    sedimentation_readiness_registry = {**shared, "entries": sorted(readiness_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    terrace_seed_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (terrace_seed_dashboard, "entries"),
        (repluralization_watchlist, "entries"),
        (sedimentation_readiness_registry, "entries"),
        (terrace_seed_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return terrace_seed_dashboard, repluralization_watchlist, sedimentation_readiness_registry, terrace_seed_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--terrace-seed-audit", type=Path, default=Path("bridge/terrace_seed_audit.json"))
    p.add_argument("--terrace-seed-recommendations", type=Path, default=Path("bridge/terrace_seed_recommendations.json"))
    p.add_argument("--terrace-seed-map", type=Path, default=Path("bridge/terrace_seed_map.json"))
    p.add_argument("--experimental-repluralization-report", type=Path, default=Path("bridge/experimental_repluralization_report.json"))
    p.add_argument("--sedimentation-readiness-scorecard", type=Path, default=Path("bridge/sedimentation_readiness_scorecard.json"))
    p.add_argument("--terrace-seed-gate", type=Path, default=Path("bridge/terrace_seed_gate.json"))

    p.add_argument("--new-delta-dashboard", type=Path, default=Path("registry/new_delta_dashboard.json"))
    p.add_argument("--reversion-watchlist", type=Path, default=Path("registry/reversion_watchlist.json"))
    p.add_argument("--crossing-resilience-registry", type=Path, default=Path("registry/crossing_resilience_registry.json"))
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

    p.add_argument("--out-terrace-seed-dashboard", type=Path, default=Path("registry/terrace_seed_dashboard.json"))
    p.add_argument("--out-repluralization-watchlist", type=Path, default=Path("registry/repluralization_watchlist.json"))
    p.add_argument("--out-sedimentation-readiness-registry", type=Path, default=Path("registry/sedimentation_readiness_registry.json"))
    p.add_argument("--out-terrace-seed-annotations", type=Path, default=Path("registry/terrace_seed_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_terrace_seed_overlays(
            load_required_json(args.terrace_seed_audit),
            load_required_json(args.terrace_seed_recommendations),
            load_required_json(args.terrace_seed_map),
            load_required_json(args.experimental_repluralization_report),
            load_required_json(args.sedimentation_readiness_scorecard),
            load_required_json(args.terrace_seed_gate),
            load_required_json(args.new_delta_dashboard),
            load_required_json(args.reversion_watchlist),
            load_required_json(args.crossing_resilience_registry),
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
        args.out_terrace_seed_dashboard,
        args.out_repluralization_watchlist,
        args.out_sedimentation_readiness_registry,
        args.out_terrace_seed_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_terrace_seed_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_repluralization_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_sedimentation_readiness_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_terrace_seed_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote terrace seed dashboard: {args.out_terrace_seed_dashboard}")
    print(f"[OK] Wrote repluralization watchlist: {args.out_repluralization_watchlist}")
    print(f"[OK] Wrote sedimentation readiness registry: {args.out_sedimentation_readiness_registry}")
    print(f"[OK] Wrote terrace seed annotations: {args.out_terrace_seed_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
