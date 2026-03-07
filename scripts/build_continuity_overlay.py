#!/usr/bin/env python3
"""Build continuity and resilience chamber overlays from Sophia-audited inputs.

This script surfaces continuity/succession review artifacts in a bounded, governance-facing,
non-canonical layer. It does not mutate governance truth, constitutional artifacts,
or reviewer appointment state.
"""

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


def _index_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        k = row.get(key)
        if isinstance(k, str):
            out[k] = row
    return out


def build_continuity_overlays(
    resilience_audit: dict[str, Any],
    succession_recommendations: dict[str, Any],
    succession_state_map: dict[str, Any],
    continuity_roster_candidates: dict[str, Any],
    governance_review_docket: dict[str, Any],
    reviewer_behavior_monitor: dict[str, Any],
    constitutional_status: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits = [a for a in as_list(resilience_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(succession_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(succession_state_map.get("entries")) if isinstance(s, dict)]
    candidates = [c for c in as_list(continuity_roster_candidates.get("candidates")) if isinstance(c, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
    candidate_by_id = _index_by_key(candidates, "candidateId")

    governance_reviewer_ids = {
        e.get("reviewerId")
        for e in as_list(governance_review_docket.get("entries"))
        if isinstance(e, dict) and isinstance(e.get("reviewerId"), str)
    }
    behavior_by_reviewer = _index_by_key(
        [e for e in as_list(reviewer_behavior_monitor.get("entries")) if isinstance(e, dict)],
        "reviewerId",
    )

    continuity_roster_entries: list[dict[str, Any]] = []
    succession_docket_entries: list[dict[str, Any]] = []
    resilience_watch_entries: list[dict[str, Any]] = []
    redundancy_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        reviewer_id = rec.get("reviewerId") if isinstance(rec.get("reviewerId"), str) else None
        audit = audit_by_review.get(review_id, {})
        state = state_by_review.get(review_id, {})

        candidate_id = rec.get("candidateId")
        candidate = candidate_by_id.get(candidate_id, {}) if isinstance(candidate_id, str) else {}

        resilience_status = str(audit.get("resilienceStatus", rec.get("resilienceStatus", "watch")))
        fragility_status = str(audit.get("fragilityStatus", rec.get("fragilityStatus", "unknown")))
        fragility_score = float(audit.get("governanceFragilityScore", rec.get("governanceFragilityScore", 0.0)))
        readiness_score = float(state.get("successionReadinessScore", rec.get("successionReadinessScore", 0.0)))
        succession_readiness = str(state.get("successionReadiness", rec.get("successionReadiness", "unknown")))
        continuity_watch_state = str(state.get("continuityWatchState", rec.get("continuityWatchState", "none")))

        anti_capture = sorted(
            [s for s in as_list(audit.get("antiCaptureSignals", rec.get("antiCaptureSignals"))) if isinstance(s, str)]
        )
        linked_target_ids = sorted(
            [t for t in as_list(rec.get("linkedTargetIds", candidate.get("linkedTargetIds"))) if isinstance(t, str)]
        )

        if action == "docket":
            continuity_roster_entries.append(
                {
                    "candidateId": candidate_id,
                    "reviewId": review_id,
                    "status": "require-broader-human-review",
                    "resilienceStatus": resilience_status,
                    "successionReadinessScore": readiness_score,
                    "successionReadiness": succession_readiness,
                    "governanceFragilityScore": fragility_score,
                    "fragilityStatus": fragility_status,
                    "continuityWatchState": continuity_watch_state,
                    "redundancySignals": sorted(
                        [s for s in as_list(candidate.get("redundancySignals", rec.get("redundancySignals"))) if isinstance(s, str)]
                    ),
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

            succession_docket_entries.append(
                {
                    "reviewId": review_id,
                    "candidateId": candidate_id,
                    "status": "recommend-deliberation",
                    "resilienceStatus": resilience_status,
                    "successionReadinessScore": readiness_score,
                    "successionReadiness": succession_readiness,
                    "governanceFragilityScore": fragility_score,
                    "fragilityStatus": fragility_status,
                    "continuityWatchState": continuity_watch_state,
                    "antiCaptureSignals": anti_capture,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

        if action == "watch":
            resilience_watch_entries.append(
                {
                    "reviewId": review_id,
                    "candidateId": candidate_id,
                    "status": "watch",
                    "resilienceStatus": resilience_status,
                    "successionReadinessScore": readiness_score,
                    "successionReadiness": succession_readiness,
                    "governanceFragilityScore": fragility_score,
                    "fragilityStatus": fragility_status,
                    "continuityWatchState": continuity_watch_state,
                    "antiCaptureSignals": anti_capture,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        behavior = behavior_by_reviewer.get(reviewer_id, {}) if reviewer_id else {}
        redundancy_annotations.append(
            {
                "reviewId": review_id,
                "candidateId": candidate_id,
                "reviewerId": reviewer_id,
                "resilienceStatus": resilience_status,
                "successionReadinessScore": readiness_score,
                "successionReadiness": succession_readiness,
                "governanceFragilityScore": fragility_score,
                "fragilityStatus": fragility_status,
                "continuityWatchState": continuity_watch_state,
                "antiCaptureSignals": anti_capture,
                "targetPublisherAction": action,
                "linkedTargetIds": linked_target_ids,
                "constitutionalBaseline": constitutional_status.get("constitutionalStatus", "unknown"),
                "governanceReviewLinked": bool(reviewer_id and reviewer_id in governance_reviewer_ids),
                "reviewerBehaviorTrend": behavior.get("behaviorTrend", "unknown"),
                "notes": rec.get("notes", candidate.get("notes", "")),
            }
        )

    continuity_roster = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "continuityResilienceChamber": True,
        "finalActionExternal": True,
        "entries": sorted(continuity_roster_entries, key=lambda e: str(e.get("candidateId", ""))),
    }

    succession_docket = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "continuityResilienceChamber": True,
        "finalActionExternal": True,
        "entries": sorted(succession_docket_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    quorum_resilience_watchlist = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "entries": sorted(resilience_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    governance_redundancy_annotations = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "noAutomaticReviewerAppointment": True,
        "noGovernanceTruthMutation": True,
        "annotations": sorted(redundancy_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return continuity_roster, succession_docket, quorum_resilience_watchlist, governance_redundancy_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resilience-audit", type=Path, default=Path("bridge/resilience_audit.json"))
    parser.add_argument(
        "--succession-recommendations", type=Path, default=Path("bridge/succession_recommendations.json")
    )
    parser.add_argument("--succession-state-map", type=Path, default=Path("bridge/succession_state_map.json"))
    parser.add_argument(
        "--continuity-roster-candidates", type=Path, default=Path("bridge/continuity_roster_candidates.json")
    )
    parser.add_argument("--governance-review-docket", type=Path, default=Path("registry/governance_review_docket.json"))
    parser.add_argument("--reviewer-behavior-monitor", type=Path, default=Path("registry/reviewer_behavior_monitor.json"))
    parser.add_argument("--constitutional-status", type=Path, default=Path("registry/constitutional_status.json"))

    parser.add_argument("--out-continuity-roster", type=Path, default=Path("registry/continuity_roster.json"))
    parser.add_argument("--out-succession-docket", type=Path, default=Path("registry/succession_docket.json"))
    parser.add_argument(
        "--out-quorum-resilience-watchlist", type=Path, default=Path("registry/quorum_resilience_watchlist.json")
    )
    parser.add_argument(
        "--out-governance-redundancy-annotations",
        type=Path,
        default=Path("registry/governance_redundancy_annotations.json"),
    )

    args = parser.parse_args()

    outputs = build_continuity_overlays(
        load_json(args.resilience_audit),
        load_json(args.succession_recommendations),
        load_json(args.succession_state_map),
        load_json(args.continuity_roster_candidates),
        load_json(args.governance_review_docket),
        load_json(args.reviewer_behavior_monitor),
        load_json(args.constitutional_status),
    )

    args.out_continuity_roster.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_succession_docket.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_quorum_resilience_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_governance_redundancy_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote continuity roster: {args.out_continuity_roster}")
    print(f"[OK] Wrote succession docket: {args.out_succession_docket}")
    print(f"[OK] Wrote quorum resilience watchlist: {args.out_quorum_resilience_watchlist}")
    print(f"[OK] Wrote governance redundancy annotations: {args.out_governance_redundancy_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
