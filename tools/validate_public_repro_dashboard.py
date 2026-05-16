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
    "SONYA-ADAPTER-SMOKE-00",
    "SONYA-LOCAL-FIXTURE-ADAPTER-01",
    "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
    "SONYA-LOCAL-FIXTURE-ADAPTER-02",
    "SONYA-LOCAL-FIXTURE-ADAPTER-03",
    "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02",
    "RW-COMP-LOCAL-ADAPTER-01",
    "PMR-00-PROVENANCE-MEMORY-RESERVOIR",
    "PMR-01-LOCAL-ARTIFACT-INDEX",
    "PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY",
    "PMR-03-LIFECYCLE-STATE-MACHINE",
    "PMR-04-LIFECYCLE-AUDIT-PREFLIGHT",
    "PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW",
    "PMR-06-USER-CONFIRMATION-PREFLIGHT",
    "PMR-07-USER-CONFIRMATION-NEGATIVE-CONTROL",
    "PMR-08-VALID-USER-CONFIRMATION-RECEIPT-SCAFFOLD",
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
    "Sonya Adapter Smoke",
    "exercises contracts, not live adapters",
    "not live adapter execution",
    "not network authorization",
    "not remote provider call",
    "not model weight training",
    "raw output rejected",
    "candidate packet",
    "failure receipts",
    "telemetry events",
    "provenance events",
    "Sonya Local Fixture Adapter",
    "deterministic local fixtures",
    "not live adapters",
    "not live adapter execution",
    "not network authorization",
    "not remote provider call",
    "not model weight training",
    "candidate packets",
    "failure receipts",
    "telemetry events",
    "provenance events",
    "Adapter output is not accepted as cognition directly.",
    "Local adapter candidates become reviewable only through the Evidence Review Pack path.",
    "Evidence Review Pack local-adapter route",
    "not accepted evidence",
    "not adapter authorization",
    "Candidate packets require UCC-controlled review.",
    "The claim map is not truth certification.",
    "The candidate is not final answer.",
    "Selection policy is not final answer.",
    "Multi-adapter local fixture selection still requires Evidence Review Pack review.",
    "Sonya Local Fixture Adapter multi-route",
    "not adapter authorization",
    "not model quality benchmark",
    "Source fixture references are not stale identity leakage.",
    "Nested SONYA-LOCAL-FIXTURE-ADAPTER-01 references are source fixture dependencies, not stale identity leakage.",
    "Current route identity is explicit.",
    "Source fixture identity is explicit.",
    "Evidence Review Pack local-adapter route references are explicit.",
    "Lineage does not grant authority.",
    "Sonya local adapter lineage packet is not adapter execution.",
    "Sonya local adapter lineage packet is not network authorization.",
    "Sonya local adapter lineage packet is not memory write.",
    "Sonya local adapter lineage packet is not final answer release.",
    "Sonya local adapter lineage packet is not deployment authority.",
    "Sonya local adapter lineage packet is not truth certification.",
    "Deltas are structural review descriptors, not hallucination reduction proof.",
    "Revised local adapter candidate remains candidate-only, not accepted evidence.",
    "Evidence Review Pack local-adapter revision loop is not final answer selection.",
    "Evidence Review Pack local-adapter revision loop is not model quality benchmark.",
    "Evidence Review Pack local-adapter revision loop is not model superiority proof.",
    "Evidence Review Pack local-adapter revision loop is not adapter authorization.",
    "Evidence Review Pack local-adapter revision loop is not memory write.",
    "Evidence Review Pack local-adapter revision loop is not model-weight training.",
    "Evidence Review Pack local-adapter revision loop is not deployment authority.",
    "Evidence Review Pack local-adapter revision loop is not recursive self-improvement.",
    "Deltas are structural review descriptors only.",
    "RW-COMP local-adapter comparison is not hallucination reduction proof or a model quality benchmark.",
    "RW-COMP local-adapter comparison is not model superiority proof.",
    "RW-COMP local-adapter comparison is not final answer selection.",
    "RW-COMP local-adapter comparison is not accepted evidence.",
    "RW-COMP local-adapter comparison is not adapter authorization.",
    "RW-COMP local-adapter comparison is not memory write.",
    "RW-COMP local-adapter comparison is not model-weight training.",
    "RW-COMP local-adapter comparison is not deployment authority.",
    "RW-COMP local-adapter comparison is not recursive self-improvement.",
    "Memory is governed provenance under resource constraints.",
    "Memory is not storage.",
    "Hash is not encryption.",
    "User controls local memory budget.",
    "PMR is not Atlas canon.",
    "PMR is not model-weight training data.",
    "PMR artifact index is not generic cache.",
    "PMR artifact lifecycle state is not truth status.",
    "PMR dependency graph is not canon graph.",
    "PMR-01 performs indexing only, not pruning.",
    "Federation is blocked by default.",
    "PMR is not resource economy or token economy.",
    "GPCU is lifecycle/storage utility, not truth score.",
    "GPCU is not reward entitlement.",
    "GPCU is not token economy.",
    "Lifecycle recommendation is not pruning.",
    "Reward mechanics are deferred.",
    "Federation remains blocked by default.",
    "PMR-02 is not Atlas canon.",
    "PMR-02 is not memory write authorization.",
    "PMR-02 is not model-weight training.",
    "PMR-02 is not deployment authority.",
    "PMR-02 is not hallucination reduction proof.",
    "Recommendation is not transition; transition candidate is not action.",
    "Recommendation is not transition.",
    "Transition candidate is not action.",
    "Lifecycle state is not truth status.",
    "Destructive action requires future Sophia lifecycle audit.",
    "Destructive action requires future user confirmation.",
    "No pruning or deletion occurs in PMR-03.",
    "PMR-03 is not federation authorization.",
    "PMR-03 is not reward entitlement.",
    "PMR-03 is not token economy.",
    "PMR-03 is not Atlas canon.",
    "PMR-03 is not memory write authorization.",
    "PMR-03 is not model-weight training.",
    "PMR-03 is not deployment authority.",
    "PMR-03 is not truth certification.",
    "Preflight is not approval.",
    "Audit candidate is not action.",
    "Sophia lifecycle audit is required before destructive action.",
    "User confirmation is required before destructive local action.",
    "No Sophia approval packet is emitted.",
    "No pruning or deletion occurs in PMR-04.",
    "PMR-04 is not federation authorization.",
    "PMR-04 is not reward entitlement.",
    "PMR-04 is not token economy.",
    "PMR-04 is not memory write authorization.",
    "PMR-04 is not deployment authority.",
    "PMR-04 is not truth certification.",
    "Sophia review is not Sophia approval.",
    "Audit recommendation is not action.",
    "No Sophia approval packet is emitted.",
    "Destructive action requires future Sophia approval.",
    "Destructive action requires future user confirmation.",
    "No pruning or deletion occurs in PMR-05.",
    "PMR-05 is not federation authorization.",
    "PMR-05 is not reward entitlement.",
    "PMR-05 is not token economy.",
    "PMR-05 is not Atlas canon.",
    "PMR-05 is not memory write authorization.",
    "PMR-05 is not model-weight training.",
    "PMR-05 is not deployment authority.",
    "PMR-05 is not truth certification.",
    "User confirmation request is not user confirmation.",
    "User confirmation is not action.",
    "No user confirmation receipt is emitted.",
    "Destructive action requires future Sophia approval.",
    "Destructive action requires future user confirmation.",
    "No pruning or deletion occurs in PMR-06.",
    "PMR-06 is not Sophia approval.",
    "PMR-06 is not federation authorization.",
    "PMR-06 is not reward entitlement.",
    "PMR-06 is not token economy.",
    "PMR-06 is not Atlas canon.",
    "PMR-06 is not memory write authorization.",
    "PMR-06 is not model-weight training.",
    "PMR-06 is not deployment authority.",
    "PMR-06 is not truth certification.",
    "Invalid confirmation is not confirmation.",
    "Missing confirmation is not confirmation.",
    "Ambiguous confirmation is not confirmation.",
    "Forged confirmation is not confirmation.",
    "Expired confirmation is not confirmation.",
    "Scope-mismatched confirmation is not confirmation.",
    "Confirmation without Sophia approval is insufficient.",
    "Confirmation cannot override retain-lock, quarantine, revocation, or dependency blocks.",
    "No user confirmation receipt is emitted in PMR-07.",
    "No pruning or deletion occurs in PMR-07.",
    "PMR-07 is not Sophia approval.",
    "PMR-07 is not federation authorization.",
    "PMR-07 is not reward entitlement.",
    "PMR-07 is not token economy.",
    "PMR-07 is not Atlas canon.",
    "PMR-07 is not memory write authorization.",
    "PMR-07 is not model-weight training.",
    "PMR-07 is not deployment authority.",
    "PMR-07 is not truth certification.",
    "Valid user confirmation receipt is not action.",
    "Confirmation authorizes eligibility for later action review, not action itself.",
    "Scope validation is not action.",
    "Destructive action still requires future Sophia approval.",
    "Destructive action still requires future explicit action request.",
    "Negative-control invalid confirmations remain blocked.",
    "No pruning or deletion occurs in PMR-08.",
    "PMR-08 is not federation authorization.",
    "PMR-08 is not reward entitlement.",
    "PMR-08 is not token economy.",
    "PMR-08 is not Atlas canon.",
    "PMR-08 is not memory write authorization.",
    "PMR-08 is not model-weight training.",
    "PMR-08 is not deployment authority.",
    "PMR-08 is not truth certification.",
    "Governed provenance resources may be future infrastructure rewards, but truth is not for sale.",
)
FORBIDDEN_PHRASES = (
    "deployment readiness",
    "deployment ready",
    "truth certification",
    "truth certified",
    "final answer authority",
    "final answer selection",
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
    "model quality benchmark",
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
    "claims deployment authority",
    "final answer released",
    "publisher finalized",
    "omega detected",
    "canon adopted",
    "memory written",
    "publication claim authorized",
    "recursive self-improvement achieved",
    "claims accepted evidence",
    "claims adapter authorization",
    "adapter authorization",
    "adapter authorized",
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
    "remote provider calls",
    "live model executed",
    "model weights trained",
    "model weight training",
    "production ready",
    "production readiness",
    "lineage authority",
    "lineage grants authority",
    "stale identity proof of execution",
    "hallucination reduction proof",
    "model quality benchmark",
    "Atlas canon",
    "memory write authorization",
    "federation authorization",
    "pruning execution",
    "resource economy",
    "token economy",
    "truth score",
    "reward entitlement",
    "human value score",
    "deletion execution",
    "encrypted shard transfer",
    "claims destructive action",
    "claims valid user confirmation",
    "user confirmation execution",
    "claims user confirmation receipt",
    "claims user confirmation",
    "Sophia approval",
    "audit action",
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


def _is_allowed_local_adapter_context(text: str, index: int) -> bool:
    window = text[max(0, index - 48) : index]
    return any(
        marker in window
        for marker in (
            "local fixture ",
            "local only fixture ",
            "local only ",
            "local ",
            "fixture adapter ",
            "fixture only ",
            "deterministic local ",
        )
    )


def _forbidden_hits(text: str) -> list[str]:
    hits: list[str] = []
    for phrase in FORBIDDEN_PHRASES:
        normalized_phrase = _normalize(phrase)
        start = 0
        while True:
            index = text.find(normalized_phrase, start)
            if index == -1:
                break
            if (
                phrase in {"adapter execution", "adapter executed"}
                and _is_allowed_local_adapter_context(text, index)
                and "lineage claims" not in text[max(0, index - 80) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "Sophia approval"
                and (
                    "requires future " in text[max(0, index - 32) : index]
                    or "without " in text[max(0, index - 32) : index]
                    or "missing " in text[max(0, index - 16) : index]
                    or text[index : index + 40].startswith("sophia approval missing")
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "token economy"
                and (
                    "does not prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 104) : index]
                    or "does not approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 112) : index]
                    or "does not confirm, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 122) : index]
                    or "does not perform destructive action, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 142) : index]
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "model quality benchmark"
                and "not hallucination reduction proof or a" in text[max(0, index - 56) : index]
            ):
                start = index + len(normalized_phrase)
                continue
            if phrase == "federation" and (
                text[index : index + 40].startswith("federation is blocked by default")
                or text[index : index + 48].startswith("federation remains blocked by default")
                or text[index : index + 40].startswith("federation_blocked")
                or text[index : index + 40].startswith("federation_authorization")
                or text[index : index + 40].startswith("federation = true")
                or text[index : index + 40].startswith('federation": true')
            ):
                start = index + len(normalized_phrase)
                continue
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
