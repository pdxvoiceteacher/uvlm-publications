#!/usr/bin/env python3
"""Build evidence-authority and propagation-rights overlays.

Publisher surfaces only Sophia-audited evidence-authority materials as bounded,
review-facing artifacts. This layer does not lift restrictions automatically and
never mutates identities, graph edges, precedents, closures, or canonical truth.
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


def _normalized_action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    if action not in {"docket", "watch", "suppressed", "rejected"}:
        return "watch"
    return action



def _as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    return default


def _normalized_targets(rec: dict[str, Any]) -> list[str]:
    return sorted([target for target in as_list(rec.get("linkedTargetIds")) if isinstance(target, str)])


def _validate_output_contracts(
    authority_gate_dashboard: dict[str, Any],
    weak_evidence_watchlist: dict[str, Any],
    propagation_annotations: dict[str, Any],
    maturity_restriction_registry: dict[str, Any],
) -> None:
    if not isinstance(authority_gate_dashboard.get("entries"), list):
        raise ValueError("authority_gate_dashboard.entries must be a list")
    if not isinstance(weak_evidence_watchlist.get("entries"), list):
        raise ValueError("weak_evidence_watchlist.entries must be a list")
    if not isinstance(propagation_annotations.get("annotations"), list):
        raise ValueError("propagation_annotations.annotations must be a list")
    if not isinstance(maturity_restriction_registry.get("entries"), list):
        raise ValueError("maturity_restriction_registry.entries must be a list")


def build_evidence_authority_overlays(
    evidence_authority_audit: dict[str, Any],
    evidence_authority_recommendations: dict[str, Any],
    evidence_authority_map: dict[str, Any],
    evidence_authority_summary: dict[str, Any],
    propagation_rights_map: dict[str, Any],
    maturity_gate_report: dict[str, Any],
    verification_dashboard: dict[str, Any],
    public_record_dashboard: dict[str, Any],
    symbolic_field_registry: dict[str, Any],
    investigation_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances: dict[str, dict[str, Any]] = {
        "evidence_authority_audit": _extract_required_provenance("evidence_authority_audit", evidence_authority_audit),
        "evidence_authority_recommendations": _extract_required_provenance("evidence_authority_recommendations", evidence_authority_recommendations),
        "evidence_authority_map": _extract_required_provenance("evidence_authority_map", evidence_authority_map),
        "evidence_authority_summary": _extract_required_provenance("evidence_authority_summary", evidence_authority_summary),
        "propagation_rights_map": _extract_required_provenance("propagation_rights_map", propagation_rights_map),
        "maturity_gate_report": _extract_required_provenance("maturity_gate_report", maturity_gate_report),
    }
    for optional_name, artifact in {
        "verification_dashboard": verification_dashboard,
        "public_record_dashboard": public_record_dashboard,
        "symbolic_field_registry": symbolic_field_registry,
        "investigation_dashboard": investigation_dashboard,
    }.items():
        optional = _extract_optional_provenance(optional_name, artifact)
        if optional:
            provenances[optional_name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(evidence_authority_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(evidence_authority_recommendations.get("recommendations")) if isinstance(r, dict)]
    authority_entries = [e for e in as_list(evidence_authority_map.get("entries")) if isinstance(e, dict)]
    authority_summaries = [e for e in as_list(evidence_authority_summary.get("entries")) if isinstance(e, dict)]
    propagation_entries = [e for e in as_list(propagation_rights_map.get("entries")) if isinstance(e, dict)]
    maturity_entries = [e for e in as_list(maturity_gate_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    authority_by_review = _index_by_key(authority_entries, "reviewId")
    summary_by_review = _index_by_key(authority_summaries, "reviewId")
    propagation_by_review = _index_by_key(propagation_entries, "reviewId")
    maturity_by_review = _index_by_key(maturity_entries, "reviewId")

    authority_dashboard_entries: list[dict[str, Any]] = []
    weak_evidence_entries: list[dict[str, Any]] = []
    propagation_annotation_entries: list[dict[str, Any]] = []
    maturity_registry_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _normalized_action(rec)
        authority_map_entry = authority_by_review.get(review_id, {})
        summary_entry = summary_by_review.get(review_id, {})
        propagation_entry = propagation_by_review.get(review_id, {})
        maturity_entry = maturity_by_review.get(review_id, {})
        audit_entry = audit_by_review.get(review_id, {})

        evidence_maturity = str(summary_entry.get("evidenceMaturity", authority_map_entry.get("evidenceMaturity", rec.get("evidenceMaturity", "weak"))))
        claim_type = str(authority_map_entry.get("claimType", rec.get("claimType", "untyped")))
        allowed_authority_class = str(authority_map_entry.get("allowedAuthorityClass", rec.get("allowedAuthorityClass", "restricted")))
        authority_mismatch_flag = _as_bool(summary_entry.get("authorityMismatchFlag", rec.get("authorityMismatchFlag", False)), False)
        propagation_restrictions = sorted([x for x in as_list(propagation_entry.get("propagationRestrictions", rec.get("propagationRestrictions", []))) if isinstance(x, str)])
        maturity_gate_status = str(maturity_entry.get("maturityGateStatus", rec.get("maturityGateStatus", "hold")))
        maturity_gate_reason = str(maturity_entry.get("maturityGateReason", rec.get("maturityGateReason", "insufficient-evidence-maturity")))
        propagation_rights = sorted([x for x in as_list(propagation_entry.get("allowedPropagationRights", rec.get("allowedPropagationRights", []))) if isinstance(x, str)])
        linked_target_ids = _normalized_targets(rec)
        authority_audit_state = str(audit_entry.get("authorityAuditState", rec.get("authorityAuditState", "none")))

        if action == "docket":
            entry = {
                "reviewId": review_id,
                "evidenceMaturity": evidence_maturity,
                "claimType": claim_type,
                "allowedAuthorityClass": allowed_authority_class,
                "authorityMismatchFlag": authority_mismatch_flag,
                "propagationRestrictions": propagation_restrictions,
                "allowedPropagationRights": propagation_rights,
                "maturityGateStatus": maturity_gate_status,
                "maturityGateReason": maturity_gate_reason,
                "authorityAuditState": authority_audit_state,
                "linkedTargetIds": linked_target_ids,
                "humanReviewFlag": _as_bool(rec.get("humanReviewFlag", True), True),
                "queuedAt": generated_at,
            }
            authority_dashboard_entries.append(entry)
            maturity_registry_entries.append(
                {
                    "reviewId": review_id,
                    "evidenceMaturity": evidence_maturity,
                    "claimType": claim_type,
                    "allowedAuthorityClass": allowed_authority_class,
                    "maturityGateStatus": maturity_gate_status,
                    "maturityGateReason": maturity_gate_reason,
                    "authorityMismatchFlag": authority_mismatch_flag,
                    "propagationRestrictions": propagation_restrictions,
                    "allowedPropagationRights": propagation_rights,
                    "linkedTargetIds": linked_target_ids,
                    "updatedAt": generated_at,
                }
            )

        if action == "watch":
            weak_evidence_entries.append(
                {
                    "reviewId": review_id,
                    "status": "watch",
                    "evidenceMaturity": evidence_maturity,
                    "claimType": claim_type,
                    "allowedAuthorityClass": allowed_authority_class,
                    "authorityMismatchFlag": authority_mismatch_flag,
                    "propagationRestrictions": propagation_restrictions,
                    "maturityGateStatus": maturity_gate_status,
                    "maturityGateReason": maturity_gate_reason,
                    "authorityAuditState": authority_audit_state,
                    "linkedTargetIds": linked_target_ids,
                    "humanReviewFlag": _as_bool(rec.get("humanReviewFlag", False), False),
                    "observational": True,
                    "nonCanonical": True,
                    "queuedAt": generated_at,
                }
            )

        propagation_annotation_entries.append(
            {
                "reviewId": review_id,
                "targetPublisherAction": action,
                "evidenceMaturity": evidence_maturity,
                "claimType": claim_type,
                "allowedAuthorityClass": allowed_authority_class,
                "authorityMismatchFlag": authority_mismatch_flag,
                "propagationRestrictions": propagation_restrictions,
                "allowedPropagationRights": propagation_rights,
                "maturityGateStatus": maturity_gate_status,
                "maturityGateReason": maturity_gate_reason,
                "authorityAuditState": authority_audit_state,
                "linkedTargetIds": linked_target_ids,
                "noAutomaticRestrictionLifting": True,
                "noAutomaticGraphHardening": True,
                "noAutomaticIdentityMutation": True,
                "noCanonicalMutation": True,
                "notes": rec.get("notes", ""),
            }
        )

    authority_gate_dashboard = {
        "generatedAt": generated_at,
        "evidenceAuthorityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(authority_dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    weak_evidence_watchlist = {
        "generatedAt": generated_at,
        "evidenceAuthorityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(weak_evidence_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    propagation_annotations = {
        "generatedAt": generated_at,
        "evidenceAuthorityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticRestrictionLifting": True,
        "noAutomaticGraphHardening": True,
        "noAutomaticIdentityMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(propagation_annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    maturity_restriction_registry = {
        "generatedAt": generated_at,
        "evidenceAuthorityProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(maturity_registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_output_contracts(
        authority_gate_dashboard,
        weak_evidence_watchlist,
        propagation_annotations,
        maturity_restriction_registry,
    )

    return authority_gate_dashboard, weak_evidence_watchlist, propagation_annotations, maturity_restriction_registry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-authority-audit", type=Path, default=Path("bridge/evidence_authority_audit.json"))
    parser.add_argument("--evidence-authority-recommendations", type=Path, default=Path("bridge/evidence_authority_recommendations.json"))
    parser.add_argument("--evidence-authority-map", type=Path, default=Path("bridge/evidence_authority_map.json"))
    parser.add_argument("--evidence-authority-summary", type=Path, default=Path("bridge/evidence_authority_summary.json"))
    parser.add_argument("--propagation-rights-map", type=Path, default=Path("bridge/propagation_rights_map.json"))
    parser.add_argument("--maturity-gate-report", type=Path, default=Path("bridge/maturity_gate_report.json"))
    parser.add_argument("--evidence-authority-snapshot", type=Path, default=None, help=argparse.SUPPRESS)

    parser.add_argument("--verification-dashboard", type=Path, default=Path("registry/verification_dashboard.json"))
    parser.add_argument("--public-record-dashboard", type=Path, default=Path("registry/public_record_dashboard.json"))
    parser.add_argument("--symbolic-field-registry", type=Path, default=Path("registry/symbolic_field_registry.json"))
    parser.add_argument("--investigation-dashboard", type=Path, default=Path("registry/investigation_dashboard.json"))

    parser.add_argument("--out-authority-gate-dashboard", type=Path, default=Path("registry/authority_gate_dashboard.json"))
    parser.add_argument("--out-weak-evidence-watchlist", type=Path, default=Path("registry/weak_evidence_watchlist.json"))
    parser.add_argument("--out-propagation-annotations", type=Path, default=Path("registry/propagation_annotations.json"))
    parser.add_argument("--out-maturity-restriction-registry", type=Path, default=Path("registry/maturity_restriction_registry.json"))

    args = parser.parse_args()

    if args.evidence_authority_snapshot is not None:
        print("[ERROR] Deprecated artifact alias detected: --evidence-authority-snapshot is no longer supported. Use canonical evidence-authority artifacts.")
        return 2

    try:
        outputs = build_evidence_authority_overlays(
            load_required_json(args.evidence_authority_audit),
            load_required_json(args.evidence_authority_recommendations),
            load_required_json(args.evidence_authority_map),
            load_required_json(args.evidence_authority_summary),
            load_required_json(args.propagation_rights_map),
            load_required_json(args.maturity_gate_report),
            load_required_json(args.verification_dashboard),
            load_required_json(args.public_record_dashboard),
            load_required_json(args.symbolic_field_registry),
            load_required_json(args.investigation_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_authority_gate_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_weak_evidence_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_propagation_annotations.parent.mkdir(parents=True, exist_ok=True)
    args.out_maturity_restriction_registry.parent.mkdir(parents=True, exist_ok=True)

    args.out_authority_gate_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_weak_evidence_watchlist.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_propagation_annotations.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_maturity_restriction_registry.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote authority gate dashboard: {args.out_authority_gate_dashboard}")
    print(f"[OK] Wrote weak evidence watchlist: {args.out_weak_evidence_watchlist}")
    print(f"[OK] Wrote propagation annotations: {args.out_propagation_annotations}")
    print(f"[OK] Wrote maturity restriction registry: {args.out_maturity_restriction_registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
