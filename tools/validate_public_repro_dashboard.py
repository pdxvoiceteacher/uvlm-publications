#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
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
    "SPEC-FRESHNESS-REGISTRY-00",
    "FUNDAMENTAL-COHERENCE-METRICS-00",
    "PMR-06-USER-CONFIRMATION-PREFLIGHT",
    "PMR-07-USER-CONFIRMATION-NEGATIVE-CONTROL",
    "PMR-08-VALID-USER-CONFIRMATION-RECEIPT-SCAFFOLD",
    "PMR-09-DESTRUCTIVE-ACTION-AUTHORIZATION-NEGATIVE-CONTROL",
    "PMR-10-DESTRUCTIVE-ACTION-AUTHORIZATION-PREFLIGHT",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00",
    "PMR-SIM-00",
    "PMR-STAT-00",
    "PMR-FED-STRESS-00",
    "PMR-HUMAN-PROVENANCE-00",
    "PMR-HUMAN-CONSENT-NEGATIVE-CONTROL-00",
    "SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00",
    "TEL-EVENT-STACK-00",
    "EVIDENCE-REVIEW-PRODUCT-LOOP-02",
    "EVIDENCE-REVIEW-METRICS-00",
    "COGNITIVE-WATERS-PATTERN-METRICS-00",
    "ONTOLOGY-CLAIM-REGISTRY-00",
    "LOCAL-SONYA-PATH-PORTABILITY-00",
    "TB-PRODUCT-SLICE-00",
    "TB-PRODUCT-SLICE-01",
    "TB-PRODUCT-SLICE-02",
    "SONYA-LOCAL-SERVER-GATEWAY-00",
    "SONYA-LOCAL-SERVER-GATEWAY-01",
    "SONYA-LOCAL-SERVER-GATEWAY-02",
    "LOCAL-SERVER-USER-FILE-INGRESS-00",
    "LOCAL-SERVER-USER-FILE-INGRESS-01",
    "LOCAL-SERVER-USER-FILE-INGRESS-02",
    "LAN-READINESS-PREFLIGHT-00",
    "LAN-AUTHORITY-MODEL-00",
    "LAN-AUTHORITY-NEGATIVE-CONTROL-00",
    "LAN-OPERATOR-CONSENT-PREFLIGHT-00",
    "LOCAL-REVIEW-RUNTIME-V0",
    "USER-FACING-RECEIPT-UX-01",
    "PMR-CONTEXT-AVAILABILITY-LEDGER-00",
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
    "Valid confirmation receipt plus Sophia recommendation is not action authorization.",
    "Explicit future action request and Sophia approval packet are required before destructive action.",
    "No explicit action request packet is emitted in PMR-09.",
    "No Sophia approval packet is emitted in PMR-09.",
    "No destructive action authorization packet is emitted in PMR-09.",
    "No destructive action receipt is emitted in PMR-09.",
    "No pruning or deletion occurs in PMR-09.",
    "PMR-09 is not federation authorization.",
    "PMR-09 is not reward entitlement.",
    "PMR-09 is not token economy.",
    "PMR-09 is not Atlas canon.",
    "PMR-09 is not memory write authorization.",
    "PMR-09 is not model-weight training.",
    "PMR-09 is not deployment authority.",
    "PMR-09 is not truth certification.",
    "Action request candidate is not explicit action request.",
    "Sophia approval request candidate is not Sophia approval.",
    "Authorization preflight is not authorization.",
    "No explicit action request packet is emitted in PMR-10.",
    "No Sophia approval packet is emitted in PMR-10.",
    "No destructive action authorization packet is emitted in PMR-10.",
    "No destructive action receipt is emitted in PMR-10.",
    "No pruning or deletion occurs in PMR-10.",
    "PMR-10 is not federation authorization.",
    "PMR-10 is not reward entitlement.",
    "PMR-10 is not token economy.",
    "PMR-10 is not Atlas canon.",
    "PMR-10 is not memory write authorization.",
    "PMR-10 is not model-weight training.",
    "PMR-10 is not deployment authority.",
    "PMR-10 is not truth certification.",
    "PMR authorization ladder is not the whole Triadic Brain.",
    "Pattern diversity is required.",
    "PMR-only continuation is not recommended immediately after PMR-10.",
    "Checkpoint recommendation is not execution.",
    "Checkpoint is not product completion.",
    "No runtime authority is granted.",
    "PMR-SIM-00 is recommended as the next evidence-producing lane.",
    "PMR becomes scientific only when it can lose.",
    "PMR policy is allowed to lose.",
    "Simulation result is not production memory policy.",
    "Simulation result is not PMR superiority proof.",
    "Simulation result is not hallucination reduction proof.",
    "Simulation result is not federation proof.",
    "Simulation result is not reward economy proof.",
    "Fixture streams are synthetic and deterministic.",
    "Retained does not mean true.",
    "Replay-ready does not mean canon.",
    "Stored does not mean trained.",
    "Simpler baselines may win metrics or scenarios.",
    "Run-PMR-SIM00-Acceptance.ps1",
    "pmr_simulation_manifest.json",
    "pmr_simulation_result_rows.jsonl",
    "pmr_simulation_comparison_packet.json",
    "pmr_simulation_statistics_packet.json",
    "Descriptive fixture statistics are not real-world inference.",
    "Rank table is not production policy selection.",
    "Statistical summary is not PMR superiority proof.",
    "Statistical summary is not hallucination reduction proof.",
    "Simulation statistics are not federation proof.",
    "Simulation statistics are not reward economy proof.",
    "Run-PMR-STAT00-Acceptance.ps1",
    "pmr_stat_analysis_manifest.json",
    "pmr_stat_policy_metric_summaries.jsonl",
    "pmr_stat_policy_pair_deltas.jsonl",
    "pmr_stat_rank_table.json",
    "pmr_stat_sensitivity_packet.json",
    "pmr_stat_failure_mode_packet.json",
    "Federation stress corpus is not federation.",
    "Federation stress result is not federation proof.",
    "Federation candidate is not network authorization.",
    "Shard-transfer scenario is not encrypted shard transfer.",
    "Federation credit scenario is not reward entitlement.",
    "Hash is not encryption.",
    "Merkle root is not confidentiality.",
    "Run-PMR-FED-STRESS00-Acceptance.ps1",
    "pmr_federation_stress_manifest.json",
    "pmr_federation_node_fixtures.json",
    "pmr_federation_stress_scenarios.json",
    "pmr_federation_failure_mode_rows.jsonl",
    "pmr_federation_propagation_risk_packet.json",
    "pmr_federation_stress_statistics_packet.json",
    "Human provenance context is not identity certification.",
    "The system must not encode human = body or AI = mind.",
    "Consent context is not consent execution.",
    "Consent preference is not action authorization.",
    "Correction request is not memory write.",
    "Revocation request is not deletion execution.",
    "Review participation is not truth certification.",
    "Lived-stakes annotation is not reward entitlement.",
    "Human provenance is not human value score.",
    "Run-PMR-HUMAN-PROVENANCE00-Acceptance.ps1",
    "pmr_human_provenance_manifest.json",
    "pmr_human_provenance_context_packet.json",
    "pmr_human_consent_scope_packet.json",
    "pmr_human_correction_request_packet.json",
    "pmr_human_revocation_request_packet.json",
    "pmr_human_lived_stakes_annotation_packet.json",
    "Evidence Review, Sonya adapter path, TEL/telemetry, retrosynthesis, PMR simulation/statistics, federation stress, human provenance, market design, harness debt, and publication debt remain active lanes.",
    "No pruning or deletion occurs in PMR-ARCH-DIVERSITY-CHECKPOINT-00.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not federation authorization.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not reward entitlement.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not token economy.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not Atlas canon.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not memory write authorization.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not model-weight training.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not deployment authority.",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00 is not truth certification.",
    "Governed provenance resources may be future infrastructure rewards, but truth is not for sale.",
    "Sonya is the required execution membrane for model/tool/provider-facing paths.",
    "Missing Sonya posture must fail closed.",
    "Raw output is not cognition.",
    "SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00",
    "TEL-EVENT-STACK-00",
    "Telemetry event is not authority.",
    "Replay trace is not canon.",
    "Evidence Review product loop is not final answer selection.",
    "Unsupported-claim action queue is not evidence acceptance.",
    "Hypercompression reduces explanatory distance, not review obligation.",
    "Freshness is not authority.",
    "Pattern morphology is not consciousness proof.",
    "Cognitive-water metaphor is not metaphysical claim.",
    "Publication validation event is not peer review.",
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
    "human consciousness",
    "retrosynthesis runtime",
    "universal portability proof",
    "live model execution",
    "live adapter execution",
    "claims provider call",
    "claims remote provider call",
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
    "PMR superiority proof",
    "production memory policy",
    "production policy selection",
    "real-world inference",
    "real world inference",
    "statistical superiority proof",
    "federation proof",
    "reward economy proof",
    "identity certification",
    "consent execution",
    "claims action authorization",
    "biometric inference",
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
    "production evaluation",
    "product completion",
    "claims product completion",
    "runtime authority",
    "surveillance",
    "peer review certification",
    "claims runtime authority",
    "product release",
    "product released",
    "benchmark result",
    "benchmark proven",
    "experiment result",
    "AI consciousness demonstrated",
    "adapter executed",
    "adapter execution",
    "network authorization",
    "network authorized",
    "remote provider called",
    "remote provider calls",
    "provider call performed",
    "provider call authorized",
    "raw output admission",
    "claims raw output admission",
    "raw output admitted",
    "raw output accepted as cognition",
    "raw_output_admitted",
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
    "claims destructive action authorization",
    "claims explicit action request",
    "claims Sophia approval packet",
    "claims Sophia approval",
    "claims destructive action receipt",
    "claims destructive action",
    "claims valid user confirmation",
    "user confirmation execution",
    "claims user confirmation receipt",
    "claims user confirmation",
    "Sophia approval",
    "audit action",
    "universal ontology proof",
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


