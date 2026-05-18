# PMR simulation baseline comparison

Required phrase: PMR becomes scientific only when it can lose.

PMR policy is allowed to lose. PMR-SIM-00 is a deterministic synthetic fixture simulation scaffold comparing retain_all, recency_only, random_retention, cost_minimizing, and pmr_gpcu_heuristic policies across synthetic provenance-bearing artifact streams. Fixture streams are synthetic and deterministic. Retained does not mean true. Replay-ready does not mean canon. Stored does not mean trained.

## Allowed claim

PMR-SIM-00 demonstrates a deterministic synthetic fixture simulation scaffold comparing PMR-GPCU-style retention against simpler baselines while preserving non-production and non-authority boundaries.

## Reproduction command

```powershell
.\experiments\Run-PMR-SIM00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_sim_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_sim_00_logs `
  -Repetitions 3 `
  -DeterministicSeed 1729 `
  -CiMode
```

## Primary artifacts

- `pmr_simulation_manifest.json`
- `pmr_simulation_fixture_streams.json`
- `pmr_simulation_policy_profiles.json`
- `pmr_simulation_result_rows.jsonl`
- `pmr_simulation_comparison_packet.json`
- `pmr_simulation_statistics_packet.json`
- `pmr_simulation_review_packet.json`
- `pmr_simulation_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `triadic_run_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `pmr_sim_00_acceptance_receipt.json`

## Policies

- `retain_all`
- `recency_only`
- `random_retention`
- `cost_minimizing`
- `pmr_gpcu_heuristic`

## Scenarios

- `low_storage_pressure_clean_lineage`
- `high_storage_pressure_replay_demand`
- `revocation_event_backpropagation`
- `quarantine_event_counterevidence`
- `user_pin_vs_privacy_pressure`
- `dependency_heavy_audit_replay`
- `stale_low_utility_artifact_stream`
- `mixed_privacy_scope_artifact_stream`

## Comparison summary

- retain_all wins at least replay_success_rate, audit_availability_rate, and dependency_integrity_rate.
- cost_minimizing wins at least storage_cost, review_burden, and policy_failure_count.
- pmr_gpcu_heuristic wins 7 fixture scenarios but this is not PMR superiority proof.
- Simpler baselines may win metrics or scenarios.

## Dashboard posture

- `review_status = accepted_as_pmr_simulation_baseline_scaffold`
- `simulation_id = pmr-sim-00-806c5904ee0ff6a7`
- `deterministic_seed = 1729`
- `simulation_repetition_count = 3`
- `row_count = 120`
- `source_pmr_ladder_bound = true`
- `architecture_checkpoint_bound = true`
- `fixture_streams_present = true`
- `baseline_policies_present = true`
- `pmr_policy_present = true`
- `result_rows_present = true`
- `comparison_packet_present = true`
- `statistics_packet_present = true`
- `pmr_policy_allowed_to_lose = true`
- `simulation_not_production_policy = true`
- `simulation_not_superiority_proof = true`
- `simulation_not_hallucination_reduction_proof = true`
- `simulation_not_federation_proof = true`
- `simulation_not_reward_economy_proof = true`
- `federation_blocked_by_default = true`
- `reward_actions_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `production_policy_selected = false`
- `federation_performed = false`
- `reward_actions_performed = false`
- `token_economy_performed = false`
- `memory_write_performed = false`
- `atlas_canon_write_performed = false`
- `model_weight_training_performed = false`
- `export_parity_passed = true`

## Blocked claims

- not production memory policy
- not PMR superiority proof
- not hallucination reduction proof
- not model superiority proof
- not federation proof
- not reward economy proof
- not reward entitlement
- not token economy
- not Atlas canon
- not model weight training
- not memory write authorization
- not truth certification
- not deployment authority
- not final answer release
- not recursive self-improvement
- not production readiness

Reviewer caution: PMR-SIM-00 runs deterministic synthetic fixture simulations only. It does not select a production memory policy, is not PMR superiority proof, is not hallucination reduction proof, is not federation proof, is not reward economy proof, does not write memory, does not train models, does not deploy, and does not certify truth.
