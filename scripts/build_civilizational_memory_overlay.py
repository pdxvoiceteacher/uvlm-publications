#!/usr/bin/env python3
"""Build civilizational memory and knowledge stewardship overlays.

Publisher surfaces only Sophia-audited civilizational memory materials; it does
not determine canon, rank traditions, or erase failed branches.
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
    civilizational_memory_dashboard: dict[str, Any],
    epistemic_resilience_registry: dict[str, Any],
    memory_fragility_watchlist: dict[str, Any],
    civilizational_memory_annotations: dict[str, Any],
) -> None:
    if not isinstance(civilizational_memory_dashboard.get("entries"), list):
        raise ValueError("civilizational_memory_dashboard.entries must be a list")
    if not isinstance(epistemic_resilience_registry.get("entries"), list):
        raise ValueError("epistemic_resilience_registry.entries must be a list")
    if not isinstance(memory_fragility_watchlist.get("entries"), list):
        raise ValueError("memory_fragility_watchlist.entries must be a list")
    if not isinstance(civilizational_memory_annotations.get("annotations"), list):
        raise ValueError("civilizational_memory_annotations.annotations must be a list")

    for payload in (civilizational_memory_dashboard, epistemic_resilience_registry, memory_fragility_watchlist, civilizational_memory_annotations):
        for key in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(key), bool):
                raise ValueError(f"{key} must be a boolean")
        json.dumps(payload)


def build_civilizational_memory_overlays(
    civilizational_memory_audit: dict[str, Any],
    civilizational_memory_recommendations: dict[str, Any],
    civilizational_memory_map: dict[str, Any],
    intergenerational_legibility_report: dict[str, Any],
    epistemic_resilience_scorecard: dict[str, Any],
    memory_fragility_report: dict[str, Any],
    theory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    civic_literacy_dashboard: dict[str, Any],
    knowledge_priority_registry: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "civilizational_memory_audit": _extract_required_provenance("civilizational_memory_audit", civilizational_memory_audit),
        "civilizational_memory_recommendations": _extract_required_provenance("civilizational_memory_recommendations", civilizational_memory_recommendations),
        "civilizational_memory_map": _extract_required_provenance("civilizational_memory_map", civilizational_memory_map),
        "intergenerational_legibility_report": _extract_required_provenance("intergenerational_legibility_report", intergenerational_legibility_report),
        "epistemic_resilience_scorecard": _extract_required_provenance("epistemic_resilience_scorecard", epistemic_resilience_scorecard),
        "memory_fragility_report": _extract_required_provenance("memory_fragility_report", memory_fragility_report),
    }
    for name, artifact in {
        "theory_dashboard": theory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "civic_literacy_dashboard": civic_literacy_dashboard,
        "knowledge_priority_registry": knowledge_priority_registry,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)
    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [e for e in as_list(civilizational_memory_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(civilizational_memory_recommendations.get("recommendations")) if isinstance(e, dict)]
    memory_entries = [e for e in as_list(civilizational_memory_map.get("entries")) if isinstance(e, dict)]
    legibility_entries = [e for e in as_list(intergenerational_legibility_report.get("entries")) if isinstance(e, dict)]
    resilience_entries = [e for e in as_list(epistemic_resilience_scorecard.get("entries")) if isinstance(e, dict)]
    fragility_entries = [e for e in as_list(memory_fragility_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    memory_by_review = _index_by_key(memory_entries, "reviewId")
    legibility_by_review = _index_by_key(legibility_entries, "reviewId")
    resilience_by_review = _index_by_key(resilience_entries, "reviewId")
    fragility_by_review = _index_by_key(fragility_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    resilience_registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        memory = memory_by_review.get(review_id, {})
        legibility = legibility_by_review.get(review_id, {})
        resilience = resilience_by_review.get(review_id, {})
        fragility = fragility_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        memory_status = str(memory.get("memoryStatus", rec.get("memoryStatus", "monitor")))
        preservation_criticality = str(memory.get("preservationCriticality", rec.get("preservationCriticality", "routine")))
        legibility_persistence = str(legibility.get("legibilityPersistence", rec.get("legibilityPersistence", "bounded")))
        vocabulary_drift_risk = str(fragility.get("vocabularyDriftRisk", rec.get("vocabularyDriftRisk", "bounded")))
        notation_fragility = str(fragility.get("notationFragility", rec.get("notationFragility", "bounded")))
        recoverability = str(resilience.get("recoverability", rec.get("recoverability", "bounded")))
        custody_diversity = str(resilience.get("custodyDiversity", rec.get("custodyDiversity", "mixed")))
        resilience_score = _to_float(resilience.get("epistemicResilienceScore", rec.get("epistemicResilienceScore", 0.0)))
        audit_state = str(audit.get("civilizationalMemoryAuditState", rec.get("civilizationalMemoryAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "memoryStatus": memory_status,
            "preservationCriticality": preservation_criticality,
            "legibilityPersistence": legibility_persistence,
            "vocabularyDriftRisk": vocabulary_drift_risk,
            "notationFragility": notation_fragility,
            "recoverability": recoverability,
            "custodyDiversity": custody_diversity,
            "epistemicResilienceScore": resilience_score,
            "civilizationalMemoryAuditState": audit_state,
            "linkedTargetIds": linked_target_ids,
        }

        if action == "docket":
            dashboard_entries.append({**base, "humanReviewFlag": bool(rec.get("humanReviewFlag", True)), "queuedAt": generated_at})
            resilience_registry_entries.append({**base, "updatedAt": generated_at})

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
            "noCommunityOrTraditionRanking": True,
            "noNegativeResultSuppression": True,
            "noAutomaticTheoryCompetitionClosure": True,
            "noGovernanceRightsMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    civilizational_memory_dashboard = {
        "generatedAt": generated_at,
        "civilizationalMemoryProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noCommunityOrTraditionRanking": True,
        "noNegativeResultSuppression": True,
        "noAutomaticTheoryCompetitionClosure": True,
        "noGovernanceRightsMutation": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    epistemic_resilience_registry = {
        "generatedAt": generated_at,
        "civilizationalMemoryProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noCommunityOrTraditionRanking": True,
        "noNegativeResultSuppression": True,
        "noAutomaticTheoryCompetitionClosure": True,
        "noGovernanceRightsMutation": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(resilience_registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    memory_fragility_watchlist = {
        "generatedAt": generated_at,
        "civilizationalMemoryProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noCommunityOrTraditionRanking": True,
        "noNegativeResultSuppression": True,
        "noAutomaticTheoryCompetitionClosure": True,
        "noGovernanceRightsMutation": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    civilizational_memory_annotations = {
        "generatedAt": generated_at,
        "civilizationalMemoryProtocol": True,
        "nonCanonical": True,
        "noCanonMutation": True,
        "noCommunityOrTraditionRanking": True,
        "noNegativeResultSuppression": True,
        "noAutomaticTheoryCompetitionClosure": True,
        "noGovernanceRightsMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        **integrity_status,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(civilizational_memory_dashboard, epistemic_resilience_registry, memory_fragility_watchlist, civilizational_memory_annotations)
    return civilizational_memory_dashboard, epistemic_resilience_registry, memory_fragility_watchlist, civilizational_memory_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--civilizational-memory-audit", type=Path, default=Path("bridge/civilizational_memory_audit.json"))
    parser.add_argument("--civilizational-memory-recommendations", type=Path, default=Path("bridge/civilizational_memory_recommendations.json"))
    parser.add_argument("--civilizational-memory-map", type=Path, default=Path("bridge/civilizational_memory_map.json"))
    parser.add_argument("--intergenerational-legibility-report", type=Path, default=Path("bridge/intergenerational_legibility_report.json"))
    parser.add_argument("--epistemic-resilience-scorecard", type=Path, default=Path("bridge/epistemic_resilience_scorecard.json"))
    parser.add_argument("--memory-fragility-report", type=Path, default=Path("bridge/memory_fragility_report.json"))

    parser.add_argument("--theory-dashboard", type=Path, default=Path("registry/theory_dashboard.json"))
    parser.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    parser.add_argument("--civic-literacy-dashboard", type=Path, default=Path("registry/civic_literacy_dashboard.json"))
    parser.add_argument("--knowledge-priority-registry", type=Path, default=Path("registry/knowledge_priority_registry.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    parser.add_argument("--out-epistemic-resilience-registry", type=Path, default=Path("registry/epistemic_resilience_registry.json"))
    parser.add_argument("--out-memory-fragility-watchlist", type=Path, default=Path("registry/memory_fragility_watchlist.json"))
    parser.add_argument("--out-civilizational-memory-annotations", type=Path, default=Path("registry/civilizational_memory_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_civilizational_memory_overlays(
            load_required_json(args.civilizational_memory_audit),
            load_required_json(args.civilizational_memory_recommendations),
            load_required_json(args.civilizational_memory_map),
            load_required_json(args.intergenerational_legibility_report),
            load_required_json(args.epistemic_resilience_scorecard),
            load_required_json(args.memory_fragility_report),
            load_required_json(args.theory_dashboard),
            load_required_json(args.commons_sovereignty_dashboard),
            load_required_json(args.civic_literacy_dashboard),
            load_required_json(args.knowledge_priority_registry),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_civilizational_memory_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_epistemic_resilience_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_memory_fragility_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_civilizational_memory_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_civilizational_memory_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_epistemic_resilience_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_memory_fragility_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_civilizational_memory_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote civilizational memory dashboard: {args.out_civilizational_memory_dashboard}")
    print(f"[OK] Wrote epistemic resilience registry: {args.out_epistemic_resilience_registry}")
    print(f"[OK] Wrote memory fragility watchlist: {args.out_memory_fragility_watchlist}")
    print(f"[OK] Wrote civilizational memory annotations: {args.out_civilizational_memory_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
