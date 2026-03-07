#!/usr/bin/env python3
"""Build symbolic field and early-warning overlays.

This script surfaces Sophia-audited symbolic field and early-warning materials
as bounded, review-facing non-canonical artifacts. It does not mutate the
canonical graph, queues, closures, or governance truth artifacts.
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


def build_symbolic_field_overlays(
    symbolic_field_audit: dict[str, Any],
    symbolic_field_recommendations: dict[str, Any],
    symbolic_field_state: dict[str, Any],
    symbolic_field_summary: dict[str, Any],
    regime_transition_report: dict[str, Any],
    early_warning_signal_map: dict[str, Any],
    institutional_status: dict[str, Any],
    queue_health_dashboard: dict[str, Any],
    priority_dashboard: dict[str, Any],
    closure_registry: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "symbolic_field_audit": _extract_required_provenance("symbolic_field_audit", symbolic_field_audit),
        "symbolic_field_recommendations": _extract_required_provenance("symbolic_field_recommendations", symbolic_field_recommendations),
        "symbolic_field_state": _extract_required_provenance("symbolic_field_state", symbolic_field_state),
        "symbolic_field_summary": _extract_required_provenance("symbolic_field_summary", symbolic_field_summary),
        "regime_transition_report": _extract_required_provenance("regime_transition_report", regime_transition_report),
        "early_warning_signal_map": _extract_required_provenance("early_warning_signal_map", early_warning_signal_map),
    }
    for optional_name, artifact in {
        "institutional_status": institutional_status,
        "queue_health_dashboard": queue_health_dashboard,
        "priority_dashboard": priority_dashboard,
        "closure_registry": closure_registry,
    }.items():
        optional = _extract_optional_provenance(optional_name, artifact)
        if optional:
            provenances[optional_name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(symbolic_field_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(symbolic_field_recommendations.get("recommendations")) if isinstance(r, dict)]
    states = [s for s in as_list(symbolic_field_state.get("entries")) if isinstance(s, dict)]
    summaries = [s for s in as_list(symbolic_field_summary.get("entries")) if isinstance(s, dict)]
    transitions = [t for t in as_list(regime_transition_report.get("entries")) if isinstance(t, dict)]
    warnings = [w for w in as_list(early_warning_signal_map.get("entries")) if isinstance(w, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(states, "reviewId")
    summary_by_review = _index_by_key(summaries, "reviewId")
    transition_by_review = _index_by_key(transitions, "reviewId")
    warning_by_review = _index_by_key(warnings, "reviewId")

    symbolic_field_entries: list[dict[str, Any]] = []
    early_warning_entries: list[dict[str, Any]] = []
    regime_watch_entries: list[dict[str, Any]] = []
    symbolic_annotations: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
        if action not in {"docket", "watch", "suppressed", "rejected"}:
            action = "watch"

        audit = audit_by_review.get(review_id, {})
        state = state_by_review.get(review_id, {})
        summary = summary_by_review.get(review_id, {})
        transition = transition_by_review.get(review_id, {})
        warning = warning_by_review.get(review_id, {})

        symbolic_field_status = str(state.get("symbolicFieldStatus", summary.get("symbolicFieldStatus", rec.get("symbolicFieldStatus", "stable"))))
        regime_class = str(state.get("regimeClass", transition.get("regimeClass", rec.get("regimeClass", "bounded-order"))))
        lambda_zone_warning_level = str(state.get("lambdaZoneWarningLevel", warning.get("lambdaZoneWarningLevel", rec.get("lambdaZoneWarningLevel", "low"))))
        architecture_hint = str(summary.get("architectureHint", rec.get("architectureHint", "monitor")))
        regime_watch_status = str(transition.get("regimeWatchStatus", rec.get("regimeWatchStatus", "none")))
        linked_target_ids = sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])
        audit_state = str(audit.get("symbolicAuditState", rec.get("symbolicAuditState", "none")))

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "symbolicFieldStatus": symbolic_field_status,
                "regimeClass": regime_class,
                "lambdaZoneWarningLevel": lambda_zone_warning_level,
                "architectureHint": architecture_hint,
                "regimeWatchStatus": regime_watch_status,
                "symbolicAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            symbolic_field_entries.append(entry)
            early_warning_entries.append({**entry, "status": "actionable"})

        if action == "watch":
            regime_watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "symbolicFieldStatus": symbolic_field_status,
                    "regimeClass": regime_class,
                    "lambdaZoneWarningLevel": lambda_zone_warning_level,
                    "architectureHint": architecture_hint,
                    "regimeWatchStatus": regime_watch_status,
                    "symbolicAuditState": audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        symbolic_annotations.append(
            {
                "reviewId": review_id,
                "targetPublisherAction": action,
                "symbolicFieldStatus": symbolic_field_status,
                "regimeClass": regime_class,
                "lambdaZoneWarningLevel": lambda_zone_warning_level,
                "architectureHint": architecture_hint,
                "regimeWatchStatus": regime_watch_status,
                "symbolicAuditState": audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticIntervention": True,
                "noMemoryMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    symbolic_field_registry = {
        "generatedAt": generated_at,
        "symbolicFieldProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(symbolic_field_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    early_warning_dashboard = {
        "generatedAt": generated_at,
        "symbolicFieldProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(early_warning_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    regime_watchlist = {
        "generatedAt": generated_at,
        "symbolicFieldProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(regime_watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    symbolic_field_annotations = {
        "generatedAt": generated_at,
        "symbolicFieldProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticIntervention": True,
        "noMemoryMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(symbolic_annotations, key=lambda e: str(e.get("reviewId", ""))),
    }

    return symbolic_field_registry, early_warning_dashboard, regime_watchlist, symbolic_field_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbolic-field-audit", type=Path, default=Path("bridge/symbolic_field_audit.json"))
    parser.add_argument("--symbolic-field-recommendations", type=Path, default=Path("bridge/symbolic_field_recommendations.json"))
    parser.add_argument("--symbolic-field-state", type=Path, default=Path("bridge/symbolic_field_state.json"))
    parser.add_argument("--symbolic-field-summary", type=Path, default=Path("bridge/symbolic_field_summary.json"))
    parser.add_argument("--regime-transition-report", type=Path, default=Path("bridge/regime_transition_report.json"))
    parser.add_argument("--early-warning-signal-map", type=Path, default=Path("bridge/early_warning_signal_map.json"))
    parser.add_argument("--symbolic-field-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--institutional-status", type=Path, default=Path("registry/institutional_status.json"))
    parser.add_argument("--queue-health-dashboard", type=Path, default=Path("registry/queue_health_dashboard.json"))
    parser.add_argument("--priority-dashboard", type=Path, default=Path("registry/priority_dashboard.json"))
    parser.add_argument("--closure-registry", type=Path, default=Path("registry/closure_registry.json"))

    parser.add_argument("--out-symbolic-field-registry", type=Path, default=Path("registry/symbolic_field_registry.json"))
    parser.add_argument("--out-early-warning-dashboard", type=Path, default=Path("registry/early_warning_dashboard.json"))
    parser.add_argument("--out-regime-watchlist", type=Path, default=Path("registry/regime_watchlist.json"))
    parser.add_argument("--out-symbolic-field-annotations", type=Path, default=Path("registry/symbolic_field_annotations.json"))

    args = parser.parse_args()

    if args.symbolic_field_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --symbolic-field-snapshot is no longer supported. Use canonical symbolic-field artifacts.")
        return 2

    try:
        outputs = build_symbolic_field_overlays(
            load_required_json(args.symbolic_field_audit),
            load_required_json(args.symbolic_field_recommendations),
            load_required_json(args.symbolic_field_state),
            load_required_json(args.symbolic_field_summary),
            load_required_json(args.regime_transition_report),
            load_required_json(args.early_warning_signal_map),
            load_required_json(args.institutional_status),
            load_required_json(args.queue_health_dashboard),
            load_required_json(args.priority_dashboard),
            load_required_json(args.closure_registry),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_symbolic_field_registry.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_early_warning_dashboard.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_regime_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_symbolic_field_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote symbolic field registry: {args.out_symbolic_field_registry}")
    print(f"[OK] Wrote early-warning dashboard: {args.out_early_warning_dashboard}")
    print(f"[OK] Wrote regime watchlist: {args.out_regime_watchlist}")
    print(f"[OK] Wrote symbolic field annotations: {args.out_symbolic_field_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
