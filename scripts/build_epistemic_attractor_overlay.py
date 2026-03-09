#!/usr/bin/env python3
"""Build epistemic attractor and topology overlays.

Publisher surfaces only Sophia-audited epistemic-topology materials; it does
not declare final truth, canonize domains, or rank scientific traditions.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from canonical_integrity_manifest import evaluate_manifest_pair, load_manifest

REQUIRED_PROVENANCE_KEYS = ("schemaVersion", "producerCommits", "sourceMode")


def load_required_json(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"Missing required canonical artifact: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in required canonical artifact {path}: {exc}") from exc


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _index_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        k = row.get(key)
        if isinstance(k, str):
            out[k] = row
    return out


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


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    return action if action in {"docket", "watch", "suppressed", "rejected"} else "watch"


def _targets(rec: dict[str, Any]) -> list[str]:
    return sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])


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


def _validate_outputs(
    knowledge_topology_dashboard: dict[str, Any],
    attractor_registry: dict[str, Any],
    dead_zone_watchlist: dict[str, Any],
    paradigm_shift_annotations: dict[str, Any],
) -> None:
    if not isinstance(knowledge_topology_dashboard.get("entries"), list):
        raise ValueError("knowledge_topology_dashboard.entries must be a list")
    if not isinstance(attractor_registry.get("entries"), list):
        raise ValueError("attractor_registry.entries must be a list")
    if not isinstance(dead_zone_watchlist.get("entries"), list):
        raise ValueError("dead_zone_watchlist.entries must be a list")
    if not isinstance(paradigm_shift_annotations.get("annotations"), list):
        raise ValueError("paradigm_shift_annotations.annotations must be a list")

    for payload in (knowledge_topology_dashboard, attractor_registry, dead_zone_watchlist, paradigm_shift_annotations):
        for key in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(key), bool):
                raise ValueError(f"{key} must be a boolean")
        json.dumps(payload)


def build_epistemic_attractor_overlays(
    epistemic_attractor_audit: dict[str, Any],
    epistemic_attractor_recommendations: dict[str, Any],
    epistemic_attractor_map: dict[str, Any],
    knowledge_basin_registry: dict[str, Any],
    dead_zone_report: dict[str, Any],
    paradigm_shift_forecast: dict[str, Any],
    emergent_domain_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "epistemic_attractor_audit": _extract_required_provenance("epistemic_attractor_audit", epistemic_attractor_audit),
        "epistemic_attractor_recommendations": _extract_required_provenance("epistemic_attractor_recommendations", epistemic_attractor_recommendations),
        "epistemic_attractor_map": _extract_required_provenance("epistemic_attractor_map", epistemic_attractor_map),
        "knowledge_basin_registry": _extract_required_provenance("knowledge_basin_registry", knowledge_basin_registry),
        "dead_zone_report": _extract_required_provenance("dead_zone_report", dead_zone_report),
        "paradigm_shift_forecast": _extract_required_provenance("paradigm_shift_forecast", paradigm_shift_forecast),
    }
    for name, artifact in {
        "emergent_domain_dashboard": emergent_domain_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "value_dashboard": value_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)
    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [e for e in as_list(epistemic_attractor_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(epistemic_attractor_recommendations.get("recommendations")) if isinstance(e, dict)]
    attractor_entries = [e for e in as_list(epistemic_attractor_map.get("entries")) if isinstance(e, dict)]
    basin_entries = [e for e in as_list(knowledge_basin_registry.get("entries")) if isinstance(e, dict)]
    dead_zone_entries = [e for e in as_list(dead_zone_report.get("entries")) if isinstance(e, dict)]
    shift_entries = [e for e in as_list(paradigm_shift_forecast.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    attractor_by_review = _index_by_key(attractor_entries, "reviewId")
    basin_by_review = _index_by_key(basin_entries, "reviewId")
    dead_zone_by_review = _index_by_key(dead_zone_entries, "reviewId")
    shift_by_review = _index_by_key(shift_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        attractor = attractor_by_review.get(review_id, {})
        basin = basin_by_review.get(review_id, {})
        dead_zone = dead_zone_by_review.get(review_id, {})
        shift = shift_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        epistemic_status = str(attractor.get("epistemicStatus", rec.get("epistemicStatus", "monitor")))
        attractor_class = str(attractor.get("attractorClass", rec.get("attractorClass", "mixed")))
        basin_class = str(basin.get("basinClass", rec.get("basinClass", "mixed")))
        dead_zone_recurrence = str(dead_zone.get("deadZoneRecurrence", rec.get("deadZoneRecurrence", "bounded")))
        paradigm_shift_forecast_signal = str(shift.get("paradigmShiftForecast", rec.get("paradigmShiftForecast", "bounded")))
        memory_retention_strength = str(rec.get("memoryRetentionStrength", "bounded"))
        governance_compatibility = str(rec.get("governanceCompatibility", "compatible"))
        shift_probability = _to_float(shift.get("shiftProbability", rec.get("shiftProbability", 0.0)))
        audit_state = str(audit.get("epistemicAttractorAuditState", rec.get("epistemicAttractorAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "epistemicStatus": epistemic_status,
            "attractorClass": attractor_class,
            "basinClass": basin_class,
            "deadZoneRecurrence": dead_zone_recurrence,
            "paradigmShiftForecast": paradigm_shift_forecast_signal,
            "shiftProbability": shift_probability,
            "memoryRetentionStrength": memory_retention_strength,
            "governanceCompatibility": governance_compatibility,
            "epistemicAttractorAuditState": audit_state,
            "linkedTargetIds": linked_target_ids,
        }

        if action == "docket":
            dashboard_entries.append({**base, "humanReviewFlag": bool(rec.get("humanReviewFlag", True)), "queuedAt": generated_at})
            registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({
                **base,
                "status": "watch",
                "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                "observational": True,
                "nonCanonical": True,
                "queuedAt": generated_at,
            })

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "noCanonMutation": True,
            "noRankingOfPersonsCommunitiesTraditions": True,
            "noTheoryCompetitionClosure": True,
            "noGovernanceRightsMutation": True,
            "noFinalTruthClaims": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    knowledge_topology_dashboard = {
        "generatedAt": generated_at,
        "epistemicTopologyProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noRankingOfPersonsCommunitiesTraditions": True,
        "noTheoryCompetitionClosure": True,
        "noGovernanceRightsMutation": True,
        "noFinalTruthClaims": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    attractor_registry = {
        "generatedAt": generated_at,
        "epistemicTopologyProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noRankingOfPersonsCommunitiesTraditions": True,
        "noTheoryCompetitionClosure": True,
        "noGovernanceRightsMutation": True,
        "noFinalTruthClaims": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    dead_zone_watchlist = {
        "generatedAt": generated_at,
        "epistemicTopologyProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noRankingOfPersonsCommunitiesTraditions": True,
        "noTheoryCompetitionClosure": True,
        "noGovernanceRightsMutation": True,
        "noFinalTruthClaims": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    paradigm_shift_annotations = {
        "generatedAt": generated_at,
        "epistemicTopologyProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noRankingOfPersonsCommunitiesTraditions": True,
        "noTheoryCompetitionClosure": True,
        "noGovernanceRightsMutation": True,
        "noFinalTruthClaims": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        **integrity_status,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(knowledge_topology_dashboard, attractor_registry, dead_zone_watchlist, paradigm_shift_annotations)
    return knowledge_topology_dashboard, attractor_registry, dead_zone_watchlist, paradigm_shift_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epistemic-attractor-audit", type=Path, default=Path("bridge/epistemic_attractor_audit.json"))
    parser.add_argument("--epistemic-attractor-recommendations", type=Path, default=Path("bridge/epistemic_attractor_recommendations.json"))
    parser.add_argument("--epistemic-attractor-map", type=Path, default=Path("bridge/epistemic_attractor_map.json"))
    parser.add_argument("--knowledge-basin-registry", type=Path, default=Path("bridge/knowledge_basin_registry.json"))
    parser.add_argument("--dead-zone-report", type=Path, default=Path("bridge/dead_zone_report.json"))
    parser.add_argument("--paradigm-shift-forecast", type=Path, default=Path("bridge/paradigm_shift_forecast.json"))

    parser.add_argument("--emergent-domain-dashboard", type=Path, default=Path("registry/emergent_domain_dashboard.json"))
    parser.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    parser.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-knowledge-topology-dashboard", type=Path, default=Path("registry/knowledge_topology_dashboard.json"))
    parser.add_argument("--out-attractor-registry", type=Path, default=Path("registry/attractor_registry.json"))
    parser.add_argument("--out-dead-zone-watchlist", type=Path, default=Path("registry/dead_zone_watchlist.json"))
    parser.add_argument("--out-paradigm-shift-annotations", type=Path, default=Path("registry/paradigm_shift_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_epistemic_attractor_overlays(
            load_required_json(args.epistemic_attractor_audit),
            load_required_json(args.epistemic_attractor_recommendations),
            load_required_json(args.epistemic_attractor_map),
            load_required_json(args.knowledge_basin_registry),
            load_required_json(args.dead_zone_report),
            load_required_json(args.paradigm_shift_forecast),
            load_required_json(args.emergent_domain_dashboard),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.commons_sovereignty_dashboard),
            load_required_json(args.value_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_knowledge_topology_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_attractor_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_dead_zone_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_paradigm_shift_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_knowledge_topology_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_attractor_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_dead_zone_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_paradigm_shift_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote knowledge topology dashboard: {args.out_knowledge_topology_dashboard}")
    print(f"[OK] Wrote attractor registry: {args.out_attractor_registry}")
    print(f"[OK] Wrote dead zone watchlist: {args.out_dead_zone_watchlist}")
    print(f"[OK] Wrote paradigm shift annotations: {args.out_paradigm_shift_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
