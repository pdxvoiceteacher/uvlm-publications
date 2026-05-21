# TB Product Slice

Phase: `TB-PRODUCT-SLICE-00`

User-visible review receipt is required.
Unsupported claim must remain visible.

```powershell
.\experiments\Run-TB-PRODUCT-SLICE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\tb_product_slice_00 `
  -LogDir C:\UVLM\run_artifacts\tb_product_slice_00_logs `
  -CiMode
```

- `tb_product_slice_manifest.json`
- `source_bundle_manifest.json`
- `sonya_candidate_packet.json`
- `claim_evidence_map.json`
- `unsupported_claim_report.json`
- `uncertainty_report.json`
- `tel_events.jsonl`
- `prior_origin_use_packet.json`
- `pmr_provenance_stub.json`
- `review_receipt.json`
- `review_receipt.md`
- `tb_product_slice_review_packet.json`
- `run_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `tb_product_slice_00_acceptance_receipt.json`
