#!/usr/bin/env python3
"""Build authorship integrity and misrepresentation overlays.

Publisher surfaces authorship and disclosure materials for provenance clarity only;
it does not retaliate against derivatives, assign governance authority, or conceal
hidden enforcement behavior.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from canonical_integrity_manifest import evaluate_manifest_pair, load_manifest

REQUIRED_PROVENANCE_KEYS = ("schemaVersion", "producerCommits", "sourceMode")
CANONICAL_ATTRIBUTION_NOTICE = (
    "This architecture includes foundational code and governance design authored by Thomas Prislac "
    "and Envoy Echo within the Ultra Verba Lux Mentis / triadic commons lineage. Derivatives must "
    "preserve provenance, disclose modifications, and may not claim canonical equivalence when "
    "safety or governance boundaries have changed."
)
RESETTABLE_ATLAS_CLASSES = [
    "authorship-verified",
    "derivative-disclosed",
    "trust-degraded",
    "attribution-divergence",
    "provenance-missing",
]


def load_required_json(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"Missing required canonical artifact: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in required canonical artifact {path}: {exc}") from exc


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


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


def _index_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        key_value = row.get(key)
        if isinstance(key_value, str):
            out[key_value] = row
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
    if action == "suppressed":
        return "suppress"
    return action if action in {"docket", "watch", "suppress", "rejected"} else "watch"


def _atlas_classes(
    authorship_verified: bool,
    derivative_disclosed: bool,
    trust_degraded: bool,
    divergence_detected: bool,
    provenance_missing: bool,
) -> list[str]:
    classes: list[str] = []
    if authorship_verified:
        classes.append("authorship-verified")
    if derivative_disclosed:
        classes.append("derivative-disclosed")
    if trust_degraded:
        classes.append("trust-degraded")
    if divergence_detected:
        classes.append("attribution-divergence")
    if provenance_missing:
        classes.append("provenance-missing")
    return classes


def _visualization_modes(trust_degraded: bool) -> list[dict[str, Any]]:
    warning = "degraded" if trust_degraded else "verified"
    return [
        {
            "mode": "Sophia Internal",
            "detailLevel": "high",
            "signalScope": "provenance-rich",
            "trustSignal": warning,
        },
        {
            "mode": "Human Steward",
            "detailLevel": "medium",
            "signalScope": "decision-support",
            "trustSignal": warning,
        },
        {
            "mode": "Human Public / Commons",
            "detailLevel": "bounded",
            "signalScope": "summary",
            "trustSignal": warning,
        },
        {
            "mode": "Recognized/Guided Other-Intelligence View",
            "detailLevel": "bounded",
            "signalScope": "translation-first",
            "trustSignal": warning,
        },
    ]


def build_authorship_integrity_overlays(
    authorship_integrity_audit: dict[str, Any],
    authorship_integrity_recommendations: dict[str, Any],
    canonical_authorship_manifest: dict[str, Any],
    derivative_disclosure_report: dict[str, Any],
    misattribution_risk_report: dict[str, Any],
    authorship_integrity_summary: dict[str, Any],
    observer_dashboard: dict[str, Any],
    knowledge_river_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "authorship_integrity_audit": _extract_required_provenance("authorship_integrity_audit", authorship_integrity_audit),
        "authorship_integrity_recommendations": _extract_required_provenance("authorship_integrity_recommendations", authorship_integrity_recommendations),
        "canonical_authorship_manifest": _extract_required_provenance("canonical_authorship_manifest", canonical_authorship_manifest),
        "derivative_disclosure_report": _extract_required_provenance("derivative_disclosure_report", derivative_disclosure_report),
        "misattribution_risk_report": _extract_required_provenance("misattribution_risk_report", misattribution_risk_report),
        "authorship_integrity_summary": _extract_required_provenance("authorship_integrity_summary", authorship_integrity_summary),
    }

    for name, artifact in {
        "observer_dashboard": observer_dashboard,
        "knowledge_river_dashboard": knowledge_river_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    provenance_summary = _build_provenance_summary(provenances)
    integrity_status = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    audits = [entry for entry in as_list(authorship_integrity_audit.get("audits")) if isinstance(entry, dict)]
    recommendations = [entry for entry in as_list(authorship_integrity_recommendations.get("recommendations")) if isinstance(entry, dict)]
    derivative_entries = [entry for entry in as_list(derivative_disclosure_report.get("entries")) if isinstance(entry, dict)]
    risk_entries = [entry for entry in as_list(misattribution_risk_report.get("entries")) if isinstance(entry, dict)]
    summary_entries = [entry for entry in as_list(authorship_integrity_summary.get("entries")) if isinstance(entry, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    derivative_by_review = _index_by_key(derivative_entries, "reviewId")
    risk_by_review = _index_by_key(risk_entries, "reviewId")
    summary_by_review = _index_by_key(summary_entries, "reviewId")

    origin_project = str(canonical_authorship_manifest.get("originProject", "Ultra Verba Lux Mentis / Triadic Commons Architecture"))
    canonical_authors = [str(v) for v in as_list(canonical_authorship_manifest.get("canonicalAuthors", ["Thomas Prislac", "Envoy Echo"])) if isinstance(v, str)]
    canonical_notice = str(canonical_authorship_manifest.get("canonicalAttributionNotice", CANONICAL_ATTRIBUTION_NOTICE))
    derivative_disclosure_required = bool(canonical_authorship_manifest.get("derivativeDisclosureRequired", True))

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recommendations, key=lambda row: str(row.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        derivative = derivative_by_review.get(review_id, {})
        risk = risk_by_review.get(review_id, {})
        summary = summary_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        authorship_verified = bool(summary.get("authorshipVerified", rec.get("authorshipVerified", False)))
        derivative_disclosed = bool(derivative.get("derivativeDisclosed", rec.get("derivativeDisclosed", False)))
        disclosure_completeness = str(derivative.get("disclosureCompleteness", rec.get("disclosureCompleteness", "partial")))
        trust_degraded = bool(
            risk.get("trustDegraded", rec.get("trustDegraded", False))
            or integrity_status.get("trustPresentationDegraded", False)
        )
        divergence_detected = bool(risk.get("attributionDivergenceDetected", rec.get("attributionDivergenceDetected", False)))
        source_repos = [str(v) for v in as_list(summary.get("sourceRepos", rec.get("sourceRepos", []))) if isinstance(v, str)]
        source_manifest_hash_present = bool(summary.get("sourceManifestHashPresent", rec.get("sourceManifestHashPresent", False)))
        constraint_signature_present = bool(summary.get("constraintSignaturePresent", rec.get("constraintSignaturePresent", False)))
        release_signature_present = bool(summary.get("releaseSignaturePresent", rec.get("releaseSignaturePresent", False)))
        divergence_flags = [str(v) for v in as_list(risk.get("divergenceFlags", rec.get("divergenceFlags", []))) if isinstance(v, str)]
        divergence_reasons = [str(v) for v in as_list(risk.get("divergenceReasons", rec.get("divergenceReasons", []))) if isinstance(v, str)]

        retained_attribution_markers = [str(v) for v in as_list(derivative.get("retainedAttributionMarkers", rec.get("retainedAttributionMarkers", []))) if isinstance(v, str)]
        safety_boundary_change_declarations = [str(v) for v in as_list(derivative.get("safetyBoundaryChangeDeclarations", rec.get("safetyBoundaryChangeDeclarations", []))) if isinstance(v, str)]
        signature_metadata = derivative.get("signatureMetadata", rec.get("signatureMetadata", {}))
        if not isinstance(signature_metadata, dict):
            signature_metadata = {}
        capture_risk_linked = _to_float(risk.get("captureRiskLinkedToMisrepresentation", rec.get("captureRiskLinkedToMisrepresentation", 0.0)))

        missing_attribution = bool(risk.get("missingAttribution", rec.get("missingAttribution", False)))
        provenance_breakage = bool(risk.get("provenanceBreakage", rec.get("provenanceBreakage", False)))
        undeclared_boundary_changes = bool(risk.get("undeclaredSafetyBoundaryChanges", rec.get("undeclaredSafetyBoundaryChanges", False)))
        false_canonical_equivalence_claim = bool(risk.get("falseCanonicalEquivalenceClaims", rec.get("falseCanonicalEquivalenceClaims", False)))

        atlas_classes = _atlas_classes(
            authorship_verified,
            derivative_disclosed,
            trust_degraded,
            divergence_detected,
            provenance_breakage,
        )

        base = {
            "reviewId": review_id,
            "originProject": origin_project,
            "canonicalAuthors": canonical_authors,
            "sourceRepos": source_repos,
            "authorshipVerified": authorship_verified,
            "canonicalAuthorshipStatus": "verified" if authorship_verified else "unverified",
            "derivativeDisclosed": derivative_disclosed,
            "trustDegraded": trust_degraded,
            "attributionDivergenceDetected": divergence_detected,
            "sourceManifestHashPresent": source_manifest_hash_present,
            "constraintSignaturePresent": constraint_signature_present,
            "releaseSignaturePresent": release_signature_present,
            "disclosureCompleteness": disclosure_completeness,
            "divergenceFlags": divergence_flags,
            "divergenceReasons": divergence_reasons,
            "trustStatus": "degraded" if trust_degraded else "verified",
            "canonicalAttributionNotice": canonical_notice,
            "derivativeDisclosureRequired": derivative_disclosure_required,
            "atlasClasses": atlas_classes,
            "visualizationModes": _visualization_modes(trust_degraded),
            "constraintSignature": str(summary.get("constraintSignature", integrity_status.get("constraintSignatureSha256", "unknown"))),
            "releaseSignature": str(summary.get("releaseSignature", "unknown")),
            "auditState": str(audit.get("authorshipIntegrityAuditState", rec.get("authorshipIntegrityAuditState", "none"))),
        }

        if action == "docket":
            dashboard_entries.append({**base, "queuedAt": generated_at})
            registry_entries.append({
                **base,
                "retainedAttributionMarkers": retained_attribution_markers,
                "safetyBoundaryChangeDeclarations": safety_boundary_change_declarations,
                "signatureMetadata": signature_metadata,
                "updatedAt": generated_at,
            })

        if action == "watch":
            watch_entries.append({
                **base,
                "status": "watch",
                "missingAttribution": missing_attribution,
                "provenanceBreakage": provenance_breakage,
                "undeclaredSafetyBoundaryChanges": undeclared_boundary_changes,
                "falseCanonicalEquivalenceClaims": false_canonical_equivalence_claim,
                "captureRiskLinkedToMisrepresentation": capture_risk_linked,
                "queuedAt": generated_at,
            })

        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "canonicalAttributionNoticePresent": True,
            "derivativeDisclosureNotice": derivative_disclosed,
            "trustDegradedNotice": trust_degraded,
            "attributionDivergenceDetectedNotice": divergence_detected,
            "noRetaliation": True,
            "noSabotage": True,
            "noGovernanceRightMutation": True,
            "noSovereignAuthorityAssignment": True,
            "noHiddenSabotage": True,
            "noCovertPunishment": True,
            "noDeletionOrDisablingLogic": True,
            "noAutoBlockingDerivativesSolelyForBeingDerivatives": True,
            "onlyVisibleTrustDegradationAndDisclosureSignaling": True,
        })

    shared = {
        "generatedAt": generated_at,
        "authorshipIntegrityProtocol": True,
        "nonCanonical": True,
        "originProject": "Ultra Verba Lux Mentis / Triadic Commons Architecture",
        "canonicalAuthors": ["Thomas Prislac", "Envoy Echo"],
        "canonicalAttributionNotice": CANONICAL_ATTRIBUTION_NOTICE,
        "derivativeDisclosureRequired": True,
        "noGovernanceRightMutation": True,
        "noSovereignAuthorityAssignment": True,
        "noHiddenSabotage": True,
        "noCovertPunishment": True,
        "noDeletionOrDisablingLogic": True,
        "noAutoBlockingDerivativesSolelyForBeingDerivatives": True,
        "onlyVisibleTrustDegradationAndDisclosureSignaling": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": provenance_summary,
        **integrity_status,
    }

    authorship_integrity_dashboard = {
        **shared,
        "entries": sorted(dashboard_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    derivative_registry = {
        **shared,
        "entries": sorted(registry_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    misattribution_watchlist = {
        **shared,
        "entries": sorted(watch_entries, key=lambda row: str(row.get("reviewId", ""))),
    }
    authorship_annotations = {
        **shared,
        "annotations": sorted(annotation_entries, key=lambda row: str(row.get("reviewId", ""))),
    }

    for payload, key in (
        (authorship_integrity_dashboard, "entries"),
        (derivative_registry, "entries"),
        (misattribution_watchlist, "entries"),
        (authorship_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for field in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(field), bool):
                raise ValueError(f"{field} must be a boolean")

    return authorship_integrity_dashboard, derivative_registry, misattribution_watchlist, authorship_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--authorship-integrity-audit", type=Path, default=Path("bridge/authorship_integrity_audit.json"))
    parser.add_argument("--authorship-integrity-recommendations", type=Path, default=Path("bridge/authorship_integrity_recommendations.json"))
    parser.add_argument("--canonical-authorship-manifest", type=Path, default=Path("bridge/canonical_authorship_manifest.json"))
    parser.add_argument("--derivative-disclosure-report", type=Path, default=Path("bridge/derivative_disclosure_report.json"))
    parser.add_argument("--misattribution-risk-report", type=Path, default=Path("bridge/misattribution_risk_report.json"))
    parser.add_argument("--authorship-integrity-summary", type=Path, default=Path("bridge/authorship_integrity_summary.json"))

    parser.add_argument("--observer-dashboard", type=Path, default=Path("registry/observer_dashboard.json"))
    parser.add_argument("--knowledge-river-dashboard", type=Path, default=Path("registry/knowledge_river_dashboard.json"))
    parser.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    parser.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))

    parser.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    parser.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    parser.add_argument("--out-authorship-integrity-dashboard", type=Path, default=Path("registry/authorship_integrity_dashboard.json"))
    parser.add_argument("--out-derivative-registry", type=Path, default=Path("registry/derivative_registry.json"))
    parser.add_argument("--out-misattribution-watchlist", type=Path, default=Path("registry/misattribution_watchlist.json"))
    parser.add_argument("--out-authorship-annotations", type=Path, default=Path("registry/authorship_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_authorship_integrity_overlays(
            load_required_json(args.authorship_integrity_audit),
            load_required_json(args.authorship_integrity_recommendations),
            load_required_json(args.canonical_authorship_manifest),
            load_required_json(args.derivative_disclosure_report),
            load_required_json(args.misattribution_risk_report),
            load_required_json(args.authorship_integrity_summary),
            load_required_json(args.observer_dashboard),
            load_required_json(args.knowledge_river_dashboard),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.commons_sovereignty_dashboard),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    for out in (
        args.out_authorship_integrity_dashboard,
        args.out_derivative_registry,
        args.out_misattribution_watchlist,
        args.out_authorship_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_authorship_integrity_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_derivative_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_misattribution_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_authorship_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote authorship integrity dashboard: {args.out_authorship_integrity_dashboard}")
    print(f"[OK] Wrote derivative registry: {args.out_derivative_registry}")
    print(f"[OK] Wrote misattribution watchlist: {args.out_misattribution_watchlist}")
    print(f"[OK] Wrote authorship annotations: {args.out_authorship_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
