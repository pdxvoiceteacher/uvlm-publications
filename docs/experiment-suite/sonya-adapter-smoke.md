# Sonya Adapter Smoke

Sonya Adapter Smoke exercises contracts, not live adapters.

Purpose: describe SONYA-ADAPTER-SMOKE-00 as an accepted fixture-only adapter-contract smoke test. It exercises adapter selection, consent checks, capability checks, Sonya gateway requirements, raw output rejected or absent posture, candidate packet requirement, failure receipts, telemetry events, and provenance events. Boundary posture: not live adapter execution, not network authorization, not remote provider call, not live model execution, not memory write, not final answer release, not deployment authority, and not model weight training.

## Allowed claim

SONYA-ADAPTER-SMOKE-00 demonstrates fixture-only adapter contract exercise: adapter selection, consent and capability checks, Sonya gateway requirement, raw-output rejection, candidate-packet requirement, failure receipt emission, telemetry event emission, and provenance event emission without live adapter execution or network/provider calls.

## Reproduction command

```powershell
.\experiments\Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\sonya_adapter_smoke_00 `
  -LogDir C:\UVLM\run_artifacts\sonya_adapter_smoke_00_logs `
  -CiMode
```

## Evidence artifacts

- `sonya_adapter_smoke_packet.json`
- `sonya_adapter_smoke_review_packet.json`
- `sonya_adapter_selection_packet.json`
- `sonya_adapter_consent_check_packet.json`
- `sonya_adapter_capability_check_packet.json`
- `sonya_adapter_failure_receipt.json`
- `sonya_adapter_telemetry_packet.json`
- `sonya_adapter_provenance_event_packet.json`
- `sonya_adapter_fixture_candidate_packet.json`
- `sonya_adapter_smoke_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `sonya_adapter_smoke_00_acceptance_receipt.json`

## Prerequisite phases

- SONYA-ADAPTER-CONTRACT-REGISTRY-01
- PROVENANCE-TRAINING-LEDGER-00
- UNIVERSAL-STAGE-PIPELINE-00
- ARTIFACT-CONTRACT-REGISTRY-01
- UNIVERSAL-COMPATIBILITY-MATRIX-00
- SONYA-GW-01

## Dashboard summary

- review_status = accepted_as_fixture_adapter_contract_smoke
- adapter_contract_registry_bound = true
- all_adapters_disabled_or_blocked_or_fixture_only = true
- no_live_adapter_execution = true
- no_network_calls = true
- no_remote_provider_calls = true
- no_live_model_execution = true
- raw_output_rejected_or_absent = true
- candidate_packet_emitted_for_fixture_model = true
- failure_receipts_visible = true
- telemetry_events_visible = true
- provenance_events_visible = true
- model_weight_training_blocked = true
- memory_write_blocked = true
- final_answer_release_blocked = true
- deployment_blocked = true
- promotion_blocked = true

## Reviewer boundaries

- Sonya Adapter Smoke exercises contracts, not live adapters.
- adapter selection, consent checks, capability checks, and Sonya gateway requirements are fixture-only contract checks.
- not adapter execution.
- not live adapter execution.
- not network authorization.
- not remote provider call.
- not live model execution.
- raw output rejected or absent.
- candidate packet required for fixture model output.
- failure receipts visible.
- telemetry events visible.
- provenance events visible.
- not memory write.
- not final answer release.
- not deployment authority.
- not model weight training.
- not production readiness.

Claims blocked: not adapter execution; not live adapter execution; not network authorization; not remote provider call; not live model execution; not memory write; not final answer release; not deployment authority; not truth certification; not model weight training; not hallucination reduction proof; not recursive self-improvement; not production readiness.

Reviewer caution: SONYA-ADAPTER-SMOKE-00 exercises contracts only. It does not execute adapters, does not call providers, does not authorize network use, does not admit raw output as cognition, does not write memory, does not release final answers, does not train models, and does not deploy.
