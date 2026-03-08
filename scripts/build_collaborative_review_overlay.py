#!/usr/bin/env python3
"""Build collaborative review, consensus, and dissent overlays.

Publisher surfaces only Sophia-audited collaborative-review materials; no
automatic consensus ratification or dissent suppression occurs from this layer.
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


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    return action if action in {"docket", "watch", "suppressed", "rejected"} else "watch"


def _targets(rec: dict[str, Any]) -> list[str]:
    return sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)])


def _validate_outputs(
    collaborative_review_dashboard: dict[str, Any],
    consensus_registry: dict[str, Any],
    dissent_watchlist: dict[str, Any],
    deliberation_annotations: dict[str, Any],
) -> None:
    if not isinstance(collaborative_review_dashboard.get("entries"), list):
        raise ValueError("collaborative_review_dashboard.entries must be a list")
    if not isinstance(consensus_registry.get("entries"), list):
        raise ValueError("consensus_registry.entries must be a list")
    if not isinstance(dissent_watchlist.get("entries"), list):
        raise ValueError("dissent_watchlist.entries must be a list")
    if not isinstance(deliberation_annotations.get("annotations"), list):
        raise ValueError("deliberation_annotations.annotations must be a list")
    for payload in (collaborative_review_dashboard, consensus_registry, dissent_watchlist, deliberation_annotations):
        json.dumps(payload)


def build_collaborative_review_overlays(
    collaborative_review_audit: dict[str, Any],
    collaborative_review_recommendations: dict[str, Any],
    reviewer_deliberation_map: dict[str, Any],
    reviewer_position_map: dict[str, Any],
    consensus_state_report: dict[str, Any],
    dissent_trace_report: dict[str, Any],
    review_packet_dashboard: dict[str, Any],
    causal_dashboard: dict[str, Any],
    authority_gate_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "collaborative_review_audit": _extract_required_provenance("collaborative_review_audit", collaborative_review_audit),
        "collaborative_review_recommendations": _extract_required_provenance("collaborative_review_recommendations", collaborative_review_recommendations),
        "reviewer_deliberation_map": _extract_required_provenance("reviewer_deliberation_map", reviewer_deliberation_map),
        "reviewer_position_map": _extract_required_provenance("reviewer_position_map", reviewer_position_map),
        "consensus_state_report": _extract_required_provenance("consensus_state_report", consensus_state_report),
        "dissent_trace_report": _extract_required_provenance("dissent_trace_report", dissent_trace_report),
    }
    for name, artifact in {
        "review_packet_dashboard": review_packet_dashboard,
        "causal_dashboard": causal_dashboard,
        "authority_gate_dashboard": authority_gate_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(collaborative_review_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(collaborative_review_recommendations.get("recommendations")) if isinstance(r, dict)]
    deliberation_entries = [e for e in as_list(reviewer_deliberation_map.get("entries")) if isinstance(e, dict)]
    position_entries = [e for e in as_list(reviewer_position_map.get("entries")) if isinstance(e, dict)]
    consensus_entries = [e for e in as_list(consensus_state_report.get("entries")) if isinstance(e, dict)]
    dissent_entries = [e for e in as_list(dissent_trace_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    deliberation_by_review = _index_by_key(deliberation_entries, "reviewId")
    position_by_review = _index_by_key(position_entries, "reviewId")
    consensus_by_review = _index_by_key(consensus_entries, "reviewId")
    dissent_by_review = _index_by_key(dissent_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    consensus_registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        deliberation = deliberation_by_review.get(review_id, {})
        position = position_by_review.get(review_id, {})
        consensus = consensus_by_review.get(review_id, {})
        dissent = dissent_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        collaborative_status = str(deliberation.get("collaborativeStatus", rec.get("collaborativeStatus", "in-review")))
        consensus_class = str(consensus.get("consensusClass", rec.get("consensusClass", "contested")))
        dissent_presence = bool(dissent.get("dissentPresent", rec.get("dissentPresent", False)))
        dissent_trace_count = int(dissent.get("dissentTraceCount", rec.get("dissentTraceCount", 0)) or 0)
        maturity_constraints = sorted([x for x in as_list(position.get("maturityConstraints", rec.get("maturityConstraints", []))) if isinstance(x, str)])
        reviewer_positions = sorted([x for x in as_list(position.get("reviewerPositions", rec.get("reviewerPositions", []))) if isinstance(x, str)])
        collaborative_audit_state = str(audit.get("collaborativeAuditState", rec.get("collaborativeAuditState", "none")))
        linked_target_ids = _targets(rec)

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "collaborativeStatus": collaborative_status,
                "consensusClass": consensus_class,
                "dissentPresent": dissent_presence,
                "dissentTraceCount": dissent_trace_count,
                "maturityConstraints": maturity_constraints,
                "reviewerPositions": reviewer_positions,
                "collaborativeAuditState": collaborative_audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            dashboard_entries.append(entry)
            consensus_registry_entries.append({**entry, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "collaborativeStatus": collaborative_status,
                    "consensusClass": consensus_class,
                    "dissentPresent": dissent_presence,
                    "dissentTraceCount": dissent_trace_count,
                    "maturityConstraints": maturity_constraints,
                    "reviewerPositions": reviewer_positions,
                    "collaborativeAuditState": collaborative_audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        annotation_entries.append(
            {
                "reviewId": review_id,
                "targetPublisherAction": action,
                "collaborativeStatus": collaborative_status,
                "consensusClass": consensus_class,
                "dissentPresent": dissent_presence,
                "dissentTraceCount": dissent_trace_count,
                "maturityConstraints": maturity_constraints,
                "reviewerPositions": reviewer_positions,
                "collaborativeAuditState": collaborative_audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticConsensusRatification": True,
                "noAutomaticDissentSuppression": True,
                "noAutomaticGraphMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    collaborative_review_dashboard = {
        "generatedAt": generated_at,
        "collaborativeReviewProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    consensus_registry = {
        "generatedAt": generated_at,
        "collaborativeReviewProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(consensus_registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    dissent_watchlist = {
        "generatedAt": generated_at,
        "collaborativeReviewProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    deliberation_annotations = {
        "generatedAt": generated_at,
        "collaborativeReviewProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticConsensusRatification": True,
        "noAutomaticDissentSuppression": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(collaborative_review_dashboard, consensus_registry, dissent_watchlist, deliberation_annotations)
    return collaborative_review_dashboard, consensus_registry, dissent_watchlist, deliberation_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collaborative-review-audit", type=Path, default=Path("bridge/collaborative_review_audit.json"))
    parser.add_argument("--collaborative-review-recommendations", type=Path, default=Path("bridge/collaborative_review_recommendations.json"))
    parser.add_argument("--reviewer-deliberation-map", type=Path, default=Path("bridge/reviewer_deliberation_map.json"))
    parser.add_argument("--reviewer-position-map", type=Path, default=Path("bridge/reviewer_position_map.json"))
    parser.add_argument("--consensus-state-report", type=Path, default=Path("bridge/consensus_state_report.json"))
    parser.add_argument("--dissent-trace-report", type=Path, default=Path("bridge/dissent_trace_report.json"))

    parser.add_argument("--review-packet-dashboard", type=Path, default=Path("registry/review_packet_dashboard.json"))
    parser.add_argument("--causal-dashboard", type=Path, default=Path("registry/causal_dashboard.json"))
    parser.add_argument("--authority-gate-dashboard", type=Path, default=Path("registry/authority_gate_dashboard.json"))

    parser.add_argument("--out-collaborative-review-dashboard", type=Path, default=Path("registry/collaborative_review_dashboard.json"))
    parser.add_argument("--out-consensus-registry", type=Path, default=Path("registry/consensus_registry.json"))
    parser.add_argument("--out-dissent-watchlist", type=Path, default=Path("registry/dissent_watchlist.json"))
    parser.add_argument("--out-deliberation-annotations", type=Path, default=Path("registry/deliberation_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_collaborative_review_overlays(
            load_required_json(args.collaborative_review_audit),
            load_required_json(args.collaborative_review_recommendations),
            load_required_json(args.reviewer_deliberation_map),
            load_required_json(args.reviewer_position_map),
            load_required_json(args.consensus_state_report),
            load_required_json(args.dissent_trace_report),
            load_required_json(args.review_packet_dashboard),
            load_required_json(args.causal_dashboard),
            load_required_json(args.authority_gate_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_collaborative_review_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_consensus_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_dissent_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_deliberation_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_collaborative_review_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_consensus_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_dissent_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_deliberation_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote collaborative review dashboard: {args.out_collaborative_review_dashboard}")
    print(f"[OK] Wrote consensus registry: {args.out_consensus_registry}")
    print(f"[OK] Wrote dissent watchlist: {args.out_dissent_watchlist}")
    print(f"[OK] Wrote deliberation annotations: {args.out_deliberation_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
