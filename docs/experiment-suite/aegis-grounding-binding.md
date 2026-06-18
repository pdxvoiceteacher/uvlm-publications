# AEGIS Grounding Binding

AEGIS-GROUNDING-BINDING-00 documents local deterministic grounding-binding artifacts for compatible admission, source-scope, and consent packets.

## Doctrine

- AEGIS Grounding Binding
- AEGIS is the admissibility shield.
- Grounding binding binds admissible source references to evidence references.
- Grounding binding does not certify source truth.
- Grounding binding does not certify compliance.
- Grounding binding does not authorize memory writes.
- A source is usable downstream only when admission, source-scope, and consent decisions are compatible.
- Failed or held grounding creates a grounding failure receipt, not a governed RequestEnvelope.
- Human review remains required.

## Dashboard summary

- grounding_case_count = 10
- bound_cases = 1
- bound_with_controls_cases = 1
- hold_cases = 2
- reject_cases = 5
- alarm_cases = 1
- admission_scenario_count = 10
- admitted_scenarios_with_downstream_use = 2
- blocked_scenarios_without_downstream_use = 8
- grounding_failure_receipts = 8
- admission_builder_emits_grounding_binding_packets = true
- bound_cases_allow_downstream_use = true
- bound_with_controls_cases_allow_downstream_use = true
- hold_reject_alarm_allow_downstream_model_use = false
- hold_reject_alarm_allow_report_generation = false
- hold_reject_alarm_allow_evidence_map_use = false
- hold_reject_alarm_allow_control_package_use = false
- request_envelope_allowed_for_bound = true
- request_envelope_allowed_for_bound_with_controls = true
- request_envelope_allowed_for_hold_reject_alarm = false
- grounding_failure_receipt_required_for_hold_reject_alarm = true
- source_truth_certified = false
- compliance_certification_emitted = false
- legal_advice_emitted = false
- audit_pass_claimed = false
- truth_certification_emitted = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false
- provider_runtime_performed = false
- network_call_performed = false
- hidden_file_read_performed = false
- directory_scan_performed = false
- connector_pull_performed = false
- product_readiness_claimed = false
- product_release_performed = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false

## Grounding statuses

- bound
- bound_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Grounding decisions

- allow
- allow_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Grounding scenarios

- valid_grounding_binding
- pasted_excerpt_grounding_with_controls
- missing_source_hash_reject
- missing_evidence_ref_hold
- admission_not_admitted_reject
- source_scope_not_allowed_reject
- consent_not_allowed_reject
- hash_mismatch_alarm
- source_instruction_quarantine_hold
- unsupported_evidence_ref_reject

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

## Compatibility language

- compatible admission decisions are admit and admit_with_controls
- compatible source-scope decisions are allow and allow_with_controls
- compatible consent decisions are allow and allow_with_controls
- bound and bound_with_controls may allow downstream model, report, evidence-map, and control-package use
- hold, reject, and alarm grounding decisions do not allow downstream model, report, evidence-map, or control-package use
- hash mismatch escalates to alarm_requires_elevated_review
- missing source hash rejects fail-closed
- missing evidence ref holds for human review
- unsupported evidence ref rejects fail-closed

## Reproducibility references

- build_grounding_binding_packet
- build_grounding_failure_receipt
- build_aegis_admission_contract
- evaluate_source_scope
- evaluate_consent
- python/tests/aegis/test_aegis_grounding_binding.py
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Relation to prior phases

- AEGIS-ADMISSION-CONTRACT-00 provides the admission contract and failure receipt behavior.
- AEGIS-SOURCE-SCOPE-CONSENT-00 provides reusable source-scope and consent checks consumed by admission.
- AEGIS-GROUNDING-BINDING-00 binds compatible admission, source-scope, and consent packets to source hashes, evidence refs, and receipt refs.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides bounded local ingress context.
- ENTERPRISE-AI-RISK-TAXONOMY-STACK-DESIGN-00 provides multi-view risk taxonomy context.
- PRODUCT-READINESS-ROADMAP-MATRIX-00 lists grounding binding as an AEGIS follow-up validation step.

## Artifact references

- docs/AEGIS_GROUNDING_BINDING.md
- python/src/coherence/aegis/grounding_binding.py
- python/src/coherence/aegis/admission.py
- python/src/coherence/aegis/source_scope.py
- python/src/coherence/aegis/consent_check.py
- python/src/coherence/aegis/policy.py
- schema/bridge/aegis_grounding_binding_packet.schema.json
- schema/bridge/aegis_grounding_failure_receipt.schema.json
- schema/bridge/aegis_grounding_binding_non_authority_boundary.schema.json
- python/tests/aegis/test_aegis_grounding_binding.py
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Allowed claim

AEGIS-GROUNDING-BINDING-00 implements local deterministic AEGIS grounding-binding artifacts that bind admitted source-scope and consent packets to canonical source references, content hashes, evidence references, and receipt links before downstream model-candidate, report-generation, evidence-map, or control-package use, while preserving that grounding binding checks admissibility linkage rather than truth and does not read hidden files, scan directories, pull connectors, call providers, perform network calls, write memory, admit Atlas memory, export traces, federate PMR, certify compliance, provide legal advice, pass audits, claim product readiness, release product, certify truth, grant final-answer authority, or grant accepted-evidence authority.

## Blocked claims

- grounding binding certifies truth
- grounding binding certifies source truth
- grounding binding authorizes memory write
- grounding binding authorizes deployment
- grounding binding certifies compliance
- grounding binding provides legal advice
- grounding binding passes audit
- grounding binding releases product
- grounding binding proves product readiness
- grounding binding grants final-answer authority
- grounding binding grants accepted-evidence authority
- failed grounding creates RequestEnvelope
- hash binding proves content truth
- evidence ref certifies compliance
- receipt ref certifies truth
- bound means truth certified
- bound_with_controls means audit passed
- downstream model use means final-answer authority
- report generation allowed means compliance certification
- evidence-map use allowed means accepted evidence
- control-package use allowed means product release

## Non-authority guardrails

- grounding_binding_is_not_truth_certification
- grounding_binding_is_not_source_truth_certification
- grounding_binding_is_not_memory_write_authorization
- grounding_binding_is_not_deployment_authority
- grounding_binding_is_not_compliance_certification
- grounding_binding_is_not_legal_advice
- grounding_binding_is_not_audit_pass
- grounding_binding_is_not_attestation_success
- grounding_binding_is_not_product_release
- grounding_binding_is_not_product_readiness
- grounding_binding_is_not_final_answer_authority
- grounding_binding_is_not_accepted_evidence_authority
- grounding_binding_does_not_write_memory
- grounding_binding_does_not_admit_atlas_memory
- grounding_binding_does_not_export_traces
- grounding_binding_does_not_federate_pmr
- human_review_required

Publication sync grants no runtime authority. live_bounded_local means bounded local validation. live_bounded_local does not mean general availability. Publication visibility does not mean product release. Status rendering does not mean runtime enforcement.
