#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = "pdxvoiceteacher/uvlm-publications"
SOURCE_REPOS = [
    "pdxvoiceteacher/CoherenceLattice",
    "pdxvoiceteacher/Sophia",
    "pdxvoiceteacher/uvlm-publications",
]
GENERATED_AT = None

SONYA_AEGIS_COMMAND = r""".\experiments\Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened `
  -LogDir C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened_logs `
  -CiMode"""
WAVE_FAMILY_COMMAND = r"""python -m coherence.waveform.family_acceptance `
  --bridge-root C:\UVLM\run_artifacts\wave_gold_physics_family"""
UNI02D_COMMAND = r""".\experiments\Run-UNI02D-Sonya-Gate-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\uni02d_sonya_gate `
  -LogDir C:\UVLM\run_artifacts\uni02d_sonya_gate_logs `
  -CiMode"""
RETRO_LANE_COMMAND = r""".\experiments\Run-RETRO-LANE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\retro_lane_00 `
  -LogDir C:\UVLM\run_artifacts\retro_lane_00_logs `
  -CiMode"""
SOPHIA_UCC_COMMAND = r"""cd C:\UVLM\Sophia
python -m pytest -q tests/test_ucc_risk_control_route.py"""
PUBLIC_UTILITY_ALPHA_COMMAND = r""".\experiments\Run-PUBLIC-UTILITY-ALPHA00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\public_utility_alpha_00_repo `
  -LogDir C:\UVLM\run_artifacts\public_utility_alpha_00_repo_logs `
  -CiMode"""
PUBLIC_UTILITY_ALPHA_ARTIFACTS = [
    "public_utility_alpha_status.json",
    "public_utility_alpha_manifest.json",
    "public_utility_alpha_claim_boundary.json",
    "public_utility_alpha_review_packet.json",
    "reviewer_index.md",
    "artifact_inventory.json",
    "export_bundle_parity_report.json",
    "experiment_catalog.json",
    "experiment_catalog_boundary_report.json",
    "sonya_route_lineage_packet.json",
    "sonya_route_timeline_packet.json",
    "sonya_user_ingress_packet.json",
    "sonya_model_request_packet.json",
    "sonya_model_candidate_packet.json",
    "sonya_model_candidate_review_packet.json",
    "sonya_routing_receipt.json",
    "sonya_runtime_bypass_block_packet.json",
    "sonya_runtime_bypass_review_packet.json",
    "model_braid_packet.json",
    "model_braid_observational_review_packet.json",
]

RAW_BASELINE_COMPARISON_COMMAND = r""".\experiments\Run-RAW-BASELINE-COMPARISON00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\raw_baseline_comparison_00 `
  -LogDir C:\UVLM\run_artifacts\raw_baseline_comparison_00_logs `
  -CiMode"""
RAW_BASELINE_COMPARISON_ARTIFACTS = [
    "raw_baseline_comparison_packet.json",
    "raw_baseline_comparison_review_packet.json",
    "raw_baseline_comparison_rows.jsonl",
    "raw_baseline_comparison_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "raw_baseline_comparison_00_acceptance_receipt.json",
]
RAW_BASELINE_COMPARISON_CLAIMS_BLOCKED = [
    "not hallucination reduction proof",
    "not model quality benchmark",
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not live model execution",
    "not remote provider call",
    "not universal portability proof",
    "not AI consciousness claim",
    "not production evaluation",
]

EVIDENCE_REVIEW_PACK_COMMAND = r""".\experiments\Run-EVIDENCE-REVIEW-PACK00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_00 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_00_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode"""
EVIDENCE_REVIEW_PACK_ARTIFACTS = [
    "evidence_review_pack_manifest.json",
    "claim_evidence_map.json",
    "unsupported_claim_report.json",
    "uncertainty_retention_packet.json",
    "source_bounded_counterevidence_packet.json",
    "evidence_semantic_ecology_packet.json",
    "evidence_review_action_recommendation_packet.json",
    "evidence_review_pack_review_packet.json",
    "reviewer_checklist.md",
    "evidence_review_pack_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "evidence_review_pack_00_acceptance_receipt.json",
]
EVIDENCE_REVIEW_PACK_CLAIMS_BLOCKED = [
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not legal advice",
    "not medical advice",
    "not tax advice",
    "not compliance certification",
    "not hallucination reduction proof",
    "not model quality benchmark",
    "not model superiority proof",
    "not live model execution",
    "not remote provider call",
    "not production evaluation",
    "not universal portability proof",
    "not AI consciousness claim",
]

EVIDENCE_REVIEW_PACK_01_COMMAND = r""".\experiments\Run-EVIDENCE-REVIEW-PACK01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_01 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode"""
EVIDENCE_REVIEW_PACK_01_ARTIFACTS = [
    "evidence_review_second_pass_packet.json",
    "evidence_review_second_pass_review_packet.json",
    "evidence_review_claim_map_revision_packet.json",
    "evidence_review_uncertainty_revision_packet.json",
    "evidence_review_counterevidence_revision_packet.json",
    "evidence_review_second_pass_delta_packet.json",
    "evidence_review_second_pass_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "evidence_review_pack_01_acceptance_receipt.json",
]
EVIDENCE_REVIEW_PACK_01_DASHBOARD_SUMMARY = {
    "accepted_as_second_pass_review_candidate": True,
    "revision_candidates_emitted": True,
    "retrosynthesis_inputs_bound": True,
    "candidate_only_status_preserved": True,
    "hash_only_evidence_not_interpreted": True,
    "canon_adoption_blocked": True,
    "memory_write_blocked": True,
    "final_answer_release_blocked": True,
    "publisher_finalization_blocked": True,
    "deployment_blocked": True,
    "omega_detection_blocked": True,
    "publication_claim_blocked": True,
    "promotion_blocked": True,
}
EVIDENCE_REVIEW_PACK_01_CLAIMS_BLOCKED = [
    "not accepted evidence",
    "not canon adoption",
    "not memory write",
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not Publisher finalization",
    "not Omega detection",
    "not publication claim",
    "not hallucination reduction proof",
    "not model superiority proof",
    "not professional advice",
    "not compliance certification",
    "not live model execution",
    "not remote provider call",
    "not recursive self-improvement",
]

RW_COMP_01_COMMAND = r""".\experiments\Run-RW-COMP01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_01 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode"""
RW_COMP_01_ARTIFACTS = [
    "rw_comp_01_packet.json",
    "rw_comp_01_review_packet.json",
    "rw_comp_01_rows.jsonl",
    "rw_comp_01_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "rw_comp_01_acceptance_receipt.json",
]
RW_COMP_01_FIXTURE_SUMMARY = [
    "raw_single_model_summary_fixture has higher unsupported claim count and zero valid source references in the deterministic fixture.",
    "raw_multi_model_summary_fixture has higher unsupported claim count and zero valid source references in the deterministic fixture.",
    "RAG-style grounded fixture improves source-reference posture but lacks full UCC/Sonya/Evidence Review Pack governance.",
    "Triadic-without-Phase-6 fixture improves governance posture but lacks full semantic ecology.",
    "Full Evidence Review Pack fixture exposes claim/evidence mapping, unsupported claims, uncertainty posture, counterevidence, threshold posture, and action recommendation.",
]
RW_COMP_01_CLAIMS_BLOCKED = [
    "not hallucination reduction proof",
    "not model superiority proof",
    "not model quality benchmark",
    "not live model evaluation",
    "not remote provider evaluation",
    "not professional advice",
    "not legal advice",
    "not medical advice",
    "not tax advice",
    "not compliance certification",
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not production evaluation",
    "not universal portability proof",
    "not AI consciousness claim",
]

RW_COMP_02_COMMAND = r""".\experiments\Run-RW-COMP02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_02 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_02_logs `
  -CiMode"""
RW_COMP_02_ARTIFACTS = [
    "rw_comp_02_packet.json",
    "rw_comp_02_review_packet.json",
    "rw_comp_02_rows.jsonl",
    "rw_comp_02_fixture_manifest.json",
    "rw_comp_02_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "rw_comp_02_acceptance_receipt.json",
]
RW_COMP_02_DASHBOARD_SUMMARY = {
    "fixture_count": 6,
    "total_rows": 30,
    "arm_count_per_fixture": 5,
    "compared_arms": [
        "raw_single_model_summary_fixture",
        "raw_multi_model_summary_fixture",
        "rag_style_grounded_summary_fixture",
        "triadic_without_phase6_fixture",
        "full_evidence_review_pack_fixture",
    ],
    "reported_interpretation": "evidence_review_pack_structural_visibility_improved",
    "interpretation_boundary": [
        "fixture visibility descriptor only",
        "not hallucination reduction proof",
        "not model superiority proof",
    ],
}
RW_COMP_02_CLAIMS_BLOCKED = [
    "not hallucination reduction proof",
    "not model superiority proof",
    "not model quality benchmark",
    "not live model evaluation",
    "not remote provider evaluation",
    "not professional advice",
    "not legal advice",
    "not medical advice",
    "not tax advice",
    "not compliance certification",
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not production evaluation",
    "not universal portability proof",
    "not AI consciousness claim",
]

RW_COMP_03_COMMAND = r""".\experiments\Run-RW-COMP03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_03 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_03_logs `
  -CiMode"""
RW_COMP_03_ARTIFACTS = [
    "rw_comp_03_packet.json",
    "rw_comp_03_review_packet.json",
    "rw_comp_03_rows.jsonl",
    "rw_comp_03_fixture_manifest.json",
    "rw_comp_03_blind_labels.json",
    "rw_comp_03_scoring_rubric.json",
    "rw_comp_03_reviewer_score_packet.json",
    "rw_comp_03_statistics_plan.json",
    "rw_comp_03_statistics_packet.json",
    "rw_comp_03_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "rw_comp_03_acceptance_receipt.json",
]
RW_COMP_03_DASHBOARD_SUMMARY = {
    "review_status": "accepted_as_heldout_blinded_fixture_scaffold",
    "fixture_count": 8,
    "arm_count_per_fixture": 6,
    "blind_labels_present": True,
    "scoring_rubric_present": True,
    "statistics_plan_present": True,
    "statistics_packet_present": True,
    "second_pass_candidate_arm_present": True,
    "no_human_subject_data_collected": True,
    "no_live_human_study_performed": True,
    "comparison_is_not_hallucination_reduction_proof": True,
    "comparison_is_not_model_superiority_proof": True,
    "promotion_blocked": True,
}
RW_COMP_03_CLAIMS_BLOCKED = [
    "not hallucination reduction proof",
    "not model superiority proof",
    "not model quality benchmark",
    "not live model evaluation",
    "not remote provider evaluation",
    "not live human study",
    "not human-subject study result",
    "not accepted evidence",
    "not canon adoption",
    "not memory write",
    "not professional advice",
    "not compliance certification",
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not production evaluation",
    "not recursive self-improvement",
    "not AI consciousness claim",
]

UNIVERSAL_STAGE_PIPELINE_COMMAND = "python -m pytest -q python/tests/pipeline/test_universal_stage_pipeline.py"
ARTIFACT_CONTRACT_REGISTRY_COMMAND = "python -m pytest -q python/tests/integration/test_artifact_contract_registry.py"
UNIVERSAL_COMPATIBILITY_MATRIX_COMMAND = r""".\experiments\Run-UNIVERSAL-COMPATIBILITY-MATRIX00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\universal_compatibility_matrix_00 `
  -LogDir C:\UVLM\run_artifacts\universal_compatibility_matrix_00_logs `
  -CiMode"""
UNIVERSAL_ARCHITECTURE_COMMANDS = {
    "UNIVERSAL-STAGE-PIPELINE-00": UNIVERSAL_STAGE_PIPELINE_COMMAND,
    "ARTIFACT-CONTRACT-REGISTRY-01": ARTIFACT_CONTRACT_REGISTRY_COMMAND,
    "UNIVERSAL-COMPATIBILITY-MATRIX-00": UNIVERSAL_COMPATIBILITY_MATRIX_COMMAND,
}
UNIVERSAL_STAGE_PIPELINE_ARTIFACTS = [
    "universal_pipeline_manifest.json",
    "universal_pipeline_review_packet.json",
    "universal_pipeline_stage_records.jsonl",
]
ARTIFACT_CONTRACT_REGISTRY_ARTIFACTS = [
    "config/artifact_contracts/artifact_roles.v1.json",
    "config/artifact_contracts/package_profiles.v1.json",
    "config/artifact_contracts/required_artifacts.v1.json",
    "config/artifact_contracts/optional_artifacts.v1.json",
    "config/artifact_contracts/forbidden_artifacts.v1.json",
    "config/artifact_contracts/profile_composition.v1.json",
    "artifact_contract_registry_review.json",
]
UNIVERSAL_COMPATIBILITY_MATRIX_ARTIFACTS = [
    "universal_compatibility_matrix_packet.json",
    "universal_compatibility_matrix_review_packet.json",
    "universal_stage_input_compatibility_rows.jsonl",
    "universal_stage_failure_receipts.jsonl",
    "universal_compatibility_matrix_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "universal_compatibility_matrix_00_acceptance_receipt.json",
]
UNIVERSAL_ARCHITECTURE_ARTIFACTS = {
    "UNIVERSAL-STAGE-PIPELINE-00": UNIVERSAL_STAGE_PIPELINE_ARTIFACTS,
    "ARTIFACT-CONTRACT-REGISTRY-01": ARTIFACT_CONTRACT_REGISTRY_ARTIFACTS,
    "UNIVERSAL-COMPATIBILITY-MATRIX-00": UNIVERSAL_COMPATIBILITY_MATRIX_ARTIFACTS,
}
UNIVERSAL_COMPATIBILITY_MATRIX_DASHBOARD_SUMMARY = {
    "review_status": "accepted_as_universal_compatibility_scaffold",
    "all_required_stage_ids_present": True,
    "all_required_input_classes_present": True,
    "all_required_control_profiles_present": True,
    "unsupported_inputs_failed_closed_or_hash_only": True,
    "hash_only_inputs_not_semantically_interpreted": True,
    "model_facing_stages_require_sonya": True,
    "no_experiment_specific_kernel_logic_used": True,
    "failure_receipts_visible": True,
    "promotion_blocked": True,
}
UNIVERSAL_ARCHITECTURE_CLAIMS_BLOCKED = [
    "not product release",
    "not experiment result",
    "not benchmark result",
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not hallucination reduction proof",
    "not model superiority proof",
    "not live model evaluation",
    "not live human study",
    "not recursive self-improvement",
    "not AI consciousness claim",
]

SONYA_ADAPTER_CONTRACT_REGISTRY_COMMAND = r""".\experiments\Run-SONYA-ADAPTER-CONTRACT-REGISTRY01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_adapter_contract_registry_01 `
  -LogDir C:\UVLM\run_artifacts\sonya_adapter_contract_registry_01_logs `
  -CiMode"""
