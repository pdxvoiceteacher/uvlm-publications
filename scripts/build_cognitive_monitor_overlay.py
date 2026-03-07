#!/usr/bin/env python3
"""Build Publisher cognitive monitor overlays from Sophia-audited monitoring artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

CANONICAL_ACTIONS = {"surface", "annotate", "store"}
OBSERVATIONAL_ACTIONS = {"watch", "escalate-human-review", "defer"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def build_monitor_overlays(
    stability_audit: dict[str, Any],
    recursive_watch_escalations: dict[str, Any],
    reasoning_threads: dict[str, Any],
    cognitive_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    canonical_reasoning_ids = {
        item.get("threadId")
        for item in as_list(reasoning_threads.get("threads"))
        if isinstance(item, dict) and isinstance(item.get("threadId"), str)
    }
    observational_watch_ids = {
        item.get("threadId")
        for item in as_list(cognitive_watchlist.get("entries"))
        if isinstance(item, dict) and isinstance(item.get("threadId"), str)
    }

    events_by_thread: dict[str, list[dict[str, Any]]] = {}
    for event in as_list(recursive_watch_escalations.get("events")):
        if not isinstance(event, dict) or not isinstance(event.get("threadId"), str):
            continue
        events_by_thread.setdefault(event["threadId"], []).append(event)

    monitor_entries: list[dict[str, Any]] = []
    stability_annotations: list[dict[str, Any]] = []
    watch_history_entries: list[dict[str, Any]] = []

    audits = [
        a for a in as_list(stability_audit.get("audits"))
        if isinstance(a, dict) and isinstance(a.get("threadId"), str)
    ]

    for audit in sorted(audits, key=lambda x: x["threadId"]):
        thread_id = audit["threadId"]
        action = str(audit.get("targetPublisherAction", "")).strip().lower()
        audit_status = str(audit.get("auditStatus", "")).strip().lower()

        linked_events = sorted(events_by_thread.get(thread_id, []), key=lambda e: str(e.get("eventDate", "")))
        watch_status = linked_events[-1].get("watchStatus") if linked_events else (
            "watch" if thread_id in observational_watch_ids else "none"
        )
        persistence_trend = audit.get("persistenceTrend")
        if persistence_trend is None and linked_events:
            persistence_trend = linked_events[-1].get("persistenceTrend")

        canonical_ok = (
            action in CANONICAL_ACTIONS and thread_id in canonical_reasoning_ids and audit_status in {"promote", "admit", "surface"}
        )
        observational_ok = (
            action in OBSERVATIONAL_ACTIONS
            or audit_status in {"watch", "defer"}
            or watch_status in {"watch", "escalate-human-review"}
            or thread_id in observational_watch_ids
        )

        if canonical_ok:
            monitor_entries.append(
                {
                    "threadId": thread_id,
                    "status": "monitor-surfaced",
                    "stabilityStatus": audit.get("stabilityStatus", "unknown"),
                    "watchStatus": watch_status,
                    "persistenceScore": audit.get("persistenceScore"),
                    "persistenceTrend": persistence_trend,
                    "coherenceScore": audit.get("coherenceScore"),
                    "riskScore": audit.get("riskScore"),
                    "sourceAuditStatus": audit_status,
                    "targetPublisherAction": action,
                    "updatedAt": generated_at,
                }
            )
            stability_annotations.append(
                {
                    "threadId": thread_id,
                    "stabilityStatus": audit.get("stabilityStatus", "unknown"),
                    "cognitiveWatchSignals": sorted([s for s in as_list(audit.get("cognitiveWatchSignals")) if isinstance(s, str)]),
                    "governingRule": audit.get("governingRule"),
                    "explanation": audit.get("explanation", ""),
                }
            )

        if observational_ok:
            watch_history_entries.append(
                {
                    "threadId": thread_id,
                    "observational": True,
                    "nonCanonical": True,
                    "watchStatus": watch_status,
                    "stabilityStatus": audit.get("stabilityStatus", "unknown"),
                    "persistenceTrend": persistence_trend,
                    "targetPublisherAction": action or "watch",
                    "historyEvents": [
                        {
                            "eventDate": e.get("eventDate"),
                            "watchStatus": e.get("watchStatus"),
                            "escalationAction": e.get("escalationAction"),
                            "reason": e.get("reason"),
                        }
                        for e in linked_events
                    ],
                }
            )

    cognitive_monitor_index = {
        "generatedAt": generated_at,
        "entries": monitor_entries,
    }
    cognitive_stability_annotations = {
        "generatedAt": generated_at,
        "annotations": stability_annotations,
    }
    recursive_watch_history = {
        "generatedAt": generated_at,
        "nonCanonical": True,
        "entries": watch_history_entries,
    }

    return cognitive_monitor_index, cognitive_stability_annotations, recursive_watch_history


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stability-audit", type=Path, default=Path("bridge/stability_audit.json"))
    parser.add_argument("--recursive-watch-escalations", type=Path, default=Path("bridge/recursive_watch_escalations.json"))
    parser.add_argument("--reasoning-threads", type=Path, default=Path("registry/reasoning_threads.json"))
    parser.add_argument("--cognitive-watchlist", type=Path, default=Path("registry/cognitive_watchlist.json"))
    parser.add_argument("--out-monitor-index", type=Path, default=Path("registry/cognitive_monitor_index.json"))
    parser.add_argument(
        "--out-stability-annotations", type=Path, default=Path("registry/cognitive_stability_annotations.json")
    )
    parser.add_argument("--out-watch-history", type=Path, default=Path("registry/recursive_watch_history.json"))
    args = parser.parse_args()

    stability_audit = load_json(args.stability_audit)
    recursive_watch_escalations = load_json(args.recursive_watch_escalations)
    reasoning_threads = load_json(args.reasoning_threads)
    cognitive_watchlist = load_json(args.cognitive_watchlist)

    monitor_index, stability_annotations, watch_history = build_monitor_overlays(
        stability_audit,
        recursive_watch_escalations,
        reasoning_threads,
        cognitive_watchlist,
    )

    args.out_monitor_index.write_text(json.dumps(monitor_index, indent=2) + "\n", encoding="utf-8")
    args.out_stability_annotations.write_text(json.dumps(stability_annotations, indent=2) + "\n", encoding="utf-8")
    args.out_watch_history.write_text(json.dumps(watch_history, indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote cognitive monitor index: {args.out_monitor_index}")
    print(f"[OK] Wrote cognitive stability annotations: {args.out_stability_annotations}")
    print(f"[OK] Wrote recursive watch history (non-canonical): {args.out_watch_history}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
