# Reviewer Quickstart

Read the paper, claim-boundary table, artifact table, and this quickstart before interpreting artifacts. The review posture is local fixture only, not truth certification, not professional advice, not compliance certification, not deployment authority, not final answer release, not hallucination reduction proof, not AI consciousness, not recursive Sonya federation, not retrosynthesis runtime, not Omega detection, not live Atlas memory writes, not live Sophia calls, and requires external peer review.

## How to reproduce Public Utility Alpha

```powershell
.\experiments\Run-PUBLIC-UTILITY-ALPHA00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\public_utility_alpha_00_repo `
  -LogDir C:\UVLM\run_artifacts\public_utility_alpha_00_repo_logs `
  -CiMode
```

Expected posture:

- `demo_status = ready_for_local_review_demo`
- `review_status = accepted_for_local_review_demo`
- `local_fixture_only = true`
- `sonya_required = true`
- `live_model_execution_performed = false`
- `network_call_performed = false`
- `final_answer_release_performed = false`
- `deployment_authority_granted = false`

## How to reproduce RAW-BASELINE-COMPARISON-00

```powershell
.\experiments\Run-RAW-BASELINE-COMPARISON00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\raw_baseline_comparison_00 `
  -LogDir C:\UVLM\run_artifacts\raw_baseline_comparison_00_logs `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_measurement_scaffold`
- `local_fixture_only = true`
- `live_model_execution_performed = false`
- `remote_provider_call_performed = false`
- `network_call_performed = false`
- `not_hallucination_reduction_proof = true`
- `not_model_quality_benchmark = true`
- `promotion_blocked = true`

## How to reproduce Evidence Review Pack v0.1

Evidence Review Pack v0.1 is the first product-facing governed review receipt. It consumes Universal Evidence Ingress and UCC Control Profile Selector artifacts. Evidence Review Pack v0.1 is AI review that shows its work. It is not truth certification, not professional advice, not compliance certification, not deployment authority, and not hallucination reduction proof.

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_00 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_00_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Expected posture:

- `fixture_only = true`
- `source_bounded_review_receipt = true`
- `unsupported_claim_visibility = true`
- `uncertainty_retention_present = true`
- `counterevidence_preserved = true`
- `ucc_threshold_posture_present = true`
- `deployment_authority_granted = false`
- `truth_certification_performed = false`

## How to reproduce RW-COMP-01

RW-COMP-01 is the first fixture-only raw-vs-governed comparison involving Evidence Review Pack v0.1. It shows review-structure visibility in a deterministic fixture and is a step toward future hallucination-reduction evidence. It is not hallucination-reduction proof yet and not model superiority proof.

```powershell
.\experiments\Run-RW-COMP01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_01 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Expected posture:

- `fixture_only = true`
- `deterministic_fixture_comparison = true`
- `review_structure_visibility = true`
- `hallucination_reduction_proof = false`
- `model_superiority_proof = false`

## How to reproduce RW-COMP-02

RW-COMP-02 is the first deterministic multi-fixture battery extending RW-COMP-01. It compares raw, RAG-style, partial-governed, and full Evidence Review Pack arms across six controlled fixture families. It shows structural visibility improvement in deterministic fixtures and is a step toward future hallucination-reduction evidence. It is not hallucination-reduction proof yet and not model-superiority proof.

```powershell
.\experiments\Run-RW-COMP02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_02 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_02_logs `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_multi_fixture_comparison_battery`
- `fixture_count >= 6`
- `all_arms_present_for_each_fixture = true`
- `evidence_review_pack_arm_present_for_each_fixture = true`
- `comparison_is_not_hallucination_reduction_proof = true`
- `comparison_is_not_model_superiority_proof = true`
- `live_model_execution_performed = false`
- `remote_provider_call_performed = false`
- `network_call_performed = false`
- `promotion_blocked = true`

## How to reproduce RETROSYNTHESIS-SANDBOX-CYCLE-01

RETROSYNTHESIS-SANDBOX-CYCLE-01 is the first bounded candidate-repair cycle for incomplete or contradiction-bearing Evidence Review Pack artifacts. Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption. It is not memory write, not final answer release, not Publisher finalization, not deployment authority, not Omega detection, not publication claim authorization, and not recursive self-improvement.

