#!/usr/bin/env python3
"""Build temporal pattern timeline and persistence overlays.

Publisher surfaces only Sophia-audited temporal pattern materials as bounded,
review-facing overlays. This layer does not mutate identities, graph edges,
precedents, closures, or canonical truth artifacts.
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


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    return action if action in {"docket", "watch", "suppressed", "rejected"} else "watch"


def _targets(rec: dict[str, Any]) -> list[str]:
    return sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])


def _normalize_timeline_events(value: Any) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for item in as_list(value):
        if not isinstance(item, dict):
            continue
        date = item.get("date")
        event = item.get("event")
        if isinstance(date, str) and isinstance(event, str):
            out.append({"date": date, "event": event})
    return sorted(out, key=lambda x: (x["date"], x["event"]))


def _validate_outputs(
    pattern_timeline_dashboard: dict[str, Any],
    pattern_persistence_registry: dict[str, Any],
    pattern_temporal_watchlist: dict[str, Any],
    pattern_temporal_annotations: dict[str, Any],
) -> None:
    if not isinstance(pattern_timeline_dashboard.get("entries"), list):
        raise ValueError("pattern_timeline_dashboard.entries must be a list")
    if not isinstance(pattern_persistence_registry.get("entries"), list):
        raise ValueError("pattern_persistence_registry.entries must be a list")
    if not isinstance(pattern_temporal_watchlist.get("entries"), list):
        raise ValueError("pattern_temporal_watchlist.entries must be a list")
    if not isinstance(pattern_temporal_annotations.get("annotations"), list):
        raise ValueError("pattern_temporal_annotations.annotations must be a list")


def build_pattern_temporal_overlays(
    pattern_temporal_audit: dict[str, Any],
    pattern_temporal_recommendations: dict[str, Any],
    pattern_timeline_map: dict[str, Any],
    pattern_persistence_map: dict[str, Any],
    pattern_temporal_conflict_report: dict[str, Any],
    pattern_dashboard: dict[str, Any],
    pattern_registry: dict[str, Any],
    pattern_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "pattern_temporal_audit": _extract_required_provenance("pattern_temporal_audit", pattern_temporal_audit),
        "pattern_temporal_recommendations": _extract_required_provenance("pattern_temporal_recommendations", pattern_temporal_recommendations),
        "pattern_timeline_map": _extract_required_provenance("pattern_timeline_map", pattern_timeline_map),
        "pattern_persistence_map": _extract_required_provenance("pattern_persistence_map", pattern_persistence_map),
        "pattern_temporal_conflict_report": _extract_required_provenance("pattern_temporal_conflict_report", pattern_temporal_conflict_report),
    }
    for name, artifact in {
        "pattern_dashboard": pattern_dashboard,
        "pattern_registry": pattern_registry,
        "pattern_watchlist": pattern_watchlist,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(pattern_temporal_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(pattern_temporal_recommendations.get("recommendations")) if isinstance(r, dict)]
    timeline_entries = [e for e in as_list(pattern_timeline_map.get("entries")) if isinstance(e, dict)]
    persistence_entries = [e for e in as_list(pattern_persistence_map.get("entries")) if isinstance(e, dict)]
    conflict_entries = [e for e in as_list(pattern_temporal_conflict_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    timeline_by_review = _index_by_key(timeline_entries, "reviewId")
    persistence_by_review = _index_by_key(persistence_entries, "reviewId")
    conflict_by_review = _index_by_key(conflict_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    persistence_registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        timeline = timeline_by_review.get(review_id, {})
        persistence = persistence_by_review.get(review_id, {})
        conflict = conflict_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        pattern_timeline_status = str(timeline.get("patternTimelineStatus", rec.get("patternTimelineStatus", "tracked")))
        pattern_persistence = str(persistence.get("patternPersistence", rec.get("patternPersistence", "fragile")))
        temporal_conflict_markers = sorted([x for x in as_list(conflict.get("temporalConflictMarkers", rec.get("temporalConflictMarkers", []))) if isinstance(x, str)])
        timeline_events = _normalize_timeline_events(timeline.get("timelineEvents", rec.get("timelineEvents", [])))
        audit_state = str(audit.get("patternTemporalAuditState", rec.get("patternTemporalAuditState", "none")))
        linked_target_ids = _targets(rec)

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "patternTimelineStatus": pattern_timeline_status,
                "patternPersistence": pattern_persistence,
                "timelineEvents": timeline_events,
                "temporalConflictMarkers": temporal_conflict_markers,
                "patternTemporalAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            dashboard_entries.append(entry)
            persistence_registry_entries.append({**entry, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "patternTimelineStatus": pattern_timeline_status,
                    "patternPersistence": pattern_persistence,
                    "timelineEvents": timeline_events,
                    "temporalConflictMarkers": temporal_conflict_markers,
                    "patternTemporalAuditState": audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        annotation_entries.append(
            {
                "reviewId": review_id,
                "targetPublisherAction": action,
                "patternTimelineStatus": pattern_timeline_status,
                "patternPersistence": pattern_persistence,
                "timelineEvents": timeline_events,
                "temporalConflictMarkers": temporal_conflict_markers,
                "patternTemporalAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticAccusation": True,
                "noAutomaticGraphMutation": True,
                "noAutomaticPrecedentMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    pattern_timeline_dashboard = {
        "generatedAt": generated_at,
        "patternTemporalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    pattern_persistence_registry = {
        "generatedAt": generated_at,
        "patternTemporalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(persistence_registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    pattern_temporal_watchlist = {
        "generatedAt": generated_at,
        "patternTemporalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    pattern_temporal_annotations = {
        "generatedAt": generated_at,
        "patternTemporalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticAccusation": True,
        "noAutomaticGraphMutation": True,
        "noAutomaticPrecedentMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(
        pattern_timeline_dashboard,
        pattern_persistence_registry,
        pattern_temporal_watchlist,
        pattern_temporal_annotations,
    )
    return pattern_timeline_dashboard, pattern_persistence_registry, pattern_temporal_watchlist, pattern_temporal_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern-temporal-audit", type=Path, default=Path("bridge/pattern_temporal_audit.json"))
    parser.add_argument("--pattern-temporal-recommendations", type=Path, default=Path("bridge/pattern_temporal_recommendations.json"))
    parser.add_argument("--pattern-timeline-map", type=Path, default=Path("bridge/pattern_timeline_map.json"))
    parser.add_argument("--pattern-persistence-map", type=Path, default=Path("bridge/pattern_persistence_map.json"))
    parser.add_argument("--pattern-temporal-conflict-report", type=Path, default=Path("bridge/pattern_temporal_conflict_report.json"))
    parser.add_argument("--pattern-temporal-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--pattern-dashboard", type=Path, default=Path("registry/pattern_dashboard.json"))
    parser.add_argument("--pattern-registry", type=Path, default=Path("registry/pattern_registry.json"))
    parser.add_argument("--pattern-watchlist", type=Path, default=Path("registry/pattern_watchlist.json"))

    parser.add_argument("--out-pattern-timeline-dashboard", type=Path, default=Path("registry/pattern_timeline_dashboard.json"))
    parser.add_argument("--out-pattern-persistence-registry", type=Path, default=Path("registry/pattern_persistence_registry.json"))
    parser.add_argument("--out-pattern-temporal-watchlist", type=Path, default=Path("registry/pattern_temporal_watchlist.json"))
    parser.add_argument("--out-pattern-temporal-annotations", type=Path, default=Path("registry/pattern_temporal_annotations.json"))

    args = parser.parse_args()

    if args.pattern_temporal_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --pattern-temporal-snapshot is no longer supported. Use canonical pattern temporal artifacts.")
        return 2

    try:
        outputs = build_pattern_temporal_overlays(
            load_required_json(args.pattern_temporal_audit),
            load_required_json(args.pattern_temporal_recommendations),
            load_required_json(args.pattern_timeline_map),
            load_required_json(args.pattern_persistence_map),
            load_required_json(args.pattern_temporal_conflict_report),
            load_required_json(args.pattern_dashboard),
            load_required_json(args.pattern_registry),
            load_required_json(args.pattern_watchlist),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_pattern_timeline_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_pattern_persistence_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_pattern_temporal_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_pattern_temporal_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_pattern_timeline_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_persistence_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_temporal_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_temporal_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote pattern timeline dashboard: {args.out_pattern_timeline_dashboard}")
    print(f"[OK] Wrote pattern persistence registry: {args.out_pattern_persistence_registry}")
    print(f"[OK] Wrote pattern temporal watchlist: {args.out_pattern_temporal_watchlist}")
    print(f"[OK] Wrote pattern temporal annotations: {args.out_pattern_temporal_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
