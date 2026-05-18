# PMR simulation statistical analysis

Required phrase: Descriptive fixture statistics are not real-world inference.

Rank table is not production policy selection. PMR policy remains allowed to lose. PMR-STAT-00 consumes PMR-SIM-00 outputs and emits descriptive fixture-bound statistical analysis only: policy metric summaries, policy pair deltas, rank table, sensitivity packet, failure mode packet, review packet, and summary.

## Allowed claim

PMR-STAT-00 demonstrates descriptive fixture-bound statistical analysis over PMR-SIM-00 outputs, including policy metric summaries, pair deltas, rank tables, sensitivity summaries, and failure-mode summaries, while preserving non-production and non-authority boundaries.

## Reproduction command

```powershell
.\experiments\Run-PMR-STAT00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_stat_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_stat_00_logs `
  -Repetitions 3 `
  -DeterministicSeed 1729 `
  -CiMode
```

## Primary artifacts

- `pmr_stat_analysis_manifest.json`
- `pmr_stat_policy_metric_summaries.jsonl`
- `pmr_stat_policy_pair_deltas.jsonl`
- `pmr_stat_rank_table.json`
- `pmr_stat_sensitivity_packet.json`
- `pmr_stat_failure_mode_packet.json`
- `pmr_stat_review_packet.json`
- `pmr_stat_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `triadic_run_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `pmr_stat_00_acceptance_receipt.json`

## Dashboard posture

- `review_status = accepted_as_pmr_statistical_analysis_scaffold`
- `stat_analysis_id = pmr-stat-00-4fe88851274ea012`
- `row_count = 120`
- `policy_count = 5`
- `scenario_count = 8`
- `repetition_count = 3`
- `metric_count = 17`
- `source_pmr_sim_bound = true`
- `source_architecture_checkpoint_bound = true`
- `policy_metric_summaries_present = true`
- `policy_pair_deltas_present = true`
- `rank_table_present = true`
- `sensitivity_packet_present = true`
- `failure_mode_packet_present = true`
- `descriptive_statistics_only = true`
- `no_inferential_real_world_claim = true`
- `pmr_policy_allowed_to_lose = true`
- `rank_table_not_production_policy_selection = true`
- `statistics_not_pmr_superiority_proof = true`
- `statistics_not_hallucination_reduction_proof = true`
- `statistics_not_federation_proof = true`
- `statistics_not_reward_economy_proof = true`
- `production_policy_selected = false`
- `federation_blocked_by_default = true`
- `reward_actions_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `policy_metric_summary_count = 85`
- `policy_pair_delta_count = 170`
- `export_parity_passed = true`

## Rank table summary

- pmr_gpcu_heuristic mean_rank = 1.882353
- recency_only mean_rank = 2.176471
- cost_minimizing mean_rank = 2.529412
- random_retention mean_rank = 2.764706
- retain_all mean_rank = 2.823529
- PMR-GPCU has best mean fixture rank but this is not PMR superiority proof.
- retain_all still wins replay_success_rate, audit_availability_rate, and dependency_integrity_rate.
- cost_minimizing still wins multiple cost / violation / review-burden metrics.
- simpler baselines are allowed to win metrics or scenarios.

## Blocked claims

- not real-world inference
- not production memory policy
- not production policy selection
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

Reviewer caution: PMR-STAT-00 runs descriptive fixture-bound analysis over PMR-SIM-00 outputs only. It does not select a production memory policy, is not real-world inference, is not PMR superiority proof, is not hallucination reduction proof, is not federation proof, is not reward economy proof, does not write memory, does not train models, does not deploy, and does not certify truth.
