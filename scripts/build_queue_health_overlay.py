#!/usr/bin/env python3
"""Build queue-pressure, anti-Goodhart, and load-shedding overlays.

This script surfaces Sophia-audited operational queue-health materials as
bounded, non-canonical publisher artifacts. It does not mutate canonical truth,
queues, dockets, or governance truth artifacts.
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
    if not isinstance(prov.get("schemaVersion"), str):
        raise ValueError(f"{name} provenance.schemaVersion must be a string")
    if not isinstance(prov.get("producerCommits"), list) or not all(
        isinstance(v, str) for v in prov.get("producerCommits", [])
    ):
        raise ValueError(f"{name} provenance.producerCommits must be a list of strings")
    if not isinstance(prov.get("sourceMode"), str):
        raise ValueError(f"{name} provenance.sourceMode must be a string")
    return prov


def _extract_optional_provenance(name: str, artifact: dict[str, Any]) -> dict[str, Any] | None:
    prov = artifact.get("provenance")
    if not isinstance(prov, dict):
        return None
    if not isinstance(prov.get("schemaVersions"), dict):
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

    derived_from_fixtures = any(mode.lower() == "fixture" for mode in source_modes.values())
    return {
        "schemaVersions": schema_versions,
        "producerCommits": producer_commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": derived_from_fixtures,
    }


def _review_id_set(artifact: dict[str, Any]) -> set[str]:
    return {
        str(e.get("reviewId"))
        for e in as_list(artifact.get("entries"))
        if isinstance(e, dict) and isinstance(e.get("reviewId"), str)
    }


def build_queue_health_overlays(
    load_shedding_audit: dict[str, Any],
    load_shedding_recommendations: dict[str, Any],
    queue_pressure_map: dict[str, Any],
    queue_pressure_summary: dict[str, Any],
    review_load_distribution: dict[str, Any],
    goodhart_risk_report: dict[str, Any],
    institutional_status: dict[str, Any],
    system_health_dashboard: dict[str, Any],
    review_docket: dict[str, Any],
    governance_review_docket: dict[str, Any],
    deliberation_docket: dict[str, Any],
    recovery_docket: dict[str, Any],
    witness_docket: dict[str, Any],
    case_docket: dict[str, Any],
    stress_test_docket: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "load_shedding_audit": _extract_required_provenance("load_shedding_audit", load_shedding_audit),
        "load_shedding_recommendations": _extract_required_provenance(
            "load_shedding_recommendations", load_shedding_recommendations
        ),
        "queue_pressure_map": _extract_required_provenance("queue_pressure_map", queue_pressure_map),
        "queue_pressure_summary": _extract_required_provenance("queue_pressure_summary", queue_pressure_summary),
        "review_load_distribution": _extract_required_provenance(
            "review_load_distribution", review_load_distribution
        ),
        "goodhart_risk_report": _extract_required_provenance("goodhart_risk_report", goodhart_risk_report),
    }

    for optional_name, artifact in {
        "institutional_status": institutional_status,
        "system_health_dashboard": system_health_dashboard,
    }.items():
        optional = _extract_optional_provenance(optional_name, artifact)
        if optional:
            provenances[optional_name] = optional

    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(load_shedding_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(load_shedding_recommendations.get("recommendations")) if isinstance(r, dict)]
    pressure_entries = [e for e in as_list(queue_pressure_map.get("entries")) if isinstance(e, dict)]
    summary_entries = [e for e in as_list(queue_pressure_summary.get("entries")) if isinstance(e, dict)]
    load_entries = [e for e in as_list(review_load_distribution.get("entries")) if isinstance(e, dict)]
    goodhart_entries = [e for e in as_list(goodhart_risk_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    pressure_by_review = _index_by_key(pressure_entries, "reviewId")
    summary_by_review = _index_by_key(summary_entries, "reviewId")
    load_by_review = _index_by_key(load_entries, "reviewId")
    goodhart_by_review = _index_by_key(goodhart_entries, "reviewId")

    docket_sets = {
        "review": _review_id_set(review_docket),
        "governance": _review_id_set(governance_review_docket),
        "deliberation": _review_id_set(deliberation_docket),
        "recovery": _review_id_set(recovery_docket),
        "witness": _review_id_set(witness_docket),
        "case": _review_id_set(case_docket),
        "stress": _review_id_set(stress_test_docket),
    }

    queue_health_entries: list[dict[str, Any]] = []
    review_backlog_entries: list[dict[str, Any]] = []
    metric_gaming_entries: list[dict[str, Any]] = []
    load_shedding_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        audit = audit_by_review.get(review_id, {})
        pressure = pressure_by_review.get(review_id, {})
        summary = summary_by_review.get(review_id, {})
        load = load_by_review.get(review_id, {})
        goodhart = goodhart_by_review.get(review_id, {})

        queue_status = str(pressure.get("queueStatus", summary.get("queueStatus", rec.get("queueStatus", "normal"))))
        backlog_pressure = str(
            pressure.get("backlogPressure", summary.get("backlogPressure", rec.get("backlogPressure", "low")))
        )
        fatigue_load_class = str(load.get("fatigueLoadClass", rec.get("fatigueLoadClass", "normal")))
        metric_gaming_watch_status = str(
            goodhart.get("metricGamingWatchStatus", rec.get("metricGamingWatchStatus", "none"))
        )
        load_shedding_recommendation_summary = str(
            summary.get(
                "loadSheddingRecommendationSummary",
                rec.get("loadSheddingRecommendationSummary", "none"),
            )
        )
        watch_state = str(audit.get("watchState", rec.get("watchState", "none")))
        watchlist_target = str(rec.get("watchlistTarget", "review_backlog_watchlist")).strip().lower()

        linked_target_ids = sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])

        if action == "docket":
            queue_health_entries.append(
                {
                    "reviewId": review_id,
                    "queueId": rec.get("queueId"),
                    "status": "docketed",
                    "queueStatus": queue_status,
                    "backlogPressure": backlog_pressure,
                    "fatigueLoadClass": fatigue_load_class,
                    "metricGamingWatchStatus": metric_gaming_watch_status,
                    "loadSheddingRecommendationSummary": load_shedding_recommendation_summary,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "crossDocketPresence": {
                        key: review_id in value for key, value in docket_sets.items()
                    },
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

        if action == "watch":
            watch_entry = {
                "reviewId": review_id,
                "queueId": rec.get("queueId"),
                "status": "watch",
                "queueStatus": queue_status,
                "backlogPressure": backlog_pressure,
                "fatigueLoadClass": fatigue_load_class,
                "metricGamingWatchStatus": metric_gaming_watch_status,
                "loadSheddingRecommendationSummary": load_shedding_recommendation_summary,
                "watchState": watch_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                "observational": True,
                "nonCanonical": True,
                "queuedAt": generated_at,
            }
            if watchlist_target == "metric_gaming_watchlist":
                metric_gaming_entries.append(watch_entry)
            else:
                review_backlog_entries.append(watch_entry)

        load_shedding_annotations.append(
            {
                "reviewId": review_id,
                "queueId": rec.get("queueId"),
                "targetPublisherAction": action,
                "queueStatus": queue_status,
                "backlogPressure": backlog_pressure,
                "fatigueLoadClass": fatigue_load_class,
                "metricGamingWatchStatus": metric_gaming_watch_status,
                "loadSheddingRecommendationSummary": load_shedding_recommendation_summary,
                "watchState": watch_state,
                "linkedTargetIds": linked_target_ids,
                "watchlistTarget": watchlist_target,
                "noAutomaticQueueMutation": True,
                "noAutomaticArchival": True,
                "noAutomaticFreeze": True,
                "noAutomaticDeletion": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", summary.get("notes", "")),
            }
        )

    queue_health_dashboard = {
        "generatedAt": generated_at,
        "operationalQueueHealth": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(queue_health_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    review_backlog_watchlist = {
        "generatedAt": generated_at,
        "operationalQueueHealth": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(review_backlog_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    metric_gaming_watchlist = {
        "generatedAt": generated_at,
        "operationalQueueHealth": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(metric_gaming_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    load_shedding_annotations_artifact = {
        "generatedAt": generated_at,
        "operationalQueueHealth": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticQueueMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(load_shedding_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return (
        queue_health_dashboard,
        review_backlog_watchlist,
        metric_gaming_watchlist,
        load_shedding_annotations_artifact,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--load-shedding-audit", type=Path, default=Path("bridge/load_shedding_audit.json"))
    parser.add_argument(
        "--load-shedding-recommendations", type=Path, default=Path("bridge/load_shedding_recommendations.json")
    )
    parser.add_argument("--queue-pressure-map", type=Path, default=Path("bridge/queue_pressure_map.json"))
    parser.add_argument("--queue-pressure-summary", type=Path, default=Path("bridge/queue_pressure_summary.json"))
    parser.add_argument(
        "--review-load-distribution", type=Path, default=Path("bridge/review_load_distribution.json")
    )
    parser.add_argument("--goodhart-risk-report", type=Path, default=Path("bridge/goodhart_risk_report.json"))
    parser.add_argument("--queue-health-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--institutional-status", type=Path, default=Path("registry/institutional_status.json"))
    parser.add_argument(
        "--system-health-dashboard", type=Path, default=Path("registry/system_health_dashboard.json")
    )
    parser.add_argument("--review-docket", type=Path, default=Path("registry/review_docket.json"))
    parser.add_argument(
        "--governance-review-docket", type=Path, default=Path("registry/governance_review_docket.json")
    )
    parser.add_argument("--deliberation-docket", type=Path, default=Path("registry/deliberation_docket.json"))
    parser.add_argument("--recovery-docket", type=Path, default=Path("registry/recovery_docket.json"))
    parser.add_argument("--witness-docket", type=Path, default=Path("registry/witness_docket.json"))
    parser.add_argument("--case-docket", type=Path, default=Path("registry/case_docket.json"))
    parser.add_argument("--stress-test-docket", type=Path, default=Path("registry/stress_test_docket.json"))

    parser.add_argument(
        "--out-queue-health-dashboard", type=Path, default=Path("registry/queue_health_dashboard.json")
    )
    parser.add_argument(
        "--out-review-backlog-watchlist", type=Path, default=Path("registry/review_backlog_watchlist.json")
    )
    parser.add_argument(
        "--out-metric-gaming-watchlist", type=Path, default=Path("registry/metric_gaming_watchlist.json")
    )
    parser.add_argument(
        "--out-load-shedding-annotations", type=Path, default=Path("registry/load_shedding_annotations.json")
    )

    args = parser.parse_args()

    if args.queue_health_snapshot is not None:
        print(
            "[ERROR] Deprecated artifact alias detected: --queue-health-snapshot is no longer supported. "
            "Use canonical queue pressure and Goodhart artifacts.",
        )
        return 2

    try:
        outputs = build_queue_health_overlays(
            load_required_json(args.load_shedding_audit),
            load_required_json(args.load_shedding_recommendations),
            load_required_json(args.queue_pressure_map),
            load_required_json(args.queue_pressure_summary),
            load_required_json(args.review_load_distribution),
            load_required_json(args.goodhart_risk_report),
            load_required_json(args.institutional_status),
            load_required_json(args.system_health_dashboard),
            load_required_json(args.review_docket),
            load_required_json(args.governance_review_docket),
            load_required_json(args.deliberation_docket),
            load_required_json(args.recovery_docket),
            load_required_json(args.witness_docket),
            load_required_json(args.case_docket),
            load_required_json(args.stress_test_docket),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_queue_health_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_review_backlog_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_metric_gaming_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_load_shedding_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote queue health dashboard: {args.out_queue_health_dashboard}")
    print(f"[OK] Wrote review backlog watchlist: {args.out_review_backlog_watchlist}")
    print(f"[OK] Wrote metric gaming watchlist: {args.out_metric_gaming_watchlist}")
    print(f"[OK] Wrote load shedding annotations: {args.out_load_shedding_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
