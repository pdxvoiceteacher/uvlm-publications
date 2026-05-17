# PMR GPCU utility scoring

Required phrase: GPCU is lifecycle/storage utility, not truth score.

PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY scores local PMR-indexed artifacts for lifecycle/storage utility and emits lifecycle recommendations. Lifecycle recommendation is not pruning. Reward mechanics are deferred. Federation remains blocked by default.

## Allowed claim

PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY demonstrates deterministic local utility scoring for PMR-indexed artifacts and emits lifecycle recommendations while preserving non-authority boundaries.

## Reproduction command

```powershell
.\experiments\Run-PMR02-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_02 `
  -LogDir C:\UVLM\run_artifacts\pmr_02_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

## Primary artifacts

- `pmr_provenance_coherence_utility_packet.json`
- `pmr_artifact_utility_scores.jsonl`
- `pmr_lifecycle_recommendation_packet.json`
- `pmr_utility_review_packet.json`
- `pmr_utility_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `pmr_02_acceptance_receipt.json`

## Dashboard posture

- `review_status = accepted_as_pmr_utility_scoring_scaffold`
- `source_pmr_policy_bound = true`
- `source_pmr_index_bound = true`
- `utility_scores_present = true`
- `lifecycle_recommendations_present = true`
- `scoring_dimensions_present = true`
- `gpcu_not_truth_score = true`
- `gpcu_not_reward_entitlement = true`
- `gpcu_not_pruning_execution = true`
- `gpcu_not_federation_authorization = true`
- `lifecycle_recommendations_not_actions = true`
- `hash_encryption_distinction_preserved = true`
- `user_budget_policy_preserved = true`
- `federation_blocked_by_default = true`
- `pruning_not_performed = true`
- `reward_actions_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `artifact_count = 8`
- `scored_artifact_count = 8`
- `pmr00_doctrine_utility_band = retain_locked`
- `pmr00_policy_utility_band = retain_locked`
- `pmr00_retention_utility_band = retain_priority`
- `rw_comp_local_adapter_anchor_utility_band = retain_priority`
- `ephemeral_summary_utility_band = compress_candidate`
- `revoked_hash_tombstone_utility_band = revoked`
- `quarantine_example_utility_band = quarantine`

## Blocked claims

- not truth score
- not reward entitlement
- not token economy
- not human value score
- not Atlas canon
- not model weight training
- not memory write authorization
- not federation authorization
- not network authorization
- not pruning execution
- not resource economy
- not truth certification
- not deployment authority
- not final answer release
- not hallucination reduction proof
- not recursive self-improvement
- not production readiness

Reviewer caution: PMR-02 computes lifecycle/storage utility scores and recommendations only. It does not prune artifacts. GPCU is not reward entitlement and not token economy. It does not certify truth. It does not authorize federation. It does not write memory, train models, deploy, or assign human value.
