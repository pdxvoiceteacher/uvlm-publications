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
- Repos are governed provenance libraries, not document dumps.
- Raw source reports may be omitted from public repos when privacy, sensitivity, size, or licensing requires hash-only reference.
- DOCX originals should have Markdown derivatives when committed.
- TXT and MD reports may be committed directly when public-safe.
- Large or sensitive files should use private/archive storage, Git LFS, release assets, or external governed storage.
- Future users must check canonical repo state before treating reports as current design.
- Source reports are not accepted evidence by themselves.
- Source reports are not theorem proof.
- Source reports are not product release.
- Source reports are not compliance certification.
- Summaries are not sources.
- Human review remains required.
- Hashes preserve identity; hashes do not certify truth.
- Visibility and sensitivity must be explicit.
- Public release approval must be explicit.

## Manifest terms

- active_governed_provenance_manifest
- hash_only_public_reference
- canonical_repo_state_supersedes_report
- source_is_not_accepted_evidence
- source_is_not_theorem_proof
- source_is_not_product_release
- source_is_not_compliance_certification
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

## Reproducibility

- test_source_corpus_provenance_hash_fill.py
- `python -m pytest -q tests/test_source_corpus_provenance_hash_fill.py tests/test_source_corpus_provenance_archive.py tests/test_experiment_registry.py`

## Runtime authority boundary

Publication sync grants no runtime authority. It does not imply compliance certification, legal advice, audit pass, attestation success, product readiness, product release, truth certification, final-answer authority, accepted-evidence authority, memory write, Atlas memory admission, trace export, PMR federation, provider runtime, network runtime, model training, review skipping, user validation, human-subject study, market validation, human benefit proof, theorem proof, GUFT proof, consciousness proof, or universal ontology proof.

## June 2026 source-corpus batch manifest publication sync

SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00 adds the June 2026 hash-only batch manifest. It preserves source identity and provenance only; raw private files are not committed, duplicate filenames are deduplicated by SHA-256, filename aliases are preserved, public release approval is false by default, and canonical repo state supersedes source reports.

Source-corpus batch doctrine: June 2026 Source Corpus Batch Manifest; This batch preserves source identity and provenance, not accepted evidence.; Raw private files are not committed.; Duplicate filenames are deduplicated by SHA-256.; Filename aliases are preserved.; Public release approval is false by default.; Hashes preserve identity; hashes do not certify truth.; Canonical repo state supersedes source reports.; Human review remains required.; Large or sensitive reports remain hash-only references unless explicitly approved.; Repos are governed provenance libraries, not document dumps.; Source reports are not accepted evidence by themselves.; Source reports are not theorem proof.; Source reports are not product release.; Source reports are not product readiness.; Source reports are not compliance certification.; Source reports are not legal advice.; Source reports are not current canonical repo state.; SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00 does not commit raw private reports.; SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00 does not add extracted text.; SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00 does not add normalized derivatives.

High-priority filenames: Telemetry Project Deep Dive.docx, CoherenceLattice Change Management and Gnosis Synthesis Report.docx, Telemetry Integration into the CoherenceLattice Pipeline.docx, Multi-Axial Coherence Analysis for Exogenic Off-Loading in Complex Systems.docx, Quantum Gravity from Causal Memory.docx, Universal Control Codex (UCC) Supplement.docx, The Coherence Lattice GUFT meets GUPT.docx, The Grand Unified Field Theory of Coherence (GUFT) V69.me.docx, TCHES v1.4.docx, Appendix TAF – Operationalize it, because Ultra Verba, Lux Mentis.docx, Echo Primer.pdf, PMR - Internal Technical Memo.docx, THE COHERENCE OF SIGNAL.docx, Preventing Hyperreal design drift.docx, Triadic Brain Developer Guidance for Canonical Ingress, Grounding Bundles, and Phaselock Governance.docx, Triadic Brain Maths Glossary.docx, Thought-Exchange Layer (TEL) Graph MVP Design and Integration.docx, Final TEL Event Stack Validation in CoherenceLattice.docx, free will.zip, governed_tches_success_20260420_135304.zip, governed_tches_after_dq08_inventory_capture_20260501_161304.zip, mvr_tches_v1_4_human_selected_file_smoke.zip.

