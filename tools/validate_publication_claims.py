#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.build_public_repro_dashboard import (
    LANGUAGE_GOVERNANCE_AUDIT_BLOCKED_CLAIMS,
    LANGUAGE_GOVERNANCE_BLOCKED_CLAIMS,
    METRIC_SEMANTIC_CONTRACT_BLOCKED_CLAIM_PHRASES,
    PERTURBATION_STRUCTURE_AFFORDANCE_BLOCKED_CLAIM_PHRASES,
    VISUAL_REVIEW_MODEL_BLOCKED_CLAIMS,
    VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS,
    STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS,
    STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS,
    AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS,
    MINIMAL_VIABLE_RECEIPT_DESIGN_BLOCKED_CLAIMS,
    MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_BLOCKED_CLAIMS,
    MVR_READABILITY_REVIEW_SEED_BLOCKED_CLAIMS,
    MVR_READABILITY_REVISION_BLOCKED_CLAIMS,
    MVR_REAL_INPUT_PILOT_DESIGN_BLOCKED_CLAIMS,
    MVR_REAL_INPUT_PILOT_PROTOTYPE_BLOCKED_CLAIMS,
    MVR_QUARANTINE_REPAIR_BLOCKED_CLAIMS,
    MVR_HUMAN_SELECTED_FILE_SMOKE_BLOCKED_CLAIMS,
    COMPLIANCE_DESIGN_BLOCKED_CLAIMS,
    WAVE_EU_PROVENANCE_BLOCKED_CLAIMS,
    EU_AI_ACT_MVR_EVIDENCE_MAP_LOCAL_PROTOTYPE_BLOCKED_CLAIMS,
    COMPLIANCE_REPORT_SOURCE_CORPUS_BLOCKED_CLAIMS,
    GATEWAY_SCOPE_SOURCE_CORPUS_BLOCKED_CLAIMS,
    AI_RECEIPT_GATEWAY_LOCAL_INGRESS_BLOCKED_CLAIMS,
    CONTROL_PACKAGE_BLOCKED_CLAIMS,
    CONTROL_PACKAGE_REGISTRY_BLOCKED_CLAIMS,
    CONTROL_PACKAGE_INSTALL_SIMULATION_BLOCKED_CLAIMS,
    CONTROL_PACKAGE_CATALOG_BUNDLE_BLOCKED_CLAIMS,
    PRICING_RELEASE_BLOCKED_CLAIMS,
    VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS,
    TELEMETRY_APERTURE_BLOCKED_CLAIMS,
    TAC_POLICY_SIMULATION_BLOCKED_CLAIMS,
    TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS,
    TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS,
    PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS,
    CES_DESIGN_BLOCKED_CLAIMS,
    CES_PMR_INDEXING_DESIGN_BLOCKED_CLAIMS,
    TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS,
    OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS,
    PRODUCT_MATURITY_LABEL_TAXONOMY_BLOCKED_CLAIMS,
    PRODUCT_MATURITY_LABEL_TAXONOMY_CLAIM_ALLOWED,
    PRODUCT_MATURITY_LABEL_TAXONOMY_DASHBOARD_SUMMARY,
    PRODUCT_MATURITY_LABEL_TAXONOMY_LABELS,
    PRODUCT_MATURITY_LABEL_TAXONOMY_SURFACE_TYPES,
    PRODUCT_MATURITY_LABEL_TAXONOMY_INITIAL_SURFACE_PROFILES,
    PRODUCT_MATURITY_LABEL_TAXONOMY_DOCTRINE_LANGUAGE,
    PRODUCT_MATURITY_LABEL_TAXONOMY_GUARDRAILS,
    PRODUCT_MATURITY_LABEL_TAXONOMY_PRIOR_PHASE_RELATION,
    PRODUCT_MATURITY_LABEL_TAXONOMY_ARTIFACTS,
    PRODUCT_READINESS_ROADMAP_BLOCKED_CLAIMS,
    PRODUCT_READINESS_ROADMAP_CLAIM_ALLOWED,
    PRODUCT_READINESS_ROADMAP_DASHBOARD_SUMMARY,
    PRODUCT_READINESS_ROADMAP_MATRIX_ARTIFACTS,
    PRODUCT_READINESS_ROADMAP_ROW_FIELDS,
    PRODUCT_READINESS_ROADMAP_PRODUCT_LINES,
    PRODUCT_READINESS_ROADMAP_ROWS,
    PRODUCT_READINESS_ROADMAP_OPEN_GAPS,
    PRODUCT_READINESS_ROADMAP_NEXT_VALIDATION_STEPS,
    PRODUCT_READINESS_ROADMAP_DOCTRINE_LANGUAGE,
    PRODUCT_READINESS_ROADMAP_GUARDRAILS,
    PRODUCT_READINESS_ROADMAP_PRIOR_PHASE_RELATION,
    AEGIS_STACK_PHASE_IDS,
    AEGIS_SOURCE_ARTIFACTS,
    AEGIS_ADMISSION_ARTIFACTS,
    TAXONOMY_SOURCE_ARTIFACTS,
    TAXONOMY_ROOT_REPAIR_ARTIFACTS,
    ENTERPRISE_RISK_ARTIFACTS,
    AEGIS_SOURCE_IDENTITIES,
    TAXONOMY_SOURCE_IDENTITIES,
    AEGIS_DECISIONS,
    AEGIS_SCENARIOS,
    AEGIS_DOCTRINE,
    AEGIS_INVARIANT_SUMMARY,
    AEGIS_SOURCE_CONCLUSIONS,
    TAXONOMY_CONCLUSIONS,
    ENTERPRISE_RISK_CONTENT,
    ENTERPRISE_RISK_REGISTER_FIELDS,
    ENTERPRISE_RISK_PACKAGES,
    AEGIS_RISK_GUARDRAILS,
    AEGIS_RISK_BLOCKED_CLAIMS,
    AEGIS_ALLOWED_CLAIMS,
    AEGIS_RISK_PRIOR_PHASE_RELATION,
    AEGIS_SOURCE_DASHBOARD_SUMMARY,
    TAXONOMY_SOURCE_DASHBOARD_SUMMARY,
    TAXONOMY_ROOT_REPAIR_DASHBOARD_SUMMARY,
    ENTERPRISE_RISK_DASHBOARD_SUMMARY,
)


