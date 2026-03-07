#!/usr/bin/env python3
"""Build normative memory and precedent chamber overlays.

This script surfaces Sophia-audited precedent/case-analogy materials as bounded,
review-facing non-canonical artifacts. It does not mutate canonical truth or review outcomes.
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


def build_precedent_overlays(
    precedent_audit: dict[str, Any],
    precedent_recommendations: dict[str, Any],
    precedent_state_map: dict[str, Any],
    case_analogy_candidates: dict[str, Any],
    review_docket: dict[str, Any],
    governance_review_docket: dict[str, Any],
    deliberation_docket: dict[str, Any],
    recovery_docket: dict[str, Any],
    witness_docket: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits = [a for a in as_list(precedent_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(precedent_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(precedent_state_map.get("entries")) if isinstance(s, dict)]
    candidates = [c for c in as_list(case_analogy_candidates.get("candidates")) if isinstance(c, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
    candidate_by_id = _index_by_key(candidates, "candidateId")

    review_ids = {
        "review": {e.get("reviewId") for e in as_list(review_docket.get("entries")) if isinstance(e, dict)},
        "governance": {e.get("reviewId") for e in as_list(governance_review_docket.get("entries")) if isinstance(e, dict)},
        "deliberation": {e.get("reviewId") for e in as_list(deliberation_docket.get("entries")) if isinstance(e, dict)},
        "recovery": {e.get("reviewId") for e in as_list(recovery_docket.get("entries")) if isinstance(e, dict)},
        "witness": {e.get("reviewId") for e in as_list(witness_docket.get("entries")) if isinstance(e, dict)},
    }

    precedent_registry_entries: list[dict[str, Any]] = []
    case_docket_entries: list[dict[str, Any]] = []
    divergence_watch_entries: list[dict[str, Any]] = []
    precedent_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        candidate_id = rec.get("candidateId")
        candidate = candidate_by_id.get(candidate_id, {}) if isinstance(candidate_id, str) else {}

        state = state_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        precedent_status = str(state.get("precedentStatus", rec.get("precedentStatus", "review-pending")))
        analogy_confidence = float(state.get("analogyConfidence", rec.get("analogyConfidence", 0.0)))
        divergence_level = str(state.get("divergenceLevel", rec.get("divergenceLevel", "none")))
        watch_state = str(audit.get("watchState", rec.get("watchState", "none")))

        linked_target_ids = sorted(
            [t for t in as_list(rec.get("linkedTargetIds", candidate.get("linkedTargetIds"))) if isinstance(t, str)]
        )

        if action == "docket":
            case_docket_entries.append(
                {
                    "reviewId": review_id,
                    "candidateId": candidate_id,
                    "status": "follow-precedent",
                    "precedentStatus": precedent_status,
                    "analogyConfidence": analogy_confidence,
                    "divergenceLevel": divergence_level,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

            precedent_registry_entries.append(
                {
                    "candidateId": candidate_id,
                    "reviewId": review_id,
                    "precedentStatus": precedent_status,
                    "analogyConfidence": analogy_confidence,
                    "divergenceLevel": divergence_level,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "crossChamberLinks": {
                        "review": review_id in review_ids["review"],
                        "governance": review_id in review_ids["governance"],
                        "deliberation": review_id in review_ids["deliberation"],
                        "recovery": review_id in review_ids["recovery"],
                        "witness": review_id in review_ids["witness"],
                    },
                }
            )

        if action == "watch":
            divergence_watch_entries.append(
                {
                    "reviewId": review_id,
                    "candidateId": candidate_id,
                    "status": "watch",
                    "precedentStatus": precedent_status,
                    "analogyConfidence": analogy_confidence,
                    "divergenceLevel": divergence_level,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "antiCaptureSignals": sorted(
                        [s for s in as_list(audit.get("antiCaptureSignals", rec.get("antiCaptureSignals"))) if isinstance(s, str)]
                    ),
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        precedent_annotations.append(
            {
                "reviewId": review_id,
                "candidateId": candidate_id,
                "targetPublisherAction": action,
                "precedentStatus": precedent_status,
                "analogyConfidence": analogy_confidence,
                "divergenceLevel": divergence_level,
                "watchState": watch_state,
                "linkedTargetIds": linked_target_ids,
                "constitutionalPriority": rec.get("constitutionalPriority", "charter-over-precedent"),
                "antiCaptureOverride": bool(rec.get("antiCaptureOverride", False)),
                "noAutomaticBindingEffect": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", candidate.get("notes", "")),
            }
        )

    precedent_registry = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "precedentMemoryChamber": True,
        "entries": sorted(precedent_registry_entries, key=lambda e: str(e.get("candidateId", ""))),
    }

    case_docket = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "precedentMemoryChamber": True,
        "finalActionExternal": True,
        "entries": sorted(case_docket_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    divergence_watchlist = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "entries": sorted(divergence_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    precedent_annotations_artifact = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "noCanonicalMutation": True,
        "noAutomaticBindingEffect": True,
        "annotations": sorted(precedent_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return precedent_registry, case_docket, divergence_watchlist, precedent_annotations_artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precedent-audit", type=Path, default=Path("bridge/precedent_audit.json"))
    parser.add_argument(
        "--precedent-recommendations", type=Path, default=Path("bridge/precedent_recommendations.json")
    )
    parser.add_argument("--precedent-state-map", type=Path, default=Path("bridge/precedent_state_map.json"))
    parser.add_argument(
        "--case-analogy-candidates", type=Path, default=Path("bridge/case_analogy_candidates.json")
    )
    parser.add_argument("--review-docket", type=Path, default=Path("registry/review_docket.json"))
    parser.add_argument("--governance-review-docket", type=Path, default=Path("registry/governance_review_docket.json"))
    parser.add_argument("--deliberation-docket", type=Path, default=Path("registry/deliberation_docket.json"))
    parser.add_argument("--recovery-docket", type=Path, default=Path("registry/recovery_docket.json"))
    parser.add_argument("--witness-docket", type=Path, default=Path("registry/witness_docket.json"))

    parser.add_argument("--out-precedent-registry", type=Path, default=Path("registry/precedent_registry.json"))
    parser.add_argument("--out-case-docket", type=Path, default=Path("registry/case_docket.json"))
    parser.add_argument("--out-divergence-watchlist", type=Path, default=Path("registry/divergence_watchlist.json"))
    parser.add_argument("--out-precedent-annotations", type=Path, default=Path("registry/precedent_annotations.json"))

    args = parser.parse_args()

    outputs = build_precedent_overlays(
        load_json(args.precedent_audit),
        load_json(args.precedent_recommendations),
        load_json(args.precedent_state_map),
        load_json(args.case_analogy_candidates),
        load_json(args.review_docket),
        load_json(args.governance_review_docket),
        load_json(args.deliberation_docket),
        load_json(args.recovery_docket),
        load_json(args.witness_docket),
    )

    args.out_precedent_registry.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_case_docket.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_divergence_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_precedent_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote precedent registry: {args.out_precedent_registry}")
    print(f"[OK] Wrote case docket: {args.out_case_docket}")
    print(f"[OK] Wrote divergence watchlist: {args.out_divergence_watchlist}")
    print(f"[OK] Wrote precedent annotations: {args.out_precedent_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
