#!/usr/bin/env python3
"""Build institutional synthesis and system-health overlays.

This script consumes canonical institutional upstream artifacts and surfaces
Sophia-audited institutional materials as bounded, non-canonical publisher
artifacts. It does not mutate canonical truth or governance truth.
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


def _extract_provenance(name: str, artifact: dict[str, Any]) -> dict[str, Any]:
    prov = artifact.get("provenance")
    if not isinstance(prov, dict):
        raise ValueError(f"{name} missing required provenance metadata")
    for key in REQUIRED_PROVENANCE_KEYS:
        if key not in prov:
            raise ValueError(f"{name} provenance missing required field: {key}")
    if not isinstance(prov.get("schemaVersion"), str):
        raise ValueError(f"{name} provenance.schemaVersion must be a string")
    if not isinstance(prov.get("producerCommits"), list) or not all(
        isinstance(v, str) for v in prov.get("producerCommits", [])
    ):
        raise ValueError(f"{name} provenance.producerCommits must be a list of strings")
    if not isinstance(prov.get("sourceMode"), str):
        raise ValueError(f"{name} provenance.sourceMode must be a string")
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

    derived_from_fixtures = any(mode.lower() == "fixture" for mode in source_modes.values())
    return {
        "schemaVersions": schema_versions,
        "producerCommits": producer_commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": derived_from_fixtures,
    }


def build_institutional_overlays(
    institutional_audit: dict[str, Any],
    institutional_recommendations: dict[str, Any],
    institutional_state_map: dict[str, Any],
    institutional_state_summary: dict[str, Any],
    institutional_conflict_report: dict[str, Any],
    institutional_health_projection: dict[str, Any],
    governance_review_docket: dict[str, Any],
    quorum_resilience_watchlist: dict[str, Any],
    integrity_testimony_watchlist: dict[str, Any],
    divergence_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "institutional_audit": _extract_provenance("institutional_audit", institutional_audit),
        "institutional_recommendations": _extract_provenance(
            "institutional_recommendations", institutional_recommendations
        ),
        "institutional_state_map": _extract_provenance("institutional_state_map", institutional_state_map),
        "institutional_state_summary": _extract_provenance(
            "institutional_state_summary", institutional_state_summary
        ),
        "institutional_conflict_report": _extract_provenance(
            "institutional_conflict_report", institutional_conflict_report
        ),
        "institutional_health_projection": _extract_provenance(
            "institutional_health_projection", institutional_health_projection
        ),
    }
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(institutional_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(institutional_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(institutional_state_map.get("entries")) if isinstance(s, dict)]
    summaries = [s for s in as_list(institutional_state_summary.get("entries")) if isinstance(s, dict)]
    conflicts = [c for c in as_list(institutional_conflict_report.get("entries")) if isinstance(c, dict)]
    projections = [p for p in as_list(institutional_health_projection.get("entries")) if isinstance(p, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
    summary_by_review = _index_by_key(summaries, "reviewId")
    conflict_by_review = _index_by_key(conflicts, "reviewId")
    projection_by_review = _index_by_key(projections, "reviewId")

    governance_ids = {
        e.get("reviewId") for e in as_list(governance_review_docket.get("entries")) if isinstance(e, dict)
    }
    quorum_ids = {
        e.get("reviewId") for e in as_list(quorum_resilience_watchlist.get("entries")) if isinstance(e, dict)
    }
    testimony_ids = {
        e.get("reviewId") for e in as_list(integrity_testimony_watchlist.get("entries")) if isinstance(e, dict)
    }
    divergence_ids = {
        e.get("reviewId") for e in as_list(divergence_watchlist.get("entries")) if isinstance(e, dict)
    }

    institutional_status_entries: list[dict[str, Any]] = []
    system_health_entries: list[dict[str, Any]] = []
    institutional_conflicts_entries: list[dict[str, Any]] = []
    institutional_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        audit = audit_by_review.get(review_id, {})
        state = state_by_review.get(review_id, {})
        summary = summary_by_review.get(review_id, {})
        conflict = conflict_by_review.get(review_id, {})
        projection = projection_by_review.get(review_id, {})

        institutional_status = str(
            state.get("institutionalStatus", summary.get("institutionalStatus", rec.get("institutionalStatus", "review-pending")))
        )
        chamber_conflict_level = str(
            conflict.get("chamberConflictLevel", state.get("chamberConflictLevel", rec.get("chamberConflictLevel", "none")))
        )
        system_health_score = float(
            projection.get("systemHealthScore", summary.get("systemHealthScore", rec.get("systemHealthScore", 0.0)))
        )
        system_health_overview = str(
            projection.get(
                "systemHealthOverview",
                summary.get("systemHealthOverview", rec.get("systemHealthOverview", "bounded-rehearsal")),
            )
        )
        watch_state = str(audit.get("watchState", rec.get("watchState", "none")))

        linked_target_ids = sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])

        if action == "docket":
            institutional_status_entries.append(
                {
                    "institutionId": rec.get("institutionId"),
                    "reviewId": review_id,
                    "institutionalStatus": institutional_status,
                    "chamberConflictLevel": chamber_conflict_level,
                    "systemHealthScore": system_health_score,
                    "systemHealthOverview": system_health_overview,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "crossChamberLinks": {
                        "governance": review_id in governance_ids,
                        "quorumResilience": review_id in quorum_ids,
                        "integrityTestimony": review_id in testimony_ids,
                        "precedentDivergence": review_id in divergence_ids,
                    },
                }
            )
            system_health_entries.append(
                {
                    "reviewId": review_id,
                    "institutionId": rec.get("institutionId"),
                    "status": "docketed",
                    "institutionalStatus": institutional_status,
                    "chamberConflictLevel": chamber_conflict_level,
                    "systemHealthScore": system_health_score,
                    "systemHealthOverview": system_health_overview,
                    "preparednessRecommendation": rec.get("preparednessRecommendation", "bounded-rehearsal"),
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

        if action == "watch":
            institutional_conflicts_entries.append(
                {
                    "reviewId": review_id,
                    "institutionId": rec.get("institutionId"),
                    "status": "watch",
                    "institutionalStatus": institutional_status,
                    "chamberConflictLevel": chamber_conflict_level,
                    "systemHealthScore": system_health_score,
                    "systemHealthOverview": system_health_overview,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        institutional_annotations.append(
            {
                "reviewId": review_id,
                "institutionId": rec.get("institutionId"),
                "targetPublisherAction": action,
                "institutionalStatus": institutional_status,
                "chamberConflictLevel": chamber_conflict_level,
                "systemHealthScore": system_health_score,
                "systemHealthOverview": system_health_overview,
                "watchState": watch_state,
                "linkedTargetIds": linked_target_ids,
                "boundedRecommendation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", projection.get("notes", summary.get("notes", ""))),
            }
        )

    institutional_status = {
        "generatedAt": generated_at,
        "institutionalSynthesis": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(institutional_status_entries, key=lambda e: str(e.get("institutionId", ""))),
    }

    system_health_dashboard = {
        "generatedAt": generated_at,
        "institutionalSynthesis": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(system_health_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    institutional_conflict_watchlist = {
        "generatedAt": generated_at,
        "institutionalSynthesis": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(institutional_conflicts_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    institutional_annotations_artifact = {
        "generatedAt": generated_at,
        "institutionalSynthesis": True,
        "nonCanonical": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        "annotations": sorted(institutional_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return (
        institutional_status,
        system_health_dashboard,
        institutional_conflict_watchlist,
        institutional_annotations_artifact,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--institutional-audit", type=Path, default=Path("bridge/institutional_audit.json"))
    parser.add_argument(
        "--institutional-recommendations",
        type=Path,
        default=Path("bridge/institutional_recommendations.json"),
    )
    parser.add_argument("--institutional-state-map", type=Path, default=Path("bridge/institutional_state_map.json"))
    parser.add_argument(
        "--institutional-state-summary",
        type=Path,
        default=Path("bridge/institutional_state_summary.json"),
    )
    parser.add_argument(
        "--institutional-conflict-report",
        type=Path,
        default=Path("bridge/institutional_conflict_report.json"),
    )
    parser.add_argument(
        "--institutional-health-projection",
        type=Path,
        default=Path("bridge/institutional_health_projection.json"),
    )
    parser.add_argument("--institutional-synthesis", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--governance-review-docket", type=Path, default=Path("registry/governance_review_docket.json"))
    parser.add_argument(
        "--quorum-resilience-watchlist", type=Path, default=Path("registry/quorum_resilience_watchlist.json")
    )
    parser.add_argument(
        "--integrity-testimony-watchlist", type=Path, default=Path("registry/integrity_testimony_watchlist.json")
    )
    parser.add_argument("--divergence-watchlist", type=Path, default=Path("registry/divergence_watchlist.json"))

    parser.add_argument("--out-institutional-status", type=Path, default=Path("registry/institutional_status.json"))
    parser.add_argument(
        "--out-system-health-dashboard", type=Path, default=Path("registry/system_health_dashboard.json")
    )
    parser.add_argument(
        "--out-institutional-conflict-watchlist",
        type=Path,
        default=Path("registry/institutional_conflict_watchlist.json"),
    )
    parser.add_argument(
        "--out-institutional-annotations", type=Path, default=Path("registry/institutional_annotations.json")
    )

    args = parser.parse_args()

    if args.institutional_synthesis is not None:
        print(
            "[ERROR] Deprecated artifact alias detected: --institutional-synthesis is no longer supported. "
            "Use canonical artifacts: institutional_state_summary, institutional_conflict_report, "
            "institutional_health_projection.",
        )
        return 2

    try:
        outputs = build_institutional_overlays(
            load_required_json(args.institutional_audit),
            load_required_json(args.institutional_recommendations),
            load_required_json(args.institutional_state_map),
            load_required_json(args.institutional_state_summary),
            load_required_json(args.institutional_conflict_report),
            load_required_json(args.institutional_health_projection),
            load_required_json(args.governance_review_docket),
            load_required_json(args.quorum_resilience_watchlist),
            load_required_json(args.integrity_testimony_watchlist),
            load_required_json(args.divergence_watchlist),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_institutional_status.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_system_health_dashboard.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_institutional_conflict_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_institutional_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote institutional status: {args.out_institutional_status}")
    print(f"[OK] Wrote system health dashboard: {args.out_system_health_dashboard}")
    print(f"[OK] Wrote institutional conflict watchlist: {args.out_institutional_conflict_watchlist}")
    print(f"[OK] Wrote institutional annotations: {args.out_institutional_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
