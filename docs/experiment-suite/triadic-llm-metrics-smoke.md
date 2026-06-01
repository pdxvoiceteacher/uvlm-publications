# Triadic LLM metrics smoke

TRIADIC-LLM-METRICS-SMOKE-00 demonstrates a local candidate-to-forensic-review smoke with source-linked and unsupported claims visible.

## Dashboard summary

- smoke_status = completed
- span_linked_claim_count = 1
- unsupported_claim_count = 1
- raw_model_output_final_answer = false
- provider_runtime_performed = false
- product_release_performed = false
- final_answer_emitted = false
- truth_certification_emitted = false
- memory_write_performed = false
- atlas_memory_admission_performed = false

## Artifacts

- `llm_metrics_smoke_request.json`
- `sonya_model_candidate_packet.json`
- `source_integrity_packet.json`
- `source_span_map.json`
- `claim_classification_packet.json`
- `claim_evidence_map.json`
- `unsupported_claim_report.json`
- `coherence_runtime_metrics_packet.json`
- `coherence_action_functional_packet.json`
- `ai_decision_trace_packet.json`
- `review_receipt.md`
- `llm_metrics_smoke_receipt.json`

## Required boundaries

- Raw model output is not final answer.
- Sonya model candidate packet is candidate-only.
- At least one claim is source-span linked.
- At least one unsupported claim is visible.
- Metrics are diagnostic and non-authoritative.
- No provider runtime occurred.
- No product release occurred.
- No memory write occurred.
- No truth certification occurred.

## Reproducibility

```powershell
python -c "from pathlib import Path; from coherence.triadic.llm_metrics_smoke import build_triadic_llm_metrics_smoke; from coherence.ucc.sophia_control_review import build_sophia_ucc_control_review; from coherence.ucc.standards_source_registry import build_ucc_standards_source_registry; from coherence.ucc.materiality_profile import build_ucc_materiality_profile; from coherence.ucc.materiality_override import build_ucc_materiality_override_receipt; root=Path(r'C:\UVLM\run_artifacts\triadic_llm_ucc_source_materiality'); build_triadic_llm_metrics_smoke(output_root=root); build_sophia_ucc_control_review(root / 'bridge'); build_ucc_standards_source_registry(root / 'bridge'); build_ucc_materiality_profile(root / 'bridge'); build_ucc_materiality_override_receipt(root / 'bridge')"
```
