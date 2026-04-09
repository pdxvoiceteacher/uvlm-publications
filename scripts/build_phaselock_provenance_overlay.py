#!/usr/bin/env python3
"""Build Atlas phaselock provenance dashboard from triadic bridge artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_INPUTS = {
    "coherence_drift_map": Path("bridge/coherence_drift_map.json"),
    "triadic_run_manifest": Path("bridge/triadic_run_manifest.json"),
    "grounding_policy": Path("bridge/grounding_policy.json"),
    "source_evidence_packet": Path("bridge/source_evidence_packet.json"),
}

OPTIONAL_INPUTS = {
    "attention_updates": Path("bridge/attention_updates.json"),
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_node_ids(drift: dict[str, Any], evidence: dict[str, Any]) -> set[str]:
    node_ids: set[str] = set()

    for key in ("nodes", "entries", "concepts", "records"):
        if isinstance(drift.get(key), list):
            for item in drift[key]:
                if isinstance(item, dict):
                    nid = item.get("node_id") or item.get("nodeId") or item.get("id")
                    if nid:
                        node_ids.add(str(nid))

    by_node = evidence.get("by_node") if isinstance(evidence, dict) else None
    if isinstance(by_node, dict):
        node_ids.update(str(k) for k in by_node.keys())

    bundles = evidence.get("bundles") if isinstance(evidence, dict) else None
    if isinstance(bundles, list):
        for item in bundles:
            if isinstance(item, dict):
                nid = item.get("node_id") or item.get("nodeId") or item.get("id")
                if nid:
                    node_ids.add(str(nid))

    return node_ids


def _extract_drift_node_map(drift: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for key in ("nodes", "entries", "concepts", "records"):
        items = drift.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            nid = item.get("node_id") or item.get("nodeId") or item.get("id")
            if nid:
                out[str(nid)] = item
    return out


def _extract_evidence_by_node(evidence: dict[str, Any]) -> dict[str, dict[str, Any]]:
    by_node = evidence.get("by_node")
    if isinstance(by_node, dict):
        return {str(k): v for k, v in by_node.items() if isinstance(v, dict)}

    out: dict[str, dict[str, Any]] = {}
    bundles = evidence.get("bundles")
    if isinstance(bundles, list):
        for item in bundles:
            if not isinstance(item, dict):
                continue
            nid = item.get("node_id") or item.get("nodeId") or item.get("id")
            if not nid:
                continue
            sid = str(nid)
            prev = out.setdefault(sid, {"bundle_count": 0, "citation_count": 0})
            prev["bundle_count"] = int(prev.get("bundle_count", 0)) + 1
            prev["citation_count"] = int(prev.get("citation_count", 0)) + int(item.get("citation_count", 0) or 0)
            prev["grounded"] = bool(item.get("grounded", prev.get("grounded", False)))
            prev["audited"] = bool(item.get("audited", prev.get("audited", False)))
    return out


def build_dashboard(
    drift: dict[str, Any],
    run_manifest: dict[str, Any],
    grounding_policy: dict[str, Any],
    source_evidence_packet: dict[str, Any],
    attention_updates: dict[str, Any] | None,
) -> dict[str, Any]:
    node_ids = _extract_node_ids(drift, source_evidence_packet)
    drift_nodes = _extract_drift_node_map(drift)
    evidence_by_node = _extract_evidence_by_node(source_evidence_packet)

    warnings: list[str] = []
    if attention_updates is None:
        warnings.append("attention_updates_missing_bounded_warning")

    run_hash = (
        run_manifest.get("run_hash")
        or run_manifest.get("canonical_run_hash")
        or run_manifest.get("id")
    )

    source_first_suppressed = bool(
        grounding_policy.get("source_first_clarification_suppressed")
        or grounding_policy.get("clarification", {}).get("source_first_suppressed")
    )

    node_dashboard: dict[str, dict[str, Any]] = {}
    for node_id in sorted(node_ids):
        drift_row = drift_nodes.get(node_id, {})
        ev = evidence_by_node.get(node_id, {})

        citation_count = int(ev.get("citation_count", ev.get("citations", 0) or 0) or 0)
        bundle_count = int(ev.get("bundle_count", ev.get("bundles", 0) or 0) or 0)
        grounded = bool(ev.get("grounded", citation_count > 0))
        audited = bool(ev.get("audited", source_evidence_packet.get("audited", False)))

        node_dashboard[node_id] = {
            "node_id": node_id,
            "grounded": grounded,
            "citation_count": citation_count,
            "audited": audited,
            "bundle_count": bundle_count,
            "source_first_clarification_suppressed": source_first_suppressed,
            "canonical_run_hash": run_hash,
            "canonical_formal_drift": drift_row.get("drift_score"),
            "attention_warning": attention_updates is None,
            "publisher_truth_origin": "external_canonical_inputs_only",
        }

    return {
        "schema": "atlas.phaselock.provenance.v1",
        "activityMismatchScore_semantics": "publisher_local_ui_only_non_canonical",
        "canonical_truth_origin": "coherencelattice_and_sophia",
        "warnings": warnings,
        "inputs": {
            "required": {k: str(v) for k, v in REQUIRED_INPUTS.items()},
            "optional": {k: str(v) for k, v in OPTIONAL_INPUTS.items()},
        },
        "nodes": node_dashboard,
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--coherence-drift-map", type=Path, default=REQUIRED_INPUTS["coherence_drift_map"])
    p.add_argument("--triadic-run-manifest", type=Path, default=REQUIRED_INPUTS["triadic_run_manifest"])
    p.add_argument("--grounding-policy", type=Path, default=REQUIRED_INPUTS["grounding_policy"])
    p.add_argument("--source-evidence-packet", type=Path, default=REQUIRED_INPUTS["source_evidence_packet"])
    p.add_argument("--attention-updates", type=Path, default=OPTIONAL_INPUTS["attention_updates"])
    p.add_argument("--out-dashboard", type=Path, default=Path("registry/phaselock_provenance_dashboard.json"))
    return p.parse_args()


def main() -> int:
    args = parse_args()

    drift = load_json(args.coherence_drift_map)
    run_manifest = load_json(args.triadic_run_manifest)
    grounding_policy = load_json(args.grounding_policy)
    source_evidence = load_json(args.source_evidence_packet)

    attention = None
    if args.attention_updates.exists():
        attention = load_json(args.attention_updates)

    dashboard = build_dashboard(drift, run_manifest, grounding_policy, source_evidence, attention)
    args.out_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_dashboard.write_text(json.dumps(dashboard, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[OK] Wrote phaselock provenance dashboard: {args.out_dashboard}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
