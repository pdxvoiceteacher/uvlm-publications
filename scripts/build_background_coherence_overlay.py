#!/usr/bin/env python3
"""Build background-coherence and civilizational-normalization overlays.

Publisher surfaces only Sophia-audited background-coherence materials; it does
not declare final epochs, certify civilizational settlement, or authorize
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
    "background-coherence-reviewable",
    "normalization-ambient",
    "ambient-memory-watch",
    "commons-habitable",
    "background-trust-degraded",
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


def _atlas_classes(background_class: str, normalization_class: str, ambient_memory_class: str, commons_habitability: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if background_class in {"quiet", "reviewable", "bounded", "conditional", "stable"}:
        out.append("background-coherence-reviewable")
    if normalization_class in {"ambient", "gradual", "bounded", "conditional", "habitable"}:
        out.append("normalization-ambient")
    if ambient_memory_class in {"present", "threaded", "recovering", "bounded", "watch"}:
        out.append("ambient-memory-watch")
    if commons_habitability in {"habitable", "ordinary", "bounded", "recovering", "durable"}:
        out.append("commons-habitable")
    if trust_degraded:
        out.append("background-trust-degraded")
    return out


def build_background_coherence_overlays(
    background_coherence_audit: dict[str, Any],
    background_coherence_recommendations: dict[str, Any],
    background_coherence_map: dict[str, Any],
    civilizational_normalization_report: dict[str, Any],
    ambient_memory_registry: dict[str, Any],
    normalization_gate: dict[str, Any],
    living_terrace_dashboard: dict[str, Any],
    plural_habitation_watchlist: dict[str, Any],
    commons_habitability_registry: dict[str, Any],
    epochal_surface_dashboard: dict[str, Any],
    terrace_seed_dashboard: dict[str, Any],
    new_delta_dashboard: dict[str, Any],
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
        "background_coherence_audit": _extract_required_provenance("background_coherence_audit", background_coherence_audit),
        "background_coherence_recommendations": _extract_required_provenance("background_coherence_recommendations", background_coherence_recommendations),
        "background_coherence_map": _extract_required_provenance("background_coherence_map", background_coherence_map),
        "civilizational_normalization_report": _extract_required_provenance("civilizational_normalization_report", civilizational_normalization_report),
        "ambient_memory_registry": _extract_required_provenance("ambient_memory_registry", ambient_memory_registry),
        "normalization_gate": _extract_required_provenance("normalization_gate", normalization_gate),
    }

    for name, artifact in {
        "living_terrace_dashboard": living_terrace_dashboard,
        "plural_habitation_watchlist": plural_habitation_watchlist,
        "commons_habitability_registry": commons_habitability_registry,
        "epochal_surface_dashboard": epochal_surface_dashboard,
        "terrace_seed_dashboard": terrace_seed_dashboard,
        "new_delta_dashboard": new_delta_dashboard,
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

    audits = [e for e in as_list(background_coherence_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(background_coherence_recommendations.get("recommendations")) if isinstance(e, dict)]
    background_entries = [e for e in as_list(background_coherence_map.get("entries")) if isinstance(e, dict)]
    normalization_entries = [e for e in as_list(civilizational_normalization_report.get("entries")) if isinstance(e, dict)]
    ambient_entries = [e for e in as_list(ambient_memory_registry.get("entries")) if isinstance(e, dict)]
    gate_entries = [e for e in as_list(normalization_gate.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    background_by = _index_by_key(background_entries, "reviewId")
    normalization_by = _index_by_key(normalization_entries, "reviewId")
    ambient_by = _index_by_key(ambient_entries, "reviewId")
    gate_by = _index_by_key(gate_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    normalization_registry_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        bg = background_by.get(review_id, {})
        no = normalization_by.get(review_id, {})
        am = ambient_by.get(review_id, {})
        ga = gate_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        background_status = str(bg.get("backgroundStatus", rec.get("backgroundStatus", "under_review")))
        background_class = str(bg.get("backgroundClass", rec.get("backgroundClass", "bounded"))).lower()
        normalization_class = str(no.get("normalizationClass", rec.get("normalizationClass", "bounded"))).lower()
        ambient_memory_class = str(am.get("ambientMemoryClass", rec.get("ambientMemoryClass", "bounded"))).lower()
        gate_status = str(ga.get("gateStatus", rec.get("gateStatus", "review"))).lower()
        trust_ordinariness = str(no.get("trustOrdinariness", rec.get("trustOrdinariness", "bounded"))).lower()
        plurality_metabolization = str(no.get("pluralityMetabolization", rec.get("pluralityMetabolization", "bounded"))).lower()
        commons_habitability = str(no.get("commonsHabitability", rec.get("commonsHabitability", "bounded"))).lower()
        pedagogy_ordinariness = _to_float(am.get("pedagogyOrdinariness", rec.get("pedagogyOrdinariness", 0.0)))
        provenance_markers = [str(v) for v in as_list(no.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(no.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(background_class, normalization_class, ambient_memory_class, commons_habitability, trust_degraded)

        base = {
            "reviewId": review_id,
            "backgroundStatus": background_status,
            "backgroundClass": background_class,
            "normalizationClass": normalization_class,
            "ambientMemoryClass": ambient_memory_class,
            "gateStatus": gate_status,
            "trustOrdinariness": trust_ordinariness,
            "pluralityMetabolization": plurality_metabolization,
            "commonsHabitability": commons_habitability,
            "pedagogyOrdinariness": pedagogy_ordinariness,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "backgroundCoherenceAuditState": str(au.get("backgroundCoherenceAuditState", rec.get("backgroundCoherenceAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            normalization_registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({**base, "status": "watch", "queuedAt": generated_at})

        annotation_entries.append(
            {
                **base,
                "targetPublisherAction": action,
                "noCanonMutation": True,
                "noDeploymentExecution": True,
                "noGovernanceRightMutation": True,
                "noRankingOfFuturesCivilizationsCommunitiesInstitutions": True,
                "backgroundVisibilityNotFinalAuthority": True,
                "noTheoryCompetitionClosure": True,
                "noEpochFinalizedOrFutureSettledPermanentlyPresentation": True,
            }
        )

    shared = {
        "generatedAt": generated_at,
        "backgroundCoherenceProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfFuturesCivilizationsCommunitiesInstitutions": True,
        "backgroundVisibilityNotFinalAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noEpochFinalizedOrFutureSettledPermanentlyPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsBackgroundCoherenceMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    background_coherence_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    ambient_memory_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    civilizational_normalization_registry = {**shared, "entries": sorted(normalization_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    background_coherence_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (background_coherence_dashboard, "entries"),
        (ambient_memory_watchlist, "entries"),
        (civilizational_normalization_registry, "entries"),
        (background_coherence_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return background_coherence_dashboard, ambient_memory_watchlist, civilizational_normalization_registry, background_coherence_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--background-coherence-audit", type=Path, default=Path("bridge/background_coherence_audit.json"))
    p.add_argument("--background-coherence-recommendations", type=Path, default=Path("bridge/background_coherence_recommendations.json"))
    p.add_argument("--background-coherence-map", type=Path, default=Path("bridge/background_coherence_map.json"))
    p.add_argument("--civilizational-normalization-report", type=Path, default=Path("bridge/civilizational_normalization_report.json"))
    p.add_argument("--ambient-memory-registry", type=Path, default=Path("bridge/ambient_memory_registry.json"))
    p.add_argument("--normalization-gate", type=Path, default=Path("bridge/normalization_gate.json"))

    p.add_argument("--living-terrace-dashboard", type=Path, default=Path("registry/living_terrace_dashboard.json"))
    p.add_argument("--plural-habitation-watchlist", type=Path, default=Path("registry/plural_habitation_watchlist.json"))
    p.add_argument("--commons-habitability-registry", type=Path, default=Path("registry/commons_habitability_registry.json"))
    p.add_argument("--epochal-surface-dashboard", type=Path, default=Path("registry/epochal_surface_dashboard.json"))
    p.add_argument("--terrace-seed-dashboard", type=Path, default=Path("registry/terrace_seed_dashboard.json"))
    p.add_argument("--new-delta-dashboard", type=Path, default=Path("registry/new_delta_dashboard.json"))
    p.add_argument("--epoch-dashboard", type=Path, default=Path("registry/epoch_dashboard.json"))
    p.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    p.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-background-coherence-dashboard", type=Path, default=Path("registry/background_coherence_dashboard.json"))
    p.add_argument("--out-ambient-memory-watchlist", type=Path, default=Path("registry/ambient_memory_watchlist.json"))
    p.add_argument("--out-civilizational-normalization-registry", type=Path, default=Path("registry/civilizational_normalization_registry.json"))
    p.add_argument("--out-background-coherence-annotations", type=Path, default=Path("registry/background_coherence_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_background_coherence_overlays(
            load_required_json(args.background_coherence_audit),
            load_required_json(args.background_coherence_recommendations),
            load_required_json(args.background_coherence_map),
            load_required_json(args.civilizational_normalization_report),
            load_required_json(args.ambient_memory_registry),
            load_required_json(args.normalization_gate),
            load_required_json(args.living_terrace_dashboard),
            load_required_json(args.plural_habitation_watchlist),
            load_required_json(args.commons_habitability_registry),
            load_required_json(args.epochal_surface_dashboard),
            load_required_json(args.terrace_seed_dashboard),
            load_required_json(args.new_delta_dashboard),
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
        args.out_background_coherence_dashboard,
        args.out_ambient_memory_watchlist,
        args.out_civilizational_normalization_registry,
        args.out_background_coherence_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_background_coherence_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_ambient_memory_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_civilizational_normalization_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_background_coherence_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote background coherence dashboard: {args.out_background_coherence_dashboard}")
    print(f"[OK] Wrote ambient memory watchlist: {args.out_ambient_memory_watchlist}")
    print(f"[OK] Wrote civilizational normalization registry: {args.out_civilizational_normalization_registry}")
    print(f"[OK] Wrote background coherence annotations: {args.out_background_coherence_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