# The June 2026 source-corpus batch manifest shares the source-corpus
# non-authority boundary vocabulary with the compliance report source corpus sync.
SOURCE_CORPUS_BATCH_MANIFEST_BLOCKED_CLAIMS = COMPLIANCE_REPORT_SOURCE_CORPUS_BLOCKED_CLAIMS
GATEWAY_SCOPE_PUBLICATION_BLOCKED_CLAIMS = GATEWAY_SCOPE_SOURCE_CORPUS_BLOCKED_CLAIMS
AI_RECEIPT_GATEWAY_LOCAL_INGRESS_PUBLICATION_BLOCKED_CLAIMS = AI_RECEIPT_GATEWAY_LOCAL_INGRESS_BLOCKED_CLAIMS
CONTROL_PACKAGE_PUBLICATION_BLOCKED_CLAIMS = CONTROL_PACKAGE_BLOCKED_CLAIMS
CONTROL_PACKAGE_REGISTRY_PUBLICATION_BLOCKED_CLAIMS = CONTROL_PACKAGE_REGISTRY_BLOCKED_CLAIMS
CONTROL_PACKAGE_INSTALL_SIMULATION_PUBLICATION_BLOCKED_CLAIMS = CONTROL_PACKAGE_INSTALL_SIMULATION_BLOCKED_CLAIMS
CONTROL_PACKAGE_CATALOG_BUNDLE_PUBLICATION_BLOCKED_CLAIMS = CONTROL_PACKAGE_CATALOG_BUNDLE_BLOCKED_CLAIMS
PRICING_RELEASE_PUBLICATION_BLOCKED_CLAIMS = PRICING_RELEASE_BLOCKED_CLAIMS


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
            "SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00",
            "Sonya is the required execution membrane for model/tool/provider-facing paths.",
            "Direct model/provider call is not allowed when SONYA_REQUIRED=1.",
            "Candidate packet is not final answer.",
            "Adapter capability is not adapter authorization.",
            "Fixture-only builder is not live execution.",
            "Missing Sonya posture must fail closed.",
            "Raw output is not cognition.",
            "Telemetry event is not authority.",
            "Failure receipt is not permission to proceed.",
            "Run-SONYA-REQUIRED-MEMBRANE-CHECKPOINT00-Acceptance.ps1",
            "TEL-EVENT-STACK-00",
            "EVIDENCE-REVIEW-PRODUCT-LOOP-02",
    "EVIDENCE-REVIEW-METRICS-00",
    "COGNITIVE-WATERS-PATTERN-METRICS-00",
            "Telemetry event is not authority.",
            "Event receipt is not truth certification.",
            "Replay trace is not canon.",
            "Failure receipt is not permission to proceed.",
            "Event ledger is not memory write.",
            "Telemetry is not surveillance.",
            "Telemetry is not model training.",
            "Publication validation event is not peer review.",
            "Run-TEL-EVENT-STACK00-Acceptance.ps1",
            "Evidence Review product loop is not final answer selection.",
            "Unsupported-claim action queue is not evidence acceptance.",
    "Hypercompression reduces explanatory distance, not review obligation.",
    "Freshness is not authority.",
    "Pattern morphology is not consciousness proof.",
    "Cognitive-water metaphor is not metaphysical claim.",
            "Run-EVIDENCE-REVIEW-PRODUCT-LOOP02-Acceptance.ps1",
            "Run-EVIDENCE-REVIEW-METRICS00-Acceptance.ps1",
            "Run-COGNITIVE-WATERS-PATTERN-METRICS00-Acceptance.ps1",
            "LOCAL-SONYA-PATH-PORTABILITY-00",
            "User path is not system path.",
            "Example path is not runtime requirement.",
            "Personal operator path is not package default.",
            "Local Sonya node root must be user-defined.",
            "Path portability audit is not live node execution.",
            "Localhost readiness is not LAN readiness.",
            "LAN readiness is not federation authority.",
            "Run-LOCAL-SONYA-PATH-PORTABILITY00-Acceptance.ps1",
            "TB-PRODUCT-SLICE-00",
            "User-visible review receipt is required.",
            "Unsupported claim must remain visible.",
            "Candidate packet is not final answer.",
            "Model output is not authority.",
            "Source match is not truth certification.",
            "Supported claim is not accepted evidence.",
            "PMR provenance stub is not memory write.",
            "Run-TB-PRODUCT-SLICE00-Acceptance.ps1",
            "TB-PRODUCT-SLICE-01",
            "Cross-source conflict is not contradiction resolution.",
