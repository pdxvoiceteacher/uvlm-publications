#!/usr/bin/env python3
"""Build deterministic phaselock provenance dashboard from canonical bridge artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_TRIADIC_RUN_MANIFEST = Path("../CoherenceLattice/bridge/triadic_run_manifest.json")
DEFAULT_GROUNDING_POLICY = Path("../CoherenceLattice/bridge/grounding_policy.json")
DEFAULT_SOURCE_EVIDENCE_PACKET = Path("../CoherenceLattice/bridge/source_evidence_packet.json")
DEFAULT_ATTENTION_UPDATES = Path("../Sophia/bridge/attention_updates.json")
DEFAULT_OUT_DASHBOARD = Path("registry/phaselock_provenance_dashboard.json")

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"Missing required input JSON: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON at {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Expected top-level JSON object at {path}")
    return payload


def _extract_citation_count(source_evidence_packet: dict[str, Any]) -> int:
    total = 0

    by_node = source_evidence_packet.get("by_node")
    if isinstance(by_node, dict):
        for row in by_node.values():
            if isinstance(row, dict):
                total += int(row.get("citation_count", row.get("citations", 0)) or 0)

    bundles = source_evidence_packet.get("bundles")
    if isinstance(bundles, list):
        for row in bundles:
            if isinstance(row, dict):
                total += int(row.get("citation_count", row.get("citations", 0)) or 0)

    if total == 0:
        total = int(source_evidence_packet.get("citation_count", source_evidence_packet.get("citations", 0)) or 0)

    return max(total, 0)


def _extract_grounding_count(source_evidence_packet: dict[str, Any]) -> int:
    grounded = 0

    by_node = source_evidence_packet.get("by_node")
    if isinstance(by_node, dict):
        for row in by_node.values():
            if isinstance(row, dict) and bool(row.get("grounded")):
                grounded += 1

    bundles = source_evidence_packet.get("bundles")
    if isinstance(bundles, list):
        for row in bundles:
            if isinstance(row, dict) and bool(row.get("grounded")):
                grounded += 1

    if grounded == 0 and bool(source_evidence_packet.get("grounded")):
        grounded = 1

    return grounded


def _extract_normalized_sha256s(
    triadic_run_manifest: dict[str, Any],
    source_evidence_packet: dict[str, Any],
) -> list[str]:
    candidates: list[str] = []

    for key in ("normalized_sha256s", "sha256s"):
        value = triadic_run_manifest.get(key)
        if isinstance(value, list):
            candidates.extend(str(v) for v in value)

    for key in ("normalized_sha256s", "sha256s"):
        value = source_evidence_packet.get(key)
        if isinstance(value, list):
            candidates.extend(str(v) for v in value)

    for key in ("sha256", "normalized_sha256"):
        value = triadic_run_manifest.get(key)
        if isinstance(value, str):
            candidates.append(value)
        value = source_evidence_packet.get(key)
        if isinstance(value, str):
            candidates.append(value)

    by_node = source_evidence_packet.get("by_node")
    if isinstance(by_node, dict):
        for row in by_node.values():
            if not isinstance(row, dict):
                continue
            for key in ("sha256", "normalized_sha256"):
                value = row.get(key)
                if isinstance(value, str):
                    candidates.append(value)

    bundles = source_evidence_packet.get("bundles")
    if isinstance(bundles, list):
        for row in bundles:
            if not isinstance(row, dict):
                continue
            for key in ("sha256", "normalized_sha256"):
                value = row.get(key)
                if isinstance(value, str):
                    candidates.append(value)

    normalized = sorted({c.strip().lower() for c in candidates if isinstance(c, str) and _SHA256_RE.match(c.strip().lower())})
    return normalized


def build_dashboard(
    triadic_run_manifest: dict[str, Any],
    grounding_policy: dict[str, Any],
    source_evidence_packet: dict[str, Any],
    attention_updates: dict[str, Any] | None,
) -> dict[str, Any]:
    citation_count = _extract_citation_count(source_evidence_packet)
    grounding_count = _extract_grounding_count(source_evidence_packet)
    grounded = grounding_count > 0 or bool(source_evidence_packet.get("grounded"))

    source_context_mode = grounding_policy.get("source_context_mode", "bundle_compact")
    clarification_state = grounding_policy.get("clarification_state", "source_resolved")

    legacy_alias_projection = True
    if isinstance(attention_updates, dict) and "legacy_alias_projection" in attention_updates:
        legacy_alias_projection = bool(attention_updates.get("legacy_alias_projection"))

    return {
        "grounded": bool(grounded),
        "grounding_count": int(grounding_count),
        "normalized_sha256s": _extract_normalized_sha256s(triadic_run_manifest, source_evidence_packet),
        "citation_count": int(citation_count),
        "citation_ready": bool(citation_count > 0),
        "source_context_mode": str(source_context_mode),
        "clarification_state": str(clarification_state),
        "legacy_alias_projection": bool(legacy_alias_projection),
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--triadic-run-manifest", type=Path, default=DEFAULT_TRIADIC_RUN_MANIFEST)
    p.add_argument("--grounding-policy", type=Path, default=DEFAULT_GROUNDING_POLICY)
    p.add_argument("--source-evidence-packet", type=Path, default=DEFAULT_SOURCE_EVIDENCE_PACKET)
    p.add_argument("--attention-updates", type=Path, default=DEFAULT_ATTENTION_UPDATES)
    p.add_argument("--out-dashboard", type=Path, default=DEFAULT_OUT_DASHBOARD)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    triadic_run_manifest = load_json(args.triadic_run_manifest)
    grounding_policy = load_json(args.grounding_policy)
    source_evidence_packet = load_json(args.source_evidence_packet)

    attention_updates = None
    if args.attention_updates.exists():
        attention_updates = load_json(args.attention_updates)

    dashboard = build_dashboard(
        triadic_run_manifest=triadic_run_manifest,
        grounding_policy=grounding_policy,
        source_evidence_packet=source_evidence_packet,
        attention_updates=attention_updates,
    )

    args.out_dashboard.parent.mkdir(parents=True, exist_ok=True)
    args.out_dashboard.write_text(json.dumps(dashboard, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[OK] Wrote phaselock provenance dashboard: {args.out_dashboard}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