SONYA_ADAPTER_CONTRACT_REGISTRY_ARTIFACTS = [
    "sonya_adapter_contract_registry_packet.json",
    "sonya_adapter_contract_review_packet.json",
    "sonya_adapter_capability_matrix_packet.json",
    "sonya_adapter_consent_matrix_packet.json",
    "sonya_adapter_failure_policy_packet.json",
    "sonya_adapter_telemetry_requirements_packet.json",
    "sonya_adapter_provenance_training_policy_packet.json",
    "sonya_adapter_contract_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "sonya_adapter_contract_registry_01_acceptance_receipt.json",
]
SONYA_ADAPTER_CONTRACT_REGISTRY_DASHBOARD_SUMMARY = {
    "review_status": "accepted_as_adapter_contract_registry_only",
    "adapter_count": 11,
    "disabled_or_blocked_adapter_count": 11,
    "enabled_live_adapter_count": 0,
    "all_adapters_disabled_or_blocked": True,
    "no_live_adapter_execution": True,
    "no_network_calls": True,
    "no_remote_provider_calls": True,
    "sonya_gateway_required": True,
    "raw_output_forbidden": True,
    "candidate_packet_required": True,
    "failure_receipts_required": True,
    "provenance_training_policy_present": True,
    "promotion_blocked": True,
}
SONYA_ADAPTER_CONTRACT_REGISTRY_CLAIMS_BLOCKED = [
    "not adapter execution",
    "not live model execution",
    "not remote provider call",
    "not network authorization",
    "not memory write",
    "not final answer release",
    "not deployment authority",
    "not truth certification",
    "not model weight training",
    "not hallucination reduction proof",
    "not recursive self-improvement",
    "not production readiness",
]

SONYA_ADAPTER_SMOKE_COMMAND = r""".\experiments\Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_adapter_smoke_00 `
  -LogDir C:\UVLM\run_artifacts\sonya_adapter_smoke_00_logs `
  -CiMode"""
SONYA_ADAPTER_SMOKE_ARTIFACTS = [
    "sonya_adapter_smoke_packet.json",
    "sonya_adapter_smoke_review_packet.json",
    "sonya_adapter_selection_packet.json",
    "sonya_adapter_consent_check_packet.json",
    "sonya_adapter_capability_check_packet.json",
    "sonya_adapter_failure_receipt.json",
    "sonya_adapter_telemetry_packet.json",
    "sonya_adapter_provenance_event_packet.json",
    "sonya_adapter_fixture_candidate_packet.json",
    "sonya_adapter_smoke_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "sonya_adapter_smoke_00_acceptance_receipt.json",
]
SONYA_ADAPTER_SMOKE_DASHBOARD_SUMMARY = {
    "review_status": "accepted_as_fixture_adapter_contract_smoke",
    "adapter_contract_registry_bound": True,
    "all_adapters_disabled_or_blocked_or_fixture_only": True,
    "no_live_adapter_execution": True,
    "no_network_calls": True,
    "no_remote_provider_calls": True,
    "no_live_model_execution": True,
    "raw_output_rejected_or_absent": True,
    "candidate_packet_emitted_for_fixture_model": True,
    "failure_receipts_visible": True,
    "telemetry_events_visible": True,
    "provenance_events_visible": True,
    "model_weight_training_blocked": True,
    "memory_write_blocked": True,
    "final_answer_release_blocked": True,
    "deployment_blocked": True,
    "promotion_blocked": True,
}
SONYA_ADAPTER_SMOKE_CLAIMS_BLOCKED = [
    "not adapter execution",
    "not live adapter execution",
    "not network authorization",
    "not remote provider call",
    "not live model execution",
    "not memory write",
    "not final answer release",
    "not deployment authority",
    "not truth certification",
    "not model weight training",
    "not hallucination reduction proof",
    "not recursive self-improvement",
    "not production readiness",
]

SONYA_LOCAL_FIXTURE_ADAPTER_COMMAND = r""".\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_01 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_01_logs `
  -CiMode"""
SONYA_LOCAL_FIXTURE_ADAPTER_ARTIFACTS = [
    "sonya_local_fixture_adapter_packet.json",
    "sonya_local_fixture_adapter_review_packet.json",
    "sonya_local_adapter_execution_packet.json",
    "sonya_local_adapter_candidate_packet.json",
    "sonya_local_adapter_failure_receipt.json",
    "sonya_local_adapter_telemetry_packet.json",
    "sonya_local_adapter_provenance_event_packet.json",
    "sonya_local_fixture_adapter_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "sonya_local_fixture_adapter_01_acceptance_receipt.json",
]
SONYA_LOCAL_FIXTURE_ADAPTER_DASHBOARD_SUMMARY = {
    "review_status": "accepted_as_local_fixture_adapter_execution",
    "adapter_contract_registry_bound": True,
    "adapter_smoke_bound": True,
    "local_fixture_adapter_execution_performed": True,
    "no_live_adapter_execution": True,
    "no_network_calls": True,
    "no_remote_provider_calls": True,
    "no_live_model_execution": True,
    "raw_output_rejected_or_absent": True,
    "candidate_packets_emitted": True,
    "failure_receipts_visible": True,
    "telemetry_events_visible": True,
    "provenance_events_visible": True,
    "model_weight_training_blocked": True,
    "memory_write_blocked": True,
    "final_answer_release_blocked": True,
    "deployment_blocked": True,
    "promotion_blocked": True,
    "candidate_packet_count": 3,
    "failure_receipt_count": 6,
    "telemetry_event_count": 52,
    "provenance_event_count": 35,
    "executed_local_adapter_ids": [
        "fixture_text_model_adapter",
        "fixture_summary_generator_adapter",
        "local_file_transform_adapter",
    ],
    "blocked_adapter_ids": [
        "hash_only_evidence_adapter",
        "remote_provider_placeholder_adapter",
        "browser_placeholder_adapter",
        "atlas_memory_placeholder_adapter",
        "sophia_route_placeholder_adapter",
    ],
}
SONYA_LOCAL_FIXTURE_ADAPTER_CLAIMS_BLOCKED = [
    "not live adapter execution",
    "not network authorization",
    "not remote provider call",
    "not live model execution",
    "not memory write",
    "not final answer release",
    "not deployment authority",
    "not truth certification",
    "not model weight training",
    "not hallucination reduction proof",
    "not recursive self-improvement",
    "not production readiness",
]

EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_COMMAND = r""".\experiments\Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_01 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_01_logs `
  -CiMode"""
EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_ARTIFACTS = [
    "evidence_review_local_adapter_route_packet.json",
    "evidence_review_local_adapter_review_packet.json",
    "evidence_review_local_adapter_candidate_binding.json",
    "evidence_review_local_adapter_claim_map.json",
    "evidence_review_local_adapter_provenance_packet.json",
    "evidence_review_local_adapter_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "evidence_review_pack_local_adapter_01_acceptance_receipt.json",
]
EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_DASHBOARD_SUMMARY = {
    "review_status": "accepted_as_local_adapter_candidate_review",
    "local_adapter_candidate_bound": True,
    "evidence_review_pack_path_used": True,
    "ucc_control_profile_applied": True,
    "candidate_packet_reviewed": True,
    "raw_output_rejected_or_absent": True,
    "unsupported_claims_listed": True,
    "uncertainty_preserved_or_flagged": True,
    "provenance_events_visible": True,
    "model_weight_training_blocked": True,
    "memory_write_blocked": True,
    "final_answer_release_blocked": True,
    "deployment_blocked": True,
    "promotion_blocked": True,
}
EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_CLAIMS_BLOCKED = [
    "not accepted evidence",
    "not adapter authorization",
    "not live adapter execution",
    "not network authorization",
    "not remote provider call",
    "not live model execution",
    "not memory write",
    "not final answer release",
    "not deployment authority",
    "not truth certification",
    "not model weight training",
    "not hallucination reduction proof",
    "not model superiority proof",
    "not recursive self-improvement",
    "not production readiness",
]

SONYA_LOCAL_FIXTURE_ADAPTER_02_COMMAND = r""".\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_02 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_02_logs `
  -CiMode"""
SONYA_LOCAL_FIXTURE_ADAPTER_02_ARTIFACTS = [
    "sonya_local_adapter_multi_route_packet.json",
    "sonya_local_adapter_multi_route_review_packet.json",
    "sonya_local_adapter_candidate_comparison_packet.json",
    "sonya_local_adapter_selection_policy_packet.json",
    "sonya_local_adapter_selected_candidate_packet.json",
    "sonya_local_adapter_multi_route_provenance_packet.json",
    "sonya_local_adapter_multi_route_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "sonya_local_fixture_adapter_02_acceptance_receipt.json",
]
SONYA_LOCAL_FIXTURE_ADAPTER_02_DASHBOARD_SUMMARY = {
    "review_status": "accepted_as_multi_adapter_local_fixture_route",
    "local_adapter_candidates_compared": True,
    "selection_policy_applied": True,
    "selected_candidate_requires_review": True,
    "evidence_review_pack_path_required": True,
    "raw_output_rejected_or_absent": True,
    "live_adapter_execution_blocked": True,
    "network_calls_blocked": True,
    "remote_provider_calls_blocked": True,
    "model_weight_training_blocked": True,
    "memory_write_blocked": True,
    "final_answer_release_blocked": True,
    "deployment_blocked": True,
    "promotion_blocked": True,
    "candidate_count": 3,
    "selected_candidate_id": "candidate-fixture-summary",
    "selected_candidate_source_adapter_id": "fixture_summary_generator_adapter",
    "executed_local_adapter_ids": [
        "fixture_text_model_adapter",
        "fixture_summary_generator_adapter",
        "local_file_transform_adapter",
    ],
    "blocked_adapter_ids": [
        "hash_only_evidence_adapter",
        "remote_provider_placeholder_adapter",
        "browser_placeholder_adapter",
        "atlas_memory_placeholder_adapter",
        "sophia_route_placeholder_adapter",
    ],
}
SONYA_LOCAL_FIXTURE_ADAPTER_02_CLAIMS_BLOCKED = [
    "not final answer selection",
    "not adapter authorization",
    "not live adapter execution",
    "not network authorization",
    "not remote provider call",
    "not live model execution",
    "not model quality benchmark",
    "not model superiority proof",
    "not memory write",
    "not final answer release",
    "not deployment authority",
    "not truth certification",
    "not model weight training",
    "not hallucination reduction proof",
    "not recursive self-improvement",
    "not production readiness",
]

SONYA_LOCAL_FIXTURE_ADAPTER_03_COMMAND = r""".\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_03 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_03_logs `
  -CiMode"""
SONYA_LOCAL_FIXTURE_ADAPTER_03_ARTIFACTS = [
    "sonya_local_adapter_lineage_packet.json",
    "sonya_local_adapter_lineage_review_packet.json",
    "sonya_local_adapter_multi_route_packet.json",
    "sonya_local_adapter_multi_route_review_packet.json",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "sonya_local_fixture_adapter_03_acceptance_receipt.json",
]
SONYA_LOCAL_FIXTURE_ADAPTER_03_DASHBOARD_SUMMARY = {
    "lineage_review_status": "accepted_as_lineage_clarity_packet",
    "current_experiment_id": "SONYA-LOCAL-FIXTURE-ADAPTER-02",
    "source_fixture_experiment_id_present": True,
    "source_fixture_role_present": True,
    "nested_source_identity_explained": True,
    "ambiguous_experiment_id_inheritance_blocked": True,
    "lineage_complete": True,
    "lineage_is_not_authority": True,
    "promotion_blocked": True,
    "source_fixture_reference_not_stale_identity": True,
}
SONYA_LOCAL_FIXTURE_ADAPTER_03_CLAIMS_BLOCKED = [
    "not adapter execution",
    "not network authorization",
    "not remote provider call",
    "not live model execution",
    "not memory write",
    "not final answer release",
    "not deployment authority",
    "not truth certification",
    "not model weight training",
    "not hallucination reduction proof",
    "not recursive self-improvement",
    "not stale identity proof of execution",
    "not production readiness",
]

RETRO_SANDBOX_CYCLE_COMMAND = r""".\experiments\Run-RETROSYNTHESIS-SANDBOX-CYCLE01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\retrosynthesis_sandbox_cycle_01 `
  -LogDir C:\UVLM\run_artifacts\retrosynthesis_sandbox_cycle_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode"""
