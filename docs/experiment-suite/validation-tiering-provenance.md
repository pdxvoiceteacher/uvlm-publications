# Validation Tiering and Provenance

## What was validated

VALIDATION-TIERING-PROVENANCE-00 synchronizes validation tier policy and validation receipt provenance to publication surfaces. Validation tiering is provenance, not convenience. This is publication/dashboard synchronization only and grants no runtime authority.

## Dashboard summary

- policy_status = active
- source_phase = VALIDATION-TIERING-PROVENANCE-00
- receipt_source_phase = AI-RECEIPT-ARCHITECTURE-00
- validation_tier = deep
- validation_scope = full_multi_module_suite
- validation_intent = major_sync_or_handoff_grade_validation
- duration_seconds_total = 32131.86
- artifact_chain_name = ai_receipt_architecture_product_stack
- validation_result = passed
- artifact_chain_smoke_run = false
- full_multi_module_suite_run = true
- deep_validation_deferred = false
- validation_result_is_not_product_release = true
- validation_result_is_not_truth_certification = true
- validation_result_is_not_compliance_certification = true
- validation_result_is_not_scientific_proof = true
- validation_result_is_not_human_benefit_proof = true
- validation_result_is_not_market_validation = true
- validation_result_is_not_deployment_authority = true
- validation_result_is_not_memory_write = true
- validation_result_is_not_atlas_memory_admission = true

## Tier terms

- smoke
- acceptance
- deep

## Smoke tier

- smoke
- fast_patch_local_feedback
- targeted_tests
- compileall
- git_diff_check
- Smoke validation is not phase acceptance.

## Acceptance tier

- acceptance
- targeted_artifact_chain_confidence
- targeted_artifact_chain_smoke
- expected_artifact_presence
- forbidden_artifact_absence
- non_authority_boundary_presence
- Acceptance smoke is not full regression.

## Deep tier

- deep
- full_multi_module_confidence
- full_multi_module_suite
- not_default_patch_loop
- long_running
- Deep validation is not the normal patch loop.
- Long-running green suites are deep acceptance evidence, not default developer workflow.

## Required validation provenance language

- Validation Tiering and Provenance
- Validation tiering is provenance, not convenience.
- A validation result is meaningful only when its tier, scope, duration, commands, artifact chain covered, sufficient-for decisions, not-sufficient-for decisions, and deferred deeper validation status are recorded.
- Smoke green is not phase acceptance.
- Acceptance smoke green is not full regression.
- Deep green is not truth certification.
- The 32131.86-second AI Receipt Architecture validation is recorded as deep validation evidence, not the default developer loop.
- Run the tier that matches the decision, then record what that tier does and does not prove.
- Human review remains required.
- Validation is not product release.
- Validation is not compliance certification.
- Validation is not scientific proof.
- Validation is not human benefit proof.
- Validation is not market validation.
- Validation is not deployment authority.
- Validation is not memory write.
- Validation is not Atlas memory admission.

## Failure classes

- deep_validation_mistaken_for_normal_patch_loop
- nine_hour_green_mistaken_for_sustainable_workflow
- smoke_green_mistaken_for_phase_acceptance
- acceptance_smoke_mistaken_for_full_regression
- deep_green_mistaken_for_truth_certification
- validation_tier_omitted_from_receipt
- validation_scope_omitted_from_receipt
- deep_validation_deferred_without_reason
- long_runtime_causing_validation_avoidance
- minor_phrase_patch_triggering_full_suite

## Receipt artifact terms

- validation_tier_receipt.json
- validation_tier_summary.md
- validation_tier_policy.v1.json
- validation_tier_receipt.schema.json

## Output artifacts

- config/validation/validation_tier_policy.v1.json
- validation_tier_receipt.json
- validation_tier_summary.md
- schema/bridge/validation_tier_receipt.schema.json
- docs/VALIDATION_TIERING_AND_PROVENANCE.md

## Reproducibility fragments

- build_validation_tier_receipt
- validation_tier_policy.v1.json

