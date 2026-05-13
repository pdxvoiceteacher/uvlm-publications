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

## Dashboard validation

```bash
python tools/build_public_repro_dashboard.py --out-dir registry --docs-dir docs/experiment-suite
python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite
```

## Publication validation

```bash
python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json
```
