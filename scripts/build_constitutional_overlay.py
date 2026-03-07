#!/usr/bin/env python3
"""Build constitutional and continuity governance overlays from Sophia-audited artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


VALID_STATUS = {"stable", "watch", "degraded", "freeze-recommended"}


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def build_constitutional_overlays(
    constitutional_audit: dict[str, Any],
    constitutional_recommendations: dict[str, Any],
    continuity_mode_assessment: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits = [a for a in as_list(constitutional_audit.get("audits")) if isinstance(a, dict)]
    recs = [r for r in as_list(constitutional_recommendations.get("recommendations")) if isinstance(r, dict)]

    continuity_entries = [e for e in as_list(continuity_mode_assessment.get("entries")) if isinstance(e, dict)]

    constitutional_annotations = []
    status_tallies: dict[str, int] = {}

    for audit in audits:
        artifact_id = audit.get("artifactId")
        if not isinstance(artifact_id, str):
            continue

        status = str(audit.get("constitutionalStatus", "watch")).strip().lower()
        if status not in VALID_STATUS:
            status = "watch"
        status_tallies[status] = status_tallies.get(status, 0) + 1

        constitutional_annotations.append(
            {
                "artifactId": artifact_id,
                "constitutionalStatus": status,
                "charterClauses": sorted([c for c in as_list(audit.get("charterClauses")) if isinstance(c, str)]),
                "governanceSignals": sorted([s for s in as_list(audit.get("governanceSignals")) if isinstance(s, str)]),
                "humanReviewFlag": bool(audit.get("humanReviewFlag", False)),
                "notes": audit.get("notes", "")
            }
        )

    continuity_mode = "normal"
    continuity_score = 0.0
    freeze_recommended = False
    if continuity_entries:
        scores = [float(e.get("continuityScore", 0.0)) for e in continuity_entries]
        continuity_score = round(sum(scores) / len(scores), 3)
        freeze_recommended = any(bool(e.get("freezeRecommended", False)) for e in continuity_entries)
        if freeze_recommended or continuity_score < 0.55:
            continuity_mode = "freeze-watch"
        elif continuity_score < 0.75:
            continuity_mode = "watch"

    recommended_status = "stable"
    for precedence in ["freeze-recommended", "degraded", "watch", "stable"]:
        if status_tallies.get(precedence, 0) > 0:
            recommended_status = precedence
            break
    if freeze_recommended:
        recommended_status = "freeze-recommended"

    constitutional_status = {
        "generatedAt": generated_at,
        "constitutionalStatus": recommended_status,
        "governanceFacing": True,
        "nonCanonical": True,
        "finalActionExternal": True,
        "countsByStatus": status_tallies,
    }

    continuity_mode_index = {
        "generatedAt": generated_at,
        "continuityMode": continuity_mode,
        "continuityScore": continuity_score,
        "freezeRecommended": freeze_recommended,
        "governanceFacing": True,
        "nonCanonical": True,
        "entries": sorted(
            [
                {
                    "artifactId": e.get("artifactId"),
                    "continuityScore": float(e.get("continuityScore", 0.0)),
                    "continuityStatus": e.get("continuityStatus", "watch"),
                    "freezeRecommended": bool(e.get("freezeRecommended", False)),
                }
                for e in continuity_entries
                if isinstance(e.get("artifactId"), str)
            ],
            key=lambda x: x["artifactId"],
        ),
    }

    annotations_artifact = {
        "generatedAt": generated_at,
        "governanceFacing": True,
        "nonCanonical": True,
        "annotations": sorted(constitutional_annotations, key=lambda x: x["artifactId"]),
    }

    watch_entries = []
    for rec in recs:
        artifact_id = rec.get("artifactId")
        if not isinstance(artifact_id, str):
            continue
        action = str(rec.get("targetPublisherAction", "watch")).lower().strip()
        if action not in {"watch", "docket", "freeze-recommended"}:
            action = "watch"
        watch_entries.append(
            {
                "artifactId": artifact_id,
                "watchStatus": action,
                "constitutionalStatus": rec.get("constitutionalStatus", "watch"),
                "humanReviewFlag": bool(rec.get("humanReviewFlag", False)),
                "reason": rec.get("reason", ""),
                "linkedTargetIds": sorted([t for t in as_list(rec.get("linkedTargetIds")) if isinstance(t, str)]),
            }
        )

    governance_failure_watchlist = {
        "generatedAt": generated_at,
        "nonCanonical": True,
        "governanceFacing": True,
        "entries": sorted(watch_entries, key=lambda x: x["artifactId"]),
    }

    return constitutional_status, continuity_mode_index, annotations_artifact, governance_failure_watchlist


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--constitutional-audit", type=Path, default=Path("bridge/constitutional_audit.json"))
    parser.add_argument(
        "--constitutional-recommendations", type=Path, default=Path("bridge/constitutional_recommendations.json")
    )
    parser.add_argument(
        "--continuity-mode-assessment", type=Path, default=Path("bridge/continuity_mode_assessment.json")
    )
    parser.add_argument("--out-constitutional-status", type=Path, default=Path("registry/constitutional_status.json"))
    parser.add_argument("--out-continuity-mode-index", type=Path, default=Path("registry/continuity_mode_index.json"))
    parser.add_argument(
        "--out-constitutional-annotations", type=Path, default=Path("registry/constitutional_annotations.json")
    )
    parser.add_argument(
        "--out-governance-failure-watchlist", type=Path, default=Path("registry/governance_failure_watchlist.json")
    )
    args = parser.parse_args()

    outputs = build_constitutional_overlays(
        load_json(args.constitutional_audit),
        load_json(args.constitutional_recommendations),
        load_json(args.continuity_mode_assessment),
    )

    args.out_constitutional_status.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_continuity_mode_index.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_constitutional_annotations.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_governance_failure_watchlist.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote constitutional status: {args.out_constitutional_status}")
    print(f"[OK] Wrote continuity mode index: {args.out_continuity_mode_index}")
    print(f"[OK] Wrote constitutional annotations: {args.out_constitutional_annotations}")
    print(f"[OK] Wrote governance failure watchlist: {args.out_governance_failure_watchlist}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
