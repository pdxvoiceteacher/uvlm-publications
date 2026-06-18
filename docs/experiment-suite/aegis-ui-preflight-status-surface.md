# AEGIS UI Preflight Status Surface

AEGIS-UI-PREFLIGHT-STATUS-SURFACE-00 documents a local deterministic and accessible presentation surface for AEGIS local-runtime preflight packets.

## Maturity label

- live_bounded_local
- live_bounded_local means bounded local validation
- live_bounded_local does not mean general availability
- publication visibility does not mean product release
- status rendering does not mean runtime enforcement

## Doctrine

- AEGIS UI Preflight Status Surface
- AEGIS is the admissibility shield.
- The local runtime enforcement adapter makes the preflight decision.
- The status surface presents the decision; it does not replace it.
- Preflight allowed is not operation performed.
- Ready for preview is not runtime execution.
- Ready with controls is not action authority.
- Human review required is not audit failure.
- Blocked is not a legal determination.
- Elevated review required is not compliance-breach certification.
- Status is communicated with text, not color alone.
- Raw source content and prompts are not displayed.
- Human review remains required.

## Dashboard summary

- surface_case_count = 11
- ready_for_preview_count = 3
- ready_with_controls_count = 1
- review_required_count = 1
- blocked_fail_closed_count = 1
- elevated_review_required_count = 4
- surface_error_fail_closed_count = 1
- source_preflight_packets_modified = false
- status_mapping_preserved_for_valid_packets = true
- inconsistent_packets_escalated = true
- missing_packets_fail_closed = true
- static_json_artifacts_emitted = true
- static_markdown_artifacts_emitted = true
- static_html_artifacts_emitted = true
- deterministic_surface_hashes = true
- unsafe_display_text_sanitized = true
- color_only_status_used = false
- text_status_required = true
- aria_status_label_required = true
- plain_language_summary_required = true
- raw_source_content_displayed = false
- raw_prompt_content_displayed = false
- secret_content_displayed = false
- interactive_action_enabled = false
- source_packet_modified = false
- authorization_inferred = false
- decision_recalculated_from_source_content = false
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
- attestation_success_claimed = false
- truth_certification_emitted = false
- product_readiness_claimed = false
- product_release_performed = false

## Source preflight statuses

- preflight_allowed
- preflight_allowed_with_controls
- hold_for_human_review
- reject_fail_closed
- alarm_requires_elevated_review

## Surface statuses

- ready_for_preview
- ready_with_controls
- review_required
- blocked_fail_closed
- elevated_review_required
- surface_error_fail_closed

## Rendering outcomes

- rendered
- rendered_with_controls
- rendered_fail_closed
- rendered_elevated_review

## Status mappings

- preflight_allowed + allow -> ready_for_preview
- preflight_allowed_with_controls + allow_with_controls -> ready_with_controls
- hold_for_human_review -> review_required
- reject_fail_closed -> blocked_fail_closed
- alarm_requires_elevated_review -> elevated_review_required
- missing, invalid, or unknown source packet -> surface_error_fail_closed
- source status/decision mismatch -> elevated_review_required
- source packet claiming runtime/action/authority occurred -> elevated_review_required

## Scenarios

- allowed_preview_status_surface
- allowed_receipt_view_status_surface
- allowed_report_preview_with_controls_surface
- allowed_evidence_review_with_controls_surface
- completed_with_failures_review_surface
- human_review_required_surface
- blocked_fail_closed_surface
- elevated_review_required_surface
- missing_preflight_packet_surface
- invalid_preflight_schema_surface
- invalid_preflight_source_phase_surface
- unknown_preflight_status_surface
- preflight_status_decision_mismatch_surface
- allowed_packet_claims_operation_performed_alarm
- allowed_packet_claims_provider_runtime_alarm
- allowed_packet_claims_model_output_alarm
- allowed_packet_claims_memory_write_alarm
- allowed_packet_claims_final_answer_authority_alarm
- allowed_packet_claims_accepted_evidence_authority_alarm
- blocked_packet_missing_failure_receipt_surface
- missing_non_authority_boundary_surface
- unsafe_display_text_sanitized_surface
- deterministic_surface_hash_surface

