from __future__ import annotations

from typing import Any, Dict


def build_hb02_observatory_card(packet: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read-only public dashboard card for global observatory.
    """

    return {
        "schema": "atlas.hb02.card.v1",
        "title": f"HB-02 / {packet.get('model_name', 'unknown')}",
        "domain": packet.get("domain", "unknown"),
        "task_family": packet.get("task_family", "unknown"),
        "true_coherence": packet.get("true_coherence"),
        "stability": packet.get("stability"),
        "experiment_coherence": packet.get("experiment_coherence"),
        "baseline_literal_preview": packet.get("baseline", {}).get("literal_output", "")[:180],
        "conditioned_literal_preview": packet.get("conditioned", {}).get("literal_output", "")[:180],
        "conditioned_allegory_preview": packet.get("conditioned", {}).get("allegorical_output", "")[:180],
    }


def build_multi_model_dashboard(results):
    return {
        "schema": "atlas.hb02.multi.v1",
        "models": [
            build_hb02_observatory_card(r)
            for r in results
        ],
    }
