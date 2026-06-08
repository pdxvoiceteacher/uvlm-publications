# Coherence Event Signatures

## What was validated

COHERENCE-EVENT-SIGNATURES-DESIGN-00 synchronizes locally validated Coherence Event Signatures design doctrine to publication surfaces. This is publication/dashboard synchronization only and grants no runtime authority. CES is design-only, event-level receipt doctrine; no runtime artifacts or authority are emitted.

## Dashboard summary

- policy_status = active_design_only
- runtime_behavior_changed = false
- ces_emission_enabled = false
- ces_runtime_artifacts_emitted = false
- ces_similarity_search_enabled = false
- cross_user_similarity_enabled = false
- federated_similarity_enabled = false
- raw_trace_retention_performed = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- model_training_performed = false
- product_release_performed = false
- event_scope = significant_transactive_events_only
- ces_definition = trace_compatible_hash_sealed_coherence_indexed_event_receipt
- metric_profile_is_not_exact_identity = true
- canonical_hash_is_not_truth_certification = true
- cross_user_similarity_disabled_by_default = true
- federated_similarity_requires_review = true
- ces_is_not_truth_certification = true
- ces_is_not_final_answer_authority = true
- ces_is_not_accepted_evidence_authority = true
- ces_is_not_biometric_score = true
- ces_is_not_user_identity = true
- ces_is_not_memory_write_authorization = true
- ces_is_not_atlas_memory_admission = true
- ces_is_not_model_training = true
- ces_is_not_trace_export_authorization = true
- ces_is_not_federation_authorization = true
- ces_is_not_product_release = true
- ces_requires_human_review = true

## Required CES doctrine language

- Coherence Event Signatures
- Coherence metrics are not identity.
- Coherence metrics are state signatures.
- Trace ID identifies event position.
- Hash seals integrity.
- TEL gives topology.
- UCC gives control context.
- Sophia gives governance status.
- TAC gives observation aperture.
- PMR gives memory and retention posture.
- AI Receipt exposes what happened to humans.
- CES binds these into an event-level cognitive receipt.
- CES should become the event-level receipt layer for Triadic Brain.
- CES is trace-compatible, hash-sealed, coherence-indexed, topology-aware, aperture-aware, PMR-retention-aware, and privacy-bounded.
- CES records what happened, what evidence it touched, how coherent the process was, what governance applied, and whether the event has any right to return as memory.
- CES is not truth certification.
- CES is not final-answer authority.
- CES is not accepted-evidence authority.
- CES is not a biometric score.
- CES is not user identity.
- CES is not memory write authorization.
- CES is not model training.
- CES is not product release.
- CES similarity is not identity merge.
- CES clustering is not model training permission.
- CES retention is not memory write.
- CES replay value is not truth.
- Human review remains required.
- COHERENCE-EVENT-SIGNATURES-DESIGN-00 does not emit CES runtime artifacts.
- COHERENCE-EVENT-SIGNATURES-DESIGN-00 does not enable similarity search.
- COHERENCE-EVENT-SIGNATURES-DESIGN-00 does not change runtime behavior.

## Product language

- Coherence Event Signatures turn AI activity into auditable cognitive receipts.
- CES records what happened, what evidence it touched, how coherent the process was, what governance applied, and whether the event has any right to return as memory.

## CES layers

- trace_identity
- integrity_profile
- coherence_profile
- topology_profile
- context_profile
- privacy_profile
- rights_retention_profile
- non_authority_boundaries

## Safe metric aliases

- E_review
- T_review
- Ψ_review
- ΔS_review
- Λ_boundary
- Eₛ_review
- TAF_review_runtime_v0
- Psi_review
- DeltaS_review
- Lambda_boundary
- Es_review

## Identity and integrity doctrine

- metric_profile_is_similarity_signal
- metric_profile_is_not_exact_identity
- trace_id_span_id_event_index_define_identity
- canonical_hash_is_integrity_signal
- canonical_hash_is_not_truth_certification
- canonical_json_sorted_keys
- canonical_json_utf8
- no_volatile_local_absolute_paths_in_ces_id
- hashes_use_sha256
- normalization_version_recorded

## Similarity and privacy doctrine

- similarity_search_design_only
- cross_user_similarity_disabled_by_default
- federated_similarity_requires_review
- similarity_is_not_identity_merge
- basin_label_is_not_truth
- ces_describes_process_state_not_personal_essence
- ces_must_not_be_hidden_user_score
- ces_must_not_be_used_for_employment_credit_health_civic_or_social_ranking
- ces_retention_must_be_consent_bounded
- ces_sharing_defaults_to_local_minimal_revocable

