# AEGIS Source Scope and Consent

AEGIS-SOURCE-SCOPE-CONSENT-00 documents local deterministic AEGIS source-scope and consent checks for configured AI work events.

## Doctrine

- AEGIS Source Scope and Consent
- AEGIS is the admissibility shield.
- Source scope must be explicit.
- Consent must be explicit for configured AI work.
- Hidden-file access is rejected fail-closed.
- Directory scans are rejected fail-closed.
- Connector sources require explicit connector scope.
- Pasted excerpts may be admitted with controls.
- Missing consent rejects fail-closed.
- allow and allow_with_controls are source-scope/consent decisions, not admission outcomes.
- admit and admit_with_controls are admission decisions, not source-scope/consent decisions.
- Failed scope/consent checks create failure receipts, not governed RequestEnvelope artifacts.
- Source-scope checks do not certify truth.
- Consent checks do not certify truth.
- Source-scope checks do not authorize memory writes.
- Consent checks do not authorize memory writes.
- Human review remains required.

## Dashboard summary

- source_scope_decisions = ['allow', 'allow_with_controls', 'hold_for_human_review', 'reject_fail_closed', 'alarm_requires_elevated_review']
- consent_decisions = ['allow', 'allow_with_controls', 'hold_for_human_review', 'reject_fail_closed', 'alarm_requires_elevated_review']
- admission_decisions = ['admit', 'admit_with_controls', 'hold_for_human_review', 'reject_fail_closed', 'alarm_requires_elevated_review']
- source_scope_case_count = 8
- consent_case_count = 7
- admission_scenario_count = 10
- admit_decisions = 1
- admit_with_controls_decisions = 1
- hold_for_human_review_decisions = 2
- reject_fail_closed_decisions = 5
- alarm_requires_elevated_review_decisions = 1
- source_scope_packets_emitted = true
- consent_packets_emitted = true
- source_scope_consent_boundary_packets_emitted = true
- failed_held_alarm_create_request_envelope = false
- failed_held_alarm_emit_failure_receipt = true
- admitted_emit_request_envelope_ref = true
- admitted_emit_failure_receipt = false
- hidden_file_read_performed = false
- directory_scan_performed = false
- connector_pull_performed = false
- consent_write_performed = false
- provider_runtime_performed = false
- network_call_performed = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false
- product_readiness_claimed = false
- product_release_performed = false
- compliance_certification_emitted = false
- legal_advice_emitted = false
- audit_pass_claimed = false
- truth_certification_emitted = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false

## Source-scope statuses

- scoped
- scoped_with_controls
- missing_scope
- hidden_file_rejected
- directory_scan_rejected
- connector_scope_missing
- unsupported_source_kind
- source_instruction_quarantine

## Consent statuses

- consent_valid
- consent_valid_with_controls
- consent_missing
- consent_scope_mismatch
- consent_revoked
- consent_expired
- consent_requires_human_review

## Source-scope / consent decisions

- allow
- allow_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Admission decisions

- admit
- admit_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Source-scope scenarios

- explicit_selected_local_file_allowed
- pasted_excerpt_allowed_with_controls
- missing_scope_hold
- hidden_file_reject
- directory_scan_reject
- connector_without_scope_reject
- unsupported_source_kind_reject
- source_instruction_quarantine_hold

## Consent scenarios

- explicit_consent_valid
- pasted_excerpt_consent_valid_with_controls
- consent_missing_reject
- consent_scope_mismatch_reject
- consent_revoked_reject
- consent_expired_reject
- consent_requires_human_review_hold

## Admission integration scenarios

- valid_explicit_local_file_admit
- valid_pasted_excerpt_admit_with_controls
- missing_scope_hold_for_human_review
- missing_consent_reject_fail_closed
- hidden_file_reject_fail_closed
- directory_scan_reject_fail_closed
- connector_without_scope_reject_fail_closed
- model_candidate_without_sonya_reject_fail_closed
- source_instruction_quarantine_hold
- side_effecting_action_alarm

## Reproducibility references

- evaluate_source_scope
- evaluate_consent
- build_aegis_admission_contract
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Relation to prior phases

- AEGIS-ADMISSION-CONTRACT-00 provides the admission contract and failure receipt behavior.
- AEGIS-SOURCE-SCOPE-CONSENT-00 provides reusable source-scope and consent checks consumed by admission.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides bounded local ingress context.
- ENTERPRISE-AI-RISK-TAXONOMY-STACK-DESIGN-00 provides multi-view risk taxonomy context.
- PRODUCT-READINESS-ROADMAP-MATRIX-00 lists source-scope and consent follow-up as product roadmap validation.

