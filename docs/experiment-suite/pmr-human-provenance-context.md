# PMR human provenance context

Required phrase: Human provenance context is not identity certification.

The system must not encode human = body or AI = mind. PMR-HUMAN-PROVENANCE-00 is a fixture-only human provenance and consent context scaffold. It models synthetic human participation in provenance, consent scope, correction requests, revocation requests, review receipt candidates, and lived-stakes annotations while preserving strict non-authority boundaries.

## Allowed claim

PMR-HUMAN-PROVENANCE-00 demonstrates a fixture-only human provenance and consent context scaffold for synthetic provenance, consent scope, correction, revocation, review participation, and lived-stakes annotation while preserving non-authority boundaries.

## Reproduction command

```powershell
.\experiments\Run-PMR-HUMAN-PROVENANCE00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_human_provenance_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_human_provenance_00_logs `
  -CiMode
```

## Primary artifacts

- `pmr_human_provenance_manifest.json`
- `pmr_human_provenance_context_packet.json`
- `pmr_human_consent_scope_packet.json`
- `pmr_human_correction_request_packet.json`
- `pmr_human_revocation_request_packet.json`
- `pmr_human_review_receipt_candidates.jsonl`
- `pmr_human_lived_stakes_annotation_packet.json`
- `pmr_human_provenance_review_packet.json`
- `pmr_human_provenance_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `triadic_run_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `pmr_human_provenance_00_acceptance_receipt.json`

## Participant roles

- `source_contributor`
- `reviewer`
- `correction_provider`
- `revocation_requester`
- `consent_scope_owner`
- `affected_stakeholder`

## Consent allowed uses

- `review_only`
- `retention_preference`
- `correction_review`
- `revocation_review`
- `simulation_only`

## Revocation scopes

- `consent_scope`
- `retention_preference`
- `review_visibility`
- `federation_eligibility`
- `training_credit_eligibility`

## Lived-stakes categories

- `privacy`
- `reputational`
- `safety`
- `authorship`
- `consent`
- `resource_burden`

## Dashboard posture

- `review_status = accepted_as_pmr_human_provenance_context_scaffold`
- `human_provenance_id = pmr-human-provenance-00-4354906b4ba13cf0`
- `participant_context_count = 6`
- `consent_scope_count = 5`
- `correction_request_count = 5`
- `revocation_request_count = 5`
- `review_receipt_candidate_count = 5`
- `lived_stakes_annotation_count = 6`
- `source_pmr_fed_stress_bound = true`
- `source_pmr_stat_bound = true`
- `source_pmr_sim_bound = true`
- `source_architecture_checkpoint_bound = true`
- `source_pmr_ladder_bound = true`
- `synthetic_human_context_only = true`
- `human_provenance_context_present = true`
- `consent_scope_packet_present = true`
- `correction_request_packet_present = true`
- `revocation_request_packet_present = true`
- `review_receipt_candidates_present = true`
- `lived_stakes_annotation_present = true`
- `human_provenance_not_identity_certification = true`
- `consent_context_not_consent_execution = true`
- `consent_preference_not_action_authorization = true`
- `correction_request_not_memory_write = true`
- `revocation_request_not_deletion_execution = true`
- `review_participation_not_truth_certification = true`
- `lived_stakes_not_reward_entitlement = true`
- `human_provenance_not_human_value_score = true`
- `no_metaphysical_identity_claim = true`
- `identity_certification_performed = false`
- `consent_execution_performed = false`
- `action_authorization_performed = false`
- `memory_write_performed = false`
- `deletion_performed = false`
- `pruning_performed = false`
- `federation_performed = false`
- `reward_actions_performed = false`
- `token_economy_performed = false`
- `model_weight_training_performed = false`
- `deployment_performed = false`
- `truth_certification_performed = false`
- `export_parity_passed = true`

## Blocked claims

- not identity certification
- not consent execution
- not action authorization
- not memory write authorization
- not deletion execution
- not pruning execution
- not truth certification
- not human value score
- not reward entitlement
- not token economy
- not federation authorization
- not model weight training
- not deployment authority
- not AI consciousness claim
- not human consciousness claim
- not hallucination reduction proof
- not recursive self-improvement

Reviewer caution: PMR-HUMAN-PROVENANCE-00 models synthetic human provenance and consent context only. It does not certify identity, does not execute consent, does not authorize action, does not write memory, does not delete, does not prune, does not federate, does not reward, does not train models, does not deploy, does not certify truth, and does not make AI or human consciousness claims.
