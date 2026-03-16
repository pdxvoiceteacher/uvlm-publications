import json
from pathlib import Path


def write_hb02_corridor_artifact(metrics: dict):
    artifact = {
        "schema": "coherence.hb02_corridor.v1",
        "metrics": metrics,
        "advisory": True,
        "semanticMode": "non-executive",
    }

    path = Path("bridge/hb02_corridor_metrics.json")

    path.parent.mkdir(exist_ok=True)

    with path.open("w") as f:
        json.dump(artifact, f, indent=2)

    return path
