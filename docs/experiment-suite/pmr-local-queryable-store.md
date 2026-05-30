# PMR local queryable store

## What was validated

PMR-LOCAL-RUNTIME-QUERYABLE-STORE-00 is a bounded local provenance query phase over the local review artifact ecology. PMR query is local provenance retrieval only. The publication dashboard records the locally validated query index and smoke-query receipt without changing CoherenceLattice runtime behavior.

## Query index summary

- query_index_status = indexed
- indexed artifacts = 44
- indexed dependency edges = 34
- indexed metric count = 37
- indexed formula count = 19
- indexed bound profile count = 19
- indexed TEL event count = 19
- indexed seed observation count = 6
- indexed flow node count = 20
- indexed Sonya coverage row count = 10
- query_count = 15
- completed_query_count = 14
- no_match_query_count = 1
- forbidden_authority_artifact_count = 0

## Supported query types

- artifact_by_name
- artifact_by_role
- artifact_by_retention_class
- dependency_upstream
- dependency_downstream
- metric_by_id
- formula_by_id
- bound_profile_by_metric
- tel_event_by_type
- sophia_decision_by_run
- seed_observation_by_fixture
- seed_observation_by_posture
- flow_node_by_stage
- sonya_coverage_by_artifact
- forbidden_authority_scan

## Allowed claim

PMR-LOCAL-RUNTIME-QUERYABLE-STORE-00 provides bounded local provenance query over the local review artifact ecology, including artifacts, dependency edges, runtime metrics, formula registry entries, metric bounds, TEL events, Sophia posture, Sonya coverage, flow nodes, and seed corpus observations.

## What this does not prove or authorize

- PMR query is not memory write.
- PMR query is not retrosynthesis.
- PMR query is not Atlas memory admission.
- PMR query is not truth certification.
- PMR query is not product release.
- PMR query is not final answer authority.
- PMR query is not accepted evidence authority.
- PMR query is not deployment.
- PMR query is not federation.
- PMR query is not provider runtime.
- PMR query is not LAN enablement.
- PMR query is not consciousness proof.
- PMR query is not Omega detection.
- PMR query is not universal ontology proof.
- PMR query is not population calibration.
- PMR query is not user benefit proof.
- PMR query is not market validation.

## Retrosynthesis-readiness boundary

PMR query prepares the substrate for future retrosynthesis-readiness analysis, but does not perform retrosynthesis. Query results remain local provenance retrieval outputs only and do not admit Atlas memory, write memory, certify truth, release product behavior, federate, deploy, or select final answers.

## Reproducibility

```powershell
.\experiments\Run-PMR-LOCAL-RUNTIME-QUERYABLE-STORE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_local_runtime_queryable_store_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_local_runtime_queryable_store_00_logs `
  -CiMode
```

The command records local query-index artifacts and smoke-query receipts only. It does not authorize provider runtime, LAN/network access, federation, memory write, Atlas memory admission, product release, deployment, or retrosynthesis.
