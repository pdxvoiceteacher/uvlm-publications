# AEGIS Admission Contract

AEGIS-ADMISSION-CONTRACT-00 documents the local deterministic AEGIS admission contract.

## AEGIS doctrine

- AEGIS Admission Contract
- AEGIS is the admissibility shield.
- AEGIS decides admissibility, not truth.
- No configured AI work enters the Triadic Brain without AEGIS admission.
- Failed admission creates a failure receipt, not a governed RequestEnvelope.
- AEGIS admission is not truth certification.
- AEGIS admission is not memory write authorization.
- AEGIS admission is not deployment authority.
- AEGIS admission is not compliance certification.
- AEGIS admission is not legal advice.
- AEGIS admission is not audit pass.
- Human review remains required.

## Invariant summary

- scenario_count = 10
- admit_decisions = 1
- admit_with_controls_decisions = 1
- hold_for_human_review_decisions = 2
- reject_fail_closed_decisions = 5
- alarm_requires_elevated_review_decisions = 1
- failed_held_alarm_emit_failure_receipt = true
- failed_held_alarm_create_request_envelope = false
- admitted_emit_request_envelope_ref = true
- admitted_emit_failure_receipt = false
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

## Decisions

- admit
- admit_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Scenarios

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

## Artifact references

- docs/AEGIS_ADMISSION_CONTRACT.md
- python/src/coherence/aegis/__init__.py
- python/src/coherence/aegis/types.py
- python/src/coherence/aegis/policy.py
- python/src/coherence/aegis/admission.py
- python/src/coherence/aegis/failure_receipt.py
- schema/bridge/aegis_admission_packet.schema.json
- schema/bridge/aegis_failure_receipt.schema.json
- schema/bridge/aegis_admission_non_authority_boundary.schema.json
- python/tests/aegis/test_aegis_admission_contract.py

## Allowed claim

AEGIS-ADMISSION-CONTRACT-00 implements a local deterministic AEGIS admission contract that emits admission packets and failure receipts for configured AI work events, deciding whether an event is admitted, admitted with controls, held for human review, rejected fail-closed, or escalated to alarm, while preserving that AEGIS decides admissibility rather than truth and does not perform provider calls, network calls, memory writes, Atlas admission, trace export, PMR federation, product readiness, product release, compliance certification, legal advice, audit pass, attestation success, truth certification, final-answer authority, or accepted-evidence authority.

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

Publication sync grants no runtime authority. live_bounded_local means bounded local validation. live_bounded_local does not mean general availability. Publication visibility does not mean product release. Status rendering does not mean runtime enforcement.
