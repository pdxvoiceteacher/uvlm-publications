#!/usr/bin/env python3
"""Build closure, repair, and reopened-case overlays.

This script surfaces Sophia-audited closure and repair materials as bounded,
review-facing non-canonical artifacts. It does not mutate queues, cases,
or canonical truth artifacts.
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


def build_closure_overlays(
    closure_audit: dict[str, Any],
    closure_recommendations: dict[str, Any],
    closure_state_map: dict[str, Any],
    closure_state_summary: dict[str, Any],
    repair_candidate_map: dict[str, Any],
    reopen_signal_report: dict[str, Any],
    priority_dashboard: dict[str, Any],
    triage_docket: dict[str, Any],
    triage_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "closure_audit": _extract_required_provenance("closure_audit", closure_audit),
        "closure_recommendations": _extract_required_provenance("closure_recommendations", closure_recommendations),
        "closure_state_map": _extract_required_provenance("closure_state_map", closure_state_map),
        "closure_state_summary": _extract_required_provenance("closure_state_summary", closure_state_summary),
        "repair_candidate_map": _extract_required_provenance("repair_candidate_map", repair_candidate_map),
        "reopen_signal_report": _extract_required_provenance("reopen_signal_report", reopen_signal_report),
    }
    for optional_name, artifact in {
        "priority_dashboard": priority_dashboard,
        "triage_docket": triage_docket,
        "triage_watchlist": triage_watchlist,
    }.items():
        optional = _extract_optional_provenance(optional_name, artifact)
        if optional:
            provenances[optional_name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(closure_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(closure_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(closure_state_map.get("entries")) if isinstance(s, dict)]
    summaries = [s for s in as_list(closure_state_summary.get("entries")) if isinstance(s, dict)]
    candidates = [c for c in as_list(repair_candidate_map.get("candidates")) if isinstance(c, dict)]
    reopen_signals = [r for r in as_list(reopen_signal_report.get("entries")) if isinstance(r, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
    summary_by_review = _index_by_key(summaries, "reviewId")
    candidate_by_id = _index_by_key(candidates, "candidateId")
    reopen_by_review = _index_by_key(reopen_signals, "reviewId")

    closure_registry_entries: list[dict[str, Any]] = []
    repair_docket_entries: list[dict[str, Any]] = []
    reopened_case_watchlist_entries: list[dict[str, Any]] = []
    closure_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        candidate = candidate_by_id.get(rec.get("candidateId"), {}) if isinstance(rec.get("candidateId"), str) else {}
        audit = audit_by_review.get(review_id, {})
        state = state_by_review.get(review_id, {})
        summary = summary_by_review.get(review_id, {})
        reopen_signal = reopen_by_review.get(review_id, {})

        closure_status = str(state.get("closureStatus", summary.get("closureStatus", rec.get("closureStatus", "pending"))))
        closure_confidence = str(state.get("closureConfidence", summary.get("closureConfidence", rec.get("closureConfidence", "low"))))
        repair_urgency = str(state.get("repairUrgency", summary.get("repairUrgency", rec.get("repairUrgency", "routine"))))
        reopened_case_watch_status = str(reopen_signal.get("reopenedCaseWatchStatus", rec.get("reopenedCaseWatchStatus", "none")))
        outcome_durability = str(summary.get("outcomeDurability", rec.get("outcomeDurability", "unverified")))
        linked_target_ids = sorted([t for t in as_list(rec.get("linkedTargetIds", candidate.get("linkedTargetIds"))) if isinstance(t, str)])
        audit_state = str(audit.get("closureAuditState", rec.get("closureAuditState", "none")))

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "candidateId": rec.get("candidateId"),
                "closureStatus": closure_status,
                "closureConfidence": closure_confidence,
                "repairUrgency": repair_urgency,
                "reopenedCaseWatchStatus": reopened_case_watch_status,
                "outcomeDurability": outcome_durability,
                "closureAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            closure_registry_entries.append(entry)
            repair_docket_entries.append({**entry, "status": "docketed"})

        if action == "watch":
            reopened_case_watchlist_entries.append(
                {
                    "reviewId": review_id,
                    "candidateId": rec.get("candidateId"),
                    "status": "watch",
                    "closureStatus": closure_status,
                    "closureConfidence": closure_confidence,
                    "repairUrgency": repair_urgency,
                    "reopenedCaseWatchStatus": reopened_case_watch_status,
                    "outcomeDurability": outcome_durability,
                    "closureAuditState": audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        closure_annotations.append(
            {
                "reviewId": review_id,
                "candidateId": rec.get("candidateId"),
                "targetPublisherAction": action,
                "closureStatus": closure_status,
                "closureConfidence": closure_confidence,
                "repairUrgency": repair_urgency,
                "reopenedCaseWatchStatus": reopened_case_watch_status,
                "outcomeDurability": outcome_durability,
                "closureAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticReopen": True,
                "noAutomaticClosure": True,
                "noAutomaticRepair": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", candidate.get("notes", "")),
            }
        )

    closure_registry = {
        "generatedAt": generated_at,
        "closureProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(closure_registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    repair_docket = {
        "generatedAt": generated_at,
        "closureProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(repair_docket_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    reopened_case_watchlist = {
        "generatedAt": generated_at,
        "closureProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(reopened_case_watchlist_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    closure_annotations_artifact = {
        "generatedAt": generated_at,
        "closureProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticReopen": True,
        "noAutomaticClosure": True,
        "noAutomaticRepair": True,
        "noCanonicalMutation": True,
        "annotations": sorted(closure_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return closure_registry, repair_docket, reopened_case_watchlist, closure_annotations_artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--closure-audit", type=Path, default=Path("bridge/closure_audit.json"))
    parser.add_argument("--closure-recommendations", type=Path, default=Path("bridge/closure_recommendations.json"))
    parser.add_argument("--closure-state-map", type=Path, default=Path("bridge/closure_state_map.json"))
    parser.add_argument("--closure-state-summary", type=Path, default=Path("bridge/closure_state_summary.json"))
    parser.add_argument("--repair-candidate-map", type=Path, default=Path("bridge/repair_candidate_map.json"))
    parser.add_argument("--reopen-signal-report", type=Path, default=Path("bridge/reopen_signal_report.json"))
    parser.add_argument("--closure-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--priority-dashboard", type=Path, default=Path("registry/priority_dashboard.json"))
    parser.add_argument("--triage-docket", type=Path, default=Path("registry/triage_docket.json"))
    parser.add_argument("--triage-watchlist", type=Path, default=Path("registry/triage_watchlist.json"))

    parser.add_argument("--out-closure-registry", type=Path, default=Path("registry/closure_registry.json"))
    parser.add_argument("--out-repair-docket", type=Path, default=Path("registry/repair_docket.json"))
    parser.add_argument("--out-reopened-case-watchlist", type=Path, default=Path("registry/reopened_case_watchlist.json"))
    parser.add_argument("--out-closure-annotations", type=Path, default=Path("registry/closure_annotations.json"))

    args = parser.parse_args()

    if args.closure_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --closure-snapshot is no longer supported. Use canonical closure/repair artifacts.")
        return 2

    try:
        outputs = build_closure_overlays(
            load_required_json(args.closure_audit),
            load_required_json(args.closure_recommendations),
            load_required_json(args.closure_state_map),
            load_required_json(args.closure_state_summary),
            load_required_json(args.repair_candidate_map),
            load_required_json(args.reopen_signal_report),
            load_required_json(args.priority_dashboard),
            load_required_json(args.triage_docket),
            load_required_json(args.triage_watchlist),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_closure_registry.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_repair_docket.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_reopened_case_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_closure_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote closure registry: {args.out_closure_registry}")
    print(f"[OK] Wrote repair docket: {args.out_repair_docket}")
    print(f"[OK] Wrote reopened-case watchlist: {args.out_reopened_case_watchlist}")
    print(f"[OK] Wrote closure annotations: {args.out_closure_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
