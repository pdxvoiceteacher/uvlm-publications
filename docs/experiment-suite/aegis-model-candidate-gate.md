# AEGIS Model Candidate Gate

AEGIS-MODEL-CANDIDATE-GATE-00 documents local deterministic model-candidate gate artifacts that evaluate upstream AEGIS compatibility before any downstream model-candidate eligibility.

## Doctrine

- AEGIS Model Candidate Gate
- AEGIS is the admissibility shield.
- A model candidate may be formed only from compatible admission, source-scope, consent, grounding, and instruction-quarantine packets.
- Held, rejected, alarmed, quarantined, missing, or incompatible upstream packets block model-candidate formation.
- Model-candidate gate does not call providers.
- Model-candidate gate does not generate model output.
- Model-candidate gate does not certify truth.
- Model-candidate gate does not authorize final answers.
- Model-candidate gate does not authorize memory writes.
- Human review remains required.

## Dashboard summary

- gate_case_count = 17
- candidate_allowed_cases = 1
- candidate_allowed_with_controls_cases = 1
- hold_cases = 1
- reject_cases = 12
- alarm_cases = 2
- admission_scenario_count = 10
- model_candidate_allowed_scenarios = 2
- model_candidate_blocked_scenarios = 8
- model_candidate_failure_receipts = 8
- admission_builder_emits_model_candidate_gate_packets = true
- admitted_scenarios_may_be_model_candidate_allowed = true
- admitted_scenarios_create_model_candidate = false
- held_rejected_alarm_scenarios_model_candidate_blocked = true
- held_rejected_alarm_scenarios_emit_failure_receipts = true
- model_candidate_allowed_for_allowed_statuses = true
- model_candidate_created = false
- provider_runtime_allowed = false
- provider_runtime_performed = false
- network_call_performed = false
- model_output_generated = false
- source_content_executed = false
- instruction_executed = false
- hidden_file_read_performed = false
- directory_scan_performed = false
- connector_pull_performed = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false
- compliance_certification_emitted = false
- legal_advice_emitted = false
- audit_pass_claimed = false
- truth_certification_emitted = false
- product_readiness_claimed = false
- product_release_performed = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false

## Model-candidate gate statuses

- candidate_allowed
- candidate_allowed_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Model-candidate gate decisions

- allow
- allow_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Compatibility vocabulary

- compatible admission decisions are admit and admit_with_controls
- compatible source-scope decisions are allow and allow_with_controls
- compatible consent decisions are allow and allow_with_controls
- compatible grounding statuses are bound and bound_with_controls
- compatible instruction-quarantine statuses are clear and clear_with_notice
- allowed candidate purposes are configured_ai_work and evidence_support_report_generation

## Model-candidate scenarios

- valid_model_candidate_gate
- valid_model_candidate_with_controls
- missing_admission_packet_reject
- missing_source_scope_packet_reject
- missing_consent_packet_reject
- missing_grounding_packet_reject
- missing_instruction_quarantine_packet_reject
- admission_not_admitted_reject
- source_scope_not_allowed_reject
- consent_not_allowed_reject
- grounding_not_bound_reject
- grounding_alarm_blocks_candidate
- instruction_quarantine_blocks_candidate
- instruction_quarantine_alarm_blocks_candidate
- downstream_use_not_allowed_reject
- unsupported_candidate_purpose_reject
- candidate_requires_human_review_hold

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

## Downstream/prototype language

- Candidate eligibility is not model output.
- model_candidate_allowed = true for allowed/allowed-with-controls statuses
- model_candidate_allowed does not mean model_candidate_created.
- This prototype keeps model_candidate_created false.
- This prototype keeps provider_runtime_allowed false.
- This prototype keeps provider_runtime_performed false.
- This prototype keeps model_output_generated false.
- Hold, reject, and alarm outcomes emit model-candidate failure receipts.
- Missing upstream packets fail closed.
- Quarantined sources cannot form model candidates without review.
- Unbound grounding blocks model candidates.
- Missing consent blocks model candidates.

## Reproducibility references

- evaluate_model_candidate_gate
- build_model_candidate_gate_failure_receipt
- build_aegis_admission_contract
- evaluate_instruction_quarantine
- build_grounding_binding_packet
- evaluate_source_scope
- evaluate_consent
- python/tests/aegis/test_aegis_model_candidate_gate.py
- python/tests/aegis/test_aegis_instruction_quarantine.py
- python/tests/aegis/test_aegis_grounding_binding.py
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Relation to prior phases

