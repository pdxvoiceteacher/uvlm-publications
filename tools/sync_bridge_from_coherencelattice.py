#!/usr/bin/env python3
"""Sync selected CoherenceLattice bridge artifacts into this repository's bridge/ folder."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

FILES_TO_SYNC = [
    'phase_lineage_registry.json',
    'coherence_memory_trace.json',
    'civilizational_memory_map.json',
    'knowledge_river_map.json',
    'corridor_braiding_report.json',
    'tributary_support_registry.json',
    'river_capture_risk_report.json',
    'civilizational_delta_map.json',
    'rupture_map.json',
    'agent_telemetry_event_map.json',
    'ai_guidance.json',
    'navigation_state.json',
    # New lens/audit artifacts (advisory-only)
    'lan01_dataset_summary.json',
    'lan01_lens_report.json',
    'lan01_corridor_series_lens_adjusted.json',
]


def sync_bridge(coherencelattice_root: Path, repo_root: Path) -> int:
    source_bridge = coherencelattice_root / 'bridge'
    destination_bridge = repo_root / 'bridge'
    destination_bridge.mkdir(parents=True, exist_ok=True)

    copied = 0
    for filename in FILES_TO_SYNC:
        src = source_bridge / filename
        dst = destination_bridge / filename
        if not src.exists():
            print(f'[skip] missing {src}')
            continue
        shutil.copy2(src, dst)
        copied += 1
        print(f'[copy] {src} -> {dst}')

    print(f'Copied {copied} artifacts.')
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--coherencelattice-root', type=Path, required=True)
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    sync_bridge(args.coherencelattice_root, args.repo_root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
