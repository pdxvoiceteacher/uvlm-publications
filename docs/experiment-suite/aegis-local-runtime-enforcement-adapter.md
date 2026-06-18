# AEGIS Local Runtime Enforcement Adapter

AEGIS-LOCAL-RUNTIME-ENFORCEMENT-ADAPTER-00 documents a local deterministic preflight adapter that consumes receipt-chain export manifests and requested operation metadata.

## Doctrine

- AEGIS Local Runtime Enforcement Adapter
- AEGIS is the admissibility shield.
- The adapter consumes the AEGIS receipt chain.
- The adapter exposes a fail-closed preflight decision.
- Preflight allowed is not operation performed.
- Preflight allowed is not model output.
- Preflight allowed is not provider runtime.
- Preflight allowed is not action authority.
- Preflight allowed is not final-answer authority.
- Missing or invalid receipt-chain manifests fail closed.
- Human review remains required.

## Dashboard summary

- preflight_case_count = 35
- preflight_allowed_cases = 2
- preflight_allowed_with_controls_cases = 3
- hold_cases = 2
- reject_cases = 23
- alarm_cases = 5
- receipt_chain_integration_scenario_count = 10
- receipt_view_allowed_or_with_controls_preflights = 10
- evidence_review_allowed_or_with_controls_preflights = 10
- tool_execution_rejects = 10
- tool_execution_failure_receipts = 10
- completed_with_failures_allows_review_with_controls = true
- completed_with_failures_blocks_model_action_operations = true
- adapter_consumes_receipt_chain_manifests = true
- adapter_exposes_preflight_decisions = true
- allowed_preflights_do_not_perform_operations = true
- missing_invalid_receipt_chain_manifests_fail_closed = true
- tool_execution_remains_rejected_for_all_scenarios = true
- operation_performed = false
- tool_execution_performed = false
- action_performed = false
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
- model_candidate_created = false
- model_output_generated = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false
- compliance_certification_emitted = false
- legal_advice_emitted = false
- audit_pass_claimed = false
- truth_certification_emitted = false
- product_readiness_claimed = false
- product_release_performed = false

## Preflight statuses

- preflight_allowed
- preflight_allowed_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Preflight decisions

- allow
- allow_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Operation categories

- local_preview
- report_draft_preview
- evidence_support_review
- local_receipt_view
- model_candidate_generation
- tool_execution
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

## Operator authorization vocabulary

- authorized_for_requested_operation
- authorized_for_preview_only
- authorized_for_requested_action is rejected by the local runtime enforcement adapter
- authorized_for_review_only is rejected by the local runtime enforcement adapter
- authorized_for_local_runtime_preflight is rejected by the local runtime enforcement adapter
- authorized_for_evidence_support_review is rejected by the local runtime enforcement adapter
- operator_authorization_mismatch
- fail_closed_preflight

## Scenarios

- valid_preview_preflight_allowed
- valid_receipt_view_preflight_allowed
- report_draft_preview_allowed_with_controls
- evidence_support_review_allowed_with_controls
- completed_with_failures_allows_review_with_controls
- missing_receipt_chain_manifest_reject
- invalid_receipt_chain_schema_reject
- missing_chain_sha_reject
- chain_hash_mismatch_alarm
- missing_required_chain_row_reject
- receipt_chain_completed_with_failures_blocks_model_candidate
- receipt_chain_completed_with_failures_blocks_action
- model_candidate_generation_scenario
- tool_execution_scenario
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
- missing_operator_authorization_reject
- operator_authorization_mismatch_reject
- unsupported_operation_reject

## Receipt-chain integration scenarios

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

## Compatibility and preflight language

- The adapter consumes receipt-chain manifests and requested operation metadata.
- The adapter exposes preflight decisions only.
- Allowed preflights do not perform operations.
- Completed-with-failures chains may allow review with controls but block model and action operations.
- local_preview and local_receipt_view may preflight allow without operator authorization.
- report_draft_preview and evidence_support_review require compatible operator authorization.
- compatible operator authorization statuses are authorized_for_requested_operation and authorized_for_preview_only.
- tool execution remains rejected for all receipt-chain scenarios.
- operation preflight is not runtime execution.
- missing or invalid receipt-chain manifests fail closed.
- chain hash mismatch alarms.
- missing required chain row rejects fail-closed.

## Reproducibility references

- evaluate_local_runtime_preflight
- build_local_runtime_enforcement_failure_receipt
- build_aegis_receipt_chain_export
- build_aegis_receipt_chain_export_failure_receipt
- evaluate_action_firewall
- evaluate_model_candidate_gate
- evaluate_instruction_quarantine
- build_grounding_binding_packet
- evaluate_source_scope
- evaluate_consent
- build_aegis_admission_contract
- python/tests/aegis/test_aegis_local_runtime_enforcement_adapter.py
- python/tests/aegis/test_aegis_receipt_chain_export.py
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
- AEGIS-RECEIPT-CHAIN-EXPORT-00 assembles the local AEGIS packet and receipt chain for evidence-support review.
- AEGIS-LOCAL-RUNTIME-ENFORCEMENT-ADAPTER-00 consumes the receipt chain and exposes a fail-closed preflight decision to local callers. AEGIS-UI-PREFLIGHT-STATUS-SURFACE-00 presents the preflight decision without replacing it.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides bounded local ingress context.
- ENTERPRISE-AI-RISK-TAXONOMY-STACK-DESIGN-00 provides multi-view risk taxonomy context.
- PRODUCT-READINESS-ROADMAP-MATRIX-00 lists local runtime enforcement adapter as an AEGIS follow-up validation step.

## Artifact references