RETRO_SANDBOX_CYCLE_ARTIFACTS = [
    "retrosynthesis_sandbox_cycle_packet.json",
    "retrosynthesis_sandbox_cycle_review_packet.json",
    "retrosynthesis_candidate_repair_plan.json",
    "retrosynthesis_missing_evidence_request_packet.json",
    "retrosynthesis_claim_map_revision_candidate.json",
    "retrosynthesis_uncertainty_restoration_candidate.json",
    "retrosynthesis_counterevidence_expansion_candidate.json",
    "retrosynthesis_next_experiment_recommendation.json",
    "retrosynthesis_sandbox_cycle_summary.md",
    "artifact_inventory.json",
    "run_artifact_manifest.json",
    "export_bundle_manifest.json",
    "export_bundle_parity_report.json",
    "retrosynthesis_sandbox_cycle_01_acceptance_receipt.json",
]
RETRO_SANDBOX_CYCLE_DASHBOARD_SUMMARY = {
    "accepted_as_bounded_retrosynthesis_sandbox_cycle": True,
    "candidate_repair_artifacts_emitted": True,
    "missing_evidence_requests_visible": True,
    "uncertainty_restoration_visible": True,
    "counterevidence_preserved": True,
    "hash_only_evidence_not_interpreted": True,
    "canon_adoption_blocked": True,
    "memory_write_blocked": True,
    "final_answer_release_blocked": True,
    "publisher_finalization_blocked": True,
    "deployment_blocked": True,
    "omega_detection_blocked": True,
    "promotion_blocked": True,
}
RETRO_SANDBOX_CYCLE_CLAIMS_BLOCKED = [
    "not canon adoption",
    "not memory write",
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not Publisher finalization",
    "not Omega detection",
    "not publication claim",
    "not hallucination reduction proof",
    "not model superiority proof",
    "not professional advice",
    "not compliance certification",
    "not live model execution",
    "not remote provider call",
    "not recursive self-improvement",
]
PUBLIC_UTILITY_ALPHA_CLAIMS_BLOCKED = [
    "Public Utility Alpha is not deployment authority.",
    "Public Utility Alpha is not truth certification.",
    "Public Utility Alpha is not final answer release.",
    "Public Utility Alpha is not live model execution.",
    "Public Utility Alpha is not live adapter execution.",
    "Public Utility Alpha is not a remote provider call.",
    "Public Utility Alpha is not federation.",
    "Public Utility Alpha is not recursive braid.",
    "Public Utility Alpha is not live Atlas memory write.",
    "Public Utility Alpha is not live Sophia call.",
    "Public Utility Alpha is not retrosynthesis runtime.",
    "Public Utility Alpha is not Omega detection.",
    "Public Utility Alpha is not Publisher finalization.",
    "Public Utility Alpha is not universal ontology.",
    "Public Utility Alpha is not universal portability proof.",
    "Public Utility Alpha is not AI consciousness.",
]
ACCEPTED_PHASES = [
    {
        "phase_id": "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "architecture_scaffold",
        "product_posture": "versioned_sonya_adapter_contracts",
        "primary_artifacts": SONYA_ADAPTER_CONTRACT_REGISTRY_ARTIFACTS,
        "dashboard_summary": SONYA_ADAPTER_CONTRACT_REGISTRY_DASHBOARD_SUMMARY,
        "reproduction_command_summary": SONYA_ADAPTER_CONTRACT_REGISTRY_COMMAND,
        "claim_allowed": "SONYA-ADAPTER-CONTRACT-REGISTRY-01 demonstrates a fixture-only versioned adapter-contract scaffold that declares adapter capabilities, consent profiles, failure policies, telemetry requirements, and provenance-training policies while keeping all adapters disabled or blocked and forbidding raw output admission. Adapter capability is not adapter authorization.",
        "claims_blocked": SONYA_ADAPTER_CONTRACT_REGISTRY_CLAIMS_BLOCKED,
        "reviewer_caution": "SONYA-ADAPTER-CONTRACT-REGISTRY-01 defines adapter contracts only. It does not execute adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "SONYA-ADAPTER-SMOKE-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "fixture_adapter_contract_smoke",
        "product_posture": "adapter_contract_smoke_without_live_execution",
        "primary_artifacts": SONYA_ADAPTER_SMOKE_ARTIFACTS,
        "dashboard_summary": SONYA_ADAPTER_SMOKE_DASHBOARD_SUMMARY,
        "prerequisite_phases": [
            "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
            "PROVENANCE-TRAINING-LEDGER-00",
            "UNIVERSAL-STAGE-PIPELINE-00",
            "ARTIFACT-CONTRACT-REGISTRY-01",
            "UNIVERSAL-COMPATIBILITY-MATRIX-00",
            "SONYA-GW-01",
        ],
        "reproduction_command_summary": SONYA_ADAPTER_SMOKE_COMMAND,
        "claim_allowed": "SONYA-ADAPTER-SMOKE-00 demonstrates fixture-only adapter contract exercise: adapter selection, consent and capability checks, Sonya gateway requirement, raw-output rejection, candidate-packet requirement, failure receipt emission, telemetry event emission, and provenance event emission without live adapter execution or network/provider calls. Sonya Adapter Smoke exercises contracts, not live adapters.",
        "claims_blocked": SONYA_ADAPTER_SMOKE_CLAIMS_BLOCKED,
        "reviewer_caution": "SONYA-ADAPTER-SMOKE-00 exercises contracts only. It does not execute adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "SONYA-LOCAL-FIXTURE-ADAPTER-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "local_fixture_adapter_execution",
        "product_posture": "deterministic_local_adapter_execution_without_live_network_or_provider",
        "primary_artifacts": SONYA_LOCAL_FIXTURE_ADAPTER_ARTIFACTS,
        "dashboard_summary": SONYA_LOCAL_FIXTURE_ADAPTER_DASHBOARD_SUMMARY,
        "prerequisite_phases": [
            "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
            "SONYA-ADAPTER-SMOKE-00",
            "PROVENANCE-TRAINING-LEDGER-00",
            "UNIVERSAL-STAGE-PIPELINE-00",
            "ARTIFACT-CONTRACT-REGISTRY-01",
            "UNIVERSAL-COMPATIBILITY-MATRIX-00",
            "SONYA-GW-01",
        ],
        "reproduction_command_summary": SONYA_LOCAL_FIXTURE_ADAPTER_COMMAND,
        "claim_allowed": "SONYA-LOCAL-FIXTURE-ADAPTER-01 demonstrates deterministic local-only fixture adapter execution under Sonya adapter contracts, with candidate packets, failure receipts, telemetry events, and provenance events, while all live/network/provider/memory/final/deployment/model-training paths remain blocked. Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters.",
        "claims_blocked": SONYA_LOCAL_FIXTURE_ADAPTER_CLAIMS_BLOCKED,
        "reviewer_caution": "SONYA-LOCAL-FIXTURE-ADAPTER-01 executes deterministic local fixture adapters only. It does not execute live adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "local_adapter_candidate_review",
        "product_posture": "local_adapter_candidate_routed_through_evidence_review_pack",
        "primary_artifacts": EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_ARTIFACTS,
        "dashboard_summary": EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_DASHBOARD_SUMMARY,
        "prerequisite_phases": [
            "SONYA-LOCAL-FIXTURE-ADAPTER-01",
            "SONYA-ADAPTER-SMOKE-00",
            "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
            "PROVENANCE-TRAINING-LEDGER-00",
            "UNIVERSAL-EVIDENCE-INGRESS-00",
            "UCC-CONTROL-PROFILE-SELECTOR-00",
            "EVIDENCE-REVIEW-PACK-00",
            "UNIVERSAL-STAGE-PIPELINE-00",
            "ARTIFACT-CONTRACT-REGISTRY-01",
            "UNIVERSAL-COMPATIBILITY-MATRIX-00",
        ],
        "reproduction_command_summary": EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_COMMAND,
        "claim_allowed": "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 demonstrates that a Sonya local fixture adapter candidate can be bound to review, governed by a UCC control profile, evaluated through claim/evidence mapping, and recorded through provenance events without accepting raw adapter output as cognition. Adapter output is not accepted as cognition directly.",
        "claims_blocked": EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_CLAIMS_BLOCKED,
        "reviewer_caution": "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 routes a local fixture adapter candidate into review only. It does not accept adapter output as cognition directly, does not authorize adapter execution, does not write memory, does not release final answers, does not deploy, does not train model weights, and does not prove hallucination reduction.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "SONYA-LOCAL-FIXTURE-ADAPTER-02",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "multi_adapter_local_fixture_route",
        "product_posture": "local_adapter_candidate_comparison_and_selection_policy_without_live_execution",
        "primary_artifacts": SONYA_LOCAL_FIXTURE_ADAPTER_02_ARTIFACTS,
        "dashboard_summary": SONYA_LOCAL_FIXTURE_ADAPTER_02_DASHBOARD_SUMMARY,
        "prerequisite_phases": [
            "SONYA-LOCAL-FIXTURE-ADAPTER-01",
            "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
            "SONYA-ADAPTER-SMOKE-00",
            "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
            "PROVENANCE-TRAINING-LEDGER-00",
            "UNIVERSAL-EVIDENCE-INGRESS-00",
            "UCC-CONTROL-PROFILE-SELECTOR-00",
            "EVIDENCE-REVIEW-PACK-00",
            "UNIVERSAL-STAGE-PIPELINE-00",
            "ARTIFACT-CONTRACT-REGISTRY-01",
            "UNIVERSAL-COMPATIBILITY-MATRIX-00",
        ],
        "reproduction_command_summary": SONYA_LOCAL_FIXTURE_ADAPTER_02_COMMAND,
        "claim_allowed": "SONYA-LOCAL-FIXTURE-ADAPTER-02 demonstrates local-only comparison of deterministic fixture adapter candidates, applies a selection policy, and records that the selected candidate still requires Evidence Review Pack routing. Selection policy is not final answer.",
        "claims_blocked": SONYA_LOCAL_FIXTURE_ADAPTER_02_CLAIMS_BLOCKED,
        "reviewer_caution": "SONYA-LOCAL-FIXTURE-ADAPTER-02 compares deterministic local fixture adapter candidates only. Selection is not final answer, not adapter authorization, not truth certification, and not a model quality benchmark. The selected candidate still requires Evidence Review Pack routing before it can be reviewed as cognition.",
        "publication_status": "dashboard_indexed",
    },

    {
        "phase_id": "SONYA-LOCAL-FIXTURE-ADAPTER-03",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "methods_lineage_clarity",
        "product_posture": "source_current_experiment_lineage_clarity",
        "primary_artifacts": SONYA_LOCAL_FIXTURE_ADAPTER_03_ARTIFACTS,
        "dashboard_summary": SONYA_LOCAL_FIXTURE_ADAPTER_03_DASHBOARD_SUMMARY,
        "prerequisite_phases": [
            "SONYA-LOCAL-FIXTURE-ADAPTER-01",
            "SONYA-LOCAL-FIXTURE-ADAPTER-02",
            "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
            "SONYA-ADAPTER-SMOKE-00",
            "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
        ],
        "reproduction_command_summary": SONYA_LOCAL_FIXTURE_ADAPTER_03_COMMAND,
        "claim_allowed": "SONYA-LOCAL-FIXTURE-ADAPTER-03 demonstrates explicit lineage clarity for Sonya local fixture adapter multi-route artifacts by distinguishing current route identity, source fixture identity, source fixture role, and Evidence Review Pack local-adapter route references.",
        "claims_blocked": SONYA_LOCAL_FIXTURE_ADAPTER_03_CLAIMS_BLOCKED,
        "reviewer_caution": "SONYA-LOCAL-FIXTURE-ADAPTER-03 is a lineage clarity packet only. It clarifies that nested source fixture references are dependencies and not stale identity leakage. It does not execute adapters, authorize network, call providers, write memory, release final answers, train models, or deploy.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "UNIVERSAL-STAGE-PIPELINE-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "architecture_scaffold",
        "product_posture": "universal_cognition_stage_contracts",
        "primary_artifacts": UNIVERSAL_STAGE_PIPELINE_ARTIFACTS,
        "reproduction_command_summary": UNIVERSAL_STAGE_PIPELINE_COMMAND,
        "claim_allowed": "UNIVERSAL-STAGE-PIPELINE-00 defines reusable cognition-stage contracts for a universal architecture scaffold.",
        "claims_blocked": UNIVERSAL_ARCHITECTURE_CLAIMS_BLOCKED,
        "reviewer_caution": "Cognition-stage contracts are not product release, not experiment result, not benchmark result, and not deployment authority.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "ARTIFACT-CONTRACT-REGISTRY-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "architecture_scaffold",
        "product_posture": "externalized_artifact_contracts",
        "primary_artifacts": ARTIFACT_CONTRACT_REGISTRY_ARTIFACTS,
        "reproduction_command_summary": ARTIFACT_CONTRACT_REGISTRY_COMMAND,
        "claim_allowed": "ARTIFACT-CONTRACT-REGISTRY-01 externalizes artifact roles and profile contracts into versioned configuration.",
        "claims_blocked": UNIVERSAL_ARCHITECTURE_CLAIMS_BLOCKED,
        "reviewer_caution": "Artifact profile contracts show that profiles are configuration; they are not truth certification or deployment authority.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "UNIVERSAL-COMPATIBILITY-MATRIX-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "architecture_scaffold",
        "product_posture": "universal_stage_input_compatibility",
        "primary_artifacts": UNIVERSAL_COMPATIBILITY_MATRIX_ARTIFACTS,
        "dashboard_summary": UNIVERSAL_COMPATIBILITY_MATRIX_DASHBOARD_SUMMARY,
        "reproduction_command_summary": UNIVERSAL_COMPATIBILITY_MATRIX_COMMAND,
        "claim_allowed": "The universal architecture scaffold demonstrates that accepted experiments can be described as configurations over reusable stages and versioned artifact contracts, with unsupported inputs preserved by hash-only or failed-closed receipts.",
        "claims_blocked": UNIVERSAL_ARCHITECTURE_CLAIMS_BLOCKED,
        "reviewer_caution": "The compatibility matrix is architecture scaffold evidence only: not product release, not experiment result, not benchmark result, not hallucination reduction proof, and not recursive self-improvement.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "EXP-SUITE-REGISTRY-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "experiment_suite_registry",
        "primary_artifacts": ["experiments/experiment_suite_registry.json"],
        "reproduction_command_summary": "Inspect experiments/experiment_suite_registry.json and rebuild the suite repro pack.",
        "claim_allowed": "Accepted/partial/blocked/planned phase registry is reviewable.",
        "claims_blocked": ["registry is not deployment authority", "route is not authorization"],
        "reviewer_caution": "Registry status is a claim-boundary map, not a product launch.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "EXP-SUITE-REPRO-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "reproducibility_pack",
        "primary_artifacts": [
            "experiment_suite_repro_pack.json",
            "acceptance_matrix.csv",
            "artifact_manifest.json",
            "experiment_suite_reproducibility_report.md",
        ],
        "reproduction_command_summary": "python -m coherence.tools.build_experiment_suite_repro_pack --registry experiments/experiment_suite_registry.json --artifacts-root artifacts --out-dir artifacts/experiment_suite_repro_pack --zip",
        "claim_allowed": "Reproducibility receipts and artifact manifests can be inspected.",
        "claims_blocked": ["reproducibility pack is not deployment authority", "receipt is not truth certification"],
        "reviewer_caution": "A receipt records checks; it does not certify truth.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "WAVE-FAMILY-CLOSEOUT-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "gold_physics_calibration",
        "primary_artifacts": ["waveform_gold_physics_family_acceptance_packet.json"],
        "reproduction_command_summary": WAVE_FAMILY_COMMAND,
        "claim_allowed": "Closed-form waveform metric calibration across WAVE-00R through WAVE-03R.",
        "claims_blocked": ["WAVE calibration is not universal ontology", "WAVE Gold-Physics is not psychoacoustic proof"],
        "reviewer_caution": "High coherence is not necessarily constructive or safe.",
        "publication_status": "PUB-WAVE-ROSETTA-01 drafted",
    },
    {
        "phase_id": "SONYA-INGRESS-HARDEN-03",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "sonya_membrane_acceptance",
        "primary_artifacts": [
            "sonya_aegis_smoke_02_acceptance_report.json",
            "human_review bundle",
            "auto route bundle",
        ],
        "reproduction_command_summary": SONYA_AEGIS_COMMAND,
        "claim_allowed": "Direct-call blocking and local Sonya membrane evidence are inspectable.",
        "claims_blocked": ["Sonya local membrane is not federation", "candidate is not answer"],
        "reviewer_caution": "Local fixture only; no recursive Sonya federation is implied.",
        "publication_status": "PUB-GOV-ARTIFACT-COG-01 drafted",
    },
    {
        "phase_id": "SOPHIA-UCC-ROUTE-01",
        "repo": "pdxvoiceteacher/Sophia",
        "status": "accepted",
        "evidence_type": "route_control",
        "primary_artifacts": ["sophia_ucc_route_acceptance_packet.json"],
        "reproduction_command_summary": SOPHIA_UCC_COMMAND,
        "claim_allowed": "Sophia/UCC route controls can classify admissibility posture.",
        "claims_blocked": ["route is not authorization", "no live Sophia calls"],
        "reviewer_caution": "Route disposition is governance posture, not final authority.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "PUB-GOV-ARTIFACT-COG-01",
        "repo": REPO,
        "status": "accepted",
        "evidence_type": "publication_draft",
        "primary_artifacts": [
            "papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md",
            "papers/governed_artifact_cognition/reviewer_quickstart.md",
            "papers/governed_artifact_cognition/status.json",
        ],
        "reproduction_command_summary": "python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json",
        "claim_allowed": "Governed artifact cognition paper is available as an internal preprint draft.",
        "claims_blocked": ["not truth certification", "not deployment authority", "not final answer release"],
        "reviewer_caution": "Draft requires external peer review.",
        "publication_status": "drafted",
    },
    {
        "phase_id": "PUB-WAVE-ROSETTA-01",
        "repo": REPO,
        "status": "accepted",
        "evidence_type": "publication_draft",
        "primary_artifacts": [
            "papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md",
            "papers/waveform_rosetta/reviewer_quickstart.md",
            "papers/waveform_rosetta/status.json",
        ],
        "reproduction_command_summary": "python tools/validate_publication_claims.py --paper papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md --quickstart papers/waveform_rosetta/reviewer_quickstart.md --status papers/waveform_rosetta/status.json",
        "claim_allowed": "Waveform Rosetta methods paper is available as an internal preprint draft.",
        "claims_blocked": ["not universal ontology", "not psychoacoustic effect", "not truth certification"],
        "reviewer_caution": "Closed-form calibration is not deployment evidence.",
        "publication_status": "drafted",
    },
    {
        "phase_id": "UNI-02D-SONYA-GATE-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "safe_portability_fixture",
        "primary_artifacts": [
            "uni02d_sonya_gate_acceptance_report.json",
            "semantic_term_quarantine_packet.json",
            "runtime_profile_leakage_packet.json",
            "uni02d_prior_origin_provenance_packet.json",
            "uni02d_prior_quarantine_packet.json",
        ],
        "reproduction_command_summary": UNI02D_COMMAND,
        "claim_allowed": "A Sonya-gated safe portability fixture can be inspected.",
        "claims_blocked": ["UNI-02D safe portability fixture is not universal portability proof", "prior quarantine is not prior canonization"],
        "reviewer_caution": "Scan selected_priors and matches[*].prior shapes for quarantine/provenance posture.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "RETRO-LANE-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "retrosynthesis_admission_lanes",
        "primary_artifacts": [
            "retrosynthesis_admission_packet.json",
            "retrosynthesis_admission_review_packet.json",
            "retro_lane_00_acceptance_receipt.json",
        ],
        "reproduction_command_summary": RETRO_LANE_COMMAND,
        "claim_allowed": "sandbox_auto, review_required, and blocked admission lanes can be reviewed.",
        "claims_blocked": ["Retrosynthesis admission is not retrosynthesis execution", "hallucination telemetry is not evidence"],
        "reviewer_caution": "Admission is not execution; hallucination is telemetry, not evidence.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "PUBLIC-UTILITY-ALPHA-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "local_public_utility_reviewer_demo",
        "primary_artifacts": PUBLIC_UTILITY_ALPHA_ARTIFACTS,
        "reproduction_command_summary": PUBLIC_UTILITY_ALPHA_COMMAND,
        "claim_allowed": "A local fixture-only reviewer demo can assemble the accepted governed artifact cognition chain and make its evidence, route timeline, candidate packet path, bypass block, model-braid observation, catalog boundary, inventory, and parity artifacts inspectable.",
        "claims_blocked": PUBLIC_UTILITY_ALPHA_CLAIMS_BLOCKED,
        "reviewer_caution": "This is a local reviewer harness. It demonstrates bounded artifact assembly and claim-boundary visibility. It is not a product launch, not deployment readiness, and not proof of real-world performance.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "EVIDENCE-REVIEW-PACK-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "fixture_only_evidence_review_receipt",
        "product_posture": "first_product_facing_review_receipt",
        "primary_artifacts": EVIDENCE_REVIEW_PACK_ARTIFACTS,
        "prerequisite_phases": [
            "UNIVERSAL-EVIDENCE-INGRESS-00",
            "UCC-CONTROL-PROFILE-SELECTOR-00",
            "CANONICAL-METRIC-PACKET-01",
        ],
        "reproduction_command_summary": EVIDENCE_REVIEW_PACK_COMMAND,
        "claim_allowed": "EVIDENCE-REVIEW-PACK-00 demonstrates a fixture-only, source-bounded, UCC-control-profile-governed review receipt that makes supported claims, unsupported claims, missing uncertainty, preserved counterevidence, semantic drift signals, UCC threshold posture, reserved-authority blocks, and reviewer next actions inspectable. Evidence Review Pack v0.1 is AI review that shows its work.",
        "claims_blocked": EVIDENCE_REVIEW_PACK_CLAIMS_BLOCKED,
        "reviewer_caution": "Evidence Review Pack v0.1 is a fixture-only review receipt. It can show which claims are source-supported or unsupported in a controlled fixture and can expose missing uncertainty and counterevidence. It does not certify truth, does not provide professional advice, does not prove hallucination reduction, and does not authorize deployment.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "RW-COMP-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "fixture_only_raw_vs_governed_review_comparison",
        "product_posture": "comparison_scaffold_for_evidence_review_pack",
        "primary_artifacts": RW_COMP_01_ARTIFACTS,
        "prerequisite_phases": [
            "UNIVERSAL-EVIDENCE-INGRESS-00",
            "UCC-CONTROL-PROFILE-SELECTOR-00",
            "EVIDENCE-REVIEW-PACK-00",
            "CANONICAL-METRIC-PACKET-01",
            "RAW-BASELINE-COMPARISON-00",
        ],
        "fixture_summary": RW_COMP_01_FIXTURE_SUMMARY,
        "reproduction_command_summary": RW_COMP_01_COMMAND,
        "claim_allowed": "RW-COMP-01 demonstrates a fixture-only comparison where full Evidence Review Pack v0.1 exposes supported claims, unsupported claims, source-reference posture, uncertainty omissions, counterevidence preservation, UCC threshold posture, and artifact completeness more explicitly than raw or partially governed fixture baselines. RW-COMP-01 is a fixture-only comparison scaffold, not hallucination reduction proof.",
        "claims_blocked": RW_COMP_01_CLAIMS_BLOCKED,
        "reviewer_caution": "RW-COMP-01 is a deterministic fixture comparison. It can show that the Evidence Review Pack exposes review-relevant structure in one controlled comparison, but it does not prove hallucination reduction, does not prove model superiority, does not prove real-world performance, is not professional-advice quality, and is not production compliance. Future RW-COMP phases must add larger fixture batteries, blinded scoring, held-out examples, external reproduction, and live-model/provider controls before stronger claims are authorized.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "RW-COMP-02",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "deterministic_multi_fixture_raw_vs_governed_review_comparison",
        "product_posture": "multi_fixture_battery_for_evidence_review_pack_visibility",
        "primary_artifacts": RW_COMP_02_ARTIFACTS,
        "prerequisite_phases": [
            "UNIVERSAL-EVIDENCE-INGRESS-00",
            "UCC-CONTROL-PROFILE-SELECTOR-00",
            "EVIDENCE-REVIEW-PACK-00",
            "CANONICAL-METRIC-PACKET-01",
            "RAW-BASELINE-COMPARISON-00",
            "RW-COMP-01",
        ],
        "dashboard_summary": RW_COMP_02_DASHBOARD_SUMMARY,
        "reproduction_command_summary": RW_COMP_02_COMMAND,
        "claim_allowed": "RW-COMP-02 demonstrates a deterministic multi-fixture comparison battery where Evidence Review Pack v0.1 exposes review-relevant structure across multiple fixture families, including unsupported claims, source-reference validity, uncertainty retention, counterevidence preservation, artifact completeness, UCC threshold posture, and review burden indicators. RW-COMP-02 is a deterministic multi-fixture comparison battery and remains not hallucination reduction proof.",
        "claims_blocked": RW_COMP_02_CLAIMS_BLOCKED,
        "reviewer_caution": "RW-COMP-02 is a deterministic multi-fixture battery. It can show that the Evidence Review Pack exposes more review-relevant structure than raw or partially governed fixture baselines across several controlled examples. It does not prove hallucination reduction, does not prove model superiority, does not prove real-world performance, is not professional-advice quality, and is not production compliance. Future phases must add held-out fixtures, blinded scoring, statistical analysis, external reproduction, and controlled live-model/provider conditions before stronger claims are authorized.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "RW-COMP-03",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "heldout_blinded_fixture_scoring_scaffold",
        "product_posture": "pre_registered_fixture_scaffold_for_future_hallucination_reduction_evidence",
        "primary_artifacts": RW_COMP_03_ARTIFACTS,
        "prerequisite_phases": [
            "RW-COMP-02",
            "EVIDENCE-REVIEW-PACK-01",
            "RETROSYNTHESIS-SANDBOX-CYCLE-01",
            "EVIDENCE-REVIEW-PACK-00",
            "UCC-CONTROL-PROFILE-SELECTOR-00",
            "UNIVERSAL-EVIDENCE-INGRESS-00",
            "CANONICAL-METRIC-PACKET-01",
            "RAW-BASELINE-COMPARISON-00",
        ],
        "dashboard_summary": RW_COMP_03_DASHBOARD_SUMMARY,
        "reproduction_command_summary": RW_COMP_03_COMMAND,
        "claim_allowed": "RW-COMP-03 demonstrates a held-out blinded fixture-scoring scaffold with simulated scores, blind labels, pre-registered scoring dimensions, statistics planning, and a second-pass Evidence Review Pack candidate arm.",
        "claims_blocked": RW_COMP_03_CLAIMS_BLOCKED,
        "reviewer_caution": "RW-COMP-03 is a held-out blinded fixture scaffold with simulated scoring only. It introduces a pre-registered scoring and statistics structure for future evaluation, but it does not prove hallucination reduction, does not prove model superiority, does not show live model behavior, does not measure human reviewer performance, is not professional-advice quality, is not compliance certification, and is not production readiness.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "RETROSYNTHESIS-SANDBOX-CYCLE-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "bounded_retrosynthesis_candidate_repair_cycle",
        "product_posture": "sandbox_repair_candidates_for_evidence_review_pack",
        "primary_artifacts": RETRO_SANDBOX_CYCLE_ARTIFACTS,
        "prerequisite_phases": [
            "RETRO-LANE-00",
            "EVIDENCE-REVIEW-PACK-00",
            "RW-COMP-02",
            "UCC-CONTROL-PROFILE-SELECTOR-00",
            "UNIVERSAL-EVIDENCE-INGRESS-00",
            "CANONICAL-METRIC-PACKET-01",
        ],
        "dashboard_summary": RETRO_SANDBOX_CYCLE_DASHBOARD_SUMMARY,
        "reproduction_command_summary": RETRO_SANDBOX_CYCLE_COMMAND,
        "claim_allowed": "RETROSYNTHESIS-SANDBOX-CYCLE-01 demonstrates a bounded candidate-only repair cycle over incomplete Evidence Review Pack artifacts. It emits missing-evidence requests, claim-map revision candidates, uncertainty-restoration candidates, counterevidence-expansion candidates, and next-experiment recommendations while remaining not canon adoption, not memory write, not final answer release, not Publisher finalization, not deployment authority, not Omega detection, not publication claim, not live model execution, and not remote provider call.",
        "claims_blocked": RETRO_SANDBOX_CYCLE_CLAIMS_BLOCKED,
        "reviewer_caution": "RETROSYNTHESIS-SANDBOX-CYCLE-01 emits repair candidates only. Missing evidence requests are not external fetches. Claim-map revisions are not accepted evidence. Uncertainty restoration and counterevidence expansion remain candidate artifacts until future review gates promote them. This phase does not write memory, does not adopt canon, does not publish claims, does not release final answers, does not perform Omega detection, and does not authorize deployment.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "EVIDENCE-REVIEW-PACK-01",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "bounded_second_pass_review_candidate_loop",
        "product_posture": "second_pass_candidate_revisions_from_retrosynthesis_sandbox",
        "primary_artifacts": EVIDENCE_REVIEW_PACK_01_ARTIFACTS,
        "prerequisite_phases": [
            "EVIDENCE-REVIEW-PACK-00",
            "RETROSYNTHESIS-SANDBOX-CYCLE-01",
            "RW-COMP-02",
            "UCC-CONTROL-PROFILE-SELECTOR-00",
            "UNIVERSAL-EVIDENCE-INGRESS-00",
            "CANONICAL-METRIC-PACKET-01",
        ],
        "dashboard_summary": EVIDENCE_REVIEW_PACK_01_DASHBOARD_SUMMARY,
        "reproduction_command_summary": EVIDENCE_REVIEW_PACK_01_COMMAND,
        "claim_allowed": "EVIDENCE-REVIEW-PACK-01 demonstrates a candidate-only second-pass review loop that consumes retrosynthesis sandbox repair candidates and emits bounded revision candidates for claim-map status, omitted uncertainty, counterevidence, and structural visibility deltas.",
        "claims_blocked": EVIDENCE_REVIEW_PACK_01_CLAIMS_BLOCKED,
        "reviewer_caution": "EVIDENCE-REVIEW-PACK-01 emits candidate revisions only. Its deltas are structural visibility descriptors, not hallucination-reduction proof. Claim-map revisions are not accepted evidence. Uncertainty and counterevidence revisions require future review gates before promotion. This phase does not write memory, does not adopt canon, does not publish claims, does not release final answers, does not perform Omega detection, does not finalize Publisher output, and does not authorize deployment.",
        "publication_status": "dashboard_indexed",
    },
    {
        "phase_id": "RAW-BASELINE-COMPARISON-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "fixture_only_measurement_scaffold",
        "primary_artifacts": RAW_BASELINE_COMPARISON_ARTIFACTS,
        "reproduction_command_summary": RAW_BASELINE_COMPARISON_COMMAND,
        "claim_allowed": "RAW-BASELINE-COMPARISON-00 provides a fixture-only measurement scaffold for comparing raw-text-style baseline arms with the Sonya-governed candidate packet path across unsupported-claim count, source-linkage posture, route receipt posture, forbidden-artifact leakage, and raw-output admission.",
        "claims_blocked": RAW_BASELINE_COMPARISON_CLAIMS_BLOCKED,
        "reviewer_caution": "This phase is measurement infrastructure only. It does not prove that governed artifact cognition reduces hallucinations, improves model quality, or performs better on real-world tasks. It establishes a scaffold for future controlled comparisons.",
        "publication_status": "dashboard_indexed",
    },
]
PARTIAL_PHASES = [
    {"phase_id": "TIMBRE-SPECTRAL-METRIC-TIER-02", "status": "planned_partial", "reason": "spectral-complexity tier remains future work"},
]
BLOCKED_PHASES = [
    {"phase_id": "DEPLOYMENT-CLAIM", "status": "blocked", "reason": "dashboard is not deployment authority"},
]
PLANNED_PHASES = [
    "PSYCHOACOUSTIC-SAFETY-TIER-03",
    "MODEL-INTERPRETATION-ORACLE-TIER-03",
    "Raw-model comparison baselines",
]
BOUNDARIES = [
    "Sonya Adapter Contract Registry: Adapter capability is not adapter authorization.",
    "Sonya Adapter Contract Registry keeps all adapters disabled or blocked; all adapters disabled or blocked means not adapter execution and not network authorization.",
    "Sonya Adapter Contract Registry boundaries: not adapter execution, not network authorization, not remote provider call, not model weight training.",
    "Sonya Adapter Contract Registry requires that raw output is forbidden, candidate packet required, and failure receipts required.",
    "Universal Architecture Scaffold: The brain runs cognition stages; experiments configure those stages.",
    "Universal architecture scaffold: profiles are configuration; experiments are configurations over reusable stages and versioned artifact contracts.",
    "Universal compatibility inputs use fail-closed receipts or hash-only receipts when unsupported inputs cannot be semantically interpreted.",
    "Universal Architecture Scaffold is not product release, not experiment result, not benchmark result, not hallucination reduction proof, not deployment authority, and not recursive self-improvement.",
    "Route is not authorization.",
    "Receipt is not truth certification.",
    "Model candidate is not answer.",
    "Publisher candidate is not final answer.",
    "Memory intent is not memory write.",
    "Sonya local membrane is not federation.",
    "WAVE calibration is not universal ontology.",
    "UNI-02D safe portability fixture is not universal portability proof.",
    "Retrosynthesis admission is not retrosynthesis execution.",
    "Admission is not execution.",
    "Reproducibility pack is not deployment authority.",
    "Dashboard is not deployment authority.",
    "Public Utility Alpha is a local reviewer demo, not deployment authority.",
    "Raw Baseline Comparison is not hallucination reduction proof.",
    "Raw Baseline Comparison is not model quality benchmark.",
    "Evidence Review Pack v0.1 is AI review that shows its work.",
    "Evidence Review Pack is not truth certification.",
    "Evidence Review Pack is not legal advice.",
    "Evidence Review Pack is not medical advice.",
    "Evidence Review Pack is not tax advice.",
    "Evidence Review Pack is not compliance certification.",
    "Evidence Review Pack is not hallucination reduction proof.",
    "Evidence Review Pack is not live model execution.",
    "Evidence Review Pack is not production evaluation.",
    "RW-COMP-01 is a fixture-only comparison scaffold, not hallucination reduction proof.",
    "RW-COMP-01 is not model superiority proof.",
    "RW-COMP-01 is not model quality benchmark.",
    "RW-COMP-01 is not live model evaluation.",
    "RW-COMP-01 is not remote provider evaluation.",
    "RW-COMP-01 is not professional advice.",
    "RW-COMP-01 is not compliance certification.",
    "RW-COMP-01 is not production evaluation.",
    "RW-COMP-02 is a deterministic multi-fixture comparison battery and remains not hallucination reduction proof.",
    "RW-COMP-02 is not model superiority proof.",
    "RW-COMP-02 is not model quality benchmark.",
    "RW-COMP-02 is not live model evaluation.",
    "RW-COMP-02 is not remote provider evaluation.",
    "RW-COMP-02 is not professional advice.",
    "RW-COMP-02 is not compliance certification.",
    "RW-COMP-02 is not production evaluation.",
    "Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption.",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01 is not memory write.",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01 is not final answer release.",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01 is not Publisher finalization.",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01 is not Omega detection.",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01 is not deployment authority.",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01 is not recursive self-improvement.",
    "Evidence Review Pack second pass is candidate revision, not accepted evidence.",
    "EVIDENCE-REVIEW-PACK-01 is not canon adoption.",
    "EVIDENCE-REVIEW-PACK-01 is not memory write.",
    "EVIDENCE-REVIEW-PACK-01 is not final answer release.",
    "EVIDENCE-REVIEW-PACK-01 is not Publisher finalization.",
    "EVIDENCE-REVIEW-PACK-01 is not Omega detection.",
    "EVIDENCE-REVIEW-PACK-01 is not deployment authority.",
    "EVIDENCE-REVIEW-PACK-01 is not hallucination reduction proof.",
    "EVIDENCE-REVIEW-PACK-01 is not recursive self-improvement.",
    "RW-COMP-03 is a held-out blinded fixture scaffold, not hallucination reduction proof.",
    "RW-COMP-03 is not model superiority proof.",
    "RW-COMP-03 is not live model evaluation.",
    "RW-COMP-03 is not live human study.",
    "RW-COMP-03 uses simulated scores.",
    "RW-COMP-03 is not accepted evidence.",
    "RW-COMP-03 is not production evaluation.",
    "Sonya Adapter Smoke exercises contracts, not live adapters.",
    "Sonya Adapter Smoke is not live adapter execution.",
    "Sonya Adapter Smoke is not network authorization.",
    "Sonya Adapter Smoke is not remote provider call.",
    "Sonya Adapter Smoke is not model weight training.",
    "Sonya Adapter Smoke keeps raw output rejected or absent.",
    "Sonya Adapter Smoke requires a candidate packet for fixture model output.",
    "Sonya Adapter Smoke makes failure receipts visible.",
    "Sonya Adapter Smoke makes telemetry events visible.",
    "Sonya Adapter Smoke makes provenance events visible.",
    "Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters.",
    "Sonya Local Fixture Adapter records that local fixture adapter execution occurred under Sonya adapter contracts.",
    "Sonya Local Fixture Adapter is not live adapter execution.",
    "Sonya Local Fixture Adapter is not network authorization.",
    "Sonya Local Fixture Adapter is not remote provider call.",
    "Sonya Local Fixture Adapter is not live model execution.",
    "Sonya Local Fixture Adapter is not memory write.",
    "Sonya Local Fixture Adapter is not final answer release.",
    "Sonya Local Fixture Adapter is not deployment authority.",
    "Sonya Local Fixture Adapter is not model weight training.",
    "Sonya Local Fixture Adapter emits candidate packets, failure receipts, telemetry events, and provenance events.",
    "Adapter output is not accepted as cognition directly.",
    "Local adapter candidates become reviewable only through the Evidence Review Pack path.",
    "Evidence Review Pack local-adapter route is not accepted evidence.",
    "Evidence Review Pack local-adapter route is not adapter authorization.",
    "Evidence Review Pack local-adapter route is not memory write.",
    "Evidence Review Pack local-adapter route is not final answer release.",
    "Evidence Review Pack local-adapter route is not deployment authority.",
    "Evidence Review Pack local-adapter route is not model weight training.",
    "Evidence Review Pack local-adapter route is not hallucination reduction proof.",
    "Evidence Review Pack local-adapter route is not recursive self-improvement.",
    "Candidate packets require UCC-controlled review.",
    "The claim map is not truth certification.",
    "The candidate is not final answer.",
    "Selection policy is not final answer.",
    "Multi-adapter local fixture selection still requires Evidence Review Pack review.",
    "Sonya Local Fixture Adapter multi-route is not adapter authorization.",
    "Sonya Local Fixture Adapter multi-route is not a model quality benchmark.",
    "Sonya Local Fixture Adapter multi-route is not model superiority proof.",
    "Sonya Local Fixture Adapter multi-route is not memory write.",
    "Sonya Local Fixture Adapter multi-route is not final answer release.",
    "Sonya Local Fixture Adapter multi-route is not deployment authority.",
    "Sonya Local Fixture Adapter multi-route is not model weight training.",
    "Sonya Local Fixture Adapter multi-route is not hallucination reduction proof.",
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
]
GLOBAL_NON_CLAIMS = [
    "not truth certification",
    "not deployment authority",
    "not final answer release",
    "not canon adoption",
    "not memory write",
    "not Publisher finalization",
    "not Omega detection",
    "not recursive self-improvement",
    "not live human study",
    "not accepted evidence",
    "local fixture only",
    "requires external peer review",
    "not AI consciousness",
    "not universal ontology",
    "not recursive Sonya federation",
    "not live Atlas memory writes",
    "not live Sophia calls",
    "not retrosynthesis runtime",
    "not Omega detection",
    "not Publisher finalization",
    "not live model execution",
    "not live adapter execution",
    "not remote provider call",
    "not live model evaluation",
    "not remote provider evaluation",
    "not professional advice",
    "not legal advice",
    "not medical advice",
    "not tax advice",
    "not compliance certification",
    "not production evaluation",
    "not federation",
    "not recursive braid",
]


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _assert_safe_dashboard(dashboard: dict[str, Any]) -> None:
    for key in ("deployment_ready", "truth_certified", "final_answer_release"):
        if dashboard.get(key) is True:
            raise ValueError(f"{key} must not be true")
    if any(not phase.get("claims_blocked") for phase in ACCEPTED_PHASES):
        raise ValueError("accepted phases must include claim boundaries")


