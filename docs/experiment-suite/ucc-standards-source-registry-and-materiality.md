# UCC standards source registry and materiality

UCC-STANDARDS-SOURCE-REGISTRY-AND-MATERIALITY-00 provides universal source-profile and materiality-profile scaffolding using a synthetic fixture and NIST reference-only example.

## Dashboard summary

- source_profile_count = 2
- active_design_fixture_ref = local_forensic_controls_fixture_v0
- real_world_reference_example_ref = nist_csf_2_0_reference
- nist_reference_is_marketing_example_only = true
- nist_source_text_stored = false
- nist_materiality_profile_applied = false
- only active source rows are synthetic fixture and NIST reference
- materiality override control = uncertainty_visible
- prior_materiality = medium
- override_materiality = high
- override_is_ad_hoc = true
- override_is_not_certification = true
- override_does_not_modify_source_standard = true

## Artifacts

- `ucc_standards_source_registry.json`
- `ucc_materiality_profile.json`
- `ucc_materiality_override_receipt.json`
- `ucc_standards_source_registry_summary.md`

## Required boundaries

- Synthetic fixture proves universal internal-control design.
- NIST CSF 2.0 is included as a reference-only real-world applicability example.
- NIST control text is not ingested.
- NIST reference is not compliance certification.
- No AICPA, COSO, PRISMA, ISO, SOC, PCAOB, clinical, legal, or academic standards are ingested in this patch.
- Future source profiles may support open-license, licensed, customer-supplied, connector-monitored, and professional-attestation external sources.
- Materiality defaults may be defined by the control/profile/system.
- Users may refine materiality ad hoc with rationale.
- User overrides do not modify the source standard.
- User overrides are not professional judgment.
- User overrides are not certification.
- Human review remains required.

## Reproducibility

```powershell
python -c "from pathlib import Path; from coherence.triadic.llm_metrics_smoke import build_triadic_llm_metrics_smoke; from coherence.ucc.sophia_control_review import build_sophia_ucc_control_review; from coherence.ucc.standards_source_registry import build_ucc_standards_source_registry; from coherence.ucc.materiality_profile import build_ucc_materiality_profile; from coherence.ucc.materiality_override import build_ucc_materiality_override_receipt; root=Path(r'C:\UVLM\run_artifacts\triadic_llm_ucc_source_materiality'); build_triadic_llm_metrics_smoke(output_root=root); build_sophia_ucc_control_review(root / 'bridge'); build_ucc_standards_source_registry(root / 'bridge'); build_ucc_materiality_profile(root / 'bridge'); build_ucc_materiality_override_receipt(root / 'bridge')"
```
