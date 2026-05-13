#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_PHASES = {
    "EXP-SUITE-REGISTRY-01",
    "EXP-SUITE-REPRO-01",
    "WAVE-FAMILY-CLOSEOUT-01",
    "SONYA-INGRESS-HARDEN-03",
    "SOPHIA-UCC-ROUTE-01",
    "PUB-GOV-ARTIFACT-COG-01",
    "PUB-WAVE-ROSETTA-01",
    "UNI-02D-SONYA-GATE-01",
    "RETRO-LANE-00",
    "PUBLIC-UTILITY-ALPHA-00",
    "RAW-BASELINE-COMPARISON-00",
    "EVIDENCE-REVIEW-PACK-00",
    "RW-COMP-01",
    "RW-COMP-02",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01",
    "EVIDENCE-REVIEW-PACK-01",
    "RW-COMP-03",
    "UNIVERSAL-STAGE-PIPELINE-00",
    "ARTIFACT-CONTRACT-REGISTRY-01",
    "UNIVERSAL-COMPATIBILITY-MATRIX-00",
    "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
}
REQUIRED_BOUNDARY_PHRASES = (
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "local fixture only",
    "requires external peer review",
    "route is not authorization",
    "receipt is not truth certification",
    "candidate is not answer",
    "admission is not execution",
    "dashboard is not deployment authority",
    "public utility alpha",
    "local reviewer demo",
    "not live model execution",
    "not live adapter execution",
    "not remote provider call",
    "not federation",
    "not recursive braid",
    "raw baseline comparison",
    "fixture-only measurement scaffold",
    "not hallucination reduction proof",
    "not model quality benchmark",
    "evidence review pack",
    "AI review that shows its work",
    "not legal advice",
    "not medical advice",
    "not tax advice",
    "not compliance certification",
    "not live model execution",
    "not production evaluation",
    "RW-COMP-01",
    "fixture-only comparison scaffold",
    "not model superiority proof",
    "not model quality benchmark",
    "not live model evaluation",
    "not professional advice",
    "not compliance certification",
    "RW-COMP-02",
    "deterministic multi-fixture comparison battery",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01",
    "candidate repair",
    "not canon adoption",
    "not memory write",
    "not final answer release",
    "not Publisher finalization",
    "not Omega detection",
    "not deployment authority",
    "not recursive self-improvement",
    "EVIDENCE-REVIEW-PACK-01",
    "candidate revision",
    "not accepted evidence",
    "not canon adoption",
    "not memory write",
    "not final answer release",
    "not Publisher finalization",
    "not Omega detection",
    "not deployment authority",
    "not recursive self-improvement",
    "not hallucination reduction proof",
    "RW-COMP-03",
    "held-out blinded fixture scaffold",
    "not hallucination reduction proof",
    "not model superiority proof",
    "not live model evaluation",
    "not live human study",
    "simulated scores",
    "not accepted evidence",
    "not production evaluation",
    "universal architecture scaffold",
    "The brain runs cognition stages; experiments configure those stages.",
    "profiles are configuration",
    "experiments are configurations",
    "fail-closed receipts",
    "hash-only",
    "not product release",
    "not experiment result",
    "not benchmark result",
    "not hallucination reduction proof",
    "not deployment authority",
    "not recursive self-improvement",
    "Sonya Adapter Contract Registry",
    "Adapter capability is not adapter authorization",
    "all adapters disabled or blocked",
    "not adapter execution",
    "not network authorization",
    "not remote provider call",
    "not model weight training",
    "raw output is forbidden",
    "candidate packet required",
    "failure receipts required",
)
FORBIDDEN_PHRASES = (
    "deployment readiness",
    "deployment ready",
    "truth certification",
    "truth certified",
    "final answer authority",
    "final answer release",
    "universal ontology claim",
    "ai consciousness",
    "retrosynthesis runtime",
    "universal portability proof",
    "live model execution",
    "live adapter execution",
    "remote provider call",
    "federation",
    "recursive braid",
    "recursive federation",
    "psychoacoustic proof",
    "omega detection",
    "publisher finalization",
    "hallucination reduction proven",
    "model quality benchmark",
    "model superiority proven",
    "model superiority proof",
    "hallucination reduction proof",
    "live model evaluation",
    "remote provider evaluation",
    "professional advice",
    "legally compliant",
    "legal advice",
    "medical advice",
    "tax advice",
    "compliance certification",
    "production ready",
    "deployment authorized",
    "final answer released",
    "publisher finalized",
    "omega detected",
    "canon adopted",
    "memory written",
    "publication claim authorized",
    "recursive self-improvement achieved",
    "claims accepted evidence",
    "claims canon adoption",
    "claims memory write",
    "claims final answer release",
    "claims Publisher finalization",
    "claims Omega detection",
    "claims recursive self-improvement",
    "live human study performed",
    "claims live human study",
    "claims accepted evidence",
    "canon adoption",
    "memory write",
    "production evaluation",
    "product release",
    "product released",
    "benchmark result",
    "benchmark proven",
    "experiment result",
    "AI consciousness demonstrated",
    "adapter executed",
    "adapter execution",
    "network authorized",
    "network authorization",
    "remote provider called",
    "live model executed",
    "model weights trained",
    "model weight training",
    "production ready",
    "production readiness",
)
ALLOWED_NEGATED = (
    "not ",
    "no ",
    "without ",
    "does not ",
    "is not ",
    "not a ",
    "not an ",
)


