# Provenance Memory Reservoir

Required phrase: Memory is governed provenance under resource constraints.

Purpose: describe PMR-00-PROVENANCE-MEMORY-RESERVOIR as a local-only architecture scaffold for Provenance Memory Reservoir doctrine and local storage policy. Memory is not storage. Hash is not encryption. User controls local memory budget. Federation is blocked by default. PMR is not Atlas canon. PMR is not model-weight training data.

## Reproduction command

```powershell
.\experiments\Run-PMR00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_00_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

## Primary artifacts

- `pmr_doctrine_packet.json`
- `pmr_local_storage_policy.json`
- `pmr_artifact_retention_classes.json`
- `pmr_review_packet.json`
- `pmr_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `pmr_00_acceptance_receipt.json`

## Dashboard posture

- `review_status = accepted_as_pmr_doctrine_and_policy_scaffold`
- `local_budget_policy_present = true`
- `retention_classes_present = true`
- `hash_encryption_distinction_present = true`
- `federation_blocked_by_default = true`
- `raw_private_data_federation_blocked = true`
- `model_weight_training_blocked = true`
- `memory_write_blocked = true`
- `canon_adoption_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`

## Blocked claims

- not generic cache
- not hidden memory hoard
- not Atlas canon
- not model weight training
- not user data training
- not memory write authorization
- not federation authorization
- not network authorization
- not truth certification
- not deployment authority
- not final answer release
- not hallucination reduction proof
- not recursive self-improvement
- not production readiness
- not pruning execution
- not resource economy
- not token economy

Reviewer caution: PMR-00 and PMR-01 define local provenance-memory doctrine, storage policy, artifact indexing, and dependency graph scaffolds only. They do not write memory, canonize artifacts, federate artifacts, transfer encrypted shards, prune artifacts, train models, certify truth, release final answers, deploy, or reward resource contributions.
