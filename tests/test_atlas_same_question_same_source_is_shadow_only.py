from atlas.retrieval import build_atlas_prior_packet


def test_same_question_same_source_prior_never_upgrades_to_answer_support(monkeypatch):
    query = {
        "question_text": "What is the capillary stability margin?",
        "question_sha256": "q-sha-1",
        "source_id": "grounding:sha256:src-1",
        "normalized_sha256": "bundle-1",
        "source_label": "src-1",
    }
    prior = {
        "question_text": "What is the capillary stability margin?",
        "question_sha256": "q-sha-1",
        "source_id": "grounding:sha256:src-1",
        "normalized_sha256": "bundle-1",
        "source_label": "src-1",
        "run_id": "run-1",
        "track_id": "track-1",
        "origin_type": "atlas_memory",
        "ai_output": "Prior answer text",
    }

    monkeypatch.setattr("atlas.retrieval.retrieve_relevant_priors", lambda q, top_k=3: [{"similarity_score": 0.99, "prior": prior}])

    packet = build_atlas_prior_packet(query)

    match = packet["matches"][0]
    decision = packet["prior_injection_decision"][0]

    assert match["prior_scope"] == "same_question_source_match"
    assert match["allowed_use"] == "shadow_only"
    assert decision["allowed_use"] in {"shadow_only", "context_only"}
    assert decision["allowed_use"] != "answer_support"


def test_missing_prior_provenance_fields_fallback_to_query(monkeypatch):
    query = {
        "question_text": "What is the capillary stability margin?",
        "query_text_flat": "capillary stability margin",
        "question_sha256": "q-sha-1",
        "source_id": "grounding:sha256:src-1",
        "source_sha256": "sha-src-1",
        "normalized_sha256": "bundle-1",
        "bundle_manifest_path": "/tmp/src-1/manifest.json",
        "source_filename": "src-1.pdf",
        "source_kind": "pdf",
        "run_id": "run-query",
        "preset": "atlas_default",
    }
    prior = {
        "question_text": "What is the capillary stability margin?",
        "question_sha256": "q-sha-1",
        "track_id": "track-1",
        "origin_type": "atlas_memory",
        "ai_output": "Prior answer text",
    }

    monkeypatch.setattr("atlas.retrieval.retrieve_relevant_priors", lambda q, top_k=3: [{"similarity_score": 0.99, "prior": prior}])
    packet = build_atlas_prior_packet(query)
    selected = packet["selected_priors"][0]

    assert selected["source_id"] == query["source_id"]
    assert selected["source_sha256"] == query["source_sha256"]
    assert selected["normalized_sha256"] == query["normalized_sha256"]
    assert selected["bundle_manifest_path"] == query["bundle_manifest_path"]
    assert selected["source_filename"] == query["source_filename"]
    assert selected["source_kind"] == query["source_kind"]
    assert selected["run_id"] == query["run_id"]
    assert selected["preset"] == query["preset"]


def test_same_source_same_bundle_does_not_exceed_context_only(monkeypatch):
    query = {
        "question_text": "What is the updated margin?",
        "question_sha256": "q-sha-new",
        "source_id": "grounding:sha256:src-2",
        "normalized_sha256": "bundle-2",
        "source_label": "src-2",
    }
    prior = {
        "question_text": "What was the previous margin?",
        "question_sha256": "q-sha-old",
        "source_id": "grounding:sha256:src-2",
        "normalized_sha256": "bundle-2",
        "source_label": "src-2",
        "run_id": "run-2",
        "track_id": "track-2",
        "origin_type": "atlas_memory",
        "ai_output": "Prior analysis from same source and bundle.",
    }

    monkeypatch.setattr("atlas.retrieval.retrieve_relevant_priors", lambda q, top_k=3: [{"similarity_score": 0.86, "prior": prior}])
    packet = build_atlas_prior_packet(query)

    selected = packet["selected_priors"][0]
    decision = packet["prior_injection_decision"][0]
    assert selected["same_source"] is True
    assert selected["same_bundle"] is True
    assert selected["allowed_use"] in {"shadow_only", "context_only"}
    assert decision["allowed_use"] in {"shadow_only", "context_only"}
