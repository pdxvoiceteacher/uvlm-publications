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
