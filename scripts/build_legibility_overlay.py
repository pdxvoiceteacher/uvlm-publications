#!/usr/bin/env python3
"""Build legibility, lineage, and queryability overlays.

Publisher surfaces only Sophia-audited legibility materials; it does not
declare final maps, certify settlement authority, or authorize institutional
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
    "lineage-visible",
    "glossary-available",
    "governance-breadcrumb-visible",
    "operator-legibility-weak",
    "queryability-ready",
    "legibility-trust-degraded",
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


def _atlas_classes(lineage_visible: bool, glossary_available: bool, governance_visible: bool, operator_legibility_flags: list[str], queryability_ready: bool, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if lineage_visible:
        out.append("lineage-visible")
    if glossary_available:
        out.append("glossary-available")
    if governance_visible:
        out.append("governance-breadcrumb-visible")
    if operator_legibility_flags:
        out.append("operator-legibility-weak")
    if queryability_ready:
        out.append("queryability-ready")
    if trust_degraded:
        out.append("legibility-trust-degraded")
    return out


def build_legibility_overlays(
    phase_lineage_registry: dict[str, Any],
    phase_glossary: dict[str, Any],
    coherence_memory_trace: dict[str, Any],
    governance_action_ledger: dict[str, Any],
    audit_lineage_registry: dict[str, Any],
    background_coherence_dashboard: dict[str, Any],
    living_terrace_dashboard: dict[str, Any],
    epochal_surface_dashboard: dict[str, Any],
    terrace_seed_dashboard: dict[str, Any],
    new_delta_dashboard: dict[str, Any],
    successor_crossing_dashboard: dict[str, Any],
    terrace_health_dashboard: dict[str, Any],
    delta_dashboard: dict[str, Any],
    trust_surface_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    provenances: dict[str, dict[str, Any]] = {
        "phase_lineage_registry": _extract_required_provenance("phase_lineage_registry", phase_lineage_registry),
        "phase_glossary": _extract_required_provenance("phase_glossary", phase_glossary),
        "coherence_memory_trace": _extract_required_provenance("coherence_memory_trace", coherence_memory_trace),
        "governance_action_ledger": _extract_required_provenance("governance_action_ledger", governance_action_ledger),
        "audit_lineage_registry": _extract_required_provenance("audit_lineage_registry", audit_lineage_registry),
    }

    for name, artifact in {
        "background_coherence_dashboard": background_coherence_dashboard,
        "living_terrace_dashboard": living_terrace_dashboard,
        "epochal_surface_dashboard": epochal_surface_dashboard,
        "terrace_seed_dashboard": terrace_seed_dashboard,
        "new_delta_dashboard": new_delta_dashboard,
        "successor_crossing_dashboard": successor_crossing_dashboard,
        "terrace_health_dashboard": terrace_health_dashboard,
        "delta_dashboard": delta_dashboard,
        "trust_surface_dashboard": trust_surface_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [e for e in as_list(audit_lineage_registry.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(governance_action_ledger.get("recommendations")) if isinstance(e, dict)]
    lineage_entries = [e for e in as_list(phase_lineage_registry.get("entries")) if isinstance(e, dict)]
    glossary_entries = [e for e in as_list(phase_glossary.get("entries")) if isinstance(e, dict)]
    memory_entries = [e for e in as_list(coherence_memory_trace.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    lineage_by = _index_by_key(lineage_entries, "reviewId")
    glossary_by = _index_by_key(glossary_entries, "reviewId")
    memory_by = _index_by_key(memory_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    glossary_registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        ln = lineage_by.get(review_id, {})
        gl = glossary_by.get(review_id, {})
        mm = memory_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        phase_lineage_visibility = bool(ln.get("phaseLineageVisibility", rec.get("phaseLineageVisibility", False)))
        glossary_availability = bool(gl.get("glossaryAvailability", rec.get("glossaryAvailability", False)))
        governance_breadcrumb_visibility = bool(mm.get("governanceBreadcrumbVisibility", rec.get("governanceBreadcrumbVisibility", False)))
        operator_legibility_flags = [str(v) for v in as_list(mm.get("operatorLegibilityFlags", rec.get("operatorLegibilityFlags", []))) if isinstance(v, str)]
        queryability_readiness = bool(mm.get("queryabilityReadiness", rec.get("queryabilityReadiness", False)))
        executive_review_visibility = bool(mm.get("executiveReviewVisibility", rec.get("executiveReviewVisibility", False)))
        provenance_markers = [str(v) for v in as_list(mm.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(mm.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]
        pedagogy_ordinariness = _to_float(mm.get("pedagogyOrdinariness", rec.get("pedagogyOrdinariness", 0.0)))

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(
            phase_lineage_visibility,
            glossary_availability,
            governance_breadcrumb_visibility,
            operator_legibility_flags,
            queryability_readiness,
            trust_degraded,
        )

        base = {
            "reviewId": review_id,
            "phaseLineageVisibility": phase_lineage_visibility,
            "glossaryAvailability": glossary_availability,
            "governanceBreadcrumbVisibility": governance_breadcrumb_visibility,
            "operatorLegibilityFlags": operator_legibility_flags,
            "queryabilityReadiness": queryability_readiness,
            "executiveReviewVisibility": executive_review_visibility,
            "pedagogyOrdinariness": pedagogy_ordinariness,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "auditLineageState": str(au.get("auditLineageState", rec.get("auditLineageState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            glossary_registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({**base, "status": "watch", "queuedAt": generated_at})

        note = rec.get("suppressedExplanatoryNote")
        note_str = str(note).strip() if isinstance(note, str) else ""
        annotation_entries.append(
            {
                **base,
                "targetPublisherAction": action,
                "suppressedExplanatoryNote": note_str if action == "suppressed" and note_str else None,
                "noCanonMutation": True,
                "noDeploymentExecution": True,
                "noGovernanceRightMutation": True,
                "noRankingOfPhasesCivilizationsFuturesInstitutions": True,
                "lineageVisibilityNotSettlementAuthority": True,
                "noTheoryCompetitionClosure": True,
                "noFinalMapCompletePresentation": True,
            }
        )

    shared = {
        "generatedAt": generated_at,
        "legibilityProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfPhasesCivilizationsFuturesInstitutions": True,
        "lineageVisibilityNotSettlementAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noFinalMapCompletePresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsLegibilityMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    phase_lineage_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    operator_glossary_registry = {**shared, "entries": sorted(glossary_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    governance_breadcrumb_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    legibility_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (phase_lineage_dashboard, "entries"),
        (operator_glossary_registry, "entries"),
        (governance_breadcrumb_watchlist, "entries"),
        (legibility_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return phase_lineage_dashboard, operator_glossary_registry, governance_breadcrumb_watchlist, legibility_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--phase-lineage-registry", type=Path, default=Path("bridge/phase_lineage_registry.json"))
    p.add_argument("--phase-glossary", type=Path, default=Path("bridge/phase_glossary.json"))
    p.add_argument("--coherence-memory-trace", type=Path, default=Path("bridge/coherence_memory_trace.json"))
    p.add_argument("--governance-action-ledger", type=Path, default=Path("bridge/governance_action_ledger.json"))
    p.add_argument("--audit-lineage-registry", type=Path, default=Path("bridge/audit_lineage_registry.json"))

    p.add_argument("--background-coherence-dashboard", type=Path, default=Path("registry/background_coherence_dashboard.json"))
    p.add_argument("--living-terrace-dashboard", type=Path, default=Path("registry/living_terrace_dashboard.json"))
    p.add_argument("--epochal-surface-dashboard", type=Path, default=Path("registry/epochal_surface_dashboard.json"))
    p.add_argument("--terrace-seed-dashboard", type=Path, default=Path("registry/terrace_seed_dashboard.json"))
    p.add_argument("--new-delta-dashboard", type=Path, default=Path("registry/new_delta_dashboard.json"))
    p.add_argument("--successor-crossing-dashboard", type=Path, default=Path("registry/successor_crossing_dashboard.json"))
    p.add_argument("--terrace-health-dashboard", type=Path, default=Path("registry/terrace_health_dashboard.json"))
    p.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    p.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-phase-lineage-dashboard", type=Path, default=Path("registry/phase_lineage_dashboard.json"))
    p.add_argument("--out-operator-glossary-registry", type=Path, default=Path("registry/operator_glossary_registry.json"))
    p.add_argument("--out-governance-breadcrumb-watchlist", type=Path, default=Path("registry/governance_breadcrumb_watchlist.json"))
    p.add_argument("--out-legibility-annotations", type=Path, default=Path("registry/legibility_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_legibility_overlays(
            load_required_json(args.phase_lineage_registry),
            load_required_json(args.phase_glossary),
            load_required_json(args.coherence_memory_trace),
            load_required_json(args.governance_action_ledger),
            load_required_json(args.audit_lineage_registry),
            load_required_json(args.background_coherence_dashboard),
            load_required_json(args.living_terrace_dashboard),
            load_required_json(args.epochal_surface_dashboard),
            load_required_json(args.terrace_seed_dashboard),
            load_required_json(args.new_delta_dashboard),
            load_required_json(args.successor_crossing_dashboard),
            load_required_json(args.terrace_health_dashboard),
            load_required_json(args.delta_dashboard),
            load_required_json(args.trust_surface_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    for out in (
        args.out_phase_lineage_dashboard,
        args.out_operator_glossary_registry,
        args.out_governance_breadcrumb_watchlist,
        args.out_legibility_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_phase_lineage_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_operator_glossary_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_governance_breadcrumb_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_legibility_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote phase lineage dashboard: {args.out_phase_lineage_dashboard}")
    print(f"[OK] Wrote operator glossary registry: {args.out_operator_glossary_registry}")
    print(f"[OK] Wrote governance breadcrumb watchlist: {args.out_governance_breadcrumb_watchlist}")
    print(f"[OK] Wrote legibility annotations: {args.out_legibility_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