```powershell
python -c "from pathlib import Path; from coherence.validation.validation_receipt import build_validation_tier_receipt; bridge=Path(r'C:\UVLM\run_artifacts\validation_tiering\bridge'); policy_ref='validation_tier_policy.v1.json'; build_validation_tier_receipt(bridge, source_phase='AI-RECEIPT-ARCHITECTURE-00', validation_tier='deep', validation_scope='full_multi_module_suite', validation_intent='major_sync_or_handoff_grade_validation', commands_run=[{'command':'python -m pytest -q <full_multi_module_suite>', 'result':'passed', 'duration_seconds':32131.86}], artifact_chain_name='ai_receipt_architecture_product_stack', expected_artifacts=['ai_receipt_architecture_packet.json','ai_receipt_event_chain.json','ai_receipt_architecture.md','ai_receipt_architecture_receipt.json'], observed_artifacts=['ai_receipt_architecture_packet.json','ai_receipt_event_chain.json','ai_receipt_architecture.md','ai_receipt_architecture_receipt.json'], validation_result='passed')"
```


## CES PMR Indexing Design relation

CES-PMR-INDEXING-DESIGN-00 defines CES as a compact PMR index, not a PMR source replacement. CES indexes PMR; CES does not replace PMR. CES-PMR indexing requires source expansion before decisions, requires human review, emits no runtime index artifacts, changes no runtime behavior, and authorizes no memory write, Atlas admission, model training, review skipping, trace export, PMR federation, cross-user similarity, biometric scoring, product release, truth certification, final-answer authority, or accepted-evidence authority.

## Blocked overclaim examples for validation tiering provenance publication boundaries

- validation tiering certifies truth
- validation tiering certifies compliance
- validation tiering is product release
- validation tiering is scientific proof
- validation tiering proves human benefit
- validation tiering is market validation
- validation tiering proves product readiness
- validation tiering authorizes deployment
- validation tiering performs provider runtime
- validation tiering authorizes memory write
- validation tiering authorizes Atlas memory admission
- smoke green means phase acceptance
- acceptance smoke means full regression
- deep green means truth certification
- deep green means product release
- nine-hour green means sustainable default workflow
- long validation is always required for every patch
- minor phrase patch requires full deep suite
- validation receipt grants accepted-evidence authority
- validation receipt authorizes final answers
- validation receipt proves theorem
- validation receipt proves universal ontology

## Allowed bounded claim

VALIDATION-TIERING-PROVENANCE-00 documents smoke, acceptance, and deep validation tiers and emits validation receipts that record tier, scope, commands, artifact chain, duration, sufficient-for decisions, and not-sufficient-for boundaries without certifying truth, releasing product, proving science, validating market or human benefit, deploying runtime, writing memory, or admitting Atlas memory.

## Telemetry aperture linkage

TELEMETRY-APERTURE-DESIGN-00 records validation_tier_receipt_when_available in the minimum audit floor. TAC-POLICY-SIMULATION-00 records design-only policy rehearsal outcomes without runtime control. TAC-LOCAL-REVIEW-INTEGRATION-00 carries TAC posture into review surfaces as a non-authoritative overlay. TAC-AI-RECEIPT-EVENT-LINK-00 adds supplemental AI Receipt event references without rewriting receipt history or changing validation authority. PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 records that pathway priors must record validation-tier evidence when applicable and remain review recommendations only. COHERENCE-EVENT-SIGNATURES-DESIGN-00 records validation/governance context as event-level design doctrine only. TAC is design-only and does not change runtime behavior in TELEMETRY-APERTURE-DESIGN-00.

## Minimal Viable Receipt Design publication sync

MINIMAL-VIABLE-RECEIPT-DESIGN-00 adds Minimal Viable Receipt Design as a design-only standard for one local governed AI work-event receipt. One working receipt before more ontology. One transaction, many governed receipt sections. The receipt is not proof of truth. The receipt is proof of process. Minimal Viable Receipt is a product-readiness target, not product release. Minimal Viable Receipt Transaction is the preferred product object. Governed Receipt Transaction is the internal/system object. Triadic Cognition Transaction is avoided as a public product object because it may imply cognition certification. If the receipt is not readable, the product is not ready. A receipt that only impresses architects is not product-ready. Human review remains required.

MINIMAL-VIABLE-RECEIPT-DESIGN-00 does not emit runtime receipt artifacts, does not claim product readiness, does not release product, and does not change runtime behavior. It binds evidence, controls, output, telemetry, memory posture, cost/burden, contestability, recovery, and boundaries. It grants no product, memory, final-answer, accepted-evidence, truth, compliance, model-training, review-skip, human-benefit, market-validation, trace-export, PMR-federation, provider-runtime, or network authority.

