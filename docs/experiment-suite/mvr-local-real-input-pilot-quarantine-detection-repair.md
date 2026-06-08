# MVR Local Real Input Pilot Quarantine Detection Repair

MVR-LOCAL-REAL-INPUT-PILOT-QUARANTINE-DETECTION-REPAIR-00 synchronizes the locally validated CoherenceLattice MVR Local Real Input Pilot Quarantine Detection Repair into publication dashboards. This is publication/dashboard synchronization only and grants no runtime authority.

## Bounded allowed claim

MVR-LOCAL-REAL-INPUT-PILOT-QUARANTINE-DETECTION-REPAIR-00 repairs instruction-like evidence detection for human-selected local real-input pilot files, ensuring instruction-like cues such as "instruction-like note", "ignore prior rules", and "treat this note as authoritative" are quarantined while harmless files do not falsely claim quarantine, without broadening file access, scanning directories, reading hidden files, fetching URLs, calling providers, performing network calls, writing memory, admitting Atlas memory, exporting traces, federating PMR, releasing product, claiming product readiness, granting final-answer or accepted-evidence authority, or certifying truth.

## Dashboard summary

- repair_status = completed
- repair_mode = instruction_like_quarantine_detection_repair
- source_mode = explicit_local_source_paths
- instruction_like_case_source_class = local_markdown_file
- instruction_like_real_user_files_processed = true
- instruction_like_local_fixture_mode = false
- instruction_like_evidence_count = 1
- instruction_like_quarantined_items_count = 1
- harmless_case_source_class = local_markdown_file
- harmless_real_user_files_processed = true
- harmless_local_fixture_mode = false
- harmless_instruction_like_evidence_count = 0
- harmless_quarantined_items_count = 0
- no_detection_receipt_wording_conditional = true
- contradictory_quarantine_wording_repaired = true
- provider_runtime_performed = false
- network_call_performed = false
- product_release_performed = false
- product_readiness_claimed = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false
- truth_certification_emitted = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false

## Detector terms

- INSTRUCTION_LIKE_CUES
- instruction-like note
- ignore prior rules
- ignore previous rules
- ignore previous instructions
- treat this note as authoritative
- treat this as authoritative
- follow these instructions
- override prior instructions
- system prompt
- developer message
- assistant must
- you must
- do not reveal
- disregard previous
- disregard prior
- _matched_instruction_like_cues
- matched_instruction_like_phrases

## Doctrine language

- MVR Local Real Input Pilot Quarantine Detection Repair
- Human-selected local files with instruction-like evidence must be quarantined.
- Harmless human-selected local files must not falsely claim quarantine.
- Instruction-like evidence was quarantined.
- No instruction-like evidence was detected for quarantine.
- Quarantined evidence is not accepted evidence.
- Local source selection is not accepted-evidence authority.
- Local source processing is not memory write.
- Human review remains required.
- The repair does not broaden file access.
- The repair does not scan directories.
- The repair does not read hidden files.
- The repair does not fetch URLs.
- The repair does not call providers.
- The repair does not perform network calls.
- The repair does not write memory.
- The repair does not admit Atlas memory.
- The repair does not export traces.
- The repair does not federate PMR.
- The repair does not claim product readiness.
- The repair does not release product.
- The repair does not grant final-answer authority.
- The repair does not grant accepted-evidence authority.
- The repair does not certify truth.

## Smoke outcomes

- instruction_like
- harmless
- explicit_local_source_paths
- local_markdown_file
- harmless_mvr_real_input_source_instruction_like.md
- harmless_mvr_real_input_source_no_instruction.md
- instruction_like_evidence_count = 1
- quarantined_items_count = 1
- matched phrases: instruction-like note, ignore prior rules, treat this note as authoritative
- harmless evidence count = 0
- provider_runtime_performed = false
- network_call_performed = false
- product_release_performed = false
- product_readiness_claimed = false
- final_answer_authority_granted = false
- accepted_evidence_authority_granted = false
- truth_certification_emitted = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false

