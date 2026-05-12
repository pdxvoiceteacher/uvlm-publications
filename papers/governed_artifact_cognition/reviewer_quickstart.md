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
