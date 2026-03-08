#!/usr/bin/env python3
"""Build investigation dashboard, plan registry, and watch overlays.

This script composes triage, verification, and public-record recommendation streams
into bounded non-canonical investigation artifacts for Atlas rendering.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

REQUIRED_PROVENANCE_KEYS = ("schemaVersion", "producerCommits", "sourceMode")


STAGE_ORDER = {
    "intake": 1,
    "triage": 1,
    "verification": 2,
    "corroboration": 2,
    "dependency-mapping": 3,
    "plan-execution": 4,
    "closed": 5,
}


def load_required_json(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"Missing required canonical artifact: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in required canonical artifact {path}: {exc}") from exc


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


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


def _stage_from_recommendation(rec: dict[str, Any], fallback: str) -> str:
    value = str(rec.get("investigationStage", fallback)).strip().lower()
    if value not in STAGE_ORDER:
        return fallback
    return value


def _progress_from_stage(stage: str) -> float:
    return round(max(0, min(5, STAGE_ORDER.get(stage, 1))) / 5, 2)


def _targets(rec: dict[str, Any]) -> list[str]:
    return sorted([target for target in as_list(rec.get("linkedTargetIds")) if isinstance(target, str)])


def build_investigation_overlays(
    triage_recommendations: dict[str, Any],
    verification_recommendations: dict[str, Any],
    public_record_recommendations: dict[str, Any],
    artifact_escrow_plan: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "triage_recommendations": _extract_required_provenance("triage_recommendations", triage_recommendations),
        "verification_recommendations": _extract_required_provenance("verification_recommendations", verification_recommendations),
        "public_record_recommendations": _extract_required_provenance("public_record_recommendations", public_record_recommendations),
    }
    provenance_summary = _build_provenance_summary(provenances)

    triage_recs = [r for r in as_list(triage_recommendations.get("recommendations")) if isinstance(r, dict)]
    verification_recs = [r for r in as_list(verification_recommendations.get("recommendations")) if isinstance(r, dict)]
    public_record_recs = [r for r in as_list(public_record_recommendations.get("recommendations")) if isinstance(r, dict)]
    escrow_entries = [e for e in as_list(artifact_escrow_plan.get("entries")) if isinstance(e, dict)]

    dependency_nodes: list[dict[str, Any]] = []
    dependency_edges: list[dict[str, Any]] = []
    for entry in escrow_entries:
        artifact_id = entry.get("artifactId")
        if not isinstance(artifact_id, str):
            continue
        dependency_nodes.append({"id": artifact_id, "kind": "artifact"})
        for dep in [d for d in as_list(entry.get("dependencyPaths")) if isinstance(d, str)]:
            dependency_nodes.append({"id": dep, "kind": "dependency"})
            dependency_edges.append({"source": dep, "target": artifact_id, "relation": "dependsOn"})

    unique_nodes = {node["id"]: node for node in dependency_nodes}
    dependency_graph = {
        "nodes": sorted(unique_nodes.values(), key=lambda n: str(n.get("id", ""))),
        "edges": sorted(dependency_edges, key=lambda e: f"{e.get('source','')}->{e.get('target','')}")
    }

    investigation_entries: list[dict[str, Any]] = []
    plan_registry_entries: list[dict[str, Any]] = []
    watchlist_entries: list[dict[str, Any]] = []
    annotations: list[dict[str, Any]] = []

    combined = [
        ("triage", triage_recs, "intake"),
        ("verification", verification_recs, "verification"),
        ("public-record", public_record_recs, "dependency-mapping"),
    ]

    for source_name, rows, default_stage in combined:
        for rec in sorted(rows, key=lambda r: str(r.get("reviewId", ""))):
            review_id = rec.get("reviewId")
            if not isinstance(review_id, str):
                continue
            action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
            if action not in {"docket", "watch", "suppressed", "rejected"}:
                action = "watch"

            linked_target_ids = _targets(rec)
            stage = _stage_from_recommendation(rec, default_stage)
            plan_status = "active" if action == "docket" else "watch"
            progress = _progress_from_stage(stage)
            blocked_dependencies = [e.get("artifactId") for e in escrow_entries if str(e.get("escrowStatus", "")) != "ready-for-review"]
            blocked_dependencies = [x for x in blocked_dependencies if isinstance(x, str)]
            total_steps = max(1, STAGE_ORDER.get(stage, 1))
            completed_steps = max(0, min(total_steps, int(round(progress * total_steps))))
            plan_id = f"investigation-plan:{review_id}"

            if action == "docket":
                dashboard_entry = {
                    "reviewId": review_id,
                    "source": source_name,
                    "investigationStage": stage,
                    "stageRank": STAGE_ORDER.get(stage, 1),
                    "planStatus": plan_status,
                    "planProgress": progress,
                    "linkedTargetIds": linked_target_ids,
                    "dependencyGraph": dependency_graph,
                    "dependencyCount": len(dependency_graph["edges"]),
                    "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                    "queuedAt": generated_at,
                }
                investigation_entries.append(dashboard_entry)
                plan_registry_entries.append(
                    {
                        "planId": plan_id,
                        "reviewId": review_id,
                        "investigationStage": stage,
                        "planStatus": plan_status,
                        "totalSteps": total_steps,
                        "completedSteps": completed_steps,
                        "planProgress": progress,
                        "blockedBy": sorted(set(blocked_dependencies)),
                        "dependencyCount": len(dependency_graph["edges"]),
                        "linkedTargetIds": linked_target_ids,
                        "updatedAt": generated_at,
                    }
                )

            if action == "watch":
                watchlist_entries.append(
                    {
                        "reviewId": review_id,
                        "source": source_name,
                        "status": "watch",
                        "investigationStage": stage,
                        "planProgress": progress,
                        "dependencyCount": len(dependency_graph["edges"]),
                        "linkedTargetIds": linked_target_ids,
                        "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                        "observational": True,
                        "nonCanonical": True,
                        "queuedAt": generated_at,
                    }
                )

            annotations.append(
                {
                    "reviewId": review_id,
                    "source": source_name,
                    "targetPublisherAction": action,
                    "investigationStage": stage,
                    "planProgress": progress,
                    "dependencyCount": len(dependency_graph["edges"]),
                    "linkedTargetIds": linked_target_ids,
                    "noAutomaticAccusation": True,
                    "noAutomaticPlanMutation": True,
                    "noCanonicalMutation": True,
                    "notes": rec.get("notes", ""),
                }
            )

    dashboard = {
        "generatedAt": generated_at,
        "investigationProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(investigation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    plan_registry = {
        "generatedAt": generated_at,
        "investigationProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(plan_registry_entries, key=lambda e: str(e.get("planId", ""))),
    }
    watchlist = {
        "generatedAt": generated_at,
        "investigationProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watchlist_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    annotation_artifact = {
        "generatedAt": generated_at,
        "investigationProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticAccusation": True,
        "noAutomaticPlanMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotations, key=lambda e: str(e.get("reviewId", ""))),
    }
    return dashboard, plan_registry, watchlist, annotation_artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage-recommendations", type=Path, default=Path("bridge/triage_recommendations.json"))
    parser.add_argument("--verification-recommendations", type=Path, default=Path("bridge/verification_recommendations.json"))
    parser.add_argument("--public-record-recommendations", type=Path, default=Path("bridge/public_record_recommendations.json"))
    parser.add_argument("--artifact-escrow-plan", type=Path, default=Path("bridge/artifact_escrow_plan.json"))
    parser.add_argument("--investigation-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--out-investigation-dashboard", type=Path, default=Path("registry/investigation_dashboard.json"))
    parser.add_argument("--out-investigation-plan-registry", type=Path, default=Path("registry/investigation_plan_registry.json"))
    parser.add_argument("--out-investigation-watchlist", type=Path, default=Path("registry/investigation_watchlist.json"))
    parser.add_argument("--out-investigation-annotations", type=Path, default=Path("registry/investigation_annotations.json"))

    args = parser.parse_args()

    if args.investigation_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --investigation-snapshot is no longer supported. Use canonical investigation artifacts.")
        return 2

    try:
        outputs = build_investigation_overlays(
            load_required_json(args.triage_recommendations),
            load_required_json(args.verification_recommendations),
            load_required_json(args.public_record_recommendations),
            load_required_json(args.artifact_escrow_plan),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_investigation_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_investigation_plan_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_investigation_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_investigation_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_investigation_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_investigation_plan_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_investigation_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_investigation_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote investigation dashboard: {args.out_investigation_dashboard}")
    print(f"[OK] Wrote investigation plan registry: {args.out_investigation_plan_registry}")
    print(f"[OK] Wrote investigation watchlist: {args.out_investigation_watchlist}")
    print(f"[OK] Wrote investigation annotations: {args.out_investigation_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
