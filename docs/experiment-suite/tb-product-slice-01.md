# TB Product Slice 01

Phase: `TB-PRODUCT-SLICE-01`

Cross-source conflict is not contradiction resolution.
Conflict must remain visible.
Multi-source review is not truth certification.
Cross-source agreement is not accepted evidence.
Candidate packet is not final answer.
Model output is not authority.
Source match is not truth certification.
Supported claim is not accepted evidence.
Unsupported claim must remain visible.
Prior context is not evidence.
TEL event is not authority.
PMR provenance stub is not memory write.
Review receipt is not deployment authority.
Local product slice is not product release.

```powershell
.\experiments\Run-TB-PRODUCT-SLICE01-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\tb_product_slice_01 `
  -LogDir C:\UVLM\run_artifacts\tb_product_slice_01_logs `
  -CiMode
```

## Primary artifacts

- `tb_product_slice_01_manifest.json`
- `multi_source_bundle_manifest.json`
- `sonya_candidate_packet.json`
- `claim_evidence_map.json`
- `source_link_map.json`
- `unsupported_claim_report.json`
- `uncertainty_report.json`
- `cross_source_conflict_report.json`
- `tel_events.jsonl`
- `prior_origin_use_packet.json`
- `pmr_provenance_stub.json`
- `review_receipt.json`
- `review_receipt.md`
- `tb_product_slice_01_review_packet.json`
- `run_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `tb_product_slice_01_acceptance_receipt.json`

## Observed review behavior

- `supported_claim_count = 2`
- `unsupported_claim_count = 2`
- `conflict_count = 2`
- `source_file_count = 3`
- `unsupported overclaim = The study proved long-term effectiveness.`
- `conflict = enrollment vs completion ambiguity.`
