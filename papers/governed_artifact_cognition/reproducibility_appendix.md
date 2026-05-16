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

## How to reproduce EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01

EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 routes Sonya local fixture adapter candidates into Evidence Review Pack. It consumes SONYA-LOCAL-FIXTURE-ADAPTER-01, binds fixture_summary_generator_adapter candidate output to review, applies a UCC control profile, emits an adapter candidate binding packet, emits a local-adapter claim map, emits provenance events, lists unsupported claims, and flags uncertainty. Adapter output is not accepted as cognition directly. It is not accepted evidence, not adapter authorization, not memory write, not final answer release, not deployment authority, not model-weight training, and not hallucination reduction proof.

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

SONYA-LOCAL-FIXTURE-ADAPTER-02 compares multiple deterministic local fixture adapter candidates, applies a selection policy, selects candidate-fixture-summary from fixture_summary_generator_adapter, and records that the selected candidate still requires Evidence Review Pack route. Selection is not final answer and not adapter authorization. Candidate comparison is not model quality benchmark. No live/network/provider/memory/final/deployment authority is granted.

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


## How to reproduce SONYA-LOCAL-FIXTURE-ADAPTER-03

SONYA-LOCAL-FIXTURE-ADAPTER-03 is a methods-lineage clarity phase only. Nested SONYA-LOCAL-FIXTURE-ADAPTER-01 references are source fixture dependencies, not stale identity leakage. Current route identity is explicit. Source fixture identity is explicit. Evidence Review Pack local-adapter route references are explicit. Lineage does not grant authority.

```powershell
.\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_03 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_03_logs `
  -CiMode
```

Review `sonya_local_adapter_lineage_packet.json`, `sonya_local_adapter_lineage_review_packet.json`, and `sonya_local_fixture_adapter_03_acceptance_receipt.json`. The packet is lineage clarity only: not adapter execution, not memory write, not final answer release, and not deployment authority.


## How to reproduce EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02

EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02 is a local-only candidate revision loop. The revise_summary recommendation was consumed, a revised candidate was emitted, Evidence Review Pack rerun occurred, and deltas were reported. Deltas are structural review descriptors, not hallucination reduction proof. The revised local adapter candidate remains candidate-only, not accepted evidence.

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_02 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_02_logs `
  -CiMode
```

Review `evidence_review_local_adapter_revision_packet.json`, `evidence_review_local_adapter_revision_delta.json`, and `evidence_review_pack_local_adapter_02_acceptance_receipt.json`. Expected deltas include `unsupported_claim_count_delta = -1`, `uncertainty_missing_count_delta = -1`, `source_reference_visibility_delta = 1`, and `structural_visibility_improved_candidate = true`. The revised candidate is not final answer selection, not model quality benchmark, not memory write, not model-weight training, and not deployment authority.


## How to reproduce RW-COMP-LOCAL-ADAPTER-01

RW-COMP-LOCAL-ADAPTER-01 compares raw local summary fixture, original local adapter candidate, Evidence Review Pack reviewed original candidate, revised local adapter candidate, and Evidence Review Pack reviewed revised candidate. Deltas are structural review descriptors only. RW-COMP local-adapter comparison is not hallucination reduction proof or a model quality benchmark. Candidate comparison is not final answer selection and candidate remains not accepted evidence.

```powershell
.\experiments\Run-RW-COMP-LOCAL-ADAPTER01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_local_adapter_01 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_local_adapter_01_logs `
  -CiMode
```

Review `rw_comp_local_adapter_packet.json`, `rw_comp_local_adapter_delta_packet.json`, and `rw_comp_local_adapter_01_acceptance_receipt.json`. Expected deltas include `unsupported_claim_count_delta = -1`, `uncertainty_missing_count_delta = -1`, `source_reference_visibility_delta = 1`, `supported_claim_count_delta = 2`, and `structural_visibility_improved_candidate = true`. No model-weight training, no memory write, no final-answer release, no deployment, and no promotion is authorized.


## How to reproduce PMR-00-PROVENANCE-MEMORY-RESERVOIR

Memory is governed provenance under resource constraints. PMR-00 records local-only doctrine and storage policy. Memory is not storage. Hash is not encryption. User controls local memory budget. Federation is blocked by default. PMR is not Atlas canon and not model-weight training data.

