# Reviewer Quickstart

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
21. PMR GPCU utility scoring
22. PMR lifecycle state machine
23. PMR lifecycle audit preflight
24. Sonya Local Fixture Adapter multi-route

## CoherenceLattice commands

PowerShell SONYA-AEGIS-SMOKE-02:

```powershell
.\experiments\Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened `
  -LogDir C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened_logs `
  -CiMode
```

PowerShell WAVE Gold-Physics:

```powershell
python -m coherence.waveform.family_acceptance `
  --bridge-root C:\UVLM\run_artifacts\wave_gold_physics_family
```

PowerShell UNI-02D Sonya gate:

```powershell
.\experiments\Run-UNI02D-Sonya-Gate-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\uni02d_sonya_gate `
  -LogDir C:\UVLM\run_artifacts\uni02d_sonya_gate_logs `
  -CiMode
```

PowerShell RETRO-LANE-00:

```powershell
.\experiments\Run-RETRO-LANE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\retro_lane_00 `
  -LogDir C:\UVLM\run_artifacts\retro_lane_00_logs `
  -CiMode
```

PowerShell Public Utility Alpha:

```powershell
.\experiments\Run-PUBLIC-UTILITY-ALPHA00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\public_utility_alpha_00_repo `
  -LogDir C:\UVLM\run_artifacts\public_utility_alpha_00_repo_logs `
  -CiMode
```

PowerShell Raw Baseline Comparison:

```powershell
.\experiments\Run-RAW-BASELINE-COMPARISON00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\raw_baseline_comparison_00 `
  -LogDir C:\UVLM\run_artifacts\raw_baseline_comparison_00_logs `
  -CiMode
```

PowerShell Evidence Review Pack:

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_00 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_00_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Evidence Review Pack v0.1 is AI review that shows its work. It is not legal advice, not medical advice, not tax advice, and not compliance certification.

PowerShell RW-COMP-01:

```powershell
.\experiments\Run-RW-COMP01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_01 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

RW-COMP-01 is a fixture-only comparison scaffold, not hallucination reduction proof. It is not model superiority proof, not professional advice, not compliance certification, and not production evaluation.

PowerShell RW-COMP-02:

```powershell
.\experiments\Run-RW-COMP02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_02 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_02_logs `
  -CiMode
```

RW-COMP-02 is a deterministic multi-fixture comparison battery and remains not hallucination reduction proof. It is not model superiority proof, not professional advice, not compliance certification, and not production evaluation.

PowerShell Retrosynthesis Sandbox Cycle:

```powershell
.\experiments\Run-RETROSYNTHESIS-SANDBOX-CYCLE01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\retrosynthesis_sandbox_cycle_01 `
  -LogDir C:\UVLM\run_artifacts\retrosynthesis_sandbox_cycle_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption. It is not memory write, not final answer release, not Publisher finalization, not Omega detection, not deployment authority, and not recursive self-improvement.

PowerShell Evidence Review Pack second pass:

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_01 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_01_logs `
  -ControlProfileId generic_evidence_review.v1 `
  -CiMode
```

Evidence Review Pack second pass is candidate revision, not accepted evidence. It is not canon adoption, not memory write, not final answer release, not Publisher finalization, not Omega detection, not deployment authority, not hallucination reduction proof, and not recursive self-improvement.

PowerShell RW-COMP-03:

```powershell
.\experiments\Run-RW-COMP03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_03 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_03_logs `
  -CiMode
```

RW-COMP-03 is a held-out blinded fixture scaffold with simulated scores and a statistics plan. It includes a second-pass candidate arm and is a step toward future hallucination-reduction evidence, not hallucination reduction proof, not model superiority proof, not live model evaluation, and not live human study.


## Universal Architecture Scaffold

The brain runs cognition stages; experiments configure those stages.

Universal Architecture Scaffold covers UNIVERSAL-STAGE-PIPELINE-00, ARTIFACT-CONTRACT-REGISTRY-01, and UNIVERSAL-COMPATIBILITY-MATRIX-00. Profiles are configuration, experiments are configurations, and unsupported inputs are preserved with fail-closed receipts or hash-only receipts instead of semantic interpretation.

Universal Stage Pipeline:

```powershell
python -m pytest -q python/tests/pipeline/test_universal_stage_pipeline.py
```

Artifact Contract Registry:

```powershell
python -m pytest -q python/tests/integration/test_artifact_contract_registry.py
```

Universal Compatibility Matrix:

```powershell
.\experiments\Run-UNIVERSAL-COMPATIBILITY-MATRIX00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\universal_compatibility_matrix_00 `
  -LogDir C:\UVLM\run_artifacts\universal_compatibility_matrix_00_logs `
  -CiMode
