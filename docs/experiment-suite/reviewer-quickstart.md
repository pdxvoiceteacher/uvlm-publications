# Reviewer Quickstart

## Read first path

1. claim boundaries
2. governed artifact cognition paper
3. WAVE Rosetta paper
4. SONYA-AEGIS-SMOKE-02
5. WAVE family
6. UNI-02D Sonya gate
7. RETRO-LANE-00

## CoherenceLattice commands

POSIX: `python -m coherence.waveform.family_acceptance --bridge-root artifacts/wave_gold_physics_family`

PowerShell: `experiments/Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1 -CiMode`

## Sophia commands

`python -m pytest -q python/tests/integration/test_sophia_ucc_route.py`

## uvlm-publications commands

`python tools/validate_publication_claims.py --paper papers/governed_artifact_cognition/PUB_GOV_ARTIFACT_COG_01.md --quickstart papers/governed_artifact_cognition/reviewer_quickstart.md --status papers/governed_artifact_cognition/status.json`

`python tools/validate_public_repro_dashboard.py --dashboard registry/experiment_suite_dashboard.json --docs-dir docs/experiment-suite`

not truth certification; not deployment authority; not final answer release; local fixture only; requires external peer review.
