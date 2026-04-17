from atlas.retrieval import _query_feature_tokens


def test_query_feature_tokens_accepts_mixed_structured_query_fields():
    query = {
        "atlas_query_contract_version": "v1",
        "question_text": "What is the critical systems-level constraint?",
        "query_text_flat": "what is the critical systems level constraint",
        "source_terms": ["Psi", "E_s", "GGZ"],
        "source_variables": ["Lambda_T", "r"],
        "source_constraints": [
            {"text": "capillary stability margin"},
            {"constraint": "thermal transient ceiling"},
            {"label": "TE integrity limit"},
        ],
    }

    toks = _query_feature_tokens(query)

    assert "critical" in toks
    assert "capillary" in toks
    assert "thermal" in toks
    assert "integrity" in toks
    assert "te" in toks
    assert "ggz" in toks
    assert "psi" in toks
    assert "r" in toks
