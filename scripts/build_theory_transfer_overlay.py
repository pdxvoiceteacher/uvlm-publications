#!/usr/bin/env python3
"""Build cross-domain theory transfer and donation-governance overlays.

Publisher surfaces only Sophia-audited theory-transfer materials; no automatic
cross-domain theory certification or canonical mutation occurs from this layer.
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


def _validate_outputs(transfer_dashboard: dict[str, Any], theory_transfer_registry: dict[str, Any], transfer_watchlist: dict[str, Any], transfer_annotations: dict[str, Any]) -> None:
    if not isinstance(transfer_dashboard.get("entries"), list):
        raise ValueError("transfer_dashboard.entries must be a list")
    if not isinstance(theory_transfer_registry.get("entries"), list):
        raise ValueError("theory_transfer_registry.entries must be a list")
    if not isinstance(transfer_watchlist.get("entries"), list):
        raise ValueError("transfer_watchlist.entries must be a list")
    if not isinstance(transfer_annotations.get("annotations"), list):
        raise ValueError("transfer_annotations.annotations must be a list")
    for payload in (transfer_dashboard, theory_transfer_registry, transfer_watchlist, transfer_annotations):
        json.dumps(payload)


def build_theory_transfer_overlays(
    theory_transfer_audit: dict[str, Any],
    theory_transfer_recommendations: dict[str, Any],
    theory_transfer_map: dict[str, Any],
    donor_target_asymmetry_report: dict[str, Any],
    transfer_replication_gate: dict[str, Any],
    transfer_risk_register: dict[str, Any],
    theory_dashboard: dict[str, Any],
    experiment_dashboard: dict[str, Any],
    agency_mode_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "theory_transfer_audit": _extract_required_provenance("theory_transfer_audit", theory_transfer_audit),
        "theory_transfer_recommendations": _extract_required_provenance("theory_transfer_recommendations", theory_transfer_recommendations),
        "theory_transfer_map": _extract_required_provenance("theory_transfer_map", theory_transfer_map),
        "donor_target_asymmetry_report": _extract_required_provenance("donor_target_asymmetry_report", donor_target_asymmetry_report),
        "transfer_replication_gate": _extract_required_provenance("transfer_replication_gate", transfer_replication_gate),
        "transfer_risk_register": _extract_required_provenance("transfer_risk_register", transfer_risk_register),
    }
    for name, artifact in {
        "theory_dashboard": theory_dashboard,
        "experiment_dashboard": experiment_dashboard,
        "agency_mode_dashboard": agency_mode_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(theory_transfer_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(theory_transfer_recommendations.get("recommendations")) if isinstance(e, dict)]
    transfers = [e for e in as_list(theory_transfer_map.get("entries")) if isinstance(e, dict)]
    asymmetry = [e for e in as_list(donor_target_asymmetry_report.get("entries")) if isinstance(e, dict)]
    replication = [e for e in as_list(transfer_replication_gate.get("entries")) if isinstance(e, dict)]
    risks = [e for e in as_list(transfer_risk_register.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    transfer_by_review = _index_by_key(transfers, "reviewId")
    asymmetry_by_review = _index_by_key(asymmetry, "reviewId")
    replication_by_review = _index_by_key(replication, "reviewId")
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
        t = transfer_by_review.get(review_id, {})
        a = asymmetry_by_review.get(review_id, {})
        g = replication_by_review.get(review_id, {})
        r = risk_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        transfer_status = str(t.get("transferStatus", rec.get("transferStatus", "under-review")))
        donor_target_asymmetry = str(a.get("donorTargetAsymmetry", rec.get("donorTargetAsymmetry", "unknown")))
        replication_gate_state = str(g.get("replicationGateState", rec.get("replicationGateState", "hold")))
        prohibited_claims = sorted([x for x in as_list(g.get("prohibitedClaims", rec.get("prohibitedClaims", []))) if isinstance(x, str)])
        risk_register_summary = str(r.get("riskRegisterSummary", rec.get("riskRegisterSummary", "bounded")))
        theory_transfer_audit_state = str(audit.get("theoryTransferAuditState", rec.get("theoryTransferAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "transferStatus": transfer_status,
            "donorTargetAsymmetry": donor_target_asymmetry,
            "replicationGateState": replication_gate_state,
            "prohibitedClaims": prohibited_claims,
            "riskRegisterSummary": risk_register_summary,
            "theoryTransferAuditState": theory_transfer_audit_state,
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
            "noAutomaticCrossDomainCertification": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    transfer_dashboard = {
        "generatedAt": generated_at,
        "theoryTransferProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    theory_transfer_registry = {
        "generatedAt": generated_at,
        "theoryTransferProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    transfer_watchlist = {
        "generatedAt": generated_at,
        "theoryTransferProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    transfer_annotations = {
        "generatedAt": generated_at,
        "theoryTransferProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticCrossDomainCertification": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(transfer_dashboard, theory_transfer_registry, transfer_watchlist, transfer_annotations)
    return transfer_dashboard, theory_transfer_registry, transfer_watchlist, transfer_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theory-transfer-audit", type=Path, default=Path("bridge/theory_transfer_audit.json"))
    parser.add_argument("--theory-transfer-recommendations", type=Path, default=Path("bridge/theory_transfer_recommendations.json"))
    parser.add_argument("--theory-transfer-map", type=Path, default=Path("bridge/theory_transfer_map.json"))
    parser.add_argument("--donor-target-asymmetry-report", type=Path, default=Path("bridge/donor_target_asymmetry_report.json"))
    parser.add_argument("--transfer-replication-gate", type=Path, default=Path("bridge/transfer_replication_gate.json"))
    parser.add_argument("--transfer-risk-register", type=Path, default=Path("bridge/transfer_risk_register.json"))

    parser.add_argument("--theory-dashboard", type=Path, default=Path("registry/theory_dashboard.json"))
    parser.add_argument("--experiment-dashboard", type=Path, default=Path("registry/experiment_dashboard.json"))
    parser.add_argument("--agency-mode-dashboard", type=Path, default=Path("registry/agency_mode_dashboard.json"))

    parser.add_argument("--out-transfer-dashboard", type=Path, default=Path("registry/transfer_dashboard.json"))
    parser.add_argument("--out-theory-transfer-registry", type=Path, default=Path("registry/theory_transfer_registry.json"))
    parser.add_argument("--out-transfer-watchlist", type=Path, default=Path("registry/transfer_watchlist.json"))
    parser.add_argument("--out-transfer-annotations", type=Path, default=Path("registry/transfer_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_theory_transfer_overlays(
            load_required_json(args.theory_transfer_audit),
            load_required_json(args.theory_transfer_recommendations),
            load_required_json(args.theory_transfer_map),
            load_required_json(args.donor_target_asymmetry_report),
            load_required_json(args.transfer_replication_gate),
            load_required_json(args.transfer_risk_register),
            load_required_json(args.theory_dashboard),
            load_required_json(args.experiment_dashboard),
            load_required_json(args.agency_mode_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_transfer_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_theory_transfer_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_transfer_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_transfer_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_transfer_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_theory_transfer_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_transfer_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_transfer_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote transfer dashboard: {args.out_transfer_dashboard}")
    print(f"[OK] Wrote theory transfer registry: {args.out_theory_transfer_registry}")
    print(f"[OK] Wrote transfer watchlist: {args.out_transfer_watchlist}")
    print(f"[OK] Wrote transfer annotations: {args.out_transfer_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
