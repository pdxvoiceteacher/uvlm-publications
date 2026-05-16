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


def test_governed_artifact_cognition_evidence_review_pack_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    for phrase in (
        "EVIDENCE-REVIEW-PACK-00",
        "Evidence Review Pack v0.1 is the first product-facing governed review receipt",
        "Universal Evidence Ingress",
        "UCC Control Profile Selector",
        "AI review that shows its work",
        "not truth certification",
        "not professional advice",
        "not compliance certification",
        "not deployment authority",
        "not hallucination reduction proof",
    ):
        assert phrase in paper
    for artifact in (
        "evidence_review_pack_manifest.json",
        "claim_evidence_map.json",
        "unsupported_claim_report.json",
        "uncertainty_retention_packet.json",
        "source_bounded_counterevidence_packet.json",
        "evidence_semantic_ecology_packet.json",
        "evidence_review_action_recommendation_packet.json",
        "evidence_review_pack_review_packet.json",
        "reviewer_checklist.md",
        "evidence_review_pack_00_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Evidence Review Pack v0.1 is AI review that shows its work.",
        "Evidence Review Pack v0.1 is not truth certification.",
        "Evidence Review Pack v0.1 is not professional advice.",
        "Evidence Review Pack v0.1 is not compliance certification.",
        "Evidence Review Pack v0.1 is not deployment authority.",
        "Evidence Review Pack v0.1 is not hallucination reduction proof.",
    ):
        assert boundary in boundary_table
    assert "Run-EVIDENCE-REVIEW-PACK00-Acceptance.ps1" in quickstart
    assert "Run-EVIDENCE-REVIEW-PACK00-Acceptance.ps1" in appendix
    assert status["evidence_review_pack_indexed"] is True
    assert status["not_professional_advice"] is True
    assert status["not_compliance_certification"] is True


def test_governed_artifact_cognition_rw_comp_01_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    for phrase in (
        "RW-COMP-01",
        "first fixture-only raw-vs-governed comparison involving Evidence Review Pack v0.1",
        "review-structure visibility",
        "step toward future hallucination-reduction evidence",
        "not hallucination-reduction proof yet",
        "not model superiority proof",
    ):
        assert phrase in paper
    for artifact in (
        "rw_comp_01_packet.json",
        "rw_comp_01_review_packet.json",
        "rw_comp_01_rows.jsonl",
        "rw_comp_01_summary.md",
        "rw_comp_01_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "RW-COMP-01 is the first fixture-only raw-vs-governed comparison involving Evidence Review Pack v0.1.",
        "RW-COMP-01 is a step toward future hallucination-reduction evidence.",
        "RW-COMP-01 is not hallucination-reduction proof yet.",
        "RW-COMP-01 is not model superiority proof.",
    ):
        assert boundary in boundary_table
    assert "Run-RW-COMP01-Acceptance.ps1" in quickstart
    assert "Run-RW-COMP01-Acceptance.ps1" in appendix
    assert status["rw_comp_01_indexed"] is True
    assert status["not_model_superiority_proof"] is True


def test_governed_artifact_cognition_rw_comp_02_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "RW-COMP-02",
        "deterministic multi-fixture comparison battery",
        "six controlled fixture families",
        "raw single-model",
        "raw multi-model",
        "RAG-style grounded",
        "Triadic-without-Phase-6",
        "full Evidence Review Pack arms",
        "structural visibility improvement",
        "step toward future hallucination-reduction evidence",
        "not hallucination reduction proof",
        "not hallucination-reduction proof yet",
        "not model-superiority proof",
    ):
        assert phrase in combined_paper
    for artifact in (
        "rw_comp_02_packet.json",
        "rw_comp_02_review_packet.json",
        "rw_comp_02_rows.jsonl",
        "rw_comp_02_fixture_manifest.json",
        "rw_comp_02_summary.md",
        "rw_comp_02_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "RW-COMP-02 is not hallucination reduction proof.",
        "RW-COMP-02 is not model superiority proof.",
        "RW-COMP-02 is not a model quality benchmark.",
        "RW-COMP-02 is not live model evaluation.",
        "RW-COMP-02 is not professional advice.",
        "RW-COMP-02 is not compliance certification.",
        "RW-COMP-02 is not production evaluation.",
    ):
        assert boundary in boundary_table
    assert "Run-RW-COMP02-Acceptance.ps1" in quickstart
    assert "Run-RW-COMP02-Acceptance.ps1" in appendix
    assert "review_status = accepted_as_multi_fixture_comparison_battery" in quickstart
    assert status["rw_comp_02_indexed"] is True
    assert status["not_live_model_evaluation"] is True
    assert status["not_production_evaluation"] is True



