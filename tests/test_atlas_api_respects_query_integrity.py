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