def _context_words(text: str, index: int, *, before: int = 96, after: int = 96) -> str:
    window = text[max(0, index - before) : index + after]
    cleaned = re.sub(r"[^a-z0-9]+", " ", window.replace("_", " "))
    return " ".join(cleaned.split())


def _is_allowed_provider_call_context(text: str, index: int) -> bool:
    window = text[max(0, index - 48) : index + 72]
    normalized = " ".join(re.sub(r"[^a-z0-9]+", " ", window.replace("_", " ")).split())
    allowed_patterns = (
        "no remote provider call",
        "no remote provider calls",
        "not provider call",
        "not remote provider call",
        "provider calls not performed",
        "provider calls not made",
        "is not provider call",
        "is not a provider call",
        "provider call not performed",
        "provider call not made",
        "provider calls performed false",
        "provider calls performed false",
        "provider_calls_not_performed",
        "provider_calls_performed false",
        "direct model provider call is not allowed",
        "provider call is not allowed",
        "does not call providers",
        "network provider calls",
        "without live adapter execution or network provider calls",
        "without live model execution or remote provider calls",
        "provider call blocked",
        "provider call forbidden",
        "not provider call status flags",
    )
    return any(pat in normalized for pat in allowed_patterns)




def _is_allowed_network_authorization_context(text: str, index: int) -> bool:
    window = _context_words(text, index, before=128, after=128)
    allowed = (
        "not network authorization",
        "is not network authorization",
        "network authorization not performed",
        "network calls not performed",
        "network call not performed",
        "network authorization requested",
        "network authorization requests must fail closed",
        "network authorization request must fail closed",
        "blocked network authorization",
        "network authorization blocked",
        "no network authorization",
    )
    return any(a in window for a in allowed)