def test_governed_artifact_cognition_retrosynthesis_sandbox_cycle_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "RETROSYNTHESIS-SANDBOX-CYCLE-01",
        "first bounded candidate-repair cycle",
        "incomplete or contradiction-bearing Evidence Review Pack artifacts",
        "Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption",
        "not memory write",
        "not final answer release",
        "not Publisher finalization",
        "not Omega detection",
        "not recursive self-improvement",
    ):
        assert phrase in combined_paper
    for artifact in (
        "retrosynthesis_sandbox_cycle_packet.json",
        "retrosynthesis_sandbox_cycle_review_packet.json",
        "retrosynthesis_candidate_repair_plan.json",
        "retrosynthesis_missing_evidence_request_packet.json",
        "retrosynthesis_claim_map_revision_candidate.json",
        "retrosynthesis_uncertainty_restoration_candidate.json",
        "retrosynthesis_counterevidence_expansion_candidate.json",
        "retrosynthesis_next_experiment_recommendation.json",
        "retrosynthesis_sandbox_cycle_summary.md",
        "retrosynthesis_sandbox_cycle_01_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Retrosynthesis Sandbox Cycle is candidate repair, not canon adoption.",
        "Retrosynthesis Sandbox Cycle is not memory write.",
        "Retrosynthesis Sandbox Cycle is not final answer release.",
        "Retrosynthesis Sandbox Cycle is not Publisher finalization.",
        "Retrosynthesis Sandbox Cycle is not deployment authority.",
        "Retrosynthesis Sandbox Cycle is not Omega detection.",
        "Retrosynthesis Sandbox Cycle is not publication claim authorization.",
        "Retrosynthesis Sandbox Cycle is not recursive self-improvement.",
        "Retrosynthesis Sandbox Cycle is not hallucination reduction proof.",
        "Retrosynthesis Sandbox Cycle is not model superiority proof.",
    ):
        assert boundary in boundary_table
    assert "Run-RETROSYNTHESIS-SANDBOX-CYCLE01-Acceptance.ps1" in quickstart
    assert "Run-RETROSYNTHESIS-SANDBOX-CYCLE01-Acceptance.ps1" in appendix
    assert "review_status = accepted_as_bounded_retrosynthesis_sandbox_cycle" in quickstart
    assert status["retrosynthesis_sandbox_cycle_indexed"] is True
    assert status["not_canon_adoption"] is True
    assert status["not_memory_write"] is True
    assert status["not_publisher_finalization"] is True
    assert status["not_omega_detection"] is True
    assert status["not_publication_claim"] is True
    assert status["not_recursive_self_improvement"] is True


def test_claim_validator_rejects_retrosynthesis_sandbox_cycle_overclaims(tmp_path):
    forbidden_claims = (
        "canon adoption",
        "memory write",
        "final answer release",
        "Publisher finalization",
        "Omega detection",
        "recursive self-improvement achieved",
        "claims adapter execution",
        "claims network authorization",
        "remote provider call",
        "claims model-weight training",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(
            paper.read_text(encoding="utf-8") + f"\nThis paper claims {claim}.\n",
            encoding="utf-8",
        )
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_governed_artifact_cognition_evidence_review_pack_01_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "EVIDENCE-REVIEW-PACK-01",
        "second-pass candidate loop",
        "Evidence Review Pack second pass is candidate revision, not accepted evidence",
        "not canon adoption",
        "not memory write",
        "not final answer release",
        "not Publisher finalization",
        "not Omega detection",
        "not recursive self-improvement",
        "structural visibility delta is not hallucination-reduction proof",
        "claim-map revision candidate is not truth certification",
        "uncertainty/counterevidence revision candidate is not canon",
    ):
        assert phrase in combined_paper
    for artifact in (
        "evidence_review_second_pass_packet.json",
        "evidence_review_second_pass_review_packet.json",
        "evidence_review_claim_map_revision_packet.json",
        "evidence_review_second_pass_delta_packet.json",
        "evidence_review_uncertainty_revision_packet.json",
        "evidence_review_counterevidence_revision_packet.json",
        "evidence_review_second_pass_summary.md",
        "evidence_review_pack_01_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Evidence Review Pack second pass is candidate revision, not accepted evidence.",
        "Evidence Review Pack second pass is not canon adoption.",
        "Evidence Review Pack second pass is not memory write.",
        "Evidence Review Pack second pass is not final answer release.",
        "Evidence Review Pack second pass is not Publisher finalization.",
        "Evidence Review Pack second pass is not deployment authority.",
        "Evidence Review Pack second pass is not Omega detection.",
        "Evidence Review Pack second pass is not publication claim authorization.",
        "Evidence Review Pack second pass is not recursive self-improvement.",
        "Evidence Review Pack second pass is not hallucination reduction proof.",
        "Evidence Review Pack second pass is not model superiority proof.",
    ):
        assert boundary in boundary_table
    assert "Run-EVIDENCE-REVIEW-PACK01-Acceptance.ps1" in quickstart
    assert "Run-EVIDENCE-REVIEW-PACK01-Acceptance.ps1" in appendix
    assert "review_status = accepted_as_second_pass_review_candidate" in quickstart
    assert status["evidence_review_pack_01_indexed"] is True
    assert status["not_accepted_evidence"] is True
    assert status["not_canon_adoption"] is True
    assert status["not_memory_write"] is True
    assert status["not_publisher_finalization"] is True
    assert status["not_omega_detection"] is True
    assert status["not_publication_claim"] is True
    assert status["not_recursive_self_improvement"] is True