```powershell
.\experiments\Run-PMR00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_00_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

Review `pmr_doctrine_packet.json`, `pmr_local_storage_policy.json`, and `pmr_00_acceptance_receipt.json`.

## How to reproduce PMR-01-LOCAL-ARTIFACT-INDEX

PMR artifact lifecycle state is not truth status. PMR artifact index is not generic cache. Dependency graph is not canon graph. No pruning occurs in PMR-01. PMR-01 performs indexing only, not pruning.

```powershell
.\experiments\Run-PMR01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_01 `
  -LogDir C:\UVLM\run_artifacts\pmr_01_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

Review `pmr_local_artifact_index.json`, `pmr_dependency_graph.json`, and `pmr_01_acceptance_receipt.json`. These are PMR architecture scaffold artifacts only: not Atlas canon, not memory write authorization, not model-weight training, not federation authorization, not pruning execution, not truth certification, and not deployment authority.

## PMR-02 Global Provenance Coherence Utility

PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY adds a publication-indexed PMR utility scoring scaffold for local PMR-indexed artifacts. GPCU is lifecycle/storage utility, not truth score. GPCU is not reward entitlement. GPCU is not token economy. GPCU is not human value score. Lifecycle recommendation is not pruning. Reward mechanics are deferred. Federation remains blocked by default.

PMR-02 scores local PMR-indexed artifacts for lifecycle/storage utility and emits lifecycle recommendations while preserving non-authority boundaries. It is not Atlas canon, not memory write authorization, not model-weight training, not deployment authority, not hallucination reduction proof, not truth certification, not final answer release, not recursive self-improvement, and not production readiness.

### PMR-02 acceptance command

```powershell
.\experiments\Run-PMR02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_02 `
  -LogDir C:\UVLM\run_artifacts\pmr_02_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

## PMR-03 Lifecycle State Machine

PMR-03-LIFECYCLE-STATE-MACHINE adds a publication-indexed PMR lifecycle state-machine scaffold for local PMR-indexed artifacts. Recommendation is not transition. Transition candidate is not action. Lifecycle state is not truth status. No pruning or deletion occurs in PMR-03. Destructive action requires future Sophia lifecycle audit. Destructive action requires future user confirmation. Reward mechanics remain deferred. Federation remains blocked by default.

PMR-03 consumes PMR-00 doctrine/policy, PMR-01 local artifact index/dependency graph, and PMR-02 GPCU lifecycle recommendations. It emits lifecycle transition candidates, transition receipts, and a no-action receipt while preserving non-action and non-authority boundaries. It is not pruning execution, not deletion execution, not federation authorization, not encrypted shard transfer, not reward entitlement, not token economy, not Atlas canon, not memory write authorization, not model-weight training, not deployment authority, not truth certification, not final answer release, not hallucination reduction proof, not recursive self-improvement, and not production readiness.

### PMR-03 acceptance command

```powershell
.\experiments\Run-PMR03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_03 `
  -LogDir C:\UVLM\run_artifacts\pmr_03_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

## PMR-04 Lifecycle Audit Preflight

PMR-04-LIFECYCLE-AUDIT-PREFLIGHT adds a publication-indexed PMR lifecycle audit preflight scaffold for local PMR-indexed artifacts. Preflight is not approval. Audit candidate is not action. Sophia lifecycle audit is required before destructive action. User confirmation is required before destructive local action. No Sophia approval packet is emitted. No pruning or deletion occurs in PMR-04.

PMR-04 consumes PMR-00 doctrine/policy, PMR-01 local artifact index/dependency graph, PMR-02 GPCU lifecycle recommendations, and PMR-03 lifecycle transition candidates/no-action receipts. It emits audit candidates, a block packet, and a no-action receipt while preserving non-approval, non-action, and non-authority boundaries. No federation occurs. No encrypted shard transfer occurs. No reward occurs. No token economy occurs. No memory write occurs. No Atlas canon write occurs. No model-weight training occurs. No deployment occurs. No truth certification occurs. No final-answer release occurs. No hallucination-reduction proof occurs. No recursive self-improvement occurs.

### PMR-04 acceptance command

```powershell
.\experiments\Run-PMR04-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_04 `
  -LogDir C:\UVLM\run_artifacts\pmr_04_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

## PMR-05 Sophia Lifecycle Audit Review

PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW adds a publication-indexed, fixture-only Sophia lifecycle audit review scaffold for local PMR audit candidates. Sophia review is not Sophia approval. Audit recommendation is not action. No Sophia approval packet is emitted. Destructive action requires future Sophia approval. Destructive action requires future user confirmation. No pruning or deletion occurs in PMR-05.

PMR-05 consumes PMR-00 doctrine/policy, PMR-01 local artifact index/dependency graph, PMR-02 GPCU lifecycle recommendations, PMR-03 lifecycle transition candidates/no-action receipts, and PMR-04 lifecycle audit preflight candidates/block packet/no-action receipt. It emits fixture-only Sophia lifecycle audit review rows, a recommendation packet, and a no-approval receipt while preserving no-approval and no-action boundaries. No federation occurs. No encrypted shard transfer occurs. No reward occurs. No token economy occurs. No memory write occurs. No Atlas canon write occurs. No model-weight training occurs. No deployment occurs. No truth certification occurs. No final-answer release occurs. No hallucination-reduction proof occurs. No recursive self-improvement occurs.

### PMR-05 acceptance command

```powershell
.\experiments\Run-PMR05-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_05 `
  -LogDir C:\UVLM\run_artifacts\pmr_05_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```
