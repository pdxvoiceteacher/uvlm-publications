#!/usr/bin/env python3
"""Build deliberation chamber overlays for quorum and amendment review artifacts.

This script surfaces Sophia-audited deliberation/amendment materials as governance-facing,
non-canonical overlays. It never mutates constitutional principle artifacts.
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
    idx: dict[str, dict[str, Any]] = {}
    for row in rows:
        k = row.get(key)
        if isinstance(k, str):
            idx[k] = row
    return idx


def build_deliberation_overlays(
    quorum_audit: dict[str, Any],
    amendment_recommendations: dict[str, Any],
    deliberation_state_map: dict[str, Any],
    amendment_candidate_map: dict[str, Any],
    constitutional_status: dict[str, Any],
    governance_review_docket: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    quorum_entries = [q for q in as_list(quorum_audit.get("audits")) if isinstance(q, dict)]
    rec_entries = [r for r in as_list(amendment_recommendations.get("recommendations")) if isinstance(r, dict)]
    deliberation_entries = [d for d in as_list(deliberation_state_map.get("entries")) if isinstance(d, dict)]
    candidate_entries = [c for c in as_list(amendment_candidate_map.get("candidates")) if isinstance(c, dict)]

    quorum_by_review = _index_by_key(quorum_entries, "reviewId")
    deliberation_by_review = _index_by_key(deliberation_entries, "reviewId")
    candidate_by_id = _index_by_key(candidate_entries, "candidateId")

    governance_reviewer_ids = {
        e.get("reviewerId")
        for e in as_list(governance_review_docket.get("entries"))
        if isinstance(e, dict) and isinstance(e.get("reviewerId"), str)
    }

    deliberation_docket_entries: list[dict[str, Any]] = []
    amendment_queue_entries: list[dict[str, Any]] = []
    quorum_watch_entries: list[dict[str, Any]] = []
    revision_annotations: list[dict[str, Any]] = []

    for rec in sorted(rec_entries, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        quorum = quorum_by_review.get(review_id, {})
        deliberation_state = deliberation_by_review.get(review_id, {})
        candidate_id = rec.get("candidateId")
        candidate = candidate_by_id.get(candidate_id, {}) if isinstance(candidate_id, str) else {}

        quorum_status = str(quorum.get("quorumStatus", "unknown"))
        amendment_status = str(rec.get("amendmentStatus", candidate.get("amendmentStatus", "review-pending")))
        urgency = str(deliberation_state.get("urgency", rec.get("deliberationUrgency", "routine")))
        anti_capture = sorted(
            [s for s in as_list(quorum.get("antiCaptureSignals", rec.get("antiCaptureSignals"))) if isinstance(s, str)]
        )

        linked_target_ids = sorted(
            [t for t in as_list(rec.get("linkedTargetIds", candidate.get("linkedTargetIds"))) if isinstance(t, str)]
        )

        if action == "docket":
            # Main queues allow only explicit Sophia docket action.
            deliberation_docket_entries.append(
                {
                    "reviewId": review_id,
                    "candidateId": candidate_id,
                    "status": "recommend-deliberation",
                    "quorumStatus": quorum_status,
                    "amendmentStatus": amendment_status,
                    "deliberationUrgency": urgency,
                    "antiCaptureSignals": anti_capture,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "governanceDependencies": sorted(
                        [r for r in as_list(rec.get("governanceDependencies")) if isinstance(r, str)]
                    ),
                    "queuedAt": generated_at,
                }
            )

            amendment_queue_entries.append(
                {
                    "candidateId": candidate_id,
                    "reviewId": review_id,
                    "status": "require-broader-human-review",
                    "amendmentStatus": amendment_status,
                    "proceduralPrinciples": sorted(
                        [p for p in as_list(candidate.get("proceduralPrinciples", rec.get("proceduralPrinciples"))) if isinstance(p, str)]
                    ),
                    "emergencyInterpretationOnly": bool(
                        candidate.get("emergencyInterpretationOnly", rec.get("emergencyInterpretationOnly", False))
                    ),
                    "reversibilityPreference": candidate.get(
                        "reversibilityPreference", rec.get("reversibilityPreference", "prefer-reversible-guidance")
                    ),
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

        if action == "watch":
            quorum_watch_entries.append(
                {
                    "reviewId": review_id,
                    "candidateId": candidate_id,
                    "status": "watch",
                    "quorumStatus": quorum_status,
                    "amendmentStatus": amendment_status,
                    "deliberationUrgency": urgency,
                    "antiCaptureSignals": anti_capture,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "nonCanonical": True,
                    "observational": True,
                    "queuedAt": generated_at,
                }
            )

        revision_annotations.append(
            {
                "reviewId": review_id,
                "candidateId": candidate_id,
                "quorumStatus": quorum_status,
                "amendmentStatus": amendment_status,
                "deliberationUrgency": urgency,
                "antiCaptureSignals": anti_capture,
                "targetPublisherAction": action,
                "linkedTargetIds": linked_target_ids,
                "constitutionalBaseline": constitutional_status.get("constitutionalStatus", "unknown"),
                "governanceReviewLinked": bool(
                    isinstance(rec.get("reviewerId"), str) and rec.get("reviewerId") in governance_reviewer_ids
                ),
                "notes": rec.get("notes", candidate.get("notes", "")),
            }
        )

    deliberation_docket = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "deliberationChamber": True,
        "finalActionExternal": True,
        "entries": sorted(deliberation_docket_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    amendment_queue = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "deliberationChamber": True,
        "finalActionExternal": True,
        "entries": sorted(amendment_queue_entries, key=lambda e: str(e.get("candidateId", ""))),
    }

    quorum_watchlist = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "entries": sorted(quorum_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    constitutional_revision_annotations = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "noAutomaticConstitutionalMutation": True,
        "annotations": sorted(revision_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return deliberation_docket, amendment_queue, quorum_watchlist, constitutional_revision_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quorum-audit", type=Path, default=Path("bridge/quorum_audit.json"))
    parser.add_argument(
        "--amendment-recommendations", type=Path, default=Path("bridge/amendment_recommendations.json")
    )
    parser.add_argument("--deliberation-state-map", type=Path, default=Path("bridge/deliberation_state_map.json"))
    parser.add_argument("--amendment-candidate-map", type=Path, default=Path("bridge/amendment_candidate_map.json"))
    parser.add_argument("--constitutional-status", type=Path, default=Path("registry/constitutional_status.json"))
    parser.add_argument("--governance-review-docket", type=Path, default=Path("registry/governance_review_docket.json"))

    parser.add_argument("--out-deliberation-docket", type=Path, default=Path("registry/deliberation_docket.json"))
    parser.add_argument("--out-amendment-queue", type=Path, default=Path("registry/amendment_queue.json"))
    parser.add_argument("--out-quorum-watchlist", type=Path, default=Path("registry/quorum_watchlist.json"))
    parser.add_argument(
        "--out-constitutional-revision-annotations",
        type=Path,
        default=Path("registry/constitutional_revision_annotations.json"),
    )

    args = parser.parse_args()

    outputs = build_deliberation_overlays(
        load_json(args.quorum_audit),
        load_json(args.amendment_recommendations),
        load_json(args.deliberation_state_map),
        load_json(args.amendment_candidate_map),
        load_json(args.constitutional_status),
        load_json(args.governance_review_docket),
    )

    args.out_deliberation_docket.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_amendment_queue.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_quorum_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_constitutional_revision_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote deliberation docket: {args.out_deliberation_docket}")
    print(f"[OK] Wrote amendment queue: {args.out_amendment_queue}")
    print(f"[OK] Wrote quorum watchlist: {args.out_quorum_watchlist}")
    print(f"[OK] Wrote constitutional revision annotations: {args.out_constitutional_revision_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
