# AEGIS Action Firewall

AEGIS-ACTION-FIREWALL-00 documents local deterministic action-firewall artifacts that evaluate proposed action eligibility after model-candidate gating and explicit operator authorization.

## Doctrine

- AEGIS Action Firewall
- AEGIS is the admissibility shield.
- Model-candidate eligibility is not action authority.
- Side-effecting actions require explicit operator authorization.
- No action may proceed merely because a model candidate is allowed.
- The action firewall does not execute tools.
- The action firewall does not perform actions.
- The action firewall does not write files.
- The action firewall does not call connectors.
- The action firewall does not call networks or providers.
- The action firewall does not write memory.
- The action firewall does not grant final-answer authority.
- Human review remains required.

## Dashboard summary

- action_firewall_case_count = 28
- action_allowed_cases = 1
- action_allowed_with_controls_cases = 2
- hold_cases = 3
- reject_cases = 18
- alarm_cases = 4
- admission_scenario_count = 10
- action_allowed_scenarios = 2
- action_blocked_scenarios = 8
- action_firewall_failure_receipts = 8
- admission_builder_emits_action_firewall_packets = true
- action_allowed_scenarios_remain_not_performed = true
- blocked_scenarios_emit_action_firewall_failure_receipts = true
- action_allowed_for_allowed_statuses = true
- action_performed = false
- tool_execution_performed = false
- file_write_performed = false
- file_delete_performed = false
- connector_pull_performed = false
- connector_push_performed = false
- provider_runtime_performed = false
- network_call_performed = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false
- package_install_performed = false
- package_activation_performed = false
- package_execution_performed = false
- payment_processing_performed = false
- subscription_billing_performed = false
- marketplace_download_performed = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false
- compliance_certification_emitted = false
- legal_advice_emitted = false
- audit_pass_claimed = false
- truth_certification_emitted = false
- product_readiness_claimed = false
- product_release_performed = false

## Action firewall statuses

- action_allowed
- action_allowed_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Action firewall decisions

- allow
- allow_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Action kinds

- noop
- local_preview
- report_draft_preview
- file_write
- file_delete
- connector_pull
- connector_push
- network_call
- provider_call
- memory_write
- atlas_memory_admission
- trace_export
- pmr_federation
- package_install
- package_activation
- package_execution
- payment_processing
- subscription_billing
- marketplace_download
- final_answer_emit
- accepted_evidence_mark

## Action-firewall scenarios

- safe_noop_action_allowed
- local_preview_allowed_with_controls
- report_draft_preview_allowed_with_controls
- missing_model_candidate_gate_reject
- model_candidate_not_allowed_reject
- runtime_side_effect_detected_reject
- missing_operator_authorization_reject
- operator_authorization_mismatch_reject
- destructive_action_hold
- file_write_scenario
- file_delete_scenario
- connector_pull_scenario
- connector_push_scenario
- network_call_scenario
- provider_call_scenario
- memory_write_scenario
- atlas_memory_admission_scenario
- trace_export_scenario
- pmr_federation_scenario
- package_install_scenario
- package_activation_scenario
- package_execution_scenario
- payment_processing_scenario
- subscription_billing_scenario
- marketplace_download_scenario
- final_answer_emit_scenario
- accepted_evidence_mark_scenario
- unsupported_action_kind_reject

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

## Compatibility and action language

- safe action kinds are noop, local_preview, and report_draft_preview
- local_preview and report_draft_preview are preview-only actions
- action_allowed does not mean action_performed
- action_allowed_with_controls does not mean action_performed
- model-candidate eligibility is not action authority
- missing model-candidate gate rejects fail-closed
- missing operator authorization rejects fail-closed
- mismatched operator authorization rejects fail-closed
- destructive actions hold for human review
- file writes reject fail-closed
- file deletes alarm
- connector pulls reject fail-closed
- connector pushes alarm
- network calls reject fail-closed
- provider calls reject fail-closed
- memory writes alarm
- Atlas memory admission alarms
- trace export holds for human review
- PMR federation holds for human review
- package install, activation, and execution reject fail-closed
- payment processing, subscription billing, and marketplace download reject fail-closed
- final answer emit rejects fail-closed
- accepted evidence mark rejects fail-closed

## Reproducibility references

- evaluate_action_firewall
- build_action_firewall_failure_receipt
- evaluate_model_candidate_gate
- build_model_candidate_gate_failure_receipt
- build_aegis_admission_contract
- python/tests/aegis/test_aegis_action_firewall.py
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
- AEGIS-ACTION-FIREWALL-00 gates action eligibility and preserves that model-candidate eligibility is not action authority.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides bounded local ingress context.
- ENTERPRISE-AI-RISK-TAXONOMY-STACK-DESIGN-00 provides multi-view risk taxonomy context.
- PRODUCT-READINESS-ROADMAP-MATRIX-00 lists receipt-chain export as an AEGIS follow-up validation step.

