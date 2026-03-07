#!/usr/bin/env python3
"""Build claim-typing, entity-resolution, and verification overlays.

This script surfaces Sophia-audited verification materials as bounded,
review-facing non-canonical artifacts. It does not mutate identities,
closures, queues, or canonical truth artifacts.
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


def build_verification_overlays(
    verification_audit: dict[str, Any],
    verification_recommendations: dict[str, Any],
    claim_type_map: dict[str, Any],
    entity_resolution_map: dict[str, Any],
    entity_resolution_summary: dict[str, Any],
    verification_task_map: dict[str, Any],
    symbolic_field_registry: dict[str, Any],
    closure_registry: dict[str, Any],
    priority_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "verification_audit": _extract_required_provenance("verification_audit", verification_audit),
        "verification_recommendations": _extract_required_provenance("verification_recommendations", verification_recommendations),
        "claim_type_map": _extract_required_provenance("claim_type_map", claim_type_map),
        "entity_resolution_map": _extract_required_provenance("entity_resolution_map", entity_resolution_map),
        "entity_resolution_summary": _extract_required_provenance("entity_resolution_summary", entity_resolution_summary),
        "verification_task_map": _extract_required_provenance("verification_task_map", verification_task_map),
    }
    for optional_name, artifact in {
        "symbolic_field_registry": symbolic_field_registry,
        "closure_registry": closure_registry,
        "priority_dashboard": priority_dashboard,
    }.items():
        optional = _extract_optional_provenance(optional_name, artifact)
        if optional:
            provenances[optional_name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(verification_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(verification_recommendations.get("recommendations")) if isinstance(r, dict)]
    claim_types = [c for c in as_list(claim_type_map.get("entries")) if isinstance(c, dict)]
    resolution_states = [r for r in as_list(entity_resolution_map.get("entries")) if isinstance(r, dict)]
    resolution_summaries = [r for r in as_list(entity_resolution_summary.get("entries")) if isinstance(r, dict)]
    verification_tasks = [v for v in as_list(verification_task_map.get("entries")) if isinstance(v, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    claim_type_by_review = _index_by_key(claim_types, "reviewId")
    resolution_by_review = _index_by_key(resolution_states, "reviewId")
    summary_by_review = _index_by_key(resolution_summaries, "reviewId")
    task_by_review = _index_by_key(verification_tasks, "reviewId")

    verification_entries: list[dict[str, Any]] = []
    entity_watch_entries: list[dict[str, Any]] = []
    claim_type_entries: list[dict[str, Any]] = []
    verification_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        audit = audit_by_review.get(review_id, {})
        claim_type = claim_type_by_review.get(review_id, {})
        resolution = resolution_by_review.get(review_id, {})
        summary = summary_by_review.get(review_id, {})
        task = task_by_review.get(review_id, {})

        claim_type_value = str(claim_type.get("claimType", rec.get("claimType", "untyped")))
        entity_resolution_status = str(resolution.get("entityResolutionStatus", summary.get("entityResolutionStatus", rec.get("entityResolutionStatus", "unresolved"))))
        ambiguity_level = str(summary.get("ambiguityLevel", resolution.get("ambiguityLevel", rec.get("ambiguityLevel", "medium"))))
        verification_urgency = str(task.get("verificationUrgency", rec.get("verificationUrgency", "routine")))
        verification_task_summary = str(task.get("verificationTaskSummary", rec.get("verificationTaskSummary", "review-evidence")))
        linked_target_ids = sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])
        audit_state = str(audit.get("verificationAuditState", rec.get("verificationAuditState", "none")))

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "claimType": claim_type_value,
                "entityResolutionStatus": entity_resolution_status,
                "ambiguityLevel": ambiguity_level,
                "verificationUrgency": verification_urgency,
                "verificationTaskSummary": verification_task_summary,
                "verificationAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            verification_entries.append(entry)
            claim_type_entries.append({
                "reviewId": review_id,
                "claimType": claim_type_value,
                "entityResolutionStatus": entity_resolution_status,
                "ambiguityLevel": ambiguity_level,
                "verificationUrgency": verification_urgency,
                "verificationTaskSummary": verification_task_summary,
                "verificationAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            })

        if action == "watch":
            entity_watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "claimType": claim_type_value,
                    "entityResolutionStatus": entity_resolution_status,
                    "ambiguityLevel": ambiguity_level,
                    "verificationUrgency": verification_urgency,
                    "verificationTaskSummary": verification_task_summary,
                    "verificationAuditState": audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        verification_annotations.append(
            {
                "reviewId": review_id,
                "targetPublisherAction": action,
                "claimType": claim_type_value,
                "entityResolutionStatus": entity_resolution_status,
                "ambiguityLevel": ambiguity_level,
                "verificationUrgency": verification_urgency,
                "verificationTaskSummary": verification_task_summary,
                "verificationAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticAccusation": True,
                "noAutomaticIdentityResolution": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    verification_dashboard = {
        "generatedAt": generated_at,
        "verificationProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(verification_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    entity_watchlist = {
        "generatedAt": generated_at,
        "verificationProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(entity_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    claim_type_registry = {
        "generatedAt": generated_at,
        "verificationProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(claim_type_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    verification_annotations_artifact = {
        "generatedAt": generated_at,
        "verificationProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticAccusation": True,
        "noAutomaticIdentityResolution": True,
        "noCanonicalMutation": True,
        "annotations": sorted(verification_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return verification_dashboard, entity_watchlist, claim_type_registry, verification_annotations_artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verification-audit", type=Path, default=Path("bridge/verification_audit.json"))
    parser.add_argument("--verification-recommendations", type=Path, default=Path("bridge/verification_recommendations.json"))
    parser.add_argument("--claim-type-map", type=Path, default=Path("bridge/claim_type_map.json"))
    parser.add_argument("--entity-resolution-map", type=Path, default=Path("bridge/entity_resolution_map.json"))
    parser.add_argument("--entity-resolution-summary", type=Path, default=Path("bridge/entity_resolution_summary.json"))
    parser.add_argument("--verification-task-map", type=Path, default=Path("bridge/verification_task_map.json"))
    parser.add_argument("--verification-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--symbolic-field-registry", type=Path, default=Path("registry/symbolic_field_registry.json"))
    parser.add_argument("--closure-registry", type=Path, default=Path("registry/closure_registry.json"))
    parser.add_argument("--priority-dashboard", type=Path, default=Path("registry/priority_dashboard.json"))

    parser.add_argument("--out-verification-dashboard", type=Path, default=Path("registry/verification_dashboard.json"))
    parser.add_argument("--out-entity-watchlist", type=Path, default=Path("registry/entity_watchlist.json"))
    parser.add_argument("--out-claim-type-registry", type=Path, default=Path("registry/claim_type_registry.json"))
    parser.add_argument("--out-verification-annotations", type=Path, default=Path("registry/verification_annotations.json"))

    args = parser.parse_args()

    if args.verification_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --verification-snapshot is no longer supported. Use canonical verification artifacts.")
        return 2

    try:
        outputs = build_verification_overlays(
            load_required_json(args.verification_audit),
            load_required_json(args.verification_recommendations),
            load_required_json(args.claim_type_map),
            load_required_json(args.entity_resolution_map),
            load_required_json(args.entity_resolution_summary),
            load_required_json(args.verification_task_map),
            load_required_json(args.symbolic_field_registry),
            load_required_json(args.closure_registry),
            load_required_json(args.priority_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_verification_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_entity_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_claim_type_registry.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_verification_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote verification dashboard: {args.out_verification_dashboard}")
    print(f"[OK] Wrote entity watchlist: {args.out_entity_watchlist}")
    print(f"[OK] Wrote claim type registry: {args.out_claim_type_registry}")
    print(f"[OK] Wrote verification annotations: {args.out_verification_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
