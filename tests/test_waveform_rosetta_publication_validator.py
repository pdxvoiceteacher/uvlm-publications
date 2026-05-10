from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tools.validate_publication_claims import validate_publication_claims

ROOT = Path("papers/waveform_rosetta")
VALIDATOR = Path("tools/validate_publication_claims.py")


def test_waveform_rosetta_claim_validator_passes_current_draft():
    result = validate_publication_claims(
        ROOT / "PUB_WAVE_ROSETTA_01.md",
        quickstart=ROOT / "reviewer_quickstart.md",
        status=ROOT / "status.json",
    )

    assert result["paper_id"] == "PUB-WAVE-ROSETTA-01"
    assert result["passed"] is True
    assert result["required_files_present"] is True
    assert result["forbidden_overclaims_found"] == []
    assert result["status_json_valid"] is True
    assert result["not_truth_certification"] is True
    assert result["not_deployment_authority"] is True
    assert result["not_final_answer_release"] is True


def test_waveform_rosetta_validator_cli_emits_json(tmp_path):
    out = tmp_path / "waveform_rosetta_validation.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--paper",
            str(ROOT / "PUB_WAVE_ROSETTA_01.md"),
            "--quickstart",
            str(ROOT / "reviewer_quickstart.md"),
            "--status",
            str(ROOT / "status.json"),
            "--out",
            str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["paper_id"] == "PUB-WAVE-ROSETTA-01"
    assert payload["passed"] is True


def test_waveform_rosetta_validator_rejects_unbounded_overclaim(tmp_path):
    paper_root = tmp_path / "waveform"
    (paper_root / "figures").mkdir(parents=True)
    valid_text = (
        "closed-form waveform metric calibration\n"
        "not universal ontology\n"
        "not psychoacoustic effect\n"
        "not AI consciousness\n"
        "not deployment authority\n"
        "not truth certification\n"
        "requires external peer review\n"
    )
    for name in (
        "abstract.md",
        "methods_appendix.md",
        "theorem_table.md",
        "claim_boundary_table.md",
        "artifact_table.md",
        "reviewer_quickstart.md",
        "figures/README.md",
    ):
        (paper_root / name).write_text(valid_text, encoding="utf-8")
    (paper_root / "PUB_WAVE_ROSETTA_01.md").write_text(
        "This draft proves psychoacoustic entrainment.\n" + valid_text,
        encoding="utf-8",
    )
    (paper_root / "status.json").write_text(
        json.dumps(
            {
                "paper_id": "PUB-WAVE-ROSETTA-01",
                "repo": "pdxvoiceteacher/uvlm-publications",
                "status": "drafted",
                "claim_level": "internal_preprint_draft",
                "requires_external_peer_review": True,
                "not_truth_certification": True,
                "not_deployment_authority": True,
                "not_final_answer_release": True,
                "not_universal_ontology_claim": True,
                "not_psychoacoustic_effect_claim": True,
                "not_ai_consciousness_claim": True,
                "not_retrosynthesis_authorization": True,
            }
        ),
        encoding="utf-8",
    )

    result = validate_publication_claims(paper_root / "PUB_WAVE_ROSETTA_01.md")

    assert result["passed"] is False
    assert result["forbidden_overclaims_found"] == ["proves psychoacoustic entrainment"]


def test_waveform_rosetta_quickstart_uses_accepted_commands():
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")

    for required in (
        "Set-Location C:\\UVLM\\CoherenceLattice",
        '$python = ".\\.venv\\Scripts\\python.exe"',
        "python/tests/waveform/test_waveform_family_acceptance.py",
        "python/tests/integration/test_experiment_suite_repro_pack.py",
        "python -m coherence.waveform.family_acceptance",
        "waveform_gold_physics_family_acceptance_packet.json",
    ):
        assert required in quickstart
