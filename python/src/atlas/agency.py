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


def compare_candidate(candidate: dict) -> dict:
    existing = load_existing_priors()

    cand_tokens = _tokens(candidate.get("ai_output", ""))
    best_match = None
    best_score = -1.0

    for item in existing:
        item_tokens = _tokens(item.get("ai_output", ""))
        sim = _jaccard(cand_tokens, item_tokens)
        if sim > best_score:
            best_score = sim
            best_match = item

    novelty_score = 1.0 - max(best_score, 0.0)

    return {
        "has_existing_priors": len(existing) > 0,
        "most_similar_track_id": best_match.get("track_id") if best_match else None,
        "most_similar_question": best_match.get("question_text") if best_match else None,
        "similarity_score": best_score if best_match else 0.0,
        "novelty_against_atlas_score": novelty_score,
        "prior_count_compared": len(existing),
    }


def adjudicate_candidate(candidate: dict) -> dict:
    cmp = compare_candidate(candidate)

    decision = "hold"
    reason = "Candidate is too similar to existing Atlas priors."

    if cmp["novelty_against_atlas_score"] >= 0.35:
        decision = "store"
        reason = "Candidate is sufficiently distinct from existing Atlas priors."
    elif cmp["novelty_against_atlas_score"] >= 0.2:
        decision = "merge_or_review"
        reason = "Candidate has partial novelty and may extend an existing prior."

    return {
        "atlas_decision": decision,
        "atlas_reason": reason,
        "comparison": cmp,
    }


def persist_candidate(candidate: dict) -> str | None:
    adjudication = adjudicate_candidate(candidate)

    if adjudication["atlas_decision"] != "store":
        return None

    ATLAS_STORE.mkdir(parents=True, exist_ok=True)
    track_id = candidate.get("track_id", "unknown_track")
    out_path = ATLAS_STORE / f"{track_id}.json"

    payload = dict(candidate)
    payload["atlas_adjudication"] = adjudication

    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(out_path)
