# Reviewer Quickstart

## What this paper claims

- WAVE Gold-Physics is a closed-form synthetic calibration family.
- The family calibrates CoherenceLattice metrics against known waveform behavior.
- WAVE-00R through WAVE-03R are accepted Gold-Physics members.
- High coherence is not equivalent to constructive output.

## What this paper does not claim

- Not universal ontology.
- Not psychoacoustic effect.
- Not AI consciousness.
- Not TCHES engineering validity.
- Not UNI-02 portability.
- Not retrosynthesis readiness.
- Not deployment authority.
- Not truth certification.
- Not final answer authority.
- Requires external peer review.

## Exact CoherenceLattice PowerShell commands

```powershell
Set-Location C:\UVLM\CoherenceLattice

$python = ".\.venv\Scripts\python.exe"
$env:PYTHONPATH = "C:\UVLM\CoherenceLattice\python\src"

& $python -m pytest -q `
  python/tests/waveform/test_waveform_family_acceptance.py `
  python/tests/integration/test_experiment_suite_repro_pack.py

$waveBridge = "C:\UVLM\run_artifacts\wave_gold_physics_family"
Remove-Item -Recurse -Force $waveBridge -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $waveBridge | Out-Null

& $python -m coherence.waveform.family_acceptance `
  --bridge-root $waveBridge

Get-Content (Join-Path $waveBridge "waveform_gold_physics_family_acceptance_packet.json")
```

## What to inspect

- Confirm WAVE-00R through WAVE-03R are present in the acceptance packet.
- Confirm guardrails: no model generation, no Sonya runtime, no retrosynthesis, no prior injection, no ontology claim, no deployment authority, and no truth certification.
- Confirm theorem mapping in `theorem_table.md` and boundary mapping in `claim_boundary_table.md`.
