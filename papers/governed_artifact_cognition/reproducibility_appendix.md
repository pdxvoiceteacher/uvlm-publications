# Reproducibility Appendix

This appendix lists reviewer commands and expected boundaries. The commands are for local fixture review only and are not truth certification, not deployment authority, not final answer release, not AI consciousness, not recursive Sonya federation, not retrosynthesis runtime, not Omega detection, not live Atlas memory writes, not live Sophia calls, and require external peer review.

## SONYA-AEGIS-SMOKE-02

```powershell
.\experiments\Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened `
  -LogDir C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened_logs `
  -CiMode
```

Legacy accepted harness references retained for reviewer traceability:

- `python/tests/integration/test_sonya_aegis_smoke_02_acceptance_harness.py`
- `python/tests/integration/test_sonya_aegis_publisher_boundary_finalizer.py`

## WAVE Gold-Physics

```powershell
python -m coherence.waveform.family_acceptance `
  --bridge-root C:\UVLM\run_artifacts\wave_gold_physics_family
```

Legacy accepted test reference retained for reviewer traceability: `python/tests/waveform/test_waveform_family_acceptance.py`.

## Experiment suite reproducibility pack

```powershell
python -m coherence.tools.build_experiment_suite_repro_pack --registry experiments/experiment_suite_registry.json --artifacts-root artifacts --out-dir artifacts/experiment_suite_repro_pack --zip
```

Legacy accepted test reference retained for reviewer traceability: `python/tests/integration/test_experiment_suite_repro_pack.py`.

## Public Utility Alpha

```powershell
.\experiments\Run-PUBLIC-UTILITY-ALPHA00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\public_utility_alpha_00_repo `
  -LogDir C:\UVLM\run_artifacts\public_utility_alpha_00_repo_logs `
  -CiMode
```

Expected posture: fixture-only, not live model execution, not live adapter execution, not remote provider calls, not federation, not recursive braid, and not final-answer release.

## Raw Baseline Comparison

```powershell
.\experiments\Run-RAW-BASELINE-COMPARISON00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\raw_baseline_comparison_00 `
  -LogDir C:\UVLM\run_artifacts\raw_baseline_comparison_00_logs `
  -CiMode
```

Expected posture: accepted fixture-only measurement scaffold, not hallucination reduction proof, not model quality benchmark, not model superiority proof, not live model execution, and not remote provider call.

## Evidence Review Pack v0.1

Evidence Review Pack v0.1 is the first product-facing governed review receipt. It consumes Universal Evidence Ingress and UCC Control Profile Selector artifacts. It is AI review that shows its work, not truth certification, not professional advice, not compliance certification, not deployment authority, and not hallucination reduction proof.

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_00 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_00_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Expected posture: fixture-only source-bounded review receipt with unsupported-claim visibility, uncertainty retention, counterevidence preservation, UCC threshold posture, reviewer next actions, and export parity.

## RW-COMP-01

RW-COMP-01 is the first fixture-only raw-vs-governed comparison involving Evidence Review Pack v0.1. It shows review-structure visibility in a deterministic fixture and is a step toward future hallucination-reduction evidence. It is not hallucination-reduction proof yet and not model superiority proof.

```powershell
.\experiments\Run-RW-COMP01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_01 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Expected posture: deterministic fixture-only comparison across raw summary, raw multi-model summary, RAG-style grounded summary, Triadic partial governance, and full Evidence Review Pack v0.1.

## RW-COMP-02

RW-COMP-02 is the first deterministic multi-fixture battery extending RW-COMP-01. It compares raw single-model, raw multi-model, RAG-style grounded, Triadic-without-Phase-6, and full Evidence Review Pack arms across six controlled fixture families. It shows structural visibility improvement in deterministic fixtures and is a step toward future hallucination-reduction evidence. It is not hallucination-reduction proof yet and not model-superiority proof.

```powershell
.\experiments\Run-RW-COMP02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_02 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_02_logs `
  -CiMode
