# Telemetry Aperture Controller

## What was validated

TELEMETRY-APERTURE-DESIGN-00 synchronizes the locally validated Telemetry Aperture Controller design to publication surfaces. This is publication/dashboard synchronization only and grants no runtime authority. TAC docs/config/schema and experiment registry tests passed locally in CoherenceLattice. TAC does not change runtime behavior in TELEMETRY-APERTURE-DESIGN-00.

## Dashboard summary

- mode_policy_status = active_design_only
- runtime_behavior_changed = false
- default_aperture_mode = pulse
- raw_trace_retention = requires_explicit_approval
- trace_export = blocked
- pmr_federation = blocked_by_default
- minimum_audit_floor_failure_policy = fail_closed
- aperture_reduction_cannot_remove_acceptance_evidence = true
- consent_bounded_observability_aperture = true
- tac_is_not_consciousness = true
- tac_is_not_surveillance_authorization = true
- tac_is_not_memory_write = true
- tac_is_not_trace_export_authorization = true
- tac_is_not_federation_authorization = true
- tac_is_not_product_release = true
- human_review_required = true

## Required TAC language

- Telemetry Aperture Controller
- TAC is a consent-bounded observability aperture controller.
- TAC regulates temporal, semantic, retention, privacy, and review apertures.
- TAC optimizes coherent sufficiency, not maximum capture.
- TAC is computational observability aperture, not consciousness.
- TAC is not surveillance authorization.
- TAC is not memory write.
- TAC is not trace export authorization.
- TAC is not federation authorization.
- TAC is not product release.
- A narrow aperture is not permission to omit failure receipts.
- A high-resolution aperture is not permission to retain private data.
- Aperture reduction cannot remove acceptance evidence.
- Human review remains required.
- TAC does not change runtime behavior in TELEMETRY-APERTURE-DESIGN-00.
- Future TAC implementation must distinguish temporary observation from durable retention.
- Future TAC implementation must preserve AI Receipt traceability.

## Modes

- off: no optional telemetry beyond mandatory safety/status receipts
- minimal: required inventory, manifest, parity, review packet, and failure receipts only
- pulse: thin periodic metric pulses using safe MET-SEM aliases
- snapshot: periodic structured snapshots of task state and key artifacts
- trace: step-level TEL events and route transitions
- tail_retain: trace temporarily, retain full detail only if trigger conditions fire
- full_audit: high-resolution trace only under explicit consent and retention policy
- quarantine: restricted safety capture after boundary violation or critical anomaly

## Aperture dimensions

- temporal_resolution
- semantic_resolution
- retention_depth
- privacy_transformation
- review_visibility

## Minimum audit floor

- artifact_inventory.json
- run_artifact_manifest.json
- export_bundle_parity_report.json
- phase_manifest
- phase_review_packet
- acceptance_receipt
- failure_receipts
- non_authority_boundary_table
- source_span_or_claim_classification_refs_when_applicable
- tel_replay_summary_when_applicable
- pmr_retention_or_context_status_when_applicable
- validation_tier_receipt_when_available
- ai_receipt_event_chain_when_available

## Policy defaults

- default_aperture_mode = pulse
- user_consent_scope = local_replay_allowed
- raw_trace_retention = requires_explicit_approval
- trace_export = blocked
- pmr_federation = blocked_by_default
- minimum_audit_floor_required = true

## Escalation triggers

- schema_validation_error
- unsupported_claim_surge
- low_T_review
- high_Λ_boundary
- high_risk_ucc_domain
- user_requested_deep_audit
- source_span_review_bound
- sophia_nonpass_or_uncertain
- ai_receipt_incomplete

## Hard blocks

- increase_raw_retention_without_consent
- export_trace_without_consent
- federate_tel_without_consent
- drop_failure_receipts_for_cost
- drop_source_spans_for_cost
- drop_run_manifest_for_cost
- drop_boundary_table_for_cost
- full_audit_mode_without_consent
- privacy_redaction_override_without_consent
- retain_sensitive_content_without_consent

## Human review gates

- increase_durable_retention
- export_trace
- federate_memory
- override_privacy_redaction
- enable_full_audit
- reduce_below_minimum_audit_floor
- convert_trace_to_pmr_memory_intent

## Safe MET-SEM aliases

