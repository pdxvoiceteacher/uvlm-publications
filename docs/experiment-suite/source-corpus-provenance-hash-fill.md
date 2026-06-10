# Source Corpus Provenance Hash Fill

SOURCE-CORPUS-PROVENANCE-HASH-FILL-00 synchronizes the source-corpus hash-fill phase into publication dashboards. It fills pending EU AI Act source-report hashes while preserving hash-only public references, public_release_approved=false, no raw private DOCX import, and all non-authority boundaries.

## Bounded allowed claim

SOURCE-CORPUS-PROVENANCE-HASH-FILL-00 fills pending EU AI Act source-report hashes in the governed source-corpus manifest and sha256sums file while preserving hash-only public references, public_release_approved=false, no raw private DOCX import, and all non-authority boundaries.

## Dashboard summary

- manifest_status = active_governed_provenance_manifest
- source_count = 5
- known_wave_guft_hashes_preserved = true
- eu_ai_act_report_hashes_filled = true
- pending_hash_placeholders_remaining = 0
- raw_private_reports_bulk_imported = false
- hash_only_public_references_preserved = true
- public_release_approved = false
- all_non_authority_boundaries_preserved = true
- memory_write_performed = false
- atlas_memory_admission_performed = false
- trace_export_performed = false
- pmr_federation_performed = false
- product_release_performed = false
- product_readiness_claimed = false
- truth_certification_emitted = false
- theorem_proof_claimed = false
- guft_proof_claimed = false
- compliance_certification_emitted = false

## Doctrine language

- Source Corpus Provenance Archive
- June 2026 Source Corpus Batch Manifest
- This batch preserves source identity and provenance, not accepted evidence.
- Raw private files are not committed.
- Duplicate filenames are deduplicated by SHA-256.
- Filename aliases are preserved.
- Public release approval is false by default.
- Repos are governed provenance libraries, not document dumps.
- Raw source reports may be omitted from public repos when privacy, sensitivity, size, or licensing requires hash-only reference.
- DOCX originals should have Markdown derivatives when committed.
- TXT and MD reports may be committed directly when public-safe.
- Large or sensitive files should use private/archive storage, Git LFS, release assets, or external governed storage.
- Future users must check canonical repo state before treating reports as current design.
- Source reports are not accepted evidence by themselves.
- Source reports are not theorem proof.
- Source reports are not product release.
- Source reports are not product readiness.
- Source reports are not compliance certification.
- Source reports are not legal advice.
- Source reports are not current canonical repo state.
- Summaries are not sources.
- Human review remains required.
- Hashes preserve identity; hashes do not certify truth.
- Visibility and sensitivity must be explicit.
- Public release approval must be explicit.
- Canonical repo state supersedes source reports.
- Large or sensitive reports remain hash-only references unless explicitly approved.
- SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00 does not commit raw private reports.
- SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00 does not add extracted text.
- SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00 does not add normalized derivatives.

## Manifest terms

- active_governed_provenance_manifest
- source_corpus_batch_20260610
- active_hash_only_provenance_manifest
- one_canonical_row_per_unique_sha256
- raw_sha256
- hash_only_public_reference
- canonical_repo_state_supersedes_report
- source_is_not_accepted_evidence
- source_is_not_theorem_proof
- source_is_not_product_release
- source_is_not_product_readiness
- source_is_not_compliance_certification
- source_is_not_legal_advice
- source_is_not_memory_write
- source_is_not_atlas_memory_admission
- summary_is_not_source
- human_review_required
- public_release_approved = false

## Source report filenames

- GUFT discussion with Thomas and Apprentice 6_8_2026_842AM.docx
- GUFT METRICS BRIDGE DISCUSSION 6_9_2026_1022AM.docx
- wave_rosetta_canonical_proxy_bridge_scientific_review_20260609.md
- EU AI Act Reporting Formats and Short-Term Product Strategy for UVLM Triadic Brain.docx
- EU AI Act Aligned Reporting Architecture for Triadic Brain Product Lines.docx