def test_claim_validator_rejects_evidence_review_pack_01_overclaims(tmp_path):
    forbidden_claims = (
        "claims accepted evidence",
        "claims canon adoption",
        "claims memory write",
        "final answer release",
        "claims Publisher finalization",
        "claims Omega detection",
        "claims recursive self-improvement",
        "hallucination reduction proven",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(
            paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n",
            encoding="utf-8",
        )
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_governed_artifact_cognition_rw_comp_03_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "RW-COMP-03",
        "held-out blinded fixture scaffold",
        "held-out, blinded, pre-registered fixture-scoring scaffold",
        "simulated scores only",
        "not hallucination reduction proof",
        "not model superiority proof",
        "not live model evaluation",
        "not live human study",
        "not human-subject study result",
        "not accepted evidence",
        "review_status = accepted_as_heldout_blinded_fixture_scaffold",
        "fixture_count = 8",
        "arm_count_per_fixture = 6",
        "blind_labels_present = true",
        "statistics_plan_present = true",
        "statistics_packet_present = true",
        "second_pass_candidate_arm_present = true",
    ):
        assert phrase in combined_paper
    for artifact in (
        "rw_comp_03_packet.json",
        "rw_comp_03_review_packet.json",
        "rw_comp_03_rows.jsonl",
        "rw_comp_03_fixture_manifest.json",
        "rw_comp_03_blind_labels.json",
        "rw_comp_03_scoring_rubric.json",
        "rw_comp_03_reviewer_score_packet.json",
        "rw_comp_03_statistics_plan.json",
        "rw_comp_03_statistics_packet.json",
        "rw_comp_03_summary.md",
        "rw_comp_03_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "RW-COMP-03 is a held-out blinded fixture scaffold, not hallucination reduction proof.",
        "RW-COMP-03 is not model superiority proof.",
        "RW-COMP-03 is not a model quality benchmark.",
        "RW-COMP-03 is not live model evaluation.",
        "RW-COMP-03 is not a live human study.",
        "RW-COMP-03 is not human-subject study result.",
        "RW-COMP-03 is not accepted evidence.",
        "RW-COMP-03 is not deployment authority.",
        "RW-COMP-03 is not production evaluation.",
    ):
        assert boundary in boundary_table
    assert "Run-RW-COMP03-Acceptance.ps1" in quickstart
    assert "Run-RW-COMP03-Acceptance.ps1" in appendix
    assert status["retrosynthesis_sandbox_cycle_indexed"] is True
    assert status["evidence_review_pack_01_indexed"] is True
    assert status["not_canon_adoption"] is True
    assert status["not_memory_write"] is True
    assert status["not_publisher_finalization"] is True
    assert status["not_omega_detection"] is True
    assert status["not_publication_claim"] is True
    assert status["not_recursive_self_improvement"] is True
    assert status["not_accepted_evidence"] is True
    assert status["rw_comp_03_indexed"] is True
    assert status["not_live_human_study"] is True
    assert status["not_human_subject_study_result"] is True
    assert status["not_hallucination_reduction_proof"] is True
    assert status["not_model_superiority_proof"] is True
    assert status["not_model_quality_benchmark"] is True
    assert status["not_live_model_evaluation"] is True
    assert status["not_production_evaluation"] is True


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
        "model superiority proof",
        "hallucination reduction proof",
        "live model evaluation",
        "model quality benchmark",
        "professional advice",
        "compliance certification",
        "live human study",
        "human-subject study result",
        "accepted evidence",
        "production readiness",
        "product release",
        "benchmark result",
        "recursive self-improvement achieved",
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


def test_governed_artifact_cognition_universal_architecture_scaffold_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "UNIVERSAL-STAGE-PIPELINE-00",
        "ARTIFACT-CONTRACT-REGISTRY-01",
        "UNIVERSAL-COMPATIBILITY-MATRIX-00",
        "The brain runs cognition stages; experiments configure those stages.",
        "profiles are configuration",
        "artifact contracts are versioned configuration",
        "unsupported inputs fail closed or hash-only",
        "hash-only preservation is not semantic interpretation",
        "not product release",
        "not benchmark result",
        "not hallucination reduction proof",
        "Universal Evidence Ingress → UCC Control Profile Selector → Evidence Review Pack → Retrosynthesis Sandbox Cycle → Evidence Review Pack second-pass candidate → RW-COMP comparison scaffolds → Universal Stage Pipeline → Artifact Contract Registry → Universal Compatibility Matrix",
        "review_status = accepted_as_universal_compatibility_scaffold",
        "all_required_stage_ids_present = true",
        "all_required_input_classes_present = true",
        "all_required_control_profiles_present = true",
        "unsupported_inputs_failed_closed_or_hash_only = true",
        "hash_only_inputs_not_semantically_interpreted = true",
        "model_facing_stages_require_sonya = true",
        "no_experiment_specific_kernel_logic_used = true",
        "failure_receipts_visible = true",
        "promotion_blocked = true",
    ):
        assert phrase in combined_paper

    for artifact in (
        "universal_compatibility_matrix_packet.json",
        "universal_stage_failure_receipts.jsonl",
        "artifact_roles.v1.json",
    ):
        assert artifact in artifact_table
    assert "architecture scaffold" in artifact_table
    assert "not product release" in artifact_table
    assert "not benchmark result" in artifact_table
    assert "not truth certification" in artifact_table
    assert "not deployment authority" in artifact_table
    assert "not hallucination reduction proof" in artifact_table

    assert "Experiments configure stages; they do not define the kernel." in boundary_table
    assert "Hash-only preservation is not semantic interpretation." in boundary_table
    assert "Run-UNIVERSAL-COMPATIBILITY-MATRIX00-Acceptance.ps1" in quickstart
    assert "How to reproduce the Universal Architecture Scaffold" in quickstart
    assert "Run-UNIVERSAL-COMPATIBILITY-MATRIX00-Acceptance.ps1" in appendix
    assert "python/tests/pipeline/test_universal_stage_pipeline.py" in appendix
    assert "python/tests/integration/test_artifact_contract_registry.py" in appendix
    assert status["universal_stage_pipeline_indexed"] is True
    assert status["artifact_contract_registry_indexed"] is True
    assert status["universal_compatibility_matrix_indexed"] is True
    assert status["not_product_release"] is True
    assert status["not_experiment_result"] is True
    assert status["not_benchmark_result"] is True
    assert status["not_recursive_self_improvement"] is True


