from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python" / "src"))

from atlas.triadic.governed_posture import GovernedPostureError, assign_governed_posture


def write_json(path: Path, value: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_run(root: Path, disposition: str = "PASS") -> Path:
    run_id = "run-fixed"
    (root / "grounding").mkdir(parents=True)
    (root / "grounding" / "segments.jsonl").write_text("{}\n", encoding="utf-8")
    manifest = write_json(root / "grounding" / "manifest.json", {"run_id": run_id, "producer_repository": "pdxvoiceteacher/CoherenceLattice"})
    candidate = write_json(root / "candidate_packet.json", {"run_id": run_id, "producer_repository": "pdxvoiceteacher/CoherenceLattice", "grounding_manifest_sha256": manifest, "answer": "Bounded answer", "claims": ["Claim"], "cited_source_passages": ["Passage"], "uncertainty": "partial", "model_identity": "local", "local_model_digest": "abc"})
    sophia = write_json(root / "sophia_audit_packet.json", {"run_id": run_id, "producer_repository": "pdxvoiceteacher/Sophia", "disposition": disposition, "candidate_sha256": candidate, "grounding_manifest_sha256": manifest, "reason_codes": ["reviewed"]})
    write_json(root / "request.json", {"run_id": run_id, "producer_repository": "pdxvoiceteacher/Sonya", "logical_time": 7, "candidate_sha256": candidate, "sophia_packet_sha256": sophia, "question": "Question", "source_identity": "source", "source_digest": "digest"})
    return root


def test_postures_and_review_are_deterministic_and_bounded(tmp_path: Path):
    expected = {"PASS": ("retain_for_human_review", "publication_blocked_pending_human_review"), "HOLD": ("quarantine", "do_not_publish"), "REJECT": ("rejected", "do_not_publish")}
    for disposition, pair in expected.items():
        root = make_run(tmp_path / disposition, disposition)
        packet = assign_governed_posture(root)
        assert (packet["retention_posture"], packet["publication_posture"]) == pair
        assert all(packet[key] is False for key in ("memory_write_performed", "publication_performed", "doi_mutated", "crossref_deposit_performed"))
        review = (root / "final_review.html").read_text(encoding="utf-8")
        for text in ("Question", "Bounded answer", "Sophia disposition", "No memory write", "Human decision: <strong>PENDING</strong>"):
            assert text in review
        before = (root / "atlas_posture_packet.json").read_bytes(), (root / "final_review.html").read_bytes()
        assign_governed_posture(root)
        assert before == ((root / "atlas_posture_packet.json").read_bytes(), (root / "final_review.html").read_bytes())


def test_missing_or_altered_sophia_and_authority_fail_closed(tmp_path: Path):
    root = make_run(tmp_path)
    (root / "sophia_audit_packet.json").unlink()
    with pytest.raises(GovernedPostureError):
        assign_governed_posture(root)
    root = make_run(tmp_path / "altered")
    packet = json.loads((root / "sophia_audit_packet.json").read_text())
    packet["candidate_sha256"] = "0" * 64
    write_json(root / "sophia_audit_packet.json", packet)
    with pytest.raises(GovernedPostureError):
        assign_governed_posture(root)
    root = make_run(tmp_path / "authority")
    packet = json.loads((root / "candidate_packet.json").read_text())
    packet["truth_certified"] = True
    write_json(root / "candidate_packet.json", packet)
    with pytest.raises(GovernedPostureError):
        assign_governed_posture(root)
