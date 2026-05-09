# Reproducibility Appendix

This appendix records reviewer-facing commands for reproducing the governed artifact cognition fixture evidence in the CoherenceLattice workspace. Paths are examples and should be adjusted to the local checkout. The commands are intentionally framed as local fixture commands: no deployment evidence, no live Atlas memory writes, no live Sophia calls, and no final answer release are implied.

## Prerequisites

- A local CoherenceLattice checkout containing the accepted SONYA-AEGIS-SMOKE-02 harness, WAVE Gold-Physics family acceptance scripts, and experiment suite reproducibility pack builder.
- A local `uvlm-publications` checkout for this draft and reviewer materials.
- The accepted fixture artifacts listed in `artifact_table.md`.

## POSIX shell

```bash
# 1. Enter the CoherenceLattice checkout.
cd ../CoherenceLattice

# 2. Run accepted SONYA-AEGIS-SMOKE-02, finalizer, repro-pack, and WAVE tests.
python -m pytest -q \
  python/tests/integration/test_sonya_aegis_smoke_02_acceptance_harness.py \
  python/tests/integration/test_sonya_aegis_publisher_boundary_finalizer.py \
  python/tests/integration/test_experiment_suite_repro_pack.py \
  python/tests/waveform/test_waveform_family_acceptance.py

# 3. Build WAVE Gold-Physics family acceptance artifacts.
python -m coherence.waveform.family_acceptance \
  --bridge-root artifacts/wave_gold_physics_family

# 4. Build the experiment suite reproducibility pack.
python -m coherence.tools.build_experiment_suite_repro_pack \
  --registry experiments/experiment_suite_registry.json \
  --artifacts-root artifacts \
  --sonya-aegis-smoke-02-report artifacts/sonya_aegis_smoke_02/sonya_aegis_smoke_02_acceptance_report.json \
  --wave-family-report artifacts/wave_gold_physics_family/waveform_gold_physics_family_acceptance_packet.json \
  --out-dir artifacts/experiment_suite_repro_pack \
  --zip

# 5. Inspect expected outputs.
python - <<'PY'
from pathlib import Path
for path in [
    'artifacts/sonya_aegis_smoke_02/sonya_aegis_smoke_02_acceptance_report.json',
    'artifacts/experiment_suite_repro_pack/experiment_suite_repro_pack.json',
    'artifacts/experiment_suite_repro_pack/acceptance_matrix.csv',
    'artifacts/experiment_suite_repro_pack/artifact_manifest.json',
    'artifacts/experiment_suite_repro_pack/experiment_suite_reproducibility_report.md',
    'artifacts/wave_gold_physics_family/waveform_gold_physics_family_acceptance_packet.json',
]:
    print(path, Path(path).exists())
PY
```

## Windows PowerShell

```powershell
# 1. Enter the CoherenceLattice checkout.
Set-Location C:\UVLM\CoherenceLattice

# 2. Run the accepted SONYA-AEGIS-SMOKE-02 harness.
.\experiments\Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened `
  -LogDir C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened_logs `
  -CiMode

# 3. Build WAVE Gold-Physics family acceptance artifacts.
$waveBridge = "C:\UVLM\run_artifacts\wave_gold_physics_family"
python -m coherence.waveform.family_acceptance `
  --bridge-root $waveBridge

# 4. Build the experiment suite reproducibility pack.
python -m coherence.tools.build_experiment_suite_repro_pack `
  --registry experiments/experiment_suite_registry.json `
  --artifacts-root C:\UVLM\run_artifacts `
  --sonya-aegis-smoke-02-report C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened\sonya_aegis_smoke_02_acceptance_report.json `
  --wave-family-report C:\UVLM\run_artifacts\wave_gold_physics_family\waveform_gold_physics_family_acceptance_packet.json `
  --out-dir C:\UVLM\run_artifacts\experiment_suite_repro_pack_v3 `
  --zip

# 5. Inspect expected outputs.
@(
  'C:\UVLM\run_artifacts\sonya_aegis_smoke_02_hardened\sonya_aegis_smoke_02_acceptance_report.json',
  'C:\UVLM\run_artifacts\experiment_suite_repro_pack_v3\experiment_suite_repro_pack.json',
  'C:\UVLM\run_artifacts\experiment_suite_repro_pack_v3\acceptance_matrix.csv',
  'C:\UVLM\run_artifacts\experiment_suite_repro_pack_v3\artifact_manifest.json',
  'C:\UVLM\run_artifacts\experiment_suite_repro_pack_v3\experiment_suite_reproducibility_report.md',
  'C:\UVLM\run_artifacts\wave_gold_physics_family\waveform_gold_physics_family_acceptance_packet.json'
) | ForEach-Object { Write-Output "$($_) $((Test-Path $_))" }
```

## Local paper validation

From the `uvlm-publications` checkout:

```bash
python tools/validate_publication_claims.py \
  --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md \
  --appendix papers/governed_artifact_cognition/reproducibility_appendix.md \
  --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md \
  --status papers/governed_artifact_cognition/status.json
```

## Interpretation boundary

Successful reproduction means the local fixture artifacts can be regenerated or inspected. It does not mean deployment readiness, truth certification, final-answer correctness, AI consciousness, universal wisdom, recursive Sonya federation, retrosynthesis runtime, Omega detection, Publisher finalization, live Atlas memory writes, or live Sophia calls.
