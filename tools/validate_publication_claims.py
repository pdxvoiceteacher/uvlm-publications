#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PAPER_CONFIGS: dict[str, dict[str, Any]] = {
    "PUB-GOV-ARTIFACT-COG-01": {
        "paper_file": "PUB_GOV_ARTIFACT_COG_01.md",
        "required_files": (
            "PUB_GOV_ARTIFACT_COG_01.md",
            "abstract.md",
            "reproducibility_appendix.md",
            "claim_boundary_table.md",
            "artifact_table.md",
            "reviewer_quickstart.md",
            "status.json",
        ),
        "text_files": (
            "PUB_GOV_ARTIFACT_COG_01.md",
            "abstract.md",
            "reproducibility_appendix.md",
            "claim_boundary_table.md",
            "artifact_table.md",
            "reviewer_quickstart.md",
        ),
        "required_phrases": (
            "not truth certification",
            "not deployment authority",
            "not final answer release",
            "local fixture only",
            "requires external peer review",
            "not ai consciousness",
            "not recursive sonya federation",
            "not retrosynthesis runtime",
            "not omega detection",
            "not live atlas memory writes",
            "not live sophia calls",
            "public-utility-alpha-00",
            "sonya gateway",
            "model braid",
            "not live model execution",
            "not federation",
            "raw-baseline-comparison-00",
            "fixture-only measurement scaffold",
            "not hallucination reduction proof",
            "not model quality benchmark",
            "evidence-review-pack-00",
            "Evidence Review Pack v0.1",
            "first product-facing governed review receipt",
            "Universal Evidence Ingress",
            "UCC Control Profile Selector",
            "AI review that shows its work",
            "not professional advice",
            "not compliance certification",
            "rw-comp-01",
            "first fixture-only raw-vs-governed comparison involving Evidence Review Pack v0.1",
            "review-structure visibility",
            "step toward future hallucination-reduction evidence",
            "not hallucination-reduction proof yet",
            "not model superiority proof",
            "rw-comp-02",
            "deterministic multi-fixture comparison battery",
            "six controlled fixture families",
            "full Evidence Review Pack arms",
            "structural visibility improvement",
            "not model-superiority proof",
            "RETROSYNTHESIS-SANDBOX-CYCLE-01",
            "first bounded candidate-repair cycle",
            "incomplete or contradiction-bearing Evidence Review Pack artifacts",
            "Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption",
            "missing-evidence requests",
            "claim-map revision candidates",
            "uncertainty-restoration candidates",
            "counterevidence-expansion candidates",
            "next-experiment recommendations",
            "not memory write",
            "not Publisher finalization",
            "not Omega detection",
            "not publication claim authorization",
            "not recursive self-improvement",
            "EVIDENCE-REVIEW-PACK-01",
            "second-pass candidate loop",
            "Evidence Review Pack second pass is candidate revision, not accepted evidence",
            "structural visibility delta",
            "not hallucination-reduction proof",
            "claim-map revision candidate",
            "not truth certification",
            "uncertainty/counterevidence revision candidate",
            "not canon",
            "no memory write",
            "no final answer release",
            "no Publisher finalization",
            "no deployment",
            "no Omega detection",
            "no recursive self-improvement claim",
            "rw-comp-03",
            "held-out blinded fixture scaffold",
            "held-out, blinded, pre-registered fixture-scoring scaffold",
            "simulated scores only",
            "not live human study",
            "not human-subject study result",
            "not accepted evidence",
            "Run-RW-COMP03-Acceptance.ps1",
            "accepted_as_heldout_blinded_fixture_scaffold",
            "The brain runs cognition stages; experiments configure those stages.",
            "UNIVERSAL-STAGE-PIPELINE-00",
            "ARTIFACT-CONTRACT-REGISTRY-01",
            "UNIVERSAL-COMPATIBILITY-MATRIX-00",
            "Universal Stage Pipeline defines reusable cognition-stage contracts",
            "Artifact Contract Registry externalizes artifact roles and package/profile contracts into versioned configuration",
            "Universal Compatibility Matrix tests whether the same stage/contracts handle multiple input classes or emit deterministic fail-closed/hash-only receipts",
            "profiles are configuration",
            "artifact contracts are versioned configuration",
            "unsupported inputs fail closed or hash-only",
            "hash-only preservation is not semantic interpretation",
            "Experiments configure stages; they do not define the kernel.",
            "Run-UNIVERSAL-COMPATIBILITY-MATRIX00-Acceptance.ps1",
            "accepted_as_universal_compatibility_scaffold",
            "Adapter capability is not adapter authorization.",
            "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
            "fixture-only versioned adapter-contract scaffold",
            "Adapter contracts declare capabilities, consent profiles, failure policies, telemetry requirements, and provenance-training policies",
            "All adapters remain disabled or blocked",
            "No live adapter execution occurred",
            "No network calls occurred",
            "Raw output is forbidden",
            "Candidate packets are required",
            "Failure receipts are required",
            "provenance-training policy is present",
            "Adapter events may support mechanism-level provenance training only when lineage, consent, and control receipts exist",
            "Adapter events may not train model weights",
            "Run-SONYA-ADAPTER-CONTRACT-REGISTRY01-Acceptance.ps1",
            "accepted_as_adapter_contract_registry_only",
            "SONYA-ADAPTER-SMOKE-00",
            "Sonya Adapter Smoke exercises contracts, not live adapters.",
            "fixture-only adapter-contract smoke test",
            "consumes SONYA-ADAPTER-CONTRACT-REGISTRY-01",
            "adapter selection",
            "consent checks",
            "capability checks",
            "Sonya gateway requirement",
            "raw-output rejection",
            "candidate-packet requirement",
            "failure receipts",
            "telemetry events",
            "provenance events",
            "fixture candidate artifacts only",
            "not adapter execution",
            "not live adapter execution",
            "not network authorization",
            "no remote provider call",
            "not model-weight training",
            "raw_output_rejected_or_absent = true",
            "candidate_packet_emitted_for_fixture_model = true",
            "failure_receipts_visible = true",
            "telemetry_events_visible = true",
            "provenance_events_visible = true",
            "Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1",
            "accepted_as_fixture_adapter_contract_smoke",
            "SONYA-LOCAL-FIXTURE-ADAPTER-01",
            "Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters.",
            "deterministic local-only fixture adapter execution",
            "consumes SONYA-ADAPTER-CONTRACT-REGISTRY-01 and SONYA-ADAPTER-SMOKE-00",
            "fixture_text_model_adapter",
            "fixture_summary_generator_adapter",
            "local_file_transform_adapter",
            "hash_only_evidence_adapter",
            "remote_provider_placeholder_adapter",
            "browser_placeholder_adapter",
            "atlas_memory_placeholder_adapter",
            "sophia_route_placeholder_adapter",
            "candidate packets",
            "failure receipts",
            "telemetry events",
            "provenance events",
            "rejects or avoids raw output admission",
            "candidate packets emitted",
            "failure receipts visible",
            "telemetry events visible",
            "provenance events visible",
            "not live adapter execution",
            "not network authorization",
            "no remote provider call",
            "not live model execution",
            "not model-weight training",
            "accepted_as_local_fixture_adapter_execution",
            "local_fixture_adapter_execution_performed = true",
            "candidate_packet_count = 3",
            "failure_receipt_count = 6",
            "telemetry_event_count = 52",
            "provenance_event_count = 35",
            "Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1",
            "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
            "Local adapter candidates become reviewable only through the Evidence Review Pack path.",
            "Adapter output is not accepted as cognition directly.",
            "Candidate packets require UCC-controlled review.",
            "The claim map is not truth certification.",
            "The candidate is not final answer.",
            "UCC control profile applied",
            "unsupported claims listed",
            "provenance events visible",
            "fixture_summary_generator_adapter candidate output",
            "adapter candidate binding packet",
            "local-adapter claim map",
            "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1",
            "accepted_as_local_adapter_candidate_review",
            "not adapter authorization",
            "SONYA-LOCAL-FIXTURE-ADAPTER-02",
            "Multi-adapter local fixture selection still requires Evidence Review Pack review.",
            "Selection policy is not final answer.",
            "Candidate comparison is not model quality benchmark.",
            "Selection is not adapter authorization.",
            "candidate-fixture-summary",
            "selection_policy_applied = true",
            "selected_candidate_requires_review = true",
            "Run-SONYA-LOCAL-FIXTURE-ADAPTER02-Acceptance.ps1",
            "SONYA-LOCAL-FIXTURE-ADAPTER-03",
            "Nested SONYA-LOCAL-FIXTURE-ADAPTER-01 references are source fixture dependencies, not stale identity leakage.",
            "current route identity is explicit",
            "source fixture identity is explicit",
            "Evidence Review Pack local-adapter route references are explicit",
            "Lineage does not grant authority.",
            "sonya_local_adapter_lineage_packet.json",
            "sonya_local_adapter_lineage_review_packet.json",
            "sonya_local_fixture_adapter_03_acceptance_receipt.json",
            "Run-SONYA-LOCAL-FIXTURE-ADAPTER03-Acceptance.ps1",
            "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02",
            "The revised local adapter candidate remains candidate-only, not accepted evidence.",
            "deltas are structural review descriptors",
            "not hallucination-reduction proof",
            "not model quality benchmark",
            "unsupported_claim_count_delta = -1",
            "uncertainty_missing_count_delta = -1",
            "source_reference_visibility_delta = 1",
            "structural_visibility_improved_candidate = true",
            "evidence_review_local_adapter_revision_packet.json",
            "evidence_review_local_adapter_revision_delta.json",
            "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER02-Acceptance.ps1",
            "RW-COMP-LOCAL-ADAPTER-01",
            "RW-COMP local-adapter comparison is not hallucination reduction proof or a model quality benchmark.",
            "deltas are structural review descriptors only",
            "unsupported_claim_count_delta = -1",
            "uncertainty_missing_count_delta = -1",
            "source_reference_visibility_delta = 1",
            "supported_claim_count_delta = 2",
            "rw_comp_local_adapter_packet.json",
            "rw_comp_local_adapter_delta_packet.json",
            "Run-RW-COMP-LOCAL-ADAPTER01-Acceptance.ps1",
            "PMR-00-PROVENANCE-MEMORY-RESERVOIR",
            "PMR-01-LOCAL-ARTIFACT-INDEX",
            "PMR artifact lifecycle state is not truth status.",
            "memory is governed provenance under resource constraints",
            "hash is not encryption",
            "dependency graph is not canon graph",
            "no pruning occurs in PMR-01",
            "federation is blocked by default",
            "pmr_local_artifact_index.json",
            "pmr_dependency_graph.json",
            "Run-PMR00-Acceptance.ps1",
            "Run-PMR01-Acceptance.ps1",
            "PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY",
            "GPCU is lifecycle/storage utility, not truth score.",
            "GPCU is not reward entitlement.",
            "GPCU is not token economy.",
            "GPCU is not human value score.",
            "Lifecycle recommendation is not pruning.",
            "Reward mechanics are deferred.",
            "Federation remains blocked by default.",
            "pmr_provenance_coherence_utility_packet.json",
            "pmr_artifact_utility_scores.jsonl",
            "pmr_lifecycle_recommendation_packet.json",
            "Run-PMR02-Acceptance.ps1",
            "PMR-03-LIFECYCLE-STATE-MACHINE",
            "Lifecycle state is not truth status.",
            "Recommendation is not transition.",
            "Transition candidate is not action.",
            "Destructive action requires future Sophia lifecycle audit.",
            "Destructive action requires future user confirmation.",
            "No pruning or deletion occurs in PMR-03.",
            "pmr_lifecycle_state_machine_packet.json",
            "pmr_lifecycle_no_action_receipt.json",
            "Run-PMR03-Acceptance.ps1",
            "PMR-04-LIFECYCLE-AUDIT-PREFLIGHT",
            "Preflight is not approval.",
            "Audit candidate is not action.",
            "Sophia lifecycle audit is required before destructive action.",
            "User confirmation is required before destructive local action.",
            "No Sophia approval packet is emitted.",
            "No pruning or deletion occurs in PMR-04.",
            "pmr_lifecycle_audit_preflight_packet.json",
            "pmr_lifecycle_audit_no_action_receipt.json",
            "Run-PMR04-Acceptance.ps1",
            "PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW",
            "Sophia review is not Sophia approval.",
            "Audit recommendation is not action.",
            "No Sophia approval packet is emitted.",
            "Destructive action requires future Sophia approval.",
            "Destructive action requires future user confirmation.",
            "No pruning or deletion occurs in PMR-05.",
            "pmr_sophia_lifecycle_audit_packet.json",
            "pmr_sophia_lifecycle_no_approval_receipt.json",
            "Run-PMR05-Acceptance.ps1",
            "PMR-06-USER-CONFIRMATION-PREFLIGHT",
            "User confirmation request is not user confirmation.",
            "User confirmation is not action.",
            "No user confirmation receipt is emitted.",
            "No pruning or deletion occurs in PMR-06.",
            "pmr_user_confirmation_preflight_packet.json",
            "pmr_user_confirmation_no_action_receipt.json",
            "Run-PMR06-Acceptance.ps1",
            "PMR-07-USER-CONFIRMATION-NEGATIVE-CONTROL",
            "Invalid confirmation is not confirmation.",
            "Scope-mismatched confirmation is not confirmation.",
            "Confirmation without Sophia approval is insufficient.",
            "Confirmation cannot override retain-lock, quarantine, revocation, or dependency blocks.",
            "No user confirmation receipt is emitted.",
            "pmr_user_confirmation_negative_control_packet.json",
            "pmr_invalid_user_confirmation_attempts.jsonl",
            "pmr_user_confirmation_negative_control_no_action_receipt.json",
            "Run-PMR07-Acceptance.ps1",
        ),
        "forbidden_overclaims": (
            "proves universal intelligence",
            "certifies truth",
            "deployment ready",
            "deployment readiness",
            "production readiness",
            "ai consciousness proven",
            "final answer authority",
            "final answer selection",
            "final answer release",
            "live model execution",
            "live model evaluation",
            "remote provider evaluation",
            "federation",
            "retrosynthesis runtime",
            "consensus proof",
            "answer selection",
            "hallucination reduction proven",
            "model superiority proven",
            "model superiority proof",
            "hallucination reduction proof",
            "model quality benchmark",
            "production evaluation",
            "live human study",
            "human-subject study result",
            "accepted evidence",
            "professional advice",
            "legal advice",
            "medical advice",
            "tax advice",
            "compliance certification",
            "remote provider call",
            "remote provider calls",
            "universal wisdom machine",
            "recursive sonya federation demonstrated",
            "retrosynthesis runtime demonstrated",
            "omega detection demonstrated",
            "claims accepted evidence",
            "claims canon adoption",
            "claims memory write",
            "claims Publisher finalization",
            "claims Omega detection",
            "claims deployment authority",
            "claims publication claim authorization",
            "claims recursive self-improvement",
            "canon adopted",
            "memory written",
            "publisher finalized",
            "omega detected",
            "publication claim authorized",
            "recursive self-improvement achieved",
            "product release",
            "benchmark result",
            "experiment result",
            "performance proof",
            "ai consciousness demonstrated",
            "claims adapter execution",
            "claims adapter authorization",
            "adapter authorization",
            "adapter authorized",
            "claims network authorization",
            "claims model-weight training",
            "network authorization",
            "model-weight training",
            "model weight training",
            "claims live adapter execution",
            "live adapter execution",
            "adapter executed",
            "live adapter execution occurred",
            "live adapter executed",
            "network authorized",
            "model weights trained",
            "claims lineage authority",
            "lineage authority",
            "lineage grants authority",
            "claims stale identity proof of execution",
            "stale identity proof of execution",
            "claims hallucination reduction proof",
            "claims model quality benchmark",
            "claims final answer selection",
            "claims accepted evidence",
            "claims Atlas canon",
            "memory write authorization",
            "claims memory write authorization",
            "claims pruning execution",
            "pruning execution",
            "claims resource economy",
            "claims federation authorization",
            "truth score",
            "claims truth score",
            "reward entitlement",
            "claims reward entitlement",
            "token economy",
            "claims token economy",
            "human value score",
            "deletion execution",
            "claims deletion execution",
            "encrypted shard transfer",
            "valid user confirmation",
            "user confirmation execution",
            "user confirmation receipt",
            "claims user confirmation",
            "Sophia approval",
            "claims Sophia approval",
            "audit action",
        ),
        "status_required": {
            "paper_id": "PUB-GOV-ARTIFACT-COG-01",
            "repo": "pdxvoiceteacher/uvlm-publications",
            "status": "drafted",
            "claim_level": "internal_preprint_draft",
            "requires_external_peer_review": True,
            "not_truth_certification": True,
            "not_deployment_authority": True,
            "not_final_answer_release": True,
            "not_live_model_execution": True,
            "not_federation": True,
            "raw_baseline_comparison_indexed": True,
            "not_hallucination_reduction_proof": True,
            "not_model_quality_benchmark": True,
            "not_remote_provider_call": True,
            "evidence_review_pack_indexed": True,
            "not_professional_advice": True,
            "not_compliance_certification": True,
            "rw_comp_01_indexed": True,
            "not_model_superiority_proof": True,
            "rw_comp_02_indexed": True,
            "rw_comp_03_indexed": True,
            "not_live_human_study": True,
            "not_human_subject_study_result": True,
            "not_live_model_evaluation": True,
            "not_production_evaluation": True,
            "not_ai_consciousness_claim": True,
            "retrosynthesis_sandbox_cycle_indexed": True,
            "evidence_review_pack_01_indexed": True,
            "not_accepted_evidence": True,
            "not_canon_adoption": True,
            "not_memory_write": True,
            "not_publisher_finalization": True,
            "not_omega_detection": True,
            "not_publication_claim": True,
            "not_recursive_self_improvement": True,
            "universal_stage_pipeline_indexed": True,
            "artifact_contract_registry_indexed": True,
            "universal_compatibility_matrix_indexed": True,
            "not_product_release": True,
            "not_experiment_result": True,
            "not_benchmark_result": True,
            "sonya_adapter_contract_registry_indexed": True,
            "not_adapter_execution": True,
            "not_network_authorization": True,
            "not_model_weight_training": True,
            "sonya_adapter_smoke_indexed": True,
            "sonya_local_fixture_adapter_indexed": True,
            "evidence_review_pack_local_adapter_indexed": True,
            "not_adapter_authorization": True,
            "sonya_local_fixture_adapter_02_indexed": True,
            "not_final_answer_selection": True,
            "not_live_adapter_execution": True,
            "sonya_local_fixture_adapter_03_indexed": True,
            "not_stale_identity_leakage": True,
            "not_lineage_authority": True,
            "evidence_review_pack_local_adapter_02_indexed": True,
            "not_structural_delta_proof": True,
            "rw_comp_local_adapter_indexed": True,
            "pmr_00_indexed": True,
            "pmr_01_indexed": True,
            "pmr_02_indexed": True,
            "pmr_03_indexed": True,
            "pmr_04_indexed": True,
            "pmr_05_indexed": True,
            "not_sophia_review_approval": True,
            "not_audit_recommendation_action": True,
            "pmr_06_indexed": True,
            "not_user_confirmation": True,
            "not_user_confirmation_receipt": True,
            "pmr_07_indexed": True,
            "not_valid_user_confirmation": True,
            "not_confirmation_authority": True,
            "not_sophia_approval": True,
            "not_audit_action": True,
            "not_lifecycle_action": True,
            "not_deletion_execution": True,
            "not_truth_score": True,
            "not_reward_entitlement": True,
            "not_human_value_score": True,
            "not_atlas_canon": True,
            "not_memory_write_authorization": True,
            "not_federation_authorization": True,
            "not_pruning_execution": True,
            "not_resource_economy": True,
            "not_token_economy": True,
        },
    },
    "PUB-WAVE-ROSETTA-01": {
        "paper_file": "PUB_WAVE_ROSETTA_01.md",
        "required_files": (
            "PUB_WAVE_ROSETTA_01.md",
            "abstract.md",
            "methods_appendix.md",
            "theorem_table.md",
            "claim_boundary_table.md",
            "artifact_table.md",
            "reviewer_quickstart.md",
            "status.json",
            "figures/README.md",
        ),
        "text_files": (
            "PUB_WAVE_ROSETTA_01.md",
            "abstract.md",
            "methods_appendix.md",
            "theorem_table.md",
            "claim_boundary_table.md",
            "artifact_table.md",
            "reviewer_quickstart.md",
            "figures/README.md",
        ),
        "required_phrases": (
            "closed form waveform metric calibration",
            "not universal ontology",
            "not psychoacoustic effect",
            "not ai consciousness",
            "not deployment authority",
            "not truth certification",
            "requires external peer review",
        ),
        "forbidden_overclaims": (
            "proves universal ontology",
            "proves psychoacoustic entrainment",
            "proves ai consciousness",
            "proves guft as final physics",
            "deployment ready",
            "truth certified",
            "cognition is literally sine waves",
        ),
        "status_required": {
            "paper_id": "PUB-WAVE-ROSETTA-01",
            "repo": "pdxvoiceteacher/uvlm-publications",
            "status": "drafted",
            "claim_level": "internal_preprint_draft",
            "requires_external_peer_review": True,
            "not_truth_certification": True,
            "not_deployment_authority": True,
            "not_final_answer_release": True,
            "not_universal_ontology_claim": True,
            "not_psychoacoustic_effect_claim": True,
            "not_ai_consciousness_claim": True,
            "not_retrosynthesis_authorization": True,
        },
    },
}
NEGATION_MARKERS = (
    "not ",
    "no ",
    "does not ",
    "do not ",
    "without ",
    "never ",
    "neither ",
    "nor ",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    normalized = text.lower().replace("‑", "-").replace("–", "-")
    return " ".join(normalized.replace("-", " ").split())


def _is_negated(normalized_text: str, start: int) -> bool:
    window = normalized_text[max(0, start - 32) : start]
    after = normalized_text[start : start + 80]
    return (
        any(marker in window for marker in NEGATION_MARKERS)
        or "performed = false" in after
        or "blocked" in after[:48]
    )


def _forbidden_hits(normalized_text: str, forbidden: tuple[str, ...]) -> list[str]:
    hits: list[str] = []
    for phrase in forbidden:
        normalized_phrase = _normalize(phrase)
        search_from = 0
        while True:
            index = normalized_text.find(normalized_phrase, search_from)
            if index == -1:
                break
            if (
                phrase == "valid user confirmation"
                and "invalid " in normalized_text[max(0, index - 24) : index] or normalized_text[max(0, index - 2) : index].endswith("in")
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase == "Sophia approval"
                and (
                    "requires future " in normalized_text[max(0, index - 32) : index]
                    or "without " in normalized_text[max(0, index - 32) : index]
                    or "missing " in normalized_text[max(0, index - 16) : index]
                    or normalized_text[index : index + 40].startswith("sophia approval missing")
                )
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase == "token economy"
                and (
                    "does not prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in normalized_text[max(0, index - 104) : index]
                    or "does not approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in normalized_text[max(0, index - 112) : index]
                    or "does not confirm, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in normalized_text[max(0, index - 122) : index]
                )
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase in {"model quality benchmark", "model quality benchmark"}
                and "not hallucination reduction proof or a" in normalized_text[max(0, index - 56) : index]
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "federation" and (
                normalized_text[index : index + 40].startswith("federation is blocked by default")
                or normalized_text[index : index + 48].startswith("federation remains blocked by default")
                or normalized_text[index : index + 40].startswith("federation_authorization")
            ):
                search_from = index + len(normalized_phrase)
                continue
            if not _is_negated(normalized_text, index):
                hits.append(phrase)
                break
            search_from = index + len(normalized_phrase)
    return hits


def _load_status_id(status: Path) -> str | None:
    try:
        payload = json.loads(status.read_text(encoding="utf-8"))
    except Exception:
        return None
    paper_id = payload.get("paper_id")
    return paper_id if isinstance(paper_id, str) else None


def _infer_config_id(paper: Path, status: Path) -> str:
    status_id = _load_status_id(status)
    if status_id in PAPER_CONFIGS:
        return status_id
    for paper_id, config in PAPER_CONFIGS.items():
        if paper.name == config["paper_file"]:
            return paper_id
    raise ValueError(f"Unsupported publication paper/status combination: {paper}")


def _resolve_paths(args: argparse.Namespace) -> dict[str, Path]:
    paper = args.paper.resolve()
    root = paper.parent
    return {
        "paper": paper,
        "appendix": (args.appendix or root / "reproducibility_appendix.md").resolve(),
        "quickstart": (args.quickstart or root / "reviewer_quickstart.md").resolve(),
        "status": (args.status or root / "status.json").resolve(),
    }


def validate_publication_claims(
    paper: Path,
    appendix: Path | None = None,
    quickstart: Path | None = None,
    status: Path | None = None,
) -> dict[str, Any]:
    root = paper.parent
    status_path = status or root / "status.json"
    paper_id = _infer_config_id(paper, status_path)
    config = PAPER_CONFIGS[paper_id]

    overrides = {
        paper.name: paper,
        "reviewer_quickstart.md": quickstart or root / "reviewer_quickstart.md",
    }
    if appendix is not None:
        overrides[appendix.name] = appendix

    required_file_paths = [
        overrides.get(name, root / name) for name in config["required_files"]
    ]
    missing_files = [str(path) for path in required_file_paths if not path.exists()]
    required_files_present = not missing_files

    text_paths = [overrides.get(name, root / name) for name in config["text_files"]]
    combined_text = "\n".join(_read_text(path) for path in text_paths if path.exists())
    normalized_text = _normalize(combined_text)

    required_phrases_present = [
        phrase
        for phrase in config["required_phrases"]
        if _normalize(phrase) in normalized_text
    ]
    missing_required_phrases = [
        phrase
        for phrase in config["required_phrases"]
        if _normalize(phrase) not in normalized_text
    ]
    forbidden_overclaims_found = _forbidden_hits(
        normalized_text, config["forbidden_overclaims"]
    )

    status_json_valid = False
    status_errors: list[str] = []
    try:
        status_payload = json.loads(status_path.read_text(encoding="utf-8"))
        status_json_valid = all(
            status_payload.get(key) == expected
            for key, expected in config["status_required"].items()
        )
        if not status_json_valid:
            status_errors = [
                key
                for key, expected in config["status_required"].items()
                if status_payload.get(key) != expected
            ]
    except Exception as exc:  # noqa: BLE001 - validator reports bounded JSON errors.
        status_errors = [str(exc)]

    passed = (
        required_files_present
        and not missing_required_phrases
        and not forbidden_overclaims_found
        and status_json_valid
    )

    return {
        "paper_id": paper_id,
        "passed": passed,
        "required_files_present": required_files_present,
        "missing_required_files": missing_files,
        "required_phrases_present": required_phrases_present,
        "missing_required_phrases": missing_required_phrases,
        "forbidden_overclaims_found": forbidden_overclaims_found,
        "status_json_valid": status_json_valid,
        "status_errors": status_errors,
        "not_truth_certification": status_json_valid,
        "not_deployment_authority": status_json_valid,
        "not_final_answer_release": status_json_valid,
    }


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate publication claim boundaries for supported papers."
    )
    parser.add_argument("--paper", required=True, type=Path)
    parser.add_argument("--appendix", type=Path)
    parser.add_argument("--quickstart", type=Path)
    parser.add_argument("--status", type=Path)
    parser.add_argument("--out", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    paths = _resolve_paths(args)
    result = validate_publication_claims(
        paths["paper"],
        appendix=paths["appendix"] if args.appendix else None,
        quickstart=paths["quickstart"],
        status=paths["status"],
    )
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