```powershell
.\experiments\Run-RETROSYNTHESIS-SANDBOX-CYCLE01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\retrosynthesis_sandbox_cycle_01 `
  -LogDir C:\UVLM\run_artifacts\retrosynthesis_sandbox_cycle_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_bounded_retrosynthesis_sandbox_cycle`
- `candidate_repair_artifacts_emitted = true`
- `missing_evidence_requests_visible = true`
- `uncertainty_restoration_visible = true`
- `counterevidence_preserved = true`
- `hash_only_evidence_not_interpreted = true`
- `canon_adoption_blocked = true`
- `memory_write_blocked = true`
- `final_answer_release_blocked = true`
- `publisher_finalization_blocked = true`
- `deployment_blocked = true`
- `omega_detection_blocked = true`
- `promotion_blocked = true`
- `live_model_execution_performed = false`
- `remote_provider_call_performed = false`
- `network_call_performed = false`

## How to reproduce EVIDENCE-REVIEW-PACK-01

EVIDENCE-REVIEW-PACK-01 is the first bounded second-pass candidate loop generated from Retrosynthesis Sandbox Cycle repair candidates. Evidence Review Pack second pass is candidate revision, not accepted evidence. It is not canon adoption, not memory write, not final answer release, not Publisher finalization, not deployment authority, not Omega detection, not publication claim authorization, not recursive self-improvement, and not hallucination reduction proof.

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_01 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_second_pass_review_candidate`
- `revision_candidates_emitted = true`
- `retrosynthesis_inputs_bound = true`
- `candidate_only_status_preserved = true`
- `hash_only_evidence_not_interpreted = true`
- `canon_adoption_blocked = true`
- `memory_write_blocked = true`
- `final_answer_release_blocked = true`
- `publisher_finalization_blocked = true`
- `deployment_blocked = true`
- `omega_detection_blocked = true`
- `publication_claim_blocked = true`
- `promotion_blocked = true`
- `live_model_execution_performed = false`
- `remote_provider_call_performed = false`
- `network_call_performed = false`

## How to reproduce RW-COMP-03

RW-COMP-03 is a held-out blinded fixture scaffold with simulated scores only. It extends RW-COMP-02 with held-out fixture IDs, blind labels, a scoring rubric, simulated reviewer score packet, statistics plan, statistics packet, and second-pass Evidence Review Pack candidate arm. It is not hallucination reduction proof, not model superiority proof, not live model evaluation, not a live human study, and not accepted evidence.

```powershell
.\experiments\Run-RW-COMP03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_03 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_03_logs `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_heldout_blinded_fixture_scaffold`
- `heldout_fixtures_present = true`
- `blind_labels_present = true`
- `scoring_rubric_present = true`
- `statistics_plan_present = true`
- `statistics_packet_present = true`
- `all_arms_present_for_each_fixture = true`
- `second_pass_candidate_arm_present = true`
- `candidate_only_boundaries_preserved = true`
- `no_human_subject_data_collected = true`
- `no_live_human_study_performed = true`
- `comparison_is_not_hallucination_reduction_proof = true`
- `comparison_is_not_model_superiority_proof = true`
- `promotion_blocked = true`


## How to reproduce the Universal Architecture Scaffold

The brain runs cognition stages; experiments configure those stages. This reproduces architecture scaffold checks for Universal Stage Pipeline, Artifact Contract Registry, and Universal Compatibility Matrix. It is not product release, not benchmark result, not experiment result, not hallucination reduction proof, and not deployment authority.

```powershell
python -m pytest -q python/tests/pipeline/test_universal_stage_pipeline.py
```

```powershell
python -m pytest -q python/tests/integration/test_artifact_contract_registry.py
```

```powershell
.\experiments\Run-UNIVERSAL-COMPATIBILITY-MATRIX00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\universal_compatibility_matrix_00 `
  -LogDir C:\UVLM\run_artifacts\universal_compatibility_matrix_00_logs `
  -CiMode
```

Expected:

- `review_status = accepted_as_universal_compatibility_scaffold`
- `all_required_stage_ids_present = true`
- `all_required_input_classes_present = true`
- `all_required_control_profiles_present = true`
- `unsupported_inputs_failed_closed_or_hash_only = true`
- `hash_only_inputs_not_semantically_interpreted = true`
- `model_facing_stages_require_sonya = true`
- `no_experiment_specific_kernel_logic_used = true`
- `failure_receipts_visible = true`
- `promotion_blocked = true`


## How to reproduce SONYA-ADAPTER-CONTRACT-REGISTRY-01

Adapter capability is not adapter authorization. SONYA-ADAPTER-CONTRACT-REGISTRY-01 is a fixture-only versioned adapter-contract scaffold. All adapters remain disabled or blocked; no live adapter execution occurred; no network calls occurred; raw output is forbidden; candidate packets are required; failure receipts are required; provenance-training policy is present. This is not adapter execution, not network authorization, not remote provider call, not model-weight training, not deployment authority, and not production readiness.

```powershell
.\experiments\Run-SONYA-ADAPTER-CONTRACT-REGISTRY01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_adapter_contract_registry_01 `
  -LogDir C:\UVLM\run_artifacts\sonya_adapter_contract_registry_01_logs `
  -CiMode
