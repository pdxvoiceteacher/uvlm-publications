#!/usr/bin/env python3
"""Build successor maturation and false-future discrimination overlays.

Publisher surfaces only Sophia-audited successor-maturation materials; it does
not declare new epochs, certify futures, or authorize institutional succession.
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
    "maturation-bounded",
    "false-future-risk",
    "plurality-retained",
    "gate-review",
    "future-trust-degraded",
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


def _atlas_classes(maturation_class: str, false_future_class: str, plurality_class: str, gate_status: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if maturation_class in {"bounded", "stable", "reviewable", "emergent"}:
        out.append("maturation-bounded")
    if false_future_class in {"high", "simulated", "captured", "compressed", "elevated"}:
        out.append("false-future-risk")
    if plurality_class in {"retained", "preserved", "bounded", "recovery"}:
        out.append("plurality-retained")
    if gate_status in {"review", "pending", "bounded", "guarded"}:
        out.append("gate-review")
    if trust_degraded:
        out.append("future-trust-degraded")
    return out


def build_successor_maturation_overlays(
    successor_maturation_audit: dict[str, Any],
    successor_maturation_recommendations: dict[str, Any],
    successor_maturation_map: dict[str, Any],
    false_future_risk_report: dict[str, Any],
    plurality_retention_scorecard: dict[str, Any],
    maturation_gate_report: dict[str, Any],
    renewal_braid_dashboard: dict[str, Any],
    successor_delta_registry: dict[str, Any],
    terrace_health_dashboard: dict[str, Any],
    epoch_dashboard: dict[str, Any],
    delta_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    trust_surface_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "successor_maturation_audit": _extract_required_provenance("successor_maturation_audit", successor_maturation_audit),
        "successor_maturation_recommendations": _extract_required_provenance("successor_maturation_recommendations", successor_maturation_recommendations),
        "successor_maturation_map": _extract_required_provenance("successor_maturation_map", successor_maturation_map),
        "false_future_risk_report": _extract_required_provenance("false_future_risk_report", false_future_risk_report),
        "plurality_retention_scorecard": _extract_required_provenance("plurality_retention_scorecard", plurality_retention_scorecard),
        "maturation_gate_report": _extract_required_provenance("maturation_gate_report", maturation_gate_report),
    }

    for name, artifact in {
        "renewal_braid_dashboard": renewal_braid_dashboard,
        "successor_delta_registry": successor_delta_registry,
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

    audits = [e for e in as_list(successor_maturation_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(successor_maturation_recommendations.get("recommendations")) if isinstance(e, dict)]
    mat_entries = [e for e in as_list(successor_maturation_map.get("entries")) if isinstance(e, dict)]
    false_entries = [e for e in as_list(false_future_risk_report.get("entries")) if isinstance(e, dict)]
    plur_entries = [e for e in as_list(plurality_retention_scorecard.get("entries")) if isinstance(e, dict)]
    gate_entries = [e for e in as_list(maturation_gate_report.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    mat_by = _index_by_key(mat_entries, "reviewId")
    false_by = _index_by_key(false_entries, "reviewId")
    plur_by = _index_by_key(plur_entries, "reviewId")
    gate_by = _index_by_key(gate_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    plurality_registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        mm = mat_by.get(review_id, {})
        ff = false_by.get(review_id, {})
        pr = plur_by.get(review_id, {})
        gt = gate_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        maturation_status = str(mm.get("maturationStatus", rec.get("maturationStatus", "monitor")))
        maturation_class = str(mm.get("maturationClass", rec.get("maturationClass", "bounded"))).lower()
        false_future_class = str(ff.get("falseFutureClass", rec.get("falseFutureClass", "bounded"))).lower()
        plurality_retention_class = str(pr.get("pluralityRetentionClass", rec.get("pluralityRetentionClass", "bounded"))).lower()
        gate_status = str(gt.get("gateStatus", rec.get("gateStatus", "review"))).lower()
        trust_legibility = str(gt.get("trustLegibility", rec.get("trustLegibility", "bounded"))).lower()
        memory_continuity = str(gt.get("memoryContinuity", rec.get("memoryContinuity", "bounded"))).lower()
        successor_capture_risk = str(ff.get("successorCaptureRisk", rec.get("successorCaptureRisk", "bounded"))).lower()
        gate_score = _to_float(gt.get("gateScore", rec.get("gateScore", 0.0)))
        provenance_markers = [str(v) for v in as_list(gt.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(gt.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(
            maturation_class,
            false_future_class,
            plurality_retention_class,
            gate_status,
            trust_degraded,
        )

        base = {
            "reviewId": review_id,
            "maturationStatus": maturation_status,
            "maturationClass": maturation_class,
            "falseFutureClass": false_future_class,
            "pluralityRetentionClass": plurality_retention_class,
            "gateStatus": gate_status,
            "trustLegibility": trust_legibility,
            "memoryContinuity": memory_continuity,
            "successorCaptureRisk": successor_capture_risk,
            "gateScore": gate_score,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "successorMaturationAuditState": str(au.get("successorMaturationAuditState", rec.get("successorMaturationAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            plurality_registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({**base, "status": "watch", "queuedAt": generated_at})

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "noCanonMutation": True,
            "noDeploymentExecution": True,
            "noGovernanceRightMutation": True,
            "noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions": True,
            "maturationVisibilityNotLegitimateAuthority": True,
            "noTheoryCompetitionClosure": True,
            "noNewAgeConfirmedOrFutureSecuredPresentation": True,
        })

    shared = {
        "generatedAt": generated_at,
        "successorMaturationProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions": True,
        "maturationVisibilityNotLegitimateAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noNewAgeConfirmedOrFutureSecuredPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsSuccessorMaturationMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    successor_maturation_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    false_future_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    plurality_retention_registry = {**shared, "entries": sorted(plurality_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    future_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (successor_maturation_dashboard, "entries"),
        (false_future_watchlist, "entries"),
        (plurality_retention_registry, "entries"),
        (future_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return successor_maturation_dashboard, false_future_watchlist, plurality_retention_registry, future_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--successor-maturation-audit", type=Path, default=Path("bridge/successor_maturation_audit.json"))
    p.add_argument("--successor-maturation-recommendations", type=Path, default=Path("bridge/successor_maturation_recommendations.json"))
    p.add_argument("--successor-maturation-map", type=Path, default=Path("bridge/successor_maturation_map.json"))
    p.add_argument("--false-future-risk-report", type=Path, default=Path("bridge/false_future_risk_report.json"))
    p.add_argument("--plurality-retention-scorecard", type=Path, default=Path("bridge/plurality_retention_scorecard.json"))
    p.add_argument("--maturation-gate-report", type=Path, default=Path("bridge/maturation_gate_report.json"))

    p.add_argument("--renewal-braid-dashboard", type=Path, default=Path("registry/renewal_braid_dashboard.json"))
    p.add_argument("--successor-delta-registry", type=Path, default=Path("registry/successor_delta_registry.json"))
    p.add_argument("--terrace-health-dashboard", type=Path, default=Path("registry/terrace_health_dashboard.json"))
    p.add_argument("--epoch-dashboard", type=Path, default=Path("registry/epoch_dashboard.json"))
    p.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    p.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-successor-maturation-dashboard", type=Path, default=Path("registry/successor_maturation_dashboard.json"))
    p.add_argument("--out-false-future-watchlist", type=Path, default=Path("registry/false_future_watchlist.json"))
    p.add_argument("--out-plurality-retention-registry", type=Path, default=Path("registry/plurality_retention_registry.json"))
    p.add_argument("--out-future-annotations", type=Path, default=Path("registry/future_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_successor_maturation_overlays(
            load_required_json(args.successor_maturation_audit),
            load_required_json(args.successor_maturation_recommendations),
            load_required_json(args.successor_maturation_map),
            load_required_json(args.false_future_risk_report),
            load_required_json(args.plurality_retention_scorecard),
            load_required_json(args.maturation_gate_report),
            load_required_json(args.renewal_braid_dashboard),
            load_required_json(args.successor_delta_registry),
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
        args.out_successor_maturation_dashboard,
        args.out_false_future_watchlist,
        args.out_plurality_retention_registry,
        args.out_future_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_successor_maturation_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_false_future_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_plurality_retention_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_future_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote successor maturation dashboard: {args.out_successor_maturation_dashboard}")
    print(f"[OK] Wrote false future watchlist: {args.out_false_future_watchlist}")
    print(f"[OK] Wrote plurality retention registry: {args.out_plurality_retention_registry}")
    print(f"[OK] Wrote future annotations: {args.out_future_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
