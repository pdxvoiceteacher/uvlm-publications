#!/usr/bin/env python3
"""Build emergent-domain and field-birth overlays.

Publisher surfaces only Sophia-audited emergent-domain materials; no automatic
canon formation, ranking of disciplines, or field sovereignty claims occur from
this layer.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from canonical_integrity_manifest import evaluate_manifest_pair, load_manifest

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


def _validate_outputs(
    emergent_domain_dashboard: dict[str, Any],
    domain_birth_registry: dict[str, Any],
    domain_boundary_watchlist: dict[str, Any],
    emergent_domain_annotations: dict[str, Any],
) -> None:
    if not isinstance(emergent_domain_dashboard.get("entries"), list):
        raise ValueError("emergent_domain_dashboard.entries must be a list")
    if not isinstance(domain_birth_registry.get("entries"), list):
        raise ValueError("domain_birth_registry.entries must be a list")
    if not isinstance(domain_boundary_watchlist.get("entries"), list):
        raise ValueError("domain_boundary_watchlist.entries must be a list")
    if not isinstance(emergent_domain_annotations.get("annotations"), list):
        raise ValueError("emergent_domain_annotations.annotations must be a list")

    for payload in (emergent_domain_dashboard, domain_birth_registry, domain_boundary_watchlist, emergent_domain_annotations):
        for key in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(key), bool):
                raise ValueError(f"{key} must be a boolean")
        json.dumps(payload)


def build_emergent_domain_overlays(
    emergent_domain_audit: dict[str, Any],
    emergent_domain_recommendations: dict[str, Any],
    emergent_domain_map: dict[str, Any],
    cross_domain_invariant_report: dict[str, Any],
    field_birth_pressure_report: dict[str, Any],
    domain_boundary_failure_map: dict[str, Any],
    transfer_dashboard: dict[str, Any],
    value_dashboard: dict[str, Any],
    uncertainty_dashboard: dict[str, Any],
    social_entropy_dashboard: dict[str, Any],
    civic_literacy_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "emergent_domain_audit": _extract_required_provenance("emergent_domain_audit", emergent_domain_audit),
        "emergent_domain_recommendations": _extract_required_provenance("emergent_domain_recommendations", emergent_domain_recommendations),
        "emergent_domain_map": _extract_required_provenance("emergent_domain_map", emergent_domain_map),
        "cross_domain_invariant_report": _extract_required_provenance("cross_domain_invariant_report", cross_domain_invariant_report),
        "field_birth_pressure_report": _extract_required_provenance("field_birth_pressure_report", field_birth_pressure_report),
        "domain_boundary_failure_map": _extract_required_provenance("domain_boundary_failure_map", domain_boundary_failure_map),
    }
    for name, artifact in {
        "transfer_dashboard": transfer_dashboard,
        "value_dashboard": value_dashboard,
        "uncertainty_dashboard": uncertainty_dashboard,
        "social_entropy_dashboard": social_entropy_dashboard,
        "civic_literacy_dashboard": civic_literacy_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)
    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [e for e in as_list(emergent_domain_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(emergent_domain_recommendations.get("recommendations")) if isinstance(e, dict)]
    domain_entries = [e for e in as_list(emergent_domain_map.get("entries")) if isinstance(e, dict)]
    invariant_entries = [e for e in as_list(cross_domain_invariant_report.get("entries")) if isinstance(e, dict)]
    pressure_entries = [e for e in as_list(field_birth_pressure_report.get("entries")) if isinstance(e, dict)]
    boundary_entries = [e for e in as_list(domain_boundary_failure_map.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    domain_by_review = _index_by_key(domain_entries, "reviewId")
    invariant_by_review = _index_by_key(invariant_entries, "reviewId")
    pressure_by_review = _index_by_key(pressure_entries, "reviewId")
    boundary_by_review = _index_by_key(boundary_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        domain = domain_by_review.get(review_id, {})
        invariant = invariant_by_review.get(review_id, {})
        pressure = pressure_by_review.get(review_id, {})
        boundary = boundary_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        domain_status = str(domain.get("domainStatus", rec.get("domainStatus", "monitor")))
        source_domains = sorted([x for x in as_list(domain.get("sourceDomains", rec.get("sourceDomains", []))) if isinstance(x, str)])
        invariant_pattern_class = str(invariant.get("invariantPatternClass", rec.get("invariantPatternClass", "unclassified")))
        field_birth_pressure = str(pressure.get("fieldBirthPressure", rec.get("fieldBirthPressure", "bounded")))
        field_birth_pressure_score = _to_float(pressure.get("fieldBirthPressureScore", rec.get("fieldBirthPressureScore", 0.0)))
        domain_boundary_failure = str(boundary.get("domainBoundaryFailure", rec.get("domainBoundaryFailure", "bounded")))
        commons_legibility_requirement = str(rec.get("commonsLegibilityRequirement", "required"))
        audit_state = str(audit.get("emergentDomainAuditState", rec.get("emergentDomainAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "domainStatus": domain_status,
            "sourceDomains": source_domains,
            "invariantPatternClass": invariant_pattern_class,
            "fieldBirthPressure": field_birth_pressure,
            "fieldBirthPressureScore": field_birth_pressure_score,
            "domainBoundaryFailure": domain_boundary_failure,
            "commonsLegibilityRequirement": commons_legibility_requirement,
            "emergentDomainAuditState": audit_state,
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
            "noAutomaticCanonFormation": True,
            "noDisciplineRanking": True,
            "noFieldSovereigntyClaims": True,
            "noTheoryStatusMutation": True,
            "noIdentityMutation": True,
            "noGovernanceRightsMutation": True,
            "noAutomaticGraphMutation": True,
            "noScientificCanonMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    emergent_domain_dashboard = {
        "generatedAt": generated_at,
        "emergentDomainProtocol": True,
        "nonCanonical": True,
        "noAutomaticCanonFormation": True,
        "noDisciplineRanking": True,
        "noFieldSovereigntyClaims": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    domain_birth_registry = {
        "generatedAt": generated_at,
        "emergentDomainProtocol": True,
        "nonCanonical": True,
        "noAutomaticCanonFormation": True,
        "noDisciplineRanking": True,
        "noFieldSovereigntyClaims": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    domain_boundary_watchlist = {
        "generatedAt": generated_at,
        "emergentDomainProtocol": True,
        "nonCanonical": True,
        "noAutomaticCanonFormation": True,
        "noDisciplineRanking": True,
        "noFieldSovereigntyClaims": True,
        "provenance": provenance_summary,
        **integrity_status,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    emergent_domain_annotations = {
        "generatedAt": generated_at,
        "emergentDomainProtocol": True,
        "nonCanonical": True,
        "noAutomaticCanonFormation": True,
        "noDisciplineRanking": True,
        "noFieldSovereigntyClaims": True,
        "noTheoryStatusMutation": True,
        "noIdentityMutation": True,
        "noGovernanceRightsMutation": True,
        "noAutomaticGraphMutation": True,
        "noScientificCanonMutation": True,
        "noCanonicalMutation": True,
        "provenance": provenance_summary,
        **integrity_status,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(emergent_domain_dashboard, domain_birth_registry, domain_boundary_watchlist, emergent_domain_annotations)
    return emergent_domain_dashboard, domain_birth_registry, domain_boundary_watchlist, emergent_domain_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emergent-domain-audit", type=Path, default=Path("bridge/emergent_domain_audit.json"))
    parser.add_argument("--emergent-domain-recommendations", type=Path, default=Path("bridge/emergent_domain_recommendations.json"))
    parser.add_argument("--emergent-domain-map", type=Path, default=Path("bridge/emergent_domain_map.json"))
    parser.add_argument("--cross-domain-invariant-report", type=Path, default=Path("bridge/cross_domain_invariant_report.json"))
    parser.add_argument("--field-birth-pressure-report", type=Path, default=Path("bridge/field_birth_pressure_report.json"))
    parser.add_argument("--domain-boundary-failure-map", type=Path, default=Path("bridge/domain_boundary_failure_map.json"))

    parser.add_argument("--transfer-dashboard", type=Path, default=Path("registry/transfer_dashboard.json"))
    parser.add_argument("--value-dashboard", type=Path, default=Path("registry/value_dashboard.json"))
    parser.add_argument("--uncertainty-dashboard", type=Path, default=Path("registry/uncertainty_dashboard.json"))
    parser.add_argument("--social-entropy-dashboard", type=Path, default=Path("registry/social_entropy_dashboard.json"))
    parser.add_argument("--civic-literacy-dashboard", type=Path, default=Path("registry/civic_literacy_dashboard.json"))
    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-emergent-domain-dashboard", type=Path, default=Path("registry/emergent_domain_dashboard.json"))
    parser.add_argument("--out-domain-birth-registry", type=Path, default=Path("registry/domain_birth_registry.json"))
    parser.add_argument("--out-domain-boundary-watchlist", type=Path, default=Path("registry/domain_boundary_watchlist.json"))
    parser.add_argument("--out-emergent-domain-annotations", type=Path, default=Path("registry/emergent_domain_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_emergent_domain_overlays(
            load_required_json(args.emergent_domain_audit),
            load_required_json(args.emergent_domain_recommendations),
            load_required_json(args.emergent_domain_map),
            load_required_json(args.cross_domain_invariant_report),
            load_required_json(args.field_birth_pressure_report),
            load_required_json(args.domain_boundary_failure_map),
            load_required_json(args.transfer_dashboard),
            load_required_json(args.value_dashboard),
            load_required_json(args.uncertainty_dashboard),
            load_required_json(args.social_entropy_dashboard),
            load_required_json(args.civic_literacy_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_emergent_domain_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_domain_birth_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_domain_boundary_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_emergent_domain_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_emergent_domain_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_domain_birth_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_domain_boundary_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_emergent_domain_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote emergent domain dashboard: {args.out_emergent_domain_dashboard}")
    print(f"[OK] Wrote domain birth registry: {args.out_domain_birth_registry}")
    print(f"[OK] Wrote domain boundary watchlist: {args.out_domain_boundary_watchlist}")
    print(f"[OK] Wrote emergent domain annotations: {args.out_emergent_domain_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
