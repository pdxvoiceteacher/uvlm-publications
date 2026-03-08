#!/usr/bin/env python3
"""Build prediction and calibration overlays.

Publisher surfaces only Sophia-audited prediction materials; no automatic
canonical mutation occurs from this layer.
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


def _validate_outputs(prediction_dashboard: dict[str, Any], forecast_registry: dict[str, Any], prediction_watchlist: dict[str, Any], calibration_annotations: dict[str, Any]) -> None:
    if not isinstance(prediction_dashboard.get("entries"), list):
        raise ValueError("prediction_dashboard.entries must be a list")
    if not isinstance(forecast_registry.get("entries"), list):
        raise ValueError("forecast_registry.entries must be a list")
    if not isinstance(prediction_watchlist.get("entries"), list):
        raise ValueError("prediction_watchlist.entries must be a list")
    if not isinstance(calibration_annotations.get("annotations"), list):
        raise ValueError("calibration_annotations.annotations must be a list")
    for payload in (prediction_dashboard, forecast_registry, prediction_watchlist, calibration_annotations):
        json.dumps(payload)


def build_prediction_overlays(
    prediction_audit: dict[str, Any],
    prediction_recommendations: dict[str, Any],
    forecast_map: dict[str, Any],
    calibration_report: dict[str, Any],
    branch_reliability_report: dict[str, Any],
    prediction_outcome_timeline: dict[str, Any],
    branch_dashboard: dict[str, Any],
    telemetry_dashboard: dict[str, Any],
    collaborative_review_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "prediction_audit": _extract_required_provenance("prediction_audit", prediction_audit),
        "prediction_recommendations": _extract_required_provenance("prediction_recommendations", prediction_recommendations),
        "forecast_map": _extract_required_provenance("forecast_map", forecast_map),
        "calibration_report": _extract_required_provenance("calibration_report", calibration_report),
        "branch_reliability_report": _extract_required_provenance("branch_reliability_report", branch_reliability_report),
        "prediction_outcome_timeline": _extract_required_provenance("prediction_outcome_timeline", prediction_outcome_timeline),
    }
    for name, artifact in {
        "branch_dashboard": branch_dashboard,
        "telemetry_dashboard": telemetry_dashboard,
        "collaborative_review_dashboard": collaborative_review_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(prediction_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(prediction_recommendations.get("recommendations")) if isinstance(r, dict)]
    forecasts = [e for e in as_list(forecast_map.get("entries")) if isinstance(e, dict)]
    calibration = [e for e in as_list(calibration_report.get("entries")) if isinstance(e, dict)]
    reliability = [e for e in as_list(branch_reliability_report.get("entries")) if isinstance(e, dict)]
    outcomes = [e for e in as_list(prediction_outcome_timeline.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    forecast_by_review = _index_by_key(forecasts, "reviewId")
    calibration_by_review = _index_by_key(calibration, "reviewId")
    reliability_by_review = _index_by_key(reliability, "reviewId")
    outcomes_by_review = _index_by_key(outcomes, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        forecast = forecast_by_review.get(review_id, {})
        calib = calibration_by_review.get(review_id, {})
        reli = reliability_by_review.get(review_id, {})
        outcome = outcomes_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        forecast_accuracy = str(forecast.get("forecastAccuracy", rec.get("forecastAccuracy", "unknown")))
        forecast_confidence = str(forecast.get("forecastConfidence", rec.get("forecastConfidence", "bounded")))
        calibration_trend = str(calib.get("calibrationTrend", rec.get("calibrationTrend", "stable")))
        calibration_error = float(calib.get("calibrationError", rec.get("calibrationError", 0.0)) or 0.0)
        branch_reliability = str(reli.get("branchReliability", rec.get("branchReliability", "unknown")))
        reliability_score = float(reli.get("reliabilityScore", rec.get("reliabilityScore", 0.0)) or 0.0)
        outcome_timeline = sorted([x for x in as_list(outcome.get("outcomeTimeline", rec.get("outcomeTimeline", []))) if isinstance(x, dict)], key=lambda e: str(e.get("date", "")))
        prediction_audit_state = str(audit.get("predictionAuditState", rec.get("predictionAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "forecastAccuracy": forecast_accuracy,
            "forecastConfidence": forecast_confidence,
            "calibrationTrend": calibration_trend,
            "calibrationError": calibration_error,
            "branchReliability": branch_reliability,
            "reliabilityScore": reliability_score,
            "outcomeTimeline": outcome_timeline,
            "predictionAuditState": prediction_audit_state,
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
            "noAutomaticPredictionPromotion": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    prediction_dashboard = {
        "generatedAt": generated_at,
        "predictionProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    forecast_registry = {
        "generatedAt": generated_at,
        "predictionProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    prediction_watchlist = {
        "generatedAt": generated_at,
        "predictionProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    calibration_annotations = {
        "generatedAt": generated_at,
        "predictionProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticPredictionPromotion": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(prediction_dashboard, forecast_registry, prediction_watchlist, calibration_annotations)
    return prediction_dashboard, forecast_registry, prediction_watchlist, calibration_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prediction-audit", type=Path, default=Path("bridge/prediction_audit.json"))
    parser.add_argument("--prediction-recommendations", type=Path, default=Path("bridge/prediction_recommendations.json"))
    parser.add_argument("--forecast-map", type=Path, default=Path("bridge/forecast_map.json"))
    parser.add_argument("--calibration-report", type=Path, default=Path("bridge/calibration_report.json"))
    parser.add_argument("--branch-reliability-report", type=Path, default=Path("bridge/branch_reliability_report.json"))
    parser.add_argument("--prediction-outcome-timeline", type=Path, default=Path("bridge/prediction_outcome_timeline.json"))

    parser.add_argument("--branch-dashboard", type=Path, default=Path("registry/branch_dashboard.json"))
    parser.add_argument("--telemetry-dashboard", type=Path, default=Path("registry/telemetry_dashboard.json"))
    parser.add_argument("--collaborative-review-dashboard", type=Path, default=Path("registry/collaborative_review_dashboard.json"))

    parser.add_argument("--out-prediction-dashboard", type=Path, default=Path("registry/prediction_dashboard.json"))
    parser.add_argument("--out-forecast-registry", type=Path, default=Path("registry/forecast_registry.json"))
    parser.add_argument("--out-prediction-watchlist", type=Path, default=Path("registry/prediction_watchlist.json"))
    parser.add_argument("--out-calibration-annotations", type=Path, default=Path("registry/calibration_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_prediction_overlays(
            load_required_json(args.prediction_audit),
            load_required_json(args.prediction_recommendations),
            load_required_json(args.forecast_map),
            load_required_json(args.calibration_report),
            load_required_json(args.branch_reliability_report),
            load_required_json(args.prediction_outcome_timeline),
            load_required_json(args.branch_dashboard),
            load_required_json(args.telemetry_dashboard),
            load_required_json(args.collaborative_review_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_prediction_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_forecast_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_prediction_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_calibration_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_prediction_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_forecast_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_prediction_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_calibration_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote prediction dashboard: {args.out_prediction_dashboard}")
    print(f"[OK] Wrote forecast registry: {args.out_forecast_registry}")
    print(f"[OK] Wrote prediction watchlist: {args.out_prediction_watchlist}")
    print(f"[OK] Wrote calibration annotations: {args.out_calibration_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
