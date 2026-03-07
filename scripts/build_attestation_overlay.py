#!/usr/bin/env python3
"""Build federated witness and external attestation chamber overlays.

This script surfaces Sophia-audited attestation/witness materials in a bounded,
integrity-facing non-canonical layer. It does not transfer authority, mutate canonical
truth, or execute automatic state changes.
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


def build_attestation_overlays(
    witness_audit: dict[str, Any],
    attestation_recommendations: dict[str, Any],
    attestation_state_map: dict[str, Any],
    witness_roster_candidates: dict[str, Any],
    escrow_index: dict[str, Any],
    recovery_docket: dict[str, Any],
    continuity_roster: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits = [a for a in as_list(witness_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(attestation_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(attestation_state_map.get("entries")) if isinstance(s, dict)]
    candidates = [c for c in as_list(witness_roster_candidates.get("candidates")) if isinstance(c, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
    candidate_by_id = _index_by_key(candidates, "candidateId")

    escrow_by_artifact = _index_by_key(
        [e for e in as_list(escrow_index.get("entries")) if isinstance(e, dict)],
        "artifactId",
    )

    recovery_reviews = {
        e.get("reviewId")
        for e in as_list(recovery_docket.get("entries"))
        if isinstance(e, dict) and isinstance(e.get("reviewId"), str)
    }
    continuity_candidates = {
        e.get("candidateId")
        for e in as_list(continuity_roster.get("entries"))
        if isinstance(e, dict) and isinstance(e.get("candidateId"), str)
    }

    attestation_registry_entries: list[dict[str, Any]] = []
    witness_docket_entries: list[dict[str, Any]] = []
    testimony_watch_entries: list[dict[str, Any]] = []
    attestation_annotations: list[dict[str, Any]] = []

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

        audit = audit_by_review.get(review_id, {})
        state = state_by_review.get(review_id, {})
        escrow = escrow_by_artifact.get(artifact_id, {}) if isinstance(artifact_id, str) else {}

        attestation_status = str(state.get("attestationStatus", rec.get("attestationStatus", "review-pending")))
        witness_sufficiency = str(state.get("witnessSufficiency", rec.get("witnessSufficiency", "insufficient")))
        attestation_need = str(state.get("attestationNeed", rec.get("attestationNeed", "moderate")))
        tamper_sensitivity = str(state.get("tamperSensitivity", rec.get("tamperSensitivity", "unknown")))
        testimony_watch_state = str(
            audit.get("integrityTestimonyWatchState", rec.get("integrityTestimonyWatchState", "none"))
        )

        linked_target_ids = sorted(
            [t for t in as_list(rec.get("linkedTargetIds", candidate.get("linkedTargetIds"))) if isinstance(t, str)]
        )
        witness_ids = sorted(
            [w for w in as_list(candidate.get("witnessIds", rec.get("witnessIds"))) if isinstance(w, str)]
        )

        if action == "docket":
            witness_docket_entries.append(
                {
                    "reviewId": review_id,
                    "artifactId": artifact_id,
                    "candidateId": candidate_id,
                    "status": "escrow-review",
                    "attestationStatus": attestation_status,
                    "witnessSufficiency": witness_sufficiency,
                    "integrityTestimonyWatchState": testimony_watch_state,
                    "attestationNeed": attestation_need,
                    "tamperSensitivity": tamper_sensitivity,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
            )

            attestation_registry_entries.append(
                {
                    "artifactId": artifact_id,
                    "reviewId": review_id,
                    "candidateId": candidate_id,
                    "attestationStatus": attestation_status,
                    "witnessSufficiency": witness_sufficiency,
                    "integrityTestimonyWatchState": testimony_watch_state,
                    "attestationNeed": attestation_need,
                    "tamperSensitivity": tamper_sensitivity,
                    "witnessIds": witness_ids,
                    "escrowStatus": escrow.get("escrowStatus", "review-pending"),
                    "recoveryLinked": review_id in recovery_reviews,
                    "continuityLinked": isinstance(candidate_id, str) and candidate_id in continuity_candidates,
                }
            )

        if action == "watch":
            testimony_watch_entries.append(
                {
                    "reviewId": review_id,
                    "artifactId": artifact_id,
                    "candidateId": candidate_id,
                    "status": "watch",
                    "attestationStatus": attestation_status,
                    "witnessSufficiency": witness_sufficiency,
                    "integrityTestimonyWatchState": testimony_watch_state,
                    "attestationNeed": attestation_need,
                    "tamperSensitivity": tamper_sensitivity,
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

        attestation_annotations.append(
            {
                "reviewId": review_id,
                "artifactId": artifact_id,
                "candidateId": candidate_id,
                "targetPublisherAction": action,
                "attestationStatus": attestation_status,
                "witnessSufficiency": witness_sufficiency,
                "integrityTestimonyWatchState": testimony_watch_state,
                "attestationNeed": attestation_need,
                "tamperSensitivity": tamper_sensitivity,
                "witnessIds": witness_ids,
                "linkedTargetIds": linked_target_ids,
                "escrowStatus": escrow.get("escrowStatus", "review-pending"),
                "noAuthorityTransfer": True,
                "noAutomaticExecution": True,
                "notes": rec.get("notes", candidate.get("notes", "")),
            }
        )

    attestation_registry = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "integrityWitnessChamber": True,
        "entries": sorted(attestation_registry_entries, key=lambda e: str(e.get("artifactId", ""))),
    }

    witness_docket = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "integrityWitnessChamber": True,
        "finalActionExternal": True,
        "entries": sorted(witness_docket_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    integrity_testimony_watchlist = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "entries": sorted(testimony_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    attestation_annotations_artifact = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "noCanonicalMutation": True,
        "noAuthorityTransfer": True,
        "noAutomaticExecution": True,
        "annotations": sorted(attestation_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return (
        attestation_registry,
        witness_docket,
        integrity_testimony_watchlist,
        attestation_annotations_artifact,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--witness-audit", type=Path, default=Path("bridge/witness_audit.json"))
    parser.add_argument(
        "--attestation-recommendations",
        type=Path,
        default=Path("bridge/attestation_recommendations.json"),
    )
    parser.add_argument("--attestation-state-map", type=Path, default=Path("bridge/attestation_state_map.json"))
    parser.add_argument(
        "--witness-roster-candidates",
        type=Path,
        default=Path("bridge/witness_roster_candidates.json"),
    )
    parser.add_argument("--escrow-index", type=Path, default=Path("registry/escrow_index.json"))
    parser.add_argument("--recovery-docket", type=Path, default=Path("registry/recovery_docket.json"))
    parser.add_argument("--continuity-roster", type=Path, default=Path("registry/continuity_roster.json"))

    parser.add_argument("--out-attestation-registry", type=Path, default=Path("registry/attestation_registry.json"))
    parser.add_argument("--out-witness-docket", type=Path, default=Path("registry/witness_docket.json"))
    parser.add_argument(
        "--out-integrity-testimony-watchlist",
        type=Path,
        default=Path("registry/integrity_testimony_watchlist.json"),
    )
    parser.add_argument(
        "--out-attestation-annotations",
        type=Path,
        default=Path("registry/attestation_annotations.json"),
    )

    args = parser.parse_args()

    outputs = build_attestation_overlays(
        load_json(args.witness_audit),
        load_json(args.attestation_recommendations),
        load_json(args.attestation_state_map),
        load_json(args.witness_roster_candidates),
        load_json(args.escrow_index),
        load_json(args.recovery_docket),
        load_json(args.continuity_roster),
    )

    args.out_attestation_registry.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_witness_docket.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_integrity_testimony_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_attestation_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote attestation registry: {args.out_attestation_registry}")
    print(f"[OK] Wrote witness docket: {args.out_witness_docket}")
    print(f"[OK] Wrote integrity testimony watchlist: {args.out_integrity_testimony_watchlist}")
    print(f"[OK] Wrote attestation annotations: {args.out_attestation_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
