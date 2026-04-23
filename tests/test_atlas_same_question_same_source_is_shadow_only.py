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
