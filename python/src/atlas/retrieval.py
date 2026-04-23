from pathlib import Path
import hashlib
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


def _sha256_text(value: str) -> str:
    return hashlib.sha256((value or "").encode("utf-8")).hexdigest()


def _normalized_bundle_sha256(payload: dict) -> str:
    try:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    except Exception:
        canonical = _to_text(payload)
    return _sha256_text(canonical)


def _safe_get(d: dict, *keys: str):
    for key in keys:
        if key in d and d.get(key) not in (None, ""):
            return d.get(key)
    return None


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


def _classify_prior_scope(query: dict, prior: dict) -> tuple[str, bool, bool, bool]:
    q_question_sha = _safe_get(query, "question_sha256")
    p_question_sha = _safe_get(prior, "question_sha256")
    if not q_question_sha:
        q_question_sha = _sha256_text(_to_text(query.get("question_text")).lower())
    if not p_question_sha:
        p_question_sha = _sha256_text(_to_text(prior.get("question_text")).lower())
    same_question = bool(q_question_sha and p_question_sha and q_question_sha == p_question_sha)

    q_bundle_sha = _safe_get(query, "normalized_sha256", "bundle_normalized_sha256")
    p_bundle_sha = _safe_get(prior, "normalized_sha256", "bundle_normalized_sha256")
    if not q_bundle_sha:
        q_bundle_sha = _normalized_bundle_sha256(
            {
                "source_label": query.get("source_label"),
                "source_terms": query.get("source_terms", []),
                "source_variables": query.get("source_variables", []),
                "source_constraints": query.get("source_constraints", []),
            }
        )
    if not p_bundle_sha:
        p_bundle_sha = _normalized_bundle_sha256(
            {
                "source_label": prior.get("source_label"),
                "source_terms": prior.get("source_terms", []),
                "source_variables": prior.get("source_variables", []),
                "source_constraints": prior.get("source_constraints", []),
            }
        )
    same_bundle = bool(q_bundle_sha and p_bundle_sha and q_bundle_sha == p_bundle_sha)

    q_source = _to_text(_safe_get(query, "source_id", "source_label")).lower()
    p_source = _to_text(_safe_get(prior, "source_id", "source_label")).lower()
    same_source = bool(q_source and p_source and q_source == p_source)

    prior_scope = "durable_prior"
    if same_question and (same_bundle or same_source):
        prior_scope = "same_question_source_match"
    elif same_source:
        prior_scope = "same_source_context"
    elif _safe_get(prior, "origin_type") == "bootstrap_fixture":
        prior_scope = "bootstrap_fixture"
    elif not _safe_get(prior, "run_id", "origin_run_id", "track_id", "origin_track_id"):
        prior_scope = "unknown"

    return prior_scope, same_question, same_bundle, same_source


def _allowed_use_and_reason(prior_scope: str, same_question: bool, same_bundle: bool, same_source: bool, prior: dict) -> tuple[str, str]:
    has_provenance = bool(
        _safe_get(prior, "run_id", "origin_run_id")
        and _safe_get(prior, "track_id", "origin_track_id")
        and _safe_get(prior, "origin_type", "source_id", "source_label")
    )

    if same_question and (same_bundle or same_source):
        return "shadow_only", "same-question and same-bundle/source prior; circularity guard enforced"
    if same_source:
        if has_provenance:
            return "context_only", "same source with different question; usable only for contextual guidance"
        return "shadow_only", "same source but provenance incomplete; shadow-only fallback"
    if prior_scope == "unknown" or not has_provenance:
        return "shadow_only", "unknown or unverifiable provenance; disallow direct answer support"
    if prior_scope == "bootstrap_fixture":
        return "cite_if_verified", "bootstrap fixture provenance requires independent verification before citation"
    return "answer_support", "different source with verified provenance"


def _enrich_match_with_provenance(query: dict, match: dict) -> dict:
    prior = match.get("prior", {})
    prior_scope, same_question, same_bundle, same_source = _classify_prior_scope(query, prior)
    allowed_use, retrieval_reason = _allowed_use_and_reason(
        prior_scope=prior_scope,
        same_question=same_question,
        same_bundle=same_bundle,
        same_source=same_source,
        prior=prior,
    )

    prior_origin_run_id = _safe_get(prior, "origin_run_id", "run_id")
    prior_origin_track_id = _safe_get(prior, "origin_track_id", "track_id")
    prior_origin_type = _safe_get(prior, "origin_type")
    prior_question_sha256 = _safe_get(prior, "question_sha256") or _sha256_text(_to_text(prior.get("question_text")).lower())
    prior_bundle_normalized_sha256 = _safe_get(prior, "bundle_normalized_sha256", "normalized_sha256")
    if not prior_bundle_normalized_sha256:
        prior_bundle_normalized_sha256 = _normalized_bundle_sha256(
            {
                "source_label": prior.get("source_label"),
                "source_terms": prior.get("source_terms", []),
                "source_variables": prior.get("source_variables", []),
                "source_constraints": prior.get("source_constraints", []),
            }
        )

    provenance_hash = _sha256_text(
        "|".join(
            [
                str(prior_origin_run_id),
                str(prior_origin_track_id),
                str(prior_origin_type),
                str(prior_question_sha256),
                str(prior_bundle_normalized_sha256),
                str(match.get("similarity_score", 0.0)),
            ]
        )
    )

    enriched = dict(match)
    enriched.update(
        {
            "prior_scope": prior_scope,
            "prior_origin_run_id": prior_origin_run_id,
            "prior_origin_track_id": prior_origin_track_id,
            "prior_origin_type": prior_origin_type,
            "prior_question_sha256": prior_question_sha256,
            "prior_bundle_normalized_sha256": prior_bundle_normalized_sha256,
            "same_question": same_question,
            "same_bundle": same_bundle,
            "same_source": same_source,
            "allowed_use": allowed_use,
            "retrieval_reason": retrieval_reason,
            "provenance_hash": provenance_hash,
        }
    )
    return enriched


def _build_injection_decision_trace(matches: list[dict]) -> tuple[list[dict], list[str]]:
    decisions = []
    trace = []
    for item in matches:
        decided_use = item.get("allowed_use", "shadow_only")
        reason = item.get("retrieval_reason", "")
        if item.get("same_question") and (item.get("same_bundle") or item.get("same_source")):
            decided_use = "shadow_only" if item.get("same_bundle") else "context_only"
            reason = "downgraded to prevent same-question same-source prior reinforcement loop"

        decisions.append(
            {
                "provenance_hash": item.get("provenance_hash"),
                "prior_scope": item.get("prior_scope"),
                "allowed_use": decided_use,
                "reason": reason,
            }
        )
        trace.append(f"{item.get('provenance_hash')}: {reason}")
    return decisions, trace


def build_atlas_prior_packet(query: dict) -> dict:
    raw_matches = retrieve_relevant_priors(query)
    matches = [_enrich_match_with_provenance(query, match) for match in raw_matches]
    prior_injection_decision, prior_injection_trace = _build_injection_decision_trace(matches)

    return {
        "question_text": query.get("question_text", ""),
        "source_label": query.get("source_label"),
        "source_terms": query.get("source_terms", []),
        "source_variables": query.get("source_variables", []),
        "source_constraints": query.get("source_constraints", []),
        "match_count": len(matches),
        "matches": matches,
        "selected_priors": matches,
        "prior_injection_decision": prior_injection_decision,
        "prior_injection_trace": prior_injection_trace,
        "prior_packet_ready": len(matches) > 0,
        "retrieval_mode": "question_plus_source_evidence",
    }