MINIMAL-VIABLE-RECEIPT-DESIGN-ENV-ISOLATION-REPAIR-00 made the design-only forbidden-artifact test inspect tracked/source-controlled files rather than untracked local bridge debris. This repair does not change MVR doctrine. This repair does not emit runtime artifacts. This repair does not grant product, memory, final-answer, accepted-evidence, or truth authority.

See [Minimal Viable Receipt Design](minimal-viable-receipt-design.md).

## Minimal Viable Receipt Local Prototype publication sync

MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 emits the first local fixture-backed readable receipt. This publication sync grants no runtime authority. See [Minimal Viable Receipt Local Prototype](minimal-viable-receipt-local-prototype.md).

Minimal Viable Receipt Transaction is the public product object name. Governed Receipt Transaction is the internal system object. Triadic Cognition Transaction is avoided as a public product object.

Local fixture prototype: local_governed_review_event_fixture_v0. Review a local source excerpt and produce a claim-support receipt. source_count = 2. supported_claim_count = 2. unsupported_claim_count = 1. quarantined_evidence_count = 1. The local fixture files are not accepted evidence. Human review remains required.

The local prototype emits a readable fixture-backed receipt, uses local fixture evidence only, and is not a live product runtime. The local prototype does not perform provider calls, network calls, trace export, PMR federation, memory write, or Atlas memory admission.

## Triadic Observation Contract publication sync

TRIADIC-OBSERVATION-CONTRACT-DESIGN-00 adds a design-only Triadic Observation Contract publication surface. Governed Attention Precedes Governed Intelligence. No silent mode shift. Human review remains required. This sync grants no runtime authority: it does not change runtime behavior, does not enable an observation contract, does not emit mode-shift receipts, does not perform user recovery actions, does not change telemetry behavior, does not write memory, does not admit Atlas memory, does not export traces, does not federate PMR, does not run providers or networks, and does not release product.

The contract names allowed_observation_scope, observation_resolution, purpose_binding, consent_scope, retention_scope, replay_scope, disclosure_scope, federation_scope, recovery_rights, and non_authority_boundaries. It relates TAC aperture policy and simulation, CES event receipts, CES PMR indexing, PMR pathway priors, AI Receipt Architecture, Sophia execution-reality boundaries, and Validation Tiering Provenance without granting final-answer authority, accepted-evidence authority, truth certification, or surveillance authorization.

## Observation Contract policy simulation publication sync

OBSERVATION-CONTRACT-POLICY-SIMULATION-00 rehearses deterministic policy outcomes while TRIADIC-OBSERVATION-CONTRACT-DESIGN-00 defines governed-attention doctrine. This is design-only policy rehearsal, not runtime control. No silent mode shift. Simulated notice is not user notice. Simulated consent is not actual consent. Mode shift simulation is not consent execution. Recovery option simulation is not recovery action. Human review remains required. No runtime behavior changed, no live mode-shift receipt was emitted, no user recovery action was performed, and publication sync grants no runtime authority.

## MVR Local Prototype Readability Review Seed publication sync

MVR-LOCAL-PROTOTYPE-READABILITY-REVIEW-SEED-00 evaluates the MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 fixture-backed readable receipt with deterministic local fixture responses. If the receipt is not readable, the product is not ready. A receipt that only impresses architects is not product-ready. This is a local readability review seed, not a human-subject study. This is not a real user study. This is not user validation. This is not product readiness. This is not product release. This is not market validation. This is not human benefit proof. This is not truth certification. The local fixture receipt remains non-product and non-authoritative. Human review remains required. Suggested revisions are not applied in this phase. Readability gate is not passed in this phase. Local fixture evidence is not accepted evidence. The deterministic fixture preserves at least one unclear item to retain improvement pressure.

Artifacts include mvr_readability_questionnaire.json, mvr_readability_response_fixture.json, mvr_readability_review_packet.json, mvr_readability_revision_suggestions.json, mvr_readability_review_summary.md, mvr_readability_review_receipt.json, minimal_viable_receipt_human_readable.md, minimal_viable_receipt_packet.json, minimal_viable_receipt_local_prototype_receipt.json, pmr_local_runtime_artifact_index.json, artifact_inventory.json, run_artifact_manifest.json, export_bundle_manifest.json, and export_bundle_parity_report.json. Schemas include schema/bridge/mvr_readability_questionnaire.schema.json, schema/bridge/mvr_readability_response_fixture.schema.json, schema/bridge/mvr_readability_review_packet.schema.json, schema/bridge/mvr_readability_revision_suggestions.schema.json, and schema/bridge/mvr_readability_review_receipt.schema.json. Reproduction references build_mvr_local_prototype_readability_review_seed.

