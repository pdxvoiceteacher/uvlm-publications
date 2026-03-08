#!/usr/bin/env python3
"""Build theory corpus, revision lineage, and negative-results overlays.

Publisher surfaces only Sophia-audited theory corpus materials; no automatic
 theory certification or canonical mutation occurs from this layer.
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


def _validate_outputs(theory_dashboard: dict[str, Any], theory_registry: dict[str, Any], negative_result_watchlist: dict[str, Any], theory_annotations: dict[str, Any]) -> None:
    if not isinstance(theory_dashboard.get("entries"), list):
        raise ValueError("theory_dashboard.entries must be a list")
    if not isinstance(theory_registry.get("entries"), list):
        raise ValueError("theory_registry.entries must be a list")
    if not isinstance(negative_result_watchlist.get("entries"), list):
        raise ValueError("negative_result_watchlist.entries must be a list")
    if not isinstance(theory_annotations.get("annotations"), list):
        raise ValueError("theory_annotations.annotations must be a list")
    for payload in (theory_dashboard, theory_registry, negative_result_watchlist, theory_annotations):
        json.dumps(payload)


def build_theory_corpus_overlays(
    theory_corpus_audit: dict[str, Any],
    theory_corpus_recommendations: dict[str, Any],
    theory_corpus_map: dict[str, Any],
    theory_revision_lineage: dict[str, Any],
    negative_result_registry: dict[str, Any],
    theory_competition_report: dict[str, Any],
    experiment_dashboard: dict[str, Any],
    prediction_dashboard: dict[str, Any],
    branch_dashboard: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    provenances = {
        "theory_corpus_audit": _extract_required_provenance("theory_corpus_audit", theory_corpus_audit),
        "theory_corpus_recommendations": _extract_required_provenance("theory_corpus_recommendations", theory_corpus_recommendations),
        "theory_corpus_map": _extract_required_provenance("theory_corpus_map", theory_corpus_map),
        "theory_revision_lineage": _extract_required_provenance("theory_revision_lineage", theory_revision_lineage),
        "negative_result_registry": _extract_required_provenance("negative_result_registry", negative_result_registry),
        "theory_competition_report": _extract_required_provenance("theory_competition_report", theory_competition_report),
    }
    for name, artifact in {
        "experiment_dashboard": experiment_dashboard,
        "prediction_dashboard": prediction_dashboard,
        "branch_dashboard": branch_dashboard,
    }.items():
        optional = _extract_optional_provenance(name, artifact)
        if optional:
            provenances[name] = optional

    provenance_summary = _build_provenance_summary(provenances)

    audits = [e for e in as_list(theory_corpus_audit.get("audits")) if isinstance(e, dict)]
    recs = [e for e in as_list(theory_corpus_recommendations.get("recommendations")) if isinstance(e, dict)]
    corpus_entries = [e for e in as_list(theory_corpus_map.get("entries")) if isinstance(e, dict)]
    lineage_entries = [e for e in as_list(theory_revision_lineage.get("entries")) if isinstance(e, dict)]
    negative_entries = [e for e in as_list(negative_result_registry.get("entries")) if isinstance(e, dict)]
    competition_entries = [e for e in as_list(theory_competition_report.get("entries")) if isinstance(e, dict)]

    audit_by_review = _index_by_key(audits, "reviewId")
    corpus_by_review = _index_by_key(corpus_entries, "reviewId")
    lineage_by_review = _index_by_key(lineage_entries, "reviewId")
    negative_by_review = _index_by_key(negative_entries, "reviewId")
    competition_by_review = _index_by_key(competition_entries, "reviewId")

    dashboard_entries: list[dict[str, Any]] = []
    registry_entries: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []
    annotation_entries: list[dict[str, Any]] = []

    for rec in sorted(recs, key=lambda r: str(r.get("reviewId", ""))):
        review_id = rec.get("reviewId")
        if not isinstance(review_id, str):
            continue

        action = _action(rec)
        corpus = corpus_by_review.get(review_id, {})
        lineage = lineage_by_review.get(review_id, {})
        negative = negative_by_review.get(review_id, {})
        competition = competition_by_review.get(review_id, {})
        audit = audit_by_review.get(review_id, {})

        theory_status = str(corpus.get("theoryStatus", rec.get("theoryStatus", "under-review")))
        falsification_status = str(corpus.get("falsificationStatus", rec.get("falsificationStatus", "pending")))
        replication_status = str(corpus.get("replicationStatus", rec.get("replicationStatus", "pending")))
        revision_lineage = sorted([x for x in as_list(lineage.get("revisionLineage", rec.get("revisionLineage", []))) if isinstance(x, str)])
        negative_result_indicators = sorted([x for x in as_list(negative.get("negativeResultIndicators", rec.get("negativeResultIndicators", []))) if isinstance(x, str)])
        competition_state = str(competition.get("competitionState", corpus.get("competitionState", rec.get("competitionState", "unresolved"))))
        competition_peers = sorted([x for x in as_list(competition.get("competitionPeers", rec.get("competitionPeers", []))) if isinstance(x, str)])
        theory_audit_state = str(audit.get("theoryAuditState", rec.get("theoryAuditState", "none")))
        linked_target_ids = _targets(rec)

        base = {
            "reviewId": review_id,
            "theoryStatus": theory_status,
            "falsificationStatus": falsification_status,
            "replicationStatus": replication_status,
            "revisionLineage": revision_lineage,
            "negativeResultIndicators": negative_result_indicators,
            "competitionState": competition_state,
            "competitionPeers": competition_peers,
            "theoryAuditState": theory_audit_state,
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
            "noAutomaticTheoryCertification": True,
            "noAutomaticGraphMutation": True,
            "noCanonicalMutation": True,
            "notes": rec.get("notes", ""),
        })

    theory_dashboard = {
        "generatedAt": generated_at,
        "theoryCorpusProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(dashboard_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    theory_registry = {
        "generatedAt": generated_at,
        "theoryCorpusProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(registry_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    negative_result_watchlist = {
        "generatedAt": generated_at,
        "theoryCorpusProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "entries": sorted(watch_entries, key=lambda e: str(e.get("reviewId", ""))),
    }
    theory_annotations = {
        "generatedAt": generated_at,
        "theoryCorpusProtocol": True,
        "nonCanonical": True,
        "provenance": provenance_summary,
        "noAutomaticTheoryCertification": True,
        "noAutomaticGraphMutation": True,
        "noCanonicalMutation": True,
        "annotations": sorted(annotation_entries, key=lambda e: str(e.get("reviewId", ""))),
    }

    _validate_outputs(theory_dashboard, theory_registry, negative_result_watchlist, theory_annotations)
    return theory_dashboard, theory_registry, negative_result_watchlist, theory_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theory-corpus-audit", type=Path, default=Path("bridge/theory_corpus_audit.json"))
    parser.add_argument("--theory-corpus-recommendations", type=Path, default=Path("bridge/theory_corpus_recommendations.json"))
    parser.add_argument("--theory-corpus-map", type=Path, default=Path("bridge/theory_corpus_map.json"))
    parser.add_argument("--theory-revision-lineage", type=Path, default=Path("bridge/theory_revision_lineage.json"))
    parser.add_argument("--negative-result-registry", type=Path, default=Path("bridge/negative_result_registry.json"))
    parser.add_argument("--theory-competition-report", type=Path, default=Path("bridge/theory_competition_report.json"))

    parser.add_argument("--experiment-dashboard", type=Path, default=Path("registry/experiment_dashboard.json"))
    parser.add_argument("--prediction-dashboard", type=Path, default=Path("registry/prediction_dashboard.json"))
    parser.add_argument("--branch-dashboard", type=Path, default=Path("registry/branch_dashboard.json"))

    parser.add_argument("--out-theory-dashboard", type=Path, default=Path("registry/theory_dashboard.json"))
    parser.add_argument("--out-theory-registry", type=Path, default=Path("registry/theory_registry.json"))
    parser.add_argument("--out-negative-result-watchlist", type=Path, default=Path("registry/negative_result_watchlist.json"))
    parser.add_argument("--out-theory-annotations", type=Path, default=Path("registry/theory_annotations.json"))

    args = parser.parse_args()

    try:
        outputs = build_theory_corpus_overlays(
            load_required_json(args.theory_corpus_audit),
            load_required_json(args.theory_corpus_recommendations),
            load_required_json(args.theory_corpus_map),
            load_required_json(args.theory_revision_lineage),
            load_required_json(args.negative_result_registry),
            load_required_json(args.theory_competition_report),
            load_required_json(args.experiment_dashboard),
            load_required_json(args.prediction_dashboard),
            load_required_json(args.branch_dashboard),
        )
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    args.out_theory_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_theory_registry.parent.mkdir(parents=True, exist_ok=True)
    args.out_negative_result_watchlist.parent.mkdir(parents=True, exist_ok=True)
    args.out_theory_annotations.parent.mkdir(parents=True, exist_ok=True)

    args.out_theory_dashboard.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_theory_registry.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_negative_result_watchlist.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_theory_annotations.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote theory dashboard: {args.out_theory_dashboard}")
    print(f"[OK] Wrote theory registry: {args.out_theory_registry}")
    print(f"[OK] Wrote negative result watchlist: {args.out_negative_result_watchlist}")
    print(f"[OK] Wrote theory annotations: {args.out_theory_annotations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
