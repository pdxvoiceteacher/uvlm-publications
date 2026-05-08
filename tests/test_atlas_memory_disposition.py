from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python" / "src"))

from atlas.memory_disposition import (  # noqa: E402
    AtlasMemoryDispositionValidationError,
    build_atlas_memory_disposition_packet,
)

SCHEMA_PATH = Path("schemas/atlas_memory_disposition_packet.schema.json")
SCRIPT = Path("scripts/build_atlas_memory_disposition_overlay.py")
SOURCE_PATHS = [
    Path("python/src/atlas/memory_disposition.py"),
    Path("scripts/build_atlas_memory_disposition_overlay.py"),
]


def valid_memory_intent_packet() -> dict:
    return {
        "schema": "uvlm.atlas_memory_intent_packet.v1",
        "memory_intent": {
            "memory_intent_id": "memory-intent-001",
            "requires_atlas_disposition": True,
            "retention_band_hint": "mtm",
            "sensitivity_class": "internal",
        },
        "audit_pass_id": "audit-pass-001",
        "submission_id": "submission-001",
        "sonya_ingress_id": "sonya-ingress-001",
        "aegis_trace_id": "aegis-trace-001",
        "request_envelope_id": "request-envelope-001",
        "analysis_profile_id": "analysis-profile-001",
        "semantic_taxonomy_id": "semantic-taxonomy-001",
        "grounding_refs": ["grounding:001"],
        "tel_refs": ["tel:001"],
        "coherence_metric_refs": ["coherence:001"],
        "candidate_routes": {
            "atlas_memory_write_authorized": False,
            "atlas_prior_canonized": False,
            "truth_certified": False,
            "deployment_authorized": False,
        },
        "source_boundary": {
            "live_atlas_call_performed": False,
            "model_call_performed": False,
            "network_call_performed": False,
        },
        "intent_not_memory_write_authorization": True,
        "intent_not_prior_canonization": True,
        "intent_not_truth_certification": True,
        "intent_not_deployment_authority": True,
        "intent_not_final_answer": True,
    }


def valid_route_trace(memory_intent_id: str = "memory-intent-001") -> dict:
    return {
        "schema": "uvlm.atlas_memory_intent_route_trace.v1",
        "memory_intent_id": memory_intent_id,
        "atlas_memory_write_performed": False,
        "live_atlas_call_performed": False,
    }


def build_packet(source: dict | None = None, route_trace: dict | None = None) -> dict:
    return build_atlas_memory_disposition_packet(
        source or valid_memory_intent_packet(), route_trace
    )


def assert_validation_error(source: dict, route_trace: dict | None = None) -> None:
    with pytest.raises(AtlasMemoryDispositionValidationError):
        build_atlas_memory_disposition_packet(source, route_trace)


def test_valid_memory_intent_builds_deterministic_disposition_packet():
    packet = build_packet()

    assert packet["schema"] == "atlas.memory_disposition_packet.v1"
    assert packet["memory_intent_id"] == "memory-intent-001"
    assert packet["source_packet_schema"] == "uvlm.atlas_memory_intent_packet.v1"
    assert packet["audit_pass_id"] == "audit-pass-001"
    assert packet["submission_id"] == "submission-001"
    assert packet["sonya_ingress_id"] == "sonya-ingress-001"
    assert packet["aegis_trace_id"] == "aegis-trace-001"
    assert packet["request_envelope_id"] == "request-envelope-001"
    assert packet["analysis_profile_id"] == "analysis-profile-001"
    assert packet["semantic_taxonomy_id"] == "semantic-taxonomy-001"
    assert packet["grounding_refs"] == ["grounding:001"]
    assert packet["tel_refs"] == ["tel:001"]
    assert packet["coherence_metric_refs"] == ["coherence:001"]
    assert packet["coherence_escrow_status"] == "review_escrow"
    assert packet["reversibility_index"] == "R2"
    assert packet["disposition"] == {
        "status": "pending_human_review",
        "allowed_use": "retrieval_candidate",
        "retention_band": "mtm",
        "sensitivity_class": "internal",
        "reason_codes": [
            "candidate_only",
            "atlas_disposition_required",
            "human_review_required",
            "not_memory_write",
            "not_prior_canonization",
            "not_truth_certification",
        ],
    }
    assert packet["review_requirements"] == {
        "requires_human_review": True,
        "requires_ltm_review": False,
        "requires_prior_canonization_review": True,
        "requires_source_lineage_review": True,
    }
    assert packet["authority_boundary"] == {
        "memory_write_authorized": False,
        "prior_canonized": False,
        "truth_certified": False,
        "deployment_authorized": False,
        "publisher_finalized": False,
        "canonical_publication_mutated": False,
    }
    assert packet["runtime_boundary"] == {
        "live_atlas_call_performed": False,
        "network_call_performed": False,
        "model_call_performed": False,
        "live_sophia_call_performed": False,
        "live_sonya_call_performed": False,
    }
    assert packet["created_at"] is None
    assert packet["meta"] == {}