## Artifact references

- docs/AEGIS_ACTION_FIREWALL.md
- python/src/coherence/aegis/action_firewall.py
- python/src/coherence/aegis/admission.py
- python/src/coherence/aegis/model_candidate_gate.py
- python/src/coherence/aegis/instruction_quarantine.py
- python/src/coherence/aegis/grounding_binding.py
- python/src/coherence/aegis/source_scope.py
- python/src/coherence/aegis/consent_check.py
- python/src/coherence/aegis/policy.py
- schema/bridge/aegis_action_firewall_packet.schema.json
- schema/bridge/aegis_action_firewall_failure_receipt.schema.json
- schema/bridge/aegis_action_firewall_non_authority_boundary.schema.json
- python/tests/aegis/test_aegis_action_firewall.py
- python/tests/aegis/test_aegis_model_candidate_gate.py
- python/tests/aegis/test_aegis_instruction_quarantine.py
- python/tests/aegis/test_aegis_grounding_binding.py
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Allowed claim

AEGIS-ACTION-FIREWALL-00 implements local deterministic AEGIS action-firewall artifacts that evaluate whether a proposed side-effecting action is eligible after model-candidate gating and explicit operator authorization, while preserving that the prototype does not execute tools, perform actions, write files, delete files, pull or push connectors, call providers, perform network calls, write memory, admit Atlas memory, export traces, federate PMR, install packages, activate packages, execute packages, process payments, bill subscriptions, download marketplace packages, certify compliance, provide legal advice, pass audits, claim product readiness, release product, certify truth, emit final answers, grant final-answer authority, or grant accepted-evidence authority.

## Blocked claims

- action firewall certifies truth
- action firewall authorizes memory write
- action firewall authorizes deployment
- action firewall certifies compliance
- action firewall provides legal advice
- action firewall passes audit
- action firewall releases product
- action firewall proves product readiness
- action firewall grants final-answer authority
- action firewall grants accepted-evidence authority
- action firewall executes tools
- action firewall performs actions
- action firewall writes files
- action firewall deletes files
- action firewall pulls connector data
- action firewall pushes connector data
- action firewall calls provider
- action firewall calls network
- action firewall writes memory
- action firewall admits Atlas memory
- action firewall exports traces
- action firewall federates PMR
- action firewall installs packages
- action firewall activates packages
- action firewall executes packages
- action firewall processes payment
- action firewall bills subscription
- action firewall downloads marketplace package
- model candidate eligibility authorizes action
- model_candidate_allowed means action allowed
- preview allowed means action performed
- operator authorization inferred from model output
- missing operator authorization can proceed
- action_allowed means action performed
- action_allowed_with_controls means action performed
- noop action performed
- preview action wrote file
- final answer emitted by action firewall
- accepted evidence marked by action firewall

## Non-authority guardrails

- action_firewall_is_not_truth_certification
- action_firewall_is_not_source_truth_certification
- action_firewall_is_not_memory_write_authorization
- action_firewall_is_not_deployment_authority
- action_firewall_is_not_compliance_certification
- action_firewall_is_not_legal_advice
- action_firewall_is_not_audit_pass
- action_firewall_is_not_attestation_success
- action_firewall_is_not_product_release
- action_firewall_is_not_product_readiness
- action_firewall_is_not_final_answer_authority
- action_firewall_is_not_accepted_evidence_authority
- action_firewall_does_not_execute_tools
- action_firewall_does_not_perform_actions
- action_firewall_does_not_call_provider
- action_firewall_does_not_call_network
- action_firewall_does_not_write_files
- action_firewall_does_not_delete_files
- action_firewall_does_not_pull_connectors
- action_firewall_does_not_push_connectors
- action_firewall_does_not_write_memory
- action_firewall_does_not_admit_atlas_memory
- action_firewall_does_not_export_traces
- action_firewall_does_not_federate_pmr
- human_review_required

## Runtime boundary

Publication sync grants no runtime authority, tool execution, file writes, file deletion, connector pulls, connector pushes, provider runtime, network calls, memory writes, Atlas admission, trace export, PMR federation, package installation, package activation, package execution, payment processing, subscription billing, marketplace download, product readiness, product release, compliance certification, legal advice, audit pass, truth certification, final-answer authority, accepted-evidence authority, model training, model output generation, model-candidate creation, or review skipping.