- Ψ_review
- E_review
- T_review
- ΔS_review
- Λ_boundary
- Eₛ_review
- TAF_review_runtime_v0

## Unsafe metric boundary

TAC does not present these as TAC measurements:

- unqualified empathy score
- unqualified transparency score
- unqualified phase-lock score
- unqualified entropy score
- unqualified ethical symmetry score
- canonical total action

## Failure classes

- aperture_theater
- silent_escalation
- pmr_hoarding
- under_observation
- over_observation
- dashboard_theater
- privacy_drift
- minimum_audit_floor_violation
- raw_retention_without_consent
- federation_without_consent
- trace_export_without_consent
- full_audit_without_consent
- omission_debt_hidden

## Artifacts

- docs/TELEMETRY_APERTURE_CONTROLLER.md
- config/telemetry_aperture/telemetry_aperture_modes.v1.json
- config/telemetry_aperture/minimum_audit_floor.v1.json
- config/telemetry_aperture/telemetry_aperture_policy_schema.v1.json
- schema/bridge/telemetry_aperture_policy_packet.schema.json
- schema/bridge/telemetry_aperture_decision_packet.schema.json
- schema/bridge/telemetry_aperture_retention_intent_packet.schema.json

## Reproducibility fragments

- TELEMETRY-APERTURE-DESIGN-00
- telemetry_aperture_modes.v1.json
- minimum_audit_floor.v1.json
- telemetry_aperture_policy_schema.v1.json
- telemetry_aperture_policy_packet.schema.json
- telemetry_aperture_decision_packet.schema.json
- telemetry_aperture_retention_intent_packet.schema.json

This design patch has no runtime builder. Reproducibility points to config/schema inspection, not runtime packet emission.

```powershell
python -m json.tool config/telemetry_aperture/telemetry_aperture_modes.v1.json && python -m json.tool config/telemetry_aperture/minimum_audit_floor.v1.json && python -m json.tool config/telemetry_aperture/telemetry_aperture_policy_schema.v1.json && python -m json.tool schema/bridge/telemetry_aperture_policy_packet.schema.json && python -m json.tool schema/bridge/telemetry_aperture_decision_packet.schema.json && python -m json.tool schema/bridge/telemetry_aperture_retention_intent_packet.schema.json
```

## Blocked overclaim examples for telemetry aperture controller publication boundaries

- TAC changed runtime telemetry behavior
- TAC is consciousness
- TAC is adaptive awareness
- TAC authorizes surveillance
- TAC authorizes trace export
- TAC authorizes PMR federation
- TAC authorizes memory write
- TAC authorizes Atlas memory admission
- TAC authorizes provider runtime
- TAC authorizes deployment
- TAC is product release
- TAC certifies truth
- TAC certifies compliance
- TAC authorizes final answers
- TAC grants accepted-evidence authority
- full_audit mode can run without consent
- raw trace retention is allowed without consent
- trace export is allowed without consent
- PMR federation is allowed by default
- aperture reduction can remove acceptance evidence
- narrow aperture can omit failure receipts
- high-resolution aperture can retain private data without consent
- safe MET-SEM aliases are canonical metric completion
- TAC proves human benefit
- TAC is market validation
- TAC proves consciousness
- TAC detects Omega
- TAC proves universal ontology

## Allowed bounded claim

TELEMETRY-APERTURE-DESIGN-00 defines a design-only, consent-bounded Telemetry Aperture Controller policy over observability modes, minimum audit floor, retention/export/federation blocks, and human-review gates without changing runtime behavior or granting surveillance, memory, trace export, federation, product, certification, deployment, final-answer, accepted-evidence, Atlas, human benefit, market, consciousness, Omega, or ontology authority.

## Policy simulation linkage

TAC-POLICY-SIMULATION-00 rehearses deterministic policy decisions from TELEMETRY-APERTURE-DESIGN-00. TAC-LOCAL-REVIEW-INTEGRATION-00 links simulated TAC posture into local review surfaces. TAC-AI-RECEIPT-EVENT-LINK-00 links TAC posture through supplemental, non-rewriting AI Receipt event references. PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 must respect TAC retention, trace export, and federation boundaries. COHERENCE-EVENT-SIGNATURES-DESIGN-00 is aperture-aware and PMR-retention-aware but does not emit CES runtime artifacts. TAC-POLICY-SIMULATION-00 does not implement live runtime control.

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