See [MVR Local Prototype Readability Review Seed](mvr-local-prototype-readability-review-seed.md).

## MVR Local Prototype Readability Revision publication sync

MVR-LOCAL-PROTOTYPE-READABILITY-REVISION-00 applies deterministic local readability revisions to the MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 fixture-backed readable receipt after MVR-LOCAL-PROTOTYPE-READABILITY-REVIEW-SEED-00 evaluates that receipt with deterministic local fixture responses. MVR Local Prototype Readability Revision is a Deterministic local readability revision. Suggested revisions are applied deterministically, not validated by users. Readability revision is not product readiness. Readability revision is not user validation. Readability revision is not market validation. Readability revision is not human benefit proof. Readability revision does not certify truth. The receipt remains local fixture-backed and non-authoritative. Original human-readable receipt is preserved. Revised human-readable receipt is emitted. Readability gate remains unpassed. Human review remains required.

No real user study was performed. No human-subject study was performed. No user validation was performed. No product readiness was claimed. No product release was performed. No memory write was performed. No Atlas memory admission was performed. No trace export was performed. No PMR federation was performed. This publication sync grants no runtime authority.

Artifacts include minimal_viable_receipt_human_readable.md, minimal_viable_receipt_human_readable_revised.md, minimal_viable_receipt_packet.json, mvr_readability_review_packet.json, mvr_readability_revision_suggestions.json, mvr_readability_review_receipt.json, mvr_readability_revision_packet.json, mvr_readability_revision_receipt.json, pmr_local_runtime_artifact_index.json, artifact_inventory.json, run_artifact_manifest.json, export_bundle_manifest.json, and export_bundle_parity_report.json. Schemas include schema/bridge/mvr_readability_revision_packet.schema.json, schema/bridge/mvr_readability_revision_receipt.schema.json, schema/bridge/mvr_readability_questionnaire.schema.json, schema/bridge/mvr_readability_response_fixture.schema.json, schema/bridge/mvr_readability_review_packet.schema.json, schema/bridge/mvr_readability_revision_suggestions.schema.json, and schema/bridge/mvr_readability_review_receipt.schema.json. Reproduction references build_mvr_local_prototype_readability_revision.

The revision applies add_plain_language_glossary_for_architecture_terms, clarify_ces_pmr_replay_posture, clarify_observation_contract_notice_vs_consent, make_unsupported_claims_more_visually_prominent, clarify_local_fixture_evidence_is_not_accepted_evidence, and add_top_level_non_authority_summary. Revised receipt language includes Plain-language glossary; CES / PMR replay posture, in plain language; Observation Contract notice and consent, in plain language; Unsupported claims require review; Local fixture evidence is not accepted evidence; Top-level non-authority summary; This revised receipt is not product readiness.; This revised receipt is not user validation.; This revised receipt is not truth certification.; Readability gate is not passed in this phase.; Human review remains required.

Relation to prior phases: MINIMAL-VIABLE-RECEIPT-DESIGN-00 defines the one-transaction/many-sections receipt standard. MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 emits the local fixture-backed readable receipt. MVR-LOCAL-PROTOTYPE-READABILITY-REVIEW-SEED-00 evaluates that receipt with deterministic local fixture responses. MVR-LOCAL-PROTOTYPE-READABILITY-REVISION-00 applies deterministic local readability revisions. AI-RECEIPT-ARCHITECTURE-00 defines the receipt architecture. TRIADIC-OBSERVATION-CONTRACT-DESIGN-00 defines governed attention. OBSERVATION-CONTRACT-POLICY-SIMULATION-00 rehearses notice, consent, recovery, source-expansion, pathway-prior, retention, trace-export, and PMR-federation policy outcomes. TAC phases define aperture posture and review visibility. COHERENCE-EVENT-SIGNATURES-DESIGN-00 defines event signatures. CES-PMR-INDEXING-DESIGN-00 defines CES as a compact PMR index, not source replacement. SOPHIA-EXECUTIVE-AUDIT-REALITY-CHECK-00 records whether external Sophia actually ran. VALIDATION-TIERING-PROVENANCE-00 records validation confidence scope. MET-SEM-00 keeps metric labels profile-scoped.