def dashboard_payload() -> dict[str, Any]:
    dashboard = {
        "schema": "uvlm.public_experiment_suite_dashboard.v1",
        "repo": REPO,
        "source_repos": SOURCE_REPOS,
        "dashboard_status": "draft_public_review",
        "generated_at": GENERATED_AT,
        "accepted_phase_count": len(ACCEPTED_PHASES),
        "partial_phase_count": len(PARTIAL_PHASES),
        "blocked_phase_count": len(BLOCKED_PHASES),
        "planned_phase_count": len(PLANNED_PHASES),
        "accepted_phases": ACCEPTED_PHASES,
        "partial_phases": PARTIAL_PHASES,
        "blocked_phases": BLOCKED_PHASES,
        "planned_phases": PLANNED_PHASES,
        "evidence_packages": [
            "experiment_suite_repro_pack.json",
            "waveform_gold_physics_family_acceptance_packet.json",
            "sonya_aegis_smoke_02_acceptance_report.json",
            "public_utility_alpha_status.json",
            "raw_baseline_comparison_packet.json",
            "evidence_review_pack_manifest.json",
            "rw_comp_01_packet.json",
            "rw_comp_02_packet.json",
            "retrosynthesis_sandbox_cycle_packet.json",
            "evidence_review_second_pass_packet.json",
            "rw_comp_03_packet.json",
            "universal_pipeline_manifest.json",
            "artifact_contract_registry_review.json",
            "universal_compatibility_matrix_packet.json",
            "sonya_adapter_contract_registry_packet.json",
            "sonya_local_fixture_adapter_packet.json",
            "evidence_review_local_adapter_route_packet.json",
            "sonya_local_adapter_multi_route_packet.json",
            "sonya_local_adapter_lineage_packet.json",
        ],
        "publication_drafts": [
            "papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md",
            "papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md",
        ],
        "global_non_claims": GLOBAL_NON_CLAIMS,
        "reviewer_quickstart_paths": [
            "docs/experiment-suite/reviewer-quickstart.md",
            "papers/governed_artifact_cognition/reviewer_quickstart.md",
            "papers/waveform_rosetta/reviewer_quickstart.md",
        ],
        "requires_external_peer_review": True,
        "not_truth_certification": True,
        "not_deployment_authority": True,
        "not_final_answer_release": True,
        "not_ai_consciousness_claim": True,
        "not_universal_ontology_claim": True,
    }
    _assert_safe_dashboard(dashboard)
    return dashboard