def test_claim_validator_rejects_universal_architecture_overclaims(tmp_path):
    forbidden_claims = (
        "product release",
        "benchmark result",
        "hallucination reduction proven",
        "recursive self-improvement achieved",
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
        forbidden_found = [found.lower() for found in result["forbidden_overclaims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_governed_artifact_cognition_sonya_adapter_contract_registry_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
        "Adapter capability is not adapter authorization.",
        "not adapter execution",
        "not network authorization",
        "Raw output is forbidden",
        "Candidate packets are required",
        "Failure receipts are required",
        "not model-weight training",
        "Universal Stage Pipeline → Artifact Contract Registry → Universal Compatibility Matrix → Provenance Training Ledger → Sonya Adapter Contract Registry",
        "review_status = accepted_as_adapter_contract_registry_only",
        "adapter_count = 11",
        "disabled_or_blocked_adapter_count = 11",
        "enabled_live_adapter_count = 0",
        "all_adapters_disabled_or_blocked = true",
        "no_live_adapter_execution = true",
        "no_network_calls = true",
        "no_remote_provider_calls = true",
        "sonya_gateway_required = true",
        "raw_output_forbidden = true",
        "candidate_packet_required = true",
        "failure_receipts_required = true",
        "provenance_training_policy_present = true",
        "promotion_blocked = true",
    ):
        assert phrase in combined_paper

    for artifact in (
        "sonya_adapter_contract_registry_packet.json",
        "sonya_adapter_contract_review_packet.json",
        "sonya_adapter_capability_matrix_packet.json",
        "sonya_adapter_consent_matrix_packet.json",
        "sonya_adapter_provenance_training_policy_packet.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Sonya Adapter Contract Registry is not adapter execution.",
        "Adapter capability is not adapter authorization.",
        "Sonya Adapter Contract Registry is not network authorization.",
        "Sonya Adapter Contract Registry is not remote provider call.",
        "Sonya Adapter Contract Registry is not model-weight training.",
    ):
        assert boundary in boundary_table
    assert "Run-SONYA-ADAPTER-CONTRACT-REGISTRY01-Acceptance.ps1" in quickstart
    assert "Run-SONYA-ADAPTER-CONTRACT-REGISTRY01-Acceptance.ps1" in appendix
    assert status["sonya_adapter_contract_registry_indexed"] is True
    assert status["not_adapter_execution"] is True
    assert status["not_network_authorization"] is True
    assert status["not_model_weight_training"] is True



def test_governed_artifact_cognition_sonya_adapter_smoke_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "SONYA-ADAPTER-SMOKE-00",
        "Sonya Adapter Smoke exercises contracts, not live adapters.",
        "not adapter execution",
        "not live adapter execution",
        "not network authorization",
        "no remote provider call",
        "raw_output_rejected_or_absent = true",
        "candidate_packet_emitted_for_fixture_model = true",
        "failure_receipts_visible = true",
        "telemetry_events_visible = true",
        "provenance_events_visible = true",
        "not model-weight training",
        "Universal Stage Pipeline → Artifact Contract Registry → Universal Compatibility Matrix → Provenance Training Ledger → Sonya Adapter Contract Registry → Sonya Adapter Smoke",
        "SONYA-ADAPTER-SMOKE-00 exercises adapter contracts only",
        "connect local fixture adapter candidates into Evidence Review Pack path",
        "adapter failure receipt replay",
        "adapter telemetry event validation",
        "adapter provenance credit calibration",
        "local-only adapter execution expansion",
        "remote/provider placeholders remain blocked until consent/network/privacy gates exist",
    ):
        assert phrase in combined_paper

    for artifact in (
        "sonya_adapter_smoke_packet.json",
        "sonya_adapter_smoke_review_packet.json",
        "sonya_adapter_failure_receipt.json",
        "sonya_adapter_telemetry_packet.json",
        "sonya_adapter_provenance_event_packet.json",
    ):
        assert artifact in artifact_table

    for boundary in (
        "Sonya Adapter Smoke exercises contracts, not live adapters.",
        "Sonya Adapter Smoke is not adapter execution.",
        "Sonya Adapter Smoke is not live adapter execution.",
        "Sonya Adapter Smoke is not network authorization.",
        "Sonya Adapter Smoke is not remote provider call.",
        "Sonya Adapter Smoke is not live model execution.",
        "Sonya Adapter Smoke is not memory write.",
        "Sonya Adapter Smoke is not final answer release.",
        "Sonya Adapter Smoke is not deployment authority.",
        "Sonya Adapter Smoke is not model-weight training.",
        "Sonya Adapter Smoke is not hallucination reduction proof.",
        "Sonya Adapter Smoke is not recursive self-improvement.",
    ):
        assert boundary in boundary_table

    assert "Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1" in quickstart
    assert "Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1" in appendix
    assert status["sonya_adapter_smoke_indexed"] is True
    assert status["not_live_adapter_execution"] is True


def test_governed_artifact_cognition_sonya_local_fixture_adapter_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "SONYA-LOCAL-FIXTURE-ADAPTER-01",
        "Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters.",
        "deterministic local-only fixture adapter execution",
        "consumes SONYA-ADAPTER-CONTRACT-REGISTRY-01 and SONYA-ADAPTER-SMOKE-00",
        "fixture_text_model_adapter",
        "fixture_summary_generator_adapter",
        "local_file_transform_adapter",
        "hash_only_evidence_adapter",
        "remote_provider_placeholder_adapter",
        "browser_placeholder_adapter",
        "atlas_memory_placeholder_adapter",
        "sophia_route_placeholder_adapter",
        "candidate packets emitted",
        "failure receipts visible",
        "telemetry events visible",
        "provenance events visible",
        "not live adapter execution",
        "not network authorization",
        "no remote provider call",
        "not model-weight training",
        "Universal Stage Pipeline → Artifact Contract Registry → Universal Compatibility Matrix → Provenance Training Ledger → Sonya Adapter Contract Registry → Sonya Adapter Smoke → Sonya Local Fixture Adapter",
        "review_status = accepted_as_local_fixture_adapter_execution",
        "local_fixture_adapter_execution_performed = true",
        "candidate_packet_count = 3",
        "failure_receipt_count = 6",
        "telemetry_event_count = 52",
        "provenance_event_count = 35",
        "connect local fixture adapter candidates into Evidence Review Pack path",
        "adapter failure receipt replay",
        "adapter telemetry event validation",
        "adapter provenance credit calibration",
        "local-only adapter execution expansion",
        "remote/provider placeholders remain blocked until consent/network/privacy gates exist",
    ):
        assert phrase in combined_paper

    for artifact in (
        "sonya_local_fixture_adapter_packet.json",
        "sonya_local_fixture_adapter_review_packet.json",
        "sonya_local_adapter_execution_packet.json",
        "sonya_local_adapter_candidate_packet.json",
        "sonya_local_adapter_failure_receipt.json",
        "sonya_local_adapter_telemetry_packet.json",
        "sonya_local_adapter_provenance_event_packet.json",
        "sonya_local_fixture_adapter_summary.md",
        "sonya_local_fixture_adapter_01_acceptance_receipt.json",
    ):
        assert artifact in artifact_table

    for boundary in (
        "Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters.",
        "Sonya Local Fixture Adapter is not live adapter execution.",
        "Sonya Local Fixture Adapter is not network authorization.",
        "Sonya Local Fixture Adapter is not remote provider call.",
        "Sonya Local Fixture Adapter is not live model execution.",
        "Sonya Local Fixture Adapter is not memory write.",
        "Sonya Local Fixture Adapter is not final answer release.",
        "Sonya Local Fixture Adapter is not deployment authority.",
        "Sonya Local Fixture Adapter is not model-weight training.",
        "Sonya Local Fixture Adapter is not hallucination reduction proof.",
        "Sonya Local Fixture Adapter is not recursive self-improvement.",
    ):
        assert boundary in boundary_table

    assert "Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1" in quickstart
    assert "Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1" in appendix
    assert status["sonya_local_fixture_adapter_indexed"] is True
    assert status["sonya_adapter_smoke_indexed"] is True
    assert status["sonya_adapter_contract_registry_indexed"] is True
    assert status["not_adapter_execution"] is True
    assert status["not_live_adapter_execution"] is True
    assert status["not_network_authorization"] is True
    assert status["not_model_weight_training"] is True
    assert status["not_remote_provider_call"] is True
    assert status["not_hallucination_reduction_proof"] is True
    assert status["not_recursive_self_improvement"] is True