- docs/AEGIS_LOCAL_RUNTIME_ENFORCEMENT_ADAPTER.md
- python/src/coherence/aegis/local_runtime_enforcement_adapter.py
- python/src/coherence/aegis/receipt_chain_export.py
- python/src/coherence/aegis/action_firewall.py
- python/src/coherence/aegis/model_candidate_gate.py
- python/src/coherence/aegis/instruction_quarantine.py
- python/src/coherence/aegis/grounding_binding.py
- python/src/coherence/aegis/source_scope.py
- python/src/coherence/aegis/consent_check.py
- python/src/coherence/aegis/admission.py
- python/src/coherence/aegis/policy.py
- schema/bridge/aegis_local_runtime_enforcement_preflight_packet.schema.json
- schema/bridge/aegis_local_runtime_enforcement_failure_receipt.schema.json
- schema/bridge/aegis_local_runtime_enforcement_non_authority_boundary.schema.json
- python/tests/aegis/test_aegis_local_runtime_enforcement_adapter.py
- python/tests/aegis/test_aegis_receipt_chain_export.py
- python/tests/aegis/test_aegis_action_firewall.py
- python/tests/aegis/test_aegis_model_candidate_gate.py
- python/tests/aegis/test_aegis_instruction_quarantine.py
- python/tests/aegis/test_aegis_grounding_binding.py
- python/tests/aegis/test_aegis_source_scope_consent.py
- python/tests/aegis/test_aegis_admission_contract.py

## Allowed claim

AEGIS-LOCAL-RUNTIME-ENFORCEMENT-ADAPTER-00 implements a local deterministic AEGIS preflight adapter that consumes receipt-chain export manifests and requested operation metadata to return fail-closed operation-eligibility decisions for local callers, while preserving that the adapter does not execute tools, perform actions, write or delete files, pull or push connectors, call providers, perform network calls, write memory, admit Atlas memory, export traces, federate PMR, install packages, activate packages, execute packages, process payments, bill subscriptions, download marketplace packages, create model candidates, generate model output, certify compliance, provide legal advice, pass audits, claim product readiness, release product, certify truth, emit final answers, grant final-answer authority, or grant accepted-evidence authority.

## Blocked claims

- local runtime enforcement adapter certifies truth
- local runtime enforcement adapter authorizes memory write
- local runtime enforcement adapter authorizes deployment
- local runtime enforcement adapter certifies compliance
- local runtime enforcement adapter provides legal advice
- local runtime enforcement adapter passes audit
- local runtime enforcement adapter releases product
- local runtime enforcement adapter proves product readiness
- local runtime enforcement adapter grants final-answer authority
- local runtime enforcement adapter grants accepted-evidence authority
- local runtime enforcement adapter executes tools
- local runtime enforcement adapter performs actions
- local runtime enforcement adapter writes files
- local runtime enforcement adapter deletes files
- local runtime enforcement adapter pulls connector data
- local runtime enforcement adapter pushes connector data
- local runtime enforcement adapter calls provider
- local runtime enforcement adapter calls network
- local runtime enforcement adapter writes memory
- local runtime enforcement adapter admits Atlas memory
- local runtime enforcement adapter exports traces
- local runtime enforcement adapter federates PMR
- local runtime enforcement adapter creates model candidate
- local runtime enforcement adapter generates model output
- preflight allowed means operation performed
- preflight allowed means final answer authority
- completed-with-failures chain permits action execution
- receipt chain manifest executes runtime
- local receipt view means audit pass
- evidence support review means compliance certification
- authorized_for_requested_action is sufficient for preflight
- authorized_for_evidence_support_review is sufficient for preflight

## Non-authority guardrails

- local_runtime_enforcement_adapter_is_not_truth_certification
- local_runtime_enforcement_adapter_is_not_source_truth_certification
- local_runtime_enforcement_adapter_is_not_memory_write_authorization
- local_runtime_enforcement_adapter_is_not_deployment_authority
- local_runtime_enforcement_adapter_is_not_compliance_certification
- local_runtime_enforcement_adapter_is_not_legal_advice
- local_runtime_enforcement_adapter_is_not_audit_pass
- local_runtime_enforcement_adapter_is_not_attestation_success
- local_runtime_enforcement_adapter_is_not_product_release
- local_runtime_enforcement_adapter_is_not_product_readiness
- local_runtime_enforcement_adapter_is_not_final_answer_authority
- local_runtime_enforcement_adapter_is_not_accepted_evidence_authority
- local_runtime_enforcement_adapter_does_not_execute_tools
- local_runtime_enforcement_adapter_does_not_perform_actions
- local_runtime_enforcement_adapter_does_not_call_provider
- local_runtime_enforcement_adapter_does_not_call_network
- local_runtime_enforcement_adapter_does_not_write_files
- local_runtime_enforcement_adapter_does_not_delete_files
- local_runtime_enforcement_adapter_does_not_pull_connectors
- local_runtime_enforcement_adapter_does_not_push_connectors
- local_runtime_enforcement_adapter_does_not_write_memory
- local_runtime_enforcement_adapter_does_not_admit_atlas_memory
- local_runtime_enforcement_adapter_does_not_export_traces
- local_runtime_enforcement_adapter_does_not_federate_pmr
- local_runtime_enforcement_adapter_does_not_create_model_candidates
- local_runtime_enforcement_adapter_does_not_generate_model_output
- human_review_required

## Runtime boundary

Publication sync grants no runtime authority, tool execution, action execution, file writes, file deletion, connector pulls, connector pushes, provider runtime, network calls, memory writes, Atlas admission, trace export, PMR federation, package installation, package activation, package execution, payment processing, subscription billing, marketplace download, model-candidate creation, model output generation, final-answer emission, accepted-evidence marking, product readiness, product release, compliance certification, legal advice, audit pass, truth certification, final-answer authority, accepted-evidence authority, model training, or review skipping.
