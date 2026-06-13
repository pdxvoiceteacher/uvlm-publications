# Source Corpus Pricing Release Reports Batch Schema Repair

SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-SCHEMA-REPAIR-00 synchronizes schema validation repair for the pricing/release source-corpus batch. This is publication/dashboard synchronization only and grants no runtime authority.

## Bounded schema repair claim

SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-SCHEMA-REPAIR-00 adds the missing source_corpus_pricing_release_report_batch schema referenced by the pricing/release source-corpus manifest, allowing schema validation while preserving hash-only provenance, no raw DOCX import, public_release_approved=false, and all non-authority boundaries.

## Dashboard summary

- batch_status = active_hash_only_pricing_release_provenance_manifest
- batch_id = pricing_release_report_batch_20260612
- row_count = 2
- unique_sha256_count = 2
- raw_files_committed = false
- normalized_derivatives_added = false
- extracted_text_added = false
- visibility = hash_only_public_reference
- public_release_approved = false
- schema_file_present = true
- raw_private_docx_files_committed = false

## Schema repair language

- schema file present: schema/bridge/source_corpus_pricing_release_report_batch.schema.json
- pricing/release source batch validates against the schema.
- no payment, subscription billing, customer entitlement, marketplace, product readiness, product release, compliance/legal/audit/truth/memory/export/federation/authority behavior emitted.

## Pricing/release source identities

- Apprentice Echo Bundle and pricing memo_6_12_2026_500PM.docx
- 3ec57bef5253bb0da3cc87aab7035f434046a5cccef5779ed341a11d0929d0c9
- Pricing Study and Release Consult 6_11_2026_918PM.docx
- a4e3fa673ffb0338fc025de78b63f14b9704adc979a0abebc55d20f686212f4b

## Preserved product strategy conclusions

- Sell governed AI work-event evidence infrastructure, not compliance certification.
- Governed Receipt Core should be the first product.
- Framework Evidence Packs should sit on top of the core.
- Enterprise Adapters and Recovery should come later.
- Governed work-event / receipt transaction is the preferred pricing unit.
- Evidence support is the product; compliance certification is not the product.
- A watermark says AI was here; a governed receipt says what happened.
- Product maturity should be labeled as live, near-ready, design-only, simulation-only, future, or out-of-scope.
- Bundle-first packaging is useful, but too many SKUs too early should be avoided.
- Unsupported claims should be first-class report objects.
- Reports should support human-readable report, machine-readable JSON, and evidence-index CSV export.

## Pricing/release doctrine

- Raw private pricing/release reports are not committed.
- Hashes preserve identity; hashes do not certify truth.
- Source reports preserve product strategy provenance, not canonical repo state.
- Pricing strategy is not payment implementation.
- Subscription strategy is not subscription billing.
- Bundle strategy is not customer entitlement.
- Product strategy is not product readiness or product release.
- Human review remains required.

## Relation to prior phases

- CONTROL-PACKAGE-MANIFEST-STANDARD-00 defines package metadata and boundaries.
- CONTROL-PACKAGE-REGISTRY-DESIGN-00 records package availability and state.
- CONTROL-PACKAGE-INSTALL-SIMULATION-00 simulates package state transitions.
- CONTROL-PACKAGE-CATALOG-BUNDLE-DESIGN-00 groups packages into customer-facing bundles.
- SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-2026-06-12-00 preserves pricing/release strategy provenance.
- SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-SCHEMA-REPAIR-00 repairs schema validation for the source batch.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides the local explicit-ingress prototype.

## Required artifacts

- docs/provenance/source_reports/2026-06/pricing_release_report_batch_20260612.json
- docs/provenance/source_reports/2026-06/pricing_release_report_batch_aliases_20260612.json
- docs/provenance/source_reports/2026-06/pricing_release_report_batch_sha256sums_20260612.txt
- docs/provenance/source_reports/2026-06/pricing_release_report_batch_summary_20260612.md
- schema/bridge/source_corpus_pricing_release_report_batch.schema.json
- python/tests/provenance/test_source_corpus_pricing_release_report_batch_20260612.py

## Blocked overclaims

- pricing report implements payment
- pricing report implements subscription billing
- pricing report grants customer entitlement
- release report releases product
- pricing report proves product readiness
- source report is canonical repo state
- source report certifies compliance
- source report provides legal advice
- source report passes audit
- source report certifies truth
- source report writes memory
- source report admits Atlas memory
- source report exports traces
- source report federates PMR
- summary is source
- hash certifies truth

## Reproducibility

- test_source_corpus_pricing_release_report_batch_20260612.py
- source_corpus_pricing_release_report_batch.schema.json
- `python -m pytest -q python/tests/provenance/test_source_corpus_pricing_release_report_batch_20260612.py tests/test_experiment_registry.py`

Publication sync grants no runtime authority. SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-SCHEMA-REPAIR-00 repairs schema validation only and does not import raw DOCX files, approve public release, implement payment/subscriptions/entitlements/marketplace behavior, release product, certify compliance/truth, write memory, export traces, federate PMR, authorize final answers, or grant accepted-evidence authority.

## Catalog bundle and pricing/release provenance publication sync

CONTROL-PACKAGE-CATALOG-BUNDLE-DESIGN-00 groups packages into customer-facing bundles without implementing payment, subscriptions, marketplace downloads, customer entitlement, install, activation, execution, compliance, audit, product release, product readiness, or authority. SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-2026-06-12-00 preserves pricing/release strategy reports as hash-only provenance, and SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-SCHEMA-REPAIR-00 repairs schema validation only.

- CONTROL-PACKAGE-MANIFEST-STANDARD-00 defines package metadata and boundaries.
- CONTROL-PACKAGE-REGISTRY-DESIGN-00 records package availability and state.
- CONTROL-PACKAGE-INSTALL-SIMULATION-00 simulates package state transitions.
- CONTROL-PACKAGE-CATALOG-BUNDLE-DESIGN-00 groups packages into customer-facing bundles.
- SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-2026-06-12-00 preserves pricing/release strategy provenance.
- SOURCE-CORPUS-PRICING-RELEASE-REPORTS-BATCH-SCHEMA-REPAIR-00 repairs schema validation for the source batch.
- AI-RECEIPT-GATEWAY-LOCAL-INGRESS-PROTOTYPE-00 provides the local explicit-ingress prototype.