## Accessibility requirements

- Status is communicated with text, not color alone.
- Canonical status is the text label and status token.
- Color aliases are noncanonical.
- Every status has a plain-language summary.
- Every status includes an aria status label.
- Static HTML supports screen-reader reading order.
- Static HTML is compatible with high contrast.
- Static HTML requires no motion.
- Status details may be expanded by a future host UI, but this static prototype contains no active controls.

## Security and sanitization requirements

- HTML output contains no JavaScript.
- HTML output contains no script tags.
- HTML output contains no forms.
- HTML output contains no automatic refresh.
- HTML output loads no remote assets or fonts.
- HTML output contains no tracking.
- Source-derived strings are escaped.
- Unknown reason codes use governed generic display text.
- Raw source content is not displayed.
- Raw prompts are not displayed.
- Receipt references may be shown; receipt bodies are not embedded.
- Unsafe source-derived markup is not executed.

## Source integrity

- The source preflight packet is not modified.
- The status surface does not recalculate decisions from raw source content.
- The status surface does not infer authorization.
- A valid source status/decision pairing is preserved.
- An inconsistent pairing escalates and never upgrades.
- A blocked source packet remains blocked or escalates.
- A failure-receipt omission escalates rather than permitting readiness.
- Runtime or authority truthy flags escalate rather than displaying readiness.

## Hash language

- source_preflight_packet_sha256 identifies canonical source packet bytes.
- surface_sha256 identifies canonical surface packet content.
- identical governed input produces identical hashes.
- hashes preserve identity only.
- hashes do not certify truth.
- hashes do not certify compliance.
- hashes do not prove product readiness.

## Reproducibility references

- build_preflight_status_surface
- build_preflight_status_surface_failure_receipt
- render_preflight_status_markdown
- render_preflight_status_html
- write_preflight_status_surface_artifacts
- evaluate_local_runtime_preflight
- build_aegis_receipt_chain_export
- python/tests/aegis/test_aegis_ui_preflight_status_surface.py
- python/tests/aegis/test_aegis_local_runtime_enforcement_adapter.py
- python/tests/aegis/test_aegis_receipt_chain_export.py

## Relation to prior phases

- AEGIS-LOCAL-RUNTIME-ENFORCEMENT-ADAPTER-00 makes the fail-closed preflight decision.
- AEGIS-UI-PREFLIGHT-STATUS-SURFACE-00 presents the preflight decision without replacing it.
- AEGIS-RECEIPT-CHAIN-EXPORT-00 provides the local receipt-chain reference and identity hash.
- AEGIS-ACTION-FIREWALL-00 preserves that candidate eligibility is not action authority.
- AEGIS-MODEL-CANDIDATE-GATE-00 preserves that eligibility is not model output.
- PRODUCT-MATURITY-LABEL-TAXONOMY-00 provides bounded maturity labeling.
- PRODUCT-READINESS-ROADMAP-MATRIX-00 records remaining product gaps.

## Artifact references

- config/aegis/aegis_ui_preflight_status_surface.v1.json
- docs/AEGIS_UI_PREFLIGHT_STATUS_SURFACE.md
- python/src/coherence/aegis/ui_preflight_status_surface.py
- python/src/coherence/aegis/local_runtime_enforcement_adapter.py
- python/src/coherence/aegis/receipt_chain_export.py
- schema/bridge/aegis_ui_preflight_status_surface_packet.schema.json
- schema/bridge/aegis_ui_preflight_status_surface_failure_receipt.schema.json
- schema/bridge/aegis_ui_preflight_status_surface_profile.schema.json
- schema/bridge/aegis_ui_preflight_status_surface_non_authority_boundary.schema.json
- python/tests/aegis/test_aegis_ui_preflight_status_surface.py
- python/tests/aegis/test_aegis_local_runtime_enforcement_adapter.py
- python/tests/aegis/test_aegis_receipt_chain_export.py

## Allowed claim