```

This scaffold is not product release, not experiment result, not benchmark result, not hallucination reduction proof, not deployment authority, and not recursive self-improvement.


## Sonya Adapter Contract Registry

Adapter capability is not adapter authorization.

Sonya Adapter Contract Registry covers SONYA-ADAPTER-CONTRACT-REGISTRY-01. Adapter contracts are versioned configuration. All adapters disabled or blocked means not adapter execution and not network authorization; raw output is forbidden, candidate packet required, failure receipts required, and provenance-training policy is present.

```powershell
.\experiments\Run-SONYA-ADAPTER-CONTRACT-REGISTRY01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_adapter_contract_registry_01 `
  -LogDir C:\UVLM\run_artifacts\sonya_adapter_contract_registry_01_logs `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_adapter_contract_registry_only`
- `adapter_count = 11`
- `disabled_or_blocked_adapter_count = 11`
- `enabled_live_adapter_count = 0`
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

This scaffold is not adapter execution, not live model execution, not remote provider call, not network authorization, not memory write, not final answer release, not deployment authority, not truth certification, not model weight training, not hallucination reduction proof, not recursive self-improvement, and not production readiness.

## Sonya Adapter Smoke

Sonya Adapter Smoke exercises contracts, not live adapters.

Sonya Adapter Smoke covers SONYA-ADAPTER-SMOKE-00 as an accepted fixture-only adapter-contract smoke test. It exercises adapter selection, consent checks, capability checks, Sonya gateway requirements, raw output rejected or absent posture, candidate packet requirement, failure receipts, telemetry events, and provenance events. Boundary posture: not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, and not model weight training.

```powershell
.\experiments\Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_adapter_smoke_00 `
  -LogDir C:\UVLM\run_artifacts\sonya_adapter_smoke_00_logs `
  -CiMode
```

Expected posture:

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

This smoke test is not adapter execution, not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, not truth certification, not model weight training, not hallucination reduction proof, not recursive self-improvement, and not production readiness.

## Sonya Local Fixture Adapter

Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters.

SONYA-LOCAL-FIXTURE-ADAPTER-01 covers accepted local-only fixture adapter execution under Sonya adapter contracts. Deterministic local fixture adapters emitted candidate packets, failure receipts, telemetry events, and provenance events. Boundary posture: not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, and not model weight training.

```powershell
.\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_01 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_01_logs `
  -CiMode
```

Expected posture:

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
- `candidate_packet_count = 3`
- `failure_receipt_count = 6`
- `telemetry_event_count = 52`
- `provenance_event_count = 35`
- `executed_local_adapter_ids = ['fixture_text_model_adapter', 'fixture_summary_generator_adapter', 'local_file_transform_adapter']`
- `blocked_adapter_ids = ['hash_only_evidence_adapter', 'remote_provider_placeholder_adapter', 'browser_placeholder_adapter', 'atlas_memory_placeholder_adapter', 'sophia_route_placeholder_adapter']`

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-01 executes deterministic local fixture adapters only. It does not execute live adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy. It is not truth certification, not hallucination reduction proof, not recursive self-improvement, and not production readiness.

## Evidence Review Pack local adapter

Adapter output is not accepted as cognition directly.

EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 routes Sonya local fixture adapter candidates into Evidence Review Pack. Candidate packets require UCC-controlled review. The claim map is not truth certification. The candidate is not final answer. No memory write is authorized. No deployment is authorized. No network authorization is granted. No provider call is made. No model-weight training is authorized. No hallucination-reduction proof is authorized.

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_01 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_01_logs `
  -CiMode
```

Expected posture:

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

Reviewer caution: EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01 routes a local fixture adapter candidate into review only. It is not accepted evidence, not adapter authorization, not memory write, not final answer release, not deployment authority, not truth certification, not model weight training, not hallucination reduction proof, and not recursive self-improvement.

## Evidence Review Pack local adapter revision

Deltas are structural review descriptors, not hallucination reduction proof.

EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02 consumes the revise_summary recommendation, emits a revised candidate, reruns Evidence Review Pack review, and reports candidate-level structural review deltas. The revised candidate is not final answer and not accepted evidence.