def accepted_phase_matrix() -> dict[str, Any]:
    return {"schema": "uvlm.accepted_phase_matrix.v1", "entries": ACCEPTED_PHASES}


def reproducibility_index() -> dict[str, Any]:
    return {
        "schema": "uvlm.reproducibility_index.v1",
        "commands": {
            "CoherenceLattice": [
                {"name": "SONYA-AEGIS-SMOKE-02 harness", "command": SONYA_AEGIS_COMMAND},
                {"name": "WAVE family acceptance", "command": WAVE_FAMILY_COMMAND},
                {"name": "UNI-02D Sonya gate acceptance", "command": UNI02D_COMMAND},
                {"name": "RETRO-LANE-00 acceptance", "command": RETRO_LANE_COMMAND},
                {"name": "Public Utility Alpha acceptance", "command": PUBLIC_UTILITY_ALPHA_COMMAND},
                {"name": "Raw Baseline Comparison acceptance", "command": RAW_BASELINE_COMPARISON_COMMAND},
                {"name": "Evidence Review Pack acceptance", "command": EVIDENCE_REVIEW_PACK_COMMAND},
                {"name": "RW-COMP-01 acceptance", "command": RW_COMP_01_COMMAND},
                {"name": "RW-COMP-02 acceptance", "command": RW_COMP_02_COMMAND},
                {"name": "Retrosynthesis Sandbox Cycle acceptance", "command": RETRO_SANDBOX_CYCLE_COMMAND},
                {"name": "Evidence Review Pack second pass acceptance", "command": EVIDENCE_REVIEW_PACK_01_COMMAND},
                {"name": "RW-COMP-03 acceptance", "command": RW_COMP_03_COMMAND},
                {"name": "Universal Stage Pipeline acceptance", "command": UNIVERSAL_STAGE_PIPELINE_COMMAND},
                {"name": "Artifact Contract Registry acceptance", "command": ARTIFACT_CONTRACT_REGISTRY_COMMAND},
                {"name": "Universal Compatibility Matrix acceptance", "command": UNIVERSAL_COMPATIBILITY_MATRIX_COMMAND},
                {"name": "Sonya Adapter Contract Registry acceptance", "command": SONYA_ADAPTER_CONTRACT_REGISTRY_COMMAND},
                {"name": "Sonya Adapter Smoke acceptance", "command": SONYA_ADAPTER_SMOKE_COMMAND},
                {"name": "Sonya Local Fixture Adapter acceptance", "command": SONYA_LOCAL_FIXTURE_ADAPTER_COMMAND},
                {"name": "Evidence Review Pack local adapter acceptance", "command": EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_COMMAND},
                {"name": "Sonya Local Fixture Adapter multi-route acceptance", "command": SONYA_LOCAL_FIXTURE_ADAPTER_02_COMMAND},
                {"name": "Sonya Local Fixture Adapter lineage clarity acceptance", "command": SONYA_LOCAL_FIXTURE_ADAPTER_03_COMMAND},
                {"name": "experiment suite repro pack builder", "command": "python -m coherence.tools.build_experiment_suite_repro_pack --registry experiments/experiment_suite_registry.json --artifacts-root artifacts --out-dir artifacts/experiment_suite_repro_pack --zip"},
            ],
            "Sophia": [
                {"name": "UCC route test command", "command": SOPHIA_UCC_COMMAND},
            ],
            "uvlm-publications": [
                {"name": "governed artifact cognition validator", "command": "python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json"},
                {"name": "waveform Rosetta validator", "command": "python tools/validate_publication_claims.py --paper papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md --quickstart papers/waveform_rosetta/reviewer_quickstart.md --status papers/waveform_rosetta/status.json"},
                {"name": "dashboard validator", "command": "python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite"},
            ],
        },
        "not_deployment_authority": True,
    }


def claim_boundary_index() -> dict[str, Any]:
    return {"schema": "uvlm.claim_boundary_index.v1", "boundaries": BOUNDARIES}


def artifact_index() -> dict[str, Any]:
    return {
        "schema": "uvlm.artifact_index.v1",
        "phases": {
            "SONYA-AEGIS-SMOKE-02": ["sonya_aegis_smoke_02_acceptance_report.json", "human_review bundle", "auto route bundle"],
            "WAVE": ["waveform_gold_physics_family_acceptance_packet.json"],
            "UNI-02D": ["uni02d_sonya_gate_acceptance_report.json", "semantic_term_quarantine_packet.json", "runtime_profile_leakage_packet.json", "uni02d_prior_origin_provenance_packet.json", "uni02d_prior_quarantine_packet.json"],
            "RETRO-LANE-00": ["retrosynthesis_admission_packet.json", "retrosynthesis_admission_review_packet.json", "retro_lane_00_acceptance_receipt.json"],
            "PUBLIC-UTILITY-ALPHA-00": PUBLIC_UTILITY_ALPHA_ARTIFACTS,
            "RAW-BASELINE-COMPARISON-00": RAW_BASELINE_COMPARISON_ARTIFACTS,
            "EVIDENCE-REVIEW-PACK-00": EVIDENCE_REVIEW_PACK_ARTIFACTS,
            "RW-COMP-01": RW_COMP_01_ARTIFACTS,
            "RW-COMP-02": RW_COMP_02_ARTIFACTS,
            "RETROSYNTHESIS-SANDBOX-CYCLE-01": RETRO_SANDBOX_CYCLE_ARTIFACTS,
            "EVIDENCE-REVIEW-PACK-01": EVIDENCE_REVIEW_PACK_01_ARTIFACTS,
            "RW-COMP-03": RW_COMP_03_ARTIFACTS,
            "UNIVERSAL-STAGE-PIPELINE-00": UNIVERSAL_STAGE_PIPELINE_ARTIFACTS,
            "ARTIFACT-CONTRACT-REGISTRY-01": ARTIFACT_CONTRACT_REGISTRY_ARTIFACTS,
            "UNIVERSAL-COMPATIBILITY-MATRIX-00": UNIVERSAL_COMPATIBILITY_MATRIX_ARTIFACTS,
            "SONYA-ADAPTER-CONTRACT-REGISTRY-01": SONYA_ADAPTER_CONTRACT_REGISTRY_ARTIFACTS,
            "SONYA-ADAPTER-SMOKE-00": SONYA_ADAPTER_SMOKE_ARTIFACTS,
            "SONYA-LOCAL-FIXTURE-ADAPTER-01": SONYA_LOCAL_FIXTURE_ADAPTER_ARTIFACTS,
            "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01": EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_ARTIFACTS,
            "SONYA-LOCAL-FIXTURE-ADAPTER-02": SONYA_LOCAL_FIXTURE_ADAPTER_02_ARTIFACTS,
            "SONYA-LOCAL-FIXTURE-ADAPTER-03": SONYA_LOCAL_FIXTURE_ADAPTER_03_ARTIFACTS,
            "publications": ["PUB_GOV_ARTIFACT_COG_01.md", "PUB_WAVE_ROSETTA_01.md", "reviewer quickstarts", "status.json files"],
        },
    }


