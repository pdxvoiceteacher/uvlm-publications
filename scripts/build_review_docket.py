#!/usr/bin/env python3
"""Build curator-facing review docket from Sophia-audited promotion recommendations."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def build_docket(
    promotion_audit: dict[str, Any],
    promotion_recommendations: dict[str, Any],
    reasoning_threads: dict[str, Any],
    cognitive_monitor_index: dict[str, Any],
    multimodal_signal_index: dict[str, Any],
    pattern_donation_annotations: dict[str, Any],
    cognitive_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits_by_candidate = {
        a.get("candidateId"): a
        for a in as_list(promotion_audit.get("audits"))
        if isinstance(a, dict) and isinstance(a.get("candidateId"), str)
    }

    # Build allowed target universe from surfaced overlays (read-only gate support)
    allowed_targets: set[str] = set()
    for thread in as_list(reasoning_threads.get("threads")):
        if isinstance(thread, dict):
            allowed_targets.update(t for t in as_list(thread.get("linkedConceptIds")) if isinstance(t, str))
    for monitor in as_list(cognitive_monitor_index.get("entries")):
        if isinstance(monitor, dict):
            pass
    for signal in as_list(multimodal_signal_index.get("signals")):
        if isinstance(signal, dict) and isinstance(signal.get("targetId"), str):
            allowed_targets.add(signal["targetId"])
    for ann in as_list(pattern_donation_annotations.get("annotations")):
        if isinstance(ann, dict) and isinstance(ann.get("targetId"), str):
            allowed_targets.add(ann["targetId"])
    for watch in as_list(cognitive_watchlist.get("entries")):
        if isinstance(watch, dict):
            allowed_targets.update(t for t in as_list(watch.get("linkedConceptIds")) if isinstance(t, str))

    docket_entries: list[dict[str, Any]] = []
    promotion_annotations: list[dict[str, Any]] = []
    watch_queue: list[dict[str, Any]] = []

    recs = [
        r for r in as_list(promotion_recommendations.get("recommendations"))
        if isinstance(r, dict) and isinstance(r.get("candidateId"), str)
    ]

    for rec in sorted(recs, key=lambda r: r["candidateId"]):
        cid = rec["candidateId"]
        audit = audits_by_candidate.get(cid, {})
        action = str(rec.get("targetPublisherAction", "")).strip().lower()
        rec_status = str(rec.get("auditStatus", "")).strip().lower()
        audit_status = str(audit.get("auditStatus", rec_status)).strip().lower()
        targets = sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])

        if targets and allowed_targets and not any(t in allowed_targets for t in targets):
            continue

        if action == "docket" and audit_status == "recommend-human-review":
            docket_entries.append(
                {
                    "candidateId": cid,
                    "candidateType": rec.get("candidateType"),
                    "status": "queued-for-human-review",
                    "linkedTargetIds": targets,
                    "sourceAuditStatus": audit_status,
                    "queuedAt": generated_at,
                }
            )
            promotion_annotations.append(
                {
                    "candidateId": cid,
                    "governingRule": rec.get("governingRule", audit.get("governingRule")),
                    "coherenceScore": rec.get("coherenceScore"),
                    "riskScore": rec.get("riskScore"),
                    "persistenceScore": rec.get("persistenceScore"),
                    "cognitiveWatchSignals": sorted(
                        [s for s in as_list(rec.get("cognitiveWatchSignals")) if isinstance(s, str)]
                    ),
                    "explanation": rec.get("explanation", audit.get("explanation", "")),
                }
            )
            continue

        if action == "watch" or rec_status == "watch" or audit_status == "watch":
            watch_queue.append(
                {
                    "candidateId": cid,
                    "candidateType": rec.get("candidateType"),
                    "status": "watch-queue",
                    "observational": True,
                    "nonCanonical": True,
                    "linkedTargetIds": targets,
                    "sourceAuditStatus": audit_status or rec_status,
                    "targetPublisherAction": action or "watch",
                    "queuedAt": generated_at,
                }
            )

    review_docket = {
        "generatedAt": generated_at,
        "entries": docket_entries,
    }
    promotion_ann = {
        "generatedAt": generated_at,
        "annotations": promotion_annotations,
    }
    promotion_watch_queue = {
        "generatedAt": generated_at,
        "nonCanonical": True,
        "entries": watch_queue,
    }
    return review_docket, promotion_ann, promotion_watch_queue


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--promotion-audit", type=Path, default=Path("bridge/promotion_audit.json"))
    parser.add_argument("--promotion-recommendations", type=Path, default=Path("bridge/promotion_recommendations.json"))
    parser.add_argument("--reasoning-threads", type=Path, default=Path("registry/reasoning_threads.json"))
    parser.add_argument("--cognitive-monitor-index", type=Path, default=Path("registry/cognitive_monitor_index.json"))
    parser.add_argument("--multimodal-signal-index", type=Path, default=Path("registry/multimodal_signal_index.json"))
    parser.add_argument("--pattern-donation-annotations", type=Path, default=Path("registry/pattern_donation_annotations.json"))
    parser.add_argument("--cognitive-watchlist", type=Path, default=Path("registry/cognitive_watchlist.json"))
    parser.add_argument("--out-review-docket", type=Path, default=Path("registry/review_docket.json"))
    parser.add_argument("--out-promotion-annotations", type=Path, default=Path("registry/promotion_annotations.json"))
    parser.add_argument("--out-promotion-watch-queue", type=Path, default=Path("registry/promotion_watch_queue.json"))
    args = parser.parse_args()

    outputs = build_docket(
        load_json(args.promotion_audit),
        load_json(args.promotion_recommendations),
        load_json(args.reasoning_threads),
        load_json(args.cognitive_monitor_index),
        load_json(args.multimodal_signal_index),
        load_json(args.pattern_donation_annotations),
        load_json(args.cognitive_watchlist),
    )

    args.out_review_docket.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_promotion_annotations.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_promotion_watch_queue.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote review docket: {args.out_review_docket}")
    print(f"[OK] Wrote promotion annotations: {args.out_promotion_annotations}")
    print(f"[OK] Wrote promotion watch queue (non-canonical): {args.out_promotion_watch_queue}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