## Artifact references

- docs/AEGIS_SOURCE_SCOPE_CONSENT.md
- python/src/coherence/aegis/source_scope.py
- python/src/coherence/aegis/consent_check.py
- python/src/coherence/aegis/admission.py
- python/src/coherence/aegis/policy.py
- python/src/coherence/aegis/failure_receipt.py
- schema/bridge/aegis_source_scope_packet.schema.json
- schema/bridge/aegis_consent_packet.schema.json
- schema/bridge/aegis_source_scope_consent_non_authority_boundary.schema.json
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Allowed claim

AEGIS-SOURCE-SCOPE-CONSENT-00 implements local deterministic AEGIS source-scope and consent checks for configured AI work events, evaluating explicit local file selection, pasted excerpts, missing scope, hidden files, directory scans, connector scope, source-instruction quarantine, valid consent, missing consent, mismatched consent, revoked consent, expired consent, and human-review consent states, while preserving that AEGIS checks admissibility rather than truth and do not perform hidden-file reads, directory scans, connector pulls, provider calls, network calls, memory writes, Atlas admission, trace export, PMR federation, product readiness, product release, compliance certification, legal advice, audit pass, truth certification, final-answer authority, or accepted-evidence authority.

## Decision vocabulary repair allowed claim

PUBLICATION-SYNC-AEGIS-SOURCE-SCOPE-CONSENT-DECISION-VOCAB-REPAIR-00 repairs the publication decision vocabulary for AEGIS-SOURCE-SCOPE-CONSENT-00 by distinguishing source-scope/consent decisions such as allow and allow_with_controls from admission decisions such as admit and admit_with_controls, while preserving that these terms are deterministic admissibility labels only and do not certify truth, authorize memory writes, grant deployment authority, certify compliance, provide legal advice, pass audits, claim product readiness, release product, grant final-answer authority, or grant accepted-evidence authority.

## Blocked claims

- source scope check certifies truth
- source scope check authorizes memory write
- source scope check authorizes deployment
- source scope check certifies compliance
- source scope check provides legal advice
- source scope check passes audit
- source scope check releases product
- source scope check proves product readiness
- source scope check grants final-answer authority
- source scope check grants accepted-evidence authority
- consent check certifies truth
- consent check authorizes memory write
- consent check authorizes deployment
- consent check certifies compliance
- consent check provides legal advice
- consent check passes audit
- consent check releases product
- consent check proves product readiness
- consent check grants final-answer authority
- consent check grants accepted-evidence authority
- hidden file is allowed by default
- directory scan is allowed by default
- connector pull is allowed without explicit scope
- missing consent can proceed
- failed scope check creates RequestEnvelope
- failed consent check creates RequestEnvelope
- allow means final-answer authority
- allow_with_controls means accepted-evidence authority
- source-scope allow certifies truth
- consent allow certifies truth
- allow means compliance certification
- allow_with_controls means audit pass
- allow means product release
- allow_with_controls means product readiness
- allow means memory write authorization
- allow means deployment authority

## Non-authority guardrails

- source_scope_check_is_not_truth_certification
- source_scope_check_is_not_memory_write_authorization
- source_scope_check_is_not_deployment_authority
- source_scope_check_is_not_compliance_certification
- source_scope_check_is_not_legal_advice
- source_scope_check_is_not_audit_pass
- source_scope_check_is_not_product_release
- source_scope_check_is_not_product_readiness
- source_scope_check_is_not_final_answer_authority
- source_scope_check_is_not_accepted_evidence_authority
- source_scope_check_does_not_write_memory
- source_scope_check_does_not_admit_atlas_memory
- source_scope_check_does_not_export_traces
- source_scope_check_does_not_federate_pmr
- consent_check_is_not_truth_certification
- consent_check_is_not_memory_write_authorization
- consent_check_is_not_deployment_authority
- consent_check_is_not_compliance_certification
- consent_check_is_not_legal_advice
- consent_check_is_not_audit_pass
- consent_check_is_not_product_release
- consent_check_is_not_product_readiness
- consent_check_is_not_final_answer_authority
- consent_check_is_not_accepted_evidence_authority
- consent_check_does_not_write_memory
- consent_check_does_not_admit_atlas_memory
- consent_check_does_not_export_traces
- consent_check_does_not_federate_pmr
- human_review_required

Publication sync grants no runtime authority.