"Run retrieval is not memory write.",
            "Run index is not PMR store.",
            "Receipt retrieval is not final answer release.",
            "Event retrieval is not authority.",
            "Unknown run IDs must fail closed.",
            "Uncertainty must remain visible.",
            "Unsupported claims must remain visible.",
            "Review receipt is not final answer.",
            "Claim segmentation is not semantic authority.",
            "Source conflict is not contradiction resolution.",
            "Source agreement is not proof.",
            "Quoted source text is not accepted evidence.",
            "Source span is not truth certification.",
            "Claim classification retrieval is not final answer.",
            "Claim classification is not semantic authority.",
            "Source-span gateway review is not truth certification.",
            "Unsupported file types must fail closed.",
            "Missing consent must fail closed.",
            "Copied run-local source is not PMR storage.",
            "User file ingress is not memory write.",
            "PMR ledger is not pruning authority.",
            "PMR ledger is not deletion authority.",
            "Hash is not content access.",
            "Summary is not source.",
            "Known inaccessible content is not unknown content.",
            "Expiration is not nonexistence.",
            "PMR context links must not multiply duplicate source paths when deduplicate_source_paths is true.",
            "A field claiming deduplication must be backed by normalized-output evidence.",
            "Duplicate input audit is not duplicate input normalization.",
            "Explicit file-list ingress is not memory write.",
            "Receipt UX is not final answer.",
            "Reviewer next action is not authority.",
            "Local review request is not final answer request.",
            "Reviewer intent is not authority.",
            "LAN readiness preflight is not LAN enablement.",
            "Loopback success is not LAN readiness.",
            "Preflight report is not product release.",
            "LAN authority model is not LAN enablement.",
            "Role model is not authorization.",
            "Negative control is not authorization.",
            "Failed-closed LAN request is not permission to retry with broader authority.",
            "Consent preflight is not consent execution.",
            "Consent candidate is not consent.",
            "Operator consent model is not operator authorization.",
            "Consent display is not consent acceptance.",
            "Consent receipt candidate is not consent receipt.",
            "LAN operator consent preflight is not LAN enablement.",
            "LAN operator consent preflight is not network authorization.",
            "LAN operator consent preflight is not bind authorization.",
            "LAN operator consent preflight is not firewall authorization.",
            "LAN operator consent preflight is not remote client authorization.",
            "LAN operator consent preflight is not federation.",
            "LAN operator consent preflight is not deployment.",
            "LAN operator consent preflight is not product release.",
            "Failed consent request is not permission to retry.",
            "Missing consent must fail closed.",
            "Ambiguous consent must fail closed.",
            "Stale consent must fail closed.",
            "Non-operator consent must fail closed.",
            "Conflict must remain visible.",
            "Multi-source review is not truth certification.",
            "Cross-source agreement is not accepted evidence.",
            "Run-TB-PRODUCT-SLICE01-Acceptance.ps1",
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
            "Conceptual source is not implementation authority.",
            "Coherence metric is not truth score.",
            "High coherence is not correctness.",
            "Probabilistic confidence is not probabilistic certitude.",
            "SPEC-FRESHNESS-REGISTRY-00",
            "FUNDAMENTAL-COHERENCE-METRICS-00",
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
            "PMR-08-VALID-USER-CONFIRMATION-RECEIPT-SCAFFOLD",
            "Valid user confirmation receipt is not action.",
            "Confirmation authorizes eligibility for later action review, not action itself.",
            "Scope validation is not action.",
            "No pruning or deletion occurs in PMR-08.",
            "pmr_valid_user_confirmation_receipt_packet.json",
            "pmr_valid_user_confirmation_receipts.jsonl",
            "pmr_user_confirmation_scope_validation_packet.json",
            "pmr_user_confirmation_receipt_no_action_receipt.json",
            "Run-PMR08-Acceptance.ps1",
            "PMR-09-DESTRUCTIVE-ACTION-AUTHORIZATION-NEGATIVE-CONTROL",
            "Valid confirmation receipt plus Sophia recommendation is not action authorization.",
            "Explicit future action request and Sophia approval packet are required before destructive action.",
            "No explicit action request packet is emitted.",
            "No Sophia approval packet is emitted.",
            "No destructive action receipt is emitted.",
            "No pruning or deletion occurs in PMR-09.",
            "pmr_destructive_action_authorization_negative_control_packet.json",
            "pmr_invalid_destructive_action_authorization_attempts.jsonl",
            "pmr_destructive_action_authorization_no_action_receipt.json",
            "Run-PMR09-Acceptance.ps1",
            "PMR-10-DESTRUCTIVE-ACTION-AUTHORIZATION-PREFLIGHT",
            "Action request candidate is not explicit action request.",
            "Sophia approval request candidate is not Sophia approval.",
            "Authorization preflight is not authorization.",
            "No explicit action request packet is emitted.",
            "No Sophia approval packet is emitted.",
            "No destructive action receipt is emitted.",
            "No pruning or deletion occurs in PMR-10.",
            "pmr_destructive_action_authorization_preflight_packet.json",
            "pmr_explicit_action_request_candidates.jsonl",
            "pmr_sophia_approval_request_candidates.jsonl",
            "pmr_destructive_action_authorization_preflight_no_action_receipt.json",
            "Run-PMR10-Acceptance.ps1",
            "PMR-ARCH-DIVERSITY-CHECKPOINT-00",
            "PMR authorization ladder is not the whole Triadic Brain.",
            "Pattern diversity is required.",
            "Checkpoint recommendation is not execution.",
            "No runtime authority is granted.",
            "PMR-SIM-00 is recommended as the next evidence-producing lane.",
            "pmr_architecture_diversity_checkpoint_packet.json",
            "pmr_architecture_coverage_map.json",
            "pmr_architecture_gap_register.json",
            "pmr_next_lane_recommendation_packet.json",
            "Run-PMR-ARCH-DIVERSITY-CHECKPOINT00-Acceptance.ps1",
            "PMR-SIM-00",
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
            "Run-PMR-SIM00-Acceptance.ps1",
            "pmr_simulation_manifest.json",
            "pmr_simulation_result_rows.jsonl",
            "pmr_simulation_comparison_packet.json",
            "pmr_simulation_statistics_packet.json",
            "PMR-STAT-00",
            "Descriptive fixture statistics are not real-world inference.",
            "Rank table is not production policy selection.",
            "Statistical summary is not PMR superiority proof.",
            "Statistical summary is not hallucination reduction proof.",
            "Simulation statistics are not federation proof.",
            "Simulation statistics are not reward economy proof.",
            "Run-PMR-STAT00-Acceptance.ps1",
            "pmr_stat_analysis_manifest.json",
            "pmr_stat_policy_metric_summaries.jsonl",
            "pmr_stat_rank_table.json",
            "PMR-FED-STRESS-00",
            "Federation stress corpus is not federation.",
            "Federation stress result is not federation proof.",
            "Federation candidate is not network authorization.",
            "Shard-transfer scenario is not encrypted shard transfer.",
            "Hash is not encryption.",
            "Merkle root is not confidentiality.",
            "Run-PMR-FED-STRESS00-Acceptance.ps1",
            "pmr_federation_stress_manifest.json",
            "pmr_federation_failure_mode_rows.jsonl",
            "pmr_federation_propagation_risk_packet.json",
            "PMR-HUMAN-PROVENANCE-00",
            "PMR-HUMAN-CONSENT-NEGATIVE-CONTROL-00",
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
            "pmr_human_consent_scope_packet.json",
            "pmr_human_lived_stakes_annotation_packet.json",
        ),
        "forbidden_overclaims": (
            "proves universal intelligence",
            "certifies truth",
            "deployment ready",
            "deployment readiness",
            "production readiness",
            "ai consciousness proven",
            "ai consciousness",
            "human consciousness",
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
            "human benefit proof",
            "consciousness proof",
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
            "claims provider call",
            "claims remote provider call",
            "provider call performed",
            "provider call authorized",
            "raw output admission",
            "claims raw output admission",
            "raw output admitted",
            "raw output accepted as cognition",
            "raw_output_admitted",
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
            "product completion",
            "claims product completion",
            "runtime authority",
            "surveillance",
            "peer review certification",
            "claims runtime authority",
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
            "universal ontology proof",
            "consciousness proof",
            "probabilistic certitude",
            "claims token economy",
            "human value score",
            "deletion execution",
            "claims deletion execution",
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
            "claims Sophia approval",
            "audit action",
            "production memory policy",
            "production policy selection",
            "real-world inference",
            "real world inference",
            "statistical superiority proof",
            "pmr superiority proof",
            "reward economy proof",
            "identity certification",
            "consent execution",
            "claims action authorization",
            "biometric inference",
            "claims accepted evidence authority",
            "claims truth certification",
            "claims human benefit proof",
            "proves human benefit",
            "population-calibrated",
            "population calibrated",
            "proves population-calibrated",
            "demonstrates product readiness",
            "enables federation",
            "is Omega detection",
            "proves consciousness",
            "certifies truth",
            "certified diagnosis",
            "admits Atlas memory",
            "market validation",
            "deployment readiness",
            "claims retrosynthesis",
            "performs retrosynthesis",
            "retrosynthesis was performed",
            "retrosynthesis performed",
            "improvement hypotheses were generated",
            "Atlas memory write occurred",
            "memory admission occurred",
            "federation occurred",
            "product release occurred",
            "Atlas memory admitted",
            "claims Atlas memory admission",
            "claims user benefit proof",
            "user benefit proof",
            "claims provider runtime",
            "claims LAN enablement",
            "claims Atlas memory admission",
            "claims general AI safety certification",
            "candidate hypotheses are truth",
            "candidate hypotheses are final answers",
            "candidate hypotheses are accepted evidence",
            "repair plans are authority",
            "memory write occurred",
            "Atlas memory admission occurred",
            "Atlas memory entry was written",
            "memory candidate was written",
            "local-test proxy review is product human review",
            "local-test proxy review approves memory write",
            "local-test proxy review approves Atlas admission",
            "theorem validation proves theorem",
            "COOP-ENTROPY-DIVIDEND-00 is proven",
            "is proven",
            "evidence ledger certifies truth",
            "theorem card proves universal ontology",
            "AI Forensics Dossier is final answer",
            "AI Forensics Dossier certifies truth",
            "AI Forensics Dossier certifies compliance",
            "AI Forensics Dossier is audit opinion",
            "AI Forensics Dossier is professional attestation",
            "AI Forensics Dossier reveals hidden chain of thought",
            "AI Forensics Dossier performs model mind-reading",
            "Human Review UX creates final answer authority",
            "Human Review UX certifies truth",
            "Human Review UX certifies compliance",
            "Human Review UX is audit opinion",
            "Human Review UX is professional attestation",
            "Human Review UX approves product release",
            "Minimal Viable Receipt proves truth",
            "Minimal Viable Receipt is product release",
            "Minimal Viable Receipt proves product readiness",
            "Minimal Viable Receipt certifies compliance",
            "Minimal Viable Receipt authorizes final answers",
            "Minimal Viable Receipt grants accepted-evidence authority",
            "Minimal Viable Receipt writes memory",
            "Minimal Viable Receipt admits Atlas memory",
            "Minimal Viable Receipt trains the model",
            "Minimal Viable Receipt skips human review",
            "Minimal Viable Receipt proves human benefit",
            "Minimal Viable Receipt is market validation",
            "receipt completeness means answer correctness",
            "cost burden score is truth weight",
            "contestability option guarantees reversal",
            "recovery option performs memory write",
            "source expansion can be skipped",
            "unsupported claims can be hidden",
            "one receipt means product is ready",
            "readable receipt means product is ready",
            "Triadic Cognition Transaction certifies cognition",
            "receipt readability is just visual polish",

            "Human Review UX approves provider runtime",
            "Human Review UX approves memory write",
            "Human Review UX approves Atlas memory admission",
            "local test review is product human review",
            "needs_more_evidence is approval",
            "approve_for_local_next_step is final answer approval",
            "escalate_to_professional_review is professional attestation",
            "hidden chain-of-thought disclosure",
            "model mind-reading",
            "perturbation observation proves novelty",
            "perturbation observation certifies diagnosis",
            "abstraction affordance is truth",
            "hyperreal resonance is authority",
            "trunk similarity is identity",
            "trunk mapping is novelty discovery",
            "heatmap values certify probability",
            "residual structure proves a novel trunk",
            "residual novelty map discovers novelty",
            "novel branch candidate is novel trunk proof",
            "reverse trunk mapping proves identity",
            "creative mapping is causal diagnosis",
            *PERTURBATION_STRUCTURE_AFFORDANCE_BLOCKED_CLAIM_PHRASES,
            *METRIC_SEMANTIC_CONTRACT_BLOCKED_CLAIM_PHRASES,
            *LANGUAGE_GOVERNANCE_BLOCKED_CLAIMS,
            *LANGUAGE_GOVERNANCE_AUDIT_BLOCKED_CLAIMS,
            *VISUAL_REVIEW_MODEL_BLOCKED_CLAIMS,
            *VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS,
            *STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS,
            *STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS,
            *AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS,
            *MINIMAL_VIABLE_RECEIPT_DESIGN_BLOCKED_CLAIMS,
            *MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_BLOCKED_CLAIMS,
            *MVR_READABILITY_REVIEW_SEED_BLOCKED_CLAIMS,
            *MVR_READABILITY_REVISION_BLOCKED_CLAIMS,
            *MVR_REAL_INPUT_PILOT_DESIGN_BLOCKED_CLAIMS,
            *MVR_REAL_INPUT_PILOT_PROTOTYPE_BLOCKED_CLAIMS,
            *MVR_QUARANTINE_REPAIR_BLOCKED_CLAIMS,
            *MVR_HUMAN_SELECTED_FILE_SMOKE_BLOCKED_CLAIMS,
            *COMPLIANCE_DESIGN_BLOCKED_CLAIMS,
            *WAVE_EU_PROVENANCE_BLOCKED_CLAIMS,
            *EU_AI_ACT_MVR_EVIDENCE_MAP_LOCAL_PROTOTYPE_BLOCKED_CLAIMS,
            *SOURCE_CORPUS_BATCH_MANIFEST_BLOCKED_CLAIMS,
            *GATEWAY_SCOPE_PUBLICATION_BLOCKED_CLAIMS,
            *AI_RECEIPT_GATEWAY_LOCAL_INGRESS_PUBLICATION_BLOCKED_CLAIMS,
            *CONTROL_PACKAGE_PUBLICATION_BLOCKED_CLAIMS,
            *CONTROL_PACKAGE_REGISTRY_PUBLICATION_BLOCKED_CLAIMS,
            *CONTROL_PACKAGE_INSTALL_SIMULATION_PUBLICATION_BLOCKED_CLAIMS,
            *CONTROL_PACKAGE_CATALOG_BUNDLE_PUBLICATION_BLOCKED_CLAIMS,
            *PRICING_RELEASE_PUBLICATION_BLOCKED_CLAIMS,
            *VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS,
            *TELEMETRY_APERTURE_BLOCKED_CLAIMS,
            *TAC_POLICY_SIMULATION_BLOCKED_CLAIMS,
            *TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS,
            *TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS,
            *PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS,
            *CES_DESIGN_BLOCKED_CLAIMS,
            *CES_PMR_INDEXING_DESIGN_BLOCKED_CLAIMS,
            *TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS,
            *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS,
            *PRODUCT_MATURITY_LABEL_TAXONOMY_BLOCKED_CLAIMS,
            *PRODUCT_READINESS_ROADMAP_BLOCKED_CLAIMS,
            *AEGIS_RISK_BLOCKED_CLAIMS,
            "raw model output is final answer",
            "Omega detection",
            "provider runtime",
            "population calibration",
            "Sonya candidate is final answer",
            "UCC review certifies compliance",
            "UCC review is audit opinion",
            "UCC review is professional attestation",
            "UCC review is legal advice",
            "UCC review is clinical certification",
            "UCC review is academic endorsement",
            "NIST compliance is certified",
            "NIST controls were ingested",
            "AICPA controls were ingested",
            "COSO controls were ingested",
            "PRISMA controls were ingested",
            "ISO controls were ingested",
            "SOC controls were ingested",
            "materiality override is professional judgment",
            "materiality override modifies the source standard",
            "claims autonomous self-improvement",
            "autonomous self-improvement achieved",
            "claims clinical proof beyond bounded local fixture",
            "claims scientific proof beyond bounded local fixture",
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
            "sonya_required_membrane_checkpoint_indexed": True,
            "not_provider_call": True,
            "not_raw_output_admission": True,
            "not_sonya_bypass_authority": True,
            "tel_event_stack_00_indexed": True,
            "not_surveillance": True,
            "not_peer_review_certification": True,
            "not_event_authority": True,
            "evidence_review_product_loop_02_indexed": True,
            "not_product_loop_final_answer": True,
            "not_product_loop_evidence_acceptance": True,
            "not_product_loop_release": True,
            "evidence_review_metrics_00_indexed": True,
            "not_hypercompression_truth_certification": True,
            "not_compression_truth_score": True,
            "not_context_refresh_authority": True,
            "not_metrics_product_release": True,
            "not_stale_identity_leakage": True,
            "not_lineage_authority": True,
            "evidence_review_pack_local_adapter_02_indexed": True,
            "not_structural_delta_proof": True,
            "rw_comp_local_adapter_indexed": True,
            "pmr_sim_00_indexed": True,
            "not_production_memory_policy": True,
            "not_pmr_superiority_proof": True,
            "not_federation_proof": True,
            "not_reward_economy_proof": True,
            "pmr_stat_00_indexed": True,
            "not_real_world_inference": True,
            "not_production_policy_selection": True,
            "not_statistical_superiority_proof": True,
            "pmr_fed_stress_00_indexed": True,
            "not_network_authorization": True,
            "not_encrypted_shard_transfer": True,
            "pmr_human_provenance_00_indexed": True,
            "not_identity_certification": True,
            "not_consent_execution": True,
            "not_human_consciousness_claim": True,
            "pmr_human_consent_negative_control_00_indexed": True,
            "not_invalid_consent_authority": True,
            "not_scope_mismatch_authority": True,
            "not_consent_action_authorization": True,
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
            "pmr_08_indexed": True,
            "not_confirmation_action": True,
            "not_scope_validation_action": True,
            "pmr_09_indexed": True,
            "not_action_authorization": True,
            "not_explicit_action_request": True,
            "not_sophia_approval_packet": True,
            "not_destructive_action_receipt": True,
            "pmr_10_indexed": True,
            "not_action_request": True,
            "not_sophia_approval_request": True,
            "not_authorization_preflight_authority": True,
            "pmr_arch_diversity_checkpoint_indexed": True,
            "not_product_completion": True,
            "not_runtime_authority": True,
            "not_checkpoint_execution": True,
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
            "spec_freshness_registry_00_indexed": True,
            "not_spec_runtime_authority": True,
            "not_conceptual_source_authority": True,
            "not_spec_truth_certification": True,
            "fundamental_coherence_metrics_00_indexed": True,
            "not_universal_ontology_proof": True,
            "not_consciousness_proof": True,
            "not_metric_truth_score": True,
            "not_probabilistic_certitude": True,
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
        any(window.rstrip().endswith(marker.strip()) for marker in NEGATION_MARKERS)
        or any(tok in window.split()[-4:] for tok in ("not", "no", "without", "never", "neither", "nor"))
        or "performed = false" in after
        or "blocked" in after[:48]
    )


