# Atlas Persistence Policy

## Purpose
Atlas should not ingest every novelty artifact automatically.
Instead, candidate artifacts are compared against existing Atlas candidates to estimate true novelty.

## Candidate lifecycle
1. CoherenceLattice emits `atlas_novelty_candidate.json`
2. Candidate is compared against stored Atlas candidates
3. `atlas_persistence_recommendation` is computed:
   - `store`
   - `hold`
4. Persistence result is emitted as `atlas_persistence_result.json`

## Current heuristic
- novelty vs existing candidates is estimated by token-level similarity
- low similarity → store
- high similarity → hold for review

## Future upgrades
- semantic similarity
- lineage-aware clustering
- phaselock validation before canonization