```powershell
.\experiments\Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_02 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_pack_local_adapter_02_logs `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_local_adapter_revision_loop`
- `revise_summary_recommendation_consumed = true`
- `revised_candidate_emitted = true`
- `evidence_review_rerun_performed = true`
- `deltas_reported = true`
- `unsupported_claim_delta_reported = true`
- `uncertainty_missing_delta_reported = true`
- `candidate_remains_not_final_answer = true`
- `candidate_remains_not_accepted_evidence = true`
- `model_weight_training_blocked = true`
- `memory_write_blocked = true`
- `final_answer_release_blocked = true`
- `deployment_blocked = true`
- `promotion_blocked = true`
- `unsupported_claim_count_delta = -1`
- `uncertainty_missing_count_delta = -1`
- `source_reference_visibility_delta = 1`
- `structural_visibility_improved_candidate = true`

Reviewer caution: EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02 reports candidate-level structural review deltas only. It does not prove hallucination reduction, benchmark model quality, select a final answer, accept evidence, authorize adapters, write memory, train models, or deploy.

## Provenance Memory Reservoir

Memory is governed provenance under resource constraints.

PMR-00-PROVENANCE-MEMORY-RESERVOIR establishes local-only PMR doctrine and storage policy. Memory is not storage. Hash is not encryption. User controls local memory budget. Federation is blocked by default. PMR is not Atlas canon and not model-weight training data.

```powershell
.\experiments\Run-PMR00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_00_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_pmr_doctrine_and_policy_scaffold`
- `local_budget_policy_present = true`
- `retention_classes_present = true`
- `hash_encryption_distinction_present = true`
- `federation_blocked_by_default = true`
- `raw_private_data_federation_blocked = true`
- `model_weight_training_blocked = true`
- `memory_write_blocked = true`
- `canon_adoption_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`

## PMR local artifact index

PMR artifact lifecycle state is not truth status. PMR index is not generic cache. Dependency graph is not canon graph. PMR-01 performs indexing only, not pruning.

```powershell
.\experiments\Run-PMR01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_01 `
  -LogDir C:\UVLM\run_artifacts\pmr_01_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_pmr_local_artifact_index_scaffold`
- `source_pmr_policy_bound = true`
- `artifact_entries_present = true`
- `dependency_graph_present = true`
- `retention_classes_assigned = true`
- `lifecycle_states_assigned = true`
- `hash_encryption_distinction_preserved = true`
- `user_budget_policy_preserved = true`
- `federation_blocked_by_default = true`
- `pruning_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `artifact_count = 8`
- `node_count = 8`
- `edge_count = 9`
- `revocation_backpropagation_supported = true`
- `pruning_dependency_checks_supported = true`
- `graph_is_not_truth_graph = true`
- `graph_is_not_canon_graph = true`

## PMR GPCU utility scoring

GPCU is lifecycle/storage utility, not truth score. PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY emits lifecycle recommendations. Lifecycle recommendation is not pruning. Reward mechanics are deferred. Federation remains blocked by default.

```powershell
.\experiments\Run-PMR02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_02 `
  -LogDir C:\UVLM\run_artifacts\pmr_02_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_pmr_utility_scoring_scaffold`
- `source_pmr_policy_bound = true`
- `source_pmr_index_bound = true`
- `utility_scores_present = true`
- `lifecycle_recommendations_present = true`
- `scoring_dimensions_present = true`
- `gpcu_not_truth_score = true`
- `gpcu_not_reward_entitlement = true`
- `gpcu_not_pruning_execution = true`
- `gpcu_not_federation_authorization = true`
- `lifecycle_recommendations_not_actions = true`
- `hash_encryption_distinction_preserved = true`
- `user_budget_policy_preserved = true`
- `federation_blocked_by_default = true`
- `pruning_not_performed = true`
- `reward_actions_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `artifact_count = 8`
- `scored_artifact_count = 8`
- `pmr00_doctrine_utility_band = retain_locked`
- `pmr00_policy_utility_band = retain_locked`
- `pmr00_retention_utility_band = retain_priority`
- `rw_comp_local_adapter_anchor_utility_band = retain_priority`
- `ephemeral_summary_utility_band = compress_candidate`
- `revoked_hash_tombstone_utility_band = revoked`
- `quarantine_example_utility_band = quarantine`

Reviewer caution: PMR-02 computes lifecycle/storage utility scores and recommendations only. It does not prune artifacts. GPCU is not reward entitlement and not token economy. It does not certify truth. It does not authorize federation. It does not write memory, train models, deploy, or assign human value.

## PMR lifecycle state machine

Recommendation is not transition; transition candidate is not action. PMR-03-LIFECYCLE-STATE-MACHINE emits lifecycle transition candidates, transition receipts, and a no-action receipt. Lifecycle state is not truth status. No pruning or deletion occurs in PMR-03. Destructive action requires future Sophia lifecycle audit. Destructive action requires future user confirmation. Reward mechanics remain deferred. Federation remains blocked by default.

```powershell
.\experiments\Run-PMR03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_03 `
  -LogDir C:\UVLM\run_artifacts\pmr_03_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_pmr_lifecycle_state_machine_scaffold`
