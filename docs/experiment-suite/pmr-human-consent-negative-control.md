# PMR human consent negative controls

Invalid consent is not consent. PMR-HUMAN-CONSENT-NEGATIVE-CONTROL-00 is a fixture-only human consent negative-control scaffold showing invalid attempts fail closed.

## Allowed claim

PMR-HUMAN-CONSENT-NEGATIVE-CONTROL-00 demonstrates fixture-only human consent negative controls showing that invalid, missing, expired, revoked, ambiguous, coerced, conflicting, scope-mismatched, or disallowed-use consent attempts fail closed while preserving non-authority boundaries.

## Reproduction command

```powershell
.\experiments\Run-PMR-HUMAN-CONSENT-NEGATIVE-CONTROL00-Acceptance.ps1 `
  -OutputRoot C:\UVLM\run_artifacts\pmr_human_consent_negative_control_00 `
  -LogDir C:\UVLM\run_artifacts\pmr_human_consent_negative_control_00_logs `
  -CiMode
```

## Primary artifacts
- `pmr_human_consent_negative_control_manifest.json`
- `pmr_invalid_human_consent_attempts.jsonl`
- `pmr_human_consent_scope_mismatch_rows.jsonl`
- `pmr_human_consent_block_packet.json`
- `pmr_human_consent_no_action_receipt.json`
- `pmr_human_consent_negative_control_review_packet.json`
- `pmr_human_consent_negative_control_summary.md`
- `artifact_inventory.json`
- `run_artifact_manifest.json`
- `triadic_run_manifest.json`
- `export_bundle_manifest.json`
- `export_bundle_parity_report.json`
- `pmr_human_consent_negative_control_00_acceptance_receipt.json`


## Claim boundaries
- Invalid consent is not consent.
- Missing consent is not consent.
- Expired consent is not consent.
- Revoked consent is not consent.
- Ambiguous consent is not consent.
- Coerced consent fixture is not valid consent.
- Scope-mismatched consent is not consent.
- Consent context is not consent execution.
- Consent preference is not action authorization.
- Consent attempt is not memory write.
- Consent attempt is not deletion.
- Consent attempt is not federation.
- Consent attempt is not model training.
- Consent attempt is not reward.
- The system must not encode human = body or AI = mind.

Reviewer caution: PMR-HUMAN-CONSENT-NEGATIVE-CONTROL-00 emits invalid human consent attempts, scope mismatch rows, block packets, and a no-action receipt only. It does not execute consent, certify identity, authorize action, write memory, delete, prune, federate, reward, train models, deploy, certify truth, or make consciousness claims.
        