def test_same_input_yields_same_disposition_id():
    first = build_packet(valid_memory_intent_packet(), valid_route_trace())
    second = build_packet(valid_memory_intent_packet(), valid_route_trace())
    assert first["disposition_id"] == second["disposition_id"]


def test_changing_memory_intent_id_changes_disposition_id():
    first_source = valid_memory_intent_packet()
    second_source = valid_memory_intent_packet()
    second_source["memory_intent"]["memory_intent_id"] = "memory-intent-002"
    first = build_packet(first_source)
    second = build_packet(second_source)
    assert first["disposition_id"] != second["disposition_id"]


def test_schema_validates():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(build_packet())


def test_disposition_remains_non_authoritative_with_escrow_defaults():
    packet = build_packet()

    assert packet["coherence_escrow_status"] == "review_escrow"
    assert packet["reversibility_index"] == "R2"
    assert packet["review_requirements"]["requires_human_review"] is True
    assert all(value is False for value in packet["authority_boundary"].values())
    assert all(value is False for value in packet["runtime_boundary"].values())
    assert "not_memory_write" in packet["disposition"]["reason_codes"]
    assert "not_prior_canonization" in packet["disposition"]["reason_codes"]
    assert "not_truth_certification" in packet["disposition"]["reason_codes"]


def test_rejects_non_memory_intent_schema():
    source = valid_memory_intent_packet()
    source["schema"] = "example.invalid"
    assert_validation_error(source)


@pytest.mark.parametrize(
    "field",
    [
        "atlas_memory_write_authorized",
        "atlas_prior_canonized",
        "truth_certified",
        "deployment_authorized",
    ],
)
def test_rejects_candidate_route_authority_flags(field: str):
    source = valid_memory_intent_packet()
    source["candidate_routes"][field] = True
    assert_validation_error(source)


@pytest.mark.parametrize(
    "field",
    [
        "live_atlas_call_performed",
        "model_call_performed",
        "network_call_performed",
    ],
)
def test_rejects_source_boundary_runtime_flags(field: str):
    source = valid_memory_intent_packet()
    source["source_boundary"][field] = True
    assert_validation_error(source)


@pytest.mark.parametrize(
    "field",
    [
        "intent_not_memory_write_authorization",
        "intent_not_prior_canonization",
        "intent_not_truth_certification",
        "intent_not_deployment_authority",
        "intent_not_final_answer",
    ],
)
def test_rejects_guardrail_booleans_false(field: str):
    source = valid_memory_intent_packet()
    source[field] = False
    assert_validation_error(source)


def test_ltm_candidate_retention_hint_maps_to_review_required_status():
    source = valid_memory_intent_packet()
    source["memory_intent"]["retention_band_hint"] = "ltm_candidate"
    packet = build_packet(source)
    assert packet["disposition"]["status"] == "ltm_candidate_review_required"
    assert packet["disposition"]["retention_band"] == "ltm_candidate"
    assert packet["review_requirements"]["requires_ltm_review"] is True


def test_route_trace_linkage_mismatch_is_rejected():
    assert_validation_error(valid_memory_intent_packet(), valid_route_trace("other"))


def test_route_trace_memory_action_performed_true_is_rejected():
    route_trace = valid_route_trace()
    route_trace["atlas_memory_write_performed"] = True
    assert_validation_error(valid_memory_intent_packet(), route_trace)


def test_cli_writes_output(tmp_path):
    memory_intent_path = tmp_path / "atlas_memory_intent_packet.json"
    route_trace_path = tmp_path / "atlas_memory_intent_route_trace.json"
    out_path = tmp_path / "bridge" / "atlas_memory_disposition_packet.json"
    memory_intent_path.write_text(
        json.dumps(valid_memory_intent_packet()), encoding="utf-8"
    )
    route_trace_path.write_text(json.dumps(valid_route_trace()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "atlas.memory_disposition",
            "--memory-intent",
            str(memory_intent_path),
            "--route-trace",
            str(route_trace_path),
            "--out",
            str(out_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "python" / "src"),
        },
    )

    assert result.returncode == 0, result.stdout + result.stderr
    packet = json.loads(out_path.read_text(encoding="utf-8"))
    assert packet["schema"] == "atlas.memory_disposition_packet.v1"
    assert packet["memory_intent_id"] == "memory-intent-001"
    assert packet["coherence_escrow_status"] == "review_escrow"
    assert packet["reversibility_index"] == "R2"
    assert packet["authority_boundary"]["memory_write_authorized"] is False


