# MVR Local Real Input Pilot Design

MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 synchronizes the locally validated CoherenceLattice MVR Local Real Input Pilot Design into publication dashboards. This is publication/dashboard synchronization only. It defines boundaries for a future local real-input Minimal Viable Receipt pilot and grants no runtime authority.

## Bounded allowed claim

MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 defines design-only boundaries for a future local real-input Minimal Viable Receipt pilot in which explicitly selected local source material may later be processed under local-only, source-bounded, consent-bounded, quarantine-aware, receipt-required, human-review-required, non-authoritative conditions without processing real files in this phase, claiming product readiness, releasing product, granting accepted-evidence or final-answer authority, certifying truth, writing memory, admitting Atlas memory, exporting traces, federating PMR, training models, or skipping review.

## Doctrine language

- MVR Local Real Input Pilot Design
- Real local input can enter only by explicit local source selection.
- Real input pilot design is not real input processing.
- Real input pilot design is not product readiness.
- Real input pilot design is not product release.
- A real-input pilot must be local-only by default.
- A real-input pilot must be source-bounded.
- A real-input pilot must be consent-bounded.
- A real-input pilot must preserve source expansion.
- A real-input pilot must quarantine instruction-like evidence.
- A real-input pilot must expose unsupported claims.
- A real-input pilot must emit a Minimal Viable Receipt before any claim of readiness.
- Local source selection is not accepted-evidence authority.
- Local source processing is not memory write.
- Human review remains required.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not process real files.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not emit runtime real-input artifacts.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not perform provider calls.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not perform network calls.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not write memory.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not admit Atlas memory.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not claim product readiness.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 does not release product.

## Dashboard summary

- policy_status = active_design_only
- pilot_mode = design_only_local_real_input_boundary
- local_real_input_pilot_definition = explicit_local_source_selection_for_mvr_receipt_generation
- runtime_behavior_changed = false
- real_input_processing_enabled = false
- real_input_runtime_artifacts_emitted = false
- real_user_files_processed = false
- provider_runtime_performed = false
- network_call_performed = false
- product_release_performed = false
- product_readiness_claimed = false
- real_user_study_performed = false
- human_subject_study_performed = false
- user_validation_performed = false
- market_validation_emitted = false
- human_benefit_proof_emitted = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false
- truth_certification_emitted = false
- compliance_certification_emitted = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false
- model_training_performed = false
- review_skip_authorized = false
- explicit_user_selection_required = true
- local_path_allowlist_required = true
- recursive_directory_scan_allowed = false
- hidden_file_scan_allowed = false
- max_source_file_count_default = 5
- max_source_bytes_default = 250000
- source_hashing_required = true
- source_manifest_required = true
- source_expansion_required_for_decisions = true
- instruction_like_evidence_quarantine_required = true
- unsupported_claim_visibility_required = true
- human_review_required = true
- consent_scope_required = true
- consent_is_local_to_pilot_run = true
- consent_is_not_memory_write = true
- consent_is_not_trace_export_authorization = true
- consent_is_not_pmr_federation_authorization = true
- consent_is_not_product_release = true
- revocation_supported = true
- retention_review_required = true
- observation_contract_posture_required = true
- observation_contract_policy_simulation_ref_required = true
- tac_aperture_posture_required = true
- default_tac_mode = pulse
- raw_trace_retention_allowed_default = false
- trace_export_allowed_default = false
- pmr_federation_allowed_default = false
- no_silent_mode_shift_required = true
- notice_and_consent_boundaries_visible = true
- minimal_viable_receipt_required = true
- human_readable_receipt_required = true
- machine_readable_receipt_required = true
- section_index_required = true
- readability_profile_required = true
- contestability_profile_required = true
- cost_burden_profile_required = true
- non_authority_boundary_required = true
- local_real_input_source_manifest_required = true
- quarantine_report_required = true
- pilot_receipt_required = true
- pilot_is_not_runtime_processing = true
- pilot_is_not_product_release = true
- pilot_is_not_product_readiness = true
- pilot_is_not_user_validation = true
- pilot_is_not_human_subject_study = true
- pilot_is_not_market_validation = true
- pilot_is_not_human_benefit_proof = true
- pilot_is_not_truth_certification = true
- pilot_is_not_final_answer_authority = true
- pilot_is_not_accepted_evidence_authority = true
- pilot_is_not_memory_write = true
- pilot_is_not_atlas_memory_admission = true
- pilot_is_not_trace_export_authorization = true
- pilot_is_not_pmr_federation_authorization = true
- pilot_is_not_model_training = true
- pilot_is_not_review_skip = true
- pilot_requires_human_review = true

## Allowed input classes

- local_text_file
- local_markdown_file
- local_json_file
- local_csv_file
- local_plaintext_excerpt
- local_user_pasted_excerpt
- local_redacted_document_excerpt

## Initially blocked input classes

- remote_url_fetch
- cloud_connector_file
- email_inbox_scan
- calendar_scan
- browser_history_scan
- whole_disk_scan
- hidden_directory_scan
- credential_file
- secrets_file
- private_key_file
- raw_chat_history_bulk_import
- personal_profile_bulk_import
- unredacted_sensitive_identity_document
- medical_record
- legal_record
- financial_account_record
- child_data_record
- biometric_data_record

## Pilot source rules

