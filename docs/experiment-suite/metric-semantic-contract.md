# Metric Semantic Contract

## What was validated

MET-SEM-00 publishes a metric semantic contract for LOCAL-REVIEW-RUNTIME-V0. The schema is `coherencelattice.metric_semantic_reconciliation_packet.v1`, and the reconciliation status is `active_profile_proxy_reconciliation`.

The original meanings remain canonical semantic targets. The canonical theory is not fully implemented by LOCAL-REVIEW-RUNTIME-V0. Current code implements profile-specific operational proxies. Current values are local-review operational proxies. Population calibration is required before stronger claims.

## Dashboard summary

- source_phase = MET-SEM-00
- runtime_profile = LOCAL-REVIEW-RUNTIME-V0
- reconciliation_status = active_profile_proxy_reconciliation
- canonical_theory_status = semantic_target_not_fully_implemented
- runtime_profile_semantics = local_review_operational_proxies
- canonical_meanings_preserved_as_targets = true
- current_values_are_profile_specific_proxies = true
- population_calibration_required_for_full_claims = true
- truth_certification_emitted = false
- product_release_performed = false
- runtime_authority_granted = false

## User-facing aliases

- E_review
- T_review
- Ψ_review
- ΔS_review
- Λ_boundary
- Eₛ_review
- TAF_review_runtime_v0

## Canonical symbols not fully measured

- E
- Ψ
- ΔS
- Λ
- Eₛ
- TAF

## Metric semantic rows

| Symbol | Canonical target | Runtime alias | Safe label | Unsafe label | Semantic coverage | Requires population calibration |
| --- | --- | --- | --- | --- | --- | --- |
| E | coherent coupling / empathy / signal energy | E_review | Reviewer-care affordance proxy | Unsafe label: Empathy score | partial | true |
| T | canonical target preserved | T_review | Review inspectability proxy | Unsafe label: Complete transparency score | profile_proxy | true |
| Ψ | canonical target preserved | Ψ_review | Local review coherence proxy | Unsafe label: Universal coherence score | profile_proxy | true |
| ΔS | canonical target preserved | ΔS_review | Review instability proxy | Unsafe label: Entropy score | profile_proxy | true |
| Λ | canonical target preserved | Λ_boundary | Governance boundary pressure proxy | Unsafe label: Phase-lock score | profile_proxy | true |
| Eₛ | canonical target preserved | Eₛ_review | Non-authority and review-equity visibility proxy | Unsafe label: Ethical symmetry score | profile_proxy | true |
| TAF | canonical target preserved | TAF_review_runtime_v0 | Governed review action-burden proxy | Unsafe label: Canonical total action | profile_proxy | true |

Formula and decomposition notes:

- Ψ_review proxy formula: E_review × T_review.
- Λ split terms: Λ_phase = not_applicable_for_local_review_v0; Λ_critical = future_candidate; Λ_boundary = implemented.
- TAF_review_runtime_v0 decomposition terms: physical_action_proxy, informational_action_proxy, coherence_agentic_action_proxy.

## Required boundary language

- The original meanings remain canonical semantic targets.
- Current code implements profile-specific operational proxies.
- Current values are local-review operational proxies.
- canonical_theory_status = semantic_target_not_fully_implemented
- runtime_profile_semantics = local_review_operational_proxies
- The canonical theory is not fully implemented by LOCAL-REVIEW-RUNTIME-V0.
- E_review is a reviewer-care affordance proxy, not full empathy.
- T_review is a review inspectability proxy.
- Ψ_review preserves Ψ = E × T only within local-review proxy scope.
- ΔS_review is a review instability proxy, not full entropy.
- Λ_boundary is governance boundary pressure, not full phase-lock.
- Eₛ_review is a non-authority/review-equity visibility proxy, not full ethical symmetry.
- TAF_review_runtime_v0 is a governed review action-burden proxy, not canonical TAF.
- Population calibration is required before stronger claims.
- Metrics are not truth certification.
- Metrics are not theorem proof.
- Metrics are not moral proof.
- Metrics are not human benefit proof.
- Metrics are not product release.
- Metrics are not psychological measures.
- Metrics are not moral worth scores.

## Unsafe labels retained only as blocked language

- Unsafe label: Empathy score
- Unsafe label: Complete transparency score
- Unsafe label: Universal coherence score
- Unsafe label: Entropy score
- Unsafe label: Phase-lock score
- Unsafe label: Ethical symmetry score
- Unsafe label: Canonical total action

These unsafe labels are present for language-governance review only; they are not publication claims.

## Blocked metric overclaim examples

- E_review measures full empathy
- E_review is psychological empathy
- Empathy score is measured without qualification
- T_review is complete transparency
- Ψ_review is universal coherence
- ΔS_review is thermodynamic entropy
- ΔS_review is canonical entropy
- Λ_boundary is phase-lock
- Λ_boundary is full Λ
- Eₛ_review is full ethical symmetry
- Eₛ_review proves fairness
- TAF_review_runtime_v0 is canonical total action
- current metrics are canonical cross-domain measurements
- current metrics are truth certification
- current metrics are theorem proof
- current metrics are human benefit proof
- current metrics are moral worth scores
- current metrics are product release
- current metrics prove consciousness
- current metrics prove Omega detection
- current metrics prove universal ontology
- current metrics authorize final answers
- current metrics authorize accepted evidence
- current metrics authorize Atlas memory admission
- current metrics authorize memory write
- current metrics authorize deployment or provider runtime
- population calibration has already been achieved

## Artifacts

- config/metric_semantics/metric_semantic_contract.v1.json
- metric_semantic_reconciliation_packet.json
- docs/METRIC_SEMANTIC_RECONCILIATION.md

## Reproducibility command

Publication surfaces include `build_runtime_metrics_seed_corpus` and `build_metric_semantic_reconciliation_packet`.

```powershell
python -c "from pathlib import Path; from coherence.local_review.seed_corpus import build_runtime_metrics_seed_corpus; from coherence.local_review.metric_semantics import build_metric_semantic_reconciliation_packet; root=Path(r'C:\UVLM\run_artifacts\runtime_metrics_seed_corpus'); bridge=root / 'bridge'; build_runtime_metrics_seed_corpus(output_root=root); build_metric_semantic_reconciliation_packet(bridge)"
```

## Allowed bounded claim

MET-SEM-00 publishes a metric semantic contract that preserves canonical coherence meanings as semantic targets while labeling current LOCAL-REVIEW-RUNTIME-V0 values as profile-specific operational proxies.

## Telemetry aperture linkage

TELEMETRY-APERTURE-DESIGN-00 uses safe MET-SEM aliases for pulse mode only: Ψ_review, E_review, T_review, ΔS_review, Λ_boundary, Eₛ_review, and TAF_review_runtime_v0. Safe MET-SEM aliases are not canonical metric completion and TAC does not present unqualified empathy score, unqualified transparency score, unqualified phase-lock score, unqualified entropy score, unqualified ethical symmetry score, or canonical total action as TAC measurements.
