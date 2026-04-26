from atlas.retrieval import build_atlas_prior_packet


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
    assert packet["run_id"] == query["run_id"]
    assert packet["preset"] == query["preset"]
    assert packet["query_text_flat"] == query["query_text_flat"]

    selected = packet["selected_priors"][0]
    assert selected["source_id"] == prior["source_id"]
    assert selected["source_sha256"] == prior["source_sha256"]
    assert selected["normalized_sha256"] == prior["normalized_sha256"]
    assert selected["bundle_manifest_path"] == prior["bundle_manifest_path"]
    assert selected["run_id"] == prior["run_id"]
    assert selected["preset"] == prior["preset"]
