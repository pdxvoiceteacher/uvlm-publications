#!/usr/bin/env python3
"""Build commons participation and cognitive literacy overlays.

Publisher surfaces only Sophia-audited commons-participation materials; no
automatic exclusion, ranking of persons, or prestige hierarchies occur from
this layer.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

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


def _validate_outputs(civic_literacy_dashboard: dict[str, Any], participation_registry: dict[str, Any], accessibility_watchlist: dict[str, Any], commons_annotations: dict[str, Any]) -> None:
    if not isinstance(civic_literacy_dashboard.get("entries"), list):
        raise ValueError("civic_literacy_dashboard.entries must be a list")
    if not isinstance(participation_registry.get("entries"), list):
        raise ValueError("participation_registry.entries must be a list")
    if not isinstance(accessibility_watchlist.get("entries"), list):
        raise ValueError("accessibility_watchlist.entries must be a list")
    if not isinstance(commons_annotations.get("annotations"), list):
        raise ValueError("commons_annotations.annotations must be a list")
    for payload in (civic_literacy_dashboard, participation_registry, accessibility_watchlist, commons_annotations):
        json.dumps(payload)


def build_commons_participation_overlays(
    commons_participation_audit: dict[str, Any],
    commons_participation_recommendations: dict[str, Any],
    civic_literacy_map: dict[str, Any],
    participation_barrier_report: dict[str, Any],
    commons_accessibility_index: dict[str, Any],
    epistemic_legibility_map: dict[str, Any],
    social_entropy_dashboard: dict[str, Any],
    federation_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    architecture_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "commons_participation_audit": _extract_required_provenance("commons_participation_audit", commons_participation_audit),
        "commons_participation_recommendations": _extract_required_provenance("commons_participation_recommendations", commons_participation_recommendations),
        "civic_literacy_map": _extract_required_provenance("civic_literacy_map", civic_literacy_map),
        "participation_barrier_report": _extract_required_provenance("participation_barrier_report", participation_barrier_report),
        "commons_accessibility_index": _extract_required_provenance("commons_accessibility_index", commons_accessibility_index),
        "epistemic_legibility_map": _extract_required_provenance("epistemic_legibility_map", epistemic_legibility_map),
    }
    for name, artifact in {
        "social_entropy_dashboard": social_entropy_dashboard,
        "federation_dashboard": federation_dashboard,
        "value_dashboard": value_dashboard,
        "architecture_dashboard": architecture_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(commons_participation_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(commons_participation_recommendations.get("recommendations")) if isinstance(e, dict)]
    literacy_entries = [e for e in as_list(civic_literacy_map.get("entries")) if isinstance(e, dict)]
    barrier_entries = [e for e in as_list(participation_barrier_report.get("entries")) if isinstance(e, dict)]
    accessibility_entries = [e for e in as_list(commons_accessibility_index.get("entries")) if isinstance(e, dict)]
    legibility_entries = [e for e in as_list(epistemic_legibility_map.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    literacy_by_review = _index_by_key(literacy_entries, "reviewId")
    barrier_by_review = _index_by_key(barrier_entries, "reviewId")
    accessibility_by_review = _index_by_key(accessibility_entries, "reviewId")
    legibility_by_review = _index_by_key(legibility_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        lit = literacy_by_review.get(review_id, {})
        bar = barrier_by_review.get(review_id, {})
        acc = accessibility_by_review.get(review_id, {})
        leg = legibility_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        participation_status = str(lit.get("participationStatus", rec.get("participationStatus", "monitor")))
        literacy_class = str(lit.get("literacyClass", rec.get("literacyClass", "mixed")))
        accessibility_class = str(acc.get("accessibilityClass", rec.get("accessibilityClass", "mixed")))
        participation_barriers = sorted([x for x in as_list(bar.get("participationBarriers", rec.get("participationBarriers", []))) if isinstance(x, str)])
        negative_result_visibility = str(leg.get("negativeResultVisibility", rec.get("negativeResultVisibility", "bounded")))
        dissent_visibility = str(leg.get("dissentVisibility", rec.get("dissentVisibility", "bounded")))
        legibility_score = _to_float(leg.get("legibilityScore", rec.get("legibilityScore", 0.0)))
        audit_state = str(audit.get("commonsParticipationAuditState", rec.get("commonsParticipationAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "participationStatus": participation_status,
            "literacyClass": literacy_class,
            "accessibilityClass": accessibility_class,
            "participationBarriers": participation_barriers,
            "negativeResultVisibility": negative_result_visibility,
            "dissentVisibility": dissent_visibility,
            "legibilityScore": legibility_score,
            "commonsParticipationAuditState": audit_state,
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
            "noAutomaticExclusion": True,
            "noRankingOfPersons": True,
            "noPrestigeHierarchies": True,
            "noTheoryStatusMutation": True,
            "noIdentityMutation": True,
            "noGovernanceRightsMutation": True,
            "noParticipationRightsMutation": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    civic_literacy_dashboard = {
        "generatedAt": generated_at,
        "commonsParticipationProtocol": True,
        "nonCanonical": True,
        "noAutomaticExclusion": True,
        "noRankingOfPersons": True,
        "noPrestigeHierarchies": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    participation_registry = {
        "generatedAt": generated_at,
        "commonsParticipationProtocol": True,
        "nonCanonical": True,
        "noAutomaticExclusion": True,
        "noRankingOfPersons": True,
        "noPrestigeHierarchies": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    accessibility_watchlist = {
        "generatedAt": generated_at,
        "commonsParticipationProtocol": True,
        "nonCanonical": True,
        "noAutomaticExclusion": True,
        "noRankingOfPersons": True,
        "noPrestigeHierarchies": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    commons_annotations = {
        "generatedAt": generated_at,
        "commonsParticipationProtocol": True,
        "nonCanonical": True,
        "noAutomaticExclusion": True,
        "noRankingOfPersons": True,
        "noPrestigeHierarchies": True,
        "noTheoryStatusMutation": True,
        "noIdentityMutation": True,
        "noGovernanceRightsMutation": True,
        "noParticipationRightsMutation": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(civic_literacy_dashboard, participation_registry, accessibility_watchlist, commons_annotations)
    return civic_literacy_dashboard, participation_registry, accessibility_watchlist, commons_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commons-participation-audit", type=Path, default=Path("bridge/commons_participation_audit.json"))
    parser.add_argument("--commons-participation-recommendations", type=Path, default=Path("bridge/commons_participation_recommendations.json"))
    parser.add_argument("--civic-literacy-map", type=Path, default=Path("bridge/civic_literacy_map.json"))
    parser.add_argument("--participation-barrier-report", type=Path, default=Path("bridge/participation_barrier_report.json"))
    parser.add_argument("--commons-accessibility-index", type=Path, default=Path("bridge/commons_accessibility_index.json"))
    parser.add_argument("--epistemic-legibility-map", type=Path, default=Path("bridge/epistemic_legibility_map.json"))

    parser.add_argument("--social-entropy-dashboard", type=Path, default=Path("registry/social_entropy_dashboard.json"))
    parser.add_argument("--federation-dashboard", type=Path, default=Path("registry/federation_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))
    parser.add_argument("--architecture-dashboard", type=Path, default=Path("registry/architecture_dashboard.json"))

    parser.add_argument("--out-civic-literacy-dashboard", type=Path, default=Path("registry/civic_literacy_dashboard.json"))
    parser.add_argument("--out-participation-registry", type=Path, default=Path("registry/participation_registry.json"))
    parser.add_argument("--out-accessibility-watchlist", type=Path, default=Path("registry/accessibility_watchlist.json"))
    parser.add_argument("--out-commons-annotations", type=Path, default=Path("registry/commons_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_commons_participation_overlays(
            load_required_json(args.commons_participation_audit),
            load_required_json(args.commons_participation_recommendations),
            load_required_json(args.civic_literacy_map),
            load_required_json(args.participation_barrier_report),
            load_required_json(args.commons_accessibility_index),
            load_required_json(args.epistemic_legibility_map),
            load_required_json(args.social_entropy_dashboard),
            load_required_json(args.federation_dashboard),
            load_required_json(args.value_dashboard),
            load_required_json(args.architecture_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_civic_literacy_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_participation_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_accessibility_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_commons_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_civic_literacy_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_participation_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_accessibility_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_commons_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote civic literacy dashboard: {args.out_civic_literacy_dashboard}")
    print(f"[OK] Wrote participation registry: {args.out_participation_registry}")
    print(f"[OK] Wrote accessibility watchlist: {args.out_accessibility_watchlist}")
    print(f"[OK] Wrote commons annotations: {args.out_commons_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
