#!/usr/bin/env python3
"""Build Publisher memory-facing Sonya artifacts from Sophia-audited decisions."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

CANONICAL_ACTIONS = {
    "store": "stored",
    "promote": "promoted",
    "observe": "observed",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_sonya_memory_artifacts(
    sonya_audit: dict[str, Any], sonya_decisions: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits_by_id = {
        item.get("inputId"): item
        for item in sonya_audit.get("audits", [])
        if isinstance(item, dict) and isinstance(item.get("inputId"), str)
    }

    canonical_entries: list[dict[str, Any]] = []
    annotations: list[dict[str, Any]] = []
    attention_candidates: list[dict[str, Any]] = []
    pending_review: list[dict[str, Any]] = []

    for decision in sorted(
        [d for d in sonya_decisions.get("decisions", []) if isinstance(d, dict) and isinstance(d.get("inputId"), str)],
        key=lambda d: d["inputId"],
    ):
        input_id = decision["inputId"]
        action = str(decision.get("targetPublisherAction", "")).strip().lower()
        decision_status = str(decision.get("auditStatus", "")).strip().lower()
        audit_status = str(audits_by_id.get(input_id, {}).get("auditStatus", decision_status)).strip().lower()
        linked_concepts = sorted([c for c in decision.get("suggestedConceptTargets", []) if isinstance(c, str)])

        is_canonical = action in CANONICAL_ACTIONS and audit_status == "admit" and decision_status == "admit"

        if is_canonical:
            stored_status = CANONICAL_ACTIONS[action]
            canonical_entries.append(
                {
                    "inputId": input_id,
                    "status": stored_status,
                    "sourceAuditStatus": audit_status,
                    "sourceAction": action,
                    "linkedConceptIds": linked_concepts,
                    "storedAt": generated_at,
                }
            )
            annotations.append(
                {
                    "inputId": input_id,
                    "status": stored_status,
                    "explanation": decision.get("explanation", ""),
                    "governingRule": decision.get("governingRule"),
                    "coherenceScore": decision.get("coherenceScore"),
                    "riskScore": decision.get("riskScore"),
                }
            )
            attention_candidates.append(
                {
                    "inputId": input_id,
                    "status": stored_status,
                    "conceptTargets": linked_concepts,
                    "attentionWeight": round(float(decision.get("coherenceScore", 0.0)), 4),
                    "reason": decision.get("explanation", ""),
                }
            )
            continue

        if decision_status == "defer" or action == "defer":
            pending_review.append(
                {
                    "inputId": input_id,
                    "status": "pending-review",
                    "sourceAuditStatus": audit_status or decision_status,
                    "targetPublisherAction": action or "defer",
                    "linkedConceptIds": linked_concepts,
                    "explanation": decision.get("explanation", ""),
                    "nonCanonical": True,
                }
            )

    sonya_memory_index = {
        "generatedAt": generated_at,
        "entries": canonical_entries,
    }
    sonya_memory_annotations = {
        "generatedAt": generated_at,
        "annotations": annotations,
    }
    sonya_attention_candidates = {
        "generatedAt": generated_at,
        "candidates": attention_candidates,
    }
    sonya_pending_review = {
        "generatedAt": generated_at,
        "nonCanonical": True,
        "entries": pending_review,
    }

    return sonya_memory_index, sonya_memory_annotations, sonya_attention_candidates, sonya_pending_review


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sonya-audit", type=Path, default=Path("bridge/sonya_audit.json"))
    parser.add_argument("--sonya-decisions", type=Path, default=Path("bridge/sonya_admission_decisions.json"))
    parser.add_argument("--out-memory-index", type=Path, default=Path("registry/sonya_memory_index.json"))
    parser.add_argument("--out-memory-annotations", type=Path, default=Path("registry/sonya_memory_annotations.json"))
    parser.add_argument("--out-attention-candidates", type=Path, default=Path("registry/sonya_attention_candidates.json"))
    parser.add_argument("--out-pending-review", type=Path, default=Path("registry/sonya_pending_review.json"))
    args = parser.parse_args()

    sonya_audit = load_json(args.sonya_audit)
    sonya_decisions = load_json(args.sonya_decisions)

    memory_index, memory_annotations, attention_candidates, pending_review = build_sonya_memory_artifacts(
        sonya_audit, sonya_decisions
    )

    args.out_memory_index.write_text(json.dumps(memory_index, indent=2) + "\n", encoding="utf-8")
    args.out_memory_annotations.write_text(json.dumps(memory_annotations, indent=2) + "\n", encoding="utf-8")
    args.out_attention_candidates.write_text(json.dumps(attention_candidates, indent=2) + "\n", encoding="utf-8")
    args.out_pending_review.write_text(json.dumps(pending_review, indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote Sonya memory index: {args.out_memory_index}")
    print(f"[OK] Wrote Sonya memory annotations: {args.out_memory_annotations}")
    print(f"[OK] Wrote Sonya attention candidates: {args.out_attention_candidates}")
    print(f"[OK] Wrote Sonya pending review (non-canonical): {args.out_pending_review}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
