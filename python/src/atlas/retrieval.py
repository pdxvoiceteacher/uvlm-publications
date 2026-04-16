from pathlib import Path
import json
import re


ATLAS_STORE = Path(r"C:\UVLM\uvlm-publications\atlas_store")


_SHORT_TOKEN_WHITELIST = {
    "te",
    "ggz",
    "psi",
    "r",
    "p",
    "t",
    "e",
}


def _to_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        for key in ("text", "constraint", "term", "display_term", "meaning", "label", "name", "value"):
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
        parts = []
        for key in sorted(value.keys()):
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                parts.append(v.strip())
        return " ".join(parts).strip()
    if isinstance(value, (list, tuple, set)):
        parts = [_to_text(v) for v in value]
        return " ".join([p for p in parts if p]).strip()
    return str(value).strip()


def _tokens(text) -> set[str]:
    normalized = _to_text(text).lower()

    # standard tokens
    toks = set(re.findall(r"[A-Za-z][A-Za-z0-9_\-]{2,}", normalized))

    # add short technical tokens from a bounded whitelist
    shorts = set(re.findall(r"\b[A-Za-z][A-Za-z0-9]?\b", normalized))
    toks |= {t for t in shorts if t in _SHORT_TOKEN_WHITELIST}

    return toks


def _query_feature_tokens(query: dict) -> set[str]:
    toks: set[str] = set()

    toks |= _tokens(query.get("question_text", ""))
    toks |= _tokens(query.get("query_text_flat", ""))

    for t in query.get("source_terms", []):
        toks |= _tokens(t)

    for v in query.get("source_variables", []):
        toks |= _tokens(v)

    for c in query.get("source_constraints", []):
        toks |= _tokens(c)

    return toks


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_existing_priors() -> list[dict]:
    ATLAS_STORE.mkdir(parents=True, exist_ok=True)
    out = []
    for p in ATLAS_STORE.glob("*.json"):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            continue
    return out


def _prior_feature_tokens(prior: dict) -> set[str]:
    toks = set()

    toks |= _tokens(prior.get("question_text", ""))
    toks |= _tokens(prior.get("ai_output", ""))

    novelty = prior.get("novelty", {})
    for t in novelty.get("novel_tokens", []):
        toks |= _tokens(t)

    # Include coherence/source labels if available
    if prior.get("source_label"):
        toks |= _tokens(prior["source_label"])

    return toks


def _structured_relevance_score(query: dict, prior: dict) -> float:
    q_tokens = _query_feature_tokens(query)
    p_tokens = _prior_feature_tokens(prior)

    base = _jaccard(q_tokens, p_tokens)

    # Bonus if source label aligns
    source_bonus = 0.0
    q_source_label = _to_text(query.get("source_label"))
    p_source_label = _to_text(prior.get("source_label"))
    if q_source_label and p_source_label and q_source_label.lower() == p_source_label.lower():
        source_bonus += 0.15

    # Bonus if query source terms appear in prior output
    term_bonus = 0.0
    prior_text = (_to_text(prior.get("ai_output")) + " " + _to_text(prior.get("question_text"))).lower()
    for term in query.get("source_terms", []):
        normalized_term = _to_text(term).lower()
        if normalized_term and normalized_term in prior_text:
            term_bonus += 0.03

    # Bonus if query variables appear
    variable_bonus = 0.0
    for var in query.get("source_variables", []):
        normalized_var = _to_text(var).lower()
        if normalized_var and normalized_var in prior_text:
            variable_bonus += 0.03

    # Bonus if constraints overlap
    constraint_bonus = 0.0
    for c in query.get("source_constraints", []):
        c_tokens = _tokens(c)
        if c_tokens and len(c_tokens & p_tokens) > 0:
            constraint_bonus += 0.04

    return min(base + source_bonus + term_bonus + variable_bonus + constraint_bonus, 1.0)


def retrieve_relevant_priors(query: dict, top_k: int = 3) -> list[dict]:
    priors = load_existing_priors()

    scored = []
    for prior in priors:
        sim = _structured_relevance_score(query, prior)
        scored.append((sim, prior))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        {
            "similarity_score": sim,
            "prior": prior,
        }
        for sim, prior in scored[:top_k]
        if sim > 0.0
    ]


def build_atlas_prior_packet(query: dict) -> dict:
    matches = retrieve_relevant_priors(query)

    return {
        "question_text": query.get("question_text", ""),
        "source_label": query.get("source_label"),
        "source_terms": query.get("source_terms", []),
        "source_variables": query.get("source_variables", []),
        "source_constraints": query.get("source_constraints", []),
        "match_count": len(matches),
        "matches": matches,
        "prior_packet_ready": len(matches) > 0,
        "retrieval_mode": "question_plus_source_evidence",
    }
