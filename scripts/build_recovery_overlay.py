#!/usr/bin/env python3
"""Build evidence escrow and recovery chamber overlays from Sophia-audited artifacts.

This script surfaces preservation/recovery review artifacts in a bounded,
governance-facing, non-canonical layer. It does not mutate canonical artifacts,
does not imply automatic replication, and does not execute recovery.
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


def build_recovery_overlays(
    recovery_audit: dict[str, Any],
    recovery_recommendations: dict[str, Any],
    preservation_state_map: dict[str, Any],
    artifact_escrow_plan: dict[str, Any],
    recovery_candidate_map: dict[str, Any],
    constitutional_status: dict[str, Any],
    continuity_mode_index: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits = [a for a in as_list(recovery_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(recovery_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(preservation_state_map.get("entries")) if isinstance(s, dict)]
    escrow_rows = [e for e in as_list(artifact_escrow_plan.get("entries")) if isinstance(e, dict)]
    candidates = [c for c in as_list(recovery_candidate_map.get("candidates")) if isinstance(c, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
    escrow_by_artifact = _index_by_key(escrow_rows, "artifactId")
    candidate_by_id = _index_by_key(candidates, "candidateId")

    escrow_entries: list[dict[str, Any]] = []
    recovery_docket_entries: list[dict[str, Any]] = []
    integrity_watch_entries: list[dict[str, Any]] = []
    recovery_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        candidate_id = rec.get("candidateId")
        candidate = candidate_by_id.get(candidate_id, {}) if isinstance(candidate_id, str) else {}
        artifact_id = rec.get("artifactId", candidate.get("artifactId"))
        escrow = escrow_by_artifact.get(artifact_id, {}) if isinstance(artifact_id, str) else {}
        audit = audit_by_review.get(review_id, {})
        state = state_by_review.get(review_id, {})

        preservation_criticality = str(
            state.get("preservationCriticality", rec.get("preservationCriticality", "moderate"))
        )
        escrow_status = str(escrow.get("escrowStatus", rec.get("escrowStatus", "review-pending")))
        recovery_readiness = str(state.get("recoveryReadiness", rec.get("recoveryReadiness", "unknown")))
        recoverability_score = float(state.get("recoverabilityScore", rec.get("recoverabilityScore", 0.0)))
        integrity_watch_state = str(audit.get("integrityWatchState", rec.get("integrityWatchState", "none")))

        linked_target_ids = sorted(
            [t for t in as_list(rec.get("linkedTargetIds", candidate.get("linkedTargetIds"))) if isinstance(t, str)]
        )
        dependency_paths = sorted(
            [d for d in as_list(escrow.get("dependencyPaths", candidate.get("dependencyPaths"))) if isinstance(d, str)]
        )

        escrow_entries.append(
            {
                "artifactId": artifact_id,
                "reviewId": review_id,
                "candidateId": candidate_id,
                "escrowStatus": escrow_status,
                "preservationCriticality": preservation_criticality,
                "recoverabilityScore": recoverability_score,
                "integrityWatchState": integrity_watch_state,
                "dependencyPaths": dependency_paths,
                "custodyModel": escrow.get("custodyModel", rec.get("custodyModel", "distributed-review")),
                "escrowReview": True,
            }
        )

        if action == "docket":
            recovery_docket_entries.append(
                {
                    "reviewId": review_id,
                    "artifactId": artifact_id,
                    "candidateId": candidate_id,
                    "status": "escrow-review",
                    "preservationCriticality": preservation_criticality,
                    "escrowStatus": escrow_status,
                    "recoveryReadiness": recovery_readiness,
                    "recoverabilityScore": recoverability_score,
                    "integrityWatchState": integrity_watch_state,
                    "dependencyPaths": dependency_paths,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

        if action == "watch":
            integrity_watch_entries.append(
                {
                    "reviewId": review_id,
                    "artifactId": artifact_id,
                    "candidateId": candidate_id,
                    "status": "watch",
                    "preservationCriticality": preservation_criticality,
                    "escrowStatus": escrow_status,
                    "recoveryReadiness": recovery_readiness,
                    "recoverabilityScore": recoverability_score,
                    "integrityWatchState": integrity_watch_state,
                    "linkedTargetIds": linked_target_ids,
                    "antiTamperSignals": sorted(
                        [s for s in as_list(audit.get("antiTamperSignals", rec.get("antiTamperSignals"))) if isinstance(s, str)]
                    ),
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        recovery_annotations.append(
            {
                "reviewId": review_id,
                "artifactId": artifact_id,
                "candidateId": candidate_id,
                "targetPublisherAction": action,
                "preservationCriticality": preservation_criticality,
                "escrowStatus": escrow_status,
                "recoveryReadiness": recovery_readiness,
                "recoverabilityScore": recoverability_score,
                "integrityWatchState": integrity_watch_state,
                "dependencyPaths": dependency_paths,
                "linkedTargetIds": linked_target_ids,
                "constitutionalBaseline": constitutional_status.get("constitutionalStatus", "unknown"),
                "continuityMode": continuity_mode_index.get("continuityMode", "normal"),
                "noAutomaticExecution": True,
                "notes": rec.get("notes", candidate.get("notes", "")),
            }
        )

    escrow_index = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "evidenceEscrowChamber": True,
        "entries": sorted(escrow_entries, key=lambda e: str(e.get("artifactId", ""))),
    }

    recovery_docket = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "evidenceEscrowChamber": True,
        "finalActionExternal": True,
        "entries": sorted(recovery_docket_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    integrity_watchlist = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "entries": sorted(integrity_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    recovery_annotations_artifact = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "noCanonicalMutation": True,
        "noAutomaticReplication": True,
        "noRecoveryExecution": True,
        "annotations": sorted(recovery_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return escrow_index, recovery_docket, integrity_watchlist, recovery_annotations_artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recovery-audit", type=Path, default=Path("bridge/recovery_audit.json"))
    parser.add_argument("--recovery-recommendations", type=Path, default=Path("bridge/recovery_recommendations.json"))
    parser.add_argument("--preservation-state-map", type=Path, default=Path("bridge/preservation_state_map.json"))
    parser.add_argument("--artifact-escrow-plan", type=Path, default=Path("bridge/artifact_escrow_plan.json"))
    parser.add_argument("--recovery-candidate-map", type=Path, default=Path("bridge/recovery_candidate_map.json"))
    parser.add_argument("--constitutional-status", type=Path, default=Path("registry/constitutional_status.json"))
    parser.add_argument("--continuity-mode-index", type=Path, default=Path("registry/continuity_mode_index.json"))

    parser.add_argument("--out-escrow-index", type=Path, default=Path("registry/escrow_index.json"))
    parser.add_argument("--out-recovery-docket", type=Path, default=Path("registry/recovery_docket.json"))
    parser.add_argument("--out-integrity-watchlist", type=Path, default=Path("registry/integrity_watchlist.json"))
    parser.add_argument("--out-recovery-annotations", type=Path, default=Path("registry/recovery_annotations.json"))

    args = parser.parse_args()

    outputs = build_recovery_overlays(
        load_json(args.recovery_audit),
        load_json(args.recovery_recommendations),
        load_json(args.preservation_state_map),
        load_json(args.artifact_escrow_plan),
        load_json(args.recovery_candidate_map),
        load_json(args.constitutional_status),
        load_json(args.continuity_mode_index),
    )

    args.out_escrow_index.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_recovery_docket.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_integrity_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_recovery_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote escrow index: {args.out_escrow_index}")
    print(f"[OK] Wrote recovery docket: {args.out_recovery_docket}")
    print(f"[OK] Wrote integrity watchlist: {args.out_integrity_watchlist}")
    print(f"[OK] Wrote recovery annotations: {args.out_recovery_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