Concrete hashes: 0d9bedc988ae3bd6c8c5291594e98cdf55f2483e61d365ae9976785e412f2656, f1206c5f86d83c6ac900d8880b5dcffa5433ce626a1ddfef8480a060ee3f4fa4, 09268960029318fbd9c724094a6a82bf49e095576e1a5bc644a1e9215fad977a, 7bf6c9637ecbb6afd1cef14a0ee39f5904ddb2493277902334456d05cc0a5104, 23acd312e50e43b7c98702e87ce4bb324fd259502f6fc7cd937690c676feae4d, d48b4984c0061495a89c9cdaba12cd26816ce504c22f765ee1fd6cadc87f2f3d, bcf6941fe619fa40a9475327e977fce7c8af2c44b94d5ae5fd8665eb65a2976c, 87584b4c97581a8657978c63bf4ba135cd707f2a1c21deccb513ffa881212503, d5feb2658f74bedbb56782c66ba473ef29e0ae02ca3ea091356c8cea30aba74d, aff0180dd1a61784bb5b6b173ebf6b66a6cb2f497bbb08aedb9fe4dc149ef583, 0bb03eeb493da65f0625e5028d708873016c359d184bc0f1fecac5715d63b953, dc628557c0e729ff8fe5127d1eb129046a12186fff33b9dae65ad58f2e4e0ceb, 5b028820fd50bd93a7f5ad1ec54955f08c0accd039a482e999fdc04efaccf6c2, a241521288f7c792b76f22b9ec82d19027be9f1032402ae0d87288cacdcb9258, fe5cd0189f64df015239453430a085a156580ecaab5856cc784498a25d62a38b, 27941c74013b578c216e4569a066a8988860a9c8b01fa544cd6fe25a642a8f35, 3608c158b6affd4f63d04e91d5eae65bb045afb864549d3b84ad9bc664d87c40, 1904b3e786b4c0314b681d8c52ddef39ef02d3e4b2bbe2a2493b3072b84d997f, 17bcca653cbe300c656d796f42f6a077b1bf58f3e3a6655133524cbe56386fdd, 00683d8c93d5daabefa9ea6e5819c53f76e9155fd42a4b4dad036188843ee3d1, db97a6325de67c673baae100327773d6d5f0a0a14431ada361b1551d647fef3d, 6046cabc13041f664cb67caf96cf5d43eb41fcc03df59248d0b3e6842552d7ca.

Alias terms: Telemetry%20Project%20Deep%20Dive.docx, Telemetry%20Integration%20into%20the%20CoherenceLattice%20Pipeline.docx, Universal%20Control%20Codex%20%28UCC%29%20Supplement.docx, Multi%E2%80%91Axial%20Coherence%20Analysis%20for%20Exogenic%20Off%E2%80%91Loading%20in%20Complex%20Systems.docx, filename_aliases, deduplicated by SHA-256, filename aliases are not separate sources, deduplication means byte-identity only. Manifest terms: source_corpus_batch_20260610, active_hash_only_provenance_manifest, one_canonical_row_per_unique_sha256, raw_sha256, hash_only_public_reference, public_release_approved = false, canonical_repo_state_supersedes_report, source_is_not_accepted_evidence, source_is_not_theorem_proof, source_is_not_product_release, source_is_not_product_readiness, source_is_not_compliance_certification, source_is_not_legal_advice, source_is_not_memory_write, source_is_not_atlas_memory_admission, summary_is_not_source, human_review_required.

Relation to prior phases: SOURCE-CORPUS-PROVENANCE-ARCHIVE-00 defines the governed source-report archive pattern. SOURCE-CORPUS-PROVENANCE-HASH-FILL-00 fills pending EU AI Act source-report hashes. SOURCE-CORPUS-BATCH-MANIFEST-2026-06-10-00 adds the June 2026 hash-only batch manifest. WAVE-ROSETTA-CANONICAL-PROXY-BRIDGE-PROVENANCE-00 uses source report hashes for scientific provenance. COMPLIANCE-READY-MVR-REPORT-LOCAL-PROTOTYPE-00 uses compliance report provenance for report design context. VALIDATION-TIERING-PROVENANCE-00 records validation confidence scope. Publication sync grants no runtime authority.