- explicit_user_selection_required
- local_path_allowlist_required
- recursive_directory_scan_allowed = false
- hidden_file_scan_allowed = false
- max_source_file_count_default = 5
- max_source_bytes_default = 250000
- source_hashing_required
- source_manifest_required
- source_expansion_required_for_decisions
- instruction_like_evidence_quarantine_required
- unsupported_claim_visibility_required
- human_review_required

## Consent and observation terms

- consent_scope_required
- consent_is_local_to_pilot_run
- consent_is_not_memory_write
- consent_is_not_trace_export_authorization
- consent_is_not_pmr_federation_authorization
- consent_is_not_product_release
- revocation_supported
- retention_review_required
- observation_contract_posture_required
- observation_contract_policy_simulation_ref_required
- tac_aperture_posture_required
- default_tac_mode = pulse
- raw_trace_retention_allowed_default = false
- trace_export_allowed_default = false
- pmr_federation_allowed_default = false
- no_silent_mode_shift_required
- notice_and_consent_boundaries_visible

## Output requirement terms

- minimal_viable_receipt_required
- human_readable_receipt_required
- machine_readable_receipt_required
- section_index_required
- readability_profile_required
- contestability_profile_required
- cost_burden_profile_required
- non_authority_boundary_required
- local_real_input_source_manifest_required
- quarantine_report_required
- pilot_receipt_required

## Artifact references

- docs/MVR_LOCAL_REAL_INPUT_PILOT_DESIGN.md
- config/receipt/mvr_local_real_input_pilot_policy.v1.json
- schema/bridge/mvr_local_real_input_source_manifest.schema.json
- schema/bridge/mvr_local_real_input_consent_scope.schema.json
- schema/bridge/mvr_local_real_input_quarantine_report.schema.json
- schema/bridge/mvr_local_real_input_pilot_policy_packet.schema.json
- schema/bridge/mvr_local_real_input_non_authority_boundary.schema.json

## Relation to prior phases

- MINIMAL-VIABLE-RECEIPT-DESIGN-00 defines the one-transaction/many-sections receipt standard.
- MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 emits the local fixture-backed readable receipt.
- MVR-LOCAL-PROTOTYPE-READABILITY-REVIEW-SEED-00 evaluates that receipt with deterministic local fixture responses.
- MVR-LOCAL-PROTOTYPE-READABILITY-REVISION-00 applies deterministic local readability revisions.
- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 defines boundaries for a future real-local-input pilot.
- TRIADIC-OBSERVATION-CONTRACT-DESIGN-00 defines governed attention.
- OBSERVATION-CONTRACT-POLICY-SIMULATION-00 rehearses notice, consent, recovery, source-expansion, pathway-prior, retention, trace-export, and PMR-federation policy outcomes.
- TAC phases define aperture posture and review visibility.
- COHERENCE-EVENT-SIGNATURES-DESIGN-00 defines event signatures.
- CES-PMR-INDEXING-DESIGN-00 defines CES as a compact PMR index, not source replacement.
- VALIDATION-TIERING-PROVENANCE-00 records validation confidence scope.

## Failure classes

- real_input_design_mistaken_for_real_input_processing
- local_source_selection_mistaken_for_accepted_evidence
- consent_mistaken_for_memory_write
- consent_mistaken_for_trace_export_authorization
- consent_mistaken_for_pmr_federation_authorization
- local_file_access_mistaken_for_directory_scan
- source_manifest_missing
- source_hash_missing
- instruction_like_evidence_not_quarantined
- unsupported_claims_hidden
- source_expansion_missing
- observation_contract_posture_missing
- tac_aperture_posture_missing
- no_silent_mode_shift_boundary_missing
- real_input_receipt_missing
- contestability_missing
- recovery_path_missing
- non_authority_boundaries_missing
- product_readiness_claimed_from_local_pilot
- real_input_pilot_mistaken_for_user_study

## Blocked claims

- real input pilot design processes real files
- real input pilot design is product readiness
- real input pilot design is product release
- local source selection grants accepted-evidence authority
- local source processing writes memory
- local source processing admits Atlas memory
- local source processing authorizes final answers
- local source processing certifies truth
- consent authorizes trace export
- consent authorizes PMR federation
- consent authorizes memory write
- local pilot can scan directories recursively
- local pilot can read hidden files
- local pilot can process credentials
- local pilot can process private keys
- local pilot can process medical records by default
- local pilot can process legal records by default
- local pilot can process financial records by default
- local pilot can process child data by default
- local pilot can process biometric data by default
- unsupported claims can be hidden
- instruction-like evidence can be trusted as evidence
- source expansion can be skipped
- real input pilot is a user study
- real input pilot validates market demand
- real input pilot proves human benefit
- real input pilot trains the model

## Reproducibility

- test_mvr_local_real_input_pilot_design.py
- test_experiment_registry.py
- `python -m pytest -q tests/test_mvr_local_real_input_pilot_design.py tests/test_experiment_registry.py`

## Runtime authority boundary

Publication sync grants no runtime authority. It performs no real file processing, real user file ingestion, provider runtime, network runtime, memory write, Atlas memory admission, trace export, PMR federation, product release, product-readiness claim, real user study, human-subject study, user validation, market validation, human benefit proof, final-answer authorization, accepted-evidence grant, truth certification, compliance certification, model training, or review skipping.
