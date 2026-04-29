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


def _enforce_prior_injection_guard(packet: dict) -> dict:
    decisions = packet.get("prior_injection_decision", [])
    trace = packet.get("prior_injection_trace", [])
    if not isinstance(trace, list):
        trace = []
    if not isinstance(decisions, list):
        return packet

    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        scope = decision.get("prior_scope")
        allowed = decision.get("allowed_use")
        should_downgrade = (
            scope == "same_question_source_match"
            or (decision.get("same_source") and decision.get("same_bundle"))
        )
        if should_downgrade and allowed not in {"shadow_only", "context_only"}:
            decision["allowed_use"] = "shadow_only"
            decision["reason"] = "downgraded in atlas api server to prevent same-question same-source prior loop"
            trace.append(f"{decision.get('provenance_hash')}: {decision['reason']}")

    # Keep selected_priors aligned with post-guard decisions while preserving all
    # provenance/scope fields already attached by retrieval.
    selected = packet.get("selected_priors", [])
    if isinstance(selected, list):
        decision_by_hash = {
            d.get("provenance_hash"): d
            for d in decisions
            if isinstance(d, dict) and d.get("provenance_hash")
        }
        for prior in selected:
            if not isinstance(prior, dict):
                continue
            decision = decision_by_hash.get(prior.get("provenance_hash"))
            if not decision:
                continue
            if decision.get("allowed_use") in {"shadow_only", "context_only", "answer_support", "cite_if_verified"}:
                prior["allowed_use"] = decision["allowed_use"]
            if decision.get("reason"):
                prior["retrieval_reason"] = decision["reason"]
    packet["prior_injection_trace"] = trace
    return packet


def _preserve_query_provenance_fields(packet: dict, query: dict) -> dict:
    for key in (
        "run_id",
        "preset",
        "source_id",
        "source_sha256",
        "normalized_sha256",
        "bundle_manifest_path",
        "source_filename",
        "source_kind",
    ):
        if packet.get(key) in (None, "") and query.get(key) not in (None, ""):
            packet[key] = query.get(key)
    return packet


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

    if not query.get("question_integrity_ok", False):
        error_payload = {
            "error": "atlas_query_integrity_failed",
            "reason": query.get("integrity_error", "question_text_failed_integrity"),
            "question_integrity_ok": False,
            "atlas_query_contract_version": query.get("atlas_query_contract_version"),
            "source_id": query.get("source_id"),
            "normalized_sha256": query.get("normalized_sha256"),
        }
        _write_json_file(BRIDGE_ROOT / "atlas_prior_error.json", error_payload)
        return error_payload

    try:
        packet = build_atlas_prior_packet(query)
        packet = _preserve_query_provenance_fields(packet, query)
        packet = _enforce_prior_injection_guard(packet)
    except Exception as e:
        error_payload = {
            "error": "atlas_retrieve_failed",
            "reason": repr(e),
            "query_keys": sorted(list(query.keys())) if isinstance(query, dict) else [],
            "question_integrity_ok": query.get("question_integrity_ok"),
            "atlas_query_contract_version": query.get("atlas_query_contract_version"),
        }
        _write_json_file(BRIDGE_ROOT / "atlas_prior_error.json", error_payload)
        return error_payload

    _write_json_file(ATLAS_PRIOR_PACKET_FILE, packet)
    return packet
