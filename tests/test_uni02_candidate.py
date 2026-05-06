import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python" / "src"))

from atlas.uni02_candidate import build_uni02_memory_candidate_packet


def test_uni02_candidate_defaults_to_shadow_only_fixture_matrix_candidate():
    packet = build_uni02_memory_candidate_packet(
        {"request_id": "uni02-request-001"},
        {},
    )

    assert packet == {
        "schema": "atlas.uni02_memory_candidate.v1",
        "request_id": "uni02-request-001",
        "candidate_status": "shadow_only",
        "allowed_use": "retrieval_candidate",
        "memory_write_authorized": False,
        "artifact_refs": [],
        "artifact_refs_by_key": {},
        "artifact_sha256s": {},
        "artifact_sha256s_by_key": {},
        "source_posture": {
            "application_portability_status": "passed",
            "cross_domain_validation_status": "partial",
            "universal_claim_status": "not_asserted",
        },
        "reason_codes": [
            "not_truth_certification",
            "human_review_required",
            "source_only_fixture_matrix",
            "cross_domain_validation_partial",
            "not_universal_truth_claim",
        ],
        "guardrails": {
            "not_authoritative_memory": True,
            "does_not_override_source": True,
            "does_not_universalize_tches": True,
            "human_review_required": True,
        },
    }


def test_uni02_candidate_uses_nested_sophia_request_id_fallback():
    packet = build_uni02_memory_candidate_packet(
        {"handoff": {"description": "missing request id"}},
        {"packet": {"requestId": "sophia-uni02-002"}},
    )

    assert packet["request_id"] == "sophia-uni02-002"
    assert packet["candidate_status"] == "shadow_only"
    assert packet["allowed_use"] == "retrieval_candidate"
    assert packet["memory_write_authorized"] is False


def test_uni02_candidate_copies_fixture_matrix_artifact_bindings():
    packet = build_uni02_memory_candidate_packet(
        {
            "request_id": "uni02-request-003",
            "artifact_refs": {
                "fixture_matrix": "artifacts/uni02_fixture_matrix.json",
                "portability_report": "artifacts/uni02_portability_report.json",
            },
            "artifact_sha256s": {
                "fixture_matrix": "1" * 64,
                "portability_report": "2" * 64,
            },
        },
        {},
    )

    assert packet["artifact_refs"] == [
        "artifacts/uni02_fixture_matrix.json",
        "artifacts/uni02_portability_report.json",
    ]
    assert all(isinstance(ref, str) for ref in packet["artifact_refs"])
    assert packet["artifact_refs_by_key"] == {
        "fixture_matrix": "artifacts/uni02_fixture_matrix.json",
        "portability_report": "artifacts/uni02_portability_report.json",
    }
    assert packet["artifact_sha256s"] == {
        "artifacts/uni02_fixture_matrix.json": "1" * 64,
        "artifacts/uni02_portability_report.json": "2" * 64,
    }
    assert packet["artifact_sha256s_by_key"] == {
        "fixture_matrix": "1" * 64,
        "portability_report": "2" * 64,
    }


def test_uni02_candidate_preserves_source_posture_and_blocked_sophia_reason():
    packet = build_uni02_memory_candidate_packet(
        {
            "request_id": "uni02-request-004",
            "source_posture": {
                "application_portability_status": "passed",
                "cross_domain_validation_status": "partial",
                "universal_claim_status": "not_asserted",
            },
        },
        {"memoryWriteAuthorized": False},
    )

    assert packet["source_posture"] == {
        "application_portability_status": "passed",
        "cross_domain_validation_status": "partial",
        "universal_claim_status": "not_asserted",
    }
    assert packet["candidate_status"] == "shadow_only"
    assert packet["memory_write_authorized"] is False
    assert "cross_domain_validation_partial" in packet["reason_codes"]
    assert "not_universal_truth_claim" in packet["reason_codes"]
    assert "authoritative_memory_write_blocked" in packet["reason_codes"]


def test_uni02_candidate_cli_writes_output_packet(tmp_path):
    handoff_path = tmp_path / "uni02_triadic_handoff_request.json"
    adjudication_path = tmp_path / "uni02_sophia_adjudication_packet.json"
    out_path = tmp_path / "nested" / "uni02_atlas_memory_candidate_packet.json"

    handoff_path.write_text(
        json.dumps(
            {
                "request_id": "uni02-cli-005",
                "applicationPortabilityStatus": "passed",
                "crossDomainValidationStatus": "partial",
                "universalClaimStatus": "not_asserted",
            }
        ),
        encoding="utf-8",
    )
    adjudication_path.write_text(json.dumps({"status": "adjudicated"}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "atlas.uni02_candidate",
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
    assert packet["schema"] == "atlas.uni02_memory_candidate.v1"
    assert packet["request_id"] == "uni02-cli-005"
    assert packet["candidate_status"] == "shadow_only"
    assert packet["allowed_use"] == "retrieval_candidate"
    assert packet["memory_write_authorized"] is False
    assert packet["artifact_refs"] == []
    assert packet["artifact_refs_by_key"] == {}
    assert packet["artifact_sha256s"] == {}
    assert packet["artifact_sha256s_by_key"] == {}
    assert packet["source_posture"] == {
        "application_portability_status": "passed",
        "cross_domain_validation_status": "partial",
        "universal_claim_status": "not_asserted",
    }
    assert packet["guardrails"] == {
        "not_authoritative_memory": True,
        "does_not_override_source": True,
        "does_not_universalize_tches": True,
        "human_review_required": True,
    }
