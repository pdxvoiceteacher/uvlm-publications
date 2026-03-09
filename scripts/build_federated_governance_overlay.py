#!/usr/bin/env python3
"""Build federated stewardship and commons governance overlays.

Publisher surfaces only Sophia-audited federated-governance materials; no
automatic centralization, ranking of communities, or sovereignty claims occur
from this layer.
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


def _validate_outputs(federation_dashboard: dict[str, Any], stewardship_registry: dict[str, Any], capture_watchlist: dict[str, Any], federation_annotations: dict[str, Any]) -> None:
    if not isinstance(federation_dashboard.get("entries"), list):
        raise ValueError("federation_dashboard.entries must be a list")
    if not isinstance(stewardship_registry.get("entries"), list):
        raise ValueError("stewardship_registry.entries must be a list")
    if not isinstance(capture_watchlist.get("entries"), list):
        raise ValueError("capture_watchlist.entries must be a list")
    if not isinstance(federation_annotations.get("annotations"), list):
        raise ValueError("federation_annotations.annotations must be a list")
    for payload in (federation_dashboard, stewardship_registry, capture_watchlist, federation_annotations):
        json.dumps(payload)


def build_federated_governance_overlays(
    federated_governance_audit: dict[str, Any],
    federated_governance_recommendations: dict[str, Any],
    stewardship_node_map: dict[str, Any],
    federation_coherence_report: dict[str, Any],
    cross_node_dissent_map: dict[str, Any],
    commons_capture_risk_report: dict[str, Any],
    social_entropy_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    architecture_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "federated_governance_audit": _extract_required_provenance("federated_governance_audit", federated_governance_audit),
        "federated_governance_recommendations": _extract_required_provenance("federated_governance_recommendations", federated_governance_recommendations),
        "stewardship_node_map": _extract_required_provenance("stewardship_node_map", stewardship_node_map),
        "federation_coherence_report": _extract_required_provenance("federation_coherence_report", federation_coherence_report),
        "cross_node_dissent_map": _extract_required_provenance("cross_node_dissent_map", cross_node_dissent_map),
        "commons_capture_risk_report": _extract_required_provenance("commons_capture_risk_report", commons_capture_risk_report),
    }
    for name, artifact in {
        "social_entropy_dashboard": social_entropy_dashboard,
        "value_dashboard": value_dashboard,
        "architecture_dashboard": architecture_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(federated_governance_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(federated_governance_recommendations.get("recommendations")) if isinstance(e, dict)]
    node_entries = [e for e in as_list(stewardship_node_map.get("entries")) if isinstance(e, dict)]
    coherence_entries = [e for e in as_list(federation_coherence_report.get("entries")) if isinstance(e, dict)]
    dissent_entries = [e for e in as_list(cross_node_dissent_map.get("entries")) if isinstance(e, dict)]
    capture_entries = [e for e in as_list(commons_capture_risk_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    node_by_review = _index_by_key(node_entries, "reviewId")
    coherence_by_review = _index_by_key(coherence_entries, "reviewId")
    dissent_by_review = _index_by_key(dissent_entries, "reviewId")
    capture_by_review = _index_by_key(capture_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        node = node_by_review.get(review_id, {})
        coherence = coherence_by_review.get(review_id, {})
        dissent = dissent_by_review.get(review_id, {})
        capture = capture_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        federation_status = str(coherence.get("federationStatus", rec.get("federationStatus", "monitor")))
        node_class = str(node.get("nodeClass", rec.get("nodeClass", "bounded")))
        dissent_portability = str(dissent.get("dissentPortability", rec.get("dissentPortability", "bounded")))
        capture_risk = str(capture.get("captureRisk", rec.get("captureRisk", "bounded")))
        legitimacy_signal = str(capture.get("legitimacySignal", rec.get("legitimacySignal", "stable")))
        mitigation_requirement = str(rec.get("mitigationRequirement", "monitor"))
        capture_risk_score = _to_float(capture.get("captureRiskScore", rec.get("captureRiskScore", 0.0)))
        audit_state = str(audit.get("federatedGovernanceAuditState", rec.get("federatedGovernanceAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "federationStatus": federation_status,
            "nodeClass": node_class,
            "dissentPortability": dissent_portability,
            "captureRisk": capture_risk,
            "legitimacySignal": legitimacy_signal,
            "mitigationRequirement": mitigation_requirement,
            "captureRiskScore": capture_risk_score,
            "federatedGovernanceAuditState": audit_state,
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
            "noAutomaticCentralization": True,
            "noCommunityRanking": True,
            "noSovereigntyClaims": True,
            "noTheoryStatusMutation": True,
            "noIdentityMutation": True,
            "noGovernanceRightsMutation": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    federation_dashboard = {
        "generatedAt": generated_at,
        "federatedGovernanceProtocol": True,
        "nonCanonical": True,
        "noAutomaticCentralization": True,
        "noCommunityRanking": True,
        "noSovereigntyClaims": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    stewardship_registry = {
        "generatedAt": generated_at,
        "federatedGovernanceProtocol": True,
        "nonCanonical": True,
        "noAutomaticCentralization": True,
        "noCommunityRanking": True,
        "noSovereigntyClaims": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    capture_watchlist = {
        "generatedAt": generated_at,
        "federatedGovernanceProtocol": True,
        "nonCanonical": True,
        "noAutomaticCentralization": True,
        "noCommunityRanking": True,
        "noSovereigntyClaims": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    federation_annotations = {
        "generatedAt": generated_at,
        "federatedGovernanceProtocol": True,
        "nonCanonical": True,
        "noAutomaticCentralization": True,
        "noCommunityRanking": True,
        "noSovereigntyClaims": True,
        "noTheoryStatusMutation": True,
        "noIdentityMutation": True,
        "noGovernanceRightsMutation": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(federation_dashboard, stewardship_registry, capture_watchlist, federation_annotations)
    return federation_dashboard, stewardship_registry, capture_watchlist, federation_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--federated-governance-audit", type=Path, default=Path("bridge/federated_governance_audit.json"))
    parser.add_argument("--federated-governance-recommendations", type=Path, default=Path("bridge/federated_governance_recommendations.json"))
    parser.add_argument("--stewardship-node-map", type=Path, default=Path("bridge/stewardship_node_map.json"))
    parser.add_argument("--federation-coherence-report", type=Path, default=Path("bridge/federation_coherence_report.json"))
    parser.add_argument("--cross-node-dissent-map", type=Path, default=Path("bridge/cross_node_dissent_map.json"))
    parser.add_argument("--commons-capture-risk-report", type=Path, default=Path("bridge/commons_capture_risk_report.json"))

    parser.add_argument("--social-entropy-dashboard", type=Path, default=Path("registry/social_entropy_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))
    parser.add_argument("--architecture-dashboard", type=Path, default=Path("registry/architecture_dashboard.json"))

    parser.add_argument("--out-federation-dashboard", type=Path, default=Path("registry/federation_dashboard.json"))
    parser.add_argument("--out-stewardship-registry", type=Path, default=Path("registry/stewardship_registry.json"))
    parser.add_argument("--out-capture-watchlist", type=Path, default=Path("registry/capture_watchlist.json"))
    parser.add_argument("--out-federation-annotations", type=Path, default=Path("registry/federation_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_federated_governance_overlays(
            load_required_json(args.federated_governance_audit),
            load_required_json(args.federated_governance_recommendations),
            load_required_json(args.stewardship_node_map),
            load_required_json(args.federation_coherence_report),
            load_required_json(args.cross_node_dissent_map),
            load_required_json(args.commons_capture_risk_report),
            load_required_json(args.social_entropy_dashboard),
            load_required_json(args.value_dashboard),
            load_required_json(args.architecture_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_federation_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_stewardship_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_capture_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_federation_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_federation_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_stewardship_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_capture_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_federation_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote federation dashboard: {args.out_federation_dashboard}")
    print(f"[OK] Wrote stewardship registry: {args.out_stewardship_registry}")
    print(f"[OK] Wrote capture watchlist: {args.out_capture_watchlist}")
    print(f"[OK] Wrote federation annotations: {args.out_federation_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
