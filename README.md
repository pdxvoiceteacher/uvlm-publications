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
