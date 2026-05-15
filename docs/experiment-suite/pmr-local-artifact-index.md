# PMR local artifact index

Memory is governed provenance under resource constraints.

Purpose: describe PMR-01-LOCAL-ARTIFACT-INDEX as a local-only artifact index and dependency graph scaffold. PMR index is not generic cache. Dependency graph is not canon graph. PMR artifact lifecycle state is not truth status. PMR-01 performs indexing only, not pruning. Federation is blocked by default.

## Reproduction command

```powershell
.\experiments\Run-PMR01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_01 `
  -LogDir C:\UVLM\run_artifacts\pmr_01_logs `
  -Mode balanced `
  -LocalStorageBudgetBytes 5368709120 `
  -CiMode
```

## Primary artifacts

- `pmr_local_artifact_index.json`
- `pmr_dependency_graph.json`
- `pmr_local_artifact_index_review_packet.json`
- `pmr_local_artifact_index_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `pmr_01_acceptance_receipt.json`

## Dashboard posture

- `review_status = accepted_as_pmr_local_artifact_index_scaffold`
- `source_pmr_policy_bound = true`
- `artifact_entries_present = true`
- `dependency_graph_present = true`
- `retention_classes_assigned = true`
- `lifecycle_states_assigned = true`
- `hash_encryption_distinction_preserved = true`
- `user_budget_policy_preserved = true`
- `federation_blocked_by_default = true`
- `pruning_not_performed = true`
- `memory_write_blocked = true`
- `atlas_canon_write_blocked = true`
- `model_weight_training_blocked = true`
- `deployment_blocked = true`
- `truth_certification_blocked = true`
- `promotion_blocked = true`
- `artifact_count = 8`
- `node_count = 8`
- `edge_count = 9`
- `revocation_backpropagation_supported = true`
- `pruning_dependency_checks_supported = true`
- `graph_is_not_truth_graph = true`
- `graph_is_not_canon_graph = true`

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
