from atlas.retrieval import build_atlas_prior_packet
import importlib
import json


def test_same_question_same_source_prior_is_shadow_only(monkeypatch):
    query = {
        "question_text": "What is the capillary stability margin for this source?",
        "question_sha256": "q-sha-1",
        "source_id": "grounding:sha256:source-a",
        "normalized_sha256": "bundle-a",
        "source_label": "source-a",
        "source_terms": ["capillary", "stability"],
        "source_variables": ["psi"],
        "source_constraints": ["ceiling"],
    }

    same_prior = {
        "question_text": "What is the capillary stability margin for this source?",
        "question_sha256": "q-sha-1",
        "source_id": "grounding:sha256:source-a",
        "normalized_sha256": "bundle-a",
        "source_label": "source-a",
        "run_id": "run-1",
        "track_id": "track-1",
        "origin_type": "atlas_memory",
        "ai_output": "A prior answer from same question and source.",
    }

    monkeypatch.setattr("atlas.retrieval.retrieve_relevant_priors", lambda q, top_k=3: [{"similarity_score": 0.95, "prior": same_prior}])

    packet = build_atlas_prior_packet(query)
    assert packet["match_count"] == 1

    match = packet["matches"][0]
    assert match["prior_scope"] == "same_question_source_match"
    assert match["same_question"] is True
    assert match["same_source"] is True
    assert match["allowed_use"] == "shadow_only"

    decision = packet["prior_injection_decision"][0]
    assert decision["allowed_use"] == "shadow_only"
    assert "downgraded" in decision["reason"]
    assert any("downgraded" in line for line in packet["prior_injection_trace"])


def test_same_source_different_question_is_context_only(monkeypatch):
    query = {
        "question_text": "What are the downstream risks?",
        "question_sha256": "q-new",
        "source_id": "grounding:sha256:source-a",
        "normalized_sha256": "bundle-new",
        "source_label": "source-a",
    }

    prior = {
        "question_text": "What is the capillary stability margin for this source?",
        "question_sha256": "q-old",
        "source_id": "grounding:sha256:source-a",
        "normalized_sha256": "bundle-old",
        "source_label": "source-a",
        "run_id": "run-2",
        "track_id": "track-2",
        "origin_type": "atlas_memory",
        "ai_output": "Earlier source-specific analysis.",
    }

    monkeypatch.setattr("atlas.retrieval.retrieve_relevant_priors", lambda q, top_k=3: [{"similarity_score": 0.71, "prior": prior}])
    packet = build_atlas_prior_packet(query)

    match = packet["matches"][0]
    assert match["prior_scope"] == "same_source_context"
    assert match["same_question"] is False
    assert match["same_source"] is True
    assert match["allowed_use"] == "context_only"


def test_verified_different_source_prior_can_support_answers(monkeypatch):
    query = {
        "question_text": "What are the downstream risks?",
        "question_sha256": "q-new",
        "source_id": "grounding:sha256:source-a",
        "normalized_sha256": "bundle-new",
        "source_label": "source-a",
    }

    prior = {
        "question_text": "What are analogous risks in comparable systems?",
        "question_sha256": "q-other",
        "source_id": "grounding:sha256:source-b",
        "normalized_sha256": "bundle-other",
        "source_label": "source-b",
        "run_id": "run-3",
        "track_id": "track-3",
        "origin_type": "atlas_memory",
        "ai_output": "Comparable system evidence with provenance.",
    }

    monkeypatch.setattr("atlas.retrieval.retrieve_relevant_priors", lambda q, top_k=3: [{"similarity_score": 0.66, "prior": prior}])

    packet = build_atlas_prior_packet(query)
    match = packet["matches"][0]

    assert match["same_source"] is False
    assert match["allowed_use"] in {"answer_support", "cite_if_verified"}
    assert isinstance(match["provenance_hash"], str)
    assert len(match["provenance_hash"]) == 64


def test_query_provenance_fields_are_preserved_in_packet_and_selected_priors(monkeypatch):
    query = {
        "atlas_query_contract_version": "v1",
        "question_text": "What are the downstream risks?",
        "query_text_flat": "what are the downstream risks",
        "source_id": "grounding:sha256:source-a",
        "source_sha256": "sha-source-a",
        "normalized_sha256": "bundle-new",
        "bundle_manifest_path": "/tmp/bundles/source-a/manifest.json",
        "source_filename": "source-a.pdf",
        "source_kind": "pdf",
        "run_id": "run-query-1",
        "preset": "atlas_default",
        "source_label": "source-a",
    }

    prior = {
        "question_text": "What are analogous risks in comparable systems?",
        "question_sha256": "q-other",
        "source_id": "grounding:sha256:source-b",
        "source_sha256": "sha-source-b",
        "normalized_sha256": "bundle-other",
        "bundle_manifest_path": "/tmp/bundles/source-b/manifest.json",
        "source_filename": "source-b.pdf",
        "source_kind": "pdf",
        "run_id": "run-3",
        "track_id": "track-3",
        "origin_type": "atlas_memory",
        "preset": "atlas_default",
        "ai_output": "Comparable system evidence with provenance.",
    }

    monkeypatch.setattr("atlas.retrieval.retrieve_relevant_priors", lambda q, top_k=3: [{"similarity_score": 0.66, "prior": prior}])

    packet = build_atlas_prior_packet(query)
    assert packet["source_id"] == query["source_id"]
    assert packet["source_sha256"] == query["source_sha256"]
    assert packet["normalized_sha256"] == query["normalized_sha256"]
    assert packet["bundle_manifest_path"] == query["bundle_manifest_path"]
    assert packet["source_filename"] == query["source_filename"]
    assert packet["source_kind"] == query["source_kind"]
    assert packet["run_id"] == query["run_id"]
    assert packet["preset"] == query["preset"]
    assert packet["query_text_flat"] == query["query_text_flat"]

    selected = packet["selected_priors"][0]
    assert selected["source_id"] == prior["source_id"]
    assert selected["source_sha256"] == prior["source_sha256"]
    assert selected["normalized_sha256"] == prior["normalized_sha256"]
    assert selected["bundle_manifest_path"] == prior["bundle_manifest_path"]
    assert selected["source_filename"] == prior["source_filename"]
    assert selected["source_kind"] == prior["source_kind"]
    assert selected["run_id"] == prior["run_id"]
    assert selected["preset"] == prior["preset"]
    assert selected["provenance_available"] is True


