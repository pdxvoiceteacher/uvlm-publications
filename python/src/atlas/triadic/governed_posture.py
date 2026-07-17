"""Bounded Atlas posture assignment and offline human-review rendering."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

PRODUCER = "pdxvoiceteacher/uvlm-publications"
SIDE_EFFECT_FLAGS = {
    "memory_write_performed": False, "prior_canonized": False,
    "publication_performed": False, "doi_mutated": False,
    "crossref_deposit_performed": False, "catalog_mutated": False,
    "knowledge_graph_mutated": False, "pmr_write_performed": False,
    "deployment_authorized": False, "truth_certified": False,
}


class GovernedPostureError(ValueError):
    """Raised when an input run cannot support a bounded Atlas posture."""


def _read(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise GovernedPostureError(f"unsafe or missing artifact: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise GovernedPostureError(f"invalid JSON: {path}") from error
    if not isinstance(value, dict):
        raise GovernedPostureError(f"artifact must be an object: {path}")
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _value(payload: dict[str, Any], *names: str) -> Any:
    for name in names:
        if payload.get(name) not in (None, ""):
            return payload[name]
    return None


def _require_equal(run_id: str, label: str, payload: dict[str, Any]) -> None:
    if _value(payload, "run_id", "runId") != run_id:
        raise GovernedPostureError(f"{label} run_id mismatch")


def _expected_hash(payload: dict[str, Any], *names: str) -> str | None:
    value = _value(payload, *names)
    if isinstance(value, str):
        return value
    parents = payload.get("parent_hashes")
    if isinstance(parents, dict):
        for name in names:
            if isinstance(parents.get(name), str):
                return parents[name]
    return None


def _validate_hash(payload: dict[str, Any], actual: str, label: str, *names: str) -> None:
    expected = _expected_hash(payload, *names)
    if expected is not None and expected != actual:
        raise GovernedPostureError(f"{label} hash mismatch")


def _walk(value: Any, key: str = "") -> None:
    lower = key.lower()
    if any(token in lower for token in ("chain_of_thought", "private_reasoning", "hidden_reasoning")):
        raise GovernedPostureError("private reasoning is prohibited")
    if isinstance(value, dict):
        for child_key, child in value.items():
            child_lower = str(child_key).lower()
            if child is True and any(token in child_lower for token in (
                "memory_write", "canonized", "publication_performed", "doi_mutated",
                "crossref_deposit", "catalog_mutated", "knowledge_graph_mutated",
                "deployment_authorized", "truth_certified", "final_decision",
            )):
                raise GovernedPostureError(f"authority field must not be true: {child_key}")
            _walk(child, str(child_key))
    elif isinstance(value, list):
        for child in value:
            _walk(child, key)


def _producer(payload: dict[str, Any], label: str, expected: str | None = None) -> str:
    producer = _value(payload, "producer_repository", "repository", "producer_repo")
    if not isinstance(producer, str) or not producer:
        raise GovernedPostureError(f"{label} producer repository missing")
    if expected and producer != expected:
        raise GovernedPostureError(f"{label} producer repository mismatch")
    return producer


def _atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=path.parent, delete=False) as temp:
        temp.write(content)
        name = temp.name
    os.replace(name, path)


def _text(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def _review_html(request: dict[str, Any], candidate: dict[str, Any], sophia: dict[str, Any], posture: dict[str, Any]) -> str:
    claims = _value(candidate, "claims", "claim_list") or []
    if not isinstance(claims, list):
        claims = [claims]
    sources = _value(candidate, "cited_source_passages", "source_passages", "evidence") or []
    if not isinstance(sources, list):
        sources = [sources]
    items = "".join(f"<li>{_text(item)}</li>" for item in claims)
    evidence = "".join(f"<li>{_text(item)}</li>" for item in sources)
    disposition = posture["sophia_disposition"]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Atlas governed review</title>
<style>body{{font-family:system-ui,sans-serif;max-width:70rem;margin:2rem auto;line-height:1.5}} .notice{{border-left:4px solid #555;padding:.5rem 1rem}} code{{overflow-wrap:anywhere}}</style></head>
<body><h1>Atlas governed human review</h1>
<p><strong>Human question:</strong> {_text(_value(request, "question", "human_question", "prompt"))}</p>
<p><strong>Source identity and source digest:</strong> {_text(_value(request, "source_identity", "source_id"))} / <code>{_text(_value(request, "source_digest", "source_sha256"))}</code></p>
<p><strong>Candidate answer:</strong> {_text(_value(candidate, "answer", "candidate_answer", "response"))}</p>
<h2>Claims</h2><ul>{items}</ul><h2>Cited source passages</h2><ul>{evidence}</ul>
<p><strong>Unsupported or partial evidence markers:</strong> {_text(_value(candidate, "unsupported_claims", "partial_evidence", "uncertainty"))}</p>
<p><strong>Model identity and local-model digest:</strong> {_text(_value(candidate, "model_identity", "model_id"))} / <code>{_text(_value(candidate, "local_model_digest", "model_digest"))}</code></p>
<p><strong>Explicit candidate uncertainty:</strong> {_text(_value(candidate, "uncertainty", "candidate_uncertainty"))}</p>
<p><strong>Sophia disposition:</strong> {_text(disposition)}</p><p><strong>Sophia reason codes:</strong> {_text(_value(sophia, "reason_codes", "reasons"))}</p>
<p><strong>Atlas retention posture:</strong> {_text(posture["retention_posture"])}</p><p><strong>Atlas publication posture:</strong> {_text(posture["publication_posture"])}</p>
<div class="notice">No memory write. No publication. No truth certification. Human decision: <strong>PENDING</strong>.</div>
<p>Human options (descriptive only): accept for personal use; request revision; reject; export; discard.</p>
</body></html>"""