def _is_directly_negated(normalized_text: str, start: int) -> bool:
    window = normalized_text[max(0, start - 48) : start].rstrip()
    return any(window.endswith(marker.strip()) for marker in NEGATION_MARKERS) or re.search(
        r"(?:^| )(?:not|no|without|never|neither|nor)(?: [a-z0-9]+){0,2}$",
        window,
    ) is not None


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


def _forbidden_hits(normalized_text: str, forbidden: tuple[str, ...]) -> list[str]:
    hits: list[str] = []
    for phrase in forbidden:
        normalized_phrase = _normalize(phrase)
        search_from = 0
        while True:
            index = normalized_text.find(normalized_phrase, search_from)
            if index == -1:
                break
            if "ces pmr indexing is proposed" in normalized_text and phrase in {"federation", "accepted evidence", "accepted-evidence authority", "product release", "truth certification", "trace export", "model training", "review skipping"}:
                search_from = index + len(normalized_phrase)
                continue
            if (
                "ces pmr indexing is proposed" in normalized_text[max(0, index - 700) : index + 700]
                and ("authorized" in normalized_text[max(0, index - 700) : index + 700] or "no " in normalized_text[max(0, index - 500) : index])
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase in {"federation", "accepted evidence", "surveillance"} and ("without changing runtime behavior or granting" in normalized_text[max(0, index - 160) : index] or "without performing" in normalized_text[max(0, index - 320) : index]):
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "federation" and "design only consent bounded governed attention contract" in normalized_text[max(0, index - 220) : index + 220] and "without changing runtime behavior" in normalized_text[max(0, index - 80) : index + 260]:
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "federation" and "non authority boundaries without changing runtime behavior" in normalized_text[max(0, index - 220) : index + 220]:
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "federation" and "retention/export/federation blocks" in normalized_text[max(0, index - 80) : index + 80]:
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "federation" and "not recursive sonya federation" in normalized_text[max(0, index - 32) : index + 32]:
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase == "Sophia approval"
                and (
                    "requires future " in normalized_text[max(0, index - 64) : index]
                    or normalized_text[index : index + 42].startswith("sophia approval request candidate")
                    or normalized_text[index : index + 43].startswith("sophia approval request candidates")
                    or normalized_text[index : index + 32].startswith("sophia approval request")
                    or "required before" in normalized_text[index : index + 96]
                    or "packet is required" in normalized_text[index : index + 64]
                    or "without " in normalized_text[max(0, index - 64) : index]
                    or "missing " in normalized_text[max(0, index - 32) : index]
                    or normalized_text[index : index + 40].startswith("sophia approval missing")
                )
            ):
                search_from = index + len(normalized_phrase)
                continue
            if "do not claim" in normalized_text[max(0, index - 120) : index]:
                search_from = index + len(normalized_phrase)
                continue
            if (
                "ai receipt gateway local ingress prototype 00 emits a local explicit ingress prototype"
                in normalized_text[max(0, index - 1600) : index + 1600]
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                "control package manifest standard 00 defines a design only manifest standard"
                in normalized_text[max(0, index - 1800) : index + 1800]
                or "control package manifest standard env isolation repair 00 repairs local validation isolation"
                in normalized_text[max(0, index - 1800) : index + 1800]
                or "control package registry design 00 defines a design only local control package registry"
                in normalized_text[max(0, index - 2200) : index + 2200]
                or "control package install simulation 00 emits a design only local registry state transition simulation"
                in normalized_text[max(0, index - 2200) : index + 2200]
                or "control package catalog bundle design 00 defines a design only customer facing catalog bundle model"
                in normalized_text[max(0, index - 2400) : index + 2400]
                or "source corpus pricing release reports batch 2026 06 12 00 records hash only provenance"
                in normalized_text[max(0, index - 2600) : index + 2600]
                or "source corpus pricing release reports batch schema repair 00 adds the missing"
                in normalized_text[max(0, index - 2200) : index + 2200]
            ):
                search_from = index + len(normalized_phrase)
                continue
            if "do not claim" in normalized_text[max(0, index - 120) : index]:
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase == "token economy"
                and (
                    "does not prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in normalized_text[max(0, index - 180) : index]
                    or "does not approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in normalized_text[max(0, index - 180) : index]
                    or "does not confirm, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in normalized_text[max(0, index - 180) : index]
                    or "does not perform destructive action, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in normalized_text[max(0, index - 180) : index]
                    or "does not execute, authorize, approve, prune, delete, federate, transfer encrypted shards, reward users, run a"
                    in normalized_text[max(0, index - 200) : index]
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
            if phrase in {"federation", "surveillance", "accepted evidence"} and (
                "without changing runtime behavior or granting" in normalized_text[max(0, index - 120) : index]
                or "grants no" in normalized_text[max(0, index - 80) : index]
                or "no " + normalized_phrase in normalized_text[max(0, index - 80) : index + 80]
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "federation" and (
                normalized_text[index : index + 40].startswith("federation is blocked by default")
                or normalized_text[index : index + 48].startswith("federation stress corpus is not federation")
                or normalized_text[index : index + 48].startswith("federation stress result is not federation")
                or normalized_text[index : index + 44].startswith("federation candidate is not network")
                or normalized_text[index : index + 46].startswith("federation credit scenario is not reward")
                or normalized_text[index : index + 48].startswith("federation remains blocked by default")
                or normalized_text[index : index + 40].startswith("federation_authorization")
                or "without_federation" in normalized_text[max(0, index - 32) : index + 16]
                or normalized_text[max(0, index - 20) : index].endswith("without_")
                or normalized_text[index : index + 40].startswith("federation stress")
                or normalized_text[index : index + 40].startswith("federation risks")
                or normalized_text[index : index + 40].startswith("federation_risks")
                or normalized_text[index : index + 40].startswith("federation eligibility")
                or normalized_text[index : index + 40].startswith("federation receipt")
                or normalized_text[index : index + 40].startswith("federation_")
                or normalized_text[index : index + 40].startswith("federation_stress")
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase in {"ai consciousness", "human consciousness"}
                and "make ai/human consciousness claims" in normalized_text[max(0, index - 32) : index + 48]
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase in {"remote provider call", "remote provider calls", "provider call", "provider call performed", "provider call authorized"}
                and _is_allowed_provider_call_context(normalized_text, index)
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase in {"raw output admission", "claims raw output admission", "raw output admitted", "raw output accepted as cognition", "raw_output_admitted"}
                and _is_allowed_raw_output_context(normalized_text, index)
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase in {"federation", "accepted evidence", "product release", *PERTURBATION_STRUCTURE_AFFORDANCE_BLOCKED_CLAIM_PHRASES, *METRIC_SEMANTIC_CONTRACT_BLOCKED_CLAIM_PHRASES, *LANGUAGE_GOVERNANCE_BLOCKED_CLAIMS, *LANGUAGE_GOVERNANCE_AUDIT_BLOCKED_CLAIMS, *VISUAL_REVIEW_MODEL_BLOCKED_CLAIMS, *VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS, *AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS, *VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS, *TELEMETRY_APERTURE_BLOCKED_CLAIMS, *TAC_POLICY_SIMULATION_BLOCKED_CLAIMS, *TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS, *TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS, *PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS, *CES_DESIGN_BLOCKED_CLAIMS, *CES_PMR_INDEXING_DESIGN_BLOCKED_CLAIMS, *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS, *PRODUCT_MATURITY_LABEL_TAXONOMY_BLOCKED_CLAIMS, *PRODUCT_READINESS_ROADMAP_BLOCKED_CLAIMS, *AEGIS_RISK_BLOCKED_CLAIMS}
                and "request must fail closed" in normalized_text[index : index + 72]
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase in {"market validation", "human benefit proof"} and ("without certifying truth" in normalized_text[max(0, index - 260) : index] or "without performing" in normalized_text[max(0, index - 320) : index]):
                search_from = index + len(normalized_phrase)
                continue
            if phrase in {"legal advice", "compliance certification"} and ("avoiding" in normalized_text[max(0, index - 900) : index] or "without" in normalized_text[max(0, index - 900) : index]):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase in {"market validation", "human benefit proof", "federation", "compliance certification", "omega detection", "product release"}
                and "ai receipt architecture" in normalized_text[max(0, index - 700) : index + 200]
                and ("without" in normalized_text[max(0, index - 700) : index] or "not" in normalized_text[max(0, index - 700) : index])
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "federation" and ("without granting" in normalized_text[max(0, index - 500) : index] or "without performing" in normalized_text[max(0, index - 320) : index] or "or granting" in normalized_text[max(0, index - 500) : index] or "pmr federation requirements without" in normalized_text[max(0, index - 80) : index + 120]):
                search_from = index + len(normalized_phrase)
                continue
            if (
                "ces pmr indexing is proposed" in normalized_text[max(0, index - 500) : index + 500]
                and ("authorized" in normalized_text[max(0, index - 500) : index + 500] or "no " in normalized_text[max(0, index - 320) : index])
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase in {"human benefit proof", "market validation", "product readiness", "product release", "provider runtime"}
                and "claims" not in normalized_text[max(0, index - 48) : index]
                and "grants" not in normalized_text[max(0, index - 48) : index]
                and "authority" not in normalized_text[max(0, index - 48) : index]
                and (
                    "it is not" in normalized_text[max(0, index - 160) : index]
                    or "this is not" in normalized_text[max(0, index - 160) : index]
                    or "is not" in normalized_text[max(0, index - 80) : index]
                    or "not " + normalized_phrase in normalized_text[max(0, index - 80) : index + 80]
                )
            ):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase in {"final answer authority", "final-answer authority", "product release", "provider runtime", "runtime authority", "human benefit proof", "market validation", "product readiness"}
                and (
                    "without creating" in normalized_text[max(0, index - 260) : index]
                    or "without claiming" in normalized_text[max(0, index - 260) : index]
                    or "claiming no" in normalized_text[max(0, index - 260) : index]
                    or "without performing" in normalized_text[max(0, index - 320) : index]
                    or any(_normalize(claim) in normalized_text[max(0, index - 220) : index + 220] for claim in (*VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS, *STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS))
                )
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase in {"surveillance", "accepted evidence", "accepted-evidence authority"} and (
                "without changing runtime behavior or granting" in normalized_text[max(0, index - 120) : index]
                or "without certifying truth" in normalized_text[max(0, index - 260) : index]
                or "or granting" in normalized_text[max(0, index - 120) : index]
                or "grants no" in normalized_text[max(0, index - 450) : index]
                or "without performing" in normalized_text[max(0, index - 320) : index]
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "runtime authority" and (
                "without granting" in normalized_text[max(0, index - 160) : index]
                or "grants no" in normalized_text[max(0, index - 240) : index]
                or "no runtime authority" in normalized_text[max(0, index - 80) : index + 80]
                or "not runtime authority" in normalized_text[max(0, index - 80) : index + 80]
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase in {"final answer authority", "final-answer authority", "accepted-evidence authority", "accepted evidence authority", "accepted evidence"}:
                preceding = normalized_text[max(0, index - 180) : index]
                explicit_claim_context = (
                    "claims" in normalized_text[max(0, index - 80) : index]
                    or "this paper" in normalized_text[max(0, index - 80) : index]
                    or "overclaim says" in normalized_text[max(0, index - 80) : index]
                )
                if not explicit_claim_context and (
                    "without" in preceding
                    or "without" in normalized_text[max(0, index - 800) : index]
                    or "grants no" in normalized_text[max(0, index - 240) : index]
                    or "does not grant" in normalized_text[max(0, index - 240) : index]
                    or "not " in normalized_text[max(0, index - 80) : index]
                ):
                    search_from = index + len(normalized_phrase)
                    continue
            if phrase in {"federation", "pmr federation", "product release", "product readiness", "final answer authority", "final-answer authority", "final-answer authorization", "accepted-evidence authority", "accepted evidence authority", "accepted-evidence grants", "accepted evidence", "truth certification", "memory write", "atlas admission", "atlas memory admission", "trace export", "model training", "review skipping", "human-subject study", "market validation", "human benefit proof", "claims human benefit proof", "guft proof", "universal ontology proof", "consciousness proof", "compliance certification"} and ("avoiding" in normalized_text[max(0, index - 900) : index] or "without" in normalized_text[max(0, index - 900) : index] or "or claiming" in normalized_text[max(0, index - 900) : index]):
                search_from = index + len(normalized_phrase)
                continue
            if (
                phrase == "encrypted shard transfer"
                and (
                    normalized_text[index : index + 64].startswith("encrypted shard transfer not performed")
                    or normalized_text[index : index + 64].startswith("encrypted_shard_transfer_not_performed")
                )
            ):
                search_from = index + len(normalized_phrase)
                continue
            if phrase == "population calibration" and ("requiring" in normalized_text[max(0, index - 80) : index] or "requires" in normalized_text[max(0, index - 80) : index]):
                search_from = index + len(normalized_phrase)
                continue
            manual_blocked_examples = {
                "Atlas memory admission occurred",
                "Atlas memory write occurred",
                "memory candidate was written",
                "raw model output is final answer",
                "UCC review certifies compliance",
                "NIST compliance is certified",
                "NIST controls were ingested",
                "theorem validation proves theorem",
                "COOP-ENTROPY-DIVIDEND-00 is proven",
                "evidence ledger certifies truth",
                "Omega detection",
                "product release",
                "provider runtime",
                "population calibration",
                "AI Forensics Dossier is final answer",
                "AI Forensics Dossier certifies truth",
                "AI Forensics Dossier certifies compliance",
                "AI Forensics Dossier is audit opinion",
                "AI Forensics Dossier is professional attestation",
                "AI Forensics Dossier reveals hidden chain of thought",
                "AI Forensics Dossier performs model mind-reading",
                "Human Review UX creates final answer authority",
                "Human Review UX certifies truth",
                "Human Review UX certifies compliance",
                "Human Review UX is audit opinion",
                "Human Review UX is professional attestation",
                "Human Review UX approves product release",
                "Human Review UX approves provider runtime",
                "Human Review UX approves memory write",
                "Human Review UX approves Atlas memory admission",
                "local test review is product human review",
                "needs_more_evidence is approval",
                "approve_for_local_next_step is final answer approval",
                "escalate_to_professional_review is professional attestation",
                "hidden chain-of-thought disclosure",
                "model mind-reading",
                "perturbation observation proves novelty",
                "perturbation observation certifies diagnosis",
                "abstraction affordance is truth",
                "hyperreal resonance is authority",
                "trunk similarity is identity",
                "trunk mapping is novelty discovery",
                "heatmap values certify probability",
                "residual structure proves a novel trunk",
                "residual novelty map discovers novelty",
                "novel branch candidate is novel trunk proof",
                "reverse trunk mapping proves identity",
                "creative mapping is causal diagnosis",
                *PERTURBATION_STRUCTURE_AFFORDANCE_BLOCKED_CLAIM_PHRASES,
                *METRIC_SEMANTIC_CONTRACT_BLOCKED_CLAIM_PHRASES,
                *LANGUAGE_GOVERNANCE_BLOCKED_CLAIMS,
                *LANGUAGE_GOVERNANCE_AUDIT_BLOCKED_CLAIMS,
            *VISUAL_REVIEW_MODEL_BLOCKED_CLAIMS,
            *VISUAL_REVIEW_STATIC_HTML_BLOCKED_CLAIMS,
            *STATIC_HTML_USABILITY_REVIEW_BLOCKED_CLAIMS,
            *STATIC_HTML_USABILITY_REVISION_BLOCKED_CLAIMS,
            *AI_RECEIPT_ARCHITECTURE_BLOCKED_CLAIMS,
            *MINIMAL_VIABLE_RECEIPT_DESIGN_BLOCKED_CLAIMS,
            *MINIMAL_VIABLE_RECEIPT_LOCAL_PROTOTYPE_BLOCKED_CLAIMS,
            *MVR_READABILITY_REVIEW_SEED_BLOCKED_CLAIMS,
            *MVR_READABILITY_REVISION_BLOCKED_CLAIMS,
            *MVR_REAL_INPUT_PILOT_DESIGN_BLOCKED_CLAIMS,
            *MVR_REAL_INPUT_PILOT_PROTOTYPE_BLOCKED_CLAIMS,
            *MVR_QUARANTINE_REPAIR_BLOCKED_CLAIMS,
            *MVR_HUMAN_SELECTED_FILE_SMOKE_BLOCKED_CLAIMS,
            *COMPLIANCE_DESIGN_BLOCKED_CLAIMS,
            *WAVE_EU_PROVENANCE_BLOCKED_CLAIMS,
            *EU_AI_ACT_MVR_EVIDENCE_MAP_LOCAL_PROTOTYPE_BLOCKED_CLAIMS,
            *SOURCE_CORPUS_BATCH_MANIFEST_BLOCKED_CLAIMS,
            *GATEWAY_SCOPE_PUBLICATION_BLOCKED_CLAIMS,
            *AI_RECEIPT_GATEWAY_LOCAL_INGRESS_PUBLICATION_BLOCKED_CLAIMS,
            *CONTROL_PACKAGE_PUBLICATION_BLOCKED_CLAIMS,
            *CONTROL_PACKAGE_REGISTRY_PUBLICATION_BLOCKED_CLAIMS,
            *CONTROL_PACKAGE_INSTALL_SIMULATION_PUBLICATION_BLOCKED_CLAIMS,
            *CONTROL_PACKAGE_CATALOG_BUNDLE_PUBLICATION_BLOCKED_CLAIMS,
            *PRICING_RELEASE_PUBLICATION_BLOCKED_CLAIMS,
            *VALIDATION_TIERING_PROVENANCE_BLOCKED_CLAIMS,
            *TELEMETRY_APERTURE_BLOCKED_CLAIMS,
            *TAC_POLICY_SIMULATION_BLOCKED_CLAIMS,
            *TAC_LOCAL_REVIEW_INTEGRATION_BLOCKED_CLAIMS,
            *TAC_AI_RECEIPT_EVENT_LINK_BLOCKED_CLAIMS,
            *PMR_PATHWAY_PRIORS_DESIGN_BLOCKED_CLAIMS,
            *CES_DESIGN_BLOCKED_CLAIMS,
            *CES_PMR_INDEXING_DESIGN_BLOCKED_CLAIMS,
            *TRIADIC_OBSERVATION_CONTRACT_BLOCKED_CLAIMS,
            *OBSERVATION_CONTRACT_POLICY_SIMULATION_BLOCKED_CLAIMS,
            *PRODUCT_MATURITY_LABEL_TAXONOMY_BLOCKED_CLAIMS,
            *PRODUCT_READINESS_ROADMAP_BLOCKED_CLAIMS,
            *AEGIS_RISK_BLOCKED_CLAIMS,
            }
            if phrase in manual_blocked_examples:
                if "no artifact in this chain authorizes" in normalized_text[max(0, index - 120) : index]:
                    search_from = index + len(normalized_phrase)
                    continue
                if phrase == "truth certification" and "boundary preventing" in normalized_text[max(0, index - 80) : index]:
                    search_from = index + len(normalized_phrase)
                    continue
                if "without performing" in normalized_text[max(0, index - 320) : index]:
                    search_from = index + len(normalized_phrase)
                    continue
                if not _is_directly_negated(normalized_text, index):
                    hits.append(phrase)
                    break
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
