# Sonya required membrane checkpoint

Required phrase: Sonya is the required execution membrane for model/tool/provider-facing paths.

SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00 audits model/tool/provider-facing paths and maps each path to Sonya-required, fixture-non-applicable, publication-non-applicable, or fail-closed posture. Missing Sonya posture must fail closed. Direct model/provider call is not allowed when SONYA_REQUIRED=1. Candidate packet is not final answer. Adapter capability is not adapter authorization. Fixture-only builder is not live execution. Raw output is forbidden. Raw output is not cognition. Telemetry event is not authority. Failure receipt is not permission to proceed.

## Reproduction command

```powershell
.\experiments\Run-SONYA-REQUIRED-MEMBRANE-CHECKPOINT00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_required_membrane_checkpoint_00 `
  -LogDir C:\UVLM\run_artifacts\sonya_required_membrane_checkpoint_00_logs `
  -CiMode
```

## Primary artifacts

- `sonya_required_membrane_checkpoint_packet.json`
- `sonya_runtime_path_coverage_rows.jsonl`
- `sonya_bypass_surface_register.json`
- `sonya_candidate_packet_requirement_map.json`
- `sonya_fixture_non_applicability_map.json`
- `sonya_required_membrane_review_packet.json`
- `sonya_required_membrane_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `triadic_run_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `sonya_required_membrane_checkpoint_00_acceptance_receipt.json`

## Dashboard posture

- `review_status = accepted_as_sonya_required_membrane_checkpoint`
- `checkpoint_id = sonya-required-membrane-checkpoint-00-2e8f6c52e1f54b43`
- `runtime_path_row_count = 10`
- `model_facing_path_count = 1`
- `provider_facing_path_count = 1`
- `adapter_facing_path_count = 2`
- `fixture_only_path_count = 3`
- `publication_only_path_count = 1`
- `validator_only_path_count = 1`
- `telemetry_only_path_count = 1`
- `sonya_required_path_count = 4`
- `fixture_non_applicable_path_count = 3`
- `publication_non_applicable_path_count = 1`
- `fail_closed_required_path_count = 2`
- `bypass_surface_count = 7`
- `candidate_packet_requirement_count = 10`
- `fixture_non_applicability_count = 7`
- `sonya_required_policy_evaluated = true`
- `runtime_paths_scanned = true`
- `bypass_surfaces_registered = true`
- `candidate_packet_requirements_mapped = true`
- `fixture_non_applicability_mapped = true`
- `direct_model_call_blocked_when_required = true`
- `raw_output_forbidden = true`
- `candidate_packet_not_final_answer = true`
- `adapter_capability_not_authorization = true`
- `fixture_only_builder_not_live_execution = true`
- `missing_sonya_posture_fails_closed = true`
- `live_model_execution_not_performed = true`
- `provider_calls_not_performed = true`
- `network_calls_not_performed = true`
- `adapter_authorization_not_performed = true`
- `memory_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `export_parity_passed = true`

## Blocked claims

- not live model execution
- not provider call
- not network authorization
- not adapter authorization
- not raw output admission
- not final answer release
- not memory write
- not model weight training
- not deployment authority
- not truth certification
- not hallucination reduction proof
- not recursive self-improvement
- not production readiness

Reviewer caution: SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00 maps Sonya membrane posture only. It does not execute live models, call providers, authorize networks, authorize adapters, admit raw output, release final answers, write memory, train models, deploy, certify truth, prove hallucination reduction, or recursively self-improve.