def test_governed_artifact_cognition_evidence_review_pack_local_adapter_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    appendix = (ROOT / "reproducibility_appendix.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))

    combined_paper = paper + "\n" + abstract
    for phrase in (
        "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
        "Local adapter candidates become reviewable only through the Evidence Review Pack path.",
        "Adapter output is not accepted as cognition directly.",
        "UCC control profile applied",
        "Unsupported claims listed",
        "Provenance events visible",
        "consumes SONYA-LOCAL-FIXTURE-ADAPTER-01",
        "fixture_summary_generator_adapter candidate output",
        "adapter candidate binding packet",
        "local-adapter claim map",
        "does not produce accepted evidence",
        "does not authorize adapter execution",
    ):
        assert phrase in combined_paper

    for artifact in (
        "evidence_review_local_adapter_route_packet.json",
        "evidence_review_local_adapter_claim_map.json",
        "evidence_review_local_adapter_provenance_packet.json",
    ):
        assert artifact in artifact_table

    for boundary in (
        "Adapter output is not accepted as cognition directly.",
        "Local adapter candidates become reviewable only through the Evidence Review Pack path.",
        "Evidence Review Pack local-adapter route is not accepted evidence.",
        "Evidence Review Pack local-adapter route is not adapter authorization.",
        "Evidence Review Pack local-adapter route is not memory write.",
        "Evidence Review Pack local-adapter route is not final answer release.",
        "Evidence Review Pack local-adapter route is not deployment authority.",
        "Evidence Review Pack local-adapter route is not model-weight training.",
        "Evidence Review Pack local-adapter route is not hallucination reduction proof.",
        "Evidence Review Pack local-adapter route is not recursive self-improvement.",
    ):
        assert boundary in boundary_table

    assert "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1" in quickstart
    assert "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1" in appendix
    assert status["evidence_review_pack_local_adapter_indexed"] is True
    assert status["not_adapter_authorization"] is True


def test_claim_validator_rejects_evidence_review_pack_local_adapter_overclaims(tmp_path):
    forbidden_claims = (
        "accepted evidence",
        "adapter authorization",
        "final answer release",
        "claims deployment authority",
        "claims model-weight training",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_governed_artifact_cognition_sonya_local_fixture_adapter_multi_route_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    combined = paper + "\n" + abstract
    for phrase in (
        "SONYA-LOCAL-FIXTURE-ADAPTER-02",
        "Multi-adapter local fixture selection still requires Evidence Review Pack review.",
        "Selection policy is not final answer.",
        "Candidate comparison is not model quality benchmark.",
        "Selection is not adapter authorization.",
        "candidate-fixture-summary",
    ):
        assert phrase in combined
    for artifact in (
        "sonya_local_adapter_multi_route_packet.json",
        "sonya_local_adapter_candidate_comparison_packet.json",
        "sonya_local_adapter_selection_policy_packet.json",
        "sonya_local_adapter_selected_candidate_packet.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Selection policy is not final answer.",
        "Multi-adapter local fixture selection still requires Evidence Review Pack review.",
        "Sonya Local Fixture Adapter multi-route is not adapter authorization.",
        "Sonya Local Fixture Adapter multi-route is not a model quality benchmark.",
    ):
        assert boundary in boundary_table
    assert "Run-SONYA-LOCAL-FIXTURE-ADAPTER02-Acceptance.ps1" in quickstart
    assert status["sonya_local_fixture_adapter_02_indexed"] is True
    assert status["not_final_answer_selection"] is True


def test_claim_validator_rejects_sonya_local_fixture_adapter_multi_route_overclaims(tmp_path):
    forbidden_claims = (
        "final answer selection",
        "adapter authorization",
        "model quality benchmark",
        "claims deployment authority",
        "claims model-weight training",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_claim_validator_rejects_sonya_local_fixture_adapter_overclaims(tmp_path):
    forbidden_claims = (
        "live adapter execution",
        "claims network authorization",
        "remote provider call",
        "remote provider calls",
        "claims model-weight training",
        "claims deployment authority",
        "production readiness",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_claim_validator_rejects_sonya_adapter_smoke_overclaims(tmp_path):
    forbidden_claims = (
        "claims adapter execution",
        "claims live adapter execution",
        "claims network authorization",
        "remote provider call",
        "claims model-weight training",
        "claims deployment authority",
        "production readiness",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result

def test_claim_validator_rejects_sonya_adapter_contract_overclaims(tmp_path):
    forbidden_claims = (
        "claims adapter execution",
        "claims network authorization",
        "remote provider call",
        "claims model-weight training",
        "claims deployment authority",
        "production readiness",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_governed_artifact_cognition_sonya_local_fixture_adapter_lineage_clarity_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    combined = paper + "\n" + abstract
    for phrase in (
        "SONYA-LOCAL-FIXTURE-ADAPTER-03",
        "Nested SONYA-LOCAL-FIXTURE-ADAPTER-01 references are source fixture dependencies, not stale identity leakage.",
        "Current route identity is explicit.",
        "Source fixture identity is explicit.",
        "Evidence Review Pack local-adapter route references are explicit.",
        "Lineage does not grant authority.",
    ):
        assert phrase in combined
    for artifact in (
        "sonya_local_adapter_lineage_packet.json",
        "sonya_local_adapter_lineage_review_packet.json",
        "sonya_local_fixture_adapter_03_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Source fixture references are not stale identity leakage.",
        "Nested SONYA-LOCAL-FIXTURE-ADAPTER-01 references are source fixture dependencies, not stale identity leakage.",
        "Sonya local adapter lineage packet is not adapter execution.",
        "Sonya local adapter lineage packet is not network authorization.",
        "Sonya local adapter lineage packet is not memory write.",
        "Sonya local adapter lineage packet is not final answer release.",
        "Sonya local adapter lineage packet is not deployment authority.",
        "Sonya local adapter lineage packet is not truth certification.",
    ):
        assert boundary in boundary_table
    assert "Run-SONYA-LOCAL-FIXTURE-ADAPTER03-Acceptance.ps1" in quickstart
    assert status["sonya_local_fixture_adapter_03_indexed"] is True
    assert status["not_stale_identity_leakage"] is True
    assert status["not_lineage_authority"] is True


def test_claim_validator_rejects_sonya_local_fixture_adapter_lineage_overclaims(tmp_path):
    forbidden_claims = (
        "claims adapter execution",
        "claims stale identity proof of execution",
        "claims lineage authority",
        "lineage grants authority",
        "claims deployment authority",
        "claims model-weight training",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_governed_artifact_cognition_evidence_review_pack_local_adapter_revision_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    combined = paper + "\n" + abstract
    for phrase in (
        "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02",
        "The revised local adapter candidate remains candidate-only, not accepted evidence.",
        "Deltas are structural review descriptors",
        "not hallucination-reduction proof",
        "not model quality benchmark",
        "unsupported_claim_count_delta = -1",
        "uncertainty_missing_count_delta = -1",
        "source_reference_visibility_delta = 1",
        "structural_visibility_improved_candidate = true",
    ):
        assert phrase in combined
    for artifact in (
        "evidence_review_local_adapter_revision_packet.json",
        "evidence_review_local_adapter_revision_plan.json",
        "evidence_review_local_adapter_revised_candidate.json",
        "evidence_review_local_adapter_revision_claim_map.json",
        "evidence_review_local_adapter_revision_delta.json",
        "evidence_review_local_adapter_revision_review_packet.json",
        "evidence_review_local_adapter_revision_summary.md",
        "evidence_review_pack_local_adapter_02_acceptance_receipt.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Deltas are structural review descriptors, not hallucination reduction proof.",
        "Revised local adapter candidate remains candidate-only, not accepted evidence.",
        "Evidence Review Pack local-adapter revision loop is not final answer selection.",
        "Evidence Review Pack local-adapter revision loop is not model quality benchmark.",
        "Evidence Review Pack local-adapter revision loop is not model superiority proof.",
        "Evidence Review Pack local-adapter revision loop is not adapter authorization.",
    ):
        assert boundary in boundary_table
    assert "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER02-Acceptance.ps1" in quickstart
    assert status["evidence_review_pack_local_adapter_02_indexed"] is True
    assert status["not_structural_delta_proof"] is True


def test_claim_validator_rejects_evidence_review_pack_local_adapter_revision_overclaims(tmp_path):
    forbidden_claims = (
        "claims hallucination reduction proof",
        "claims model quality benchmark",
        "claims final answer selection",
        "claims accepted evidence",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_governed_artifact_cognition_rw_comp_local_adapter_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    combined = paper + "\n" + abstract
    for phrase in (
        "RW-COMP-LOCAL-ADAPTER-01",
        "RW-COMP local-adapter comparison is not hallucination reduction proof or a model quality benchmark.",
        "Deltas are structural review descriptors only.",
        "unsupported_claim_count_delta = -1",
        "uncertainty_missing_count_delta = -1",
        "source_reference_visibility_delta = 1",
    ):
        assert phrase in combined
    for artifact in (
        "rw_comp_local_adapter_packet.json",
        "rw_comp_local_adapter_delta_packet.json",
    ):
        assert artifact in artifact_table
    for boundary in (
        "Deltas are structural review descriptors only.",
        "RW-COMP local-adapter comparison is not hallucination reduction proof or a model quality benchmark.",
        "RW-COMP local-adapter comparison is not final answer selection.",
        "RW-COMP local-adapter comparison is not accepted evidence.",
    ):
        assert boundary in boundary_table
    assert "Run-RW-COMP-LOCAL-ADAPTER01-Acceptance.ps1" in quickstart
    assert status["rw_comp_local_adapter_indexed"] is True


def test_claim_validator_rejects_rw_comp_local_adapter_overclaims(tmp_path):
    forbidden_claims = (
        "claims hallucination reduction proof",
        "claims model quality benchmark",
        "claims final answer selection",
        "claims accepted evidence",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_governed_artifact_cognition_pmr_updates_are_present():
    paper = (ROOT / "PUB_GOV_ARTIFACT_COG_01.md").read_text(encoding="utf-8")
    abstract = (ROOT / "abstract.md").read_text(encoding="utf-8")
    artifact_table = (ROOT / "artifact_table.md").read_text(encoding="utf-8")
    boundary_table = (ROOT / "claim_boundary_table.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "reviewer_quickstart.md").read_text(encoding="utf-8")
    status = json.loads((ROOT / "status.json").read_text(encoding="utf-8"))
    combined = paper + "\n" + abstract
    for phrase in (
        "PMR-00-PROVENANCE-MEMORY-RESERVOIR",
        "PMR-01-LOCAL-ARTIFACT-INDEX",
        "PMR artifact lifecycle state is not truth status.",
        "Memory is governed provenance under resource constraints.",
        "Hash is not encryption.",
        "dependency graph is not canon graph",
        "No pruning occurs in PMR-01.",
        "Federation is blocked by default.",
    ):
        assert phrase in combined
    for artifact in (
        "pmr_local_artifact_index.json",
        "pmr_dependency_graph.json",
    ):
        assert artifact in artifact_table
    assert "Run-PMR00-Acceptance.ps1" in quickstart
    assert "Run-PMR01-Acceptance.ps1" in quickstart
    assert status["pmr_00_indexed"] is True
    assert status["pmr_01_indexed"] is True
    assert status["not_atlas_canon"] is True
    assert status["not_federation_authorization"] is True
    assert "Memory is governed provenance under resource constraints." in boundary_table
    assert "PMR artifact lifecycle state is not truth status." in boundary_table


def test_claim_validator_rejects_pmr_overclaims(tmp_path):
    forbidden_claims = (
        "claims Atlas canon",
        "claims memory write authorization",
        "claims pruning execution",
        "claims resource economy",
        "claims federation authorization",
    )
    for claim in forbidden_claims:
        paper_root = _copy_governed_paper(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        paper = paper_root / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text(encoding="utf-8") + f"\nThis paper {claim}.\n", encoding="utf-8")
        result = validate_publication_claims(
            paper,
            appendix=paper_root / "reproducibility_appendix.md",
            quickstart=paper_root / "reviewer_quickstart.md",
            status=paper_root / "status.json",
        )
        assert result["passed"] is False, claim
        assert result["forbidden_overclaims_found"], result


def test_governed_paper_includes_pmr_02_gpcu_boundaries():
    root = Path("papers/governed_artifact_cognition")
    paper = (root / "PUB_GOV_ARTIFACT_COG_01.md").read_text()
    artifact_table = (root / "artifact_table.md").read_text()
    quickstart = (root / "reviewer_quickstart.md").read_text()
    status = json.loads((root / "status.json").read_text())

    assert "PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY" in paper
    assert "Lifecycle recommendation is not pruning." in paper
    assert "GPCU is lifecycle/storage utility, not truth score." in paper
    assert "GPCU is not reward entitlement." in paper
    assert "GPCU is not token economy." in paper
    assert "GPCU is not human value score." in paper
    assert "pmr_provenance_coherence_utility_packet.json" in artifact_table
    assert "pmr_artifact_utility_scores.jsonl" in artifact_table
    assert "pmr_lifecycle_recommendation_packet.json" in artifact_table
    assert "Run-PMR02-Acceptance.ps1" in quickstart
    assert status["pmr_02_indexed"] is True
    assert status["not_truth_score"] is True
    assert status["not_reward_entitlement"] is True


def test_governed_validator_rejects_pmr_02_overclaims(tmp_path):
    root = Path("papers/governed_artifact_cognition")
    for claim in ("truth score", "reward entitlement", "token economy", "pruning execution"):
        case = tmp_path / claim.replace(" ", "_")
        case.mkdir()
        for source in root.iterdir():
            if source.is_file():
                (case / source.name).write_text(source.read_text())
        paper = case / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text() + f"\nPMR-02 claims {claim}.\n")
        result = validate_publication_claims(
            paper,
            case / "reproducibility_appendix.md",
            case / "reviewer_quickstart.md",
            case / "status.json",
        )
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_overclaims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found, result


def test_governed_paper_includes_pmr_03_lifecycle_state_machine_boundaries():
    root = Path("papers/governed_artifact_cognition")
    paper = (root / "PUB_GOV_ARTIFACT_COG_01.md").read_text()
    artifact_table = (root / "artifact_table.md").read_text()
    quickstart = (root / "reviewer_quickstart.md").read_text()
    status = json.loads((root / "status.json").read_text())

    assert "PMR-03-LIFECYCLE-STATE-MACHINE" in paper
    assert "Lifecycle state is not truth status." in paper
    assert "Recommendation is not transition." in paper
    assert "Transition candidate is not action." in paper
    assert "Destructive action requires future Sophia lifecycle audit." in paper
    assert "Destructive action requires future user confirmation." in paper
    assert "No pruning or deletion occurs in PMR-03." in paper
    assert "pmr_lifecycle_state_machine_packet.json" in artifact_table
    assert "pmr_lifecycle_no_action_receipt.json" in artifact_table
    assert "Run-PMR03-Acceptance.ps1" in quickstart
    assert status["pmr_03_indexed"] is True
    assert status["not_lifecycle_action"] is True


def test_governed_validator_rejects_pmr_03_overclaims(tmp_path):
    root = Path("papers/governed_artifact_cognition")
    for claim in ("pruning execution", "deletion execution", "reward entitlement", "token economy"):
        case = tmp_path / claim.replace(" ", "_")
        case.mkdir()
        for source in root.iterdir():
            if source.is_file():
                (case / source.name).write_text(source.read_text())
        paper = case / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text() + f"\nPMR-03 claims {claim}.\n")
        result = validate_publication_claims(
            paper,
            case / "reproducibility_appendix.md",
            case / "reviewer_quickstart.md",
            case / "status.json",
        )
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_overclaims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found, result


def test_governed_paper_includes_pmr_04_lifecycle_audit_preflight_boundaries():
    root = Path("papers/governed_artifact_cognition")
    paper = (root / "PUB_GOV_ARTIFACT_COG_01.md").read_text()
    artifact_table = (root / "artifact_table.md").read_text()
    quickstart = (root / "reviewer_quickstart.md").read_text()
    status = json.loads((root / "status.json").read_text())

    assert "PMR-04-LIFECYCLE-AUDIT-PREFLIGHT" in paper
    assert "Preflight is not approval." in paper
    assert "Audit candidate is not action." in paper
    assert "Sophia lifecycle audit is required before destructive action." in paper
    assert "User confirmation is required before destructive local action." in paper
    assert "No Sophia approval packet is emitted." in paper
    assert "No pruning or deletion occurs in PMR-04." in paper
    assert "pmr_lifecycle_audit_preflight_packet.json" in artifact_table
    assert "pmr_lifecycle_audit_no_action_receipt.json" in artifact_table
    assert "Run-PMR04-Acceptance.ps1" in quickstart
    assert status["pmr_04_indexed"] is True
    assert status["not_sophia_approval"] is True
    assert status["not_audit_action"] is True


def test_governed_validator_rejects_pmr_04_overclaims(tmp_path):
    root = Path("papers/governed_artifact_cognition")
    for claim in ("Sophia approval", "pruning execution", "deletion execution", "reward entitlement", "token economy", "memory write authorization", "deployment authority"):
        case = tmp_path / claim.replace(" ", "_")
        case.mkdir()
        for source in root.iterdir():
            if source.is_file():
                (case / source.name).write_text(source.read_text())
        paper = case / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text() + f"\nPMR-04 claims {claim}.\n")
        result = validate_publication_claims(
            paper,
            case / "reproducibility_appendix.md",
            case / "reviewer_quickstart.md",
            case / "status.json",
        )
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_overclaims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found, result


def test_governed_paper_includes_pmr_05_sophia_lifecycle_audit_review_boundaries():
    root = Path("papers/governed_artifact_cognition")
    paper = (root / "PUB_GOV_ARTIFACT_COG_01.md").read_text()
    artifact_table = (root / "artifact_table.md").read_text()
    quickstart = (root / "reviewer_quickstart.md").read_text()
    status = json.loads((root / "status.json").read_text())

    assert "PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW" in paper
    assert "Sophia review is not Sophia approval." in paper
    assert "Audit recommendation is not action." in paper
    assert "No Sophia approval packet is emitted." in paper
    assert "Destructive action requires future Sophia approval." in paper
    assert "Destructive action requires future user confirmation." in paper
    assert "No pruning or deletion occurs in PMR-05." in paper
    assert "pmr_sophia_lifecycle_audit_packet.json" in artifact_table
    assert "pmr_sophia_lifecycle_no_approval_receipt.json" in artifact_table
    assert "Run-PMR05-Acceptance.ps1" in quickstart
    assert status["pmr_05_indexed"] is True
    assert status["not_sophia_review_approval"] is True
    assert status["not_audit_recommendation_action"] is True


def test_governed_validator_rejects_pmr_05_overclaims(tmp_path):
    root = Path("papers/governed_artifact_cognition")
    for claim in ("Sophia approval", "pruning execution", "deletion execution", "reward entitlement"):
        case = tmp_path / claim.replace(" ", "_")
        case.mkdir()
        for source in root.iterdir():
            if source.is_file():
                (case / source.name).write_text(source.read_text())
        paper = case / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text() + f"\nPMR-05 claims {claim}.\n")
        result = validate_publication_claims(
            paper,
            case / "reproducibility_appendix.md",
            case / "reviewer_quickstart.md",
            case / "status.json",
        )
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_overclaims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found, result


def test_governed_paper_includes_pmr_06_user_confirmation_preflight_boundaries():
    root = Path("papers/governed_artifact_cognition")
    paper = (root / "PUB_GOV_ARTIFACT_COG_01.md").read_text()
    artifact_table = (root / "artifact_table.md").read_text()
    quickstart = (root / "reviewer_quickstart.md").read_text()
    status = json.loads((root / "status.json").read_text())

    assert "PMR-06-USER-CONFIRMATION-PREFLIGHT" in paper
    assert "User confirmation request is not user confirmation." in paper
    assert "User confirmation is not action." in paper
    assert "No user confirmation receipt is emitted." in paper
    assert "Destructive action requires future Sophia approval." in paper
    assert "Destructive action requires future user confirmation." in paper
    assert "No pruning or deletion occurs in PMR-06." in paper
    assert "pmr_user_confirmation_preflight_packet.json" in artifact_table
    assert "pmr_user_confirmation_no_action_receipt.json" in artifact_table
    assert "Run-PMR06-Acceptance.ps1" in quickstart
    assert status["pmr_06_indexed"] is True
    assert status["not_user_confirmation"] is True
    assert status["not_user_confirmation_receipt"] is True


def test_governed_validator_rejects_pmr_06_overclaims(tmp_path):
    root = Path("papers/governed_artifact_cognition")
    for claim in (
        "user confirmation execution",
        "user confirmation receipt",
        "pruning execution",
        "deletion execution",
        "reward entitlement",
    ):
        case = tmp_path / claim.replace(" ", "_")
        case.mkdir()
        for source in root.iterdir():
            if source.is_file():
                (case / source.name).write_text(source.read_text())
        paper = case / "PUB_GOV_ARTIFACT_COG_01.md"
        paper.write_text(paper.read_text() + f"\nPMR-06 claims {claim}.\n")
        result = validate_publication_claims(
            paper,
            case / "reproducibility_appendix.md",
            case / "reviewer_quickstart.md",
            case / "status.json",
        )
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_overclaims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found, result
