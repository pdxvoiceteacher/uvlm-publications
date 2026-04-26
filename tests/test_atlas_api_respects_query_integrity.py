import json

from atlas.api_server import app
from fastapi.testclient import TestClient


def test_atlas_retrieve_returns_bounded_error_when_query_integrity_fails(tmp_path, monkeypatch):
    bridge = tmp_path

    monkeypatch.setattr("atlas.api_server.BRIDGE_ROOT", bridge)
    monkeypatch.setattr("atlas.api_server.ATLAS_QUERY_FILE", bridge / "atlas_query.json")
    monkeypatch.setattr("atlas.api_server.ATLAS_PRIOR_PACKET_FILE", bridge / "atlas_prior_packet.json")

    (bridge / "atlas_query.json").write_text(
        json.dumps(
            {
                "atlas_query_contract_version": "v1",
                "question_text": "",
                "question_integrity_ok": False,
                "integrity_error": "question_text_failed_integrity",
                "source_id": "grounding:sha256:abc",
                "normalized_sha256": "abc",
            }
        ),
        encoding="utf-8",
    )

    client = TestClient(app)
    resp = client.post("/atlas/retrieve")
    data = resp.json()

    assert data["error"] == "atlas_query_integrity_failed"
    assert data["question_integrity_ok"] is False


def test_atlas_retrieve_preserves_query_provenance_fields(tmp_path, monkeypatch):
    bridge = tmp_path

    monkeypatch.setattr("atlas.api_server.BRIDGE_ROOT", bridge)
    monkeypatch.setattr("atlas.api_server.ATLAS_QUERY_FILE", bridge / "atlas_query.json")
    monkeypatch.setattr("atlas.api_server.ATLAS_PRIOR_PACKET_FILE", bridge / "atlas_prior_packet.json")

    (bridge / "atlas_query.json").write_text(
        json.dumps(
            {
                "atlas_query_contract_version": "v1",
                "question_text": "What is the capillary stability margin?",
                "query_text_flat": "capillary stability margin",
                "question_integrity_ok": True,
                "source_id": "grounding:sha256:abc",
                "source_sha256": "sha-abc",
                "normalized_sha256": "norm-abc",
                "bundle_manifest_path": "/tmp/abc/manifest.json",
                "run_id": "run-abc",
                "preset": "atlas_default",
                "source_label": "abc",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "atlas.api_server.build_atlas_prior_packet",
        lambda q: {
            "atlas_query_contract_version": q.get("atlas_query_contract_version"),
            "question_text": q.get("question_text"),
            "query_text_flat": q.get("query_text_flat"),
            "source_id": q.get("source_id"),
            "source_sha256": q.get("source_sha256"),
            "normalized_sha256": q.get("normalized_sha256"),
            "bundle_manifest_path": q.get("bundle_manifest_path"),
            "run_id": q.get("run_id"),
            "preset": q.get("preset"),
            "matches": [],
            "selected_priors": [],
            "prior_injection_decision": [],
            "prior_injection_trace": [],
        },
    )

    client = TestClient(app)
    resp = client.post("/atlas/retrieve")
    data = resp.json()

    assert data["source_id"] == "grounding:sha256:abc"
    assert data["source_sha256"] == "sha-abc"
    assert data["normalized_sha256"] == "norm-abc"
    assert data["bundle_manifest_path"] == "/tmp/abc/manifest.json"
    assert data["run_id"] == "run-abc"
    assert data["preset"] == "atlas_default"