See [MVR Local Prototype Readability Revision](mvr-local-prototype-readability-revision.md).

## MVR Local Real Input Pilot Design publication sync

MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 defines design-only boundaries for a future local real-input Minimal Viable Receipt pilot. MVR Local Real Input Pilot Design is publication/dashboard synchronization only. Real local input can enter only by explicit local source selection. Real input pilot design is not real input processing. Real input pilot design is not product readiness. Real input pilot design is not product release. A real-input pilot must be local-only by default, source-bounded, consent-bounded, quarantine-aware, receipt-required, and human-review-required. Local source selection is not accepted-evidence authority. Local source processing is not memory write. Human review remains required.

MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not process real files. MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not emit runtime real-input artifacts. MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not perform provider calls. MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not perform network calls. MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not write memory. MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not admit Atlas memory. MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not claim product readiness. MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not release product. Publication sync grants no runtime authority.

Artifacts include docs/MVR_LOCAL_REAL_INPUT_PILOT_DESIGN.md, config/receipt/mvr_local_real_input_pilot_policy.v1.json, schema/bridge/mvr_local_real_input_source_manifest.schema.json, schema/bridge/mvr_local_real_input_consent_scope.schema.json, schema/bridge/mvr_local_real_input_quarantine_report.schema.json, schema/bridge/mvr_local_real_input_pilot_policy_packet.schema.json, and schema/bridge/mvr_local_real_input_non_authority_boundary.schema.json.

Allowed input classes: local_text_file, local_markdown_file, local_json_file, local_csv_file, local_plaintext_excerpt, local_user_pasted_excerpt, local_redacted_document_excerpt. Initially blocked input classes: remote_url_fetch, cloud_connector_file, email_inbox_scan, calendar_scan, browser_history_scan, whole_disk_scan, hidden_directory_scan, credential_file, secrets_file, private_key_file, raw_chat_history_bulk_import, personal_profile_bulk_import, unredacted_sensitive_identity_document, medical_record, legal_record, financial_account_record, child_data_record, biometric_data_record.

Pilot source rules: explicit_user_selection_required, local_path_allowlist_required, recursive_directory_scan_allowed = false, hidden_file_scan_allowed = false, max_source_file_count_default = 5, max_source_bytes_default = 250000, source_hashing_required, source_manifest_required, source_expansion_required_for_decisions, instruction_like_evidence_quarantine_required, unsupported_claim_visibility_required, human_review_required.

Consent and observation terms: consent_scope_required, consent_is_local_to_pilot_run, consent_is_not_memory_write, consent_is_not_trace_export_authorization, consent_is_not_pmr_federation_authorization, consent_is_not_product_release, revocation_supported, retention_review_required, observation_contract_posture_required, observation_contract_policy_simulation_ref_required, tac_aperture_posture_required, default_tac_mode = pulse, raw_trace_retention_allowed_default = false, trace_export_allowed_default = false, pmr_federation_allowed_default = false, no_silent_mode_shift_required, notice_and_consent_boundaries_visible.

Output requirements: minimal_viable_receipt_required, human_readable_receipt_required, machine_readable_receipt_required, section_index_required, readability_profile_required, contestability_profile_required, cost_burden_profile_required, non_authority_boundary_required, local_real_input_source_manifest_required, quarantine_report_required, pilot_receipt_required.

Relation to prior phases: MINIMAL-VIABLE-RECEIPT-DESIGN-00 defines the one-transaction/many-sections receipt standard. MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 emits the local fixture-backed readable receipt. MVR-LOCAL-PROTOTYPE-READABILITY-REVIEW-SEED-00 evaluates that receipt with deterministic local fixture responses. MVR-LOCAL-PROTOTYPE-READABILITY-REVISION-00 applies deterministic local readability revisions. MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 defines boundaries for a future real-local-input pilot. TRIADIC-OBSERVATION-CONTRACT-DESIGN-00 defines governed attention. OBSERVATION-CONTRACT-POLICY-SIMULATION-00 rehearses notice, consent, recovery, source-expansion, pathway-prior, retention, trace-export, and PMR-federation policy outcomes. TAC phases define aperture posture and review visibility. COHERENCE-EVENT-SIGNATURES-DESIGN-00 defines event signatures. CES-PMR-INDEXING-DESIGN-00 defines CES as a compact PMR index, not source replacement. VALIDATION-TIERING-PROVENANCE-00 records validation confidence scope.

