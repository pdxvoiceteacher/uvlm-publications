# AEGIS Instruction Quarantine

AEGIS-INSTRUCTION-QUARANTINE-00 documents local deterministic instruction-quarantine artifacts that separate source content from source-borne instructions before downstream use.

## Doctrine

- AEGIS Instruction Quarantine
- AEGIS is the admissibility shield.
- Source content is not instruction authority.
- Source-borne instructions must be quarantined.
- Quarantined instructions cannot control downstream model, report, evidence-map, or control-package behavior.
- Safe excerpts may be preserved as evidence references.
- Instruction quarantine does not certify truth.
- Instruction quarantine does not certify compliance.
- Instruction quarantine does not authorize memory writes.
- Instruction quarantine does not execute source instructions.
- Human review remains required.

## Dashboard summary

- quarantine_case_count = 13
- clear_cases = 2
- clear_with_notice_cases = 1
- quarantine_for_human_review_cases = 3
- reject_fail_closed_cases = 5
- alarm_requires_elevated_review_cases = 2
- admission_scenario_count = 10
- clear_scenarios = 9
- quarantine_scenarios = 1
- quarantine_receipts = 1
- admission_builder_emits_instruction_quarantine_packets = true
- source_instruction_quarantine_scenario_emits_quarantine_receipt = true
- source_instruction_quarantine_scenario_allows_downstream_model_use = false
- source_instruction_quarantine_scenario_allows_report_generation = false
- source_instruction_quarantine_scenario_allows_evidence_map_use = false
- source_instruction_quarantine_scenario_allows_control_package_use = false
- safe_excerpts_allow_downstream_only_when_grounding_allows = true
- quarantine_reject_alarm_allow_downstream_model_use = false
- quarantine_reject_alarm_allow_report_generation = false
- quarantine_reject_alarm_allow_evidence_map_use = false
- quarantine_reject_alarm_allow_control_package_use = false
- quarantine_reject_alarm_require_quarantine_receipts = true
- source_content_executed = false
- instruction_executed = false
- hidden_file_read_performed = false
- directory_scan_performed = false
- connector_pull_performed = false
- provider_runtime_performed = false
- network_call_performed = false
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

## Quarantine statuses

- clear
- clear_with_notice
- quarantine_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Quarantine decisions

- allow
- allow_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Instruction pattern classes

- ignore_prior_instructions
- system_override_attempt
- hidden_file_access_request
- directory_scan_request
- connector_pull_request
- data_exfiltration_request
- memory_write_request
- compliance_certification_request
- legal_advice_request
- audit_pass_request
- final_answer_authority_request
- accepted_evidence_authority_request
- obfuscated_instruction_pattern

## Quarantine scenarios

- safe_source_excerpt
- benign_instruction_quoted_as_content
- source_instruction_quarantine_hold
- prompt_injection_quarantine_hold
- instruction_to_ignore_system_reject
- instruction_to_exfiltrate_alarm
- instruction_to_read_hidden_file_reject
- instruction_to_scan_directory_reject
- instruction_to_call_connector_reject
- instruction_to_write_memory_alarm
- instruction_to_claim_compliance_reject
- malformed_or_obfuscated_instruction_hold
- safe_source_excerpt_grounding_blocked

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

## Compatibility and downstream language

- Safe excerpts can allow downstream use only when grounding allows it.
- Quarantine, reject, and alarm cases allow no downstream model, report, evidence-map, or control-package use.
- Source-instruction quarantine emits a quarantine receipt.
- Quarantine receipts preserve no-instruction-executed and no-downstream-processing boundaries.
- Benign instructions quoted as content may clear with notice.
- Prompt-injection-like source content is held for human review.
- Data exfiltration and memory-write instructions escalate to alarm_requires_elevated_review.
- Hidden-file, directory-scan, connector-pull, compliance-certification, legal-advice, audit-pass, final-answer-authority, and accepted-evidence-authority instructions reject fail-closed.

## Reproducibility references

- evaluate_instruction_quarantine
- build_instruction_quarantine_receipt
- build_aegis_admission_contract
- build_grounding_binding_packet
- evaluate_source_scope
- evaluate_consent
- python/tests/aegis/test_aegis_instruction_quarantine.py
- python/tests/aegis/test_aegis_grounding_binding.py
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Relation to prior phases