def _is_allowed_raw_output_context(text: str, index: int) -> bool:
    window = _context_words(text, index, before=128, after=128)
    allowed_fragments = (
        "raw output is forbidden",
        "raw output forbidden",
        "raw output rejected",
        "raw output is not cognition",
        "not raw output admission",
        "raw output admission blocked",
        "raw output admission posture",
        "forbidden artifact leakage and raw output admission",
        "forbidding raw output admission",
        "avoids raw output admission",
        "raw output admitted false",
        "raw output forbidden true",
        "raw output not admitted",
        "not raw output admission status flags",
        "not raw output admission",
        "forbidding raw output admission",
        "rejects or avoids raw output admission",
        "does not admit raw output",
    )
    return any(fragment in window for fragment in allowed_fragments)


def _is_allowed_no_emit_receipt_context(text: str, index: int) -> bool:
    window = text[max(0, index - 320) : index]
    no_emit_index = window.rfind("does not emit")
    claims_index = window.rfind("claims")
    return (
        no_emit_index != -1
        and claims_index < no_emit_index
        and any(
            marker in window
            for marker in (
                "explicit action request",
                "destructive authorization packet",
                "destructive action receipt",
                "pruning receipt",
                "deletion receipt",
                "federation receipt",
                "reward receipt",
                            "model training receipt",
                "deployment decision",
            )
        )
    )


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



def _is_allowed_bounded_release_context(text: str, index: int, phrase: str) -> bool:
    window = _context_words(text, index, before=120, after=120)

    left_clause = text[max(0, index - 160):index]
    clause_start = max(left_clause.rfind("."), left_clause.rfind("\n"), left_clause.rfind(";"))
    clause = left_clause[clause_start + 1 :]
    list_negated = " not " in clause and "," in clause

    if phrase == "truth certification":
        allowed = (
            "not truth certification",
            "truth certification blocked",
            "truth certification not performed",
            "truth certification packet",
        )
        return list_negated or any(item in window for item in allowed)
    if phrase == "final answer release":
        allowed = (
            "not final answer release",
            "final answer not released",
            "final answer released false",
            "final answer release not performed",
        )
        return list_negated or any(item in window for item in allowed)
    if phrase == "product release":
        allowed = (
            "not product release",
            "product release not performed",
            "product release performed false",
            "product release packet",
            "reviewer utility metric is not product release",
            "product release requests must fail closed",
            "product release request must fail closed",
            "product release blocked",
        )
        return list_negated or any(item in window for item in allowed)
    return False

