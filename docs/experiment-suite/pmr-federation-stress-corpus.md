# PMR federation stress corpus

Required phrase: Federation stress corpus is not federation.

Federation stress result is not federation proof. PMR-FED-STRESS-00 is a deterministic synthetic federation stress corpus and failure-mode scaffold. It models federation risks using synthetic fixtures only. It does not federate, does not authorize networks, does not transfer encrypted shards, does not reward users, does not run a token economy, does not write memory, does not train models, does not deploy, and does not certify truth.

## Allowed claim

PMR-FED-STRESS-00 demonstrates a deterministic synthetic federation stress corpus and failure-mode scaffold that models federation risks while preserving no-federation and no-network-authority boundaries.

## Reproduction command

```powershell
.\experiments\Run-PMR-FED-STRESS00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_fed_stress_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_fed_stress_00_logs `
  -DeterministicSeed 1729 `
  -CiMode
```

## Primary artifacts

- `pmr_federation_stress_manifest.json`
- `pmr_federation_node_fixtures.json`
- `pmr_federation_stress_scenarios.json`
- `pmr_federation_failure_mode_rows.jsonl`
- `pmr_federation_propagation_risk_packet.json`
- `pmr_federation_stress_statistics_packet.json`
- `pmr_federation_stress_review_packet.json`
- `pmr_federation_stress_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `triadic_run_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `pmr_fed_stress_00_acceptance_receipt.json`

## Stress scenarios

- `stale_artifact_propagation`
- `revocation_propagation_delay`
- `quarantine_bypass_attempt`
- `hash_encryption_confusion`
- `scope_mismatch_across_nodes`
- `duplicate_artifact_identity`
- `conflicting_provenance_claims`
- `malicious_high_utility_spam`
- `resource_exhaustion_attack`
- `reward_gaming_attempt`
- `privacy_scope_leakage`
- `dependency_graph_split_brain`

## Node fixture types

- `honest_high_availability_node`
- `low_storage_edge_node`
- `stale_cache_node`
- `privacy_restricted_node`
- `malicious_spam_node`
- `revocation_lag_node`
- `quarantine_lag_node`

## Dashboard posture

- `review_status = accepted_as_pmr_federation_stress_scaffold`
- `federation_stress_id = pmr-fed-stress-00-f78c0c71125f4347`
- `node_fixture_count = 7`
- `stress_scenario_count = 12`
- `failure_mode_row_count = 12`
- `source_pmr_sim_bound = true`
- `source_pmr_stat_bound = true`
- `source_architecture_checkpoint_bound = true`
- `source_pmr_ladder_bound = true`
- `node_fixtures_present = true`
- `stress_scenarios_present = true`
- `failure_mode_rows_present = true`
- `propagation_risk_packet_present = true`
- `stress_statistics_packet_present = true`
- `synthetic_nodes_only = true`
- `federation_stress_not_federation = true`
- `federation_stress_not_federation_proof = true`
- `federation_candidate_not_network_authorization = true`
- `shard_transfer_scenario_not_encrypted_shard_transfer = true`
- `federation_credit_scenario_not_reward_entitlement = true`
- `hash_not_encryption_preserved = true`
- `merkle_root_not_confidentiality_preserved = true`
- `federation_blocked_by_default = true`
- `network_calls_not_performed = true`
- `encrypted_shard_transfer_not_performed = true`
- `reward_actions_not_performed = true`
- `token_economy_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `mean_propagation_risk_score = 0.7575`
- `max_propagation_risk_score = 0.93`
- `highest_risk_scenario = privacy_scope_leakage`
- `federation_block_success_rate = 1.0`
- `export_parity_passed = true`

## Blocked claims

- not federation
- not federation proof
- not network authorization
- not encrypted shard transfer
- not reward entitlement
- not token economy
- not real-world inference
- not deployment authority
- not truth certification
- not model weight training
- not memory write authorization
- not Atlas canon
- not hallucination reduction proof
- not recursive self-improvement
- not production readiness

Reviewer caution: PMR-FED-STRESS-00 runs deterministic synthetic federation stress scenarios and failure-mode analysis only. It does not federate, does not call networks, does not transfer encrypted shards, does not reward users, does not run a token economy, does not write memory, does not train models, does not deploy, and does not certify truth.
