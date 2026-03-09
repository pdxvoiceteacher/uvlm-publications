#!/usr/bin/env python3
"""Build architecture overlays.

Publisher surfaces only Sophia-audited architecture materials;
architecture proposals may guide review but cannot mutate safeguards or canonical
state without explicit human approval.
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

    schema_version = prov.get("schemaVersion")
    if not isinstance(schema_version, str) or not schema_version.strip():
        raise ValueError(f"{name} provenance.schemaVersion must be a non-empty string")
    producer_commits = prov.get("producerCommits")
    if not isinstance(producer_commits, list) or not producer_commits or not all(isinstance(v, str) and v.strip() for v in producer_commits):
        raise ValueError(f"{name} provenance.producerCommits must be a non-empty list of non-empty strings")
    source_mode = prov.get("sourceMode")
    if not isinstance(source_mode, str) or not source_mode.strip():
        raise ValueError(f"{name} provenance.sourceMode must be a non-empty string")
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


def _to_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError:
            return default
    return default


def _validate_outputs(architecture_dashboard: dict[str, Any], module_performance_registry: dict[str, Any], architecture_watchlist: dict[str, Any], architecture_annotations: dict[str, Any]) -> None:
    if not isinstance(architecture_dashboard.get("entries"), list):
        raise ValueError("architecture_dashboard.entries must be a list")
    if not isinstance(module_performance_registry.get("entries"), list):
        raise ValueError("module_performance_registry.entries must be a list")
    if not isinstance(architecture_watchlist.get("entries"), list):
        raise ValueError("architecture_watchlist.entries must be a list")
    if not isinstance(architecture_annotations.get("annotations"), list):
        raise ValueError("architecture_annotations.annotations must be a list")
    for payload in (architecture_dashboard, module_performance_registry, architecture_watchlist, architecture_annotations):
        json.dumps(payload)


def build_architecture_overlays(
    architecture_audit: dict[str, Any],
    architecture_recommendations: dict[str, Any],
    module_performance_report: dict[str, Any],
    discovery_productivity_report: dict[str, Any],
    safeguard_performance_report: dict[str, Any],
    architecture_proposal_report: dict[str, Any],
    meta_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    responsibility_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "architecture_audit": _extract_required_provenance("architecture_audit", architecture_audit),
        "architecture_recommendations": _extract_required_provenance("architecture_recommendations", architecture_recommendations),
        "module_performance_report": _extract_required_provenance("module_performance_report", module_performance_report),
        "discovery_productivity_report": _extract_required_provenance("discovery_productivity_report", discovery_productivity_report),
        "safeguard_performance_report": _extract_required_provenance("safeguard_performance_report", safeguard_performance_report),
        "architecture_proposal_report": _extract_required_provenance("architecture_proposal_report", architecture_proposal_report),
    }
    for name, artifact in {
        "meta_dashboard": meta_dashboard,
        "value_dashboard": value_dashboard,
        "responsibility_dashboard": responsibility_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(architecture_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(architecture_recommendations.get("recommendations")) if isinstance(e, dict)]
    module_entries = [e for e in as_list(module_performance_report.get("entries")) if isinstance(e, dict)]
    discovery_entries = [e for e in as_list(discovery_productivity_report.get("entries")) if isinstance(e, dict)]
    safeguard_entries = [e for e in as_list(safeguard_performance_report.get("entries")) if isinstance(e, dict)]
    proposal_entries = [e for e in as_list(architecture_proposal_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    module_by_review = _index_by_key(module_entries, "reviewId")
    discovery_by_review = _index_by_key(discovery_entries, "reviewId")
    safeguard_by_review = _index_by_key(safeguard_entries, "reviewId")
    proposal_by_review = _index_by_key(proposal_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        module = module_by_review.get(review_id, {})
        discovery = discovery_by_review.get(review_id, {})
        safeguard = safeguard_by_review.get(review_id, {})
        proposal = proposal_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        module_performance = str(module.get("modulePerformance", rec.get("modulePerformance", "monitor")))
        module_performance_score = _to_float(module.get("modulePerformanceScore", rec.get("modulePerformanceScore", 0.0)))
        discovery_productivity = _to_float(discovery.get("discoveryProductivity", rec.get("discoveryProductivity", 0.0)))
        safeguard_performance = str(safeguard.get("safeguardPerformance", rec.get("safeguardPerformance", "bounded")))
        architecture_improvement_proposal = str(proposal.get("architectureImprovementProposal", rec.get("architectureImprovementProposal", "none")))
        architecture_audit_state = str(audit.get("architectureAuditState", rec.get("architectureAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "modulePerformance": module_performance,
            "modulePerformanceScore": module_performance_score,
            "discoveryProductivity": discovery_productivity,
            "safeguardPerformance": safeguard_performance,
            "architectureImprovementProposal": architecture_improvement_proposal,
            "architectureAuditState": architecture_audit_state,
            "linkedTargetIds": linked_target_ids,
        }

        if action == "docket":
            dashboard_entries.append({**base, "humanReviewFlag": bool(rec.get("humanReviewFlag", True)), "queuedAt": generated_at})
            registry_entries.append({**base, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append({
                **base,
                "status": "watch",
                "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                "observational": True,
                "nonCanonical": True,
                "queuedAt": generated_at,
            })

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "noAutonomousCoreSafetyMutation": True,
            "humanApprovalRequiredForArchitectureChanges": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    architecture_dashboard = {
        "generatedAt": generated_at,
        "architectureProtocol": True,
        "nonCanonical": True,
        "noAutonomousCoreSafetyMutation": True,
        "humanApprovalRequiredForArchitectureChanges": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    module_performance_registry = {
        "generatedAt": generated_at,
        "architectureProtocol": True,
        "nonCanonical": True,
        "noAutonomousCoreSafetyMutation": True,
        "humanApprovalRequiredForArchitectureChanges": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    architecture_watchlist = {
        "generatedAt": generated_at,
        "architectureProtocol": True,
        "nonCanonical": True,
        "noAutonomousCoreSafetyMutation": True,
        "humanApprovalRequiredForArchitectureChanges": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    architecture_annotations = {
        "generatedAt": generated_at,
        "architectureProtocol": True,
        "nonCanonical": True,
        "noAutonomousCoreSafetyMutation": True,
        "humanApprovalRequiredForArchitectureChanges": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(architecture_dashboard, module_performance_registry, architecture_watchlist, architecture_annotations)
    return architecture_dashboard, module_performance_registry, architecture_watchlist, architecture_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture-audit", type=Path, default=Path("bridge/architecture_audit.json"))
    parser.add_argument("--architecture-recommendations", type=Path, default=Path("bridge/architecture_recommendations.json"))
    parser.add_argument("--module-performance-report", type=Path, default=Path("bridge/module_performance_report.json"))
    parser.add_argument("--discovery-productivity-report", type=Path, default=Path("bridge/discovery_productivity_report.json"))
    parser.add_argument("--safeguard-performance-report", type=Path, default=Path("bridge/safeguard_performance_report.json"))
    parser.add_argument("--architecture-proposal-report", type=Path, default=Path("bridge/architecture_proposal_report.json"))

    parser.add_argument("--meta-dashboard", type=Path, default=Path("registry/meta_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))
    parser.add_argument("--responsibility-dashboard", type=Path, default=Path("registry/responsibility_dashboard.json"))

    parser.add_argument("--out-architecture-dashboard", type=Path, default=Path("registry/architecture_dashboard.json"))
    parser.add_argument("--out-module-performance-registry", type=Path, default=Path("registry/module_performance_registry.json"))
    parser.add_argument("--out-architecture-watchlist", type=Path, default=Path("registry/architecture_watchlist.json"))
    parser.add_argument("--out-architecture-annotations", type=Path, default=Path("registry/architecture_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_architecture_overlays(
            load_required_json(args.architecture_audit),
            load_required_json(args.architecture_recommendations),
            load_required_json(args.module_performance_report),
            load_required_json(args.discovery_productivity_report),
            load_required_json(args.safeguard_performance_report),
            load_required_json(args.architecture_proposal_report),
            load_required_json(args.meta_dashboard),
            load_required_json(args.value_dashboard),
            load_required_json(args.responsibility_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_architecture_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_module_performance_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_architecture_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_architecture_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_architecture_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_module_performance_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_architecture_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_architecture_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote architecture dashboard: {args.out_architecture_dashboard}")
    print(f"[OK] Wrote module performance registry: {args.out_module_performance_registry}")
    print(f"[OK] Wrote architecture watchlist: {args.out_architecture_watchlist}")
    print(f"[OK] Wrote architecture annotations: {args.out_architecture_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
