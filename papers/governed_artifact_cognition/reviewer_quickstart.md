# Reviewer Quickstart

Read the paper, claim-boundary table, artifact table, and this quickstart before interpreting artifacts. The review posture is local fixture only, not truth certification, not deployment authority, not final answer release, not AI consciousness, not recursive Sonya federation, not retrosynthesis runtime, not Omega detection, not live Atlas memory writes, not live Sophia calls, and requires external peer review.

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