def assign_governed_posture(run_root: str | Path) -> dict[str, Any]:
    """Validate a captured run, then atomically emit bounded posture and review files."""
    root = Path(run_root).resolve()
    if not root.is_absolute() or not root.is_dir():
        raise GovernedPostureError("run_root must be an existing absolute directory")
    paths = {
        "request": root / "request.json", "manifest": root / "grounding" / "manifest.json",
        "segments": root / "grounding" / "segments.jsonl", "candidate": root / "candidate_packet.json",
        "sophia": root / "sophia_audit_packet.json",
    }
    if not paths["segments"].is_file() or paths["segments"].is_symlink():
        raise GovernedPostureError("unsafe or missing grounding segments")
    request, manifest, candidate, sophia = (_read(paths[key]) for key in ("request", "manifest", "candidate", "sophia"))
    run_id = _value(request, "run_id", "runId")
    if not isinstance(run_id, str) or not run_id:
        raise GovernedPostureError("request run_id missing")
    for label, packet in (("manifest", manifest), ("candidate", candidate), ("Sophia", sophia)):
        _require_equal(run_id, label, packet)
        _walk(packet)
    _walk(request)
    _producer(request, "request")
    _producer(manifest, "manifest", "pdxvoiceteacher/CoherenceLattice")
    _producer(candidate, "candidate", "pdxvoiceteacher/CoherenceLattice")
    _producer(sophia, "Sophia", "pdxvoiceteacher/Sophia")
    candidate_hash, sophia_hash, manifest_hash = _digest(paths["candidate"]), _digest(paths["sophia"]), _digest(paths["manifest"])
    _validate_hash(sophia, candidate_hash, "candidate", "candidate_sha256", "candidate_packet_sha256")
    _validate_hash(sophia, manifest_hash, "grounding manifest", "grounding_manifest_sha256", "manifest_sha256")
    _validate_hash(candidate, manifest_hash, "grounding manifest", "grounding_manifest_sha256", "manifest_sha256")
    _validate_hash(request, candidate_hash, "candidate", "candidate_sha256", "candidate_packet_sha256")
    _validate_hash(request, sophia_hash, "Sophia", "sophia_packet_sha256", "sophia_audit_packet_sha256")
    disposition = _value(sophia, "disposition", "audit_disposition", "status")
    if disposition not in {"PASS", "HOLD", "REJECT"}:
        raise GovernedPostureError("Sophia disposition missing or invalid")
    retention, publication = {"PASS": ("retain_for_human_review", "publication_blocked_pending_human_review"), "HOLD": ("quarantine", "do_not_publish"), "REJECT": ("rejected", "do_not_publish")}[disposition]
    logical_time = _value(request, "logical_time", "logicalTime")
    if logical_time is None:
        raise GovernedPostureError("logical_time missing")
    posture: dict[str, Any] = {
        "schema_id": "uvlm.atlas.posture_packet.v1", "schema_version": "1.0",
        "packet_type": "atlas_posture_packet", "run_id": run_id, "logical_time": logical_time,
        "producer": {"repository": PRODUCER, "commit": _value(request, "atlas_commit") or "unknown", "clean_tree": True, "cli": "atlas.triadic.governed_posture", "version": "1.0"},
        "candidate_sha256": candidate_hash, "sophia_packet_sha256": sophia_hash,
        "parent_hashes": {"request.json": _digest(paths["request"]), "grounding/manifest.json": manifest_hash, "candidate_packet.json": candidate_hash, "sophia_audit_packet.json": sophia_hash},
        "sophia_disposition": disposition, "retention_posture": retention, "publication_posture": publication,
        "reason_codes": list(_value(sophia, "reason_codes", "reasons") or []), "expiry_posture": "review_bounded", "revocation_posture": "revocable",
        "requires_human_review": True, "nonauthority": True, "human_decision": "PENDING", **SIDE_EFFECT_FLAGS,
    }
    packet_bytes = (json.dumps(posture, sort_keys=True, indent=2) + "\n").encode()
    review_bytes = _review_html(request, candidate, sophia, posture).encode()
    _atomic(root / "atlas_posture_packet.json", packet_bytes)
    _atomic(root / "final_review.html", review_bytes)
    return posture


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", required=True)
    args = parser.parse_args()
    assign_governed_posture(args.run_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