def test_selected_prior_explicitly_marks_unavailable_provenance(monkeypatch):
    query = {
        "question_text": "What changed in source context?",
        "source_id": "grounding:sha256:source-a",
        "source_sha256": "sha-source-a",
        "normalized_sha256": "bundle-a",
        "bundle_manifest_path": "/tmp/bundles/source-a/manifest.json",
        "source_filename": "source-a.pdf",
        "source_kind": "pdf",
        "run_id": "run-query-9",
    }
    prior = {
        "question_text": "What changed in source context?",
        "source_label": "source-a",
        "ai_output": "Partial prior without explicit provenance identifiers.",
    }

    monkeypatch.setattr("atlas.retrieval.retrieve_relevant_priors", lambda q, top_k=3: [{"similarity_score": 0.2, "prior": prior}])
    packet = build_atlas_prior_packet(query)
    selected = packet["selected_priors"][0]

    for key in (
        "allowed_use",
        "same_question",
        "same_source",
        "same_bundle",
        "prior_scope",
        "provenance_available",
        "provenance_unavailable_reason",
        "source_id",
        "source_sha256",
        "normalized_sha256",
        "bundle_manifest_path",
        "source_filename",
        "source_kind",
    ):
        assert key in selected

    assert selected["source_id"] == query["source_id"]
    assert selected["normalized_sha256"] == query["normalized_sha256"]
    assert selected["provenance_available"] is False
    assert "missing run_id/source_id/normalized_sha256" in selected["provenance_unavailable_reason"]


def test_api_response_preserves_selected_prior_fields_after_guard(tmp_path, monkeypatch):
    monkeypatch.setenv("TRIADIC_BRIDGE_ROOT", str(tmp_path))
    api_server = importlib.import_module("atlas.api_server")
    TestClient = importlib.import_module("fastapi.testclient").TestClient

    query = {
        "question_integrity_ok": True,
        "question_text": "Q",
        "source_id": "grounding:sha256:source-a",
        "source_sha256": "sha-source-a",
        "normalized_sha256": "bundle-a",
        "bundle_manifest_path": "/tmp/a/manifest.json",
        "source_filename": "a.pdf",
        "source_kind": "pdf",
        "run_id": "run-q",
        "preset": "atlas_default",
    }
    (tmp_path / "atlas_query.json").write_text(json.dumps(query), encoding="utf-8")
    monkeypatch.setattr(api_server, "ATLAS_QUERY_FILE", tmp_path / "atlas_query.json")
    monkeypatch.setattr(api_server, "ATLAS_PRIOR_PACKET_FILE", tmp_path / "atlas_prior_packet.json")

    monkeypatch.setattr(
        api_server,
        "build_atlas_prior_packet",
        lambda q: {
            "question_text": q["question_text"],
            "source_id": q["source_id"],
            "source_sha256": q["source_sha256"],
            "normalized_sha256": q["normalized_sha256"],
            "bundle_manifest_path": q["bundle_manifest_path"],
            "source_filename": q["source_filename"],
            "source_kind": q["source_kind"],
            "run_id": q["run_id"],
            "preset": q["preset"],
            "selected_priors": [
                {
                    "provenance_hash": "ph-1",
                    "allowed_use": "answer_support",
                    "same_question": True,
                    "same_source": True,
                    "same_bundle": True,
                    "prior_scope": "same_question_source_match",
                    "provenance_available": False,
                    "provenance_unavailable_reason": "missing run_id/source_id/normalized_sha256 in prior provenance",
                    "source_id": q["source_id"],
                    "source_sha256": q["source_sha256"],
                    "normalized_sha256": q["normalized_sha256"],
                    "bundle_manifest_path": q["bundle_manifest_path"],
                    "source_filename": q["source_filename"],
                    "source_kind": q["source_kind"],
                }
            ],
            "prior_injection_decision": [
                {
                    "provenance_hash": "ph-1",
                    "prior_scope": "same_question_source_match",
                    "same_question": True,
                    "same_source": True,
                    "same_bundle": True,
                    "allowed_use": "answer_support",
                    "reason": "unsafe pre-guard state",
                }
            ],
            "prior_injection_trace": [],
            "matches": [],
        },
    )

    client = TestClient(api_server.app)
    payload = client.post("/atlas/retrieve").json()
    selected = payload["selected_priors"][0]

    assert selected["allowed_use"] == "shadow_only"
    assert selected["same_question"] is True
    assert selected["same_source"] is True
    assert selected["same_bundle"] is True
    assert selected["prior_scope"] == "same_question_source_match"
    assert selected["provenance_available"] is False
    assert selected["provenance_unavailable_reason"]
    assert selected["source_id"] == query["source_id"]
    assert selected["source_sha256"] == query["source_sha256"]
    assert selected["normalized_sha256"] == query["normalized_sha256"]
    assert selected["bundle_manifest_path"] == query["bundle_manifest_path"]
    assert selected["source_filename"] == query["source_filename"]
    assert selected["source_kind"] == query["source_kind"]
