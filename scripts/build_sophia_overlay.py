#!/usr/bin/env python3
"""Build deterministic Sophia memory feedback overlay artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_scores(items: dict[str, float], default: float = 1.0) -> dict[str, float]:
    if not items:
        return {}
    vals = [v for v in items.values() if isinstance(v, (int, float))]
    if not vals:
        return {k: default for k in sorted(items)}
    lo = min(vals)
    hi = max(vals)
    if hi == lo:
        return {k: 1.0 for k in sorted(items)}
    return {k: round((float(items[k]) - lo) / (hi - lo), 4) for k in sorted(items)}


def build_overlay(
    graph: dict[str, Any],
    constellations: dict[str, Any],
    atlas_paths: dict[str, Any],
    coherence_assessment: dict[str, Any],
    recommendations: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    concept_ids = sorted([n["id"] for n in graph.get("nodes", []) if n.get("class") == "concept"])
    constellation_ids = sorted([c.get("id") for c in constellations.get("constellations", []) if isinstance(c, dict)])

    concept_raw: dict[str, float] = {}
    for cid in concept_ids:
        concept_raw[cid] = float(coherence_assessment.get("conceptScores", {}).get(cid, 0.0))

    constellation_raw: dict[str, float] = {}
    for csid in constellation_ids:
        constellation_raw[csid] = float(coherence_assessment.get("constellationScores", {}).get(csid, 0.0))

    path_raw: dict[str, float] = {}
    for p in atlas_paths.get("paths", []):
        if isinstance(p, dict) and isinstance(p.get("id"), str):
            path_raw[p["id"]] = float(recommendations.get("pathPromotions", {}).get(p["id"], 0.0))

    concept_weights = normalize_scores(concept_raw)
    constellation_weights = normalize_scores(constellation_raw)
    path_weights = normalize_scores(path_raw)

    coherence_weights = {
        "generatedAt": dt.date.today().isoformat(),
        "conceptWeights": concept_weights,
        "constellationWeights": constellation_weights,
        "pathWeights": path_weights,
    }

    sophia_annotations = {
        "generatedAt": dt.date.today().isoformat(),
        "conceptAnnotations": {
            cid: {
                "note": coherence_assessment.get("conceptNotes", {}).get(cid, "No Sophia note."),
                "weight": concept_weights.get(cid, 0.0),
            }
            for cid in concept_ids
        },
        "constellationAnnotations": {
            csid: {
                "note": coherence_assessment.get("constellationNotes", {}).get(csid, "No Sophia note."),
                "weight": constellation_weights.get(csid, 0.0),
            }
            for csid in constellation_ids
        },
    }

    attention_ranking = sorted(
        [{"id": cid, "weight": w} for cid, w in concept_weights.items()],
        key=lambda x: (-x["weight"], x["id"]),
    )
    constellation_ranking = sorted(
        [{"id": cid, "weight": w} for cid, w in constellation_weights.items()],
        key=lambda x: (-x["weight"], x["id"]),
    )
    path_ranking = sorted(
        [{"id": pid, "weight": w} for pid, w in path_weights.items()],
        key=lambda x: (-x["weight"], x["id"]),
    )

    sophia_attention_state = {
        "generatedAt": dt.date.today().isoformat(),
        "attention": {
            "concepts": attention_ranking,
            "constellations": constellation_ranking,
            "paths": path_ranking,
        },
    }

    path_lookup = {p["id"]: p for p in atlas_paths.get("paths", []) if isinstance(p, dict) and isinstance(p.get("id"), str)}
    promoted = []
    for entry in path_ranking:
        p = path_lookup.get(entry["id"])
        if not p:
            continue
        promoted.append(
            {
                "id": p["id"],
                "title": p.get("title", p["id"]),
                "promotionWeight": entry["weight"],
                "nodes": sorted(p.get("nodes", [])),
                "reason": recommendations.get("pathReasons", {}).get(p["id"], "Sophia promotion"),
            }
        )

    sophia_paths = {
        "generatedAt": dt.date.today().isoformat(),
        "promotedPaths": promoted,
    }

    return coherence_weights, sophia_annotations, sophia_attention_state, sophia_paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=Path("registry/knowledge_graph.json"))
    parser.add_argument("--constellations", type=Path, default=Path("registry/constellations.json"))
    parser.add_argument("--atlas-paths", type=Path, default=Path("registry/atlas_paths.json"))
    parser.add_argument("--coherence-assessment", type=Path, default=Path("bridge/coherence_assessment.json"))
    parser.add_argument("--sophia-recommendations", type=Path, default=Path("bridge/sophia_recommendations.json"))
    parser.add_argument("--out-coherence-weights", type=Path, default=Path("registry/coherence_weights.json"))
    parser.add_argument("--out-sophia-annotations", type=Path, default=Path("registry/sophia_annotations.json"))
    parser.add_argument("--out-sophia-attention-state", type=Path, default=Path("registry/sophia_attention_state.json"))
    parser.add_argument("--out-sophia-paths", type=Path, default=Path("registry/sophia_paths.json"))
    args = parser.parse_args()

    graph = load_json(args.graph)
    constellations = load_json(args.constellations)
    atlas_paths = load_json(args.atlas_paths)
    coherence_assessment = load_json(args.coherence_assessment)
    recommendations = load_json(args.sophia_recommendations)

    coherence_weights, sophia_annotations, sophia_attention_state, sophia_paths = build_overlay(
        graph, constellations, atlas_paths, coherence_assessment, recommendations
    )

    args.out_coherence_weights.write_text(json.dumps(coherence_weights, indent=2) + "\n", encoding="utf-8")
    args.out_sophia_annotations.write_text(json.dumps(sophia_annotations, indent=2) + "\n", encoding="utf-8")
    args.out_sophia_attention_state.write_text(json.dumps(sophia_attention_state, indent=2) + "\n", encoding="utf-8")
    args.out_sophia_paths.write_text(json.dumps(sophia_paths, indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Wrote overlay: {args.out_coherence_weights}")
    print(f"[OK] Wrote overlay: {args.out_sophia_annotations}")
    print(f"[OK] Wrote overlay: {args.out_sophia_attention_state}")
    print(f"[OK] Wrote overlay: {args.out_sophia_paths}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
