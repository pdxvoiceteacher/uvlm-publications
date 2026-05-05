import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python" / "src"))

from atlas.phase6_candidate import build_phase6_memory_candidate_packet


def test_phase6_candidate_is_shadow_only_and_not_authoritative():
    handoff_request = {
        "request_id": "phase6-request-001",
        "artifact_refs": ["handoff-source-a"],
    }
    sophia_adjudication = {
        "adjudication_status": "candidate",
        "truth_certification": True,
        "memory_write_authorized": True,
    }

    packet = build_phase6_memory_candidate_packet(handoff_request, sophia_adjudication)

    assert packet == {
        "schema": "atlas.phase6_memory_candidate.v1",
        "request_id": "phase6-request-001",
        "candidate_status": "shadow_only",
        "allowed_use": "retrieval_candidate",
        "memory_write_authorized": False,
        "reason_codes": [
            "not_truth_certification",
            "human_review_required",
            "cross_domain_validation_pending",
        ],
        "artifact_refs": [],
        "artifact_sha256s": {},
        "guardrails": {
            "not_authoritative_memory": True,
            "does_not_override_source": True,
            "human_review_required": True,
        },
    }


def test_phase6_candidate_uses_nested_sophia_request_id_fallback():
    packet = build_phase6_memory_candidate_packet(
        {"handoff": {"description": "missing request id"}},
        {"packet": {"requestId": "sophia-request-002"}},
    )

    assert packet["request_id"] == "sophia-request-002"
    assert packet["candidate_status"] == "shadow_only"
    assert packet["allowed_use"] == "retrieval_candidate"


def test_phase6_candidate_cli_writes_output_packet(tmp_path):
    handoff_path = tmp_path / "phase6_triadic_handoff_request.json"
    adjudication_path = tmp_path / "phase6_sophia_adjudication_packet.json"
    out_path = tmp_path / "nested" / "phase6_atlas_memory_candidate_packet.json"

    handoff_path.write_text(json.dumps({"request_id": "phase6-cli-003"}), encoding="utf-8")
    adjudication_path.write_text(json.dumps({"status": "adjudicated"}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "atlas.phase6_candidate",
            "--handoff-request",
            str(handoff_path),
            "--sophia-adjudication",
            str(adjudication_path),
            "--out",
            str(out_path),
        ],
        text=True,
        capture_output=True,
        check=False,
        env={
            **os.environ,
            "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "python" / "src"),
        },
    )

    assert result.returncode == 0, result.stdout + result.stderr
    packet = json.loads(out_path.read_text(encoding="utf-8"))
    assert packet["schema"] == "atlas.phase6_memory_candidate.v1"
    assert packet["request_id"] == "phase6-cli-003"
    assert packet["memory_write_authorized"] is False
    assert packet["guardrails"]["not_authoritative_memory"] is True