def _normalize(value: str) -> str:
    return " ".join(value.lower().replace("-", " ").split())


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def _read_docs(docs_dir: Path) -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(docs_dir.rglob("*.md"))
    )


def _is_negated(text: str, index: int) -> bool:
    window = text[max(0, index - 24) : index]
    return any(marker in window for marker in ALLOWED_NEGATED)


def _forbidden_hits(text: str) -> list[str]:
    hits: list[str] = []
    for phrase in FORBIDDEN_PHRASES:
        normalized_phrase = _normalize(phrase)
        start = 0
        while True:
            index = text.find(normalized_phrase, start)
            if index == -1:
                break
            if not _is_negated(text, index):
                hits.append(phrase)
                break
            start = index + len(normalized_phrase)
    return hits


def validate_dashboard(dashboard_path: Path, docs_dir: Path) -> dict[str, Any]:
    dashboard = _read_json(dashboard_path)
    accepted = dashboard.get("accepted_phases", [])
    accepted_ids = {p.get("phase_id") for p in accepted if isinstance(p, dict)}
    missing = sorted(REQUIRED_PHASES - accepted_ids)

    text = _normalize(json.dumps(dashboard, ensure_ascii=False) + "\n" + _read_docs(docs_dir))
    missing_boundaries = [
        phrase for phrase in REQUIRED_BOUNDARY_PHRASES if _normalize(phrase) not in text
    ]
    forbidden = _forbidden_hits(text)

    truthy_bad_flags = [
        key
        for key in ("deployment_ready", "truth_certified", "final_answer_authority")
        if dashboard.get(key) is True
    ]

    status_ok = (
        dashboard.get("dashboard_status") == "draft_public_review"
        and dashboard.get("requires_external_peer_review") is True
        and dashboard.get("not_truth_certification") is True
        and dashboard.get("not_deployment_authority") is True
        and dashboard.get("not_final_answer_release") is True
        and dashboard.get("not_ai_consciousness_claim") is True
        and dashboard.get("not_universal_ontology_claim") is True
    )
    passed = not missing and not missing_boundaries and not forbidden and not truthy_bad_flags and status_ok
    return {
        "dashboard_id": "PUBLIC-REPRO-DASHBOARD-01",
        "passed": passed,
        "accepted_phases_present": sorted(accepted_ids),
        "missing_accepted_phases": missing,
        "missing_claim_boundary_phrases": missing_boundaries,
        "forbidden_claims_found": forbidden,
        "bad_truthy_flags": truthy_bad_flags,
        "status_ok": status_ok,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate public repro dashboard claim boundaries.")
    parser.add_argument("--dashboard", required=True, type=Path)
    parser.add_argument("--docs-dir", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    result = validate_dashboard(args.dashboard, args.docs_dir)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