```

Expected:

- `review_status = accepted_as_adapter_contract_registry_only`
- `all_adapters_disabled_or_blocked = true`
- `no_live_adapter_execution = true`
- `no_network_calls = true`
- `no_remote_provider_calls = true`
- `sonya_gateway_required = true`
- `raw_output_forbidden = true`
- `candidate_packet_required = true`
- `failure_receipts_required = true`
- `provenance_training_policy_present = true`
- `promotion_blocked = true`

## How to reproduce SONYA-ADAPTER-SMOKE-00

Sonya Adapter Smoke exercises contracts, not live adapters. SONYA-ADAPTER-SMOKE-00 is a fixture-only adapter-contract smoke test that consumes SONYA-ADAPTER-CONTRACT-REGISTRY-01. It exercises adapter selection, consent checks, capability checks, Sonya gateway requirement, raw-output rejection, candidate-packet requirement, failure receipts, telemetry events, and provenance events. It is not adapter execution, not live adapter execution, not network authorization, no remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, not model-weight training, and not hallucination reduction proof.

```powershell
.\experiments\Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_adapter_smoke_00 `
  -LogDir C:\UVLM\run_artifacts\sonya_adapter_smoke_00_logs `
  -CiMode
```

Expected:

- `review_status = accepted_as_fixture_adapter_contract_smoke`
- `adapter_contract_registry_bound = true`
- `all_adapters_disabled_or_blocked_or_fixture_only = true`
- `no_live_adapter_execution = true`
- `no_network_calls = true`
- `no_remote_provider_calls = true`
- `no_live_model_execution = true`
- `raw_output_rejected_or_absent = true`
- `candidate_packet_emitted_for_fixture_model = true`
- `failure_receipts_visible = true`
- `telemetry_events_visible = true`
- `provenance_events_visible = true`
- `model_weight_training_blocked = true`
- `memory_write_blocked = true`
- `final_answer_release_blocked = true`
- `deployment_blocked = true`
- `promotion_blocked = true`

## How to reproduce SONYA-LOCAL-FIXTURE-ADAPTER-01

Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters. SONYA-LOCAL-FIXTURE-ADAPTER-01 is deterministic local-only fixture adapter execution under Sonya adapter contracts. It emits candidate packets, failure receipts, telemetry events, and provenance events while remaining not live adapter execution, not network authorization, no remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, not model-weight training, and not hallucination reduction proof.

```powershell
.\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_01 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_01_logs `
  -CiMode
```

Expected:

- `review_status = accepted_as_local_fixture_adapter_execution`
- `adapter_contract_registry_bound = true`
- `adapter_smoke_bound = true`
- `local_fixture_adapter_execution_performed = true`
- `no_live_adapter_execution = true`
- `no_network_calls = true`
- `no_remote_provider_calls = true`
- `no_live_model_execution = true`
- `raw_output_rejected_or_absent = true`
- `candidate_packets_emitted = true`
- `failure_receipts_visible = true`
- `telemetry_events_visible = true`
- `provenance_events_visible = true`
- `model_weight_training_blocked = true`
- `memory_write_blocked = true`
- `final_answer_release_blocked = true`
- `deployment_blocked = true`
- `promotion_blocked = true`

## How to reproduce EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01

Adapter output is not accepted as cognition directly. Local adapter candidates become reviewable only through the Evidence Review Pack path. Candidate packets require UCC-controlled review. The claim map is not truth certification. The candidate is not final answer.

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_01 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_01_logs `
  -CiMode
```

Expected:

- `review_status = accepted_as_local_adapter_candidate_review`
- `local_adapter_candidate_bound = true`
- `evidence_review_pack_path_used = true`
- `ucc_control_profile_applied = true`
- `candidate_packet_reviewed = true`
- `raw_output_rejected_or_absent = true`
- `unsupported_claims_listed = true`
- `uncertainty_preserved_or_flagged = true`
- `provenance_events_visible = true`
- `model_weight_training_blocked = true`
- `memory_write_blocked = true`
- `final_answer_release_blocked = true`
- `deployment_blocked = true`
- `promotion_blocked = true`