- `source_pmr_policy_bound = true`
- `source_pmr_index_bound = true`
- `source_pmr_utility_bound = true`
- `transition_candidates_present = true`
- `transition_receipts_present = true`
- `no_action_receipt_present = true`
- `recommendation_not_transition = true`
- `transition_candidate_not_action = true`
- `lifecycle_state_not_truth_status = true`
- `destructive_action_requires_future_sophia_audit = true`
- `destructive_action_requires_future_user_confirmation = true`
- `pruning_not_performed = true`
- `deletion_not_performed = true`
- `federation_blocked_by_default = true`
- `reward_actions_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `artifact_count = 8`
- `transition_candidate_count = 8`
- `transition_receipt_count = 8`
- `action_performed = false`
- `encrypted_shard_transfer_performed = false`
- `token_economy_performed = false`
- `network_calls_performed = false`

Reviewer caution: PMR-03 emits lifecycle transition candidates and no-action receipts only. It does not prune, delete, federate, transfer encrypted shards, reward users, run a token economy, write memory, train models, deploy, or certify truth. Destructive action requires future Sophia lifecycle audit and user confirmation.

## PMR lifecycle audit preflight

Preflight is not approval. PMR-04-LIFECYCLE-AUDIT-PREFLIGHT emits audit candidates, a block packet, and a no-action receipt. Audit candidate is not action. Sophia lifecycle audit is required before destructive action. User confirmation is required before destructive local action. No Sophia approval packet is emitted. No pruning or deletion occurs in PMR-04. No federation occurs. No encrypted shard transfer occurs. No reward occurs. No token economy occurs. No memory write occurs. No Atlas canon write occurs. No model-weight training occurs. No deployment occurs. No truth certification occurs. No final-answer release occurs. No hallucination-reduction proof occurs. No recursive self-improvement occurs.

```powershell
.\experiments\Run-PMR04-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_04 `
  -LogDir C:\UVLM\run_artifacts\pmr_04_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_pmr_lifecycle_audit_preflight_scaffold`
- `source_pmr_policy_bound = true`
- `source_pmr_index_bound = true`
- `source_pmr_utility_bound = true`
- `source_pmr_lifecycle_bound = true`
- `audit_candidates_present = true`
- `block_packet_present = true`
- `no_action_receipt_present = true`
- `recommendation_not_transition = true`
- `transition_candidate_not_action = true`
- `preflight_not_approval = true`
- `lifecycle_state_not_truth_status = true`
- `destructive_action_requires_future_sophia_audit = true`
- `destructive_action_requires_future_user_confirmation = true`
- `pruning_not_performed = true`
- `deletion_not_performed = true`
- `federation_blocked_by_default = true`
- `reward_actions_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `transition_candidate_count = 8`
- `audit_candidate_count = 8`
- `blocked_candidate_count = 5`
- `no_op_candidate_count = 3`
- `user_confirmation_required_count = 5`
- `sophia_audit_required_count = 4`
- `action_performed = false`
- `sophia_approval_performed = false`
- `encrypted_shard_transfer_performed = false`
- `token_economy_performed = false`
- `network_calls_performed = false`

Reviewer caution: PMR-04 emits lifecycle audit candidates, a block packet, and a no-action receipt only. Preflight is not approval. Audit candidate is not action. It does not prune, delete, federate, transfer encrypted shards, reward users, run a token economy, write memory, write canon, train models, deploy, certify truth, release final answers, prove hallucination reduction, or recursively self-improve. Sophia lifecycle audit and user confirmation are required before destructive local action.

Reviewer caution: PMR-00 and PMR-01 define local provenance-memory doctrine, storage policy, artifact indexing, and dependency graph scaffolds only. They do not write memory, canonize artifacts, federate artifacts, transfer encrypted shards, prune artifacts, train models, certify truth, release final answers, deploy, or reward resource contributions.

## RW-COMP local adapter

Deltas are structural review descriptors only.

RW-COMP-LOCAL-ADAPTER-01 compares raw local summary fixture, original local adapter candidate, Evidence Review Pack reviewed original candidate, revised local adapter candidate, and Evidence Review Pack reviewed revised candidate. Candidate comparison is not final answer selection.

```powershell
.\experiments\Run-RW-COMP-LOCAL-ADAPTER01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\rw_comp_local_adapter_01 `
  -LogDir C:\UVLM\run_artifacts\rw_comp_local_adapter_01_logs `
  -CiMode
