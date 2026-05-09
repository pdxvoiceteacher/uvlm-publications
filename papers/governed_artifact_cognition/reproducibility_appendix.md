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

# 2. Run the SONYA-AEGIS-SMOKE-02 harness.
python -m pytest -q tests/test_sonya_aegis_smoke_02.py

# 3. Run WAVE Gold-Physics family acceptance.
python -m pytest -q tests/test_wave_gold_physics_family.py

# 4. Build the experiment suite reproducibility pack.
python scripts/build_experiment_suite_repro_pack.py \
  --registry experiments/experiment_suite_registry.json \
  --out-dir artifacts/experiment_suite_repro_pack

# 5. Inspect expected outputs.
python - <<'PY'
from pathlib import Path
for path in [
    'artifacts/sonya_aegis_smoke_02_acceptance_report.json',
    'artifacts/experiment_suite_repro_pack/experiment_suite_repro_pack.json',
    'artifacts/experiment_suite_repro_pack/acceptance_matrix.csv',
    'artifacts/experiment_suite_repro_pack/artifact_manifest.json',
    'artifacts/experiment_suite_repro_pack/experiment_suite_reproducibility_report.md',
    'artifacts/waveform_gold_physics_family_acceptance_packet.json',
]:
    print(path, Path(path).exists())
PY
```

## Windows PowerShell

```powershell
# 1. Enter the CoherenceLattice checkout.
Set-Location ..\CoherenceLattice

# 2. Run the SONYA-AEGIS-SMOKE-02 harness.
python -m pytest -q tests/test_sonya_aegis_smoke_02.py

# 3. Run WAVE Gold-Physics family acceptance.
python -m pytest -q tests/test_wave_gold_physics_family.py

# 4. Build the experiment suite reproducibility pack.
python scripts/build_experiment_suite_repro_pack.py `
  --registry experiments/experiment_suite_registry.json `
  --out-dir artifacts/experiment_suite_repro_pack

# 5. Inspect expected outputs.
@(
  'artifacts/sonya_aegis_smoke_02_acceptance_report.json',
  'artifacts/experiment_suite_repro_pack/experiment_suite_repro_pack.json',
  'artifacts/experiment_suite_repro_pack/acceptance_matrix.csv',
  'artifacts/experiment_suite_repro_pack/artifact_manifest.json',
  'artifacts/experiment_suite_repro_pack/experiment_suite_reproducibility_report.md',
  'artifacts/waveform_gold_physics_family_acceptance_packet.json'
) | ForEach-Object { Write-Output "$($_) $((Test-Path $_))" }
```

## Local paper validation

From the `uvlm-publications` checkout:

```bash
python - <<'PY'
from pathlib import Path
root = Path('papers/governed_artifact_cognition')
required = [
    'PUB_GOV_ARTIFACT_COG_01.md',
    'reproducibility_appendix.md',
    'claim_boundary_table.md',
    'artifact_table.md',
    'reviewer_quickstart.md',
    'status.json',
]
missing = [name for name in required if not (root / name).exists()]
if missing:
    raise SystemExit(f'missing required draft files: {missing}')
text = '\n'.join((root / name).read_text(encoding='utf-8') for name in required if name.endswith('.md'))
for phrase in [
    'not truth certification',
    'not deployment authority',
    'not final answer release',
    'local fixture only',
    'requires external peer review',
]:
    if phrase not in text:
        raise SystemExit(f'missing non-claim phrase: {phrase}')
print('governed artifact cognition draft checks passed')
PY
```

## Interpretation boundary

Successful reproduction means the local fixture artifacts can be regenerated or inspected. It does not mean deployment readiness, truth certification, final-answer correctness, AI consciousness, universal wisdom, recursive Sonya federation, retrosynthesis runtime, Omega detection, Publisher finalization, live Atlas memory writes, or live Sophia calls.
