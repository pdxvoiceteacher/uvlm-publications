"""Repository-local contract tests for the Atlas provenance apprentice materials."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
PROFILE_REL = Path("docs/provenance/atlas_provenance_apprentice_profile.v1.json")
SCHEMA_REL = Path("docs/provenance/uvlm_provenance_repository_apprentice_profile.v1.schema.json")
OVERLAY_REL = Path("docs/provenance/uvlm_provenance_pedagogy_refinement.v1.1.json")
PROFILE_MD_REL = Path("docs/provenance/ATLAS_PROVENANCE_PRESENTATION_PROFILE_v1.md")
OVERLAY_MD_REL = Path("docs/provenance/UVLM_PROVENANCE_PEDAGOGY_REFINEMENT_OVERLAY_v1.1.md")
README_REL = Path("docs/provenance/README.md")

FORBIDDEN_CODEPOINTS = {"\x00", "\ufeff", "\u061c", "\u200b", "\u200c", "\u200d", "\u200e", "\u200f", *(chr(value) for value in range(0x202A, 0x202F)), "\u2066", "\u2067", "\u2068", "\u2069"}
DOCTRINE = {
    "Provenance is lineage, not truth.",
    "Integrity is not correctness.",
    "Authenticity is not authority.",
    "A hash identifies bytes; it does not justify a claim.",
    "Canonicalization creates stable identity, not certainty.",
    "Retention is consent-bounded inspectability, not canon.",
    "Provenance controls must remain useful and proportionate.",
}


def load_json(root: Path, relative: Path) -> dict:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def validate_profile_artifacts(root: Path = ROOT) -> None:
    """Validate the installed profile/overlay contract at a repository root."""
    profile = load_json(root, PROFILE_REL)
    schema = load_json(root, SCHEMA_REL)
    overlay = load_json(root, OVERLAY_REL)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(profile, schema, format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER)

    assert profile["repository"] == "pdxvoiceteacher/uvlm-publications"
    assert profile["profile_id"] == "uvlm.provenance.profile.atlas.v1"
    assert profile["schema_id"] == "uvlm.provenance.repository_apprentice_profile.v1"
    assert profile["authority_effect"] == "none"
    assert profile["role"] == "posture_presenter_and_human_decision_boundary"
    assert profile["canonical_curriculum"] == {
        "repository": "pdxvoiceteacher/CoherenceLattice",
        "path": "docs/provenance/pedagogy/machine/uvlm_provenance_curriculum.v1.json",
        "version": "1.0.0",
    }
    assert set(profile["required_competencies"]) == {f"PV-C{i:02d}" for i in range(1, 13)}
    assert len(profile["required_competencies"]) == len(set(profile["required_competencies"]))
    assert DOCTRINE <= set(profile["doctrine"])

    assert overlay["schema_id"] == "urn:uvlm:provenance:pedagogy-refinement:v1.1"
    assert overlay["version"] == "1.1.0"
    assert overlay["authority_effect"] == "none"
    competencies = overlay["new_competencies"]
    assert {item["competency_id"] for item in competencies} == {f"PV-C{i:02d}" for i in range(13, 19)}
    assert len(competencies) == len({item["competency_id"] for item in competencies})
    refinements = overlay["refinements"]
    assert {item["id"] for item in refinements} == {f"PV-R{i:02d}" for i in range(1, 11)}
    assert len(refinements) == len({item["id"] for item in refinements})
    assert all(item["title"] and item["rule"] for item in refinements)

    # A stable JSON representation makes byte-independent contract comparison possible.
    for relative in (PROFILE_REL, SCHEMA_REL, OVERLAY_REL):
        parsed = load_json(root, relative)
        canonical = json.dumps(parsed, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        assert json.loads(canonical) == parsed

    for relative in (PROFILE_REL, SCHEMA_REL, OVERLAY_REL, PROFILE_MD_REL, OVERLAY_MD_REL, README_REL):
        text = (root / relative).read_text(encoding="utf-8")
        assert not (FORBIDDEN_CODEPOINTS & set(text)), relative

    profile_markdown = (root / PROFILE_MD_REL).read_text(encoding="utf-8")
    for marker in (
        "CoherenceLattice candidate and Sophia audit", "file-byte and canonical-content digests",
        "presentation quality, posture, and evidentiary quality", "immutable human-decision receipt",
        "APPROVE, HOLD, and REJECT", "observed failure", "Accepted predecessor evidence",
        "sensitivity evidence", "validation-driver defect", "Retention is consent-bounded",
        "DOI, Crossref, catalog, graph, publication, deployment, or release", "Invalidation, supersession, and revocation",
        "Polished presentation is not evidence",
    ):
        assert marker in profile_markdown

    readme = (root / README_REL).read_text(encoding="utf-8")
    root_readme = (root / "README.md").read_text(encoding="utf-8")
    assert "docs/provenance/README.md" in root_readme
    for relative in (PROFILE_MD_REL.name, PROFILE_REL.name, SCHEMA_REL.name, OVERLAY_MD_REL.name, OVERLAY_REL.name):
        assert relative in readme
        assert (root / "docs/provenance" / relative).is_file()


def test_provenance_apprentice_profile_contract():
    validate_profile_artifacts()


@pytest.mark.parametrize("relative", [PROFILE_REL, OVERLAY_REL])
def test_profile_validator_is_sensitive_to_required_artifact_removal_or_corruption(tmp_path: Path, relative: Path):
    copied = tmp_path / "repository"
    shutil.copytree(ROOT / "docs/provenance", copied / "docs/provenance")
    target = copied / relative
    if relative == PROFILE_REL:
        target.unlink()
    else:
        target.write_text("{not valid JSON}\n", encoding="utf-8")
    with pytest.raises((AssertionError, FileNotFoundError, json.JSONDecodeError, jsonschema.ValidationError)):
        validate_profile_artifacts(copied)
