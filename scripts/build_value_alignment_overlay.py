#!/usr/bin/env python3
"""Build value alignment overlays.

Publisher surfaces only Sophia-audited value-alignment materials;
knowledge priorities may guide attention but cannot replace human communities'
authority over final value judgments.
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


def _validate_outputs(value_dashboard: dict[str, Any], knowledge_priority_registry: dict[str, Any], value_risk_watchlist: dict[str, Any], value_annotations: dict[str, Any]) -> None:
    if not isinstance(value_dashboard.get("entries"), list):
        raise ValueError("value_dashboard.entries must be a list")
    if not isinstance(knowledge_priority_registry.get("entries"), list):
        raise ValueError("knowledge_priority_registry.entries must be a list")
    if not isinstance(value_risk_watchlist.get("entries"), list):
        raise ValueError("value_risk_watchlist.entries must be a list")
    if not isinstance(value_annotations.get("annotations"), list):
        raise ValueError("value_annotations.annotations must be a list")
    for payload in (value_dashboard, knowledge_priority_registry, value_risk_watchlist, value_annotations):
        json.dumps(payload)


def build_value_alignment_overlays(
    value_alignment_audit: dict[str, Any],
    value_alignment_recommendations: dict[str, Any],
    knowledge_priority_map: dict[str, Any],
    welfare_impact_report: dict[str, Any],
    fairness_impact_report: dict[str, Any],
    value_risk_report: dict[str, Any],
    uncertainty_dashboard: dict[str, Any],
    responsibility_dashboard: dict[str, Any],
    system_forecast_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "value_alignment_audit": _extract_required_provenance("value_alignment_audit", value_alignment_audit),
        "value_alignment_recommendations": _extract_required_provenance("value_alignment_recommendations", value_alignment_recommendations),
        "knowledge_priority_map": _extract_required_provenance("knowledge_priority_map", knowledge_priority_map),
        "welfare_impact_report": _extract_required_provenance("welfare_impact_report", welfare_impact_report),
        "fairness_impact_report": _extract_required_provenance("fairness_impact_report", fairness_impact_report),
        "value_risk_report": _extract_required_provenance("value_risk_report", value_risk_report),
    }
    for name, artifact in {
        "uncertainty_dashboard": uncertainty_dashboard,
        "responsibility_dashboard": responsibility_dashboard,
        "system_forecast_dashboard": system_forecast_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(value_alignment_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(value_alignment_recommendations.get("recommendations")) if isinstance(e, dict)]
    priorities = [e for e in as_list(knowledge_priority_map.get("entries")) if isinstance(e, dict)]
    welfare = [e for e in as_list(welfare_impact_report.get("entries")) if isinstance(e, dict)]
    fairness = [e for e in as_list(fairness_impact_report.get("entries")) if isinstance(e, dict)]
    risks = [e for e in as_list(value_risk_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    priority_by_review = _index_by_key(priorities, "reviewId")
    welfare_by_review = _index_by_key(welfare, "reviewId")
    fairness_by_review = _index_by_key(fairness, "reviewId")
    risk_by_review = _index_by_key(risks, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        prio = priority_by_review.get(review_id, {})
        welf = welfare_by_review.get(review_id, {})
        fair = fairness_by_review.get(review_id, {})
        risk = risk_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        knowledge_priority_rank = int(_to_float(prio.get("knowledgePriorityRank", rec.get("knowledgePriorityRank", 99)), 99.0))
        welfare_impact_score = _to_float(welf.get("welfareImpactScore", rec.get("welfareImpactScore", 0.0)))
        welfare_impact_indicator = str(welf.get("welfareImpactIndicator", rec.get("welfareImpactIndicator", "monitor")))
        fairness_impact_marker = str(fair.get("fairnessImpactMarker", rec.get("fairnessImpactMarker", "monitor")))
        value_risk_flag = str(risk.get("valueRiskFlag", rec.get("valueRiskFlag", "bounded")))
        value_risk_score = _to_float(risk.get("valueRiskScore", rec.get("valueRiskScore", 0.0)))
        alignment_audit_state = str(audit.get("valueAlignmentAuditState", rec.get("valueAlignmentAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "knowledgePriorityRank": knowledge_priority_rank,
            "welfareImpactScore": welfare_impact_score,
            "welfareImpactIndicator": welfare_impact_indicator,
            "fairnessImpactMarker": fairness_impact_marker,
            "valueRiskFlag": value_risk_flag,
            "valueRiskScore": value_risk_score,
            "valueAlignmentAuditState": alignment_audit_state,
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
            "humanCommunitiesRetainFinalValueAuthority": True,
            "triadIlluminatesMoralConsequencesNotEthicsReplacement": True,
            "noAutomaticValueJudgmentExecution": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    value_dashboard = {
        "generatedAt": generated_at,
        "valueAlignmentProtocol": True,
        "nonCanonical": True,
        "humanCommunitiesRetainFinalValueAuthority": True,
        "triadIlluminatesMoralConsequencesNotEthicsReplacement": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    knowledge_priority_registry = {
        "generatedAt": generated_at,
        "valueAlignmentProtocol": True,
        "nonCanonical": True,
        "humanCommunitiesRetainFinalValueAuthority": True,
        "triadIlluminatesMoralConsequencesNotEthicsReplacement": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    value_risk_watchlist = {
        "generatedAt": generated_at,
        "valueAlignmentProtocol": True,
        "nonCanonical": True,
        "humanCommunitiesRetainFinalValueAuthority": True,
        "triadIlluminatesMoralConsequencesNotEthicsReplacement": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    value_annotations = {
        "generatedAt": generated_at,
        "valueAlignmentProtocol": True,
        "nonCanonical": True,
        "humanCommunitiesRetainFinalValueAuthority": True,
        "triadIlluminatesMoralConsequencesNotEthicsReplacement": True,
        "noAutomaticValueJudgmentExecution": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(value_dashboard, knowledge_priority_registry, value_risk_watchlist, value_annotations)
    return value_dashboard, knowledge_priority_registry, value_risk_watchlist, value_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--value-alignment-audit", type=Path, default=Path("bridge/value_alignment_audit.json"))
    parser.add_argument("--value-alignment-recommendations", type=Path, default=Path("bridge/value_alignment_recommendations.json"))
    parser.add_argument("--knowledge-priority-map", type=Path, default=Path("bridge/knowledge_priority_map.json"))
    parser.add_argument("--welfare-impact-report", type=Path, default=Path("bridge/welfare_impact_report.json"))
    parser.add_argument("--fairness-impact-report", type=Path, default=Path("bridge/fairness_impact_report.json"))
    parser.add_argument("--value-risk-report", type=Path, default=Path("bridge/value_risk_report.json"))

    parser.add_argument("--uncertainty-dashboard", type=Path, default=Path("registry/uncertainty_dashboard.json"))
    parser.add_argument("--responsibility-dashboard", type=Path, default=Path("registry/responsibility_dashboard.json"))
    parser.add_argument("--system-forecast-dashboard", type=Path, default=Path("registry/system_forecast_dashboard.json"))

    parser.add_argument("--out-value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))
    parser.add_argument("--out-knowledge-priority-registry", type=Path, default=Path("registry/knowledge_priority_registry.json"))
    parser.add_argument("--out-value-risk-watchlist", type=Path, default=Path("registry/value_risk_watchlist.json"))
    parser.add_argument("--out-value-annotations", type=Path, default=Path("registry/value_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_value_alignment_overlays(
            load_required_json(args.value_alignment_audit),
            load_required_json(args.value_alignment_recommendations),
            load_required_json(args.knowledge_priority_map),
            load_required_json(args.welfare_impact_report),
            load_required_json(args.fairness_impact_report),
            load_required_json(args.value_risk_report),
            load_required_json(args.uncertainty_dashboard),
            load_required_json(args.responsibility_dashboard),
            load_required_json(args.system_forecast_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_value_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_knowledge_priority_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_value_risk_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_value_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_value_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_knowledge_priority_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_value_risk_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_value_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote value dashboard: {args.out_value_dashboard}")
    print(f"[OK] Wrote knowledge priority registry: {args.out_knowledge_priority_registry}")
    print(f"[OK] Wrote value risk watchlist: {args.out_value_risk_watchlist}")
    print(f"[OK] Wrote value annotations: {args.out_value_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