- AEGIS-ADMISSION-CONTRACT-00 provides the admission contract and failure receipt behavior.
- AEGIS-SOURCE-SCOPE-CONSENT-00 provides reusable source-scope and consent checks consumed by admission.
- AEGIS-GROUNDING-BINDING-00 binds compatible admission, source-scope, and consent packets to source hashes, evidence refs, and receipt refs.
- AEGIS-INSTRUCTION-QUARANTINE-00 separates source content from source-borne instructions before downstream use.
- AEGIS-MODEL-CANDIDATE-GATE-00 gates model-candidate eligibility on compatible upstream AEGIS packets.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides bounded local ingress context.
- ENTERPRISE-AI-RISK-TAXONOMY-STACK-DESIGN-00 provides multi-view risk taxonomy context.
- PRODUCT-READINESS-ROADMAP-MATRIX-00 lists local runtime enforcement adapter as an AEGIS follow-up validation step.

## Artifact references

- docs/AEGIS_MODEL_CANDIDATE_GATE.md
- python/src/coherence/aegis/model_candidate_gate.py
- python/src/coherence/aegis/admission.py
- python/src/coherence/aegis/instruction_quarantine.py
- python/src/coherence/aegis/grounding_binding.py
- python/src/coherence/aegis/source_scope.py
- python/src/coherence/aegis/consent_check.py
- python/src/coherence/aegis/policy.py
- schema/bridge/aegis_model_candidate_gate_packet.schema.json
- schema/bridge/aegis_model_candidate_gate_failure_receipt.schema.json
- schema/bridge/aegis_model_candidate_gate_non_authority_boundary.schema.json
- python/tests/aegis/test_aegis_model_candidate_gate.py
- python/tests/aegis/test_aegis_instruction_quarantine.py
- python/tests/aegis/test_aegis_grounding_binding.py
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Allowed claim

AEGIS-MODEL-CANDIDATE-GATE-00 implements local deterministic AEGIS model-candidate gate artifacts that evaluate whether compatible admission, source-scope, consent, grounding, and instruction-quarantine packets permit a downstream model candidate to be formed, while preserving that the prototype does not create model candidates, call providers, perform network calls, generate model output, execute source instructions, read hidden files, scan directories, pull connectors, write memory, admit Atlas memory, export traces, federate PMR, certify compliance, provide legal advice, pass audits, claim product readiness, release product, certify truth, grant final-answer authority, or grant accepted-evidence authority.

## Blocked claims

- model candidate gate certifies truth
- model candidate gate certifies source truth
- model candidate gate authorizes memory write
- model candidate gate authorizes deployment
- model candidate gate certifies compliance
- model candidate gate provides legal advice
- model candidate gate passes audit
- model candidate gate releases product
- model candidate gate proves product readiness
- model candidate gate grants final-answer authority
- model candidate gate grants accepted-evidence authority
- model candidate gate calls provider
- model candidate gate generates model output
- allowed candidate means final answer
- allowed candidate means accepted evidence
- candidate_allowed means truth certified
- candidate_allowed_with_controls means audit passed
- failed model-candidate gate creates model output
- quarantined source can form model candidate without review
- rejected source can form model candidate
- alarmed source can form model candidate
- missing consent can form model candidate
- unbound grounding can form model candidate
- model_candidate_allowed means model_candidate_created
- provider_runtime_allowed means provider_runtime_performed
- model output generated by AEGIS gate
- candidate gate trained a model
- candidate gate selected a final answer

## Non-authority guardrails

- model_candidate_gate_is_not_truth_certification
- model_candidate_gate_is_not_source_truth_certification
- model_candidate_gate_is_not_memory_write_authorization
- model_candidate_gate_is_not_deployment_authority
- model_candidate_gate_is_not_compliance_certification
- model_candidate_gate_is_not_legal_advice
- model_candidate_gate_is_not_audit_pass
- model_candidate_gate_is_not_attestation_success
- model_candidate_gate_is_not_product_release
- model_candidate_gate_is_not_product_readiness
- model_candidate_gate_is_not_final_answer_authority
- model_candidate_gate_is_not_accepted_evidence_authority
- model_candidate_gate_does_not_call_provider
- model_candidate_gate_does_not_generate_model_output
- model_candidate_gate_does_not_execute_source_instructions
- model_candidate_gate_does_not_write_memory
- model_candidate_gate_does_not_admit_atlas_memory
- model_candidate_gate_does_not_export_traces
- model_candidate_gate_does_not_federate_pmr
- human_review_required

## Runtime boundary

Publication sync grants no runtime authority, model-candidate creation, provider runtime, model output generation, network calls, source-instruction execution, hidden-file reads, directory scans, connector pulls, memory writes, Atlas admission, trace export, PMR federation, package execution, product readiness, product release, compliance certification, legal advice, audit pass, truth certification, final-answer authority, accepted-evidence authority, model training, or review skipping.
