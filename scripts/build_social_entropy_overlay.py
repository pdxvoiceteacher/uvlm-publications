#!/usr/bin/env python3
"""Build social entropy and civic cohesion overlays.

Publisher surfaces only Sophia-audited social-entropy materials; no automatic
suppression, ranking of persons, or coercive normalization occurs from this
layer.
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
    commits = prov.get("producerCommits")
    if not isinstance(commits, list) or not commits or not all(isinstance(v, str) and v.strip() for v in commits):
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


def _validate_outputs(social_entropy_dashboard: dict[str, Any], civic_cohesion_registry: dict[str, Any], legitimacy_watchlist: dict[str, Any], social_repair_annotations: dict[str, Any]) -> None:
    if not isinstance(social_entropy_dashboard.get("entries"), list):
        raise ValueError("social_entropy_dashboard.entries must be a list")
    if not isinstance(civic_cohesion_registry.get("entries"), list):
        raise ValueError("civic_cohesion_registry.entries must be a list")
    if not isinstance(legitimacy_watchlist.get("entries"), list):
        raise ValueError("legitimacy_watchlist.entries must be a list")
    if not isinstance(social_repair_annotations.get("annotations"), list):
        raise ValueError("social_repair_annotations.annotations must be a list")
    for payload in (social_entropy_dashboard, civic_cohesion_registry, legitimacy_watchlist, social_repair_annotations):
        json.dumps(payload)


def build_social_entropy_overlays(
    social_entropy_audit: dict[str, Any],
    social_entropy_recommendations: dict[str, Any],
    social_entropy_map: dict[str, Any],
    civic_cohesion_report: dict[str, Any],
    legitimacy_drift_report: dict[str, Any],
    review_participation_risk_map: dict[str, Any],
    collaborative_review_dashboard: dict[str, Any],
    theory_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    architecture_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "social_entropy_audit": _extract_required_provenance("social_entropy_audit", social_entropy_audit),
        "social_entropy_recommendations": _extract_required_provenance("social_entropy_recommendations", social_entropy_recommendations),
        "social_entropy_map": _extract_required_provenance("social_entropy_map", social_entropy_map),
        "civic_cohesion_report": _extract_required_provenance("civic_cohesion_report", civic_cohesion_report),
        "legitimacy_drift_report": _extract_required_provenance("legitimacy_drift_report", legitimacy_drift_report),
        "review_participation_risk_map": _extract_required_provenance("review_participation_risk_map", review_participation_risk_map),
    }
    for name, artifact in {
        "collaborative_review_dashboard": collaborative_review_dashboard,
        "theory_dashboard": theory_dashboard,
        "value_dashboard": value_dashboard,
        "architecture_dashboard": architecture_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(social_entropy_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(social_entropy_recommendations.get("recommendations")) if isinstance(e, dict)]
    entropy_entries = [e for e in as_list(social_entropy_map.get("entries")) if isinstance(e, dict)]
    cohesion_entries = [e for e in as_list(civic_cohesion_report.get("entries")) if isinstance(e, dict)]
    legitimacy_entries = [e for e in as_list(legitimacy_drift_report.get("entries")) if isinstance(e, dict)]
    participation_entries = [e for e in as_list(review_participation_risk_map.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    entropy_by_review = _index_by_key(entropy_entries, "reviewId")
    cohesion_by_review = _index_by_key(cohesion_entries, "reviewId")
    legitimacy_by_review = _index_by_key(legitimacy_entries, "reviewId")
    participation_by_review = _index_by_key(participation_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        entropy = entropy_by_review.get(review_id, {})
        cohesion = cohesion_by_review.get(review_id, {})
        legitimacy = legitimacy_by_review.get(review_id, {})
        participation = participation_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        social_status = str(entropy.get("socialStatus", rec.get("socialStatus", "monitor")))
        social_entropy = _to_float(entropy.get("socialEntropy", rec.get("socialEntropy", 0.0)))
        cohesion_class = str(cohesion.get("cohesionClass", rec.get("cohesionClass", "mixed")))
        legitimacy_drift = str(legitimacy.get("legitimacyDrift", rec.get("legitimacyDrift", "bounded")))
        reviewer_concentration = _to_float(participation.get("reviewerConcentration", rec.get("reviewerConcentration", 0.0)))
        reviewer_fatigue = str(participation.get("reviewerFatigue", rec.get("reviewerFatigue", "bounded")))
        repair_priority = str(rec.get("repairPriority", "routine"))
        audit_state = str(audit.get("socialEntropyAuditState", rec.get("socialEntropyAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "socialStatus": social_status,
            "socialEntropy": social_entropy,
            "cohesionClass": cohesion_class,
            "legitimacyDrift": legitimacy_drift,
            "reviewerConcentration": reviewer_concentration,
            "reviewerFatigue": reviewer_fatigue,
            "repairPriority": repair_priority,
            "socialEntropyAuditState": audit_state,
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
            "noAutomaticSuppression": True,
            "noRankingOfPersons": True,
            "noCoerciveNormalization": True,
            "noTheoryStatusMutation": True,
            "noIdentityMutation": True,
            "noGovernanceRightsMutation": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    social_entropy_dashboard = {
        "generatedAt": generated_at,
        "socialEntropyProtocol": True,
        "nonCanonical": True,
        "noAutomaticSuppression": True,
        "noRankingOfPersons": True,
        "noCoerciveNormalization": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    civic_cohesion_registry = {
        "generatedAt": generated_at,
        "socialEntropyProtocol": True,
        "nonCanonical": True,
        "noAutomaticSuppression": True,
        "noRankingOfPersons": True,
        "noCoerciveNormalization": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    legitimacy_watchlist = {
        "generatedAt": generated_at,
        "socialEntropyProtocol": True,
        "nonCanonical": True,
        "noAutomaticSuppression": True,
        "noRankingOfPersons": True,
        "noCoerciveNormalization": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    social_repair_annotations = {
        "generatedAt": generated_at,
        "socialEntropyProtocol": True,
        "nonCanonical": True,
        "noAutomaticSuppression": True,
        "noRankingOfPersons": True,
        "noCoerciveNormalization": True,
        "noTheoryStatusMutation": True,
        "noIdentityMutation": True,
        "noGovernanceRightsMutation": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(social_entropy_dashboard, civic_cohesion_registry, legitimacy_watchlist, social_repair_annotations)
    return social_entropy_dashboard, civic_cohesion_registry, legitimacy_watchlist, social_repair_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--social-entropy-audit", type=Path, default=Path("bridge/social_entropy_audit.json"))
    parser.add_argument("--social-entropy-recommendations", type=Path, default=Path("bridge/social_entropy_recommendations.json"))
    parser.add_argument("--social-entropy-map", type=Path, default=Path("bridge/social_entropy_map.json"))
    parser.add_argument("--civic-cohesion-report", type=Path, default=Path("bridge/civic_cohesion_report.json"))
    parser.add_argument("--legitimacy-drift-report", type=Path, default=Path("bridge/legitimacy_drift_report.json"))
    parser.add_argument("--review-participation-risk-map", type=Path, default=Path("bridge/review_participation_risk_map.json"))

    parser.add_argument("--collaborative-review-dashboard", type=Path, default=Path("registry/collaborative_review_dashboard.json"))
    parser.add_argument("--theory-dashboard", type=Path, default=Path("registry/theory_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))
    parser.add_argument("--architecture-dashboard", type=Path, default=Path("registry/architecture_dashboard.json"))

    parser.add_argument("--out-social-entropy-dashboard", type=Path, default=Path("registry/social_entropy_dashboard.json"))
    parser.add_argument("--out-civic-cohesion-registry", type=Path, default=Path("registry/civic_cohesion_registry.json"))
    parser.add_argument("--out-legitimacy-watchlist", type=Path, default=Path("registry/legitimacy_watchlist.json"))
    parser.add_argument("--out-social-repair-annotations", type=Path, default=Path("registry/social_repair_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_social_entropy_overlays(
            load_required_json(args.social_entropy_audit),
            load_required_json(args.social_entropy_recommendations),
            load_required_json(args.social_entropy_map),
            load_required_json(args.civic_cohesion_report),
            load_required_json(args.legitimacy_drift_report),
            load_required_json(args.review_participation_risk_map),
            load_required_json(args.collaborative_review_dashboard),
            load_required_json(args.theory_dashboard),
            load_required_json(args.value_dashboard),
            load_required_json(args.architecture_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_social_entropy_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_civic_cohesion_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_legitimacy_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_social_repair_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_social_entropy_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_civic_cohesion_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_legitimacy_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_social_repair_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote social entropy dashboard: {args.out_social_entropy_dashboard}")
    print(f"[OK] Wrote civic cohesion registry: {args.out_civic_cohesion_registry}")
    print(f"[OK] Wrote legitimacy watchlist: {args.out_legitimacy_watchlist}")
    print(f"[OK] Wrote social repair annotations: {args.out_social_repair_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
