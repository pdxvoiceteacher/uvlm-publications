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
