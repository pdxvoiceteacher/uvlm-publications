# Atlas Continuity Handoff
## Date: 2026-04-02

---

## Role of this repo

Atlas is the memory adjudication and storage organ.

It is responsible for:
- comparing novelty candidates against stored priors
- deciding store / hold / merge_or_review
- persisting approved priors
- returning stored prior lists
- later retrieving relevant priors into new runs

Atlas should be the authority on:
- whether something is truly novel relative to memory
- whether/how it should be stored
- later what should be returned into active cognition

Atlas should **not** depend on CoherenceLattice to decide memory worthiness for it.

---

## Verified working in this repo

- `/health`
- `/atlas/adjudicate`
- `/atlas/persist`
- `/atlas/priors`

Current behavior:
- reads `atlas_novelty_candidate.json` from CoherenceLattice bridge
- compares against `atlas_store`
- returns adjudication
- persists when judged novel enough

This is the currently verified working milestone.

---

## Design cautions

### 1. Atlas comparison is currently shallow
Comparison is token-level / lexical and should later become:
- lineage-aware
- source-aware
- more semantic

### 2. Atlas retrieval back into active cognition is not yet active
This is the main next step.

### 3. Atlas should remain agentic
Do not push storage judgment back into CoherenceLattice.

---

## Current next step for this repo

### Atlas Retrieval + Prior Injection
Needed here:
- retrieval API for relevant priors
- `atlas_prior_packet.json` emission
- later:
  - merge suggestions
  - lineage edges
  - source affinity hints

Atlas should become a contributor back into discussion, not only a storage sink.

---

## Presentation protocol for future Echo iterations

For Atlas patches:
- clearly separate adjudication behavior from retrieval behavior
- show exact adjudication JSON
- show exact persistence JSON
- show exact prior retrieval packet shape
- include exact verification commands
