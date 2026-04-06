import json
import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from atlas.agency import adjudicate_candidate, persist_candidate, load_existing_priors
from atlas.retrieval import build_atlas_prior_packet

app = FastAPI(title="Atlas Agency API", version="0.2")


def _resolve_bridge_root() -> Path:
    """
    Resolve the shared triadic bridge root.
    See Sophia for the same contract.
    """
    env = os.getenv("TRIADIC_BRIDGE_ROOT")
    if env:
        return Path(env).expanduser().resolve()

    coh_root = os.getenv("COHERENCE_LATTICE_ROOT")
    if coh_root:
        candidate = (Path(coh_root) / "bridge").expanduser().resolve()
        if candidate.exists():
            return candidate

    repo_root = Path(__file__).resolve().parents[3]  # .../python/src/atlas/api_server.py -> repo root
    sibling = (repo_root.parent / "CoherenceLattice" / "bridge").resolve()
    if sibling.exists():
        return sibling

    raise RuntimeError(
        "Atlas cannot resolve triadic bridge root. "
        "Set TRIADIC_BRIDGE_ROOT to the CoherenceLattice bridge directory."
    )


BRIDGE_ROOT = _resolve_bridge_root()
ATLAS_NOVELTY_CANDIDATE_FILE = BRIDGE_ROOT / "atlas_novelty_candidate.json"
ATLAS_ADJUDICATION_FILE = BRIDGE_ROOT / "atlas_adjudication.json"
ATLAS_PERSISTENCE_RESULT_FILE = BRIDGE_ROOT / "atlas_persistence_result.json"
ATLAS_QUERY_FILE = BRIDGE_ROOT / "atlas_query.json"
ATLAS_PRIOR_PACKET_FILE = BRIDGE_ROOT / "atlas_prior_packet.json"


def _read_json_file(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json_file(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok", "service": "atlas", "bridge_root": str(BRIDGE_ROOT)}


@app.post("/atlas/adjudicate")
def atlas_adjudicate():
    if not ATLAS_NOVELTY_CANDIDATE_FILE.exists():
        return {"error": "atlas_novelty_candidate.json not found"}

    candidate = _read_json_file(ATLAS_NOVELTY_CANDIDATE_FILE)
    adjudication = adjudicate_candidate(candidate)

    _write_json_file(ATLAS_ADJUDICATION_FILE, adjudication)
    return adjudication


@app.post("/atlas/persist")
def atlas_persist():
    if not ATLAS_NOVELTY_CANDIDATE_FILE.exists():
        return {"error": "atlas_novelty_candidate.json not found"}

    candidate = _read_json_file(ATLAS_NOVELTY_CANDIDATE_FILE)
    stored_path = persist_candidate(candidate)

    result = {
        "stored": stored_path is not None,
        "path": stored_path,
    }

    _write_json_file(ATLAS_PERSISTENCE_RESULT_FILE, result)
    return result


@app.get("/atlas/priors")
def atlas_priors():
    return {"atlas_priors": load_existing_priors()}


@app.post("/atlas/retrieve")
def atlas_retrieve():
    if not ATLAS_QUERY_FILE.exists():
        return {"error": "atlas_query.json not found"}

    query = _read_json_file(ATLAS_QUERY_FILE)
    packet = build_atlas_prior_packet(query)

    _write_json_file(ATLAS_PRIOR_PACKET_FILE, packet)
    return packet