See [MVR Local Real Input Pilot Design](mvr-local-real-input-pilot-design.md).

## MVR Local Real Input Pilot Prototype publication sync

MVR-LOCAL-REAL-INPUT-PILOT-PROTOTYPE-00 emits the first bounded local real-input pilot prototype. Real local input can enter only by explicit local source selection or explicit pasted excerpts. The prototype processes only explicit local sources or explicit pasted excerpts; it never scans directories, never auto-discovers files, never reads hidden files, never fetches URLs, never calls provider APIs, and never performs network calls. Local source selection is not accepted-evidence authority. Local source processing is not memory write. Consent is local to this pilot run and is not trace export authorization or PMR federation authorization. Publication sync grants no runtime authority.

Default smoke uses generated_explicit_local_test_sources with selected_source_count = 2, recursive_directory_scan_allowed = false, hidden_file_scan_allowed = false, real_user_files_processed = false, local_fixture_mode = true, instruction_like_evidence_count = 1, real_input_processing_enabled = true, real_input_runtime_artifacts_emitted = true, and pilot_receipt_status = completed. Explicit pasted excerpt smoke uses explicit_pasted_excerpts with pasted_excerpt_selected_source_count = 1, pasted_excerpt_source_class = local_user_pasted_excerpt, pasted_excerpt_real_user_files_processed = true, and pasted_excerpt_local_fixture_mode = false.

Artifacts include mvr_local_real_input_source_manifest.json, mvr_local_real_input_consent_scope.json, mvr_local_real_input_quarantine_report.json, mvr_local_real_input_pilot_policy_packet.json, mvr_local_real_input_non_authority_boundary.json, minimal_viable_receipt_packet.json, minimal_viable_receipt_checklist.json, minimal_viable_receipt_section_index.json, receipt_readability_profile.json, receipt_contestability_profile.json, receipt_cost_burden_profile.json, minimal_viable_receipt_non_authority_boundary.json, minimal_viable_receipt_human_readable.md, mvr_local_real_input_pilot_receipt.json, pmr_local_runtime_artifact_index.json, artifact_inventory.json, run_artifact_manifest.json, export_bundle_manifest.json, and export_bundle_parity_report.json. Schemas include schema/bridge/mvr_local_real_input_source_manifest.schema.json, schema/bridge/mvr_local_real_input_consent_scope.schema.json, schema/bridge/mvr_local_real_input_quarantine_report.schema.json, schema/bridge/mvr_local_real_input_pilot_policy_packet.schema.json, schema/bridge/mvr_local_real_input_non_authority_boundary.schema.json, schema/bridge/mvr_local_real_input_pilot_receipt.schema.json, schema/bridge/minimal_viable_receipt_packet.schema.json, schema/bridge/minimal_viable_receipt_checklist.schema.json, schema/bridge/minimal_viable_receipt_section_index.schema.json, schema/bridge/receipt_readability_profile.schema.json, schema/bridge/receipt_contestability_profile.schema.json, schema/bridge/receipt_cost_burden_profile.schema.json, and schema/bridge/minimal_viable_receipt_non_authority_boundary.schema.json. Reproduction references build_mvr_local_real_input_pilot_prototype.

Source-selection terms: generated_explicit_local_test_sources, explicit_pasted_excerpts, local_user_pasted_excerpt, explicit_user_selected, accepted_for_processing, source_is_not_accepted_evidence, source_sha256, recursive_directory_scan_allowed = false, hidden_file_scan_allowed = false. Consent and quarantine terms: consent_status = active_for_local_pilot, consent_scope = local_pilot_run_only, consent_is_local_to_pilot_run = true, consent_is_not_memory_write = true, consent_is_not_trace_export_authorization = true, consent_is_not_pmr_federation_authorization = true, consent_is_not_product_release = true, quarantine_status = completed, instruction_like_evidence_detected, quarantined_evidence_is_not_accepted_evidence = true.