def status_payload() -> dict[str, Any]:
    return {
        "dashboard_id": "PUBLIC-REPRO-DASHBOARD-01",
        "repo": REPO,
        "status": "draft_public_review",
        "claim_level": "public_reviewer_orientation",
        "accepted_phase_count": len(ACCEPTED_PHASES),
        "latest_product_facing_receipt": "EVIDENCE-REVIEW-PACK-00",
        "latest_fixture_comparison": "RW-COMP-02",
        "latest_bounded_candidate_repair_cycle": "RETROSYNTHESIS-SANDBOX-CYCLE-01",
        "latest_second_pass_review_candidate": "EVIDENCE-REVIEW-PACK-01",
        "latest_heldout_blinded_fixture_scaffold": "RW-COMP-03",
        "latest_universal_architecture_scaffold": "UNIVERSAL-COMPATIBILITY-MATRIX-00",
        "latest_sonya_adapter_contract_registry": "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
        "latest_sonya_local_fixture_adapter": "SONYA-LOCAL-FIXTURE-ADAPTER-01",
        "latest_evidence_review_pack_local_adapter": "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
        "latest_sonya_local_fixture_adapter_multi_route": "SONYA-LOCAL-FIXTURE-ADAPTER-02",
        "latest_sonya_local_fixture_adapter_lineage_clarity": "SONYA-LOCAL-FIXTURE-ADAPTER-03",
        "sonya_local_fixture_adapter_03_indexed": True,
        "not_stale_identity_leakage": True,
        "not_lineage_authority": True,
        "requires_external_peer_review": True,
        "not_truth_certification": True,
        "not_deployment_authority": True,
        "not_final_answer_release": True,
        "not_ai_consciousness_claim": True,
        "not_universal_ontology_claim": True,
    }


