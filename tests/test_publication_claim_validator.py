from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tools.validate_publication_claims import validate_publication_claims

ROOT = Path("papers/governed_artifact_cognition")
VALIDATOR = Path("tools/validate_publication_claims.py")


def test_governed_artifact_cognition_claim_validator_passes_current_draft():
    result = validate_publication_claims(
        ROOT / "PUB_GOV_ARTIFACT_COG_01.md",
        appendix=ROOT / "reproducibility_appendix.md",
        quickstart=ROOT / "reviewer_quickstart.md",
        status=ROOT / "status.json",
    )

    assert result["passed"] is True
    assert result["required_files_present"] is True
    assert result["forbidden_overclaims_found"] == []
    assert result["status_json_valid"] is True
    assert result["not_truth_certification"] is True
    assert result["not_deployment_authority"] is True
    assert result["not_final_answer_release"] is True


def test_claim_validator_cli_emits_json_and_supports_out(tmp_path):
    out = tmp_path / "claim_validation.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--paper",
            str(ROOT / "PUB_GOV_ARTIFACT_COG_01.md"),
            "--appendix",
            str(ROOT / "reproducibility_appendix.md"),
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
    assert payload["paper_id"] == "PUB-GOV-ARTIFACT-COG-01"
    assert payload["passed"] is True


def test_claim_validator_rejects_unnegated_forbidden_overclaim(tmp_path):
    paper_root = tmp_path / "paper"
    paper_root.mkdir(parents=True)
    for name in (
        "reproducibility_appendix.md",
        "claim_boundary_table.md",
        "artifact_table.md",
        "reviewer_quickstart.md",
    ):
        (paper_root / name).write_text(
            "not truth certification\n"
            "not deployment authority\n"
            "not final answer release\n"
            "local fixture only\n"
            "requires external peer review\n"
            "not AI consciousness\n"
            "not recursive Sonya federation\n"
            "not retrosynthesis runtime\n"
            "not Omega detection\n"
            "not live Atlas memory writes\n"
            "not live Sophia calls\n",
            encoding="utf-8",
        )
    (paper_root / "PUB_GOV_ARTIFACT_COG_01.md").write_text(
        "This draft proves universal intelligence.", encoding="utf-8"
    )
    (paper_root / "status.json").write_text(
        json.dumps(
            {
                "paper_id": "PUB-GOV-ARTIFACT-COG-01",
                "repo": "pdxvoiceteacher/uvlm-publications",
                "status": "drafted",
                "claim_level": "internal_preprint_draft",
                "requires_external_peer_review": True,
                "not_truth_certification": True,
                "not_deployment_authority": True,
                "not_final_answer_release": True,
                "not_ai_consciousness_claim": True,
            }
        ),
        encoding="utf-8",
    )

    result = validate_publication_claims(paper_root / "PUB_GOV_ARTIFACT_COG_01.md")

    assert result["passed"] is False
    assert result["forbidden_overclaims_found"] == ["proves universal intelligence"]


def test_claim_validator_rejects_invalid_status_json(tmp_path):
    paper_root = tmp_path / "paper"
    paper_root.mkdir()
    valid_text = (
        "not truth certification\n"
        "not deployment authority\n"
        "not final answer release\n"
        "local fixture only\n"
        "requires external peer review\n"
        "not AI consciousness\n"
        "not recursive Sonya federation\n"
        "not retrosynthesis runtime\n"
        "not Omega detection\n"
        "not live Atlas memory writes\n"
        "not live Sophia calls\n"
    )
    for name in (
        "PUB_GOV_ARTIFACT_COG_01.md",
        "reproducibility_appendix.md",
        "claim_boundary_table.md",
        "artifact_table.md",
        "reviewer_quickstart.md",
    ):
        (paper_root / name).write_text(valid_text, encoding="utf-8")
    (paper_root / "status.json").write_text(
        json.dumps({"paper_id": "PUB-GOV-ARTIFACT-COG-01"}), encoding="utf-8"
    )

    result = validate_publication_claims(paper_root / "PUB_GOV_ARTIFACT_COG_01.md")

    assert result["passed"] is False
    assert result["status_json_valid"] is False
    assert "not_truth_certification" in result["status_errors"]


