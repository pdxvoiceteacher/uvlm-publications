#!/usr/bin/env python3
"""Build stress-test and adversarial scenario rehearsal overlays.

This script surfaces Sophia-audited hypothetical scenario materials as bounded,
preparedness-facing non-canonical artifacts. It does not mutate canonical truth,
governance truth, or trigger live authority.
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


def build_scenario_overlays(
    scenario_audit: dict[str, Any],
    scenario_recommendations: dict[str, Any],
    scenario_state_map: dict[str, Any],
    scenario_outcome_projection: dict[str, Any],
    governance_review_docket: dict[str, Any],
    quorum_resilience_watchlist: dict[str, Any],
    integrity_testimony_watchlist: dict[str, Any],
    divergence_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits = [a for a in as_list(scenario_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(scenario_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(scenario_state_map.get("entries")) if isinstance(s, dict)]
    projections = [p for p in as_list(scenario_outcome_projection.get("entries")) if isinstance(p, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
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

    scenario_registry_entries: list[dict[str, Any]] = []
    stress_test_docket_entries: list[dict[str, Any]] = []
    resilience_watch_entries: list[dict[str, Any]] = []
    scenario_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        state = state_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})
        projection = projection_by_review.get(review_id, {})

        scenario_status = str(state.get("scenarioStatus", rec.get("scenarioStatus", "review-pending")))
        projected_capture_risk = str(
            projection.get("projectedCaptureRisk", rec.get("projectedCaptureRisk", "unknown"))
        )
        projected_continuity_risk = str(
            projection.get("projectedContinuityRisk", rec.get("projectedContinuityRisk", "unknown"))
        )
        preparedness_recommendation = str(
            projection.get(
                "preparednessRecommendation",
                rec.get("preparednessRecommendation", "rehearse-recovery"),
            )
        )
        watch_state = str(audit.get("watchState", rec.get("watchState", "none")))

        linked_target_ids = sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])

        if action == "docket":
            stress_test_docket_entries.append(
                {
                    "reviewId": review_id,
                    "scenarioId": rec.get("scenarioId"),
                    "status": "stress-test-docketed",
                    "scenarioStatus": scenario_status,
                    "projectedCaptureRisk": projected_capture_risk,
                    "projectedContinuityRisk": projected_continuity_risk,
                    "preparednessRecommendation": preparedness_recommendation,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

            scenario_registry_entries.append(
                {
                    "scenarioId": rec.get("scenarioId"),
                    "reviewId": review_id,
                    "scenarioStatus": scenario_status,
                    "projectedCaptureRisk": projected_capture_risk,
                    "projectedContinuityRisk": projected_continuity_risk,
                    "preparednessRecommendation": preparedness_recommendation,
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

        if action == "watch":
            resilience_watch_entries.append(
                {
                    "reviewId": review_id,
                    "scenarioId": rec.get("scenarioId"),
                    "status": "watch",
                    "scenarioStatus": scenario_status,
                    "projectedCaptureRisk": projected_capture_risk,
                    "projectedContinuityRisk": projected_continuity_risk,
                    "preparednessRecommendation": preparedness_recommendation,
                    "watchState": watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        scenario_annotations.append(
            {
                "reviewId": review_id,
                "scenarioId": rec.get("scenarioId"),
                "targetPublisherAction": action,
                "scenarioStatus": scenario_status,
                "projectedCaptureRisk": projected_capture_risk,
                "projectedContinuityRisk": projected_continuity_risk,
                "preparednessRecommendation": preparedness_recommendation,
                "watchState": watch_state,
                "linkedTargetIds": linked_target_ids,
                "freezeBeforeBlindEscalation": bool(rec.get("freezeBeforeBlindEscalation", True)),
                "preparednessNotAuthority": True,
                "noAutomaticEmergencyActivation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", projection.get("notes", "")),
            }
        )

    scenario_registry = {
        "generatedAt": generated_at,
        "preparednessFacing": True,
        "nonCanonical": True,
        "stressRehearsalChamber": True,
        "entries": sorted(scenario_registry_entries, key=lambda e: str(e.get("scenarioId", ""))),
    }

    stress_test_docket = {
        "generatedAt": generated_at,
        "preparednessFacing": True,
        "nonCanonical": True,
        "stressRehearsalChamber": True,
        "finalActionExternal": True,
        "entries": sorted(stress_test_docket_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    resilience_findings_watchlist = {
        "generatedAt": generated_at,
        "preparednessFacing": True,
        "nonCanonical": True,
        "entries": sorted(resilience_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    scenario_annotations_artifact = {
        "generatedAt": generated_at,
        "preparednessFacing": True,
        "nonCanonical": True,
        "preparednessNotAuthority": True,
        "noAutomaticEmergencyActivation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(scenario_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return (
        scenario_registry,
        stress_test_docket,
        resilience_findings_watchlist,
        scenario_annotations_artifact,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario-audit", type=Path, default=Path("bridge/scenario_audit.json"))
    parser.add_argument(
        "--scenario-recommendations", type=Path, default=Path("bridge/scenario_recommendations.json")
    )
    parser.add_argument("--scenario-state-map", type=Path, default=Path("bridge/scenario_state_map.json"))
    parser.add_argument(
        "--scenario-outcome-projection",
        type=Path,
        default=Path("bridge/scenario_outcome_projection.json"),
    )
    parser.add_argument(
        "--governance-review-docket",
        type=Path,
        default=Path("registry/governance_review_docket.json"),
    )
    parser.add_argument(
        "--quorum-resilience-watchlist",
        type=Path,
        default=Path("registry/quorum_resilience_watchlist.json"),
    )
    parser.add_argument(
        "--integrity-testimony-watchlist",
        type=Path,
        default=Path("registry/integrity_testimony_watchlist.json"),
    )
    parser.add_argument(
        "--divergence-watchlist",
        type=Path,
        default=Path("registry/divergence_watchlist.json"),
    )

    parser.add_argument("--out-scenario-registry", type=Path, default=Path("registry/scenario_registry.json"))
    parser.add_argument("--out-stress-test-docket", type=Path, default=Path("registry/stress_test_docket.json"))
    parser.add_argument(
        "--out-resilience-findings-watchlist",
        type=Path,
        default=Path("registry/resilience_findings_watchlist.json"),
    )
    parser.add_argument(
        "--out-scenario-annotations",
        type=Path,
        default=Path("registry/scenario_annotations.json"),
    )

    args = parser.parse_args()

    outputs = build_scenario_overlays(
        load_json(args.scenario_audit),
        load_json(args.scenario_recommendations),
        load_json(args.scenario_state_map),
        load_json(args.scenario_outcome_projection),
        load_json(args.governance_review_docket),
        load_json(args.quorum_resilience_watchlist),
        load_json(args.integrity_testimony_watchlist),
        load_json(args.divergence_watchlist),
    )

    args.out_scenario_registry.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_stress_test_docket.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_resilience_findings_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_scenario_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote scenario registry: {args.out_scenario_registry}")
    print(f"[OK] Wrote stress test docket: {args.out_stress_test_docket}")
    print(f"[OK] Wrote resilience findings watchlist: {args.out_resilience_findings_watchlist}")
    print(f"[OK] Wrote scenario annotations: {args.out_scenario_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