def test_overlay_builder_writes_registry_review_queue_and_annotations(tmp_path):
    bridge = tmp_path / "bridge"
    registry = tmp_path / "registry"
    packet = build_packet()
    disposition_path = bridge / "atlas_memory_disposition_packet.json"
    disposition_path.parent.mkdir(parents=True)
    disposition_path.write_text(json.dumps(packet), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--atlas-memory-disposition-packet",
            str(disposition_path),
            "--out-disposition-registry",
            str(registry / "atlas_memory_disposition_registry.json"),
            "--out-review-queue",
            str(registry / "atlas_memory_review_queue.json"),
            "--out-annotations",
            str(registry / "atlas_memory_disposition_annotations.json"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    disposition_registry = json.loads(
        (registry / "atlas_memory_disposition_registry.json").read_text(
            encoding="utf-8"
        )
    )
    review_queue = json.loads(
        (registry / "atlas_memory_review_queue.json").read_text(encoding="utf-8")
    )
    annotations = json.loads(
        (registry / "atlas_memory_disposition_annotations.json").read_text(
            encoding="utf-8"
        )
    )
    assert disposition_registry["nonAuthoritativeOnly"] is True
    assert disposition_registry["coherenceEscrowStatus"] == "review_escrow"
    assert disposition_registry["reversibilityIndex"] == "R2"
    assert disposition_registry["entries"][0]["status"] == "pending_human_review"
    assert disposition_registry["entries"][0]["coherenceEscrowStatus"] == "review_escrow"
    assert disposition_registry["entries"][0]["reversibilityIndex"] == "R2"
    assert review_queue["coherenceEscrowStatus"] == "review_escrow"
    assert review_queue["reversibilityIndex"] == "R2"
    assert review_queue["entries"][0]["memoryIntentId"] == "memory-intent-001"
    assert review_queue["entries"][0]["coherenceEscrowStatus"] == "review_escrow"
    assert review_queue["entries"][0]["reversibilityIndex"] == "R2"
    assert annotations["coherenceEscrowStatus"] == "review_escrow"
    assert annotations["reversibilityIndex"] == "R2"
    assert annotations["watchlistOnly"] is True


def test_overlay_builder_never_mutates_publication_catalog_or_doi_registries(tmp_path):
    bridge = tmp_path / "bridge"
    registry = tmp_path / "registry"
    packet = build_packet()
    disposition_path = bridge / "atlas_memory_disposition_packet.json"
    disposition_path.parent.mkdir(parents=True)
    disposition_path.write_text(json.dumps(packet), encoding="utf-8")

    sentinels = {
        registry / "publications.json": {"sentinel": "publications"},
        registry / "catalog.json": {"sentinel": "catalog"},
        registry / "dois.json": {"sentinel": "dois"},
    }
    for path, payload in sentinels.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")

    before = {path: path.read_text(encoding="utf-8") for path in sentinels}
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--atlas-memory-disposition-packet",
            str(disposition_path),
            "--out-disposition-registry",
            str(registry / "atlas_memory_disposition_registry.json"),
            "--out-review-queue",
            str(registry / "atlas_memory_review_queue.json"),
            "--out-annotations",
            str(registry / "atlas_memory_disposition_annotations.json"),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    after = {path: path.read_text(encoding="utf-8") for path in sentinels}

    assert result.returncode == 0, result.stdout + result.stderr
    assert after == before


def test_overlay_builder_rejects_authoritative_or_runtime_boundary_mutation():
    authoritative_packet = build_packet()
    authoritative_packet["authority_boundary"]["truth_certified"] = True
    runtime_packet = build_packet()
    runtime_packet["runtime_boundary"]["network_call_performed"] = True

    for packet in (authoritative_packet, runtime_packet):
        with pytest.raises(ValueError):
            from scripts.build_atlas_memory_disposition_overlay import (
                build_overlay_outputs,
            )

            build_overlay_outputs(packet)


def test_disposition_sources_do_not_introduce_forbidden_runtime_tokens():
    tokens = [
        "write" + "_memory",
        "memory_write_authorized" + " = " + "True",
        "persist" + "_candidate(",
        "call" + "_openai",
        "requests" + ".",
        "http" + "x",
        "Oll" + "ama",
        "Sophia" + "Client",
        "Sonya" + "LocalModelNode",
    ]
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_PATHS)

    for token in tokens:
        assert token not in source_text
