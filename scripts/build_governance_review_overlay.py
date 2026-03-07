#!/usr/bin/env python3
"""Build governance review overlays from Sophia-audited governance artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def build_governance_overlays(
    governance_audit: dict[str, Any],
    governance_recommendations: dict[str, Any],
    reviewer_behavior_audit: dict[str, Any],
    review_docket: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audit_by_reviewer = {
        a.get("reviewerId"): a
        for a in as_list(governance_audit.get("audits"))
        if isinstance(a, dict) and isinstance(a.get("reviewerId"), str)
    }
    behavior_by_reviewer = {
        b.get("reviewerId"): b
        for b in as_list(reviewer_behavior_audit.get("reviews"))
        if isinstance(b, dict) and isinstance(b.get("reviewerId"), str)
    }

    # Read dependency for phase traceability (no mutation)
    _ = review_docket

    docket_entries: list[dict[str, Any]] = []
    integrity_annotations: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    behavior_monitor_entries: list[dict[str, Any]] = []

    recs = [
        r for r in as_list(governance_recommendations.get("recommendations"))
        if isinstance(r, dict) and isinstance(r.get("reviewerId"), str)
    ]

    for rec in sorted(recs, key=lambda r: r["reviewerId"]):
        reviewer_id = rec["reviewerId"]
        audit = audit_by_reviewer.get(reviewer_id, {})
        behavior = behavior_by_reviewer.get(reviewer_id, {})

        action = str(rec.get("targetPublisherAction", "")).strip().lower()
        rec_status = str(rec.get("auditStatus", "")).strip().lower()
        audit_status = str(audit.get("auditStatus", rec_status)).strip().lower()

        if action == "docket" and audit_status == "recommend-human-review":
            docket_entries.append(
                {
                    "reviewerId": reviewer_id,
                    "status": "queued-for-human-governance-review",
                    "sourceAuditStatus": audit_status,
                    "governanceStatus": rec.get("governanceStatus", audit.get("governanceStatus", "unknown")),
                    "linkedTargetIds": sorted(
                        [t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)]
                    ),
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )
            integrity_annotations.append(
                {
                    "reviewerId": reviewer_id,
                    "coherenceScore": rec.get("coherenceScore", audit.get("coherenceScore")),
                    "riskScore": rec.get("riskScore", audit.get("riskScore")),
                    "conflictRisk": rec.get("conflictRisk", audit.get("conflictRisk")),
                    "integritySignals": sorted(
                        [s for s in as_list(rec.get("integritySignals", audit.get("integritySignals"))) if isinstance(s, str)]
                    ),
                    "governingRule": rec.get("governingRule", audit.get("governingRule")),
                    "explanation": rec.get("explanation", audit.get("explanation", "")),
                }
            )

        if action == "watch" or rec_status == "watch" or audit_status == "watch":
            watch_entries.append(
                {
                    "reviewerId": reviewer_id,
                    "status": "watch",
                    "observational": True,
                    "nonCanonical": True,
                    "governanceStatus": rec.get("governanceStatus", audit.get("governanceStatus", "watch")),
                    "linkedTargetIds": sorted(
                        [t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)]
                    ),
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "queuedAt": generated_at,
                }
            )

        # Reviewer behavior monitor is observational, regardless of docket/watch admission.
        if behavior:
            behavior_monitor_entries.append(
                {
                    "reviewerId": reviewer_id,
                    "observational": True,
                    "nonCanonical": True,
                    "behaviorTrend": behavior.get("behaviorTrend", "unknown"),
                    "continuedEligibilityStatus": behavior.get("continuedEligibilityStatus", "unknown"),
                    "humanReviewFlag": bool(behavior.get("humanReviewFlag", False)),
                    "notes": behavior.get("notes", ""),
                }
            )

    governance_review_docket = {
        "generatedAt": generated_at,
        "entries": docket_entries,
    }
    reviewer_integrity_annotations = {
        "generatedAt": generated_at,
        "annotations": integrity_annotations,
    }
    reviewer_watch_queue = {
        "generatedAt": generated_at,
        "nonCanonical": True,
        "entries": watch_entries,
    }
    reviewer_behavior_monitor = {
        "generatedAt": generated_at,
        "nonCanonical": True,
        "entries": sorted(behavior_monitor_entries, key=lambda e: e.get("reviewerId", "")),
    }

    return governance_review_docket, reviewer_integrity_annotations, reviewer_watch_queue, reviewer_behavior_monitor


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--governance-audit", type=Path, default=Path("bridge/governance_audit.json"))
    parser.add_argument("--governance-recommendations", type=Path, default=Path("bridge/governance_recommendations.json"))
    parser.add_argument("--reviewer-behavior-audit", type=Path, default=Path("bridge/reviewer_behavior_audit.json"))
    parser.add_argument("--review-docket", type=Path, default=Path("registry/review_docket.json"))
    parser.add_argument("--out-governance-review-docket", type=Path, default=Path("registry/governance_review_docket.json"))
    parser.add_argument(
        "--out-reviewer-integrity-annotations", type=Path, default=Path("registry/reviewer_integrity_annotations.json")
    )
    parser.add_argument("--out-reviewer-watch-queue", type=Path, default=Path("registry/reviewer_watch_queue.json"))
    parser.add_argument("--out-reviewer-behavior-monitor", type=Path, default=Path("registry/reviewer_behavior_monitor.json"))
    args = parser.parse_args()

    outputs = build_governance_overlays(
        load_json(args.governance_audit),
        load_json(args.governance_recommendations),
        load_json(args.reviewer_behavior_audit),
        load_json(args.review_docket),
    )

    args.out_governance_review_docket.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_reviewer_integrity_annotations.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_reviewer_watch_queue.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_reviewer_behavior_monitor.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote governance review docket: {args.out_governance_review_docket}")
    print(f"[OK] Wrote reviewer integrity annotations: {args.out_reviewer_integrity_annotations}")
    print(f"[OK] Wrote reviewer watch queue (non-canonical): {args.out_reviewer_watch_queue}")
    print(f"[OK] Wrote reviewer behavior monitor (non-canonical): {args.out_reviewer_behavior_monitor}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
