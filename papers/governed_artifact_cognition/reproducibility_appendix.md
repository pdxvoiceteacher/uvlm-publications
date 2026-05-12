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

## Dashboard validation

```bash
python tools/build_public_repro_dashboard.py --out-dir registry --docs-dir docs/experiment-suite
python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite
```

## Publication validation

```bash
python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json
```
