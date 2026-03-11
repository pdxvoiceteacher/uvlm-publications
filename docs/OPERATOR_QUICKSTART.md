# Operator Quickstart

## Where to start
1. Open high-level posture dashboards first:
   - `registry/background_coherence_dashboard.json`
   - `registry/living_terrace_dashboard.json`
   - `registry/phase_lineage_dashboard.json`
2. Check trust posture:
   - verify `canonicalIntegrityVerified`
   - if `trustPresentationDegraded` is `true`, treat outputs as bounded legibility aids.

## Move from raw artifacts to summaries
1. Raw bridge artifacts are source-facing and often dense (`bridge/*.json`).
2. Run overlay builders to produce operator summaries in `registry/*.json`.
3. Prefer entries in dashboard/registry artifacts for action context; use annotations for rationale and safeguards.

## Use lineage/glossary overlays
- `registry/phase_lineage_dashboard.json` gives phase-lineage visibility and operator/queryability indicators.
- `registry/operator_glossary_registry.json` mirrors actionable, docket-routed glossary-linked entries.
- `registry/legibility_annotations.json` preserves explanatory notes (including suppressed-note context) without elevating authority.

## Interpret routing in legibility artifacts
- `docket`: actionable, appears in lineage dashboard + glossary registry.
- `watch`: appears in `registry/governance_breadcrumb_watchlist.json`; monitor and collect more bounded evidence.
- `suppressed`: excluded from actionable overlays, but explanatory notes may still appear in annotations for stewardship continuity.

## Practical operator loop
1. Start with dashboard entries.
2. Cross-check watchlist for drift or governance breadcrumb concerns.
3. Read annotations for constraints and suppressed explanatory notes.
4. Escalate only bounded, provenance-backed items to executive review channels.
