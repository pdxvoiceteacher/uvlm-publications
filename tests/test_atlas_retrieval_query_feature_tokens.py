from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python" / "src"))

from atlas.retrieval import _query_feature_tokens


def test_query_feature_tokens_accepts_dict_constraints():
    query = {
        "question_text": "What is the critical systems-level constraint?",
        "source_terms": ["criticality", "capillary"],
        "source_variables": ["flow stability"],
        "source_constraints": [
            {"text": "capillary stability margin"},
            {"constraint": "thermal transient ceiling"},
            {"label": "TE integrity limit"},
        ],
    }

    toks = _query_feature_tokens(query)

    assert "critical" in toks or "criticality" in toks
    assert "capillary" in toks
    assert "thermal" in toks
    assert "integrity" in toks
