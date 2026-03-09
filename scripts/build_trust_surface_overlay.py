#!/usr/bin/env python3
"""Build trust surface and delegated access transparency overlays.

Phase BD exposes delegated-access and legitimacy surfaces for transparency and research only.
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
    "trust-surface-stable",
    "revocation-asymmetry",
    "legitimacy-risk",
    "wrapper-provenance-risk",
    "trust-compression-warning",
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
    if action == "suppressed":
        return "suppress"
    return action if action in {"docket", "watch", "suppress", "rejected"} else "watch"


def _classes(status: str, rev_asym: float, leg: float, compression: str, lineage: str) -> list[str]:
    out: list[str] = []
    if status in {"stable", "verified", "bounded"}:
        out.append("trust-surface-stable")
    if rev_asym >= 0.5:
        out.append("revocation-asymmetry")
    if leg < 0.5:
        out.append("legitimacy-risk")
    if "unknown" in lineage.lower() or "opaque" in lineage.lower() or "missing" in lineage.lower():
        out.append("wrapper-provenance-risk")
    if compression in {"high", "elevated", "critical"}:
        out.append("trust-compression-warning")
    return out


def build_trust_surface_overlays(
    trust_surface_audit: dict[str, Any],
    trust_surface_recommendations: dict[str, Any],
    trust_surface_map: dict[str, Any],
    delegated_access_registry_bridge: dict[str, Any],
    revocation_asymmetry_report: dict[str, Any],
    interface_legitimacy_risk_report: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "trust_surface_audit": _extract_required_provenance("trust_surface_audit", trust_surface_audit),
        "trust_surface_recommendations": _extract_required_provenance("trust_surface_recommendations", trust_surface_recommendations),
        "trust_surface_map": _extract_required_provenance("trust_surface_map", trust_surface_map),
        "delegated_access_registry": _extract_required_provenance("delegated_access_registry", delegated_access_registry_bridge),
        "revocation_asymmetry_report": _extract_required_provenance("revocation_asymmetry_report", revocation_asymmetry_report),
        "interface_legitimacy_risk_report": _extract_required_provenance("interface_legitimacy_risk_report", interface_legitimacy_risk_report),
    }

    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [e for e in as_list(trust_surface_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(trust_surface_recommendations.get("recommendations")) if isinstance(e, dict)]
    map_entries = [e for e in as_list(trust_surface_map.get("entries")) if isinstance(e, dict)]
    delegated_entries = [e for e in as_list(delegated_access_registry_bridge.get("entries")) if isinstance(e, dict)]
    rev_entries = [e for e in as_list(revocation_asymmetry_report.get("entries")) if isinstance(e, dict)]
    leg_entries = [e for e in as_list(interface_legitimacy_risk_report.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    map_by = _index_by_key(map_entries, "reviewId")
    delegated_by = _index_by_key(delegated_entries, "reviewId")
    rev_by = _index_by_key(rev_entries, "reviewId")
    leg_by = _index_by_key(leg_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda row: str(row.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        tmap = map_by.get(review_id, {})
        dreg = delegated_by.get(review_id, {})
        rev = rev_by.get(review_id, {})
        leg = leg_by.get(review_id, {})
        audit = audit_by.get(review_id, {})

        trust_surface_status = str(tmap.get("trustSurfaceStatus", rec.get("trustSurfaceStatus", "monitor")))
        persistence_class = str(tmap.get("persistenceClass", rec.get("persistenceClass", "bounded")))
        revocation_asymmetry_score = _to_float(rev.get("revocationAsymmetryScore", rec.get("revocationAsymmetryScore", 0.0)))
        interface_legitimacy_score = _to_float(leg.get("interfaceLegitimacyScore", rec.get("interfaceLegitimacyScore", 0.0)))
        trust_compression_risk = str(leg.get("trustCompressionRisk", rec.get("trustCompressionRisk", "bounded"))).lower()
        audit_burden_score = _to_float(leg.get("auditBurdenScore", rec.get("auditBurdenScore", 0.0)))
        wrapper_lineage = str(dreg.get("wrapperLineage", rec.get("wrapperLineage", "unknown")))

        base = {
            "reviewId": review_id,
            "trustSurfaceStatus": trust_surface_status,
            "persistenceClass": persistence_class,
            "revocationAsymmetryScore": revocation_asymmetry_score,
            "interfaceLegitimacyScore": interface_legitimacy_score,
            "trustCompressionRisk": trust_compression_risk,
            "auditBurdenScore": audit_burden_score,
            "wrapperLineage": wrapper_lineage,
            "auditState": str(audit.get("trustSurfaceAuditState", rec.get("trustSurfaceAuditState", "none"))),
            "atlasClasses": _classes(
                trust_surface_status,
                revocation_asymmetry_score,
                interface_legitimacy_score,
                trust_compression_risk,
                wrapper_lineage,
            ),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({**base, "status": "watch", "queuedAt": generated_at})

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "noAutomaticAccusation": True,
            "noEnforcementActions": True,
            "noIdentityMutation": True,
            "noGovernanceAuthorityAssignment": True,
            "informationalSignalsOnly": True,
        })

    shared = {
        "generatedAt": generated_at,
        "trustSurfaceProtocol": True,
        "nonCanonical": True,
        "noAutomaticAccusation": True,
        "noEnforcementActions": True,
        "noIdentityMutation": True,
        "noGovernanceAuthorityAssignment": True,
        "informationalSignalsOnly": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    trust_surface_dashboard = {**shared, "entries": dashboard_entries}
    delegated_access_registry = {**shared, "entries": registry_entries}
    revocation_watchlist = {**shared, "entries": watch_entries}
    interface_legitimacy_annotations = {**shared, "annotations": annotation_entries}

    for payload, key in (
        (trust_surface_dashboard, "entries"),
        (delegated_access_registry, "entries"),
        (revocation_watchlist, "entries"),
        (interface_legitimacy_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for flag in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(flag), bool):
                raise ValueError(f"{flag} must be a boolean")

    return trust_surface_dashboard, delegated_access_registry, revocation_watchlist, interface_legitimacy_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trust-surface-audit", type=Path, default=Path("bridge/trust_surface_audit.json"))
    parser.add_argument("--trust-surface-recommendations", type=Path, default=Path("bridge/trust_surface_recommendations.json"))
    parser.add_argument("--trust-surface-map", type=Path, default=Path("bridge/trust_surface_map.json"))
    parser.add_argument("--delegated-access-registry", type=Path, default=Path("bridge/delegated_access_registry.json"))
    parser.add_argument("--revocation-asymmetry-report", type=Path, default=Path("bridge/revocation_asymmetry_report.json"))
    parser.add_argument("--interface-legitimacy-risk-report", type=Path, default=Path("bridge/interface_legitimacy_risk_report.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))
    parser.add_argument("--out-delegated-access-registry", type=Path, default=Path("registry/delegated_access_registry.json"))
    parser.add_argument("--out-revocation-watchlist", type=Path, default=Path("registry/revocation_watchlist.json"))
    parser.add_argument("--out-interface-legitimacy-annotations", type=Path, default=Path("registry/interface_legitimacy_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_trust_surface_overlays(
            load_required_json(args.trust_surface_audit),
            load_required_json(args.trust_surface_recommendations),
            load_required_json(args.trust_surface_map),
            load_required_json(args.delegated_access_registry),
            load_required_json(args.revocation_asymmetry_report),
            load_required_json(args.interface_legitimacy_risk_report),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    for out in (
        args.out_trust_surface_dashboard,
        args.out_delegated_access_registry,
        args.out_revocation_watchlist,
        args.out_interface_legitimacy_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_trust_surface_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_delegated_access_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_revocation_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_interface_legitimacy_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote trust surface dashboard: {args.out_trust_surface_dashboard}")
    print(f"[OK] Wrote delegated access registry: {args.out_delegated_access_registry}")
    print(f"[OK] Wrote revocation watchlist: {args.out_revocation_watchlist}")
    print(f"[OK] Wrote interface legitimacy annotations: {args.out_interface_legitimacy_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
