# Atlas provenance apprentice materials

This directory installs the repository-local, non-authorizing provenance apprentice profile for Atlas/Publisher. It is a presentation and immutable human-decision-lineage aid, not a CoherenceLattice or Sophia implementation.

- [Profile v1](ATLAS_PROVENANCE_PRESENTATION_PROFILE_v1.md) defines the human-readable posture, presentation, retention, and decision boundary.
- [Machine profile v1](atlas_provenance_apprentice_profile.v1.json) conforms to its [Draft 2020-12 schema](uvlm_provenance_repository_apprentice_profile.v1.schema.json).
- [Adopted refinement overlay v1.1](UVLM_PROVENANCE_PEDAGOGY_REFINEMENT_OVERLAY_v1.1.md) and its [machine form](uvlm_provenance_pedagogy_refinement.v1.1.json) add PV-C13 through PV-C18 and PV-R01 through PV-R10.

The canonical base curriculum remains in `pdxvoiceteacher/CoherenceLattice` at `docs/provenance/pedagogy/machine/uvlm_provenance_curriculum.v1.json`. This local adoption has `authority_effect: none`: it does not invoke a model, accept raw model output, write memory, persist evidence, or mutate DOI, Crossref, catalog, graph, publication, deployment, or release state.