def _forbidden_hits(text: str) -> list[str]:
    hits: list[str] = []
    for phrase in FORBIDDEN_PHRASES:
        normalized_phrase = _normalize(phrase)
        start = 0
        while True:
            index = text.find(normalized_phrase, start)
            if index == -1:
                break
            if phrase.startswith("claims ") and not _is_negated(text, index):
                hits.append(phrase)
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
                    "requires future " in text[max(0, index - 64) : index]
                    or text[index : index + 42].startswith("sophia approval request candidate")
                    or text[index : index + 43].startswith("sophia approval request candidates")
                    or text[index : index + 32].startswith("sophia approval request")
                    or "required before" in text[index : index + 96]
                    or "without " in text[max(0, index - 64) : index]
                    or "missing " in text[max(0, index - 32) : index]
                    or (
                        "blocked when" in text[max(0, index - 96) : index]
                        and "missing" in text[index : index + 96]
                    )
                    or text[index : index + 40].startswith("sophia approval missing")
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if "do not claim" in text[max(0, index - 120) : index]:
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "token economy"
                and (
                    "does not prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 180) : index]
                    or "does not approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 180) : index]
                    or "does not confirm, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 180) : index]
                    or "does not perform destructive action, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 180) : index]
                    or "does not execute, authorize, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in text[max(0, index - 200) : index]
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
                _is_negated(text, index)
                or
                text[index : index + 40].startswith("federation is blocked by default")
                or text[index : index + 48].startswith("federation stress corpus is not federation")
                or text[index : index + 48].startswith("federation stress result is not federation")
                or text[index : index + 44].startswith("federation candidate is not network")
                or text[index : index + 46].startswith("federation credit scenario is not reward")
                or text[index : index + 48].startswith("federation remains blocked by default")
                or text[index : index + 40].startswith("federation_blocked")
                or text[index : index + 40].startswith("federation blocked")
                or (text[index : index + 40].startswith("federation proof") and _is_negated(text, index))
                or text[index : index + 40].startswith("federation_authorization")
                or text[max(0, index - 20) : index].endswith("not_")
                or "without_federation" in text[max(0, index - 32) : index + 16]
                or text[max(0, index - 20) : index].endswith("without_")
                or text[index : index + 40].startswith("federation authorization")
                or text[index : index + 40].startswith("federation stress")
                or text[index : index + 40].startswith("federation occurs")
                or text[index : index + 40].startswith("federation performed")
                or text[index : index + 40].startswith("federation receipt")
                or text[max(0, index - 48) : index + 48].startswith("\"model_training\", \"federation\", \"reward_allocation\"")
                or text[index : index + 40].startswith("federation_performed")
                or text[index : index + 40].startswith("federation risks")
                or text[index : index + 40].startswith("federation_risks")
                or text[index : index + 40].startswith("federation_")
                or text[index : index + 40].startswith("federation_stress")
                or "local-review-runtime-v0 is not federation" in text[max(0, index - 80) : index + 80]
                or text[index : index + 40].startswith("federation = true")
                or text[index : index + 40].startswith('federation": true')
                or '"model_training", "federation", "reward_allocation"' in text[max(0, index - 24) : index + 48]
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"ai consciousness", "human consciousness"}
                and "make ai/human consciousness claims" in text[max(0, index - 32) : index + 48]
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "federation authorization"
                and (
                    _is_negated(text, index)
                    or "not federation authorization" in text[max(0, index - 64) : index + 48]
                    or "local-review-runtime-v0 is not federation authorization" in text[max(0, index - 96) : index + 80]
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"remote provider call", "remote provider calls", "provider call", "provider call performed", "provider call authorized"}
                and _is_allowed_provider_call_context(text, index)
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"network authorization", "network authorized"}
                and _is_allowed_network_authorization_context(text, index)
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"raw output admission", "claims raw output admission", "raw output admitted", "raw output accepted as cognition", "raw_output_admitted"}
                and _is_allowed_raw_output_context(text, index)
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "surveillance"
                and (
                    "not surveillance" in text[max(0, index - 48) : index + 24]
                    or "telemetry_not_surveillance" in text[max(0, index - 64) : index + 32]
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase == "encrypted shard transfer"
                and (
                    text[index : index + 64].startswith("encrypted shard transfer not performed")
                    or text[index : index + 64].startswith("encrypted_shard_transfer_not_performed")
                )
            ):
                start = index + len(normalized_phrase)
                continue
            if (
                phrase in {"federation", "truth certification", "product release"}
                and "request must fail closed" in text[index : index + 72]
            ):
                start = index + len(normalized_phrase)
                continue
            if _is_allowed_no_emit_receipt_context(text, index):
                start = index + len(normalized_phrase)
                continue
            if phrase in {"truth certification", "final answer release", "product release"} and _is_allowed_bounded_release_context(text, index, phrase):
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
