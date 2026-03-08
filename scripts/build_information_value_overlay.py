#!/usr/bin/env python3
"""Build uncertainty and information-value overlays.

Publisher surfaces only Sophia-audited information-value materials;
information-seeking may prioritize attention but never justify surveillance
expansion without explicit human authorization.
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


def _validate_outputs(uncertainty_dashboard: dict[str, Any], observation_priority_registry: dict[str, Any], curiosity_watchlist: dict[str, Any], curiosity_annotations: dict[str, Any]) -> None:
    if not isinstance(uncertainty_dashboard.get("entries"), list):
        raise ValueError("uncertainty_dashboard.entries must be a list")
    if not isinstance(observation_priority_registry.get("entries"), list):
        raise ValueError("observation_priority_registry.entries must be a list")
    if not isinstance(curiosity_watchlist.get("entries"), list):
        raise ValueError("curiosity_watchlist.entries must be a list")
    if not isinstance(curiosity_annotations.get("annotations"), list):
        raise ValueError("curiosity_annotations.annotations must be a list")
    for payload in (uncertainty_dashboard, observation_priority_registry, curiosity_watchlist, curiosity_annotations):
        json.dumps(payload)


def build_information_value_overlays(
    information_value_audit: dict[str, Any],
    information_value_recommendations: dict[str, Any],
    uncertainty_map: dict[str, Any],
    information_gain_report: dict[str, Any],
    experiment_priority_map: dict[str, Any],
    entropy_reduction_forecast: dict[str, Any],
    system_forecast_dashboard: dict[str, Any],
    experiment_dashboard: dict[str, Any],
    theory_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "information_value_audit": _extract_required_provenance("information_value_audit", information_value_audit),
        "information_value_recommendations": _extract_required_provenance("information_value_recommendations", information_value_recommendations),
        "uncertainty_map": _extract_required_provenance("uncertainty_map", uncertainty_map),
        "information_gain_report": _extract_required_provenance("information_gain_report", information_gain_report),
        "experiment_priority_map": _extract_required_provenance("experiment_priority_map", experiment_priority_map),
        "entropy_reduction_forecast": _extract_required_provenance("entropy_reduction_forecast", entropy_reduction_forecast),
    }
    for name, artifact in {
        "system_forecast_dashboard": system_forecast_dashboard,
        "experiment_dashboard": experiment_dashboard,
        "theory_dashboard": theory_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(information_value_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(information_value_recommendations.get("recommendations")) if isinstance(e, dict)]
    uncertainty_entries = [e for e in as_list(uncertainty_map.get("entries")) if isinstance(e, dict)]
    gain_entries = [e for e in as_list(information_gain_report.get("entries")) if isinstance(e, dict)]
    priority_entries = [e for e in as_list(experiment_priority_map.get("entries")) if isinstance(e, dict)]
    entropy_entries = [e for e in as_list(entropy_reduction_forecast.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    uncertainty_by_review = _index_by_key(uncertainty_entries, "reviewId")
    gain_by_review = _index_by_key(gain_entries, "reviewId")
    priority_by_review = _index_by_key(priority_entries, "reviewId")
    entropy_by_review = _index_by_key(entropy_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        unc = uncertainty_by_review.get(review_id, {})
        gain = gain_by_review.get(review_id, {})
        prio = priority_by_review.get(review_id, {})
        ent = entropy_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        uncertainty_gradient = str(unc.get("uncertaintyGradient", rec.get("uncertaintyGradient", "moderate")))
        information_gain = _to_float(gain.get("informationGain", rec.get("informationGain", 0.0)))
        experiment_priority = str(prio.get("experimentPriority", rec.get("experimentPriority", "monitor")))
        entropy_reduction_forecast_value = _to_float(ent.get("entropyReductionForecast", rec.get("entropyReductionForecast", 0.0)))
        audit_state = str(audit.get("informationValueAuditState", rec.get("informationValueAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "uncertaintyGradient": uncertainty_gradient,
            "informationGain": information_gain,
            "experimentPriority": experiment_priority,
            "entropyReductionForecast": entropy_reduction_forecast_value,
            "informationValueAuditState": audit_state,
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
            "noSurveillanceExpansionWithoutHumanAuthorization": True,
            "curiosityGuidesInvestigationNotIntrusion": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    uncertainty_dashboard = {
        "generatedAt": generated_at,
        "informationValueProtocol": True,
        "nonCanonical": True,
        "noSurveillanceExpansionWithoutHumanAuthorization": True,
        "curiosityGuidesInvestigationNotIntrusion": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    observation_priority_registry = {
        "generatedAt": generated_at,
        "informationValueProtocol": True,
        "nonCanonical": True,
        "noSurveillanceExpansionWithoutHumanAuthorization": True,
        "curiosityGuidesInvestigationNotIntrusion": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    curiosity_watchlist = {
        "generatedAt": generated_at,
        "informationValueProtocol": True,
        "nonCanonical": True,
        "noSurveillanceExpansionWithoutHumanAuthorization": True,
        "curiosityGuidesInvestigationNotIntrusion": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    curiosity_annotations = {
        "generatedAt": generated_at,
        "informationValueProtocol": True,
        "nonCanonical": True,
        "noSurveillanceExpansionWithoutHumanAuthorization": True,
        "curiosityGuidesInvestigationNotIntrusion": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(uncertainty_dashboard, observation_priority_registry, curiosity_watchlist, curiosity_annotations)
    return uncertainty_dashboard, observation_priority_registry, curiosity_watchlist, curiosity_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--information-value-audit", type=Path, default=Path("bridge/information_value_audit.json"))
    parser.add_argument("--information-value-recommendations", type=Path, default=Path("bridge/information_value_recommendations.json"))
    parser.add_argument("--uncertainty-map", type=Path, default=Path("bridge/uncertainty_map.json"))
    parser.add_argument("--information-gain-report", type=Path, default=Path("bridge/information_gain_report.json"))
    parser.add_argument("--experiment-priority-map", type=Path, default=Path("bridge/experiment_priority_map.json"))
    parser.add_argument("--entropy-reduction-forecast", type=Path, default=Path("bridge/entropy_reduction_forecast.json"))

    parser.add_argument("--system-forecast-dashboard", type=Path, default=Path("registry/system_forecast_dashboard.json"))
    parser.add_argument("--experiment-dashboard", type=Path, default=Path("registry/experiment_dashboard.json"))
    parser.add_argument("--theory-dashboard", type=Path, default=Path("registry/theory_dashboard.json"))

    parser.add_argument("--out-uncertainty-dashboard", type=Path, default=Path("registry/uncertainty_dashboard.json"))
    parser.add_argument("--out-observation-priority-registry", type=Path, default=Path("registry/observation_priority_registry.json"))
    parser.add_argument("--out-curiosity-watchlist", type=Path, default=Path("registry/curiosity_watchlist.json"))
    parser.add_argument("--out-curiosity-annotations", type=Path, default=Path("registry/curiosity_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_information_value_overlays(
            load_required_json(args.information_value_audit),
            load_required_json(args.information_value_recommendations),
            load_required_json(args.uncertainty_map),
            load_required_json(args.information_gain_report),
            load_required_json(args.experiment_priority_map),
            load_required_json(args.entropy_reduction_forecast),
            load_required_json(args.system_forecast_dashboard),
            load_required_json(args.experiment_dashboard),
            load_required_json(args.theory_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_uncertainty_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_observation_priority_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_curiosity_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_curiosity_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_uncertainty_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_observation_priority_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_curiosity_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_curiosity_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote uncertainty dashboard: {args.out_uncertainty_dashboard}")
    print(f"[OK] Wrote observation priority registry: {args.out_observation_priority_registry}")
    print(f"[OK] Wrote curiosity watchlist: {args.out_curiosity_watchlist}")
    print(f"[OK] Wrote curiosity annotations: {args.out_curiosity_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
