#!/usr/bin/env python3
"""Build observer onboarding overlays for Atlas and dashboard views.

Publisher surfaces Sophia-audited observer and onboarding materials for legibility
and bounded participation only; no automatic governance-right expansion,
personhood declaration, ranking, or sovereignty assignment occurs from this layer.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from canonical_integrity_manifest import evaluate_manifest_pair, load_manifest

REQUIRED_PROVENANCE_KEYS = ("schemaVersion", "producerCommits", "sourceMode")
RESETTABLE_ATLAS_CLASSES = [
    "observer-guided",
    "observer-public",
    "observer-sophia",
    "observer-witness",
    "standing-bounded",
    "standing-review",
    "capture-risk",
    "translation-required",
    "trust-presentation-degraded",
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


def _index_by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        kv = row.get(key)
        if isinstance(kv, str):
            out[kv] = row
    return out


def _extract_required_provenance(name: str, artifact: dict[str, Any]) -> dict[str, Any]:
    prov = artifact.get("provenance")
    if not isinstance(prov, dict):
        raise ValueError(f"{name} missing required provenance metadata")
    for key in REQUIRED_PROVENANCE_KEYS:
        if key not in prov:
            raise ValueError(f"{name} provenance missing required field: {key}")
    if not isinstance(prov.get("schemaVersion"), str) or not str(prov.get("schemaVersion", "")).strip():
        raise ValueError(f"{name} provenance.schemaVersion must be a non-empty string")
    commits = prov.get("producerCommits")
    if not isinstance(commits, list) or not commits or not all(isinstance(v, str) and v.strip() for v in commits):
        raise ValueError(f"{name} provenance.producerCommits must be a non-empty list of non-empty strings")
    if not isinstance(prov.get("sourceMode"), str) or not str(prov.get("sourceMode", "")).strip():
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


def _build_provenance_summary(provs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    commits: list[str] = []
    schema_versions: dict[str, str] = {}
    source_modes: dict[str, str] = {}
    for name, prov in provs.items():
        schema_versions[name] = str(prov.get("schemaVersion"))
        source_modes[name] = str(prov.get("sourceMode"))
        for commit in prov.get("producerCommits", []):
            if commit not in commits:
                commits.append(commit)
    return {
        "schemaVersions": schema_versions,
        "producerCommits": commits,
        "sourceModes": source_modes,
        "derivedFromFixtures": any(mode.lower() == "fixture" for mode in source_modes.values()),
    }


def _to_float(v: Any, default: float = 0.0) -> float:
    if isinstance(v, bool):
        return default
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip()) if v.strip() else default
        except ValueError:
            return default
    return default


def _action(rec: dict[str, Any]) -> str:
    action = str(rec.get("targetPublisherAction", "watch")).strip().lower()
    if action == "suppressed":
        return "suppress"
    return action if action in {"docket", "watch", "suppress", "rejected"} else "watch"


def _modes(observer_class: str, guided_required: bool, translation_required: bool) -> list[dict[str, Any]]:
    base = [
        {
            "mode": "Sophia Internal",
            "detailLevel": "high",
            "renderMode": "provenance-rich",
            "auditVisibility": "full",
            "unsafeMutationSurfaceExposure": "none",
        },
        {
            "mode": "Human Steward",
            "detailLevel": "medium",
            "renderMode": "decision-support",
            "auditVisibility": "review-queue",
            "unsafeMutationSurfaceExposure": "none",
        },
        {
            "mode": "Human Public / Commons",
            "detailLevel": "bounded",
            "renderMode": "public-summary",
            "auditVisibility": "bounded",
            "unsafeMutationSurfaceExposure": "none",
        },
        {
            "mode": "Recognized/Guided Other-Intelligence View",
            "detailLevel": "low" if translation_required else "medium",
            "renderMode": "translation-first",
            "auditVisibility": "bounded",
            "unsafeMutationSurfaceExposure": "none",
        },
    ]
    if observer_class == "witness":
        base[1]["renderMode"] = "witness-cues"
    if guided_required:
        for m in base:
            m["guidedParticipation"] = True
    return base


def _atlas_classes(observer_class: str, standing: str, capture_risk: str, translation_required: bool, trust_degraded: bool) -> list[str]:
    klass = {
        "sophia": "observer-sophia",
        "public": "observer-public",
        "guided": "observer-guided",
        "witness": "observer-witness",
    }.get(observer_class, "observer-guided")
    out = [klass]
    out.append("standing-review" if standing in {"review", "unclear", "pending"} else "standing-bounded")
    if capture_risk in {"high", "elevated", "critical"}:
        out.append("capture-risk")
    if translation_required:
        out.append("translation-required")
    if trust_degraded:
        out.append("trust-presentation-degraded")
    return out


def build_observer_onboarding_overlays(
    observer_onboarding_audit: dict[str, Any],
    observer_onboarding_recommendations: dict[str, Any],
    observer_class_map: dict[str, Any],
    visualization_readiness_report: dict[str, Any],
    participatory_standing_registry: dict[str, Any],
    onboarding_capture_risk_report: dict[str, Any],
    commons_sovereignty_dashboard: dict[str, Any],
    civilizational_memory_dashboard: dict[str, Any],
    knowledge_river_dashboard: dict[str, Any],
    river_capture_watchlist: dict[str, Any],
    bridge_canonical_integrity_manifest: dict[str, Any] | None = None,
    registry_canonical_integrity_manifest: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()
    integrity = evaluate_manifest_pair(bridge_canonical_integrity_manifest, registry_canonical_integrity_manifest)

    provs = {
        "observer_onboarding_audit": _extract_required_provenance("observer_onboarding_audit", observer_onboarding_audit),
        "observer_onboarding_recommendations": _extract_required_provenance("observer_onboarding_recommendations", observer_onboarding_recommendations),
        "observer_class_map": _extract_required_provenance("observer_class_map", observer_class_map),
        "visualization_readiness_report": _extract_required_provenance("visualization_readiness_report", visualization_readiness_report),
        "participatory_standing_registry": _extract_required_provenance("participatory_standing_registry", participatory_standing_registry),
        "onboarding_capture_risk_report": _extract_required_provenance("onboarding_capture_risk_report", onboarding_capture_risk_report),
    }
    for name, artifact in {
        "commons_sovereignty_dashboard": commons_sovereignty_dashboard,
        "civilizational_memory_dashboard": civilizational_memory_dashboard,
        "knowledge_river_dashboard": knowledge_river_dashboard,
        "river_capture_watchlist": river_capture_watchlist,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provs[name] = optional

    class_by_id = _index_by_key([e for e in as_list(observer_class_map.get("entries")) if isinstance(e, dict)], "reviewId")
    viz_by_id = _index_by_key([e for e in as_list(visualization_readiness_report.get("entries")) if isinstance(e, dict)], "reviewId")
    standing_by_id = _index_by_key([e for e in as_list(participatory_standing_registry.get("entries")) if isinstance(e, dict)], "reviewId")
    risk_by_id = _index_by_key([e for e in as_list(onboarding_capture_risk_report.get("entries")) if isinstance(e, dict)], "reviewId")
    audit_by_id = _index_by_key([e for e in as_list(observer_onboarding_audit.get("audits")) if isinstance(e, dict)], "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    visualization_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    class_counts: dict[str, int] = {}
    guided_needs = 0
    standing_review_queue = 0
    capture_warnings = 0

    recs = [e for e in as_list(observer_onboarding_recommendations.get("recommendations")) if isinstance(e, dict)]
    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue
        action = _action(rec)

        cls = class_by_id.get(review_id, {})
        viz = viz_by_id.get(review_id, {})
        std = standing_by_id.get(review_id, {})
        risk = risk_by_id.get(review_id, {})
        audit = audit_by_id.get(review_id, {})

        observer_class = str(cls.get("observerClass", rec.get("observerClass", "guided"))).lower()
        view_legibility = str(viz.get("viewLegibility", rec.get("viewLegibility", "bounded")))
        guided_required = bool(viz.get("guidedInterfaceRequired", rec.get("guidedInterfaceRequired", True)))
        participatory_standing = str(std.get("participatoryStanding", rec.get("participatoryStanding", "review")))
        suffrage_review_flag = bool(std.get("suffrageReviewFlag", rec.get("suffrageReviewFlag", True)))
        translation_required = bool(viz.get("translationSupportRequired", rec.get("translationSupportRequired", False)))
        capture_risk = str(risk.get("captureRisk", rec.get("captureRisk", "bounded"))).lower()
        anti_priesthood_guard = bool(rec.get("antiPriesthoodGuard", True))
        witness_only = bool(std.get("witnessOnly", rec.get("witnessOnly", observer_class == "witness")))
        trust_degraded = bool(integrity.get("trustPresentationDegraded", False))

        visualization_readiness = _to_float(viz.get("visualizationReadiness", rec.get("visualizationReadiness", 0.0)))
        cognitive_load_class = str(viz.get("cognitiveLoadClass", rec.get("cognitiveLoadClass", "bounded")))
        panel_eligibility = as_list(viz.get("panelEligibility", rec.get("panelEligibility", ["summary"])))
        detail_level = str(viz.get("detailLevel", rec.get("detailLevel", "bounded")))
        render_mode = str(viz.get("renderMode", rec.get("renderMode", "review")))
        translation_support_requirements = as_list(viz.get("translationSupportRequirements", rec.get("translationSupportRequirements", [])))
        vote_eligibility_basis = str(std.get("voteEligibilityBasis", rec.get("voteEligibilityBasis", "bounded-review")))
        revocation_conditions = as_list(std.get("revocationConditions", rec.get("revocationConditions", ["capture-risk-elevation"])))
        provenance_markers = as_list(risk.get("provenanceMarkers", rec.get("provenanceMarkers", [])))
        canonical_markers = as_list(risk.get("canonicalIntegrityMarkers", rec.get("canonicalIntegrityMarkers", [])))

        class_counts[observer_class] = class_counts.get(observer_class, 0) + 1
        if guided_required:
            guided_needs += 1
        if participatory_standing in {"review", "unclear", "pending"}:
            standing_review_queue += 1
        if capture_risk in {"high", "elevated", "critical"}:
            capture_warnings += 1

        base = {
            "reviewId": review_id,
            "observerClass": observer_class,
            "viewLegibility": view_legibility,
            "guidedInterfaceRequired": guided_required,
            "participatoryStanding": participatory_standing,
            "suffrageReviewFlag": suffrage_review_flag,
            "translationSupportRequired": translation_required,
            "captureRisk": capture_risk,
            "antiPriesthoodGuard": anti_priesthood_guard,
            "trustPresentationDegraded": trust_degraded,
            "visualizationReadiness": visualization_readiness,
            "canonicalIntegrityStatus": "degraded" if trust_degraded else "verified",
            "provenanceMarkers": provenance_markers,
            "canonicalIntegrityMarkers": canonical_markers,
        }

        if action == "docket":
            dashboard_entries.append({
                **base,
                "allowedPanels": panel_eligibility,
                "standingStatus": participatory_standing,
                "guidedViewNeeds": guided_required,
                "captureWarnings": capture_risk in {"high", "elevated", "critical"},
                "standingReviewQueue": participatory_standing in {"review", "unclear", "pending"},
                "visualizationReadinessByClass": {observer_class: visualization_readiness},
                "queuedAt": generated_at,
            })
            visualization_entries.append({
                **base,
                "panelEligibility": panel_eligibility,
                "detailLevel": detail_level,
                "renderMode": render_mode,
                "cognitiveLoadClass": cognitive_load_class,
                "translationSupportRequirements": translation_support_requirements,
                "visualizationModes": _modes(observer_class, guided_required, translation_required),
                "atlasClasses": _atlas_classes(observer_class, participatory_standing, capture_risk, translation_required, trust_degraded),
                "voteEligibilityBasis": vote_eligibility_basis,
                "revocationConditions": revocation_conditions,
                "updatedAt": generated_at,
            })

        if action == "watch":
            watch_entries.append({
                **base,
                "status": "watch",
                "unclearStanding": participatory_standing in {"review", "unclear", "pending"},
                "lowLegibilityParticipant": view_legibility in {"low", "opaque", "unclear"},
                "unresolvedSuffrageReview": suffrage_review_flag,
                "highCaptureRiskCandidate": capture_risk in {"high", "elevated", "critical"},
                "queuedAt": generated_at,
            })

        # include bounded annotation even for suppress action
        annotation_entries.append({
            **base,
            "targetPublisherAction": action,
            "witnessOnly": witness_only,
            "guidedParticipation": guided_required,
            "boundedSuffrageEligible": participatory_standing in {"bounded", "eligible"} and not suffrage_review_flag,
            "translationRequired": translation_required,
            "atlasClasses": _atlas_classes(observer_class, participatory_standing, capture_risk, translation_required, trust_degraded),
            "auditState": str(audit.get("observerOnboardingAuditState", rec.get("observerOnboardingAuditState", "none"))),
            "noGovernanceRightMutation": True,
            "noSovereignAuthorityAssignment": True,
            "noAutomaticWorthRanking": True,
            "noCoerciveNormalization": True,
            "noCanonClosure": True,
            "noHiddenMutationControls": True,
        })

    shared = {
        "generatedAt": generated_at,
        "observerOnboardingProtocol": True,
        "nonCanonical": True,
        "noGovernanceRightMutation": True,
        "noSovereignAuthorityAssignment": True,
        "noAutomaticWorthRanking": True,
        "noCoerciveNormalization": True,
        "noCanonClosure": True,
        "noHiddenMutationControls": True,
        "atlasResetRemovesClasses": RESETTABLE_ATLAS_CLASSES,
        "provenance": _build_provenance_summary(provs),
        **integrity,
    }

    observer_dashboard = {
        **shared,
        "observerClassCounts": class_counts,
        "guidedViewNeeds": guided_needs,
        "standingReviewQueues": standing_review_queue,
        "captureWarnings": capture_warnings,
        "visualizationReadinessByClass": {
            e["observerClass"]: e["visualizationReadiness"] for e in dashboard_entries
        },
        "entries": dashboard_entries,
    }
    visualization_registry = {**shared, "entries": visualization_entries}
    onboarding_watchlist = {**shared, "entries": watch_entries}
    participation_annotations = {**shared, "annotations": annotation_entries}

    for payload, key in (
        (observer_dashboard, "entries"),
        (visualization_registry, "entries"),
        (onboarding_watchlist, "entries"),
        (participation_annotations, "annotations"),
    ):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"{key} must be a list")
        for b in ("canonicalIntegrityVerified", "modificationDisclosureMissing", "trustPresentationDegraded"):
            if not isinstance(payload.get(b), bool):
                raise ValueError(f"{b} must be a boolean")

    return observer_dashboard, visualization_registry, onboarding_watchlist, participation_annotations


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--observer-onboarding-audit", type=Path, default=Path("bridge/observer_onboarding_audit.json"))
    p.add_argument("--observer-onboarding-recommendations", type=Path, default=Path("bridge/observer_onboarding_recommendations.json"))
    p.add_argument("--observer-class-map", type=Path, default=Path("bridge/observer_class_map.json"))
    p.add_argument("--visualization-readiness-report", type=Path, default=Path("bridge/visualization_readiness_report.json"))
    p.add_argument("--participatory-standing-registry", type=Path, default=Path("bridge/participatory_standing_registry.json"))
    p.add_argument("--onboarding-capture-risk-report", type=Path, default=Path("bridge/onboarding_capture_risk_report.json"))

    p.add_argument("--commons-sovereignty-dashboard", type=Path, default=Path("registry/commons_sovereignty_dashboard.json"))
    p.add_argument("--civilizational-memory-dashboard", type=Path, default=Path("registry/civilizational_memory_dashboard.json"))
    p.add_argument("--knowledge-river-dashboard", type=Path, default=Path("registry/knowledge_river_dashboard.json"))
    p.add_argument("--river-capture-watchlist", type=Path, default=Path("registry/river_capture_watchlist.json"))

    p.add_argument("--bridge-canonical-integrity-manifest", type=Path, default=Path("bridge/canonical_integrity_manifest.json"))
    p.add_argument("--registry-canonical-integrity-manifest", type=Path, default=Path("registry/canonical_integrity_manifest.json"))

    p.add_argument("--out-observer-dashboard", type=Path, default=Path("registry/observer_dashboard.json"))
    p.add_argument("--out-visualization-registry", type=Path, default=Path("registry/visualization_registry.json"))
    p.add_argument("--out-onboarding-watchlist", type=Path, default=Path("registry/onboarding_watchlist.json"))
    p.add_argument("--out-participation-annotations", type=Path, default=Path("registry/participation_annotations.json"))
    args = p.parse_args()

    try:
        outputs = build_observer_onboarding_overlays(
            load_required_json(args.observer_onboarding_audit),
            load_required_json(args.observer_onboarding_recommendations),
            load_required_json(args.observer_class_map),
            load_required_json(args.visualization_readiness_report),
            load_required_json(args.participatory_standing_registry),
            load_required_json(args.onboarding_capture_risk_report),
            load_required_json(args.commons_sovereignty_dashboard),
            load_required_json(args.civilizational_memory_dashboard),
            load_required_json(args.knowledge_river_dashboard),
            load_required_json(args.river_capture_watchlist),
            load_manifest(args.bridge_canonical_integrity_manifest),
            load_manifest(args.registry_canonical_integrity_manifest),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    for out in (
        args.out_observer_dashboard,
        args.out_visualization_registry,
        args.out_onboarding_watchlist,
        args.out_participation_annotations,
    ):
        out.parent.mkdir(parents=True, exist_ok=True)

    args.out_observer_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_visualization_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_onboarding_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_participation_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote observer dashboard: {args.out_observer_dashboard}")
    print(f"[OK] Wrote visualization registry: {args.out_visualization_registry}")
    print(f"[OK] Wrote onboarding watchlist: {args.out_onboarding_watchlist}")
    print(f"[OK] Wrote participation annotations: {args.out_participation_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
