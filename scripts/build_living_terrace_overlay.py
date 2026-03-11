#!/usr/bin/env python3
"""Build living-terrace emergence and commons-habitability overlays.

Publisher surfaces only Sophia-audited living-terrace materials; it does not
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
    "living-terrace-reviewable",
    "commons-habitability-conditional",
    "plural-habitation-open",
    "plurality-metabolized",
    "living-terrace-trust-degraded",
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


def _atlas_classes(living_terrace_class: str, habitability_class: str, habitation_class: str, plurality_metabolization: str, trust_degraded: bool) -> list[str]:
    out: list[str] = []
    if living_terrace_class in {"emergent", "reviewable", "bounded", "conditional", "living"}:
        out.append("living-terrace-reviewable")
    if habitability_class in {"habitable", "conditional", "guarded", "bounded", "forming"}:
        out.append("commons-habitability-conditional")
    if habitation_class in {"open", "plural", "recovering", "bounded", "experimental"}:
        out.append("plural-habitation-open")
    if plurality_metabolization in {"metabolized", "durable", "retained", "bounded", "recovering"}:
        out.append("plurality-metabolized")
    if trust_degraded:
        out.append("living-terrace-trust-degraded")
    return out


def build_living_terrace_overlays(
    living_terrace_audit: dict[str, Any],
    living_terrace_recommendations: dict[str, Any],
    living_terrace_map: dict[str, Any],
    commons_habitability_report: dict[str, Any],
    plural_habitation_registry: dict[str, Any],
    terrace_consolidation_gate: dict[str, Any],
    epochal_surface_dashboard: dict[str, Any],
    reopened_experiment_watchlist: dict[str, Any],
    habitable_plateau_registry: dict[str, Any],
    terrace_seed_dashboard: dict[str, Any],
    new_delta_dashboard: dict[str, Any],
    successor_crossing_dashboard: dict[str, Any],
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
        "living_terrace_audit": _extract_required_provenance("living_terrace_audit", living_terrace_audit),
        "living_terrace_recommendations": _extract_required_provenance("living_terrace_recommendations", living_terrace_recommendations),
        "living_terrace_map": _extract_required_provenance("living_terrace_map", living_terrace_map),
        "commons_habitability_report": _extract_required_provenance("commons_habitability_report", commons_habitability_report),
        "plural_habitation_registry": _extract_required_provenance("plural_habitation_registry", plural_habitation_registry),
        "terrace_consolidation_gate": _extract_required_provenance("terrace_consolidation_gate", terrace_consolidation_gate),
    }

    for name, artifact in {
        "epochal_surface_dashboard": epochal_surface_dashboard,
        "reopened_experiment_watchlist": reopened_experiment_watchlist,
        "habitable_plateau_registry": habitable_plateau_registry,
        "terrace_seed_dashboard": terrace_seed_dashboard,
        "new_delta_dashboard": new_delta_dashboard,
        "successor_crossing_dashboard": successor_crossing_dashboard,
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

    audits = [e for e in as_list(living_terrace_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(living_terrace_recommendations.get("recommendations")) if isinstance(e, dict)]
    terrace_entries = [e for e in as_list(living_terrace_map.get("entries")) if isinstance(e, dict)]
    habitability_entries = [e for e in as_list(commons_habitability_report.get("entries")) if isinstance(e, dict)]
    habitation_entries = [e for e in as_list(plural_habitation_registry.get("entries")) if isinstance(e, dict)]
    gate_entries = [e for e in as_list(terrace_consolidation_gate.get("entries")) if isinstance(e, dict)]

    audit_by = _index_by_key(audits, "reviewId")
    terrace_by = _index_by_key(terrace_entries, "reviewId")
    habitability_by = _index_by_key(habitability_entries, "reviewId")
    habitation_by = _index_by_key(habitation_entries, "reviewId")
    gate_by = _index_by_key(gate_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    habitability_registry_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        te = terrace_by.get(review_id, {})
        hb = habitability_by.get(review_id, {})
        ha = habitation_by.get(review_id, {})
        ga = gate_by.get(review_id, {})
        au = audit_by.get(review_id, {})

        terrace_status = str(te.get("terraceStatus", rec.get("terraceStatus", "under_review")))
        living_terrace_class = str(te.get("livingTerraceClass", rec.get("livingTerraceClass", "bounded"))).lower()
        habitability_class = str(hb.get("habitabilityClass", rec.get("habitabilityClass", "bounded"))).lower()
        habitation_class = str(ha.get("habitationClass", rec.get("habitationClass", "bounded"))).lower()
        gate_status = str(ga.get("gateStatus", rec.get("gateStatus", "review"))).lower()
        trust_ordinariness = str(hb.get("trustOrdinariness", rec.get("trustOrdinariness", "bounded"))).lower()
        memory_teachability = str(hb.get("memoryTeachability", rec.get("memoryTeachability", "bounded"))).lower()
        plurality_metabolization = str(hb.get("pluralityMetabolization", rec.get("pluralityMetabolization", "bounded"))).lower()
        ordinary_steward_usability = _to_float(ha.get("ordinaryStewardUsability", rec.get("ordinaryStewardUsability", 0.0)))
        provenance_markers = [str(v) for v in as_list(hb.get("provenanceMarkers", rec.get("provenanceMarkers", []))) if isinstance(v, str)]
        canonical_integrity_markers = [str(v) for v in as_list(hb.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", []))) if isinstance(v, str)]

        trust_degraded = bool(integrity_status.get("trustPresentationDegraded", False))
        atlas_classes = _atlas_classes(living_terrace_class, habitability_class, habitation_class, plurality_metabolization, trust_degraded)

        base = {
            "reviewId": review_id,
            "terraceStatus": terrace_status,
            "livingTerraceClass": living_terrace_class,
            "habitabilityClass": habitability_class,
            "habitationClass": habitation_class,
            "gateStatus": gate_status,
            "trustOrdinariness": trust_ordinariness,
            "memoryTeachability": memory_teachability,
            "pluralityMetabolization": plurality_metabolization,
            "ordinaryStewardUsability": ordinary_steward_usability,
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_integrity_markers,
            "atlasClasses": atlas_classes,
            "livingTerraceAuditState": str(au.get("livingTerraceAuditState", rec.get("livingTerraceAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            habitability_registry_entries.append({**base, "updatedAt": generated_at})

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
                "terraceVisibilityNotSettledAuthority": True,
                "noTheoryCompetitionClosure": True,
                "noNewAgeSettledOrFutureSecuredPermanentlyPresentation": True,
            }
        )

    shared = {
        "generatedAt": generated_at,
        "livingTerraceProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noDeploymentExecution": True,
        "noGovernanceRightMutation": True,
        "noRankingOfFuturesSuccessorOrdersCivilizationsCommunitiesInstitutions": True,
        "terraceVisibilityNotSettledAuthority": True,
        "noTheoryCompetitionClosure": True,
        "noNewAgeSettledOrFutureSecuredPermanentlyPresentation": True,
        "atlasStylingSubtleClassesOnly": True,
        "atlasResetClearsLivingTerraceMarkers": True,
        "preserveTrustPresentationDegraded": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provenances),
        **integrity_status,
    }

    living_terrace_dashboard = {**shared, "entries": sorted(dashboard_entries, key=lambda r: str(r.get("reviewId", "")))}
    plural_habitation_watchlist = {**shared, "entries": sorted(watch_entries, key=lambda r: str(r.get("reviewId", "")))}
    commons_habitability_registry = {**shared, "entries": sorted(habitability_registry_entries, key=lambda r: str(r.get("reviewId", "")))}
    living_terrace_annotations = {**shared, "annotations": sorted(annotation_entries, key=lambda r: str(r.get("reviewId", "")))}

    for payload, key in (
        (living_terrace_dashboard, "entries"),
        (plural_habitation_watchlist, "entries"),
        (commons_habitability_registry, "entries"),
        (living_terrace_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for f in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(f), bool):
                raise ValueError(f"{f} must be a boolean")

    return living_terrace_dashboard, plural_habitation_watchlist, commons_habitability_registry, living_terrace_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--living-terrace-audit", type=Path, default=Path("bridge/living_terrace_audit.json"))
    p.add_argument("--living-terrace-recommendations", type=Path, default=Path("bridge/living_terrace_recommendations.json"))
    p.add_argument("--living-terrace-map", type=Path, default=Path("bridge/living_terrace_map.json"))
    p.add_argument("--commons-habitability-report", type=Path, default=Path("bridge/commons_habitability_report.json"))
    p.add_argument("--plural-habitation-registry", type=Path, default=Path("bridge/plural_habitation_registry.json"))
    p.add_argument("--terrace-consolidation-gate", type=Path, default=Path("bridge/terrace_consolidation_gate.json"))

    p.add_argument("--epochal-surface-dashboard", type=Path, default=Path("registry/epochal_surface_dashboard.json"))
    p.add_argument("--reopened-experiment-watchlist", type=Path, default=Path("registry/reopened_experiment_watchlist.json"))
    p.add_argument("--habitable-plateau-registry", type=Path, default=Path("registry/habitable_plateau_registry.json"))
    p.add_argument("--terrace-seed-dashboard", type=Path, default=Path("registry/terrace_seed_dashboard.json"))
    p.add_argument("--new-delta-dashboard", type=Path, default=Path("registry/new_delta_dashboard.json"))
    p.add_argument("--successor-crossing-dashboard", type=Path, default=Path("registry/successor_crossing_dashboard.json"))
    p.add_argument("--terrace-health-dashboard", type=Path, default=Path("registry/terrace_health_dashboard.json"))
    p.add_argument("--epoch-dashboard", type=Path, default=Path("registry/epoch_dashboard.json"))
    p.add_argument("--delta-dashboard", type=Path, default=Path("registry/delta_dashboard.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    p.add_argument("--trust-surface-dashboard", type=Path, default=Path("registry/trust_surface_dashboard.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-living-terrace-dashboard", type=Path, default=Path("registry/living_terrace_dashboard.json"))
    p.add_argument("--out-plural-habitation-watchlist", type=Path, default=Path("registry/plural_habitation_watchlist.json"))
    p.add_argument("--out-commons-habitability-registry", type=Path, default=Path("registry/commons_habitability_registry.json"))
    p.add_argument("--out-living-terrace-annotations", type=Path, default=Path("registry/living_terrace_annotations.json"))

    args = p.parse_args()

    try:
        outputs = build_living_terrace_overlays(
            load_required_json(args.living_terrace_audit),
            load_required_json(args.living_terrace_recommendations),
            load_required_json(args.living_terrace_map),
            load_required_json(args.commons_habitability_report),
            load_required_json(args.plural_habitation_registry),
            load_required_json(args.terrace_consolidation_gate),
            load_required_json(args.epochal_surface_dashboard),
            load_required_json(args.reopened_experiment_watchlist),
            load_required_json(args.habitable_plateau_registry),
            load_required_json(args.terrace_seed_dashboard),
            load_required_json(args.new_delta_dashboard),
            load_required_json(args.successor_crossing_dashboard),
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
        args.out_living_terrace_dashboard,
        args.out_plural_habitation_watchlist,
        args.out_commons_habitability_registry,
        args.out_living_terrace_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_living_terrace_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_plural_habitation_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_commons_habitability_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_living_terrace_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote living terrace dashboard: {args.out_living_terrace_dashboard}")
    print(f"[OK] Wrote plural habitation watchlist: {args.out_plural_habitation_watchlist}")
    print(f"[OK] Wrote commons habitability registry: {args.out_commons_habitability_registry}")
    print(f"[OK] Wrote living terrace annotations: {args.out_living_terrace_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