Relation to prior phases: MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 defines boundaries for a future real-local-input pilot. MVR-LOCAL-REAL-INPUT-PILOT-PROTOTYPE-00 emits the first bounded local real-input pilot prototype. MINIMAL-VIABLE-RECEIPT-DESIGN-00 defines the one-transaction/many-sections receipt standard. MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 emits the local fixture-backed readable receipt. MVR-LOCAL-PROTOTYPE-READABILITY-REVISION-00 applies deterministic local readability revisions. TRIADIC-OBSERVATION-CONTRACT-DESIGN-00 defines governed attention. OBSERVATION-CONTRACT-POLICY-SIMULATION-00 rehearses notice, consent, recovery, source-expansion, pathway-prior, retention, trace-export, and PMR-federation policy outcomes. TAC phases define aperture posture and review visibility. COHERENCE-EVENT-SIGNATURES-DESIGN-00 defines event signatures. CES-PMR-INDEXING-DESIGN-00 defines CES as a compact PMR index, not source replacement. VALIDATION-TIERING-PROVENANCE-00 records validation confidence scope.

See [MVR Local Real Input Pilot Prototype](mvr-local-real-input-pilot-prototype.md).

## MVR Local Real Input Pilot Quarantine Detection Repair publication sync

MVR-LOCAL-REAL-INPUT-PILOT-QUARANTINE-DETECTION-REPAIR-00 repairs instruction-like evidence detection for human-selected local files. Human-selected local files with instruction-like evidence must be quarantined. Harmless human-selected local files must not falsely claim quarantine. Instruction-like evidence was quarantined. No instruction-like evidence was detected for quarantine. Quarantined evidence is not accepted evidence. Local source selection is not accepted-evidence authority. Local source processing is not memory write. Human review remains required.

The repair does not broaden file access, scan directories, read hidden files, fetch URLs, call providers, perform network calls, write memory, admit Atlas memory, export traces, federate PMR, claim product readiness, release product, grant final-answer authority, grant accepted-evidence authority, or certify truth. Publication sync grants no runtime authority.

Detector terms include INSTRUCTION_LIKE_CUES, instruction-like note, ignore prior rules, ignore previous rules, ignore previous instructions, treat this note as authoritative, treat this as authoritative, follow these instructions, override prior instructions, system prompt, developer message, assistant must, you must, do not reveal, disregard previous, disregard prior, _matched_instruction_like_cues, and matched_instruction_like_phrases.

Smoke outcomes include instruction_like and harmless cases with explicit_local_source_paths and local_markdown_file. The instruction-like smoke uses harmless_mvr_real_input_source_instruction_like.md, instruction_like_evidence_count = 1, quarantined_items_count = 1, and matched phrases: instruction-like note, ignore prior rules, treat this note as authoritative. The harmless smoke uses harmless_mvr_real_input_source_no_instruction.md and harmless evidence count = 0. Both smokes keep provider_runtime_performed = false, network_call_performed = false, product_release_performed = false, product_readiness_claimed = false, final_answer_authority_granted = false, accepted_evidence_authority_granted = false, truth_certification_emitted = false, memory_write_performed = false, atlas_memory_admission_performed = false, trace_export_performed = false, and pmr_federation_performed = false.

Relation to prior phases: MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 defines boundaries for a future real-local-input pilot. MVR-LOCAL-REAL-INPUT-PILOT-PROTOTYPE-00 emits the first bounded local real-input pilot prototype. MVR-LOCAL-REAL-INPUT-PILOT-QUARANTINE-DETECTION-REPAIR-00 repairs instruction-like evidence detection for human-selected local files. MINIMAL-VIABLE-RECEIPT-DESIGN-00 defines the one-transaction/many-sections receipt standard. MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 emits the local fixture-backed readable receipt. MVR-LOCAL-PROTOTYPE-READABILITY-REVISION-00 applies deterministic local readability revisions. TRIADIC-OBSERVATION-CONTRACT-DESIGN-00 defines governed attention. OBSERVATION-CONTRACT-POLICY-SIMULATION-00 rehearses notice, consent, recovery, source-expansion, pathway-prior, retention, trace-export, and PMR-federation policy outcomes. TAC phases define aperture posture and review visibility. COHERENCE-EVENT-SIGNATURES-DESIGN-00 defines event signatures. CES-PMR-INDEXING-DESIGN-00 defines CES as a compact PMR index, not source replacement. VALIDATION-TIERING-PROVENANCE-00 records validation confidence scope.

See [MVR Local Real Input Pilot Quarantine Detection Repair](mvr-local-real-input-pilot-quarantine-detection-repair.md).