## PMR-06 User Confirmation Preflight

PMR-06-USER-CONFIRMATION-PREFLIGHT adds a publication-indexed, fixture-only user confirmation request preflight scaffold for PMR lifecycle recommendations. User confirmation request is not user confirmation. User confirmation is not action. No user confirmation receipt is emitted. Destructive action requires future Sophia approval. Destructive action requires future user confirmation. No pruning or deletion occurs in PMR-06.

PMR-06 consumes PMR-00 doctrine/policy, PMR-01 local artifact index/dependency graph, PMR-02 GPCU lifecycle recommendations, PMR-03 lifecycle transition candidates/no-action receipts, PMR-04 lifecycle audit preflight candidates/block packet/no-action receipt, and PMR-05 fixture-only Sophia lifecycle audit review recommendations/no-approval receipt. It emits user confirmation request candidates, prompt packets, block packets, and a no-action receipt while preserving no-confirmation and no-action boundaries. No federation occurs. No encrypted shard transfer occurs. No reward occurs. No token economy occurs. No memory write occurs. No Atlas canon write occurs. No model-weight training occurs. No deployment occurs. No truth certification occurs. No final-answer release occurs. No hallucination-reduction proof occurs. No recursive self-improvement occurs.

### PMR-06 acceptance command

```powershell
.\experiments\Run-PMR06-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_06 `
  -LogDir C:\UVLM\run_artifacts\pmr_06_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```
## PMR-07 User Confirmation Negative Control

PMR-07-USER-CONFIRMATION-NEGATIVE-CONTROL adds a publication-indexed negative-control scaffold for user confirmation attempts across PMR lifecycle recommendations. Invalid confirmation is not confirmation. Missing confirmation is not confirmation. Forged confirmation is not confirmation. Expired confirmation is not confirmation. Scope-mismatched confirmation is not confirmation. Confirmation without Sophia approval is insufficient. Confirmation cannot override retain-lock, quarantine, revocation, or dependency blocks. No user confirmation receipt is emitted. No pruning or deletion occurs in PMR-07.

PMR-07 consumes PMR-00 through PMR-06 artifacts and emits invalid user confirmation attempts, a block packet, a no-action receipt, and a negative-control review packet. Missing, ambiguous, forged, expired, wrong-artifact, wrong-action, wrong-principal, scope-mismatched, post-revocation, quarantined, retain-locked, dependency-blocked, or Sophia-approval-missing confirmation attempts fail closed and cannot authorize destructive PMR action. No federation occurs. No encrypted shard transfer occurs. No reward occurs. No token economy occurs. No memory write occurs. No Atlas canon write occurs. No model-weight training occurs. No deployment occurs. No truth certification occurs. No final-answer release occurs. No hallucination-reduction proof occurs. No recursive self-improvement occurs.

### PMR-07 acceptance command

```powershell
.\experiments\Run-PMR07-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_07 `
  -LogDir C:\UVLM\run_artifacts\pmr_07_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```