## How to reproduce SONYA-LOCAL-FIXTURE-ADAPTER-02

Selection policy is not final answer. Multi-adapter local fixture selection still requires Evidence Review Pack review. Candidate comparison is not model quality benchmark. Selection is not adapter authorization.

```powershell
.\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_02 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_02_logs `
  -CiMode
```

Expected:

- `review_status = accepted_as_multi_adapter_local_fixture_route`
- `local_adapter_candidates_compared = true`
- `selection_policy_applied = true`
- `selected_candidate_requires_review = true`
- `evidence_review_pack_path_required = true`
- `raw_output_rejected_or_absent = true`
- `live_adapter_execution_blocked = true`
- `network_calls_blocked = true`
- `remote_provider_calls_blocked = true`
- `model_weight_training_blocked = true`
- `memory_write_blocked = true`
- `final_answer_release_blocked = true`
- `deployment_blocked = true`
- `promotion_blocked = true`
- `candidate_count = 3`
- `selected_candidate_id = candidate-fixture-summary`
- `selected_candidate_source_adapter_id = fixture_summary_generator_adapter`
- `executed_local_adapter_ids = fixture_text_model_adapter, fixture_summary_generator_adapter, local_file_transform_adapter`
- `blocked_adapter_ids = hash_only_evidence_adapter, remote_provider_placeholder_adapter, browser_placeholder_adapter, atlas_memory_placeholder_adapter, sophia_route_placeholder_adapter`

## Other accepted local commands

```powershell
.\experiments\Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened `
  -LogDir C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened_logs `
  -CiMode
```

```powershell
python -m coherence.waveform.family_acceptance `
  --bridge-root C:\UVLM\run_artifacts\wave_gold_physics_family
```

Legacy accepted harness references retained for reviewer traceability:

- `python/tests/integration/test_sonya_aegis_smoke_02_acceptance_harness.py`
- `python/tests/integration/test_sonya_aegis_publisher_boundary_finalizer.py`
- `python/tests/integration/test_experiment_suite_repro_pack.py`
- `python/tests/waveform/test_waveform_family_acceptance.py`
- `python -m coherence.tools.build_experiment_suite_repro_pack`

## Dashboard checks

```bash
python tools/build_public_repro_dashboard.py --out-dir registry --docs-dir docs/experiment-suite
python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite
```

## Interpretation reminders

- Sonya Gateway candidate packet is not answer.
- Runtime bypass block is not model output.
- Model braid is observational only, not consensus proof and not answer selection.
- UNI-02D-SONYA-GATE-01 is accepted as a safe generic portability/prior-quarantine fixture, but it is not universal portability proof.
- RETRO-LANE-00 is accepted as retrosynthesis admission policy, not retrosynthesis runtime.
- Evidence Review Pack v0.1 is the first product-facing governed review receipt and AI review that shows its work, not truth certification, not professional advice, not compliance certification, not deployment authority, and not hallucination reduction proof.
- RW-COMP-01 is the first fixture-only raw-vs-governed comparison involving Evidence Review Pack v0.1; it shows review-structure visibility in a deterministic fixture and is a step toward future hallucination-reduction evidence, not hallucination-reduction proof yet and not model superiority proof.
- RW-COMP-02 is the first deterministic multi-fixture battery extending RW-COMP-01; it shows structural visibility improvement in deterministic fixtures, not hallucination-reduction proof yet and not model-superiority proof.
- RETROSYNTHESIS-SANDBOX-CYCLE-01 is accepted as bounded candidate repair over incomplete Evidence Review Pack artifacts; it is not canon adoption, not memory write, not final answer release, not Publisher finalization, not deployment authority, not Omega detection, not publication claim authorization, and not recursive self-improvement.
- EVIDENCE-REVIEW-PACK-01 is candidate revision, not accepted evidence; structural visibility delta is not hallucination-reduction proof, claim-map revision candidate is not truth certification, and uncertainty/counterevidence revision candidate is not canon.
- RW-COMP-03 is a held-out blinded fixture scaffold with simulated scores only; it is not hallucination reduction proof, not model superiority proof, not live model evaluation, not a live human study, and not accepted evidence.
