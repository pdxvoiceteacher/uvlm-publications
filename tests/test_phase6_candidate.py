import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python" / "src"))

from atlas.phase6_candidate import build_phase6_memory_candidate_packet


def test_phase6_candidate_is_artifact_bound_shadow_only_and_not_authoritative():
    handoff_request = {
        "request_id": "phase6-request-001",
        "artifact_refs": ["handoff-source-a", "metrics-report-a"],
        "artifact_refs_by_key": {},
        "artifact_sha256s": {
            "handoff-source-a": "a" * 64,
            "metrics-report-a": "b" * 64,
        },
        "artifact_sha256s_by_key": {},
        "source_posture": {
            "metrics_consistency_passed": True,
            "ready_for_retrosynthesis_seed": True,
            "application_portability_status": "bounded",
            "domain_boundedness_status": "domain_bounded",
            "cross_domain_validation_status": "not_yet_tested",
            "universal_claim_status": "not_asserted",
        },
    }
    sophia_adjudication = {
        "adjudication_status": "candidate",
        "truth_certification": True,
        "authoritative_memory_write_blocked": True,
        "sophia_directive": "block_authoritative_memory_write",
        "sophia_retrosynthesis_status": "seed_candidate_only",
    }

    packet = build_phase6_memory_candidate_packet(
        handoff_request,
        sophia_adjudication,
        handoff_request_ref="phase6_triadic_handoff_request.json",
        handoff_request_sha256="c" * 64,
        sophia_adjudication_ref="phase6_sophia_adjudication_packet.json",
        sophia_adjudication_sha256="d" * 64,
    )

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
            "metrics_consistency_passed",
            "authoritative_memory_write_blocked",
        ],
        "artifact_refs": ["handoff-source-a", "metrics-report-a"],
        "artifact_refs_by_key": {},
        "artifact_sha256s": {
            "handoff-source-a": "a" * 64,
            "metrics-report-a": "b" * 64,
        },
        "artifact_sha256s_by_key": {},
        "handoff_request_ref": "phase6_triadic_handoff_request.json",
        "handoff_request_sha256": "c" * 64,
        "sophia_adjudication_ref": "phase6_sophia_adjudication_packet.json",
        "sophia_adjudication_sha256": "d" * 64,
        "sophia_directive": "block_authoritative_memory_write",
        "sophia_retrosynthesis_status": "seed_candidate_only",
        "source_posture": {
            "metrics_consistency_passed": True,
            "ready_for_retrosynthesis_seed": True,
            "application_portability_status": "bounded",
            "domain_boundedness_status": "domain_bounded",
            "cross_domain_validation_status": "not_yet_tested",
            "universal_claim_status": "not_asserted",
        },
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
    assert packet["memory_write_authorized"] is False


def test_phase6_candidate_normalizes_dict_artifact_refs_to_portable_refs():
    packet = build_phase6_memory_candidate_packet(
        {
            "request_id": "phase6-request-003",
            "artifact_refs": {
                "phase6_review": "artifacts/phase6_review.json",
                "universality_drift": "artifacts/universality_drift.json",
            },
            "artifact_sha256s": {
                "phase6_review": "1" * 64,
                "universality_drift": "2" * 64,
            },
            "cross_domain_validation_status": "not_yet_tested",
        },
        {},
    )

    assert packet["artifact_refs"] == [
        "artifacts/phase6_review.json",
        "artifacts/universality_drift.json",
    ]
    assert all(isinstance(ref, str) for ref in packet["artifact_refs"])
    assert packet["artifact_refs_by_key"] == {
        "phase6_review": "artifacts/phase6_review.json",
        "universality_drift": "artifacts/universality_drift.json",
    }
    assert packet["artifact_sha256s"] == {
        "artifacts/phase6_review.json": "1" * 64,
        "artifacts/universality_drift.json": "2" * 64,
    }
    assert packet["artifact_sha256s_by_key"] == {
        "phase6_review": "1" * 64,
        "universality_drift": "2" * 64,
    }


