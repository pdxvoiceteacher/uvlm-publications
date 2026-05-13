# Universal Architecture Scaffold

The brain runs cognition stages; experiments configure those stages.

Purpose: show the accepted anti-experimentware architecture scaffold that makes CoherenceLattice a reusable artifact-cognition substrate rather than a pile of bespoke experiment wrappers.

## Architecture summary

- UNIVERSAL-STAGE-PIPELINE-00 defines reusable cognition-stage contracts.
- ARTIFACT-CONTRACT-REGISTRY-01 externalizes artifact roles and profile contracts into versioned configuration.
- UNIVERSAL-COMPATIBILITY-MATRIX-00 tests whether the same stages and contracts handle varied input classes or emit deterministic fail-closed receipts.

profiles are configuration. experiments are configurations over reusable cognition stages and versioned artifact contracts.

## Reproduction commands

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

## Evidence artifacts

- UNIVERSAL-STAGE-PIPELINE-00: `universal_pipeline_manifest.json`, `universal_pipeline_review_packet.json`, `universal_pipeline_stage_records.jsonl`.
- ARTIFACT-CONTRACT-REGISTRY-01: `config/artifact_contracts/artifact_roles.v1.json`, `config/artifact_contracts/package_profiles.v1.json`, `config/artifact_contracts/required_artifacts.v1.json`, `config/artifact_contracts/optional_artifacts.v1.json`, `config/artifact_contracts/forbidden_artifacts.v1.json`, `config/artifact_contracts/profile_composition.v1.json`, `artifact_contract_registry_review.json`.
- UNIVERSAL-COMPATIBILITY-MATRIX-00: `universal_compatibility_matrix_packet.json`, `universal_compatibility_matrix_review_packet.json`, `universal_stage_input_compatibility_rows.jsonl`, `universal_stage_failure_receipts.jsonl`, `universal_compatibility_matrix_summary.md`, `artifact_inventory.json`, `run_artifact_manifest.json`, `export_bundle_manifest.json`, `export_bundle_parity_report.json`, `universal_compatibility_matrix_00_acceptance_receipt.json`.

## Allowed claim

The universal architecture scaffold demonstrates that accepted experiments can be described as configurations over reusable stages and versioned artifact contracts, with unsupported inputs preserved by hash-only or failed-closed receipts.

## Universal Compatibility Matrix dashboard summary

- review_status = accepted_as_universal_compatibility_scaffold
- all_required_stage_ids_present = true
- all_required_input_classes_present = true
- all_required_control_profiles_present = true
- unsupported_inputs_failed_closed_or_hash_only = true
- hash_only_inputs_not_semantically_interpreted = true
- model_facing_stages_require_sonya = true
- no_experiment_specific_kernel_logic_used = true
- failure_receipts_visible = true
- promotion_blocked = true

## Blocked claims

Claims blocked: not product release; not experiment result; not benchmark result; not truth certification; not deployment authority; not final answer release; not hallucination reduction proof; not model superiority proof; not live model evaluation; not live human study; not recursive self-improvement; not AI consciousness claim.

Reviewer caution: this is not product release, not experiment result, not benchmark result, not truth certification, not deployment authority, not final answer release, not hallucination reduction proof, not model superiority proof, not live model evaluation, not live human study, not recursive self-improvement, and not AI consciousness claim.