```

Expected posture: accepted deterministic multi-fixture battery with `fixture_count = 6`, `total_rows = 30`, `arm_count_per_fixture = 5`, all fixture arms present, no live model evaluation, no remote provider evaluation, not hallucination reduction proof, and not model superiority proof.

## RETROSYNTHESIS-SANDBOX-CYCLE-01

Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption. Expected posture is accepted bounded candidate repair with missing-evidence requests, claim-map revision candidates, uncertainty-restoration candidates, counterevidence-expansion candidates, next-experiment recommendations, no live model execution, no remote provider call, and no network call. It is not memory write, not final answer release, not Publisher finalization, not deployment authority, not Omega detection, not publication claim authorization, and not recursive self-improvement.

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

## EVIDENCE-REVIEW-PACK-01

Evidence Review Pack second pass is candidate revision, not accepted evidence. Expected posture is accepted second-pass review candidate with revision candidates emitted from bounded retrosynthesis inputs, no live model execution, no remote provider call, and no network call. Structural visibility delta is not hallucination-reduction proof; claim-map revision candidate is not truth certification; uncertainty/counterevidence revision candidate is not canon.

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

## RW-COMP-03

RW-COMP-03 is the first held-out, blinded, pre-registered fixture-scoring scaffold. It extends RW-COMP-02 with held-out fixture IDs, blind arm labels, a scoring rubric, simulated reviewer score packet, statistics plan, statistics packet, and a second-pass Evidence Review Pack candidate arm. RW-COMP-03 is a held-out blinded fixture scaffold, not hallucination reduction proof. It is not model superiority proof, not live model evaluation, not a live human study, and not accepted evidence.

```powershell
.\experiments\Run-RW-COMP03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_03 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_03_logs `
  -CiMode
```

Expected posture: `review_status = accepted_as_heldout_blinded_fixture_scaffold`, `heldout_fixtures_present = true`, `blind_labels_present = true`, `scoring_rubric_present = true`, `statistics_plan_present = true`, `statistics_packet_present = true`, `all_arms_present_for_each_fixture = true`, `second_pass_candidate_arm_present = true`, `candidate_only_boundaries_preserved = true`, `no_human_subject_data_collected = true`, `no_live_human_study_performed = true`, `comparison_is_not_hallucination_reduction_proof = true`, `comparison_is_not_model_superiority_proof = true`, and `promotion_blocked = true`.

## Dashboard validation

```bash
python tools/build_public_repro_dashboard.py --out-dir registry --docs-dir docs/experiment-suite
python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite
```

## Publication validation

```bash
python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json
```


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

SONYA-LOCAL-FIXTURE-ADAPTER-01 is deterministic local-only fixture adapter execution. It consumes SONYA-ADAPTER-CONTRACT-REGISTRY-01 and SONYA-ADAPTER-SMOKE-00, executes fixture_text_model_adapter, fixture_summary_generator_adapter, and local_file_transform_adapter, blocks hash_only_evidence_adapter, remote_provider_placeholder_adapter, browser_placeholder_adapter, atlas_memory_placeholder_adapter, and sophia_route_placeholder_adapter, and emits candidate packets, failure receipts, telemetry events, and provenance events. It rejects or avoids raw output admission and remains not live adapter execution, not network authorization, no remote provider call, not live model execution, not model-weight training, not memory write, not final answer release, and not deployment authority.

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

Observed fixture counts:

- `candidate_packet_count = 3`
- `failure_receipt_count = 6`
- `telemetry_event_count = 52`
- `provenance_event_count = 35`
- `executed_local_adapter_ids = fixture_text_model_adapter, fixture_summary_generator_adapter, local_file_transform_adapter`
- `blocked_adapter_ids = hash_only_evidence_adapter, remote_provider_placeholder_adapter, browser_placeholder_adapter, atlas_memory_placeholder_adapter, sophia_route_placeholder_adapter`
