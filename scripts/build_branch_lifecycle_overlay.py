#!/usr/bin/env python3
"""Build branch lifecycle overlays for bounded review-facing branch signals.

Publisher surfaces only Sophia-audited branch lifecycle materials; no automatic
branch activation or canonical mutation occurs from this layer.
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
    return {
        "schemaVersions": schema_versions,
        "producerCommits": producer_commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": any(mode.lower() == "fixture" for mode in source_modes.values()),
    }


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    return action if action in {"docket", "watch", "suppressed", "rejected"} else "watch"


def _targets(rec: dict[str, Any]) -> list[str]:
    return sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])


def _validate_outputs(branch_dashboard: dict[str, Any], branch_registry: dict[str, Any], branch_watchlist: dict[str, Any], branch_annotations: dict[str, Any]) -> None:
    if not isinstance(branch_dashboard.get("entries"), list):
        raise ValueError("branch_dashboard.entries must be a list")
    if not isinstance(branch_registry.get("entries"), list):
        raise ValueError("branch_registry.entries must be a list")
    if not isinstance(branch_watchlist.get("entries"), list):
        raise ValueError("branch_watchlist.entries must be a list")
    if not isinstance(branch_annotations.get("annotations"), list):
        raise ValueError("branch_annotations.annotations must be a list")
    for payload in (branch_dashboard, branch_registry, branch_watchlist, branch_annotations):
        json.dumps(payload)


def build_branch_lifecycle_overlays(
    branch_lifecycle_audit: dict[str, Any],
    branch_lifecycle_recommendations: dict[str, Any],
    branch_state_map: dict[str, Any],
    branch_conflict_graph: dict[str, Any],
    branch_decay_report: dict[str, Any],
    branch_reinforcement_trend: dict[str, Any],
    telemetry_dashboard: dict[str, Any],
    causal_dashboard: dict[str, Any],
    collaborative_review_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "branch_lifecycle_audit": _extract_required_provenance("branch_lifecycle_audit", branch_lifecycle_audit),
        "branch_lifecycle_recommendations": _extract_required_provenance("branch_lifecycle_recommendations", branch_lifecycle_recommendations),
        "branch_state_map": _extract_required_provenance("branch_state_map", branch_state_map),
        "branch_conflict_graph": _extract_required_provenance("branch_conflict_graph", branch_conflict_graph),
        "branch_decay_report": _extract_required_provenance("branch_decay_report", branch_decay_report),
        "branch_reinforcement_trend": _extract_required_provenance("branch_reinforcement_trend", branch_reinforcement_trend),
    }
    for name, artifact in {
        "telemetry_dashboard": telemetry_dashboard,
        "causal_dashboard": causal_dashboard,
        "collaborative_review_dashboard": collaborative_review_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(branch_lifecycle_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(branch_lifecycle_recommendations.get("recommendations")) if isinstance(r, dict)]
    state_entries = [e for e in as_list(branch_state_map.get("entries")) if isinstance(e, dict)]
    conflict_entries = [e for e in as_list(branch_conflict_graph.get("entries")) if isinstance(e, dict)]
    decay_entries = [e for e in as_list(branch_decay_report.get("entries")) if isinstance(e, dict)]
    trend_entries = [e for e in as_list(branch_reinforcement_trend.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    state_by_review = _index_by_key(state_entries, "reviewId")
    conflict_by_review = _index_by_key(conflict_entries, "reviewId")
    decay_by_review = _index_by_key(decay_entries, "reviewId")
    trend_by_review = _index_by_key(trend_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        state = state_by_review.get(review_id, {})
        conflict = conflict_by_review.get(review_id, {})
        decay = decay_by_review.get(review_id, {})
        trend = trend_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        branch_status = str(state.get("branchLifecycleStatus", rec.get("branchLifecycleStatus", "monitor")))
        branch_stage = str(state.get("branchStage", rec.get("branchStage", "emergent")))
        conflict_nodes = sorted([x for x in as_list(conflict.get("conflictNodes", rec.get("conflictNodes", []))) if isinstance(x, str)])
        conflict_edges = sorted([x for x in as_list(conflict.get("conflictEdges", rec.get("conflictEdges", []))) if isinstance(x, str)])
        decay_risk = str(decay.get("decayRisk", rec.get("decayRisk", "low")))
        decay_signals = sorted([x for x in as_list(decay.get("decaySignals", rec.get("decaySignals", []))) if isinstance(x, str)])
        reinforcement_trend = str(trend.get("reinforcementTrend", rec.get("reinforcementTrend", "balanced")))
        contradiction_trend = str(trend.get("contradictionTrend", rec.get("contradictionTrend", "low")))
        branch_audit_state = str(audit.get("branchAuditState", rec.get("branchAuditState", "none")))
        linked_target_ids = _targets(rec)

        entry = {
            "reviewId": review_id,
            "branchLifecycleStatus": branch_status,
            "branchStage": branch_stage,
            "conflictNodes": conflict_nodes,
            "conflictEdges": conflict_edges,
            "decayRisk": decay_risk,
            "decaySignals": decay_signals,
            "reinforcementTrend": reinforcement_trend,
            "contradictionTrend": contradiction_trend,
            "branchAuditState": branch_audit_state,
            "linkedTargetIds": linked_target_ids,
        }

        if action == "docket":
            dashboard_entries.append({**entry, "humanReviewFlag": bool(rec.get("humanReviewFlag", True)), "queuedAt": generated_at})
            registry_entries.append({**entry, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({
                **entry,
                "status": "watch",
                "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                "observational": True,
                "nonCanonical": True,
                "queuedAt": generated_at,
            })

        annotation_entries.append({
            **entry,
            "targetPublisherAction": action,
            "noAutomaticBranchActivation": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    branch_dashboard = {
        "generatedAt": generated_at,
        "branchLifecycleProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    branch_registry = {
        "generatedAt": generated_at,
        "branchLifecycleProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    branch_watchlist = {
        "generatedAt": generated_at,
        "branchLifecycleProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    branch_annotations = {
        "generatedAt": generated_at,
        "branchLifecycleProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticBranchActivation": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(branch_dashboard, branch_registry, branch_watchlist, branch_annotations)
    return branch_dashboard, branch_registry, branch_watchlist, branch_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch-lifecycle-audit", type=Path, default=Path("bridge/branch_lifecycle_audit.json"))
    parser.add_argument("--branch-lifecycle-recommendations", type=Path, default=Path("bridge/branch_lifecycle_recommendations.json"))
    parser.add_argument("--branch-state-map", type=Path, default=Path("bridge/branch_state_map.json"))
    parser.add_argument("--branch-conflict-graph", type=Path, default=Path("bridge/branch_conflict_graph.json"))
    parser.add_argument("--branch-decay-report", type=Path, default=Path("bridge/branch_decay_report.json"))
    parser.add_argument("--branch-reinforcement-trend", type=Path, default=Path("bridge/branch_reinforcement_trend.json"))

    parser.add_argument("--telemetry-dashboard", type=Path, default=Path("registry/telemetry_dashboard.json"))
    parser.add_argument("--causal-dashboard", type=Path, default=Path("registry/causal_dashboard.json"))
    parser.add_argument("--collaborative-review-dashboard", type=Path, default=Path("registry/collaborative_review_dashboard.json"))

    parser.add_argument("--out-branch-dashboard", type=Path, default=Path("registry/branch_dashboard.json"))
    parser.add_argument("--out-branch-registry", type=Path, default=Path("registry/branch_registry.json"))
    parser.add_argument("--out-branch-watchlist", type=Path, default=Path("registry/branch_watchlist.json"))
    parser.add_argument("--out-branch-annotations", type=Path, default=Path("registry/branch_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_branch_lifecycle_overlays(
            load_required_json(args.branch_lifecycle_audit),
            load_required_json(args.branch_lifecycle_recommendations),
            load_required_json(args.branch_state_map),
            load_required_json(args.branch_conflict_graph),
            load_required_json(args.branch_decay_report),
            load_required_json(args.branch_reinforcement_trend),
            load_required_json(args.telemetry_dashboard),
            load_required_json(args.causal_dashboard),
            load_required_json(args.collaborative_review_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_branch_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_branch_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_branch_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_branch_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_branch_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_branch_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_branch_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_branch_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote branch dashboard: {args.out_branch_dashboard}")
    print(f"[OK] Wrote branch registry: {args.out_branch_registry}")
    print(f"[OK] Wrote branch watchlist: {args.out_branch_watchlist}")
    print(f"[OK] Wrote branch annotations: {args.out_branch_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
