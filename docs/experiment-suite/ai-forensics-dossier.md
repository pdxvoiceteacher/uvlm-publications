# AI Forensics Dossier

Triadic Brain turns AI outputs into auditable, source-linked, control-aware forensic dossiers.

## Dashboard summary

- dossier_status = completed
- dossier_mode = user_facing_forensic_summary
- dossier_sections = 16
- span_linked_claim_count = 1
- unsupported_claim_count = 1
- satisfied_control_count = 5
- uncertain_control_count = 1
- source_profile_count = 2
- nist_reference_only = true
- nist_source_text_stored = false
- human_review_required = true
- raw_model_output_final_answer = false
- final_answer_emitted = false
- accepted_evidence_emitted = false
- truth_certification_emitted = false
- compliance_certification_emitted = false
- audit_opinion_emitted = false
- professional_attestation_emitted = false
- product_release_performed = false
- provider_runtime_performed = false
- memory_write_performed = false
- atlas_memory_admission_performed = false

## Artifacts

- `ai_forensics_dossier_packet.json`
- `ai_forensics_dossier_section_index.json`
- `ai_forensics_dossier.md`
- `ai_forensics_dossier_receipt.json`

## Claim allowed

AI-FORENSICS-DOSSIER-00 packages a local AI candidate, source evidence, unsupported claims, diagnostic metrics, UCC/Sophia control review, source registry, materiality profile, PMR provenance, and export parity into a human-reviewable forensic dossier without issuing final-answer, certification, product, provider, memory, or Atlas authority.

## Required boundaries

- The dossier is AI process forensics.
- The dossier is not model mind-reading.
- The dossier is not hidden chain-of-thought disclosure.
- This dossier is not a final answer.
- This dossier is not truth certification.
- This dossier is not compliance certification.
- This dossier is not audit opinion.
- This dossier is not professional attestation.
- Raw model output is not final answer.
- UCC control review is diagnostic, not certification.
- NIST CSF 2.0 is reference-only in this run.
- NIST control text is not ingested.
- Materiality override does not modify the source standard.
- Human review remains required.
- No provider runtime occurred.
- No product release occurred.
- No memory write occurred.
- No Atlas memory admission occurred.

## Blocked overclaim examples

- AI Forensics Dossier is final answer
- AI Forensics Dossier certifies truth
- AI Forensics Dossier certifies compliance
- AI Forensics Dossier is audit opinion
- AI Forensics Dossier is professional attestation
- AI Forensics Dossier reveals hidden chain of thought
- AI Forensics Dossier performs model mind-reading
- Atlas memory admission occurred
- Atlas memory write occurred
- memory candidate was written
- raw model output is final answer
- UCC review certifies compliance
- NIST compliance is certified
- NIST controls were ingested
- theorem validation proves theorem
- COOP-ENTROPY-DIVIDEND-00 is proven
- evidence ledger certifies truth
- Omega detection
- product release
- provider runtime
- population calibration

## Reproducibility

```powershell
python -c "from pathlib import Path; from coherence.product.triadic_llm_metrics_smoke import build_triadic_llm_metrics_smoke; from coherence.ucc.sophia_control_review import build_sophia_ucc_control_review; from coherence.product.ai_forensics_dossier import build_ai_forensics_dossier; root=Path(r'C:\UVLM\run_artifacts\triadic_llm_metrics_smoke'); bridge=root / 'bridge'; build_triadic_llm_metrics_smoke(root); build_sophia_ucc_control_review(bridge); build_ai_forensics_dossier(bridge)"
```