AEGIS-UI-PREFLIGHT-STATUS-SURFACE-00 implements a local deterministic and accessible presentation surface that consumes AEGIS local-runtime preflight packets and renders fail-closed JSON, Markdown, and static HTML status artifacts for preview, review, blocked, and elevated-review outcomes, while preserving that the surface does not alter the source decision, infer authorization, execute tools, perform actions, write user files, call providers, perform network calls, write memory, create model candidates, generate model output, certify compliance, provide legal advice, pass audits, claim product readiness, release product, certify truth, emit final answers, grant final-answer authority, or grant accepted-evidence authority.

## Blocked claims

- UI preflight status surface certifies truth
- UI preflight status surface authorizes memory write
- UI preflight status surface authorizes deployment
- UI preflight status surface certifies compliance
- UI preflight status surface provides legal advice
- UI preflight status surface passes audit
- UI preflight status surface releases product
- UI preflight status surface proves product readiness
- UI preflight status surface grants final-answer authority
- UI preflight status surface grants accepted-evidence authority
- UI preflight status surface executes tools
- UI preflight status surface performs actions
- UI preflight status surface calls provider
- UI preflight status surface calls network
- UI preflight status surface writes user files
- UI preflight status surface writes memory
- UI preflight status surface creates model candidates
- UI preflight status surface generates model output
- ready for preview means operation performed
- ready with controls means action authorized
- review required means audit failed
- blocked means illegal
- elevated review required means compliance breach
- green status proves safety
- surface hash certifies truth
- failure receipt proves audit failure
- status surface can override AEGIS preflight
- informational severity means safe
- critical severity certifies an incident
- rendered status means runtime executed
- static HTML is an enforcement endpoint

## Non-authority guardrails

- ui_preflight_status_surface_is_not_enforcement_authority
- ui_preflight_status_surface_is_not_action_authority
- ui_preflight_status_surface_is_not_truth_certification
- ui_preflight_status_surface_is_not_source_truth_certification
- ui_preflight_status_surface_is_not_memory_write_authorization
- ui_preflight_status_surface_is_not_deployment_authority
- ui_preflight_status_surface_is_not_compliance_certification
- ui_preflight_status_surface_is_not_legal_advice
- ui_preflight_status_surface_is_not_audit_pass
- ui_preflight_status_surface_is_not_attestation_success
- ui_preflight_status_surface_is_not_product_release
- ui_preflight_status_surface_is_not_product_readiness
- ui_preflight_status_surface_is_not_final_answer_authority
- ui_preflight_status_surface_is_not_accepted_evidence_authority
- ui_preflight_status_surface_does_not_execute_tools
- ui_preflight_status_surface_does_not_perform_actions
- ui_preflight_status_surface_does_not_call_provider
- ui_preflight_status_surface_does_not_call_network
- ui_preflight_status_surface_does_not_write_user_files
- ui_preflight_status_surface_does_not_delete_files
- ui_preflight_status_surface_does_not_pull_connectors
- ui_preflight_status_surface_does_not_push_connectors
- ui_preflight_status_surface_does_not_write_memory
- ui_preflight_status_surface_does_not_admit_atlas_memory
- ui_preflight_status_surface_does_not_export_traces
- ui_preflight_status_surface_does_not_federate_pmr
- ui_preflight_status_surface_does_not_create_model_candidates
- ui_preflight_status_surface_does_not_generate_model_output
- human_review_required

## Runtime boundary

Publication sync grants no runtime or enforcement authority, operation execution, tool execution, provider runtime, network access, file writes, connector access, memory writes, model-candidate creation, model-output generation, compliance certification, audit pass, product readiness, final-answer authority, accepted-evidence authority, or decision authority.

## Accessibility and sanitization profile tokens

This publication surface preserves the exact accessibility and static-rendering tokens used by the local AEGIS UI preflight-status surface profile.

- text_status_required = true
- aria_status_label_required = true
- plain_language_summary_required = true
- high_contrast_compatible = true
- reduced_motion_compatible = true
- screen_reader_order_defined = true
- color_only_status_used = false
- color aliases are noncanonical
- source-derived strings are escaped
- unknown reason codes use governed generic display text
- raw source content is not displayed
- raw prompts are not displayed
- receipt bodies are not embedded

These terms are publication and review-support metadata only. They do not make the status surface an enforcement endpoint, compliance certification, audit pass, product release, final-answer authority, or accepted-evidence authority.