def test_phase6_candidate_prefers_explicit_refs_by_key_and_never_emits_dict_refs():
    packet = build_phase6_memory_candidate_packet(
        {
            "request_id": "phase6-request-005",
            "artifact_refs": [
                {
                    "phase6_review": "runtime/phase6_review.json",
                    "universality_drift": "runtime/universality_drift.json",
                }
            ],
            "artifact_refs_by_key": {
                "phase6_review": "portable/phase6_review.json",
                "universality_drift": "portable/universality_drift.json",
            },
            "artifact_sha256s": {
                "portable/phase6_review.json": "3" * 64,
                "portable/universality_drift.json": "4" * 64,
            },
            "cross_domain_validation_status": "not_yet_tested",
        },
        {},
    )

    assert packet["artifact_refs"] == [
        "runtime/phase6_review.json",
        "runtime/universality_drift.json",
    ]
    assert all(isinstance(ref, str) for ref in packet["artifact_refs"])
    assert packet["artifact_refs_by_key"] == {
        "phase6_review": "portable/phase6_review.json",
        "universality_drift": "portable/universality_drift.json",
    }
    assert packet["artifact_sha256s"] == {
        "portable/phase6_review.json": "3" * 64,
        "portable/universality_drift.json": "4" * 64,
    }
    assert packet["artifact_sha256s_by_key"] == {
        "phase6_review": "3" * 64,
        "universality_drift": "4" * 64,
    }


def test_phase6_candidate_adds_retrosynthesis_blocked_reason():
    packet = build_phase6_memory_candidate_packet(
        {
            "request_id": "phase6-request-004",
            "ready_for_retrosynthesis_seed": False,
            "cross_domain_validation_status": "validated_in_domain_only",
        },
        {},
    )

    assert "retrosynthesis_blocked" in packet["reason_codes"]
    assert "cross_domain_validation_pending" not in packet["reason_codes"]
    assert packet["memory_write_authorized"] is False


def test_phase6_candidate_cli_writes_artifact_bound_output_packet(tmp_path):
    handoff_path = tmp_path / "phase6_triadic_handoff_request.json"
    adjudication_path = tmp_path / "phase6_sophia_adjudication_packet.json"
    out_path = tmp_path / "nested" / "phase6_atlas_memory_candidate_packet.json"
    handoff_payload = {
        "request_id": "phase6-cli-003",
        "artifact_refs": ["coherence:handoff:003"],
        "artifact_sha256s": {"coherence:handoff:003": "e" * 64},
        "metricsConsistencyPassed": True,
        "readyForRetrosynthesisSeed": False,
        "applicationPortabilityStatus": "bounded_transfer_only",
        "domainBoundednessStatus": "domain_bounded",
        "crossDomainValidationStatus": "not_yet_tested",
        "universalClaimStatus": "not_asserted",
    }
    adjudication_payload = {
        "status": "adjudicated",
        "sophiaDirective": "shadow_only_no_authoritative_memory_write",
        "retrosynthesisStatus": "blocked_pending_human_review",
        "memoryWriteAuthorized": False,
    }
    handoff_path.write_text(json.dumps(handoff_payload), encoding="utf-8")
    adjudication_path.write_text(json.dumps(adjudication_payload), encoding="utf-8")

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
    assert packet["candidate_status"] == "shadow_only"
    assert packet["memory_write_authorized"] is False
    assert packet["artifact_refs"] == ["coherence:handoff:003"]
    assert packet["artifact_refs_by_key"] == {}
    assert packet["artifact_sha256s"] == {"coherence:handoff:003": "e" * 64}
    assert packet["artifact_sha256s_by_key"] == {}
    assert packet["handoff_request_ref"] == str(handoff_path)
    assert packet["handoff_request_sha256"] == hashlib.sha256(
        handoff_path.read_bytes()
    ).hexdigest()
    assert packet["sophia_adjudication_ref"] == str(adjudication_path)
    assert packet["sophia_adjudication_sha256"] == hashlib.sha256(
        adjudication_path.read_bytes()
    ).hexdigest()
    assert packet["sophia_directive"] == "shadow_only_no_authoritative_memory_write"
    assert packet["sophia_retrosynthesis_status"] == "blocked_pending_human_review"
    assert packet["source_posture"] == {
        "metrics_consistency_passed": True,
        "ready_for_retrosynthesis_seed": False,
        "application_portability_status": "bounded_transfer_only",
        "domain_boundedness_status": "domain_bounded",
        "cross_domain_validation_status": "not_yet_tested",
        "universal_claim_status": "not_asserted",
    }
    assert "cross_domain_validation_pending" in packet["reason_codes"]
    assert "retrosynthesis_blocked" in packet["reason_codes"]
    assert "metrics_consistency_passed" in packet["reason_codes"]
    assert "authoritative_memory_write_blocked" in packet["reason_codes"]
    assert packet["guardrails"] == {
        "not_authoritative_memory": True,
        "does_not_override_source": True,
        "human_review_required": True,
    }
