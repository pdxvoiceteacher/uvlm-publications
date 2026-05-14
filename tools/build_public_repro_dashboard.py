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
ACCEPTED_PHASES = [
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
        "phase_id": "SONYA-ADAPTER-SMOKE-00",
        "repo": "pdxvoiceteacher/CoherenceLattice",
        "status": "accepted",
        "evidence_type": "fixture_adapter_contract_smoke",
        "product_posture": "adapter_contract_smoke_without_live_execution",
        "primary_artifacts": SONYA_ADAPTER_SMOKE_ARTIFACTS,
        "prerequisite_phases": [
            "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
            "PROVENANCE-TRAINING-LEDGER-00",
            "UNIVERSAL-STAGE-PIPELINE-00",
            "ARTIFACT-CONTRACT-REGISTRY-01",
            "UNIVERSAL-COMPATIBILITY-MATRIX-00",
            "SONYA-GW-01",
        ],
        "dashboard_summary": SONYA_ADAPTER_SMOKE_DASHBOARD_SUMMARY,
        "reproduction_command_summary": SONYA_ADAPTER_SMOKE_COMMAND,
        "claim_allowed": "SONYA-ADAPTER-SMOKE-00 demonstrates fixture-only adapter contract exercise: adapter selection, consent and capability checks, Sonya gateway requirement, raw-output rejection, candidate-packet requirement, failure receipt emission, telemetry event emission, and provenance event emission without live adapter execution or network/provider calls. Sonya Adapter Smoke exercises contracts, not live adapters.",
        "claims_blocked": SONYA_ADAPTER_SMOKE_CLAIMS_BLOCKED,
        "reviewer_caution": "SONYA-ADAPTER-SMOKE-00 exercises contracts only. It does not execute adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy.",
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
    "Sonya Adapter Smoke exercises contracts, not live adapters.",
    "Sonya Adapter Smoke is not adapter execution.",
    "Sonya Adapter Smoke is not live adapter execution.",
    "Sonya Adapter Smoke is not network authorization.",
    "Sonya Adapter Smoke is not remote provider call.",
    "Sonya Adapter Smoke is not live model execution.",
    "Sonya Adapter Smoke keeps raw output rejected or absent.",
    "Sonya Adapter Smoke requires a candidate packet.",
    "Sonya Adapter Smoke makes failure receipts visible.",
    "Sonya Adapter Smoke makes telemetry events visible.",
    "Sonya Adapter Smoke makes provenance events visible.",
    "Sonya Adapter Smoke is not model weight training.",
    "Sonya Adapter Smoke is not memory write.",
    "Sonya Adapter Smoke is not final answer release.",
    "Sonya Adapter Smoke is not deployment authority.",
    "Sonya Adapter Smoke is not truth certification.",
    "Sonya Adapter Smoke is not hallucination reduction proof.",
    "Sonya Adapter Smoke is not recursive self-improvement.",
    "Sonya Adapter Smoke is not production readiness.",
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
]
GLOBAL_NON_CLAIMS = [
    "not truth certification",
    "not deployment authority",
    "not final answer release",
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
                {"name": "Sonya Adapter Smoke acceptance", "command": SONYA_ADAPTER_SMOKE_COMMAND},
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
            "SONYA-ADAPTER-SMOKE-00": SONYA_ADAPTER_SMOKE_ARTIFACTS,
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
        "latest_fixture_adapter_contract_smoke": "SONYA-ADAPTER-SMOKE-00",
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
        "index.md": f"# Public Experiment Suite Dashboard\n\nThis dashboard presents accepted evidence for reviewer orientation. It is not truth certification, not deployment authority, not final answer release, local fixture only, and requires external peer review.\n\n## Accepted evidence\n\n| Phase | Repo | Status | What this supports | Reviewer caution |\n| --- | --- | --- | --- | --- |\n{phase_rows}\n\n## Reviewer path\n\nStart with claim boundaries, then read the governed artifact cognition paper, WAVE Rosetta paper, SONYA-AEGIS-SMOKE-02, WAVE family, UNI-02D Sonya gate, and RETRO-LANE-00, Public Utility Alpha, Raw Baseline Comparison, Evidence Review Pack, RW-COMP-01, RW-COMP-02, and Sonya Adapter Smoke pages.\n\n## What this proves\n\nIt proves only that accepted local fixture artifacts and draft publication materials are organized for review.\n\n## What this does not prove\n\nNo oracle posture, no deployment posture, no final-answer posture, no AI consciousness claim, and no universal ontology claim.\n\n## Phase pages\n\n- [SONYA-AEGIS-SMOKE-02](sonya-aegis-smoke-02.md)\n- [WAVE Gold-Physics](wave-gold-physics.md)\n- [UNI-02D Sonya gate](uni02d-sonya-gate.md)\n- [RETRO-LANE-00](retro-lane-00.md)\n- [Public Utility Alpha](public-utility-alpha.md)\n- [Raw Baseline Comparison](raw-baseline-comparison.md)\n- [Evidence Review Pack](evidence-review-pack.md)\n- [RW-COMP-01](rw-comp-01.md)\n- [RW-COMP-02](rw-comp-02.md)\n- [Sonya Adapter Smoke](sonya-adapter-smoke.md)\n- [Governed artifact cognition paper](governed-artifact-cognition-paper.md)\n- [Waveform Rosetta paper](waveform-rosetta-paper.md)\n",
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
        "sonya-adapter-smoke.md": f"""# Sonya Adapter Smoke

Purpose: inspect SONYA-ADAPTER-SMOKE-00 as an accepted fixture-only adapter-contract smoke test. Sonya Adapter Smoke exercises contracts, not live adapters.

Run command:

```powershell
{SONYA_ADAPTER_SMOKE_COMMAND}
```

Evidence: {", ".join(f"`{artifact}`" for artifact in SONYA_ADAPTER_SMOKE_ARTIFACTS)}.

Prerequisite phases: SONYA-ADAPTER-CONTRACT-REGISTRY-01, PROVENANCE-TRAINING-LEDGER-00, UNIVERSAL-STAGE-PIPELINE-00, ARTIFACT-CONTRACT-REGISTRY-01, UNIVERSAL-COMPATIBILITY-MATRIX-00, and SONYA-GW-01.

Claim allowed: SONYA-ADAPTER-SMOKE-00 demonstrates fixture-only adapter contract exercise: adapter selection, consent and capability checks, Sonya gateway requirement, raw-output rejection, candidate-packet requirement, failure receipt emission, telemetry event emission, and provenance event emission without live adapter execution or network/provider calls.

Dashboard summary:

{chr(10).join(f"- {key} = {str(value).lower()}" for key, value in SONYA_ADAPTER_SMOKE_DASHBOARD_SUMMARY.items())}

Claims blocked: {"; ".join(SONYA_ADAPTER_SMOKE_CLAIMS_BLOCKED)}.

Reviewer caution: SONYA-ADAPTER-SMOKE-00 exercises contracts only. It does not execute adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy. It is not network authorization, not remote provider call, not model weight training, not truth certification, not hallucination reduction proof, not recursive self-improvement, and not production readiness.
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
13. Sonya Adapter Smoke

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

PowerShell Sonya Adapter Smoke:

```powershell
{SONYA_ADAPTER_SMOKE_COMMAND}
```

Sonya Adapter Smoke exercises contracts, not live adapters. It inspects fixture-only adapter selection, consent checks, capability checks, Sonya gateway requirements, raw output rejected or absent, candidate packet emission, failure receipts, telemetry events, and provenance events. It is not live adapter execution, not network authorization, not remote provider call, not live model execution, not model weight training, not memory write, not final answer release, not deployment authority, and not production readiness.

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
