from pathlib import Path
import json
import re


ATLAS_STORE = Path(r"C:\UVLM\uvlm-publications\atlas_store")


def _tokens(text: str) -> set[str]:
    toks = re.findall(r"[A-Za-z][A-Za-z0-9_\-]{2,}", (text or "").lower())
    stop = {
        "the", "and", "for", "with", "what", "which", "when", "where", "why",
        "how", "that", "this", "from", "into", "your", "their", "they", "are",
        "was", "were", "but", "can", "could", "should", "would", "have", "has"
    }
    return {t for t in toks if t not in stop}


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


def retrieve_relevant_priors(question_text: str, top_k: int = 3) -> list[dict]:
    priors = load_existing_priors()
    q_tokens = _tokens(question_text)

    scored = []
    for prior in priors:
        p_tokens = _tokens(prior.get("ai_output", "")) | _tokens(prior.get("question_text", ""))
        sim = _jaccard(q_tokens, p_tokens)
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


def build_atlas_prior_packet(question_text: str) -> dict:
    matches = retrieve_relevant_priors(question_text)

    return {
        "question_text": question_text,
        "match_count": len(matches),
        "matches": matches,
        "prior_packet_ready": len(matches) > 0,
    }
