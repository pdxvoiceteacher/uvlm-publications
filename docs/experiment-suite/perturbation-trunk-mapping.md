# Perturbation trunk mapping

PERTURBATION-TRUNK-MAPPING-00 maps known trunk families before novelty claims and does not claim identity or discovery.

## Dashboard summary

- mapping_status = completed
- mapping_mode = known_trunk_mapping_only
- trunk_count = 7
- mapped_trunk_count = 7
- top_trunk_candidate = electrical_decay_trunk
- top_trunk_similarity_score = 0.88
- heatmap_rows = 63
- residual_novelty_mapping_performed = false
- novelty_detection_performed = false
- residual_novelty_claimed = false
- reverse_novel_trunk_claimed = false

## Artifacts

- `perturbation_known_trunk_registry.json`
- `perturbation_trunk_mapping_packet.json`
- `trunk_similarity_heatmap.json`
- `mapped_trunk_residue_report.json`
- `trunk_mapping_boundary_table.json`
- `perturbation_trunk_mapping_summary.md`

## Required boundaries

- Known trunks were mapped before novelty claims.
- Trunk similarity is not identity.
- Known-trunk mapping is not novelty discovery.
- Residual structure is not novel trunk proof.
- Heatmap values are diagnostic, not probability certification.
- Reverse mapping is not performed in this phase.
- Human review remains required.

## Blocked overclaim examples

- trunk similarity is identity
- trunk mapping is novelty discovery
- heatmap values certify probability
- residual structure proves a novel trunk
- truth certification
- final-answer authority
- product release
- model superiority proof
- human benefit proof
- market validation
- consciousness proof
- Omega detection
- universal ontology proof

## Reproducibility

```powershell
python -c "from pathlib import Path; from coherence.perturbation.observation_capture import build_perturbation_observation_capture; from coherence.perturbation.trunk_mapping import build_perturbation_trunk_mapping; from coherence.perturbation.residual_novelty_map import build_perturbation_residual_novelty_map; bridge=Path(r'C:\UVLM\run_artifacts\perturbation_observation_capture\bridge'); build_perturbation_observation_capture(bridge); build_perturbation_trunk_mapping(bridge); build_perturbation_residual_novelty_map(bridge)"
```
