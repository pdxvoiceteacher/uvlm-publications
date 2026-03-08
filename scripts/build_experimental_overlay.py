#!/usr/bin/env python3
"""Build experimental design, falsification, and replication overlays.

Publisher surfaces only Sophia-audited experimental materials; no automatic
theory promotion or canonical mutation occurs from this layer.
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


def _validate_outputs(experiment_dashboard: dict[str, Any], hypothesis_registry: dict[str, Any], falsification_watchlist: dict[str, Any], theory_gate_annotations: dict[str, Any]) -> None:
    if not isinstance(experiment_dashboard.get("entries"), list):
        raise ValueError("experiment_dashboard.entries must be a list")
    if not isinstance(hypothesis_registry.get("entries"), list):
        raise ValueError("hypothesis_registry.entries must be a list")
    if not isinstance(falsification_watchlist.get("entries"), list):
        raise ValueError("falsification_watchlist.entries must be a list")
    if not isinstance(theory_gate_annotations.get("annotations"), list):
        raise ValueError("theory_gate_annotations.annotations must be a list")
    for payload in (experiment_dashboard, hypothesis_registry, falsification_watchlist, theory_gate_annotations):
        json.dumps(payload)


def build_experimental_overlays(
    experimental_audit: dict[str, Any],
    experimental_recommendations: dict[str, Any],
    experimental_hypothesis_map: dict[str, Any],
    falsification_design_report: dict[str, Any],
    replication_pathway_map: dict[str, Any],
    theory_promotion_gate: dict[str, Any],
    prediction_dashboard: dict[str, Any],
    branch_dashboard: dict[str, Any],
    authority_gate_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "experimental_audit": _extract_required_provenance("experimental_audit", experimental_audit),
        "experimental_recommendations": _extract_required_provenance("experimental_recommendations", experimental_recommendations),
        "experimental_hypothesis_map": _extract_required_provenance("experimental_hypothesis_map", experimental_hypothesis_map),
        "falsification_design_report": _extract_required_provenance("falsification_design_report", falsification_design_report),
        "replication_pathway_map": _extract_required_provenance("replication_pathway_map", replication_pathway_map),
        "theory_promotion_gate": _extract_required_provenance("theory_promotion_gate", theory_promotion_gate),
    }
    for name, artifact in {
        "prediction_dashboard": prediction_dashboard,
        "branch_dashboard": branch_dashboard,
        "authority_gate_dashboard": authority_gate_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional
    provenance_summary = _build_provenance_summary(provenances)

    audits = [a for a in as_list(experimental_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(experimental_recommendations.get("recommendations")) if isinstance(r, dict)]
    hypotheses = [e for e in as_list(experimental_hypothesis_map.get("entries")) if isinstance(e, dict)]
    falsification = [e for e in as_list(falsification_design_report.get("entries")) if isinstance(e, dict)]
    replication = [e for e in as_list(replication_pathway_map.get("entries")) if isinstance(e, dict)]
    theory_gate = [e for e in as_list(theory_promotion_gate.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    hypothesis_by_review = _index_by_key(hypotheses, "reviewId")
    falsification_by_review = _index_by_key(falsification, "reviewId")
    replication_by_review = _index_by_key(replication, "reviewId")
    gate_by_review = _index_by_key(theory_gate, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        hyp = hypothesis_by_review.get(review_id, {})
        fal = falsification_by_review.get(review_id, {})
        rep = replication_by_review.get(review_id, {})
        gate = gate_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        experimental_status = str(hyp.get("experimentalStatus", rec.get("experimentalStatus", "design")))
        hypothesis_class = str(hyp.get("hypothesisClass", rec.get("hypothesisClass", "exploratory")))
        falsification_readiness = str(fal.get("falsificationReadiness", rec.get("falsificationReadiness", "pending")))
        falsification_plan = sorted([x for x in as_list(fal.get("falsificationPlan", rec.get("falsificationPlan", []))) if isinstance(x, str)])
        replication_pathway_status = str(rep.get("replicationPathwayStatus", rec.get("replicationPathwayStatus", "pending")))
        replication_pathways = sorted([x for x in as_list(rep.get("replicationPathways", rec.get("replicationPathways", []))) if isinstance(x, str)])
        theory_gate_class = str(gate.get("theoryGateClass", rec.get("theoryGateClass", "hold")))
        theory_gate_reason = str(gate.get("theoryGateReason", rec.get("theoryGateReason", "insufficient-evidence")))
        experimental_audit_state = str(audit.get("experimentalAuditState", rec.get("experimentalAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "experimentalStatus": experimental_status,
            "hypothesisClass": hypothesis_class,
            "falsificationReadiness": falsification_readiness,
            "falsificationPlan": falsification_plan,
            "replicationPathwayStatus": replication_pathway_status,
            "replicationPathways": replication_pathways,
            "theoryGateClass": theory_gate_class,
            "theoryGateReason": theory_gate_reason,
            "experimentalAuditState": experimental_audit_state,
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
            "noAutomaticTheoryPromotion": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    experiment_dashboard = {
        "generatedAt": generated_at,
        "experimentalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    hypothesis_registry = {
        "generatedAt": generated_at,
        "experimentalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    falsification_watchlist = {
        "generatedAt": generated_at,
        "experimentalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    theory_gate_annotations = {
        "generatedAt": generated_at,
        "experimentalProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticTheoryPromotion": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(experiment_dashboard, hypothesis_registry, falsification_watchlist, theory_gate_annotations)
    return experiment_dashboard, hypothesis_registry, falsification_watchlist, theory_gate_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experimental-audit", type=Path, default=Path("bridge/experimental_audit.json"))
    parser.add_argument("--experimental-recommendations", type=Path, default=Path("bridge/experimental_recommendations.json"))
    parser.add_argument("--experimental-hypothesis-map", type=Path, default=Path("bridge/experimental_hypothesis_map.json"))
    parser.add_argument("--falsification-design-report", type=Path, default=Path("bridge/falsification_design_report.json"))
    parser.add_argument("--replication-pathway-map", type=Path, default=Path("bridge/replication_pathway_map.json"))
    parser.add_argument("--theory-promotion-gate", type=Path, default=Path("bridge/theory_promotion_gate.json"))

    parser.add_argument("--prediction-dashboard", type=Path, default=Path("registry/prediction_dashboard.json"))
    parser.add_argument("--branch-dashboard", type=Path, default=Path("registry/branch_dashboard.json"))
    parser.add_argument("--authority-gate-dashboard", type=Path, default=Path("registry/authority_gate_dashboard.json"))

    parser.add_argument("--out-experiment-dashboard", type=Path, default=Path("registry/experiment_dashboard.json"))
    parser.add_argument("--out-hypothesis-registry", type=Path, default=Path("registry/hypothesis_registry.json"))
    parser.add_argument("--out-falsification-watchlist", type=Path, default=Path("registry/falsification_watchlist.json"))
    parser.add_argument("--out-theory-gate-annotations", type=Path, default=Path("registry/theory_gate_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_experimental_overlays(
            load_required_json(args.experimental_audit),
            load_required_json(args.experimental_recommendations),
            load_required_json(args.experimental_hypothesis_map),
            load_required_json(args.falsification_design_report),
            load_required_json(args.replication_pathway_map),
            load_required_json(args.theory_promotion_gate),
            load_required_json(args.prediction_dashboard),
            load_required_json(args.branch_dashboard),
            load_required_json(args.authority_gate_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_experiment_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_hypothesis_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_falsification_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_theory_gate_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_experiment_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_hypothesis_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_falsification_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_theory_gate_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote experiment dashboard: {args.out_experiment_dashboard}")
    print(f"[OK] Wrote hypothesis registry: {args.out_hypothesis_registry}")
    print(f"[OK] Wrote falsification watchlist: {args.out_falsification_watchlist}")
    print(f"[OK] Wrote theory gate annotations: {args.out_theory_gate_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