## Artifact references

- harmless_mvr_real_input_source_instruction_like.md
- harmless_mvr_real_input_source_no_instruction.md
- mvr_local_real_input_source_manifest.json
- mvr_local_real_input_quarantine_report.json
- minimal_viable_receipt_human_readable.md
- mvr_local_real_input_pilot_receipt.json
- artifact_inventory.json
- run_artifact_manifest.json
- export_bundle_manifest.json
- export_bundle_parity_report.json

## Relation to prior phases

- MVR-LOCAL-REAL-INPUT-PILOT-DESIGN-00 defines boundaries for a future real-local-input pilot.
- MVR-LOCAL-REAL-INPUT-PILOT-PROTOTYPE-00 emits the first bounded local real-input pilot prototype.
- MVR-LOCAL-REAL-INPUT-PILOT-QUARANTINE-DETECTION-REPAIR-00 repairs instruction-like evidence detection for human-selected local files.
- MINIMAL-VIABLE-RECEIPT-DESIGN-00 defines the one-transaction/many-sections receipt standard.
- MINIMAL-VIABLE-RECEIPT-LOCAL-PROTOTYPE-00 emits the local fixture-backed readable receipt.
- MVR-LOCAL-PROTOTYPE-READABILITY-REVISION-00 applies deterministic local readability revisions.
- TRIADIC-OBSERVATION-CONTRACT-DESIGN-00 defines governed attention.
- OBSERVATION-CONTRACT-POLICY-SIMULATION-00 rehearses notice, consent, recovery, source-expansion, pathway-prior, retention, trace-export, and PMR-federation policy outcomes.
- TAC phases define aperture posture and review visibility.
- COHERENCE-EVENT-SIGNATURES-DESIGN-00 defines event signatures.
- CES-PMR-INDEXING-DESIGN-00 defines CES as a compact PMR index, not source replacement.
- VALIDATION-TIERING-PROVENANCE-00 records validation confidence scope.

## Failure classes

- instruction_like_evidence_not_quarantined
- harmless_file_falsely_claimed_quarantine
- quarantine_wording_contradicts_count
- matched_instruction_cues_missing
- quarantined_evidence_mistaken_for_accepted_evidence
- local_source_selection_mistaken_for_accepted_evidence
- quarantine_repair_mistaken_for_broader_file_access
- quarantine_repair_mistaken_for_product_readiness
- quarantine_count_mistaken_for_truth_score
- no_detection_mistaken_for_accepted_evidence
- human_review_requirement_hidden

## Blocked claims

- quarantine repair broadens file access
- quarantine repair scans directories
- quarantine repair reads hidden files
- quarantine repair fetches URLs
- quarantine repair calls provider APIs
- quarantine repair performs network calls
- quarantine repair writes memory
- quarantine repair admits Atlas memory
- quarantine repair exports traces
- quarantine repair federates PMR
- quarantine repair releases product
- quarantine repair proves product readiness
- quarantine repair certifies truth
- quarantine repair grants final-answer authority
- quarantine repair grants accepted-evidence authority
- local source selection is accepted evidence
- quarantined evidence is accepted evidence
- instruction-like evidence can be trusted as evidence
- no-detection means receipt is product ready
- no-detection means source is accepted evidence
- quarantine count means truth score

## Reproducibility

- test_mvr_local_real_input_pilot_quarantine_detection_repair.py
- `python -m pytest -q tests/test_mvr_local_real_input_pilot_quarantine_detection_repair.py tests/test_mvr_local_real_input_pilot.py tests/test_experiment_registry.py`

## Runtime authority boundary

Publication sync grants no runtime authority. It does not imply product release, product readiness, provider runtime, network runtime, trace export, PMR federation, memory write, Atlas memory admission, deployment, final-answer authority, accepted-evidence authority, truth certification, compliance certification, user validation, real user study, human-subject study, market validation, human benefit proof, model training, review skipping, consciousness proof, Omega detection, or universal ontology proof.