## Concrete source hashes

- 2f49da190fcf5e3a04330f53bd9e6d30228c0a999cdabf8be2e94e957e6dfb09
- 9eaba6d5a49de7d09542b3e879cbb9eb936181a37e660b3434a5e31e110ccfe6
- 21045f07f5e2122db9714741a418f582cb87b6d004f6c66f4a63d4b6b7e77fd6
- 9140a5dad410be3f38bcb933b6c360537957d0ce1d4b5ea0d259941eaa3c581e
- 94703c4678eccd407adb9009b34d2b178ab6ab18ee20b6df22d9407eda50dde1

## Artifact references

- docs/SOURCE_CORPUS_PROVENANCE_ARCHIVE.md
- docs/provenance/source_reports/README.md
- docs/provenance/source_reports/manifest.schema.json
- docs/provenance/source_reports/manifest.json
- docs/provenance/source_reports/sha256sums.txt
- docs/provenance/source_reports/2026-06/README.md
- docs/provenance/source_reports/2026-06/raw/.gitkeep
- docs/provenance/source_reports/2026-06/normalized/.gitkeep
- docs/provenance/source_reports/2026-06/summaries/.gitkeep

## Blocked claims

- Compliance-ready MVR report local prototype certifies compliance
- Compliance-ready MVR report local prototype provides legal advice
- Compliance-ready MVR report local prototype passes audit
- Compliance-ready MVR report local prototype guarantees attestation success
- Compliance-ready MVR report local prototype proves product readiness
- Compliance-ready MVR report local prototype is product release
- Compliance-ready MVR report local prototype certifies truth
- Compliance-ready MVR report local prototype authorizes final answers
- Compliance-ready MVR report local prototype grants accepted-evidence authority
- Compliance-ready MVR report local prototype writes memory
- Compliance-ready MVR report local prototype admits Atlas memory
- Compliance-ready MVR report local prototype exports traces
- Compliance-ready MVR report local prototype federates PMR
- source manifest is accepted evidence
- traceability means truth
- control mapping means control effectiveness
- visible gap means compliance failure
- no visible gap means compliance success
- human review role means human signoff occurred
- mapped evidence means compliance satisfied
- WAVE bridge means canonical measurement
- source corpus archive proves GUFT
- source corpus archive proves compliance
- source corpus archive certifies truth
- source reports are accepted evidence
- source reports are canonical repo state
- source reports authorize product release
- source reports certify product readiness
- summaries are sources
- hashes certify truth
- raw reports may be public by default
- private reports may be bulk imported without review
- GitHub repo is a backup store
- source corpus archive writes memory
- source corpus archive admits Atlas memory
- source corpus batch proves GUFT
- source corpus batch proves compliance
- source corpus batch certifies truth
- source corpus batch grants accepted-evidence authority
- source corpus batch is canonical repo state
- source corpus batch authorizes product release
- source corpus batch certifies product readiness
- source corpus batch writes memory
- source corpus batch admits Atlas memory
- filename aliases are separate sources
- raw private reports are public by default
- deduplication means source equivalence beyond byte identity
- source reports are theorem proof
- source reports are compliance certification
- source reports are product release
- source reports are product readiness
- source reports are current canonical repo state

## Reproducibility

- test_source_corpus_provenance_hash_fill.py
- `python -m pytest -q tests/test_source_corpus_provenance_hash_fill.py tests/test_source_corpus_provenance_archive.py tests/test_experiment_registry.py`

## Runtime authority boundary

Publication sync grants no runtime authority. It does not imply compliance certification, legal advice, audit pass, attestation success, product readiness, product release, truth certification, final-answer authority, accepted-evidence authority, memory write, Atlas memory admission, trace export, PMR federation, provider runtime, network runtime, model training, review skipping, user validation, human-subject study, market validation, human benefit proof, theorem proof, GUFT proof, consciousness proof, or universal ontology proof.
