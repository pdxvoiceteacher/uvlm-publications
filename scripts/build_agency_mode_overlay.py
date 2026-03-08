#!/usr/bin/env python3
"""Build agency-mode comparator and governance-switching overlays.

Publisher surfaces only Sophia-audited agency-mode materials; no automatic
metaphysical classification or canonical mutation occurs from this layer.
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


def _validate_outputs(agency_mode_dashboard: dict[str, Any], agency_fit_registry: dict[str, Any], agency_disagreement_watchlist: dict[str, Any], agency_governance_annotations: dict[str, Any]) -> None:
    if not isinstance(agency_mode_dashboard.get("entries"), list):
        raise ValueError("agency_mode_dashboard.entries must be a list")
    if not isinstance(agency_fit_registry.get("entries"), list):
        raise ValueError("agency_fit_registry.entries must be a list")
    if not isinstance(agency_disagreement_watchlist.get("entries"), list):
        raise ValueError("agency_disagreement_watchlist.entries must be a list")
    if not isinstance(agency_governance_annotations.get("annotations"), list):
        raise ValueError("agency_governance_annotations.annotations must be a list")
    for payload in (agency_mode_dashboard, agency_fit_registry, agency_disagreement_watchlist, agency_governance_annotations):
        json.dumps(payload)


def build_agency_mode_overlays(
    agency_mode_audit: dict[str, Any],
    agency_mode_recommendations: dict[str, Any],
    agency_mode_hypothesis_map: dict[str, Any],
    agency_fit_comparison_report: dict[str, Any],
    tel_branch_signature_map: dict[str, Any],
    agency_governance_mode_gate: dict[str, Any],
    theory_dashboard: dict[str, Any],
    prediction_dashboard: dict[str, Any],
    experiment_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "agency_mode_audit": _extract_required_provenance("agency_mode_audit", agency_mode_audit),
        "agency_mode_recommendations": _extract_required_provenance("agency_mode_recommendations", agency_mode_recommendations),
        "agency_mode_hypothesis_map": _extract_required_provenance("agency_mode_hypothesis_map", agency_mode_hypothesis_map),
        "agency_fit_comparison_report": _extract_required_provenance("agency_fit_comparison_report", agency_fit_comparison_report),
        "tel_branch_signature_map": _extract_required_provenance("tel_branch_signature_map", tel_branch_signature_map),
        "agency_governance_mode_gate": _extract_required_provenance("agency_governance_mode_gate", agency_governance_mode_gate),
    }
    for name, artifact in {
        "theory_dashboard": theory_dashboard,
        "prediction_dashboard": prediction_dashboard,
        "experiment_dashboard": experiment_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(agency_mode_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(agency_mode_recommendations.get("recommendations")) if isinstance(e, dict)]
    hypotheses = [e for e in as_list(agency_mode_hypothesis_map.get("entries")) if isinstance(e, dict)]
    fits = [e for e in as_list(agency_fit_comparison_report.get("entries")) if isinstance(e, dict)]
    signatures = [e for e in as_list(tel_branch_signature_map.get("entries")) if isinstance(e, dict)]
    gates = [e for e in as_list(agency_governance_mode_gate.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    hypothesis_by_review = _index_by_key(hypotheses, "reviewId")
    fit_by_review = _index_by_key(fits, "reviewId")
    signature_by_review = _index_by_key(signatures, "reviewId")
    gate_by_review = _index_by_key(gates, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        hypothesis = hypothesis_by_review.get(review_id, {})
        fit = fit_by_review.get(review_id, {})
        signature = signature_by_review.get(review_id, {})
        gate = gate_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        agency_status = str(hypothesis.get("agencyStatus", rec.get("agencyStatus", "under-review")))
        deterministic_fit = float(fit.get("deterministicFit", rec.get("deterministicFit", 0.0)) or 0.0)
        volitional_fit = float(fit.get("volitionalFit", rec.get("volitionalFit", 0.0)) or 0.0)
        provisional_v_hat = float(fit.get("provisionalVHat", rec.get("provisionalVHat", 0.0)) or 0.0)
        tel_branch_signature = str(signature.get("telBranchSignature", rec.get("telBranchSignature", "untyped")))
        governance_mode_class = str(gate.get("governanceModeClass", rec.get("governanceModeClass", "bounded-watch")))
        consent_signal = str(gate.get("consentSignal", rec.get("consentSignal", "required")))
        blame_suppression_signal = str(gate.get("blameSuppressionSignal", rec.get("blameSuppressionSignal", "enabled")))
        agency_audit_state = str(audit.get("agencyAuditState", rec.get("agencyAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "agencyStatus": agency_status,
            "deterministicFit": deterministic_fit,
            "volitionalFit": volitional_fit,
            "provisionalVHat": provisional_v_hat,
            "telBranchSignature": tel_branch_signature,
            "governanceModeClass": governance_mode_class,
            "consentSignal": consent_signal,
            "blameSuppressionSignal": blame_suppression_signal,
            "agencyAuditState": agency_audit_state,
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
            "noAutomaticMetaphysicalClassification": True,
            "noAutomaticGovernanceMutation": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    agency_mode_dashboard = {
        "generatedAt": generated_at,
        "agencyModeProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    agency_fit_registry = {
        "generatedAt": generated_at,
        "agencyModeProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    agency_disagreement_watchlist = {
        "generatedAt": generated_at,
        "agencyModeProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    agency_governance_annotations = {
        "generatedAt": generated_at,
        "agencyModeProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticMetaphysicalClassification": True,
        "noAutomaticGovernanceMutation": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(agency_mode_dashboard, agency_fit_registry, agency_disagreement_watchlist, agency_governance_annotations)
    return agency_mode_dashboard, agency_fit_registry, agency_disagreement_watchlist, agency_governance_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agency-mode-audit", type=Path, default=Path("bridge/agency_mode_audit.json"))
    parser.add_argument("--agency-mode-recommendations", type=Path, default=Path("bridge/agency_mode_recommendations.json"))
    parser.add_argument("--agency-mode-hypothesis-map", type=Path, default=Path("bridge/agency_mode_hypothesis_map.json"))
    parser.add_argument("--agency-fit-comparison-report", type=Path, default=Path("bridge/agency_fit_comparison_report.json"))
    parser.add_argument("--tel-branch-signature-map", type=Path, default=Path("bridge/tel_branch_signature_map.json"))
    parser.add_argument("--agency-governance-mode-gate", type=Path, default=Path("bridge/agency_governance_mode_gate.json"))

    parser.add_argument("--theory-dashboard", type=Path, default=Path("registry/theory_dashboard.json"))
    parser.add_argument("--prediction-dashboard", type=Path, default=Path("registry/prediction_dashboard.json"))
    parser.add_argument("--experiment-dashboard", type=Path, default=Path("registry/experiment_dashboard.json"))

    parser.add_argument("--out-agency-mode-dashboard", type=Path, default=Path("registry/agency_mode_dashboard.json"))
    parser.add_argument("--out-agency-fit-registry", type=Path, default=Path("registry/agency_fit_registry.json"))
    parser.add_argument("--out-agency-disagreement-watchlist", type=Path, default=Path("registry/agency_disagreement_watchlist.json"))
    parser.add_argument("--out-agency-governance-annotations", type=Path, default=Path("registry/agency_governance_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_agency_mode_overlays(
            load_required_json(args.agency_mode_audit),
            load_required_json(args.agency_mode_recommendations),
            load_required_json(args.agency_mode_hypothesis_map),
            load_required_json(args.agency_fit_comparison_report),
            load_required_json(args.tel_branch_signature_map),
            load_required_json(args.agency_governance_mode_gate),
            load_required_json(args.theory_dashboard),
            load_required_json(args.prediction_dashboard),
            load_required_json(args.experiment_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_agency_mode_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_agency_fit_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_agency_disagreement_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_agency_governance_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_agency_mode_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_agency_fit_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_agency_disagreement_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_agency_governance_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote agency mode dashboard: {args.out_agency_mode_dashboard}")
    print(f"[OK] Wrote agency fit registry: {args.out_agency_fit_registry}")
    print(f"[OK] Wrote agency disagreement watchlist: {args.out_agency_disagreement_watchlist}")
    print(f"[OK] Wrote agency governance annotations: {args.out_agency_governance_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
