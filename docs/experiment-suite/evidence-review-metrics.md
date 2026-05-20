# Evidence Review metrics

Required phrase: Hypercompression reduces explanatory distance, not review obligation.

EVIDENCE-REVIEW-METRICS-00 is a fixture-only metrics scaffold over Evidence Review product-loop artifacts.

Freshness is not authority.

```powershell
.\experiments\Run-EVIDENCE-REVIEW-METRICS00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\evidence_review_metrics_00 `
  -LogDir C:\UVLM\run_artifacts\evidence_review_metrics_00_logs `
  -CiMode
```

## Primary artifacts

- `evidence_review_metrics_manifest.json`
- `evidence_review_metric_rows.jsonl`
- `evidence_review_hypercompression_packet.json`
- `evidence_review_preservation_packet.json`
- `evidence_review_reviewer_utility_packet.json`
- `evidence_review_metrics_review_packet.json`
- `evidence_review_metrics_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `evidence_review_metrics_00_acceptance_receipt.json`

## Dashboard posture

- `review_status = accepted_as_evidence_review_metrics_scaffold`
- `metrics_id = evidence-review-metrics-00-fixture`
- `metric_rows_present = true`
- `hypercompression_packet_present = true`
- `preservation_packet_present = true`
- `reviewer_utility_packet_present = true`
- `descriptive_fixture_metrics_only = true`
- `audited_context_refresh_measured = true`
- `freshness_not_authority = true`
- `recency_not_correctness = true`
- `context_refresh_requires_audit = true`
- `supersession_requires_lineage = true`
- `context_refresh_not_memory_write = true`
- `context_refresh_not_truth_certification = true`
- `hypercompression_not_truth_certification = true`
- `compression_ratio_not_truth_score = true`
- `high_coherence_not_correctness = true`
- `compressed_review_state_not_accepted_evidence = true`
- `compressed_task_board_not_final_answer = true`
- `preservation_metrics_not_hallucination_reduction_proof = true`
- `reviewer_utility_not_product_release = true`
- `metrics_not_model_superiority_proof = true`
- `metrics_not_peer_review_certification = true`
- `final_answer_not_released = true`
- `accepted_evidence_not_admitted = true`
- `truth_certification_blocked = true`
- `memory_write_blocked = true`
- `provider_calls_not_performed = true`
- `network_calls_not_performed = true`
- `deployment_blocked = true`
- `blocked_claims_verified = true`
- `run_artifact_manifest_status = verified`
- `export_parity_passed = true`

## Blocked claims

- not truth certification
- not hallucination reduction proof
- not model superiority proof
- not peer review certification
- not product release
- not deployment authority
- not final answer selection
- not accepted evidence
- not memory write
- not provider call
