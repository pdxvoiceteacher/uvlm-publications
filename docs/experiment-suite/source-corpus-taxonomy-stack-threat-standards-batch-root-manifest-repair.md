# Taxonomy Stack Threat Standards Root Manifest Repair

SOURCE-CORPUS-TAXONOMY-STACK-THREAT-STANDARDS-BATCH-ROOT-MANIFEST-REPAIR-00 repairs source-corpus root manifest discoverability.

## Dashboard summary

- repair_status = completed
- root_batch_manifest_entry = taxonomy_stack_threat_standards_batch_20260613
- manifest_ref_present = true
- sha256sums_ref_present = true
- summary_ref_present = true
- aliases_ref_present = true
- raw_files_committed = false
- authority_emitted = false

## Artifact references

- docs/provenance/source_reports/manifest.json
- taxonomy_stack_threat_standards_batch_20260613
- docs/provenance/source_reports/2026-06/taxonomy_stack_threat_standards_batch_20260613.json
- docs/provenance/source_reports/2026-06/taxonomy_stack_threat_standards_batch_sha256sums_20260613.txt
- docs/provenance/source_reports/2026-06/taxonomy_stack_threat_standards_batch_summary_20260613.md
- docs/provenance/source_reports/2026-06/taxonomy_stack_threat_standards_batch_aliases_20260613.json

## Allowed claim

PUBLICATION-SYNC-AEGIS-SOURCE-SCOPE-CONSENT-DECISION-VOCAB-REPAIR-00 repairs the publication decision vocabulary for AEGIS-SOURCE-SCOPE-CONSENT-00 by distinguishing source-scope/consent decisions such as allow and allow_with_controls from admission decisions such as admit and admit_with_controls, while preserving that these terms are deterministic admissibility labels only and do not certify truth, authorize memory writes, grant deployment authority, certify compliance, provide legal advice, pass audits, claim product readiness, release product, grant final-answer authority, or grant accepted-evidence authority.

## Non-authority guardrails

- aegis_admission_is_not_truth_certification
- aegis_admission_is_not_memory_write_authorization
- aegis_admission_is_not_deployment_authority
- aegis_admission_is_not_compliance_certification
- aegis_admission_is_not_legal_advice
- aegis_admission_is_not_audit_pass
- aegis_admission_is_not_attestation_success
- aegis_admission_is_not_product_release
- aegis_admission_is_not_product_readiness
- aegis_admission_is_not_final_answer_authority
- aegis_admission_is_not_accepted_evidence_authority
- aegis_admission_does_not_write_memory
- aegis_admission_does_not_admit_atlas_memory
- aegis_admission_does_not_export_traces
- aegis_admission_does_not_federate_pmr
- risk_taxonomy_is_not_compliance_certification
- risk_taxonomy_is_not_legal_advice
- risk_taxonomy_is_not_audit_pass
- risk_taxonomy_is_not_attestation_success
- risk_taxonomy_is_not_product_readiness
- risk_taxonomy_is_not_product_release
- risk_taxonomy_is_not_truth_certification
- risk_taxonomy_is_not_final_answer_authority
- risk_taxonomy_is_not_accepted_evidence_authority
- risk_taxonomy_does_not_write_memory
- risk_taxonomy_does_not_admit_atlas_memory
- risk_taxonomy_does_not_export_traces
- risk_taxonomy_does_not_federate_pmr
- human_review_required
- professional_review_required_for_compliance_use

Publication sync grants no runtime authority.
