#!/usr/bin/env python3
"""Build multimodal donation overlays from Sophia-audited pattern decisions."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

CANONICAL_ACTIONS = {"admit-overlay", "annotate", "surface"}
WATCH_ACTIONS = {"watch", "defer", "escalate-human-review"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def build_multimodal_overlays(
    pattern_donation_audit: dict[str, Any],
    pattern_donation_decisions: dict[str, Any],
    cross_modal_reinforcement_report: dict[str, Any],
    cognitive_monitor_index: dict[str, Any],
    reasoning_threads: dict[str, Any],
    cognitive_watchlist: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits_by_id = {
        item.get("donationId"): item
        for item in as_list(pattern_donation_audit.get("audits"))
        if isinstance(item, dict) and isinstance(item.get("donationId"), str)
    }
    reinforce_by_id = {
        item.get("donationId"): item
        for item in as_list(cross_modal_reinforcement_report.get("reports"))
        if isinstance(item, dict) and isinstance(item.get("donationId"), str)
    }

    # Build target validity set from reasoning/watch overlays so we only annotate known surfaced entities.
    valid_targets: set[str] = set()
    for t in as_list(reasoning_threads.get("threads")):
        if isinstance(t, dict):
            valid_targets.update(cid for cid in as_list(t.get("linkedConceptIds")) if isinstance(cid, str))
    for w in as_list(cognitive_watchlist.get("entries")):
        if isinstance(w, dict):
            valid_targets.update(cid for cid in as_list(w.get("linkedConceptIds")) if isinstance(cid, str))

    # keep read dependency explicit for phase traceability
    _ = cognitive_monitor_index

    canonical_signals: list[dict[str, Any]] = []
    donation_annotations: list[dict[str, Any]] = []
    cross_modal_overlays: list[dict[str, Any]] = []
    donation_watchlist: list[dict[str, Any]] = []

    decisions = [
        d for d in as_list(pattern_donation_decisions.get("decisions"))
        if isinstance(d, dict) and isinstance(d.get("donationId"), str)
    ]

    for decision in sorted(decisions, key=lambda d: d["donationId"]):
        donation_id = decision["donationId"]
        audit = audits_by_id.get(donation_id, {})
        report = reinforce_by_id.get(donation_id, {})

        decision_status = str(decision.get("auditStatus", "")).strip().lower()
        audit_status = str(audit.get("auditStatus", decision_status)).strip().lower()
        action = str(decision.get("targetPublisherAction", "")).strip().lower()
        target_id = decision.get("targetId")
        target_type = decision.get("targetType")

        if not isinstance(target_id, str) or (valid_targets and target_id not in valid_targets):
            # Keep publisher overlays scoped to known surfaced entities.
            continue

        canonical_ok = action in CANONICAL_ACTIONS and decision_status == "admit" and audit_status == "admit"
        watch_ok = action in WATCH_ACTIONS or decision_status in {"watch", "defer"} or audit_status in {"watch", "defer"}

        if canonical_ok:
            canonical_signals.append(
                {
                    "donationId": donation_id,
                    "sourceInputId": decision.get("sourceInputId"),
                    "targetType": target_type,
                    "targetId": target_id,
                    "status": "admit-overlay",
                    "sourceAuditStatus": audit_status,
                    "reinforcementScore": decision.get("reinforcementScore"),
                    "coherenceScore": decision.get("coherenceScore"),
                    "riskScore": decision.get("riskScore"),
                    "updatedAt": generated_at,
                }
            )
            donation_annotations.append(
                {
                    "donationId": donation_id,
                    "targetId": target_id,
                    "explanation": decision.get("explanation", audit.get("explanation", "")),
                    "governingRule": audit.get("governingRule"),
                    "reinforcementStatus": report.get("reinforcementStatus", "reinforced"),
                    "monitorFlags": sorted([m for m in as_list(report.get("monitorFlags")) if isinstance(m, str)]),
                }
            )
            cross_modal_overlays.append(
                {
                    "donationId": donation_id,
                    "targetId": target_id,
                    "reinforcementStatus": report.get("reinforcementStatus", "reinforced"),
                    "reinforcementTrend": report.get("reinforcementTrend", "stable"),
                    "reinforcementScore": decision.get("reinforcementScore"),
                }
            )
            continue

        if watch_ok:
            donation_watchlist.append(
                {
                    "donationId": donation_id,
                    "targetId": target_id,
                    "targetType": target_type,
                    "observational": True,
                    "nonCanonical": True,
                    "watchStatus": action if action in WATCH_ACTIONS else (audit_status or decision_status or "watch"),
                    "auditStatus": audit_status or decision_status,
                    "reinforcementStatus": report.get("reinforcementStatus", "watch"),
                    "reinforcementTrend": report.get("reinforcementTrend", "unknown"),
                    "explanation": decision.get("explanation", audit.get("explanation", "")),
                }
            )

    multimodal_signal_index = {
        "generatedAt": generated_at,
        "signals": canonical_signals,
    }
    pattern_donation_annotations = {
        "generatedAt": generated_at,
        "annotations": donation_annotations,
    }
    cross_modal_attention_overlays = {
        "generatedAt": generated_at,
        "overlays": cross_modal_overlays,
    }
    pattern_donation_watchlist = {
        "generatedAt": generated_at,
        "nonCanonical": True,
        "entries": donation_watchlist,
    }

    return (
        multimodal_signal_index,
        pattern_donation_annotations,
        cross_modal_attention_overlays,
        pattern_donation_watchlist,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern-donation-audit", type=Path, default=Path("bridge/pattern_donation_audit.json"))
    parser.add_argument("--pattern-donation-decisions", type=Path, default=Path("bridge/pattern_donation_decisions.json"))
    parser.add_argument(
        "--cross-modal-reinforcement-report", type=Path, default=Path("bridge/cross_modal_reinforcement_report.json")
    )
    parser.add_argument("--cognitive-monitor-index", type=Path, default=Path("registry/cognitive_monitor_index.json"))
    parser.add_argument("--reasoning-threads", type=Path, default=Path("registry/reasoning_threads.json"))
    parser.add_argument("--cognitive-watchlist", type=Path, default=Path("registry/cognitive_watchlist.json"))
    parser.add_argument("--out-multimodal-signal-index", type=Path, default=Path("registry/multimodal_signal_index.json"))
    parser.add_argument(
        "--out-pattern-donation-annotations", type=Path, default=Path("registry/pattern_donation_annotations.json")
    )
    parser.add_argument(
        "--out-cross-modal-attention-overlays", type=Path, default=Path("registry/cross_modal_attention_overlays.json")
    )
    parser.add_argument("--out-pattern-donation-watchlist", type=Path, default=Path("registry/pattern_donation_watchlist.json"))
    args = parser.parse_args()

    outputs = build_multimodal_overlays(
        load_json(args.pattern_donation_audit),
        load_json(args.pattern_donation_decisions),
        load_json(args.cross_modal_reinforcement_report),
        load_json(args.cognitive_monitor_index),
        load_json(args.reasoning_threads),
        load_json(args.cognitive_watchlist),
    )

    args.out_multimodal_signal_index.write_text(json.dumps(outputs[0], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_donation_annotations.write_text(json.dumps(outputs[1], indent=2) + "\n", encoding="utf-8")
    args.out_cross_modal_attention_overlays.write_text(json.dumps(outputs[2], indent=2) + "\n", encoding="utf-8")
    args.out_pattern_donation_watchlist.write_text(json.dumps(outputs[3], indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote multimodal signal index: {args.out_multimodal_signal_index}")
    print(f"[OK] Wrote pattern donation annotations: {args.out_pattern_donation_annotations}")
    print(f"[OK] Wrote cross-modal attention overlays: {args.out_cross_modal_attention_overlays}")
    print(f"[OK] Wrote pattern donation watchlist (non-canonical): {args.out_pattern_donation_watchlist}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
