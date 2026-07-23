# Deterministic Atlas posture explanation and decision context

## Purpose and boundaries

`atlas.triadic.governed_posture_explain` is a deterministic, file-only Atlas renderer. It translates an already-sealed Atlas posture and a separately produced Sophia explanation into bounded plain-language decision context. It does not call a model, accept raw provider output, alter a candidate/audit/posture, execute repair, write memory or PMR, canonize, publish, mutate DOI/Crossref/catalog/graph state, deploy, release, or advance a phase.

The explanation is lineage and presentation, not truth. Sophia's disposition informs the presentation but does not certify truth; Atlas does not rank or recommend the human choices.

## Inputs and command

All paths are absolute. `--run-root` identifies a complete sealed run with checksum closure. `--sophia-explanation` is an external `sophia_explanation_packet.json`; it must bind exactly to the sealed candidate and Sophia audit. `--output-root` is an external directory and must not be inside the sealed run.

```bash
PYTHONPATH=python/src python -m atlas.triadic.governed_posture_explain \
  --run-root /absolute/path/to/sealed-run \
  --sophia-explanation /absolute/path/to/sophia_explanation_packet.json \
  --output-root /absolute/path/to/external-explanations
```

The command atomically writes `atlas_explanation_packet.json` using sorted canonical JSON and one final LF. Identical sealed inputs and Sophia explanation bytes produce identical output bytes. Unknown posture values, malformed/unsafe packets, identity/digest mismatches, positive authority/effects, or sealed-root output fail closed with stable error codes.

## What Atlas explains

The packet translates only current `retention_posture`, `publication_posture`, `expiry_posture`, `revocation_posture`, `requires_human_review`, and `human_decision` context. It states why human review remains required, why memory/PMR/canonization/publication/DOI/Crossref/catalog/graph/deployment/release remain separate, and whether the Sophia packet marks repair as available.

The fixed decision meanings are bounded:

- **APPROVE:** accept this bounded output for the stated use.
- **HOLD:** correction or more evidence is required.
- **REJECT:** do not accept this candidate for the stated use.

The only deterministic next-action labels are `REQUEST_REPAIR`, `RECORD_DECISION`, and `EXPORT_EVIDENCE`. Atlas does not execute repairs; repair remains Sonya-routed and produces a new child lineage requiring complete re-review.

## Human-review presentation and evidence binding

The existing loopback review UI remains compatible without an explanation. Supply an optional exact external explanation file to render structured sections, while preserving the review → preview → one-time confirmation → immutable receipt flow:

```bash
PYTHONPATH=python/src python -m atlas.triadic.human_review_ui \
  --run-root /absolute/path/to/sealed-run \
  --explanation-path /absolute/path/to/external-explanations/atlas_explanation_packet.json
```

When presented, a committed receipt records the explanation file and canonical hashes in optional `explanation_evidence_bindings`. Those hashes show the context that was presented; they do not prove that a human read, agreed with, or accepted it. The sealed run remains immutable.
