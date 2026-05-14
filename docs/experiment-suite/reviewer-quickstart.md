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

## Sophia commands

```powershell
cd C:\UVLM\Sophia
python -m pytest -q tests/test_ucc_risk_control_route.py
```

## uvlm-publications commands

`python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json`

`python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite`

not truth certification; not deployment authority; not final answer release; local fixture only; requires external peer review.