def test_reproducibility_docs_use_accepted_coherencelattice_commands():
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    combined = appendix + "\n" + quickstart

    for required in (
        "python/tests/integration/test_sonya_aegis_smoke_02_acceptance_harness.py",
        "python/tests/integration/test_sonya_aegis_publisher_boundary_finalizer.py",
        "python/tests/integration/test_experiment_suite_repro_pack.py",
        "python/tests/waveform/test_waveform_family_acceptance.py",
        "python -m coherence.waveform.family_acceptance",
        "python -m coherence.tools.build_experiment_suite_repro_pack",
        "experiments\\Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1",
    ):
        assert required in combined

    for placeholder in (
        "tests/test_sonya_aegis_smoke_02.py",
        "tests/test_wave_gold_physics_family.py",
        "scripts/build_experiment_suite_repro_pack.py",
    ):
        assert placeholder not in combined


def test_governed_artifact_cognition_public_utility_alpha_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")

    assert "PUBLIC-UTILITY-ALPHA-00" in paper
    assert "SONYA-GW-01" in paper or "Sonya Gateway candidate path" in paper
    assert "observational telemetry only" in paper
    assert "UNI-02D remains partial" not in paper
    assert "not universal portability proof" in paper
    for artifact in (
        "public_utility_alpha_status.json",
        "public_utility_alpha_manifest.json",
        "public_utility_alpha_claim_boundary.json",
        "public_utility_alpha_review_packet.json",
        "reviewer_index.md",
        "sonya_user_ingress_packet.json",
        "sonya_model_request_packet.json",
        "sonya_model_candidate_packet.json",
        "sonya_model_candidate_review_packet.json",
        "sonya_routing_receipt.json",
        "sonya_runtime_bypass_block_packet.json",
        "sonya_runtime_bypass_review_packet.json",
        "sonya_route_lineage_packet.json",
        "sonya_route_timeline_packet.json",
        "sonya_route_view_review_packet.json",
        "model_braid_packet.json",
        "model_braid_observational_review_packet.json",
        "experiment_catalog_boundary_report.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Public Utility Alpha is not deployment authority.",
        "Public Utility Alpha is not truth certification.",
        "Public Utility Alpha is not final-answer release.",
        "Sonya Gateway candidate packet is not answer.",
        "Runtime bypass block is not model output.",
        "Model braid is not consensus proof.",
        "Model braid is not recursive cognition.",
        "Model braid is not answer selection.",
        "Model braid is not universal ontology.",
        "Experiment catalog is reviewer index, not authority.",
        "Dashboard is reviewer orientation, not deployment.",
    ):
        assert boundary in boundary_table
    assert "Run-PUBLIC-UTILITY-ALPHA00-Acceptance.ps1" in quickstart
    assert "Run-PUBLIC-UTILITY-ALPHA00-Acceptance.ps1" in appendix


def test_governed_artifact_cognition_raw_baseline_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    assert "RAW-BASELINE-COMPARISON-00" in paper
    assert "fixture-only measurement scaffold" in paper
    assert "not hallucination reduction proof" in paper
    assert "not a model quality benchmark" in paper
    assert "raw-model comparison baselines" not in paper
    assert "hallucination reduction proven" not in paper
    assert "model superiority proven" not in paper
    for artifact in (
        "raw_baseline_comparison_packet.json",
        "raw_baseline_comparison_review_packet.json",
        "raw_baseline_comparison_rows.jsonl",
        "raw_baseline_comparison_summary.md",
        "raw_baseline_comparison_00_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Raw Baseline Comparison is not hallucination reduction proof.",
        "Raw Baseline Comparison is not a model quality benchmark.",
        "Raw Baseline Comparison is not model superiority proof.",
        "Raw Baseline Comparison is not live model execution.",
        "Raw Baseline Comparison is not remote provider evaluation.",
        "Raw Baseline Comparison is not production evaluation.",
    ):
        assert boundary in boundary_table
    assert "Run-RAW-BASELINE-COMPARISON00-Acceptance.ps1" in quickstart
    assert status["raw_baseline_comparison_indexed"] is True
    assert status["not_hallucination_reduction_proof"] is True
    assert status["not_model_quality_benchmark"] is True


def _copy_governed_paper(tmp_path: Path) -> Path:
    paper_root = tmp_path / "paper"
    paper_root.mkdir(parents=True)
    for path in ROOT.rglob("*"):
        if path.is_file():
            target = paper_root / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return paper_root


def test_claim_validator_rejects_new_governed_artifact_overclaims(tmp_path):
    forbidden_claims = (
        "deployment readiness",
        "final-answer release",
        "live model execution",
        "federation",
        "retrosynthesis runtime",
        "model braid is consensus proof",
        "model braid is answer selection",
        "hallucination reduction proven",
        "model superiority proven",
        "model quality benchmark",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper claims {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result