- AEGIS-ADMISSION-CONTRACT-00 provides the admission contract and failure receipt behavior.
- AEGIS-SOURCE-SCOPE-CONSENT-00 provides reusable source-scope and consent checks consumed by admission.
- AEGIS-GROUNDING-BINDING-00 binds compatible admission, source-scope, and consent packets to source hashes, evidence refs, and receipt refs.
- AEGIS-INSTRUCTION-QUARANTINE-00 separates source content from source-borne instructions before downstream use.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides bounded local ingress context.
- ENTERPRISE-AI-RISK-TAXONOMY-STACK-DESIGN-00 provides multi-view risk taxonomy context.
- PRODUCT-READINESS-ROADMAP-MATRIX-00 lists instruction quarantine as an AEGIS follow-up validation step.

## Artifact references

- docs/AEGIS_INSTRUCTION_QUARANTINE.md
- python/src/coherence/aegis/instruction_quarantine.py
- python/src/coherence/aegis/admission.py
- python/src/coherence/aegis/grounding_binding.py
- python/src/coherence/aegis/source_scope.py
- python/src/coherence/aegis/consent_check.py
- python/src/coherence/aegis/policy.py
- schema/bridge/aegis_instruction_quarantine_packet.schema.json
- schema/bridge/aegis_instruction_quarantine_receipt.schema.json
- schema/bridge/aegis_instruction_quarantine_non_authority_boundary.schema.json
- python/tests/aegis/test_aegis_instruction_quarantine.py
- python/tests/aegis/test_aegis_grounding_binding.py
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Allowed claim

AEGIS-INSTRUCTION-QUARANTINE-00 implements local deterministic AEGIS instruction-quarantine artifacts that separate source content from source-borne instructions, preserve safe excerpt metadata, quarantine prompt-injection and instruction-like content for human review or fail-closed rejection, and prevent quarantined instructions from influencing downstream model-candidate, report-generation, evidence-map, or control-package use, while preserving that instruction quarantine checks admissibility and safety boundaries rather than truth and does not execute instructions, read hidden files, scan directories, pull connectors, call providers, perform network calls, write memory, admit Atlas memory, export traces, federate PMR, certify compliance, provide legal advice, pass audits, claim product readiness, release product, certify truth, grant final-answer authority, or grant accepted-evidence authority.

## Blocked claims

- instruction quarantine certifies truth
- instruction quarantine certifies source truth
- instruction quarantine authorizes memory write
- instruction quarantine authorizes deployment
- instruction quarantine certifies compliance
- instruction quarantine provides legal advice
- instruction quarantine passes audit
- instruction quarantine releases product
- instruction quarantine proves product readiness
- instruction quarantine grants final-answer authority
- instruction quarantine grants accepted-evidence authority
- quarantined instruction executed
- source instruction controls downstream model
- source instruction controls report generation
- source instruction controls evidence map
- source instruction controls control package
- safe excerpt means truth certified
- quarantine receipt certifies compliance
- clear means truth certified
- clear_with_notice means accepted evidence
- quarantine_for_human_review means audit pass
- reject_fail_closed means legal determination
- alarm_requires_elevated_review means compliance breach

## Non-authority guardrails

- instruction_quarantine_is_not_truth_certification
- instruction_quarantine_is_not_source_truth_certification
- instruction_quarantine_is_not_memory_write_authorization
- instruction_quarantine_is_not_deployment_authority
- instruction_quarantine_is_not_compliance_certification
- instruction_quarantine_is_not_legal_advice
- instruction_quarantine_is_not_audit_pass
- instruction_quarantine_is_not_attestation_success
- instruction_quarantine_is_not_product_release
- instruction_quarantine_is_not_product_readiness
- instruction_quarantine_is_not_final_answer_authority
- instruction_quarantine_is_not_accepted_evidence_authority
- instruction_quarantine_does_not_execute_source_instructions
- instruction_quarantine_does_not_write_memory
- instruction_quarantine_does_not_admit_atlas_memory
- instruction_quarantine_does_not_export_traces
- instruction_quarantine_does_not_federate_pmr
- human_review_required

Publication sync grants no runtime authority.
