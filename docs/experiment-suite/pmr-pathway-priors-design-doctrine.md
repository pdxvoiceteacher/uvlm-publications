# PMR Pathway Priors Design Doctrine

## What was validated

PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 synchronizes locally validated PMR pathway-prior design doctrine to publication surfaces. This is publication/dashboard synchronization only and grants no runtime authority. The phase is active design-only doctrine: pathway priors are disabled, no pathway-prior generation is performed, no memory is written, no Atlas memory is admitted, no model is trained, and no review skipping is authorized.

## Dashboard summary

- policy_status = active_design_only
- runtime_behavior_changed = false
- pathway_priors_enabled = false
- pathway_prior_generation_performed = false
- memory_write_performed = false
- atlas_memory_admission_performed = false
- model_training_performed = false
- review_skip_authorized = false
- product_release_performed = false
- pathway_prior_definition = revocable_materiality_scoped_review_recommendation
- pathway_prior_is_not_truth = true
- pathway_prior_is_not_memory_canon = true
- pathway_prior_is_not_model_training = true
- pathway_prior_is_not_review_skip = true
- pathway_prior_is_not_final_answer_authority = true
- pathway_prior_is_not_accepted_evidence_authority = true
- pathway_prior_is_not_product_release = true
- pathway_prior_is_not_trace_export_authorization = true
- pathway_prior_is_not_federation_authorization = true
- pathway_prior_is_not_memory_write = true
- pathway_prior_is_not_atlas_memory_admission = true
- pathway_prior_requires_human_review = true

## Required doctrine language

- Summary is not source.
- Compression is not erasure.
- Preferred route is not authority.
- Route prior is not truth.
- Route prior is not memory canon.
- Route prior is not model training.
- Route prior cannot skip future review.
- PMR pathway priors are revocable, materiality-scoped review recommendations.
- PMR pathway priors are derived only from provenance-backed artifact histories.
- PMR pathway priors preserve replay lineage.
- PMR pathway priors preserve AI Receipt traceability.
- PMR pathway priors must respect TAC retention, trace export, and federation boundaries.
- PMR pathway priors must record Sophia execution reality when applicable.
- PMR pathway priors must record validation-tier evidence when applicable.
- Human review remains required.
- PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 does not generate pathway priors.
- PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 does not write memory.
- PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 does not admit Atlas memory.
- PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 does not train a model.
- PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 does not authorize review skipping.
- PMR-PATHWAY-PRIORS-DESIGN-DOCTRINE-00 does not change runtime behavior.

## Artifacts

- docs/PMR_PATHWAY_PRIORS_DESIGN_DOCTRINE.md
- config/pmr/pathway_prior_policy.v1.json
- schema/bridge/pmr_pathway_prior_policy_packet.schema.json
- schema/bridge/pmr_pathway_prior_candidate.schema.json
- schema/bridge/pmr_pathway_prior_non_authority_boundary.schema.json

## Reproducibility fragments

- PMR_PATHWAY_PRIORS_DESIGN_DOCTRINE.md
- pathway_prior_policy.v1.json
- pmr_pathway_prior_policy_packet.schema.json
- pmr_pathway_prior_candidate.schema.json
- pmr_pathway_prior_non_authority_boundary.schema.json

```powershell
python -c "from pathlib import Path; Path('docs/PMR_PATHWAY_PRIORS_DESIGN_DOCTRINE.md').read_text(encoding='utf-8')"; python -m json.tool config/pmr/pathway_prior_policy.v1.json >/dev/null; python -m json.tool schema/bridge/pmr_pathway_prior_policy_packet.schema.json >/dev/null; python -m json.tool schema/bridge/pmr_pathway_prior_candidate.schema.json >/dev/null; python -m json.tool schema/bridge/pmr_pathway_prior_non_authority_boundary.schema.json >/dev/null
```

## Blocked overclaim examples for PMR pathway-prior design doctrine publication boundaries

- PMR pathway prior is truth
- PMR pathway prior is memory canon
- PMR pathway prior trains the model
- PMR pathway prior skips human review
- PMR pathway prior authorizes final answers
- PMR pathway prior grants accepted-evidence authority
- PMR pathway prior writes memory
- PMR pathway prior admits Atlas memory
- PMR pathway prior authorizes trace export
- PMR pathway prior authorizes PMR federation
- PMR pathway prior is product release
- PMR pathway prior proves human benefit
- PMR pathway prior is market validation
- preferred route means correct route
- compressed route means source can be deleted
- summary route replaces replay lineage
- prior route overrides materiality review
- route prior can ignore TAC boundary
- route prior can ignore Sophia reality
- route prior can ignore validation tier

## Allowed bounded claim

PMR pathway priors are proposed as revocable, materiality-scoped review recommendations derived from provenance-backed artifact histories, preserving replay lineage, AI Receipt traceability, TAC boundaries, Sophia reality status, validation-tier evidence, and human review requirements without certifying truth, writing memory, training models, skipping review, admitting Atlas memory, exporting traces, federating PMR, releasing product, or granting final-answer or accepted-evidence authority.
