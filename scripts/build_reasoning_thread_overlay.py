#!/usr/bin/env python3
"""Build Publisher reasoning-thread overlays from Sophia-audited thread artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

CANONICAL_PUBLISHER_ACTIONS = {"annotate", "store", "promote", "surface"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def build_reasoning_overlays(
    reasoning_audit: dict[str, Any],
    recursive_candidates: dict[str, Any],
    sonya_memory_index: dict[str, Any],
    sonya_memory_annotations: dict[str, Any],
    sonya_attention_candidates: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    generated_at = dt.date.today().isoformat()

    audits_by_thread = {
        item.get("threadId"): item
        for item in _as_list(reasoning_audit.get("audits"))
        if isinstance(item, dict) and isinstance(item.get("threadId"), str)
    }

    admitted_memory_ids = {
        item.get("inputId")
        for item in _as_list(sonya_memory_index.get("entries"))
        if isinstance(item, dict) and isinstance(item.get("inputId"), str)
    }

    attention_by_input = {
        item.get("inputId"): item
        for item in _as_list(sonya_attention_candidates.get("candidates"))
        if isinstance(item, dict) and isinstance(item.get("inputId"), str)
    }

    canonical_threads: list[dict[str, Any]] = []
    annotations: list[dict[str, Any]] = []
    watch_entries: list[dict[str, Any]] = []

    candidates = [
        c for c in _as_list(recursive_candidates.get("candidates"))
        if isinstance(c, dict) and isinstance(c.get("threadId"), str)
    ]

    for candidate in sorted(candidates, key=lambda c: c["threadId"]):
        thread_id = candidate["threadId"]
        action = str(candidate.get("targetPublisherAction", "")).strip().lower()
        candidate_status = str(candidate.get("auditStatus", "")).strip().lower()
        audit_status = str(audits_by_thread.get(thread_id, {}).get("auditStatus", candidate_status)).strip().lower()

        source_input_ids = sorted([sid for sid in _as_list(candidate.get("sourceInputIds")) if isinstance(sid, str)])
        admitted_source_ids = [sid for sid in source_input_ids if sid in admitted_memory_ids]

        linked_concepts = sorted([cid for cid in _as_list(candidate.get("linkedConceptIds")) if isinstance(cid, str)])
        if not linked_concepts:
            recovered: set[str] = set()
            for sid in admitted_source_ids:
                recovered.update(
                    cid for cid in _as_list(attention_by_input.get(sid, {}).get("conceptTargets")) if isinstance(cid, str)
                )
            linked_concepts = sorted(recovered)

        canonical_ok = (
            audit_status == "admit"
            and candidate_status == "admit"
            and action in CANONICAL_PUBLISHER_ACTIONS
            and len(admitted_source_ids) > 0
        )

        if canonical_ok:
            canonical_threads.append(
                {
                    "threadId": thread_id,
                    "status": "admitted-thread",
                    "sourceAuditStatus": audit_status,
                    "targetPublisherAction": action,
                    "sourceInputIds": admitted_source_ids,
                    "linkedConceptIds": linked_concepts,
                    "recursivePotentialScore": candidate.get("recursivePotentialScore"),
                    "coherenceScore": candidate.get("coherenceScore"),
                    "riskScore": candidate.get("riskScore"),
                    "surfacedAt": generated_at,
                }
            )
            annotations.append(
                {
                    "threadId": thread_id,
                    "explanation": candidate.get("explanation", ""),
                    "governingRule": audits_by_thread.get(thread_id, {}).get("governingRule", candidate.get("governingRule")),
                    "cognitiveWatchSignals": sorted(
                        [sig for sig in _as_list(candidate.get("cognitiveWatchSignals")) if isinstance(sig, str)]
                    ),
                    "recursivePotentialScore": candidate.get("recursivePotentialScore"),
                }
            )
            continue

        if audit_status in {"watch", "defer"} or candidate_status in {"watch", "defer"} or action in {"watch", "defer"}:
            watch_entries.append(
                {
                    "threadId": thread_id,
                    "status": "watch",
                    "observational": True,
                    "nonCanonical": True,
                    "sourceAuditStatus": audit_status or candidate_status,
                    "targetPublisherAction": action or "watch",
                    "sourceInputIds": source_input_ids,
                    "linkedConceptIds": linked_concepts,
                    "recursivePotentialScore": candidate.get("recursivePotentialScore"),
                    "cognitiveWatchSignals": sorted(
                        [sig for sig in _as_list(candidate.get("cognitiveWatchSignals")) if isinstance(sig, str)]
                    ),
                    "explanation": candidate.get("explanation", ""),
                }
            )

    reasoning_threads = {
        "generatedAt": generated_at,
        "threads": canonical_threads,
    }
    reasoning_thread_annotations = {
        "generatedAt": generated_at,
        "annotations": annotations,
    }
    cognitive_watchlist = {
        "generatedAt": generated_at,
        "nonCanonical": True,
        "entries": watch_entries,
    }

    return reasoning_threads, reasoning_thread_annotations, cognitive_watchlist


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reasoning-audit", type=Path, default=Path("bridge/reasoning_audit.json"))
    parser.add_argument("--recursive-candidates", type=Path, default=Path("bridge/recursive_reasoning_candidates.json"))
    parser.add_argument("--sonya-memory-index", type=Path, default=Path("registry/sonya_memory_index.json"))
    parser.add_argument("--sonya-memory-annotations", type=Path, default=Path("registry/sonya_memory_annotations.json"))
    parser.add_argument("--sonya-attention-candidates", type=Path, default=Path("registry/sonya_attention_candidates.json"))
    parser.add_argument("--out-reasoning-threads", type=Path, default=Path("registry/reasoning_threads.json"))
    parser.add_argument(
        "--out-reasoning-thread-annotations", type=Path, default=Path("registry/reasoning_thread_annotations.json")
    )
    parser.add_argument("--out-cognitive-watchlist", type=Path, default=Path("registry/cognitive_watchlist.json"))
    args = parser.parse_args()

    reasoning_audit = load_json(args.reasoning_audit)
    recursive_candidates = load_json(args.recursive_candidates)
    sonya_memory_index = load_json(args.sonya_memory_index)
    sonya_memory_annotations = load_json(args.sonya_memory_annotations)
    sonya_attention_candidates = load_json(args.sonya_attention_candidates)

    reasoning_threads, reasoning_thread_annotations, cognitive_watchlist = build_reasoning_overlays(
        reasoning_audit,
        recursive_candidates,
        sonya_memory_index,
        sonya_memory_annotations,
        sonya_attention_candidates,
    )

    args.out_reasoning_threads.write_text(json.dumps(reasoning_threads, indent=2) + "\n", encoding="utf-8")
    args.out_reasoning_thread_annotations.write_text(
        json.dumps(reasoning_thread_annotations, indent=2) + "\n", encoding="utf-8"
    )
    args.out_cognitive_watchlist.write_text(json.dumps(cognitive_watchlist, indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote reasoning threads: {args.out_reasoning_threads}")
    print(f"[OK] Wrote reasoning thread annotations: {args.out_reasoning_thread_annotations}")
    print(f"[OK] Wrote cognitive watchlist (non-canonical): {args.out_cognitive_watchlist}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
