#!/usr/bin/env python3
"""Build resolution priority and triage overlays.

This script surfaces Sophia-audited triage and priority materials as bounded,
review-facing non-canonical artifacts. It does not mutate queues, dockets,
or canonical truth artifacts.
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
    if not isinstance(prov.get("producerCommits"), list) or not all(isinstance(v, str) for v in prov.get("producerCommits", [])):
        raise ValueError(f"{name} provenance.producerCommits must be a list of strings")
    if not isinstance(prov.get("sourceMode"), str):
        raise ValueError(f"{name} provenance.sourceMode must be a string")
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
    derived_from_fixtures = any(mode.lower() == "fixture" for mode in source_modes.values())
    return {
        "schemaVersions": schema_versions,
        "producerCommits": producer_commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": derived_from_fixtures,
    }


def build_priority_overlays(
    triage_audit: dict[str, Any],
    triage_recommendations: dict[str, Any],
    priority_state_map: dict[str, Any],
    priority_state_summary: dict[str, Any],
    triage_candidate_map: dict[str, Any],
    triage_conflict_report: dict[str, Any],
    queue_health_dashboard: dict[str, Any],
    system_health_dashboard: dict[str, Any],
    review_backlog_watchlist: dict[str, Any],
    metric_gaming_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "triage_audit": _extract_required_provenance("triage_audit", triage_audit),
        "triage_recommendations": _extract_required_provenance("triage_recommendations", triage_recommendations),
        "priority_state_map": _extract_required_provenance("priority_state_map", priority_state_map),
        "priority_state_summary": _extract_required_provenance("priority_state_summary", priority_state_summary),
        "triage_candidate_map": _extract_required_provenance("triage_candidate_map", triage_candidate_map),
        "triage_conflict_report": _extract_required_provenance("triage_conflict_report", triage_conflict_report),
    }
    for optional_name, artifact in {
        "queue_health_dashboard": queue_health_dashboard,
        "system_health_dashboard": system_health_dashboard,
        "review_backlog_watchlist": review_backlog_watchlist,
        "metric_gaming_watchlist": metric_gaming_watchlist,
    }.items():
        optional = _extract_optional_provenance(optional_name, artifact)
        if optional:
            provenances[optional_name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(triage_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(triage_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(priority_state_map.get("entries")) if isinstance(s, dict)]
    summaries = [s for s in as_list(priority_state_summary.get("entries")) if isinstance(s, dict)]
    candidates = [c for c in as_list(triage_candidate_map.get("candidates")) if isinstance(c, dict)]
    conflicts = [c for c in as_list(triage_conflict_report.get("entries")) if isinstance(c, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
    summary_by_review = _index_by_key(summaries, "reviewId")
    candidate_by_id = _index_by_key(candidates, "candidateId")
    conflict_by_review = _index_by_key(conflicts, "reviewId")

    priority_dashboard_entries: list[dict[str, Any]] = []
    triage_docket_entries: list[dict[str, Any]] = []
    triage_watchlist_entries: list[dict[str, Any]] = []
    priority_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        candidate = candidate_by_id.get(rec.get("candidateId"), {}) if isinstance(rec.get("candidateId"), str) else {}
        audit = audit_by_review.get(review_id, {})
        state = state_by_review.get(review_id, {})
        summary = summary_by_review.get(review_id, {})
        conflict = conflict_by_review.get(review_id, {})

        triage_status = str(state.get("triageStatus", summary.get("triageStatus", rec.get("triageStatus", "pending"))))
        urgency_level = str(state.get("urgencyLevel", summary.get("urgencyLevel", rec.get("urgencyLevel", "routine"))))
        priority_class = str(state.get("priorityClass", summary.get("priorityClass", rec.get("priorityClass", "standard"))))
        triage_conflict_status = str(conflict.get("triageConflictStatus", rec.get("triageConflictStatus", "none")))
        recommendation_summary = str(summary.get("recommendationSummary", rec.get("recommendationSummary", "none")))
        watch_state = str(audit.get("watchState", rec.get("watchState", "none")))
        linked_target_ids = sorted([t for t in as_list(rec.get("linkedTargetIds", candidate.get("linkedTargetIds"))) if isinstance(t, str)])

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "candidateId": rec.get("candidateId"),
                "triageStatus": triage_status,
                "urgencyLevel": urgency_level,
                "priorityClass": priority_class,
                "triageConflictStatus": triage_conflict_status,
                "recommendationSummary": recommendation_summary,
                "watchState": watch_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            priority_dashboard_entries.append(entry)
            triage_docket_entries.append({**entry, "status": "docketed"})

        if action == "watch":
            triage_watchlist_entries.append(
                {
                    "reviewId": review_id,
                    "candidateId": rec.get("candidateId"),
                    "status": "watch",
                    "triageStatus": triage_status,
                    "urgencyLevel": urgency_level,
                    "priorityClass": priority_class,
                    "triageConflictStatus": triage_conflict_status,
                    "recommendationSummary": recommendation_summary,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        priority_annotations.append(
            {
                "reviewId": review_id,
                "candidateId": rec.get("candidateId"),
                "targetPublisherAction": action,
                "triageStatus": triage_status,
                "urgencyLevel": urgency_level,
                "priorityClass": priority_class,
                "triageConflictStatus": triage_conflict_status,
                "recommendationSummary": recommendation_summary,
                "watchState": watch_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticQueueReordering": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", candidate.get("notes", "")),
            }
        )

    priority_dashboard = {
        "generatedAt": generated_at,
        "priorityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(priority_dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    triage_docket = {
        "generatedAt": generated_at,
        "priorityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(triage_docket_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    triage_watchlist = {
        "generatedAt": generated_at,
        "priorityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(triage_watchlist_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    priority_annotations_artifact = {
        "generatedAt": generated_at,
        "priorityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticQueueReordering": True,
        "noCanonicalMutation": True,
        "annotations": sorted(priority_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return priority_dashboard, triage_docket, triage_watchlist, priority_annotations_artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage-audit", type=Path, default=Path("bridge/triage_audit.json"))
    parser.add_argument("--triage-recommendations", type=Path, default=Path("bridge/triage_recommendations.json"))
    parser.add_argument("--priority-state-map", type=Path, default=Path("bridge/priority_state_map.json"))
    parser.add_argument("--priority-state-summary", type=Path, default=Path("bridge/priority_state_summary.json"))
    parser.add_argument("--triage-candidate-map", type=Path, default=Path("bridge/triage_candidate_map.json"))
    parser.add_argument("--triage-conflict-report", type=Path, default=Path("bridge/triage_conflict_report.json"))
    parser.add_argument("--priority-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--queue-health-dashboard", type=Path, default=Path("registry/queue_health_dashboard.json"))
    parser.add_argument("--system-health-dashboard", type=Path, default=Path("registry/system_health_dashboard.json"))
    parser.add_argument("--review-backlog-watchlist", type=Path, default=Path("registry/review_backlog_watchlist.json"))
    parser.add_argument("--metric-gaming-watchlist", type=Path, default=Path("registry/metric_gaming_watchlist.json"))

    parser.add_argument("--out-priority-dashboard", type=Path, default=Path("registry/priority_dashboard.json"))
    parser.add_argument("--out-triage-docket", type=Path, default=Path("registry/triage_docket.json"))
    parser.add_argument("--out-triage-watchlist", type=Path, default=Path("registry/triage_watchlist.json"))
    parser.add_argument("--out-priority-annotations", type=Path, default=Path("registry/priority_annotations.json"))

    args = parser.parse_args()

    if args.priority_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --priority-snapshot is no longer supported. Use canonical triage/priority artifacts.")
        return 2

    try:
        outputs = build_priority_overlays(
            load_required_json(args.triage_audit),
            load_required_json(args.triage_recommendations),
            load_required_json(args.priority_state_map),
            load_required_json(args.priority_state_summary),
            load_required_json(args.triage_candidate_map),
            load_required_json(args.triage_conflict_report),
            load_required_json(args.queue_health_dashboard),
            load_required_json(args.system_health_dashboard),
            load_required_json(args.review_backlog_watchlist),
            load_required_json(args.metric_gaming_watchlist),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_priority_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_triage_docket.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_triage_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_priority_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote priority dashboard: {args.out_priority_dashboard}")
    print(f"[OK] Wrote triage docket: {args.out_triage_docket}")
    print(f"[OK] Wrote triage watchlist: {args.out_triage_watchlist}")
    print(f"[OK] Wrote priority annotations: {args.out_priority_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