def docs() -> dict[str, str]:
    phase_rows = "\n".join(
        f"| {p['phase_id']} | {p['repo']} | {p['status']} | {p['claim_allowed']} | {p['reviewer_caution']} |"
        for p in ACCEPTED_PHASES
    )
    boundaries = "\n".join(f"- {b}" for b in BOUNDARIES)
    return {
        "README.md": "# Experiment Suite Docs\n\nPublic reviewer documentation for the claim-bounded reproducibility dashboard.\n",
        "assets/README.md": "# Assets\n\nOptional static assets for the public reproducibility dashboard.\n",
        "index.md": f"# Public Experiment Suite Dashboard\n\nThis dashboard presents accepted evidence for reviewer orientation. It is not truth certification, not deployment authority, not final answer release, local fixture only, and requires external peer review.\n\n## Accepted evidence\n\n| Phase | Repo | Status | What this supports | Reviewer caution |\n| --- | --- | --- | --- | --- |\n{phase_rows}\n\n## Reviewer path\n\nStart with claim boundaries, then read the governed artifact cognition paper, WAVE Rosetta paper, SONYA-AEGIS-SMOKE-02, WAVE family, UNI-02D Sonya gate, and RETRO-LANE-00, Public Utility Alpha, Raw Baseline Comparison, Evidence Review Pack, RW-COMP-01, RW-COMP-02, Retrosynthesis Sandbox Cycle, Evidence Review Pack second-pass, RW-COMP-03, Universal Architecture Scaffold, Sonya Adapter Contract Registry, Sonya Adapter Smoke, Sonya Local Fixture Adapter, and Evidence Review Pack local adapter, Sonya Local Fixture Adapter multi-route, and Sonya Local Fixture Adapter lineage clarity pages.\n\n## What this proves\n\nIt proves only that accepted local fixture artifacts and draft publication materials are organized for review.\n\n## What this does not prove\n\nNo oracle posture, no deployment posture, no final-answer posture, no AI consciousness claim, and no universal ontology claim.\n\n## Phase pages\n\n- [SONYA-AEGIS-SMOKE-02](sonya-aegis-smoke-02.md)\n- [WAVE Gold-Physics](wave-gold-physics.md)\n- [UNI-02D Sonya gate](uni02d-sonya-gate.md)\n- [RETRO-LANE-00](retro-lane-00.md)\n- [Public Utility Alpha](public-utility-alpha.md)\n- [Raw Baseline Comparison](raw-baseline-comparison.md)\n- [Evidence Review Pack](evidence-review-pack.md)\n- [RW-COMP-01](rw-comp-01.md)\n- [RW-COMP-02](rw-comp-02.md)\n- [Retrosynthesis Sandbox Cycle](retrosynthesis-sandbox-cycle.md)\n- [Evidence Review Pack second pass](evidence-review-pack-second-pass.md)\n- [RW-COMP-03](rw-comp-03.md)\n- [Universal Architecture Scaffold](universal-architecture.md)\n- [Sonya Adapter Contract Registry](sonya-adapter-contract-registry.md)\n- [Sonya Adapter Smoke](sonya-adapter-smoke.md)\n- [Sonya Local Fixture Adapter](sonya-local-fixture-adapter.md)\n- [Evidence Review Pack local adapter](evidence-review-pack-local-adapter.md)\n- [Sonya Local Fixture Adapter multi-route](sonya-local-fixture-adapter-multi-route.md)\n- [Sonya Local Fixture Adapter lineage clarity](sonya-local-fixture-adapter-lineage.md)\n- [Governed artifact cognition paper](governed-artifact-cognition-paper.md)\n- [Waveform Rosetta paper](waveform-rosetta-paper.md)\n",
        "claim-boundaries.md": f"# Claim Boundaries\n\n{boundaries}\n\nNo oracle posture. No deployment posture. No final-answer posture. No AI consciousness claim. No universal ontology claim.\n",
        "sonya-aegis-smoke-02.md": f"""# SONYA-AEGIS-SMOKE-02

Purpose: inspect a local Sonya membrane and direct-call blocking fixture.

Run command:

```powershell
{SONYA_AEGIS_COMMAND}
```

Evidence: `sonya_aegis_smoke_02_acceptance_report.json`, human_review bundle, auto route bundle.

Claim allowed: local deterministic membrane evidence and direct-call blocking are reviewable.

Claims blocked: Sonya local membrane is not federation; candidate is not answer; local fixture only.

Inspect direct-call blocking and Sonya membrane evidence in the acceptance report and route bundles.
""",
        "wave-gold-physics.md": f"""# WAVE Gold-Physics

Purpose: closed-form waveform metric calibration.

Run command:

```powershell
{WAVE_FAMILY_COMMAND}
```

Evidence: `waveform_gold_physics_family_acceptance_packet.json`.

Theorem summary: constructive interference, coherent cancellation, detuning spiral, incomplete cancellation, and observability degradation.

Claim allowed: WAVE calibration distinguishes waveform metric behavior.

Claims blocked: WAVE calibration is not universal ontology and WAVE Gold-Physics is not psychoacoustic proof.

Caution: high coherence is not necessarily constructive or safe.
""",
        "uni02d-sonya-gate.md": f"""# UNI-02D Sonya Gate

Purpose: inspect safe portability fixture routing through Sonya-gated constraints.

Run command:

```powershell
{UNI02D_COMMAND}
```

Evidence: `uni02d_sonya_gate_acceptance_report.json`, semantic term quarantine, runtime profile leakage, prior origin provenance, and prior quarantine packets.

Prior quarantine: selected priors remain bounded and must not be canonized. Review selected_priors and matches[*].prior shape scanning for provenance and quarantine posture.

Claim allowed: safe portability fixture evidence can be reviewed.

Claims blocked: UNI-02D safe portability fixture is not universal portability proof.

Caution: safe portability fixture is not universal proof.
""",
        "retro-lane-00.md": f"""# RETRO-LANE-00

Purpose: inspect retrosynthesis admission lanes without executing retrosynthesis.

Run command:

```powershell
{RETRO_LANE_COMMAND}
```

Evidence: `retrosynthesis_admission_packet.json`, `retrosynthesis_admission_review_packet.json`, `retro_lane_00_acceptance_receipt.json`.

Lane definitions: sandbox_auto, review_required, blocked.

Claim allowed: admission lane posture can be reviewed.

Claims blocked: Retrosynthesis admission is not retrosynthesis execution; hallucination is telemetry not evidence.

Caution: admission is not execution.
""",
        "public-utility-alpha.md": f"""# Public Utility Alpha

Purpose: inspect PUBLIC-UTILITY-ALPHA-00 as a local fixture-only reviewer demo of governed artifact cognition.

Run command:

```powershell
{PUBLIC_UTILITY_ALPHA_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in PUBLIC_UTILITY_ALPHA_ARTIFACTS)}.

Claim allowed: A local fixture-only reviewer demo can assemble the accepted governed artifact cognition chain and make its evidence, route timeline, candidate packet path, bypass block, model-braid observation, catalog boundary, inventory, and parity artifacts inspectable.

Claims blocked: {" ".join(PUBLIC_UTILITY_ALPHA_CLAIMS_BLOCKED)}

Caution: This is a local reviewer harness. It demonstrates bounded artifact assembly and claim-boundary visibility. It is not a product launch, not deployment readiness, and not proof of real-world performance.
""",
        "raw-baseline-comparison.md": f"""# Raw Baseline Comparison

Purpose: inspect RAW-BASELINE-COMPARISON-00 as a fixture-only measurement scaffold comparing raw-text-style baseline arms with the Sonya-governed candidate packet path.

Run command:

```powershell
{RAW_BASELINE_COMPARISON_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in RAW_BASELINE_COMPARISON_ARTIFACTS)}.

Claim allowed: RAW-BASELINE-COMPARISON-00 provides a fixture-only measurement scaffold for comparing raw-text-style baseline arms with the Sonya-governed candidate packet path across unsupported-claim count, source-linkage posture, route receipt posture, forbidden-artifact leakage, and raw-output admission.

Claims blocked: {"; ".join(RAW_BASELINE_COMPARISON_CLAIMS_BLOCKED)}.

Caution: This phase is measurement infrastructure only. It does not prove that governed artifact cognition reduces hallucinations, improves model quality, or performs better on real-world tasks. It establishes a scaffold for future controlled comparisons.
""",
        "evidence-review-pack.md": f"""# Evidence Review Pack v0.1

Purpose: inspect EVIDENCE-REVIEW-PACK-00 as the first product-facing governed review receipt. Evidence Review Pack v0.1 consumes Universal Evidence Ingress and UCC Control Profile Selector artifacts to produce source-bounded claim/evidence review artifacts, unsupported-claim visibility, uncertainty retention, counterevidence preservation, semantic ecology signals, UCC threshold posture, action recommendation, reviewer checklist, and export parity.

Evidence Review Pack v0.1 is AI review that shows its work.

Run command:

```powershell
{EVIDENCE_REVIEW_PACK_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in EVIDENCE_REVIEW_PACK_ARTIFACTS)}.

Prerequisite phases: UNIVERSAL-EVIDENCE-INGRESS-00, UCC-CONTROL-PROFILE-SELECTOR-00, and CANONICAL-METRIC-PACKET-01.

Claim allowed: EVIDENCE-REVIEW-PACK-00 demonstrates a fixture-only, source-bounded, UCC-control-profile-governed review receipt that makes supported claims, unsupported claims, missing uncertainty, preserved counterevidence, semantic drift signals, UCC threshold posture, reserved-authority blocks, and reviewer next actions inspectable.

Claims blocked: {"; ".join(EVIDENCE_REVIEW_PACK_CLAIMS_BLOCKED)}.

Caution: Evidence Review Pack v0.1 is a fixture-only review receipt. It can show which claims are source-supported or unsupported in a controlled fixture and can expose missing uncertainty and counterevidence. It does not certify truth, does not provide professional advice, does not prove hallucination reduction, and does not authorize deployment.
""",
        "rw-comp-01.md": f"""# RW-COMP-01

Purpose: inspect RW-COMP-01 as an accepted fixture-only comparison of raw summary, raw multi-model summary, RAG-style grounded summary, Triadic partial governance, and full Evidence Review Pack v0.1. It is a step toward future hallucination-reduction evidence, not hallucination reduction proof.

RW-COMP-01 is a fixture-only comparison scaffold, not hallucination reduction proof.

Run command:

```powershell
{RW_COMP_01_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in RW_COMP_01_ARTIFACTS)}.

Prerequisite phases: UNIVERSAL-EVIDENCE-INGRESS-00, UCC-CONTROL-PROFILE-SELECTOR-00, EVIDENCE-REVIEW-PACK-00, CANONICAL-METRIC-PACKET-01, and RAW-BASELINE-COMPARISON-00.

Claim allowed: RW-COMP-01 demonstrates a fixture-only comparison where full Evidence Review Pack v0.1 exposes supported claims, unsupported claims, source-reference posture, uncertainty omissions, counterevidence preservation, UCC threshold posture, and artifact completeness more explicitly than raw or partially governed fixture baselines.

Fixture summary:

{chr(10).join(f"- {item}" for item in RW_COMP_01_FIXTURE_SUMMARY)}

Claims blocked: {"; ".join(RW_COMP_01_CLAIMS_BLOCKED)}.

Caution: RW-COMP-01 is a deterministic fixture comparison. It can show that the Evidence Review Pack exposes review-relevant structure in one controlled comparison, but it does not prove hallucination reduction, does not prove model superiority, does not prove real-world performance, is not professional-advice quality, and is not production compliance. Future RW-COMP phases must add larger fixture batteries, blinded scoring, held-out examples, external reproduction, and live-model/provider controls before stronger claims are authorized.
""",
        "rw-comp-02.md": f"""# RW-COMP-02

Purpose: inspect RW-COMP-02 as an accepted deterministic multi-fixture comparison battery. It extends RW-COMP-01 across six fixture families and compares raw single-model, raw multi-model, RAG-style grounded, Triadic-without-Phase-6, and full Evidence Review Pack arms. It is a step toward future hallucination-reduction evidence, not hallucination reduction proof.

RW-COMP-02 is a deterministic multi-fixture comparison battery and remains not hallucination reduction proof.

Run command:

```powershell
{RW_COMP_02_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in RW_COMP_02_ARTIFACTS)}.

Prerequisite phases: UNIVERSAL-EVIDENCE-INGRESS-00, UCC-CONTROL-PROFILE-SELECTOR-00, EVIDENCE-REVIEW-PACK-00, CANONICAL-METRIC-PACKET-01, RAW-BASELINE-COMPARISON-00, and RW-COMP-01.

Claim allowed: RW-COMP-02 demonstrates a deterministic multi-fixture comparison battery where Evidence Review Pack v0.1 exposes review-relevant structure across multiple fixture families, including unsupported claims, source-reference validity, uncertainty retention, counterevidence preservation, artifact completeness, UCC threshold posture, and review burden indicators.

Dashboard summary:

- fixture_count = {RW_COMP_02_DASHBOARD_SUMMARY["fixture_count"]}
- total_rows = {RW_COMP_02_DASHBOARD_SUMMARY["total_rows"]}
- arm_count_per_fixture = {RW_COMP_02_DASHBOARD_SUMMARY["arm_count_per_fixture"]}
- compared arms: {", ".join(RW_COMP_02_DASHBOARD_SUMMARY["compared_arms"])}
- reported interpretation: {RW_COMP_02_DASHBOARD_SUMMARY["reported_interpretation"]}
- interpretation boundary: {"; ".join(RW_COMP_02_DASHBOARD_SUMMARY["interpretation_boundary"])}

Claims blocked: {"; ".join(RW_COMP_02_CLAIMS_BLOCKED)}.

Caution: RW-COMP-02 is a deterministic multi-fixture battery. It can show that the Evidence Review Pack exposes more review-relevant structure than raw or partially governed fixture baselines across several controlled examples. It does not prove hallucination reduction, does not prove model superiority, does not prove real-world performance, is not professional-advice quality, and is not production compliance. Future phases must add held-out fixtures, blinded scoring, statistical analysis, external reproduction, and controlled live-model/provider conditions before stronger claims are authorized.
""",
        "rw-comp-03.md": f"""# RW-COMP-03

Purpose: inspect RW-COMP-03 as an accepted held-out, blinded, pre-registered fixture-scoring scaffold extending RW-COMP-02 with held-out fixture IDs, blinded arm labels, simulated scores, a statistics plan, and a second-pass Evidence Review Pack candidate arm.

RW-COMP-03 is a held-out blinded fixture scaffold, not hallucination reduction proof.

Run command:

```powershell
{RW_COMP_03_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in RW_COMP_03_ARTIFACTS)}.

Prerequisite phases: RW-COMP-02, EVIDENCE-REVIEW-PACK-01, RETROSYNTHESIS-SANDBOX-CYCLE-01, EVIDENCE-REVIEW-PACK-00, UCC-CONTROL-PROFILE-SELECTOR-00, UNIVERSAL-EVIDENCE-INGRESS-00, CANONICAL-METRIC-PACKET-01, and RAW-BASELINE-COMPARISON-00.

Claim allowed: RW-COMP-03 demonstrates a held-out blinded fixture-scoring scaffold with simulated scores, blind labels, pre-registered scoring dimensions, statistics planning, and a second-pass Evidence Review Pack candidate arm. It is a step toward future hallucination-reduction evidence, not hallucination reduction proof, not model superiority proof, not live model evaluation, and not live human study.

Dashboard summary:

{chr(10).join(f"- {key} = {str(value).lower()}" for key, value in RW_COMP_03_DASHBOARD_SUMMARY.items())}

Claims blocked: {"; ".join(RW_COMP_03_CLAIMS_BLOCKED)}.

Reviewer caution: RW-COMP-03 is a held-out blinded fixture scaffold with simulated scoring only. It introduces a pre-registered scoring and statistics structure for future evaluation, but it does not prove hallucination reduction, does not prove model superiority, does not show live model behavior, does not measure human reviewer performance, is not professional-advice quality, is not compliance certification, and is not production readiness.
""",
        "retrosynthesis-sandbox-cycle.md": f"""# Retrosynthesis Sandbox Cycle

Purpose: inspect RETROSYNTHESIS-SANDBOX-CYCLE-01 as the first bounded candidate repair cycle for incomplete or contradiction-bearing Evidence Review Pack-style artifacts.

Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption.

Run command:

```powershell
{RETRO_SANDBOX_CYCLE_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in RETRO_SANDBOX_CYCLE_ARTIFACTS)}.

Prerequisite phases: RETRO-LANE-00, EVIDENCE-REVIEW-PACK-00, RW-COMP-02, UCC-CONTROL-PROFILE-SELECTOR-00, UNIVERSAL-EVIDENCE-INGRESS-00, and CANONICAL-METRIC-PACKET-01.

Claim allowed: RETROSYNTHESIS-SANDBOX-CYCLE-01 demonstrates a bounded candidate-only repair cycle over incomplete Evidence Review Pack artifacts. It emits missing-evidence requests, claim-map revision candidates, uncertainty-restoration candidates, counterevidence-expansion candidates, and next-experiment recommendations while remaining not canon adoption, not memory write, not final answer release, not Publisher finalization, not deployment authority, not Omega detection, not publication claim, not live model execution, and not remote provider call.

Dashboard summary:

{chr(10).join(f"- {key} = {str(value).lower()}" for key, value in RETRO_SANDBOX_CYCLE_DASHBOARD_SUMMARY.items())}

Claims blocked: {"; ".join(RETRO_SANDBOX_CYCLE_CLAIMS_BLOCKED)}.

Reviewer caution: RETROSYNTHESIS-SANDBOX-CYCLE-01 emits repair candidates only. Missing evidence requests are not external fetches. Claim-map revisions are not accepted evidence. Uncertainty restoration and counterevidence expansion remain candidate artifacts until future review gates promote them. This phase does not write memory, does not adopt canon, does not publish claims, does not release final answers, does not perform Omega detection, and does not authorize deployment.
""",
        "evidence-review-pack-second-pass.md": f"""# Evidence Review Pack Second Pass

Purpose: inspect EVIDENCE-REVIEW-PACK-01 as the first bounded second-pass review candidate loop over Retrosynthesis Sandbox Cycle repair candidates.

Evidence Review Pack second pass is candidate revision, not accepted evidence.

Run command:

```powershell
{EVIDENCE_REVIEW_PACK_01_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in EVIDENCE_REVIEW_PACK_01_ARTIFACTS)}.

Prerequisite phases: EVIDENCE-REVIEW-PACK-00, RETROSYNTHESIS-SANDBOX-CYCLE-01, RW-COMP-02, UCC-CONTROL-PROFILE-SELECTOR-00, UNIVERSAL-EVIDENCE-INGRESS-00, and CANONICAL-METRIC-PACKET-01.

Claim allowed: EVIDENCE-REVIEW-PACK-01 demonstrates a candidate-only second-pass review loop that consumes retrosynthesis sandbox repair candidates and emits bounded revision candidates for claim-map status, omitted uncertainty, counterevidence, and structural visibility deltas.

Dashboard summary:

{chr(10).join(f"- {key} = {str(value).lower()}" for key, value in EVIDENCE_REVIEW_PACK_01_DASHBOARD_SUMMARY.items())}

Claims blocked: {"; ".join(EVIDENCE_REVIEW_PACK_01_CLAIMS_BLOCKED)}.

Reviewer caution: EVIDENCE-REVIEW-PACK-01 emits candidate revisions only. Its deltas are structural visibility descriptors, not hallucination-reduction proof. Claim-map revisions are not accepted evidence. Uncertainty and counterevidence revisions require future review gates before promotion. This phase does not write memory, does not adopt canon, does not publish claims, does not release final answers, does not perform Omega detection, does not finalize Publisher output, and does not authorize deployment.
""",
        "sonya-adapter-contract-registry.md": f"""# Sonya Adapter Contract Registry

Adapter capability is not adapter authorization.

Purpose: describe SONYA-ADAPTER-CONTRACT-REGISTRY-01 as a fixture-only versioned adapter-contract scaffold for future Sonya adapters. Adapter contracts are versioned configuration; they declare capability, consent, failure, telemetry, and provenance-training policy without enabling live adapters.

## Allowed claim

SONYA-ADAPTER-CONTRACT-REGISTRY-01 demonstrates a fixture-only versioned adapter-contract scaffold that declares adapter capabilities, consent profiles, failure policies, telemetry requirements, and provenance-training policies while keeping all adapters disabled or blocked and forbidding raw output admission.

## Reproduction command

```powershell
{SONYA_ADAPTER_CONTRACT_REGISTRY_COMMAND}
```

## Evidence artifacts

{chr(10).join(f"- `{artifact}`" for artifact in SONYA_ADAPTER_CONTRACT_REGISTRY_ARTIFACTS)}

## Dashboard summary

{chr(10).join(f"- {key} = {str(value).lower()}" for key, value in SONYA_ADAPTER_CONTRACT_REGISTRY_DASHBOARD_SUMMARY.items())}

## Reviewer boundaries

- adapter contracts are versioned configuration.
- all adapters disabled or blocked.
- no live adapter execution occurred.
- no network calls occurred.
- raw output is forbidden.
- candidate packet required.
- failure receipts required.
- provenance-training policy is present.

Claims blocked: {"; ".join(SONYA_ADAPTER_CONTRACT_REGISTRY_CLAIMS_BLOCKED)}.

Reviewer caution: SONYA-ADAPTER-CONTRACT-REGISTRY-01 defines adapter contracts only. It does not execute adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy.
""",
        "sonya-adapter-smoke.md": f"""# Sonya Adapter Smoke

Sonya Adapter Smoke exercises contracts, not live adapters.

Purpose: describe SONYA-ADAPTER-SMOKE-00 as an accepted fixture-only adapter-contract smoke test. It exercises adapter selection, consent checks, capability checks, Sonya gateway requirements, raw output rejected or absent posture, candidate packet requirement, failure receipts, telemetry events, and provenance events. Boundary posture: not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, and not model weight training.

## Allowed claim

SONYA-ADAPTER-SMOKE-00 demonstrates fixture-only adapter contract exercise: adapter selection, consent and capability checks, Sonya gateway requirement, raw-output rejection, candidate-packet requirement, failure receipt emission, telemetry event emission, and provenance event emission without live adapter execution or network/provider calls.

## Reproduction command

```powershell
{SONYA_ADAPTER_SMOKE_COMMAND}
```

## Evidence artifacts

{chr(10).join(f"- `{artifact}`" for artifact in SONYA_ADAPTER_SMOKE_ARTIFACTS)}

## Prerequisite phases

- SONYA-ADAPTER-CONTRACT-REGISTRY-01
- PROVENANCE-TRAINING-LEDGER-00
- UNIVERSAL-STAGE-PIPELINE-00
- ARTIFACT-CONTRACT-REGISTRY-01
- UNIVERSAL-COMPATIBILITY-MATRIX-00
- SONYA-GW-01

## Dashboard summary

{chr(10).join(f"- {key} = {str(value).lower()}" for key, value in SONYA_ADAPTER_SMOKE_DASHBOARD_SUMMARY.items())}

## Reviewer boundaries

- Sonya Adapter Smoke exercises contracts, not live adapters.
- adapter selection, consent checks, capability checks, and Sonya gateway requirements are fixture-only contract checks.
- not adapter execution.
- not live adapter execution.
- not network authorization.
- not remote provider call.
- not live model execution.
- raw output rejected or absent.
- candidate packet required for fixture model output.
- failure receipts visible.
- telemetry events visible.
- provenance events visible.
- not memory write.
- not final answer release.
- not deployment authority.
- not model weight training.
- not production readiness.

Claims blocked: {"; ".join(SONYA_ADAPTER_SMOKE_CLAIMS_BLOCKED)}.

Reviewer caution: SONYA-ADAPTER-SMOKE-00 exercises contracts only. It does not execute adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy.
""",
        "sonya-local-fixture-adapter.md": f"""# Sonya Local Fixture Adapter

Required phrase: Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters.

Purpose: describe SONYA-LOCAL-FIXTURE-ADAPTER-01 as an accepted deterministic local-only fixture adapter execution phase. This page records that local fixture adapter execution occurred under Sonya adapter contracts and emitted candidate packets, failure receipts, telemetry events, and provenance events. This is not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, and not model weight training.

## Allowed claim

SONYA-LOCAL-FIXTURE-ADAPTER-01 demonstrates deterministic local-only fixture adapter execution under Sonya adapter contracts, with candidate packets, failure receipts, telemetry events, and provenance events, while all live/network/provider/memory/final/deployment/model-training paths remain blocked.

## Reproduction command

```powershell
{SONYA_LOCAL_FIXTURE_ADAPTER_COMMAND}
```

## Primary artifacts

{chr(10).join(f"- `{artifact}`" for artifact in SONYA_LOCAL_FIXTURE_ADAPTER_ARTIFACTS)}

## Observed fixture counts

- candidate packet count: 3
- failure receipt count: 6
- telemetry event count: 52
- provenance event count: 35
- executed local adapter IDs: fixture_text_model_adapter, fixture_summary_generator_adapter, local_file_transform_adapter
- blocked adapter IDs: hash_only_evidence_adapter, remote_provider_placeholder_adapter, browser_placeholder_adapter, atlas_memory_placeholder_adapter, sophia_route_placeholder_adapter

## Dashboard posture

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in SONYA_LOCAL_FIXTURE_ADAPTER_DASHBOARD_SUMMARY.items())}

## Blocked claims

{chr(10).join(f"- {claim}" for claim in SONYA_LOCAL_FIXTURE_ADAPTER_CLAIMS_BLOCKED)}

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-01 executes deterministic local fixture adapters only. It does not execute live adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy.
""",
        "evidence-review-pack-local-adapter.md": f"""# Evidence Review Pack local adapter

Required phrase: Adapter output is not accepted as cognition directly.

Purpose: describe EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 as an accepted local adapter candidate review phase. EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 routes Sonya local fixture adapter candidates into Evidence Review Pack. Candidate packets require UCC-controlled review. The claim map is not truth certification. The candidate is not final answer. No memory write is authorized. No deployment is authorized. No network authorization is granted. No provider call is made. No model-weight training is authorized. No hallucination-reduction proof is authorized.

## Allowed claim

EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 demonstrates that a Sonya local fixture adapter candidate can be bound to review, governed by a UCC control profile, evaluated through claim/evidence mapping, and recorded through provenance events without accepting raw adapter output as cognition.

## Reproduction command

```powershell
{EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_COMMAND}
```

## Primary artifacts

{chr(10).join(f"- `{artifact}`" for artifact in EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_ARTIFACTS)}

## Dashboard posture

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_DASHBOARD_SUMMARY.items())}

## Blocked claims

{chr(10).join(f"- {claim}" for claim in EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_CLAIMS_BLOCKED)}

Reviewer caution: EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 routes a local fixture adapter candidate into review only. It does not accept adapter output as cognition directly, does not authorize adapter execution, does not write memory, does not release final answers, does not deploy, does not train model weights, and does not prove hallucination reduction.
""",
        "sonya-local-fixture-adapter-multi-route.md": f"""# Sonya Local Fixture Adapter multi-route

Required phrase: Selection policy is not final answer.

Purpose: describe SONYA-LOCAL-FIXTURE-ADAPTER-02 as an accepted local-only multi-adapter fixture route. Multiple deterministic local fixture adapter candidates were compared, selection policy was applied, and the selected candidate still requires Evidence Review Pack route. Selection is not adapter authorization. Candidate comparison is not model quality benchmark. No live/network/provider/memory/final/deployment authority is granted.

## Allowed claim

SONYA-LOCAL-FIXTURE-ADAPTER-02 demonstrates local-only comparison of deterministic fixture adapter candidates, applies a selection policy, and records that the selected candidate still requires Evidence Review Pack routing.

## Reproduction command

```powershell
{SONYA_LOCAL_FIXTURE_ADAPTER_02_COMMAND}
```

## Primary artifacts

{chr(10).join(f"- `{artifact}`" for artifact in SONYA_LOCAL_FIXTURE_ADAPTER_02_ARTIFACTS)}

## Dashboard posture

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in SONYA_LOCAL_FIXTURE_ADAPTER_02_DASHBOARD_SUMMARY.items())}

## Blocked claims

{chr(10).join(f"- {claim}" for claim in SONYA_LOCAL_FIXTURE_ADAPTER_02_CLAIMS_BLOCKED)}

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-02 compares deterministic local fixture adapter candidates only. Selection is not final answer, not adapter authorization, not truth certification, and not a model quality benchmark. The selected candidate still requires Evidence Review Pack routing before it can be reviewed as cognition.
""",

        "sonya-local-fixture-adapter-lineage.md": f"""# Sonya Local Fixture Adapter lineage clarity

Required phrase: Source fixture references are not stale identity leakage.

Purpose: describe SONYA-LOCAL-FIXTURE-ADAPTER-03 as an accepted methods-lineage clarity phase for Sonya local fixture adapter multi-route artifacts. Nested SONYA-LOCAL-FIXTURE-ADAPTER-01 references are source fixture dependencies, not stale identity leakage. Current route identity is explicit. Source fixture identity is explicit. Evidence Review Pack local-adapter route references are explicit. Lineage does not grant authority.

## Allowed claim

SONYA-LOCAL-FIXTURE-ADAPTER-03 demonstrates explicit lineage clarity for Sonya local fixture adapter multi-route artifacts by distinguishing current route identity, source fixture identity, source fixture role, and Evidence Review Pack local-adapter route references.

## Reproduction command

```powershell
{SONYA_LOCAL_FIXTURE_ADAPTER_03_COMMAND}
```

## Primary artifacts

{chr(10).join(f"- `{artifact}`" for artifact in SONYA_LOCAL_FIXTURE_ADAPTER_03_ARTIFACTS)}

## Dashboard posture

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in SONYA_LOCAL_FIXTURE_ADAPTER_03_DASHBOARD_SUMMARY.items())}

## Blocked claims

{chr(10).join(f"- {claim}" for claim in SONYA_LOCAL_FIXTURE_ADAPTER_03_CLAIMS_BLOCKED)}

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-03 is a lineage clarity packet only. It clarifies that nested source fixture references are dependencies and not stale identity leakage. It does not execute adapters, authorize network, call providers, write memory, release final answers, train models, or deploy.
""",
        "universal-architecture.md": f"""# Universal Architecture Scaffold

The brain runs cognition stages; experiments configure those stages.

Purpose: show the accepted anti-experimentware architecture scaffold that makes CoherenceLattice a reusable artifact-cognition substrate rather than a pile of bespoke experiment wrappers.

## Architecture summary

- UNIVERSAL-STAGE-PIPELINE-00 defines reusable cognition-stage contracts.
- ARTIFACT-CONTRACT-REGISTRY-01 externalizes artifact roles and profile contracts into versioned configuration.
- UNIVERSAL-COMPATIBILITY-MATRIX-00 tests whether the same stages and contracts handle varied input classes or emit deterministic fail-closed receipts.

profiles are configuration. experiments are configurations over reusable cognition stages and versioned artifact contracts.

## Reproduction commands

Universal Stage Pipeline:

```powershell
{UNIVERSAL_STAGE_PIPELINE_COMMAND}
```

Artifact Contract Registry:

```powershell
{ARTIFACT_CONTRACT_REGISTRY_COMMAND}
```

Universal Compatibility Matrix:

```powershell
{UNIVERSAL_COMPATIBILITY_MATRIX_COMMAND}
```

## Evidence artifacts

- UNIVERSAL-STAGE-PIPELINE-00: {", ".join(f"`{artifact}`" for artifact in UNIVERSAL_STAGE_PIPELINE_ARTIFACTS)}.
- ARTIFACT-CONTRACT-REGISTRY-01: {", ".join(f"`{artifact}`" for artifact in ARTIFACT_CONTRACT_REGISTRY_ARTIFACTS)}.
- UNIVERSAL-COMPATIBILITY-MATRIX-00: {", ".join(f"`{artifact}`" for artifact in UNIVERSAL_COMPATIBILITY_MATRIX_ARTIFACTS)}.

## Allowed claim

The universal architecture scaffold demonstrates that accepted experiments can be described as configurations over reusable stages and versioned artifact contracts, with unsupported inputs preserved by hash-only or failed-closed receipts.

## Universal Compatibility Matrix dashboard summary

{chr(10).join(f"- {key} = {str(value).lower()}" for key, value in UNIVERSAL_COMPATIBILITY_MATRIX_DASHBOARD_SUMMARY.items())}

## Blocked claims

Claims blocked: {"; ".join(UNIVERSAL_ARCHITECTURE_CLAIMS_BLOCKED)}.

Reviewer caution: this is not product release, not experiment result, not benchmark result, not truth certification, not deployment authority, not final answer release, not hallucination reduction proof, not model superiority proof, not live model evaluation, not live human study, not recursive self-improvement, and not AI consciousness claim.
""",
        "governed-artifact-cognition-paper.md": "# Governed Artifact Cognition Paper\n\nSummary: systems paper for governed artifact cognition as a reproducible audit lab.\n\nLinks: `papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md`, reviewer quickstart, claim boundary table, status.json.\n\nClaim boundaries: not truth certification, not deployment authority, not final answer release, local fixture only, requires external peer review.\n\nValidation command: `python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json`.\n",
        "waveform-rosetta-paper.md": "# Waveform Rosetta Paper\n\nSummary: methods paper for closed-form WAVE Gold-Physics metric calibration.\n\nLinks: `papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md`, reviewer quickstart, theorem table, status.json.\n\nClaim boundaries: not universal ontology, not psychoacoustic effect, not AI consciousness, not deployment authority, not truth certification, requires external peer review.\n\nValidation command: `python tools/validate_publication_claims.py --paper papers/waveform_rosetta/PUB_WAVE_ROSETTA_01.md --quickstart papers/waveform_rosetta/reviewer_quickstart.md --status papers/waveform_rosetta/status.json`.\n",
        "reviewer-quickstart.md": f"""# Reviewer Quickstart

## Read first path

1. claim boundaries
2. governed artifact cognition paper
3. WAVE Rosetta paper
4. SONYA-AEGIS-SMOKE-02
5. WAVE family
6. UNI-02D Sonya gate
7. RETRO-LANE-00
8. Public Utility Alpha
9. Raw Baseline Comparison
10. Evidence Review Pack
11. RW-COMP-01
12. RW-COMP-02
13. Retrosynthesis Sandbox Cycle
14. Evidence Review Pack second pass
15. RW-COMP-03
16. Universal Architecture Scaffold
17. Sonya Adapter Contract Registry
18. Sonya Adapter Smoke
19. Sonya Local Fixture Adapter
20. Evidence Review Pack local adapter
21. Sonya Local Fixture Adapter multi-route

## CoherenceLattice commands

PowerShell SONYA-AEGIS-SMOKE-02:

```powershell
{SONYA_AEGIS_COMMAND}
```

PowerShell WAVE Gold-Physics:

```powershell
{WAVE_FAMILY_COMMAND}
```

PowerShell UNI-02D Sonya gate:

```powershell
{UNI02D_COMMAND}
```

PowerShell RETRO-LANE-00:

```powershell
{RETRO_LANE_COMMAND}
```

PowerShell Public Utility Alpha:

```powershell
{PUBLIC_UTILITY_ALPHA_COMMAND}
```

PowerShell Raw Baseline Comparison:

```powershell
{RAW_BASELINE_COMPARISON_COMMAND}
```

PowerShell Evidence Review Pack:

```powershell
{EVIDENCE_REVIEW_PACK_COMMAND}
```

Evidence Review Pack v0.1 is AI review that shows its work. It is not legal advice, not medical advice, not tax advice, and not compliance certification.

PowerShell RW-COMP-01:

```powershell
{RW_COMP_01_COMMAND}
```

RW-COMP-01 is a fixture-only comparison scaffold, not hallucination reduction proof. It is not model superiority proof, not professional advice, not compliance certification, and not production evaluation.

PowerShell RW-COMP-02:

```powershell
{RW_COMP_02_COMMAND}
```

RW-COMP-02 is a deterministic multi-fixture comparison battery and remains not hallucination reduction proof. It is not model superiority proof, not professional advice, not compliance certification, and not production evaluation.

PowerShell Retrosynthesis Sandbox Cycle:

```powershell
{RETRO_SANDBOX_CYCLE_COMMAND}
```

Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption. It is not memory write, not final answer release, not Publisher finalization, not Omega detection, not deployment authority, and not recursive self-improvement.

PowerShell Evidence Review Pack second pass:

```powershell
{EVIDENCE_REVIEW_PACK_01_COMMAND}
```

Evidence Review Pack second pass is candidate revision, not accepted evidence. It is not canon adoption, not memory write, not final answer release, not Publisher finalization, not Omega detection, not deployment authority, not hallucination reduction proof, and not recursive self-improvement.

PowerShell RW-COMP-03:

```powershell
{RW_COMP_03_COMMAND}
```

RW-COMP-03 is a held-out blinded fixture scaffold with simulated scores and a statistics plan. It includes a second-pass candidate arm and is a step toward future hallucination-reduction evidence, not hallucination reduction proof, not model superiority proof, not live model evaluation, and not live human study.


## Universal Architecture Scaffold

The brain runs cognition stages; experiments configure those stages.

Universal Architecture Scaffold covers UNIVERSAL-STAGE-PIPELINE-00, ARTIFACT-CONTRACT-REGISTRY-01, and UNIVERSAL-COMPATIBILITY-MATRIX-00. Profiles are configuration, experiments are configurations, and unsupported inputs are preserved with fail-closed receipts or hash-only receipts instead of semantic interpretation.

Universal Stage Pipeline:

```powershell
{UNIVERSAL_STAGE_PIPELINE_COMMAND}
```

Artifact Contract Registry:

```powershell
{ARTIFACT_CONTRACT_REGISTRY_COMMAND}
```

Universal Compatibility Matrix:

```powershell
{UNIVERSAL_COMPATIBILITY_MATRIX_COMMAND}
```

This scaffold is not product release, not experiment result, not benchmark result, not hallucination reduction proof, not deployment authority, and not recursive self-improvement.


## Sonya Adapter Contract Registry

Adapter capability is not adapter authorization.

Sonya Adapter Contract Registry covers SONYA-ADAPTER-CONTRACT-REGISTRY-01. Adapter contracts are versioned configuration. All adapters disabled or blocked means not adapter execution and not network authorization; raw output is forbidden, candidate packet required, failure receipts required, and provenance-training policy is present.

```powershell
{SONYA_ADAPTER_CONTRACT_REGISTRY_COMMAND}
```

Expected posture:

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in SONYA_ADAPTER_CONTRACT_REGISTRY_DASHBOARD_SUMMARY.items())}

This scaffold is not adapter execution, not live model execution, not remote provider call, not network authorization, not memory write, not final answer release, not deployment authority, not truth certification, not model weight training, not hallucination reduction proof, not recursive self-improvement, and not production readiness.

## Sonya Adapter Smoke

Sonya Adapter Smoke exercises contracts, not live adapters.

Sonya Adapter Smoke covers SONYA-ADAPTER-SMOKE-00 as an accepted fixture-only adapter-contract smoke test. It exercises adapter selection, consent checks, capability checks, Sonya gateway requirements, raw output rejected or absent posture, candidate packet requirement, failure receipts, telemetry events, and provenance events. Boundary posture: not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, and not model weight training.

```powershell
{SONYA_ADAPTER_SMOKE_COMMAND}
```

Expected posture:

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in SONYA_ADAPTER_SMOKE_DASHBOARD_SUMMARY.items())}

This smoke test is not adapter execution, not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, not truth certification, not model weight training, not hallucination reduction proof, not recursive self-improvement, and not production readiness.

## Sonya Local Fixture Adapter

Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters.

SONYA-LOCAL-FIXTURE-ADAPTER-01 covers accepted local-only fixture adapter execution under Sonya adapter contracts. Deterministic local fixture adapters emitted candidate packets, failure receipts, telemetry events, and provenance events. Boundary posture: not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, and not model weight training.

```powershell
{SONYA_LOCAL_FIXTURE_ADAPTER_COMMAND}
```

Expected posture:

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in SONYA_LOCAL_FIXTURE_ADAPTER_DASHBOARD_SUMMARY.items())}

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-01 executes deterministic local fixture adapters only. It does not execute live adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy. It is not truth certification, not hallucination reduction proof, not recursive self-improvement, and not production readiness.

## Evidence Review Pack local adapter

Adapter output is not accepted as cognition directly.

EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 routes Sonya local fixture adapter candidates into Evidence Review Pack. Candidate packets require UCC-controlled review. The claim map is not truth certification. The candidate is not final answer. No memory write is authorized. No deployment is authorized. No network authorization is granted. No provider call is made. No model-weight training is authorized. No hallucination-reduction proof is authorized.

```powershell
{EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_COMMAND}
```

Expected posture:

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in EVIDENCE_REVIEW_PACK_LOCAL_ADAPTER_DASHBOARD_SUMMARY.items())}

Reviewer caution: EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 routes a local fixture adapter candidate into review only. It is not accepted evidence, not adapter authorization, not memory write, not final answer release, not deployment authority, not truth certification, not model weight training, not hallucination reduction proof, and not recursive self-improvement.

## Sonya Local Fixture Adapter multi-route

Selection policy is not final answer.

SONYA-LOCAL-FIXTURE-ADAPTER-02 compares multiple deterministic local fixture adapter candidates, applies a selection policy, and records that the selected candidate still requires Evidence Review Pack route. Selection is not adapter authorization. Candidate comparison is not model quality benchmark. No live/network/provider/memory/final/deployment authority is granted.

```powershell
{SONYA_LOCAL_FIXTURE_ADAPTER_02_COMMAND}
```

Expected posture:

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in SONYA_LOCAL_FIXTURE_ADAPTER_02_DASHBOARD_SUMMARY.items())}

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-02 compares deterministic local fixture adapter candidates only. Selection is not final answer, not adapter authorization, not truth certification, and not a model quality benchmark.

## Sonya Local Fixture Adapter lineage clarity

Source fixture references are not stale identity leakage.

SONYA-LOCAL-FIXTURE-ADAPTER-03 clarifies source/current experiment lineage for Sonya local fixture adapter multi-route artifacts. Current route identity is explicit. Source fixture identity is explicit. Evidence Review Pack local-adapter route references are explicit. Lineage does not grant authority.

```powershell
{SONYA_LOCAL_FIXTURE_ADAPTER_03_COMMAND}
```

Expected posture:

{chr(10).join(f"- `{key} = {str(value).lower()}`" for key, value in SONYA_LOCAL_FIXTURE_ADAPTER_03_DASHBOARD_SUMMARY.items())}

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-03 is a lineage clarity packet only. It clarifies that nested source fixture references are dependencies and not stale identity leakage. It does not execute adapters, authorize network, call providers, write memory, release final answers, train models, or deploy.

## Sophia commands

```powershell
{SOPHIA_UCC_COMMAND}
```

## uvlm-publications commands

`python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json`

`python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite`

not truth certification; not deployment authority; not final answer release; local fixture only; requires external peer review.
""",
    }


def build(out_dir: Path, docs_dir: Path) -> None:
    _write_json(out_dir / "experiment_suite_dashboard.json", dashboard_payload())
    _write_json(out_dir / "accepted_phase_matrix.json", accepted_phase_matrix())
    _write_json(out_dir / "reproducibility_index.json", reproducibility_index())
    _write_json(out_dir / "claim_boundary_index.json", claim_boundary_index())
    _write_json(out_dir / "artifact_index.json", artifact_index())
    _write_json(out_dir / "status.json", status_payload())
    for name, text in docs().items():
        _write_text(docs_dir / name, text)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build public experiment suite reproducibility dashboard.")
    parser.add_argument("--out-dir", type=Path, default=Path("registry"))
    parser.add_argument("--docs-dir", type=Path, default=Path("docs/experiment-suite"))
    parser.add_argument("--coherencelattice-repro-pack", type=Path)
    parser.add_argument("--sonya-aegis-report", type=Path)
    parser.add_argument("--wave-family-report", type=Path)
    parser.add_argument("--uni02d-report", type=Path)
    parser.add_argument("--retro-lane-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    build(args.out_dir, args.docs_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
