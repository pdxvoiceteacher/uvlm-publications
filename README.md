# Ultra Verba Lux Mentis Publication Registry

![Mint DOI](https://github.com/ultra-verba-lux-mentis/uvlm-publications/actions/workflows/mint_doi.yml/badge.svg)

Canonical source for UVLM scholarly publications and DOI minting.

## Repository Structure

- `papers/`: publication packages (`paper.pdf`, `metadata.yaml`, local docs).
- `schemas/`: JSON schema validation rules (publication, knowledge graph, constellations).
- `scripts/`: metadata validation, hash generation, Crossref XML/deposit automation.
- `registry/dois.json`: slug-based DOI state registry.
- `registry/publications.json`: global publication index keyed by DOI suffix.
- `registry/catalog.json`: website-oriented publication feed generated from metadata + index.
- `registry/knowledge_graph.json`: deterministic knowledge graph generated from catalog + declared relations.
- `registry/deposits/`: deposit audit logs.
- `.github/workflows/`: CI workflows.
- `DOI_NAMESPACE.md`: canonical DOI naming policy.

## DOI Namespace Policy

UVLM DOI suffixes must follow:

`uvlm.<type>.<slug>.<version>`

Examples:

- `uvlm.paper.echo-atlas-primer.v1`
- `uvlm.dataset.coherence-lattice.v1`
- `uvlm.software.sophia-ledger.v1`

Final DOI format in Crossref is:

`10.<prefix>/uvlm.<type>.<slug>.<version>`

## Metadata Format

Each `papers/<slug>/metadata.yaml` includes:

- `title`
- `type` (`paper`, `dataset`, `software`, `book`, `working-paper`)
- `authors` with required ORCID (`0000-0000-0000-0000`)
- `publisher` (explicit, e.g. `Ultra Verba Lux Mentis`)
- `series` (e.g. `UVLM Working Papers`)
- `language` (2-letter code, e.g. `en`)
- `keywords` (array of indexable topic strings)
- optional `concepts` (explicit concept labels for concept graph nodes)
- optional `concept_relations` (explicit concept hierarchy relations such as `contains`)
- required `abstract`
- `publication_date` in ISO format `YYYY-MM-DD`
- `doi_suffix`
- `url` (must be a secure `https://` URL)
- `content_hash` (SHA-256 of `paper.pdf`)
- optional `relations` entries with DOI links

Schema is enforced by `schemas/publication_schema.json`.

## DOI Generation Workflow

1. `scripts/update_content_hash.py` computes deterministic `content_hash`.
2. `scripts/validate_metadata.py` validates schema + verifies hash.
3. `scripts/generate_crossref_xml.py` creates `crossref_deposit.xml` with relation, language, and keyword support.
4. `scripts/validate_crossref_xml.py` validates generated Crossref XML structure and DOI/resource fields.
5. `scripts/deposit_crossref.py --dry-run` validates payload without minting.
6. `scripts/deposit_crossref.py` deposits and updates:
   - `registry/dois.json` (`pending`, `registered`, `failed`, `updated`)
   - `registry/publications.json` global publication index
   - `registry/deposits/<date>_<slug>.json` audit logs
7. `scripts/build_catalog.py` generates `registry/catalog.json` for website/indexing consumers.
8. `scripts/build_knowledge_graph.py` generates `registry/knowledge_graph.json`.
9. `scripts/validate_knowledge_graph.py` validates graph node/edge structure.

Required environment variables:

- `CROSSREF_USERNAME`
- `CROSSREF_PASSWORD`
- `DOI_PREFIX`

## Local Validation Quickstart

Use this minimal sequence before committing publication or overlay changes:

```bash
python3 scripts/validate_metadata.py
python3 scripts/build_catalog.py
python3 scripts/build_knowledge_graph.py
python3 scripts/validate_knowledge_graph.py
python3 -m unittest tests/test_build_public_record_overlay.py tests/test_build_verification_overlay.py tests/test_build_investigation_overlay.py tests/test_build_evidence_authority_overlay.py tests/test_build_review_packet_overlay.py tests/test_build_pattern_overlay.py tests/test_build_pattern_temporal_overlay.py tests/test_build_symbolic_field_overlay.py tests/test_build_closure_overlay.py tests/test_build_priority_overlay.py tests/test_build_queue_health_overlay.py tests/test_build_institutional_overlay.py tests/test_validate_atlas_timeline.py tests/test_validate_constellations.py
```

These checks keep metadata, graph artifacts, and overlay contracts deterministic and auditable.

## Live Knowledge Graph (Phase 1: Deterministic)

`registry/knowledge_graph.json` is built from:

- `registry/catalog.json`
- declared per-paper `relations` in `papers/**/metadata.yaml`
- declared per-paper `concepts` in `papers/**/metadata.yaml`
- declared per-paper `concept_relations` in `papers/**/metadata.yaml`

Node classes:

- `publication`
- `author`
- `keyword`
- `series`
- `concept`

Edge classes:

- `authoredBy`
- `taggedWith`
- `publishedIn`
- `mentionsConcept`
- `contains`
- `cites`
- `isVersionOf`
- `isPartOf`
- `isReferencedBy`

Phase 1 intentionally avoids inferred similarity edges and ontology expansion to keep the graph explicit, deterministic, and auditable.



## UVLM Research Atlas (Phase 2)

An interactive atlas is available at `atlas/index.html`.

- engine: Cytoscape.js with deterministic preset positions + light `fcose` relaxation
- input: `registry/knowledge_graph.json`
- modular frontend files:
  - `atlas/atlas.js` (bootstrap + view orchestration)
  - `atlas/layoutConfig.js` (physics + orbit constants)
  - `atlas/layoutEngine.js` (concept anchors, publication orbits, shell placement)
  - `atlas/zoomLevels.js` (zoom thresholds + visibility layers)
  - `atlas/zoomController.js` (camera-driven multi-scale transitions)
  - `atlas/nodeStyles.js` (class style map)
  - `atlas/search.js` (search/filter helpers)
  - `atlas/metadataPanel.js` (detail panel rendering)

### Multi-Scale Zoom Architecture

Zoom controls graph abstraction layers (not only camera scale):

- **Galaxy view**: `concept + series`
- **Solar view**: `concept + publication + series`
- **Orbit view**: `concept + publication + keyword + author + series`

Atlas supports both automatic zoom-driven transitions and manual controls (`Galaxy`, `Solar`, `Orbit`).

- concept click → focus solar-system view
- publication click → focus orbit-detail view
- smooth transitions via Cytoscape animations

Visual metaphor mapping:

- `concept` → star
- `publication` → planet
- `author` → constellation
- `keyword` → nebula
- `series` → solar system

To run locally:

```bash
python3 -m http.server 8000
# open http://localhost:8000/atlas/
```

### Phase-lock integration rule (CoherenceLattice → Sophia → Publisher)

The atlas overlay pipeline follows a strict order:

1. **CoherenceLattice** provides formal coherence truth (including canonical drift).
2. **Sophia** provides executive interpretation (canonical attention updates).
3. **Publisher (Atlas)** renders overlays and presents memory-facing metadata.

Semantics used in this repo:

- **Formal drift** = CoherenceLattice truth (`bridge/coherence_drift_map.json`).
- **Attention update** = Sophia executive interpretation (`bridge/attention_updates.json`).
- **Overlay rendering** = Publisher visualization layer (Atlas modules).

Publisher may include local UI diagnostics, but they must be clearly separated from canonical policy metrics (e.g., `activityMismatchScore` is a local rendering diagnostic, not formal drift).

### Sonya memory ingestion gate (Phase C)

Publisher memory artifacts ingest **only Sophia-audited Sonya decisions**.

Required order:

1. raw Sonya input
2. CoherenceLattice projection
3. Sophia audit/admission decision
4. Publisher memory storage

Publisher does **not** store raw Sonya input directly into canonical corpus memory.

Current memory-gating artifacts:

- inputs: `bridge/sonya_audit.json`, `bridge/sonya_admission_decisions.json`
- canonical outputs: `registry/sonya_memory_index.json`, `registry/sonya_memory_annotations.json`, `registry/sonya_attention_candidates.json`
- non-canonical holding area (optional): `registry/sonya_pending_review.json`

Build command:

```bash
python3 scripts/build_sonya_memory_overlay.py
```

### Reasoning-thread overlay gate (Phase D)

Publisher surfaces only **Sophia-audited reasoning-thread overlays** and watch artifacts.
It does not independently infer, certify, or mutate higher cognition truth.

- inputs: `bridge/reasoning_audit.json`, `bridge/recursive_reasoning_candidates.json`, and admitted Sonya memory artifacts
- canonical outputs: `registry/reasoning_threads.json`, `registry/reasoning_thread_annotations.json`
- observational non-canonical output: `registry/cognitive_watchlist.json`

Build command:

```bash
python3 scripts/build_reasoning_thread_overlay.py
```

### Recursive coherence monitoring overlay gate (Phase E)

Publisher surfaces only **Sophia-audited monitoring overlays** and watch / human-review signals.
It does not independently certify cognitive status.

- inputs: `bridge/stability_audit.json`, `bridge/recursive_watch_escalations.json`, `registry/reasoning_threads.json`, `registry/cognitive_watchlist.json`
- canonical outputs: `registry/cognitive_monitor_index.json`, `registry/cognitive_stability_annotations.json`
- observational non-canonical output: `registry/recursive_watch_history.json`

Build command:

```bash
python3 scripts/build_cognitive_monitor_overlay.py
```

### Multimodal pattern donation overlay gate (Phase F)

Publisher surfaces only **Sophia-audited multimodal donation overlays** and watch artifacts.
It does not independently interpret raw pattern signals or mutate canonical structure.

- inputs: `bridge/pattern_donation_audit.json`, `bridge/pattern_donation_decisions.json`, `bridge/cross_modal_reinforcement_report.json`, monitor/reasoning/watch overlays
- canonical outputs: `registry/multimodal_signal_index.json`, `registry/pattern_donation_annotations.json`, `registry/cross_modal_attention_overlays.json`
- observational non-canonical output: `registry/pattern_donation_watchlist.json`

Build command:

```bash
python3 scripts/build_multimodal_overlay.py
```

### Human review promotion gate (Phase G)

Publisher surfaces only **Sophia-audited review candidates and watch items**.
Human promotion decisions remain external to automation.

- inputs: `bridge/promotion_audit.json`, `bridge/promotion_recommendations.json`, and surfaced reasoning/monitoring/multimodal overlays
- canonical output: `registry/review_docket.json`, `registry/promotion_annotations.json`
- observational non-canonical output: `registry/promotion_watch_queue.json`

Build command:

```bash
python3 scripts/build_review_docket.py
```

### Governance integrity protocol (Phase H)

Publisher surfaces only **Sophia-audited governance review materials**.
Final appointment/removal decisions remain human/community decisions external to automation.

- inputs: `bridge/governance_audit.json`, `bridge/governance_recommendations.json`, optional `bridge/reviewer_behavior_audit.json`, `registry/review_docket.json`
- canonical output: `registry/governance_review_docket.json`, `registry/reviewer_integrity_annotations.json`
- observational non-canonical outputs: `registry/reviewer_watch_queue.json`, `registry/reviewer_behavior_monitor.json`

Build command:

```bash
python3 scripts/build_governance_review_overlay.py
```

### Constitutional charter and continuity mode overlays (Phase I)

Publisher surfaces only **Sophia-audited constitutional and continuity overlays**.
These artifacts are governance-facing recommendations only; final constitutional actions remain external (human/community governed).

- inputs: `bridge/constitutional_audit.json`, `bridge/constitutional_recommendations.json`, `bridge/continuity_mode_assessment.json`
- governance-facing non-canonical outputs: `registry/constitutional_status.json`, `registry/continuity_mode_index.json`, `registry/constitutional_annotations.json`, `registry/governance_failure_watchlist.json`

Build command:

```bash
python3 scripts/build_constitutional_overlay.py
```


### Deliberative quorum and amendment protocol (Phase J)

Publisher surfaces only **Sophia-audited deliberation and amendment review materials** as a deliberation chamber.
The system prepares lawful constitutional review context; constitutional change remains external to automation.

- inputs: `bridge/quorum_audit.json`, `bridge/amendment_recommendations.json`, `bridge/deliberation_state_map.json`, `bridge/amendment_candidate_map.json`, `registry/constitutional_status.json`, `registry/governance_review_docket.json`
- governance-facing non-canonical outputs: `registry/deliberation_docket.json`, `registry/amendment_queue.json`, `registry/quorum_watchlist.json`, `registry/constitutional_revision_annotations.json`
- phase lock: constitutional state → deliberation/amendment formalization → Sophia quorum/amendment audit → publisher deliberation docket + amendment queue → human/community constitutional review

Build command:

```bash
python3 scripts/build_deliberation_overlay.py
```


### Succession, redundancy, and anti-capture resilience protocol (Phase K)

Publisher surfaces **Sophia-audited continuity and succession review materials only** as a continuity and resilience chamber.
Final continuity and reviewer appointment decisions remain external and human/community governed.

- inputs: `bridge/resilience_audit.json`, `bridge/succession_recommendations.json`, `bridge/succession_state_map.json`, `bridge/continuity_roster_candidates.json`, `registry/governance_review_docket.json`, `registry/reviewer_behavior_monitor.json`, `registry/constitutional_status.json`
- governance-facing non-canonical outputs: `registry/continuity_roster.json`, `registry/succession_docket.json`, `registry/quorum_resilience_watchlist.json`, `registry/governance_redundancy_annotations.json`
- phase lock: governance body state → succession/resilience formalization → Sophia resilience audit → publisher continuity/succession overlays → human/community continuity decision

Build command:

```bash
python3 scripts/build_continuity_overlay.py
```


### Evidence escrow, replication, and recovery protocol (Phase L)

Publisher surfaces only **Sophia-audited preservation and recovery review materials** as an evidence escrow and recovery chamber.
Actual escrow or recovery action remains external and human/community governed.

- inputs: `bridge/recovery_audit.json`, `bridge/recovery_recommendations.json`, `bridge/preservation_state_map.json`, `bridge/artifact_escrow_plan.json`, `bridge/recovery_candidate_map.json`, `registry/constitutional_status.json`, `registry/continuity_mode_index.json`
- governance-facing non-canonical outputs: `registry/escrow_index.json`, `registry/recovery_docket.json`, `registry/integrity_watchlist.json`, `registry/recovery_annotations.json`
- phase lock: artifact/governance/continuity state → preservation/recovery formalization → Sophia recovery audit → publisher escrow/recovery overlays → human/community recovery action
- procedural guardrails: evidence escrow over opaque persistence; recovery by review (no silent resurrection); freeze under tamper ambiguity; dependency transparency; distributed preservation over concentrated custody

Build command:

```bash
python3 scripts/build_recovery_overlay.py
```


### Federated witness and external attestation protocol (Phase M)

Publisher surfaces only **Sophia-audited attestation and witness materials** as an integrity witness chamber.
Actual witnessing and any resulting human/community decisions remain external to automation.

- inputs: `bridge/witness_audit.json`, `bridge/attestation_recommendations.json`, `bridge/attestation_state_map.json`, `bridge/witness_roster_candidates.json`, `registry/escrow_index.json`, `registry/recovery_docket.json`, `registry/continuity_roster.json`
- governance-facing non-canonical outputs: `registry/attestation_registry.json`, `registry/witness_docket.json`, `registry/integrity_testimony_watchlist.json`, `registry/attestation_annotations.json`
- phase lock: canonical/continuity/recovery state → attestation formalization → Sophia witness/attestation audit → publisher attestation overlays → external human/community witnessing
- procedural guardrails: witnessing over secrecy; distribution over monopoly; attestation without sovereignty; freeze under attestation ambiguity; evidence-first continuity

Build command:

```bash
python3 scripts/build_attestation_overlay.py
```


### Normative memory and precedent protocol (Phase N)

Publisher surfaces only **Sophia-audited precedent and case-analogy materials** as a precedent and case-memory chamber.
Actual doctrinal use remains external to automation.

- inputs: `bridge/precedent_audit.json`, `bridge/precedent_recommendations.json`, `bridge/precedent_state_map.json`, `bridge/case_analogy_candidates.json`, `registry/review_docket.json`, `registry/governance_review_docket.json`, `registry/deliberation_docket.json`, `registry/recovery_docket.json`, `registry/witness_docket.json`
- governance-facing non-canonical outputs: `registry/precedent_registry.json`, `registry/case_docket.json`, `registry/divergence_watchlist.json`, `registry/precedent_annotations.json`
- phase lock: review/governance/continuity/attestation outcomes → precedent formalization → Sophia precedent audit → publisher precedent/case-memory overlays → human/community use of precedent
- procedural guardrails: precedent is persuasive, not absolute; divergence requires explanation; weak precedent must not harden into dogma; constitutional principles outrank precedent; anti-capture overrides convenience

Build command:

```bash
python3 scripts/build_precedent_overlay.py
```



### Simulation, stress testing, and adversarial scenario protocol (Phase O)

Publisher surfaces only **Sophia-audited hypothetical scenario materials; these are preparedness tools, not live authority triggers**.

- inputs: `bridge/scenario_audit.json`, `bridge/scenario_recommendations.json`, `bridge/scenario_state_map.json`, `bridge/scenario_outcome_projection.json`, `registry/governance_review_docket.json`, `registry/quorum_resilience_watchlist.json`, `registry/integrity_testimony_watchlist.json`, `registry/divergence_watchlist.json`
- preparedness-facing non-canonical outputs: `registry/scenario_registry.json`, `registry/stress_test_docket.json`, `registry/resilience_findings_watchlist.json`, `registry/scenario_annotations.json`
- phase lock: current system state → CoherenceLattice scenario formalization → Sophia scenario audit → publisher scenario/stress-test overlays → human/community preparedness review
- procedural principles: rehearse before crisis; freeze before blind escalation; capture rehearsal matters; preparedness is not authority; recovery conflicts must be rehearsed
- caution: supports stress rehearsal and resilience findings for review; does **not** authorize automatic emergency activation or scenario-based sovereignty

Build command:

```bash
python3 scripts/build_scenario_overlay.py
```


### Institutional synthesis and system-health protocol (Phase P)

Publisher surfaces institutional state from **CoherenceLattice deterministic synthesis and Sophia-audited bounded recommendations** as preparedness and governance context, without mutating canonical truth.

- inputs: `bridge/institutional_audit.json`, `bridge/institutional_recommendations.json`, `bridge/institutional_state_map.json`, `bridge/institutional_state_summary.json`, `bridge/institutional_conflict_report.json`, `bridge/institutional_health_projection.json`, `registry/governance_review_docket.json`, `registry/quorum_resilience_watchlist.json`, `registry/integrity_testimony_watchlist.json`, `registry/divergence_watchlist.json`
- non-canonical outputs: `registry/institutional_status.json`, `registry/system_health_dashboard.json`, `registry/institutional_conflict_watchlist.json`, `registry/institutional_annotations.json`
- publication rules: only `targetPublisherAction=docket` enters institutional status and system-health dashboard; watch entries remain in institutional conflict watchlist; suppressed entries stay annotation-only
- UI focus: institutional status indicator, chamber conflict indicators, and system health overview for bounded visibility
- contract hardening: `bridge/institutional_synthesis.json` is deprecated and rejected by the builder to prevent semantic aliasing

Build command:

```bash
python3 scripts/build_institutional_overlay.py
```


### Queue pressure, anti-Goodhart, and load-shedding protocol (Phase Q)

Publisher surfaces only **Sophia-audited queue-health and anti-Goodhart materials; no automatic archival, freezing, or deletion occurs from this layer alone**.

- inputs: `bridge/load_shedding_audit.json`, `bridge/load_shedding_recommendations.json`, `bridge/queue_pressure_map.json`, `bridge/queue_pressure_summary.json`, `bridge/review_load_distribution.json`, `bridge/goodhart_risk_report.json`, `registry/institutional_status.json`, `registry/system_health_dashboard.json`, `registry/review_docket.json`, `registry/governance_review_docket.json`, `registry/deliberation_docket.json`, `registry/recovery_docket.json`, `registry/witness_docket.json`, `registry/case_docket.json`, `registry/stress_test_docket.json`
- non-canonical outputs: `registry/queue_health_dashboard.json`, `registry/review_backlog_watchlist.json`, `registry/metric_gaming_watchlist.json`, `registry/load_shedding_annotations.json`
- phase lock: queue/review/watchlist state → CoherenceLattice pressure formalization → Sophia load-shedding and anti-Goodhart audit → publisher queue-health overlays → human/community operational review
- principles: queue overload is a governance signal; delay can be capture; metric performance is not integrity; review fatigue reduces legitimacy; load shedding must be explicit, auditable, and reversible

Build command:

```bash
python3 scripts/build_queue_health_overlay.py
```


### Resolution priority and triage protocol (Phase R)

Publisher surfaces only **Sophia-audited priority and triage materials; no automatic queue reordering or canonical mutation occurs from this layer**.

- inputs: `bridge/triage_audit.json`, `bridge/triage_recommendations.json`, `bridge/priority_state_map.json`, `bridge/priority_state_summary.json`, `bridge/triage_candidate_map.json`, `bridge/triage_conflict_report.json`, `registry/queue_health_dashboard.json`, `registry/system_health_dashboard.json`, `registry/review_backlog_watchlist.json`, `registry/metric_gaming_watchlist.json`
- non-canonical outputs: `registry/priority_dashboard.json`, `registry/triage_docket.json`, `registry/triage_watchlist.json`, `registry/priority_annotations.json`
- phase lock: institutional/queue/watchlist state → CoherenceLattice priority formalization → Sophia triage audit → publisher priority overlays → human/community ordered review
- principles: attention is a constitutional resource; priority must be explicit; reversible issues can wait longer than irreversible ones; capture risk increases priority; triage must remain reviewable

Build command:

```bash
python3 scripts/build_priority_overlay.py
```


### Closure, outcome logging, and repair protocol (Phase S)

Publisher surfaces only **Sophia-audited closure and repair materials; no automatic reopening, closure, or repair occurs from this layer**.

- inputs: `bridge/closure_audit.json`, `bridge/closure_recommendations.json`, `bridge/closure_state_map.json`, `bridge/closure_state_summary.json`, `bridge/repair_candidate_map.json`, `bridge/reopen_signal_report.json`, `registry/priority_dashboard.json`, `registry/triage_docket.json`, `registry/triage_watchlist.json`
- non-canonical outputs: `registry/closure_registry.json`, `registry/repair_docket.json`, `registry/reopened_case_watchlist.json`, `registry/closure_annotations.json`
- phase lock: docket/outcome/recommendation state → CoherenceLattice closure and repair formalization → Sophia closure audit → publisher closure and repair overlays → human/community review of outcome durability
- principles: processed is not the same as resolved; closure must be reviewable; provisional closure should be explicit; repair is part of integrity; reopening must be evidence-bound

Build command:

```bash
python3 scripts/build_closure_overlay.py
```


### Multi-axial symbolic field and early-warning protocol (Phase T)

Publisher surfaces only **Sophia-audited symbolic field and early-warning materials; no automatic intervention or memory mutation occurs from this layer**.

- inputs: `bridge/symbolic_field_audit.json`, `bridge/symbolic_field_recommendations.json`, `bridge/symbolic_field_state.json`, `bridge/symbolic_field_summary.json`, `bridge/regime_transition_report.json`, `bridge/early_warning_signal_map.json`, `registry/institutional_status.json`, `registry/queue_health_dashboard.json`, `registry/priority_dashboard.json`, `registry/closure_registry.json`
- non-canonical outputs: `registry/symbolic_field_registry.json`, `registry/early_warning_dashboard.json`, `registry/regime_watchlist.json`, `registry/symbolic_field_annotations.json`
- phase lock: institutional/queue/priority/closure state → CoherenceLattice symbolic field formalization → Sophia symbolic field audit → publisher symbolic field overlays → human/community early-warning review
- principles: symbolic signals are directional, not verdicts; early warning must be bounded and evidence-tied; TEL-like memory visibility must remain auditable; watch state is not automatic intervention; architecture hints are review inputs, not canonical edits

Build command:

```bash
python3 scripts/build_symbolic_field_overlay.py
```


### Claim typing, entity resolution, and verification task protocol (Phase U)

Publisher surfaces only **Sophia-audited verification materials; no automatic accusation, identity resolution, or canonical mutation occurs from this layer**.

- inputs: `bridge/verification_audit.json`, `bridge/verification_recommendations.json`, `bridge/claim_type_map.json`, `bridge/entity_resolution_map.json`, `bridge/entity_resolution_summary.json`, `bridge/verification_task_map.json`, `registry/symbolic_field_registry.json`, `registry/closure_registry.json`, `registry/priority_dashboard.json`
- non-canonical outputs: `registry/verification_dashboard.json`, `registry/entity_watchlist.json`, `registry/claim_type_registry.json`, `registry/verification_annotations.json`
- phase lock: symbolic/closure/priority state → CoherenceLattice claim typing and identity formalization → Sophia verification audit → publisher verification overlays → human/community evidence review
- principles: claim typing is triage, not blame; ambiguity must remain explicit; verification work must be evidence-bound; unresolved identity cannot be auto-resolved; watch state is observational, not punitive

Build command:

```bash
python3 scripts/build_verification_overlay.py
```


### Public record ingestion, entity graph, and chain-of-custody protocol (Phase V)

Publisher surfaces only **Sophia-audited public-record mapping materials; no automatic accusation, graph hardening, or identity mutation occurs from this layer**.

- inputs: `bridge/public_record_audit.json`, `bridge/public_record_recommendations.json`, `bridge/public_record_intake_map.json`, `bridge/entity_graph_map.json`, `bridge/relationship_edge_map.json`, `bridge/chain_of_custody_report.json`, `registry/verification_dashboard.json`, `registry/claim_type_registry.json`, `registry/entity_watchlist.json`
- non-canonical outputs: `registry/public_record_dashboard.json`, `registry/entity_graph_registry.json`, `registry/relationship_watchlist.json`, `registry/chain_of_custody_annotations.json`
- phase lock: verification/claim/entity state → CoherenceLattice public-record and custody formalization → Sophia public-record audit → publisher record-mapping overlays → human/community lawful record review
- principles: record intake is evidentiary, not accusatory; relationship ambiguity must remain explicit; custody integrity must stay traceable; watch state is observational; graph visibility is not canonical graph mutation

Build command:

```bash
python3 scripts/build_public_record_overlay.py
```


### Investigation staging and dependency-plan protocol (Phase W)

Publisher surfaces only **bounded investigation planning overlays; no automatic adjudication, identity mutation, or canonical state mutation occurs from this layer**.

- inputs: `bridge/triage_recommendations.json`, `bridge/verification_recommendations.json`, `bridge/public_record_recommendations.json`, `bridge/artifact_escrow_plan.json`
- non-canonical outputs: `registry/investigation_dashboard.json`, `registry/investigation_plan_registry.json`, `registry/investigation_watchlist.json`, `registry/investigation_annotations.json`
- phase lock: triage/verification/public-record recommendations → dependency-aware plan composition → publisher investigation overlays → human/community execution review
- principles: stage indicators are workflow signals, not verdicts; dependency graphs remain evidence-local; plan progress is observational and review-facing; watch states never auto-trigger canonical mutation

Build command:

```bash
python3 scripts/build_investigation_overlay.py
```



### Evidence maturity gating and propagation rights protocol (Phase X.1)

Publisher surfaces only Sophia-audited evidence-authority materials; no automatic restriction lifting or graph hardening occurs from this layer.

- inputs: `bridge/evidence_authority_audit.json`, `bridge/evidence_authority_recommendations.json`, `bridge/evidence_authority_map.json`, `bridge/evidence_authority_summary.json`, `bridge/propagation_rights_map.json`, `bridge/maturity_gate_report.json`, `registry/verification_dashboard.json`, `registry/public_record_dashboard.json`, `registry/symbolic_field_registry.json`, `registry/investigation_dashboard.json`
- non-canonical outputs: `registry/authority_gate_dashboard.json`, `registry/weak_evidence_watchlist.json`, `registry/propagation_annotations.json`, `registry/maturity_restriction_registry.json`
- phase lock: claim / entity / graph / closure / precedent / investigation state → CoherenceLattice evidence-authority formalization → Sophia evidence-authority audit → Publisher authority-gating overlays → human/community review of propagation limits
- principles: weak evidence remains watch-only; propagation restrictions are bounded and non-punitive; suppressed recommendations are excluded from actionable authority overlays; no automatic mutation of identities/edges/precedents/closures/canonical truth artifacts

Build command:

```bash
python3 scripts/build_evidence_authority_overlay.py
```



### Human review packet and narrative synthesis protocol (Phase Y)

Publisher surfaces only Sophia-audited review packets and uncertainty disclosures; no automatic accusation, publication, or canonical mutation occurs from this layer.

- inputs: `bridge/review_packet_audit.json`, `bridge/review_packet_recommendations.json`, `bridge/review_packet_map.json`, `bridge/review_packet_summary.json`, `bridge/narrative_synthesis_map.json`, `bridge/uncertainty_disclosure_report.json`, `registry/investigation_dashboard.json`, `registry/public_record_dashboard.json`, `registry/authority_gate_dashboard.json`
- non-canonical outputs: `registry/review_packet_dashboard.json`, `registry/review_packet_registry.json`, `registry/uncertainty_watchlist.json`, `registry/review_packet_annotations.json`
- phase lock: investigation / verification / evidence-authority state → CoherenceLattice review-packet formalization → Sophia packet audit → Publisher review-packet overlays → human/community bounded review
- principles: docket packets stay bounded and uncertainty-explicit; watch packets remain observational; suppressed items are excluded from actionable overlays; no automatic mutation of identities/edges/precedents/closures/canonical truth artifacts

Build command:

```bash
python3 scripts/build_review_packet_overlay.py
```



### Pattern cluster and cross-case protocol (Phase Z)

Publisher surfaces only Sophia-audited pattern cluster materials; no automatic accusation, publication, graph mutation, or canonical mutation occurs from this layer.

- inputs: `bridge/pattern_audit.json`, `bridge/pattern_recommendations.json`, `bridge/pattern_cluster_map.json`, `bridge/pattern_maturity_map.json`, `bridge/cross_case_relationship_map.json`, `bridge/pattern_conflict_report.json`, `registry/investigation_dashboard.json`, `registry/authority_gate_dashboard.json`, `registry/review_packet_dashboard.json`
- non-canonical outputs: `registry/pattern_dashboard.json`, `registry/pattern_registry.json`, `registry/pattern_watchlist.json`, `registry/pattern_annotations.json`
- phase lock: investigation / authority / review-packet state → CoherenceLattice pattern formalization → Sophia pattern audit → Publisher pattern overlays → human/community bounded review
- principles: actionable pattern clusters require docket recommendation; watch patterns remain observational; suppressed items excluded from actionable overlays; conflict markers are cautionary hints, not verdicts

Build command:

```bash
python3 scripts/build_pattern_overlay.py
```



### Pattern temporal persistence protocol (Phase Z.1)

Publisher surfaces only Sophia-audited temporal pattern materials; no automatic accusation, graph mutation, or canonical mutation occurs from this layer.

- inputs: `bridge/pattern_temporal_audit.json`, `bridge/pattern_temporal_recommendations.json`, `bridge/pattern_timeline_map.json`, `bridge/pattern_persistence_map.json`, `bridge/pattern_temporal_conflict_report.json`, `registry/pattern_dashboard.json`, `registry/pattern_registry.json`, `registry/pattern_watchlist.json`
- non-canonical outputs: `registry/pattern_timeline_dashboard.json`, `registry/pattern_persistence_registry.json`, `registry/pattern_temporal_watchlist.json`, `registry/pattern_temporal_annotations.json`
- phase lock: pattern cluster state → CoherenceLattice temporal formalization → Sophia temporal audit → Publisher temporal overlays → human/community bounded temporal review
- principles: actionable timeline indicators require docket recommendation; persistence markers remain review-facing hints; temporal conflict markers are cautionary and non-punitive

Build command:

```bash
python3 scripts/build_pattern_temporal_overlay.py
```


## UVLM Research Atlas

### Product Vision (Engineering + Research Brief)

#### Mission

The UVLM Research Atlas transforms the Ultra Verba Lux Mentis corpus from a static archive of papers into a living, navigable map of ideas.

Instead of browsing isolated documents, readers explore a cosmic topology of knowledge where:

- Concepts are stars
- Publications orbit them as planets
- Authors form constellations
- Keywords appear as nebulae
- Series define solar systems

The Atlas allows scholars to explore how ideas emerge, connect, and evolve through time.

#### Core Product Idea

The Atlas is both:

1. **A Research Navigation System**

   Users can visually explore relationships between:

   - concepts
   - papers
   - authors
   - keywords
   - research series

2. **A Theory Development Visualizer**

   Temporal playback shows how a research program evolves as new publications appear and concept clusters grow.

#### Design Philosophy

The Atlas follows five principles:

1. **Deterministic Truth**

   All nodes and relationships originate from declared metadata. No speculative inference.

2. **Multi-Scale Exploration**

   Users can move smoothly between three levels of abstraction:

   - Galaxy View
   - Concept Solar System
   - Paper Orbit

3. **Temporal Awareness**

   The corpus grows through time, revealing the development of ideas.

4. **Scientific Legibility**

   The interface should look beautiful, but every visual structure must reflect real graph structure.

5. **Machine-Readable Scholarship**

   The same data powering the visualization should support automated research tools.

#### Core Data Model

The Atlas is powered by structured artifacts produced by the publishing pipeline:

```text
metadata.yaml (per publication)
       ↓
knowledge_graph.json
       ↓
atlas_timeline.json
       ↓
Atlas UI
```

**Node types**

- concept
- publication
- author
- keyword
- series

**Edge types**

- mentionsConcept
- authoredBy
- taggedWith
- publishedIn
- cites / references
- contains (concept hierarchy)

#### Interface Overview

##### Galaxy View

Shows the full conceptual landscape.

- concepts = bright stars
- concept hierarchy = constellations
- publications hidden until zoom

**Purpose:** Reveal the structure of the research domain.

##### Concept Solar System

Zooming toward a concept reveals its system.

```text
concept (star)
      ↓
publications orbiting
```

**Purpose:** Understand which works build a concept cluster.

##### Paper Orbit View

Zooming further reveals detailed scholarly context.

```text
publication
    ↓
authors
keywords
series
```

**Purpose:** Explore metadata and connections for a specific work.

##### Temporal Evolution Mode

Temporal mode replays the corpus growth.

Users can:

- press play
- scrub through time
- watch concept stars brighten
- see new publications emerge

Concept intensity reflects accumulated research:

```text
brightness(concept) ∝ log(number of connected publications)
```

The Atlas becomes a time-lapse of intellectual development.

#### Reader Experience

A scholar opening the Atlas might:

1. Explore the galaxy of concepts.
2. Zoom into “coherence lattice”.
3. See all orbiting publications.
4. Click a paper to view its metadata and DOI.
5. Press play to watch the theory emerge chronologically.

The interface makes the research program legible as a structure.

#### What Makes This Distinctive

Most scholarly sites provide a paper list.

The Atlas provides an idea ecosystem.

Instead of asking “What papers exist?”, users can ask:

- What concepts organize this research?
- How do ideas relate?
- Which papers formed the core of the theory?
- When did each concept emerge?

This is closer to how knowledge actually develops.

#### Sweet Sauce Enhancements

The Atlas becomes extraordinary when these elements are layered in:

##### Rich Node Objects

Every publication node should include:

- title
- abstract
- DOI
- authors
- concepts
- keywords
- series
- link to publication page

Graph and page must show the same object.

##### Concept Ontology

Concept nodes can relate to each other through declared relationships:

- contains
- dependsOn
- refines
- extends
- contrastsWith

This turns the Atlas into a map of theory, not just a tag network.

##### Guided Research Paths

Add curated pathways such as:

- Start here
- Coherence Lattice lineage
- Narrative Systems cluster

These help readers orient themselves inside the corpus.

##### Page ↔ Atlas Integration

Publication pages should include “View this work in the Research Atlas”, and Atlas nodes should link back to the publication.

This creates a two-way knowledge interface.

#### Technical Architecture

The Atlas runs entirely from generated artifacts:

- `registry/catalog.json`
- `registry/knowledge_graph.json`
- `registry/atlas_timeline.json`

The frontend consumes these artifacts and renders:

- Cytoscape graph
- zoom architecture
- timeline playback
- metadata panels

Because the artifacts are deterministic, the Atlas is reproducible and auditable.

#### Long-Term Potential

As the UVLM corpus grows, the Atlas becomes:

- a research navigation interface
- a theory development map
- a machine-readable knowledge graph
- a visualization of intellectual coherence

It can eventually support:

- concept lineage tracing
- automated bibliography discovery
- AI-assisted corpus exploration
- interactive research pedagogy

#### One-Sentence Vision

The UVLM Research Atlas is a living star map of ideas, where the structure and evolution of a research program can be explored visually, chronologically, and conceptually.


## Research Constellations (Derived Layer)

The Atlas now includes a deterministic **research constellations** layer generated into `registry/constellations.json`.

### What constellations are

A constellation is a derived, explainable cluster of publications + concepts (with contextual authors/series) computed from declared graph topology.

### Deterministic graph vs derived constellation layer

- **Deterministic core graph (`registry/knowledge_graph.json`)**: direct representation of declared metadata only.
- **Derived constellation layer (`registry/constellations.json`)**: computed analysis view built on top of the deterministic graph.

Constellations do **not** mutate `knowledge_graph.json`; they remain a separate artifact for exploration and pedagogy.

### Computation method (v1)

`python3 scripts/build_constellations.py` uses deterministic topology clustering:

1. Build a projection over publication + concept nodes.
2. Connect nodes using declared structural edges (`mentionsConcept`, concept relations, publication reference/citation relations).
3. Compute deterministic connected components in fixed sorted order.
4. Expand each component with weak context (authors/series) for interpretability.
5. Emit stable IDs, stable sorted members, stats, and machine-readable explanations.

No embeddings, no inferred free-text semantics, and no non-declared edges are introduced.

### Validation and auditability

- `schemas/constellations_schema.json` defines the artifact contract for `registry/constellations.json`.
- `scripts/validate_constellations.py` validates structure, references to graph node/edge IDs, duplicates, ordering, and stats consistency.
- CI builds and validates `registry/constellations.json` alongside catalog/graph/timeline artifacts.

## CI Safety Policy

The workflow at `.github/workflows/mint_doi.yml` runs on `papers/**` changes:

- **Pull requests**: validates metadata, generates/validates XML, performs **dry-run only** deposit, and builds/validates catalog + graph artifacts.
- **Pushes to `main`**: performs minting deposit, updates registries/catalog/graph, commits audit artifacts.

This prevents accidental DOI minting before merge while keeping public metadata artifacts fresh.

## Collaborative Review Workflow & Deliberation Trace Overlay (Phase AC)

Publisher surfaces only **Sophia-audited collaborative-review materials**; no automatic consensus ratification or dissent suppression occurs from this layer.

- script: `scripts/build_collaborative_review_overlay.py`
- inputs: `bridge/collaborative_review_audit.json`, `bridge/collaborative_review_recommendations.json`, `bridge/reviewer_deliberation_map.json`, `bridge/reviewer_position_map.json`, `bridge/consensus_state_report.json`, `bridge/dissent_trace_report.json`, `registry/review_packet_dashboard.json`, `registry/causal_dashboard.json`, `registry/authority_gate_dashboard.json`
- outputs: `registry/collaborative_review_dashboard.json`, `registry/consensus_registry.json`, `registry/dissent_watchlist.json`, `registry/deliberation_annotations.json`
- policy: docket items are actionable collaborative entries, watch items are bounded dissent tracking, suppressed items are excluded from actionable overlays.

```bash
python3 scripts/build_collaborative_review_overlay.py
python3 -m unittest tests/test_build_collaborative_review_overlay.py
```

## Telemetry Field Unification & Total Action Functional Overlay (Phase AD)

Publisher surfaces only **Sophia-audited telemetry-field and TAF materials**; no automatic branch activation or canonical mutation occurs from this layer.

- script: `scripts/build_telemetry_field_overlay.py`
- inputs: `bridge/telemetry_field_audit.json`, `bridge/telemetry_field_recommendations.json`, `bridge/telemetry_field_map.json`, `bridge/lattice_projection_map.json`, `bridge/pattern_donation_registry.json`, `bridge/action_functional_scorecard.json`, `bridge/branch_emergence_report.json`, `registry/symbolic_field_registry.json`, `registry/investigation_dashboard.json`, `registry/authority_gate_dashboard.json`
- outputs: `registry/telemetry_dashboard.json`, `registry/lattice_projection_registry.json`, `registry/pattern_donation_watchlist.json`, `registry/action_functional_annotations.json`
- policy: docket items are actionable telemetry/branch overlays, watch items remain bounded in pattern-donation watchlist, suppressed items are excluded from actionable overlays.

```bash
python3 scripts/build_telemetry_field_overlay.py
python3 -m unittest tests/test_build_telemetry_field_overlay.py
```

## Branch Lifecycle Overlay

Publisher surfaces only **Sophia-audited branch lifecycle materials**; no automatic branch activation or canonical mutation occurs from this layer.

- script: `scripts/build_branch_lifecycle_overlay.py`
- outputs: `registry/branch_dashboard.json`, `registry/branch_registry.json`, `registry/branch_watchlist.json`, `registry/branch_annotations.json`

```bash
python3 scripts/build_branch_lifecycle_overlay.py
python3 -m unittest tests/test_build_branch_lifecycle_overlay.py
```

## Prediction Overlay (Phase AF)

Publisher surfaces only **Sophia-audited prediction materials**; no automatic branch activation or canonical mutation occurs from this layer.

- script: `scripts/build_prediction_overlay.py`
- outputs: `registry/prediction_dashboard.json`, `registry/forecast_registry.json`, `registry/prediction_watchlist.json`, `registry/calibration_annotations.json`

```bash
python3 scripts/build_prediction_overlay.py
python3 -m unittest tests/test_build_prediction_overlay.py
```

## Experimental Design, Falsification, and Replication Overlay (Phase AG)

Publisher surfaces only **Sophia-audited experimental materials**; no automatic theory promotion or canonical mutation occurs from this layer.

- script: `scripts/build_experimental_overlay.py`
- inputs: `bridge/experimental_audit.json`, `bridge/experimental_recommendations.json`, `bridge/experimental_hypothesis_map.json`, `bridge/falsification_design_report.json`, `bridge/replication_pathway_map.json`, `bridge/theory_promotion_gate.json`, `registry/prediction_dashboard.json`, `registry/branch_dashboard.json`, `registry/authority_gate_dashboard.json`
- outputs: `registry/experiment_dashboard.json`, `registry/hypothesis_registry.json`, `registry/falsification_watchlist.json`, `registry/theory_gate_annotations.json`

```bash
python3 scripts/build_experimental_overlay.py
python3 -m unittest tests/test_build_experimental_overlay.py
```

## Theory Corpus, Negative Results, and Revision Lineage Overlay (Phase AH)

Publisher surfaces only **Sophia-audited theory corpus materials**; no automatic theory certification or canonical mutation occurs from this layer.

- script: `scripts/build_theory_corpus_overlay.py`
- inputs: `bridge/theory_corpus_audit.json`, `bridge/theory_corpus_recommendations.json`, `bridge/theory_corpus_map.json`, `bridge/theory_revision_lineage.json`, `bridge/negative_result_registry.json`, `bridge/theory_competition_report.json`, `registry/experiment_dashboard.json`, `registry/prediction_dashboard.json`, `registry/branch_dashboard.json`
- outputs: `registry/theory_dashboard.json`, `registry/theory_registry.json`, `registry/negative_result_watchlist.json`, `registry/theory_annotations.json`

```bash
python3 scripts/build_theory_corpus_overlay.py
python3 -m unittest tests/test_build_theory_corpus_overlay.py
```

## Agency-Mode Comparator and Governance Switching Overlay (Phase AI)

Publisher surfaces only **Sophia-audited agency-mode materials**; no automatic metaphysical classification or governance mutation occurs from this layer.

- script: `scripts/build_agency_mode_overlay.py`
- inputs: `bridge/agency_mode_audit.json`, `bridge/agency_mode_recommendations.json`, `bridge/agency_mode_hypothesis_map.json`, `bridge/agency_fit_comparison_report.json`, `bridge/tel_branch_signature_map.json`, `bridge/agency_governance_mode_gate.json`, `registry/theory_dashboard.json`, `registry/prediction_dashboard.json`, `registry/experiment_dashboard.json`
- outputs: `registry/agency_mode_dashboard.json`, `registry/agency_fit_registry.json`, `registry/agency_disagreement_watchlist.json`, `registry/agency_governance_annotations.json`

```bash
python3 scripts/build_agency_mode_overlay.py
python3 -m unittest tests/test_build_agency_mode_overlay.py
```

## Responsibility, Support, and Intervention Boundary Overlay (Phase AJ)

Publisher surfaces only **Sophia-audited responsibility/support materials**; no automatic sanctioning, coercion, or moral classification occurs from this layer.

- script: `scripts/build_responsibility_overlay.py`
- inputs: `bridge/responsibility_audit.json`, `bridge/responsibility_recommendations.json`, `bridge/responsibility_mode_map.json`, `bridge/support_pathway_map.json`, `bridge/intervention_boundary_report.json`, `bridge/sanction_suppression_gate.json`, `registry/agency_mode_dashboard.json`, `registry/theory_dashboard.json`, `registry/experiment_dashboard.json`
- outputs: `registry/responsibility_dashboard.json`, `registry/support_registry.json`, `registry/intervention_watchlist.json`, `registry/responsibility_annotations.json`

```bash
python3 scripts/build_responsibility_overlay.py
python3 -m unittest tests/test_build_responsibility_overlay.py
```

## Cross-Domain Theory Transfer & Donation Governance Overlay (Phase AK)

Publisher surfaces only **Sophia-audited theory-transfer materials**; no automatic cross-domain theory certification or canonical mutation occurs from this layer.

- script: `scripts/build_theory_transfer_overlay.py`
- inputs: `bridge/theory_transfer_audit.json`, `bridge/theory_transfer_recommendations.json`, `bridge/theory_transfer_map.json`, `bridge/donor_target_asymmetry_report.json`, `bridge/transfer_replication_gate.json`, `bridge/transfer_risk_register.json`, `registry/theory_dashboard.json`, `registry/experiment_dashboard.json`, `registry/agency_mode_dashboard.json`
- outputs: `registry/transfer_dashboard.json`, `registry/theory_transfer_registry.json`, `registry/transfer_watchlist.json`, `registry/transfer_annotations.json`

```bash
python3 scripts/build_theory_transfer_overlay.py
python3 -m unittest tests/test_build_theory_transfer_overlay.py
```

## System Forecast Overlay (Phase AL)

Publisher surfaces only **Sophia-audited system forecast materials**; no automatic cross-domain theory certification or canonical mutation occurs from this layer.

Forecasts may guide attention, but never justify pre-emptive coercion.

- script: `scripts/build_system_forecast_overlay.py`
- outputs: `registry/system_forecast_dashboard.json`, `registry/regime_transition_registry.json`, `registry/trajectory_watchlist.json`, `registry/system_forecast_annotations.json`

```bash
python3 scripts/build_system_forecast_overlay.py
python3 -m unittest tests/test_build_system_forecast_overlay.py
```

## Information Value Overlay (Phase AM)

Publisher surfaces only **Sophia-audited information-value materials**; no automatic surveillance expansion or canonical mutation occurs from this layer.

Information-seeking may prioritize attention, but never justify surveillance expansion without explicit human authorization.
Curiosity must guide investigation, not intrusion.

- script: `scripts/build_information_value_overlay.py`
- outputs: `registry/uncertainty_dashboard.json`, `registry/observation_priority_registry.json`, `registry/curiosity_watchlist.json`, `registry/curiosity_annotations.json`

```bash
python3 scripts/build_information_value_overlay.py
python3 -m unittest tests/test_build_information_value_overlay.py
```



## Value Alignment Overlay (Phase AN)

Publisher surfaces only **Sophia-audited value-alignment materials**; no automatic moral execution or canonical mutation occurs from this layer.

The system may recommend knowledge priorities, but human communities must retain authority over final value judgments.
The triad should illuminate moral consequences, not replace human ethics.

- script: `scripts/build_value_alignment_overlay.py`
- outputs: `registry/value_dashboard.json`, `registry/knowledge_priority_registry.json`, `registry/value_risk_watchlist.json`, `registry/value_annotations.json`

```bash
python3 scripts/build_value_alignment_overlay.py
python3 -m unittest tests/test_build_value_alignment_overlay.py
```

When Phase AN is complete, the architecture supports the full civilizational cognition cycle:

`telemetry → lattice projection → pattern discovery → hypothesis generation → prediction → experiment design → theory memory → agency governance → responsibility boundaries → cross-domain transfer governance → trajectory forecasting → curiosity-driven inquiry → value-aligned discovery priorities`


## Meta-Cognition Overlay (Phase AO)

Publisher surfaces only **Sophia-audited meta-cognition materials**; no autonomous safety-constraint mutation or canonical mutation occurs from this layer.

The system may evaluate its architecture but cannot autonomously modify core safety constraints.
Meta-cognition may propose improvements, but humans must approve structural changes.

Immutable without human approval:

- evidence maturity gating
- provenance requirements
- sanction suppression rules
- agency humility protocol
- non-coercion forecasting rule
- human authority over value judgments

- script: `scripts/build_meta_cognition_overlay.py`
- outputs: `registry/meta_dashboard.json`, `registry/reasoning_performance_registry.json`, `registry/meta_watchlist.json`, `registry/meta_annotations.json`

```bash
python3 scripts/build_meta_cognition_overlay.py
python3 -m unittest tests/test_build_meta_cognition_overlay.py
```

## Architecture Overlay (Phase AP)

Publisher surfaces only **Sophia-audited architecture materials**; architecture evaluations may inform review, but cannot mutate core safeguards or canonical state without explicit human approval.

- script: `scripts/build_architecture_overlay.py`
- outputs: `registry/architecture_dashboard.json`, `registry/module_performance_registry.json`, `registry/architecture_watchlist.json`, `registry/architecture_annotations.json`

```bash
python3 scripts/build_architecture_overlay.py
python3 -m unittest tests/test_build_architecture_overlay.py
```

## Social Entropy & Civic Cohesion Overlay (Phase AQ)

Publisher surfaces only **Sophia-audited social-entropy materials**; no automatic suppression, ranking of persons, or coercive normalization occurs from this layer.

- script: `scripts/build_social_entropy_overlay.py`
- outputs: `registry/social_entropy_dashboard.json`, `registry/civic_cohesion_registry.json`, `registry/legitimacy_watchlist.json`, `registry/social_repair_annotations.json`

```bash
python3 scripts/build_social_entropy_overlay.py
python3 -m unittest tests/test_build_social_entropy_overlay.py
```

Codex context note: this interface should help humans see where the commons is fraying without turning the system into a civics panopticon.

## Federated Stewardship & Commons Governance Overlay (Phase AR)

Publisher surfaces only **Sophia-audited federated-governance materials**; no automatic centralization, ranking of communities, or sovereignty claims occur from this layer.

- script: `scripts/build_federated_governance_overlay.py`
- outputs: `registry/federation_dashboard.json`, `registry/stewardship_registry.json`, `registry/capture_watchlist.json`, `registry/federation_annotations.json`

```bash
python3 scripts/build_federated_governance_overlay.py
python3 -m unittest tests/test_build_federated_governance_overlay.py
```

Codex context note: this interface should help humans see where the commons is centralizing or fracturing, not create a new prestige hierarchy.

## Emergent Domain Detection & Field Birth Overlay (Phase AT)

Publisher surfaces only **Sophia-audited emergent-domain materials; no automatic canon formation, ranking of disciplines, or field sovereignty claims occur from this layer.**

The interface should show the birth of a field as a pattern of convergence, not a proclamation.

- script: `scripts/build_emergent_domain_overlay.py`
- inputs: `bridge/emergent_domain_audit.json`, `bridge/emergent_domain_recommendations.json`, `bridge/emergent_domain_map.json`, `bridge/cross_domain_invariant_report.json`, `bridge/field_birth_pressure_report.json`, `bridge/domain_boundary_failure_map.json`, `registry/transfer_dashboard.json`, `registry/value_dashboard.json`, `registry/uncertainty_dashboard.json`, `registry/social_entropy_dashboard.json`, `registry/civic_literacy_dashboard.json`
- outputs: `registry/emergent_domain_dashboard.json`, `registry/domain_birth_registry.json`, `registry/domain_boundary_watchlist.json`, `registry/emergent_domain_annotations.json`
- policy: docket items are actionable emergent-domain entries, watch items are bounded domain-boundary tracking, suppressed items are excluded from actionable overlays.
- canonical integrity helper: `scripts/canonical_integrity_manifest.py` evaluates bridge/registry manifest metadata and degrades trust presentation when manifests are missing, diverged, or have invalid constraint signatures.

```bash
python3 scripts/build_emergent_domain_overlay.py
python3 -m unittest tests/test_build_emergent_domain_overlay.py
```

Canonical trust rule: derivatives that remove provenance or alter safety boundaries without disclosure lose canonical trust status.

### Phase-lock integration rule (Phase AT)

`transfer / theory / prediction / curiosity / value / commons context -> CoherenceLattice emergent-domain formalization -> Sophia emergent-domain audit -> Publisher field-birth overlays -> human/community/scientific ratification pathways`


## Canonical Integrity & Derivative Trust

Bridge/registry artifacts may include canonical integrity manifests with constraint signatures.
If immutable safety constraints change, the constraint signature must change accordingly.
Derivatives that remove provenance or alter safety boundaries without disclosure lose canonical trust status and should be presented with degraded trust markers.

## Civilizational Commons Safeguard Overlay (Phase AU)

Publisher surfaces only **Sophia-audited commons sovereignty signals; it does not determine governance authority**.

The UI should show the health of the commons, not elevate any institution above it.

- script: `scripts/build_commons_sovereignty_overlay.py`
- inputs: `bridge/commons_sovereignty_audit.json`, `bridge/commons_sovereignty_recommendations.json`, `bridge/commons_sovereignty_map.json`, `bridge/institutional_capture_risk_report.json`, `bridge/public_trust_signal_map.json`, `bridge/civilizational_integrity_report.json`, `registry/federation_dashboard.json`, `registry/social_entropy_dashboard.json`, `registry/value_dashboard.json`, `registry/architecture_dashboard.json`
- outputs: `registry/commons_sovereignty_dashboard.json`, `registry/institutional_capture_registry.json`, `registry/public_trust_watchlist.json`, `registry/civilizational_integrity_annotations.json`
- policy: docket items enter actionable dashboard/registry sections, watch items enter public trust watchlist, and suppressed items are excluded from actionable overlays.

```bash
python3 scripts/build_commons_sovereignty_overlay.py
python3 -m unittest tests/test_build_commons_sovereignty_overlay.py
```

## Civilizational Memory & Knowledge Stewardship Overlay (Phase AV)

Publisher surfaces only **Sophia-audited civilizational memory materials; it does not determine canon, rank traditions, or erase failed branches**.

The interface should make preservation feel participatory and legible, never priestly or opaque.

- script: `scripts/build_civilizational_memory_overlay.py`
- inputs: `bridge/civilizational_memory_audit.json`, `bridge/civilizational_memory_recommendations.json`, `bridge/civilizational_memory_map.json`, `bridge/intergenerational_legibility_report.json`, `bridge/epistemic_resilience_scorecard.json`, `bridge/memory_fragility_report.json`, `registry/theory_dashboard.json`, `registry/commons_sovereignty_dashboard.json`, `registry/civic_literacy_dashboard.json`, `registry/knowledge_priority_registry.json`
- outputs: `registry/civilizational_memory_dashboard.json`, `registry/epistemic_resilience_registry.json`, `registry/memory_fragility_watchlist.json`, `registry/civilizational_memory_annotations.json`
- policy: docket items are actionable memory/stewardship entries, watch items are bounded fragility tracking, suppressed items are excluded from actionable overlays.

```bash
python3 scripts/build_civilizational_memory_overlay.py
python3 -m unittest tests/test_build_civilizational_memory_overlay.py
```

## Operationalization Boundary & Deployment Maturity Overlay (Phase AX)

Publisher surfaces only **Sophia-audited operationalization materials; it does not authorize deployment, implementation, or institutional control.**

Readiness is shown as bounded possibility, not a green light: the interface communicates stewardship thresholds and translation risk, never deployment triumph.

- script: `scripts/build_operationalization_overlay.py`
- inputs: `bridge/operationalization_audit.json`, `bridge/operationalization_recommendations.json`, `bridge/operational_maturity_map.json`, `bridge/deployment_boundary_report.json`, `bridge/translation_risk_register.json`, `bridge/operationalization_gate.json`, `registry/knowledge_topology_dashboard.json`, `registry/emergent_domain_dashboard.json`, `registry/civilizational_memory_dashboard.json`, `registry/commons_sovereignty_dashboard.json`, `registry/value_dashboard.json`
- outputs: `registry/operational_maturity_dashboard.json`, `registry/deployment_boundary_registry.json`, `registry/translation_risk_watchlist.json`, `registry/operationalization_annotations.json`
- policy: `docket` routes to actionable operational maturity/deployment-boundary outputs, `watch` routes to translation-risk watchlist, and `suppressed` is excluded from actionable overlays.
- safeguards: no deployment execution, no policy enactment, no governance-right mutation, no canon closure, no ranking of persons/communities/institutions, and no claim that scientific maturity alone licenses operational control.

```bash
python3 scripts/build_operationalization_overlay.py
python3 -m unittest tests/test_build_operationalization_overlay.py
```

Phase lock: attractor / basin / dead-zone / memory / sovereignty / value context -> CoherenceLattice operational maturity and deployment-boundary formalization -> Sophia bounded operationalization audit -> Publisher deployment-maturity overlays -> human/community/scientific/institutional deliberation.

## Discovery Navigation Engine Overlay (Phase BA)

Publisher surfaces only **Sophia-audited discovery-navigation materials; it does not authorize autonomous pursuit, deployment, canonization, or institutional control.**

Render discovery as bounded terrain and navigable corridors, not as an oracle path.

- script: `scripts/build_discovery_navigation_overlay.py`
- inputs: `bridge/discovery_navigation_audit.json`, `bridge/discovery_navigation_recommendations.json`, `bridge/discovery_vector_field.json`, `bridge/cross_domain_bridge_map.json`, `bridge/entropy_reduction_corridor.json`, `bridge/discovery_navigation_report.json`, `registry/knowledge_topology_dashboard.json`, `registry/operational_maturity_dashboard.json`, `registry/civilizational_memory_dashboard.json`, `registry/commons_sovereignty_dashboard.json`, `registry/value_dashboard.json`
- outputs: `registry/discovery_navigation_dashboard.json`, `registry/discovery_corridor_registry.json`, `registry/discovery_risk_watchlist.json`, `registry/discovery_annotations.json`
- policy: `docket` routes to actionable dashboard/corridor outputs, `watch` routes to discovery risk watchlist, and `suppressed` is excluded from actionable overlays.
- safeguards: no autonomous research execution, no deployment execution, no governance-right mutation, no canon closure, no ranking of communities/institutions, and no implication that corridor priority equals truth authority.

```bash
python3 scripts/build_discovery_navigation_overlay.py
python3 -m unittest tests/test_build_discovery_navigation_overlay.py
```

Phase lock: attractor / basin / dead-zone / operational-boundary / value / commons context -> CoherenceLattice discovery-vector and corridor formalization -> Sophia bounded discovery-navigation audit -> Publisher corridor overlays -> human/community/scientific deliberation and bounded exploration.