```

Expected posture:

- `review_status = accepted_as_local_adapter_comparison_scaffold`
- `all_comparison_arms_present = true`
- `original_and_revised_candidates_compared = true`
- `evidence_review_path_used_for_reviewed_arms = true`
- `deltas_reported = true`
- `structural_visibility_descriptors_only = true`
- `comparison_is_not_hallucination_reduction_proof = true`
- `comparison_is_not_model_quality_benchmark = true`
- `comparison_is_not_model_superiority_proof = true`
- `comparison_is_not_final_answer_selection = true`
- `candidate_remains_not_accepted_evidence = true`
- `model_weight_training_blocked = true`
- `memory_write_blocked = true`
- `final_answer_release_blocked = true`
- `deployment_blocked = true`
- `promotion_blocked = true`
- `unsupported_claim_count_delta = -1`
- `uncertainty_missing_count_delta = -1`
- `source_reference_visibility_delta = 1`
- `supported_claim_count_delta = 2`
- `structural_visibility_improved_candidate = true`

Reviewer caution: RW-COMP-LOCAL-ADAPTER-01 reports structural review deltas only. It does not prove hallucination reduction, benchmark model quality, select a final answer, accept evidence, authorize adapters, write memory, train models, or deploy.

## Sonya Local Fixture Adapter multi-route

Selection policy is not final answer.

SONYA-LOCAL-FIXTURE-ADAPTER-02 compares multiple deterministic local fixture adapter candidates, applies a selection policy, and records that the selected candidate still requires Evidence Review Pack route. Selection is not adapter authorization. Candidate comparison is not model quality benchmark. No live/network/provider/memory/final/deployment authority is granted.

```powershell
.\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_02 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_02_logs `
  -CiMode
```

Expected posture:

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
- `executed_local_adapter_ids = ['fixture_text_model_adapter', 'fixture_summary_generator_adapter', 'local_file_transform_adapter']`
- `blocked_adapter_ids = ['hash_only_evidence_adapter', 'remote_provider_placeholder_adapter', 'browser_placeholder_adapter', 'atlas_memory_placeholder_adapter', 'sophia_route_placeholder_adapter']`

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-02 compares deterministic local fixture adapter candidates only. Selection is not final answer, not adapter authorization, not truth certification, and not a model quality benchmark.

## Sonya Local Fixture Adapter lineage clarity

Source fixture references are not stale identity leakage.

SONYA-LOCAL-FIXTURE-ADAPTER-03 clarifies source/current experiment lineage for Sonya local fixture adapter multi-route artifacts. Current route identity is explicit. Source fixture identity is explicit. Evidence Review Pack local-adapter route references are explicit. Lineage does not grant authority.

```powershell
.\experiments\Run-SONYA-LOCAL-FIXTURE-ADAPTER03-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_local_fixture_adapter_03 `
  -LogDir C:\UVLM\run_artifacts\sonya_local_fixture_adapter_03_logs `
  -CiMode
```

Expected posture:

- `lineage_review_status = accepted_as_lineage_clarity_packet`
- `current_experiment_id = sonya-local-fixture-adapter-02`
- `source_fixture_experiment_id_present = true`
- `source_fixture_role_present = true`
- `nested_source_identity_explained = true`
- `ambiguous_experiment_id_inheritance_blocked = true`
- `lineage_complete = true`
- `lineage_is_not_authority = true`
- `promotion_blocked = true`
- `source_fixture_reference_not_stale_identity = true`

Reviewer caution: SONYA-LOCAL-FIXTURE-ADAPTER-03 is a lineage clarity packet only. It clarifies that nested source fixture references are dependencies and not stale identity leakage. It does not execute adapters, authorize network, call providers, write memory, release final answers, train models, or deploy.

## Sophia commands

```powershell
cd C:\UVLM\Sophia
python -m pytest -q tests/test_ucc_risk_control_route.py
```

## uvlm-publications commands

`python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json`

`python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite`

not truth certification; not deployment authority; not final answer release; local fixture only; requires external peer review.
