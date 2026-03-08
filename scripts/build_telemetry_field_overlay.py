#!/usr/bin/env python3
"""Build telemetry-field, lattice, and total-action-functional overlays.

Publisher surfaces only Sophia-audited telemetry-field and TAF materials; no
automatic branch activation or canonical mutation occurs from this layer.
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


def _validate_outputs(
    telemetry_dashboard: dict[str, Any],
    lattice_projection_registry: dict[str, Any],
    pattern_donation_watchlist: dict[str, Any],
    action_functional_annotations: dict[str, Any],
) -> None:
    if not isinstance(telemetry_dashboard.get("entries"), list):
        raise ValueError("telemetry_dashboard.entries must be a list")
    if not isinstance(lattice_projection_registry.get("entries"), list):
        raise ValueError("lattice_projection_registry.entries must be a list")
    if not isinstance(pattern_donation_watchlist.get("entries"), list):
        raise ValueError("pattern_donation_watchlist.entries must be a list")
    if not isinstance(action_functional_annotations.get("annotations"), list):
        raise ValueError("action_functional_annotations.annotations must be a list")
    for payload in (telemetry_dashboard, lattice_projection_registry, pattern_donation_watchlist, action_functional_annotations):
        json.dumps(payload)


def build_telemetry_field_overlays(
    telemetry_field_audit: dict[str, Any],
    telemetry_field_recommendations: dict[str, Any],
    telemetry_field_map: dict[str, Any],
    lattice_projection_map: dict[str, Any],
    pattern_donation_registry: dict[str, Any],
    action_functional_scorecard: dict[str, Any],
    branch_emergence_report: dict[str, Any],
    symbolic_field_registry: dict[str, Any],
    investigation_dashboard: dict[str, Any],
    authority_gate_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "telemetry_field_audit": _extract_required_provenance("telemetry_field_audit", telemetry_field_audit),
        "telemetry_field_recommendations": _extract_required_provenance("telemetry_field_recommendations", telemetry_field_recommendations),
        "telemetry_field_map": _extract_required_provenance("telemetry_field_map", telemetry_field_map),
        "lattice_projection_map": _extract_required_provenance("lattice_projection_map", lattice_projection_map),
        "pattern_donation_registry": _extract_required_provenance("pattern_donation_registry", pattern_donation_registry),
        "action_functional_scorecard": _extract_required_provenance("action_functional_scorecard", action_functional_scorecard),
        "branch_emergence_report": _extract_required_provenance("branch_emergence_report", branch_emergence_report),
    }
    for name, artifact in {
        "symbolic_field_registry": symbolic_field_registry,
        "investigation_dashboard": investigation_dashboard,
        "authority_gate_dashboard": authority_gate_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(telemetry_field_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(telemetry_field_recommendations.get("recommendations")) if isinstance(r, dict)]
    fields = [e for e in as_list(telemetry_field_map.get("entries")) if isinstance(e, dict)]
    lattice = [e for e in as_list(lattice_projection_map.get("entries")) if isinstance(e, dict)]
    donations = [e for e in as_list(pattern_donation_registry.get("entries")) if isinstance(e, dict)]
    taf = [e for e in as_list(action_functional_scorecard.get("entries")) if isinstance(e, dict)]
    branch = [e for e in as_list(branch_emergence_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    field_by_review = _index_by_key(fields, "reviewId")
    lattice_by_review = _index_by_key(lattice, "reviewId")
    donation_by_review = _index_by_key(donations, "reviewId")
    taf_by_review = _index_by_key(taf, "reviewId")
    branch_by_review = _index_by_key(branch, "reviewId")

    telemetry_entries: list[dict[str, Any]] = []
    lattice_registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        field = field_by_review.get(review_id, {})
        lat = lattice_by_review.get(review_id, {})
        donation = donation_by_review.get(review_id, {})
        taf_entry = taf_by_review.get(review_id, {})
        branch_entry = branch_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        telemetry_field_status = str(field.get("telemetryFieldStatus", rec.get("telemetryFieldStatus", "monitor")))
        latticeCoordinates = str(lat.get("latticeCoordinates", rec.get("latticeCoordinates", "0,0,0")))
        latticeRegime = str(lat.get("latticeRegime", rec.get("latticeRegime", "bounded-order")))
        donorPatternPedigree = sorted([x for x in as_list(donation.get("donorPatternPedigree", rec.get("donorPatternPedigree", []))) if isinstance(x, str)])
        donation_watch_status = str(donation.get("donationWatchStatus", rec.get("donationWatchStatus", "none")))
        tafScoreSummary = str(taf_entry.get("tafScoreSummary", rec.get("tafScoreSummary", "bounded")))
        tafScore = float(taf_entry.get("tafScore", rec.get("tafScore", 0.0)) or 0.0)
        branchNovelty = str(branch_entry.get("branchNovelty", rec.get("branchNovelty", "low")))
        maturityCeiling = str(branch_entry.get("maturityCeiling", rec.get("maturityCeiling", "bounded-review")))
        telemetry_audit_state = str(audit.get("telemetryAuditState", rec.get("telemetryAuditState", "none")))
        linked_target_ids = _targets(rec)

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "telemetryFieldStatus": telemetry_field_status,
                "latticeCoordinates": latticeCoordinates,
                "latticeRegime": latticeRegime,
                "donorPatternPedigree": donorPatternPedigree,
                "tafScoreSummary": tafScoreSummary,
                "tafScore": tafScore,
                "branchNovelty": branchNovelty,
                "maturityCeiling": maturityCeiling,
                "telemetryAuditState": telemetry_audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": bool(rec.get("humanReviewFlag", True)),
                "queuedAt": generated_at,
            }
            telemetry_entries.append(entry)
            lattice_registry_entries.append({**entry, "updatedAt": generated_at})

        if action == "watch":
            watch_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "donationWatchStatus": donation_watch_status,
                    "telemetryFieldStatus": telemetry_field_status,
                    "latticeCoordinates": latticeCoordinates,
                    "latticeRegime": latticeRegime,
                    "donorPatternPedigree": donorPatternPedigree,
                    "tafScoreSummary": tafScoreSummary,
                    "tafScore": tafScore,
                    "branchNovelty": branchNovelty,
                    "maturityCeiling": maturityCeiling,
                    "telemetryAuditState": telemetry_audit_state,
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
                "telemetryFieldStatus": telemetry_field_status,
                "latticeCoordinates": latticeCoordinates,
                "latticeRegime": latticeRegime,
                "donorPatternPedigree": donorPatternPedigree,
                "tafScoreSummary": tafScoreSummary,
                "tafScore": tafScore,
                "branchNovelty": branchNovelty,
                "maturityCeiling": maturityCeiling,
                "telemetryAuditState": telemetry_audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticBranchActivation": True,
                "noAutomaticGraphMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    telemetry_dashboard = {
        "generatedAt": generated_at,
        "telemetryFieldProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(telemetry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    lattice_projection_registry = {
        "generatedAt": generated_at,
        "telemetryFieldProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(lattice_registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    pattern_donation_watchlist = {
        "generatedAt": generated_at,
        "telemetryFieldProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    action_functional_annotations = {
        "generatedAt": generated_at,
        "telemetryFieldProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticBranchActivation": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(telemetry_dashboard, lattice_projection_registry, pattern_donation_watchlist, action_functional_annotations)
    return telemetry_dashboard, lattice_projection_registry, pattern_donation_watchlist, action_functional_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--telemetry-field-audit", type=Path, default=Path("bridge/telemetry_field_audit.json"))
    parser.add_argument("--telemetry-field-recommendations", type=Path, default=Path("bridge/telemetry_field_recommendations.json"))
    parser.add_argument("--telemetry-field-map", type=Path, default=Path("bridge/telemetry_field_map.json"))
    parser.add_argument("--lattice-projection-map", type=Path, default=Path("bridge/lattice_projection_map.json"))
    parser.add_argument("--pattern-donation-registry", type=Path, default=Path("bridge/pattern_donation_registry.json"))
    parser.add_argument("--action-functional-scorecard", type=Path, default=Path("bridge/action_functional_scorecard.json"))
    parser.add_argument("--branch-emergence-report", type=Path, default=Path("bridge/branch_emergence_report.json"))

    parser.add_argument("--symbolic-field-registry", type=Path, default=Path("registry/symbolic_field_registry.json"))
    parser.add_argument("--investigation-dashboard", type=Path, default=Path("registry/investigation_dashboard.json"))
    parser.add_argument("--authority-gate-dashboard", type=Path, default=Path("registry/authority_gate_dashboard.json"))

    parser.add_argument("--out-telemetry-dashboard", type=Path, default=Path("registry/telemetry_dashboard.json"))
    parser.add_argument("--out-lattice-projection-registry", type=Path, default=Path("registry/lattice_projection_registry.json"))
    parser.add_argument("--out-pattern-donation-watchlist", type=Path, default=Path("registry/pattern_donation_watchlist.json"))
    parser.add_argument("--out-action-functional-annotations", type=Path, default=Path("registry/action_functional_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_telemetry_field_overlays(
            load_required_json(args.telemetry_field_audit),
            load_required_json(args.telemetry_field_recommendations),
            load_required_json(args.telemetry_field_map),
            load_required_json(args.lattice_projection_map),
            load_required_json(args.pattern_donation_registry),
            load_required_json(args.action_functional_scorecard),
            load_required_json(args.branch_emergence_report),
            load_required_json(args.symbolic_field_registry),
            load_required_json(args.investigation_dashboard),
            load_required_json(args.authority_gate_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_telemetry_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_lattice_projection_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_pattern_donation_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_action_functional_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_telemetry_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_lattice_projection_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_donation_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_action_functional_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote telemetry dashboard: {args.out_telemetry_dashboard}")
    print(f"[OK] Wrote lattice projection registry: {args.out_lattice_projection_registry}")
    print(f"[OK] Wrote pattern donation watchlist: {args.out_pattern_donation_watchlist}")
    print(f"[OK] Wrote action functional annotations: {args.out_action_functional_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