## Proposed design-only event types

- review_request_created
- source_file_accepted
- source_file_rejected
- source_normalized
- claim_extracted
- source_span_created
- claim_classified
- unsupported_claim_preserved
- metric_packet_emitted
- taf_packet_emitted
- flow_topology_emitted
- sophia_audit_bound
- pmr_context_linked
- human_receipt_emitted
- acceptance_receipt_emitted

## Negative controls

- metric_collision_negative_control
- replay_nondeterminism_negative_control
- privacy_behavioral_biometric_negative_control
- tamper_negative_control
- sampling_aperture_negative_control

## Failure classes

- metric_profile_mistaken_for_identity
- hash_mistaken_for_truth_certification
- ces_mistaken_for_biometric_score
- ces_mistaken_for_user_identity
- ces_similarity_mistaken_for_identity_merge
- ces_clustering_mistaken_for_model_training
- ces_retention_mistaken_for_memory_write
- ces_replay_mistaken_for_truth
- cross_user_similarity_enabled_without_review
- federated_similarity_enabled_without_review
- behavioral_biometric_risk_ignored
- volatile_local_path_in_ces_id
- replay_lineage_missing
- tac_aperture_context_missing
- pmr_retention_context_missing
- sophia_governance_context_missing
- metric_semantic_profile_missing

## Relation to PMR

- CES can serve as a compact PMR event index.
- CES does not replace PMR source artifacts.
- CES is a searchable event signature for PMR, while PMR remains the evidentiary replay store.
- CES may support future revocable pathway-prior candidates.
- CES does not authorize pathway-prior generation in COHERENCE-EVENT-SIGNATURES-DESIGN-00.
- CES does not write memory.
- CES does not admit Atlas memory.

CES-PMR-INDEXING-DESIGN-00 defines CES as a compact PMR index, not a PMR source replacement. Future runtime CES-PMR indexing remains disabled in this design patch.

## Artifacts

- docs/COHERENCE_EVENT_SIGNATURES.md
- config/ces/coherence_event_signature_policy.v1.json
- schema/bridge/coherence_event_signature_packet.schema.json
- schema/bridge/ces_chain_summary_packet.schema.json
- schema/bridge/ces_similarity_index_packet.schema.json
- schema/bridge/ces_non_authority_boundary.schema.json

## Reproducibility fragments

- COHERENCE_EVENT_SIGNATURES.md
- coherence_event_signature_policy.v1.json
- coherence_event_signature_packet.schema.json
- ces_chain_summary_packet.schema.json
- ces_similarity_index_packet.schema.json
- ces_non_authority_boundary.schema.json

```powershell
python -c "from pathlib import Path; Path('docs/COHERENCE_EVENT_SIGNATURES.md').read_text(encoding='utf-8')"; python -m json.tool config/ces/coherence_event_signature_policy.v1.json >/dev/null; python -m json.tool schema/bridge/coherence_event_signature_packet.schema.json >/dev/null; python -m json.tool schema/bridge/ces_chain_summary_packet.schema.json >/dev/null; python -m json.tool schema/bridge/ces_similarity_index_packet.schema.json >/dev/null; python -m json.tool schema/bridge/ces_non_authority_boundary.schema.json >/dev/null
```

## Blocked overclaim examples for Coherence Event Signatures design publication boundaries

- CES proves truth
- CES reveals the model's reasoning
- CES fingerprints the user
- CES is a biometric score
- CES identifies the user
- CES certifies cognition
- CES certifies professional oversight
- CES authorizes final answers
- CES grants accepted-evidence authority
- CES authorizes memory write
- CES admits Atlas memory
- CES authorizes trace export
- CES authorizes PMR federation
- CES trains the model
- CES similarity is identity
- CES clustering is model training
- CES replay value is truth
- CES retention is memory write
- CES makes memory safe
- hash seal certifies truth
- metric profile uniquely identifies event
- basin label is truth
- cross-user similarity is enabled by default
- federated similarity is allowed without review

## Allowed bounded claim

Coherence Event Signatures are proposed as trace-compatible, hash-sealed, coherence-indexed, topology-aware, aperture-aware, PMR-retention-aware, and privacy-bounded event receipts for significant Triadic Brain transactions, preserving trace identity, integrity, coherence state, process topology, governance context, retention rights, and non-authority boundaries without certifying truth, identifying users, authorizing final answers, accepting evidence, writing memory, admitting Atlas memory, training models, exporting traces, federating PMR, or releasing product.

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
