from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tools.validate_public_repro_dashboard import REQUIRED_PHASES as VALIDATOR_REQUIRED_PHASES
from tools.validate_public_repro_dashboard import validate_dashboard

BUILDER = Path("tools/build_public_repro_dashboard.py")
VALIDATOR = Path("tools/validate_public_repro_dashboard.py")
REQUIRED_JSON = {
    "experiment_suite_dashboard.json",
    "accepted_phase_matrix.json",
    "reproducibility_index.json",
    "claim_boundary_index.json",
    "artifact_index.json",
    "status.json",
}
REQUIRED_DOCS = {
    "index.md",
    "sonya-aegis-smoke-02.md",
    "wave-gold-physics.md",
    "uni02d-sonya-gate.md",
    "retro-lane-00.md",
    "governed-artifact-cognition-paper.md",
    "waveform-rosetta-paper.md",
    "reviewer-quickstart.md",
    "claim-boundaries.md",
    "public-utility-alpha.md",
    "raw-baseline-comparison.md",
    "evidence-review-pack.md",
    "rw-comp-01.md",
    "rw-comp-02.md",
    "retrosynthesis-sandbox-cycle.md",
    "evidence-review-pack-second-pass.md",
    "rw-comp-03.md",
    "universal-architecture.md",
    "sonya-adapter-contract-registry.md",
    "sonya-adapter-smoke.md",
    "sonya-local-fixture-adapter.md",
    "evidence-review-pack-local-adapter.md",
    "sonya-local-fixture-adapter-multi-route.md",
    "sonya-local-fixture-adapter-lineage.md",
}
REQUIRED_PHASES = {
    "EXP-SUITE-REGISTRY-01",
    "EXP-SUITE-REPRO-01",
    "WAVE-FAMILY-CLOSEOUT-01",
    "SONYA-INGRESS-HARDEN-03",
    "SOPHIA-UCC-ROUTE-01",
    "PUB-GOV-ARTIFACT-COG-01",
    "PUB-WAVE-ROSETTA-01",
    "UNI-02D-SONYA-GATE-01",
    "RETRO-LANE-00",
    "PUBLIC-UTILITY-ALPHA-00",
    "RAW-BASELINE-COMPARISON-00",
    "EVIDENCE-REVIEW-PACK-00",
    "RW-COMP-01",
    "RW-COMP-02",
    "RETROSYNTHESIS-SANDBOX-CYCLE-01",
    "EVIDENCE-REVIEW-PACK-01",
    "RW-COMP-03",
    "UNIVERSAL-STAGE-PIPELINE-00",
    "ARTIFACT-CONTRACT-REGISTRY-01",
    "UNIVERSAL-COMPATIBILITY-MATRIX-00",
    "SONYA-ADAPTER-CONTRACT-REGISTRY-01",
    "SONYA-ADAPTER-SMOKE-00",
    "SONYA-LOCAL-FIXTURE-ADAPTER-01",
    "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01",
    "SONYA-LOCAL-FIXTURE-ADAPTER-02",
    "SONYA-LOCAL-FIXTURE-ADAPTER-03",
}

REQUIRED_COMMAND_FRAGMENTS = (
    "Run-SONYA-AEGIS-SMOKE02-Acceptance.ps1",
    "Run-UNI02D-Sonya-Gate-Acceptance.ps1",
    "Run-RETRO-LANE00-Acceptance.ps1",
    "coherence.waveform.family_acceptance",
    "tests/test_ucc_risk_control_route.py",
    "Run-PUBLIC-UTILITY-ALPHA00-Acceptance.ps1",
    "Run-RAW-BASELINE-COMPARISON00-Acceptance.ps1",
    "Run-EVIDENCE-REVIEW-PACK00-Acceptance.ps1",
    "Run-RW-COMP01-Acceptance.ps1",
    "Run-RW-COMP02-Acceptance.ps1",
    "Run-RETROSYNTHESIS-SANDBOX-CYCLE01-Acceptance.ps1",
    "Run-EVIDENCE-REVIEW-PACK01-Acceptance.ps1",
    "Run-RW-COMP03-Acceptance.ps1",
    "test_universal_stage_pipeline.py",
    "test_artifact_contract_registry.py",
    "Run-UNIVERSAL-COMPATIBILITY-MATRIX00-Acceptance.ps1",
    "Run-SONYA-ADAPTER-CONTRACT-REGISTRY01-Acceptance.ps1",
    "Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1",
    "Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1",
    "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1",
    "Run-SONYA-LOCAL-FIXTURE-ADAPTER02-Acceptance.ps1",
    "Run-SONYA-LOCAL-FIXTURE-ADAPTER03-Acceptance.ps1",
)
STALE_COMMAND_FRAGMENTS = (
    "tests/test_sonya_aegis_smoke_02.py",
    "tests/test_wave_gold_physics_family.py",
    "scripts/build_experiment_suite_repro_pack.py",
    "test_retro_lane_00_acceptance.py",
    "test_sophia_ucc_route.py",
)


def run_builder(tmp_path: Path) -> tuple[Path, Path]:
    out_dir = tmp_path / "registry"
    docs_dir = tmp_path / "docs" / "experiment-suite"
    completed = subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--out-dir",
            str(out_dir),
            "--docs-dir",
            str(docs_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return out_dir, docs_dir


def test_builder_writes_all_registry_json_files(tmp_path):
    out_dir, _docs_dir = run_builder(tmp_path)
    assert REQUIRED_JSON <= {path.name for path in out_dir.glob("*.json")}


def test_builder_writes_all_docs_pages(tmp_path):
    _out_dir, docs_dir = run_builder(tmp_path)
    assert REQUIRED_DOCS <= {path.name for path in docs_dir.glob("*.md")}


def test_dashboard_contains_all_accepted_phases(tmp_path):
    out_dir, _docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert phase_ids == REQUIRED_PHASES
    assert dashboard["accepted_phase_count"] == 26


def test_dashboard_command_summaries_use_accepted_harnesses(tmp_path):
    out_dir, _docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    summaries = "\n".join(
        entry["reproduction_command_summary"] for entry in dashboard["accepted_phases"]
    )
    for fragment in REQUIRED_COMMAND_FRAGMENTS:
        assert fragment in summaries


def test_validator_required_phases_include_public_utility_alpha_raw_baseline_and_evidence_review_pack():
    assert "PUBLIC-UTILITY-ALPHA-00" in VALIDATOR_REQUIRED_PHASES
    assert "RAW-BASELINE-COMPARISON-00" in VALIDATOR_REQUIRED_PHASES
    assert "EVIDENCE-REVIEW-PACK-00" in VALIDATOR_REQUIRED_PHASES
    assert "RETROSYNTHESIS-SANDBOX-CYCLE-01" in VALIDATOR_REQUIRED_PHASES
    assert "EVIDENCE-REVIEW-PACK-01" in VALIDATOR_REQUIRED_PHASES
    assert "RW-COMP-03" in VALIDATOR_REQUIRED_PHASES
    assert "UNIVERSAL-STAGE-PIPELINE-00" in VALIDATOR_REQUIRED_PHASES
    assert "ARTIFACT-CONTRACT-REGISTRY-01" in VALIDATOR_REQUIRED_PHASES
    assert "UNIVERSAL-COMPATIBILITY-MATRIX-00" in VALIDATOR_REQUIRED_PHASES
    assert "SONYA-ADAPTER-CONTRACT-REGISTRY-01" in VALIDATOR_REQUIRED_PHASES
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-01" in VALIDATOR_REQUIRED_PHASES
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01" in VALIDATOR_REQUIRED_PHASES
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-02" in VALIDATOR_REQUIRED_PHASES


def test_public_utility_alpha_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()

    commands = json.dumps(reproducibility)
    assert "Run-PUBLIC-UTILITY-ALPHA00-Acceptance.ps1" in commands
    assert "PUBLIC-UTILITY-ALPHA-00" in artifact_index["phases"]
    assert "public_utility_alpha_review_packet.json" in artifact_index["phases"]["PUBLIC-UTILITY-ALPHA-00"]
    assert (docs_dir / "public-utility-alpha.md").exists()
    assert "Public Utility Alpha" in quickstart
    assert (
        "Public Utility Alpha is a local reviewer demo, not deployment authority."
        in claim_boundaries["boundaries"]
    )


def test_raw_baseline_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()

    commands = json.dumps(reproducibility)
    assert "Run-RAW-BASELINE-COMPARISON00-Acceptance.ps1" in commands
    assert "RAW-BASELINE-COMPARISON-00" in artifact_index["phases"]
    assert "raw_baseline_comparison_packet.json" in artifact_index["phases"]["RAW-BASELINE-COMPARISON-00"]
    assert "raw_baseline_comparison_00_acceptance_receipt.json" in artifact_index["phases"]["RAW-BASELINE-COMPARISON-00"]
    assert (docs_dir / "raw-baseline-comparison.md").exists()
    assert "Raw Baseline Comparison" in quickstart
    boundary_text = "\n".join(claim_boundaries["boundaries"]).lower()
    assert "not hallucination reduction proof" in boundary_text
    assert "not model quality benchmark" in boundary_text



def test_evidence_review_pack_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()

    commands = json.dumps(reproducibility)
    assert "Run-EVIDENCE-REVIEW-PACK00-Acceptance.ps1" in commands
    assert "EVIDENCE-REVIEW-PACK-00" in artifact_index["phases"]
    assert "evidence_review_pack_manifest.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-00"]
    assert "claim_evidence_map.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-00"]
    assert (docs_dir / "evidence-review-pack.md").exists()
    assert "Evidence Review Pack" in quickstart
    assert "AI review that shows its work" in boundaries
    boundary_text = "\n".join(claim_boundaries["boundaries"]).lower()
    for phrase in (
        "not legal advice",
        "not medical advice",
        "not tax advice",
        "not compliance certification",
    ):
        assert phrase in boundary_text


def test_rw_comp_01_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()

    commands = json.dumps(reproducibility)
    assert "Run-RW-COMP01-Acceptance.ps1" in commands
    assert "RW-COMP-01" in artifact_index["phases"]
    assert "rw_comp_01_packet.json" in artifact_index["phases"]["RW-COMP-01"]
    assert "rw_comp_01_acceptance_receipt.json" in artifact_index["phases"]["RW-COMP-01"]
    assert (docs_dir / "rw-comp-01.md").exists()
    assert "RW-COMP-01" in quickstart
    assert "rw-comp-01.md" in index
    assert "fixture-only comparison scaffold" in boundaries
    boundary_text = "\n".join(claim_boundaries["boundaries"]).lower()
    for phrase in (
        "not hallucination reduction proof",
        "not model superiority proof",
        "not model quality benchmark",
        "not professional advice",
        "not compliance certification",
    ):
        assert phrase in boundary_text


def test_rw_comp_02_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()

    commands = json.dumps(reproducibility)
    assert "Run-RW-COMP02-Acceptance.ps1" in commands
    assert "RW-COMP-02" in artifact_index["phases"]
    assert "rw_comp_02_packet.json" in artifact_index["phases"]["RW-COMP-02"]
    assert "rw_comp_02_fixture_manifest.json" in artifact_index["phases"]["RW-COMP-02"]
    assert "rw_comp_02_acceptance_receipt.json" in artifact_index["phases"]["RW-COMP-02"]
    assert (docs_dir / "rw-comp-02.md").exists()
    assert "RW-COMP-02" in quickstart
    assert "rw-comp-02.md" in index
    assert "deterministic multi-fixture comparison battery" in boundaries
    boundary_text = "\n".join(claim_boundaries["boundaries"]).lower()
    for phrase in (
        "not hallucination reduction proof",
        "not model superiority proof",
        "not model quality benchmark",
        "not professional advice",
        "not compliance certification",
    ):
        assert phrase in boundary_text


def test_retrosynthesis_sandbox_cycle_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "RETROSYNTHESIS-SANDBOX-CYCLE-01"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "bounded_retrosynthesis_candidate_repair_cycle"
    assert phase["dashboard_summary"]["candidate_repair_artifacts_emitted"] is True
    assert phase["dashboard_summary"]["canon_adoption_blocked"] is True
    commands = json.dumps(reproducibility)
    assert "Run-RETROSYNTHESIS-SANDBOX-CYCLE01-Acceptance.ps1" in commands
    assert "RETROSYNTHESIS-SANDBOX-CYCLE-01" in artifact_index["phases"]
    assert "retrosynthesis_sandbox_cycle_packet.json" in artifact_index["phases"]["RETROSYNTHESIS-SANDBOX-CYCLE-01"]
    assert "retrosynthesis_claim_map_revision_candidate.json" in artifact_index["phases"]["RETROSYNTHESIS-SANDBOX-CYCLE-01"]
    assert (docs_dir / "retrosynthesis-sandbox-cycle.md").exists()
    assert "Retrosynthesis Sandbox Cycle" in quickstart
    assert "retrosynthesis-sandbox-cycle.md" in index
    assert "candidate repair, not canon adoption" in boundaries
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    for phrase in (
        "not memory write",
        "not Publisher finalization",
        "not Omega detection",
        "not deployment authority",
        "not recursive self-improvement",
    ):
        assert phrase in boundary_text


def test_validator_fails_if_retrosynthesis_sandbox_cycle_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "canon adopted",
        "memory written",
        "final answer released",
        "Publisher finalized",
        "Omega detected",
        "deployment authorized",
        "publication claim authorized",
        "hallucination reduction proven",
        "model superiority proven",
        "recursive self-improvement achieved",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "retrosynthesis-sandbox-cycle.md"
        page.write_text(page.read_text() + f"\nRETROSYNTHESIS-SANDBOX-CYCLE-01 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        assert claim.lower() in result["forbidden_claims_found"], result


def test_evidence_review_pack_second_pass_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "EVIDENCE-REVIEW-PACK-01"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "bounded_second_pass_review_candidate_loop"
    assert phase["dashboard_summary"]["revision_candidates_emitted"] is True
    assert phase["dashboard_summary"]["candidate_only_status_preserved"] is True
    commands = json.dumps(reproducibility)
    assert "Run-EVIDENCE-REVIEW-PACK01-Acceptance.ps1" in commands
    assert "EVIDENCE-REVIEW-PACK-01" in artifact_index["phases"]
    assert "evidence_review_second_pass_packet.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-01"]
    assert "evidence_review_second_pass_review_packet.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-01"]
    assert "evidence_review_claim_map_revision_packet.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-01"]
    assert "evidence_review_uncertainty_revision_packet.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-01"]
    assert (docs_dir / "evidence-review-pack-second-pass.md").exists()
    assert "Evidence Review Pack second pass" in quickstart
    assert "evidence-review-pack-second-pass.md" in index
    assert "candidate revision, not accepted evidence" in boundaries
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    for phrase in (
        "not canon adoption",
        "not memory write",
        "not Publisher finalization",
        "not Omega detection",
    ):
        assert phrase in boundary_text


def test_validator_fails_if_evidence_review_pack_second_pass_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "claims accepted evidence",
        "claims canon adoption",
        "claims memory write",
        "claims final answer release",
        "claims Publisher finalization",
        "claims Omega detection",
        "deployment authorized",
        "publication claim authorized",
        "hallucination reduction proven",
        "model superiority proven",
        "claims recursive self-improvement",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "evidence-review-pack-second-pass.md"
        page.write_text(page.read_text() + f"\nEVIDENCE-REVIEW-PACK-01 {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result


def test_rw_comp_03_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "RW-COMP-03"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "heldout_blinded_fixture_scoring_scaffold"
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_heldout_blinded_fixture_scaffold"
    assert phase["dashboard_summary"]["second_pass_candidate_arm_present"] is True
    commands = json.dumps(reproducibility)
    assert "Run-RW-COMP03-Acceptance.ps1" in commands
    assert "RW-COMP-03" in artifact_index["phases"]
    for artifact in (
        "rw_comp_03_packet.json",
        "rw_comp_03_review_packet.json",
        "rw_comp_03_blind_labels.json",
        "rw_comp_03_scoring_rubric.json",
        "rw_comp_03_statistics_plan.json",
        "rw_comp_03_statistics_packet.json",
        "rw_comp_03_acceptance_receipt.json",
    ):
        assert artifact in artifact_index["phases"]["RW-COMP-03"]
    assert (docs_dir / "rw-comp-03.md").exists()
    assert "RW-COMP-03" in quickstart
    assert "rw-comp-03.md" in index
    assert "held-out blinded fixture scaffold" in boundaries
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    for phrase in (
        "not hallucination reduction proof",
        "not model superiority proof",
        "not live model evaluation",
        "not live human study",
    ):
        assert phrase in boundary_text


def test_validator_fails_if_rw_comp_03_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "hallucination reduction proof",
        "model superiority proof",
        "live model evaluation",
        "claims live human study",
        "claims accepted evidence",
        "deployment authorized",
        "production evaluation",
        "production ready",
        "recursive self-improvement achieved",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "rw-comp-03.md"
        page.write_text(page.read_text() + f"\nRW-COMP-03 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result



def test_universal_architecture_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "universal-architecture.md"

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "UNIVERSAL-STAGE-PIPELINE-00" in phase_ids
    assert "ARTIFACT-CONTRACT-REGISTRY-01" in phase_ids
    assert "UNIVERSAL-COMPATIBILITY-MATRIX-00" in phase_ids
    compatibility = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "UNIVERSAL-COMPATIBILITY-MATRIX-00"
    )
    assert compatibility["dashboard_summary"]["review_status"] == "accepted_as_universal_compatibility_scaffold"
    assert compatibility["dashboard_summary"]["unsupported_inputs_failed_closed_or_hash_only"] is True
    assert page.exists()
    page_text = page.read_text()
    assert "# Universal Architecture Scaffold" in page_text
    assert "The brain runs cognition stages; experiments configure those stages." in page_text
    assert "profiles are configuration" in page_text
    assert "experiments are configurations" in page_text
    assert "fail-closed receipts" in page_text
    assert "hash-only" in page_text
    assert "Universal Architecture Scaffold" in quickstart
    assert "The brain runs cognition stages; experiments configure those stages." in boundaries
    assert "universal-architecture.md" in index

    commands = json.dumps(reproducibility)
    assert "Run-UNIVERSAL-COMPATIBILITY-MATRIX00-Acceptance.ps1" in commands
    assert "test_universal_stage_pipeline.py" in commands
    assert "test_artifact_contract_registry.py" in commands
    assert "UNIVERSAL-COMPATIBILITY-MATRIX-00" in artifact_index["phases"]
    for artifact in (
        "universal_compatibility_matrix_packet.json",
        "universal_compatibility_matrix_review_packet.json",
        "universal_stage_input_compatibility_rows.jsonl",
        "universal_stage_failure_receipts.jsonl",
        "universal_compatibility_matrix_00_acceptance_receipt.json",
    ):
        assert artifact in artifact_index["phases"]["UNIVERSAL-COMPATIBILITY-MATRIX-00"]
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    for phrase in (
        "not product release",
        "not experiment result",
        "not benchmark result",
        "not hallucination reduction proof",
        "not deployment authority",
        "not recursive self-improvement",
    ):
        assert phrase in boundary_text


def test_validator_fails_if_universal_architecture_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "product release",
        "product released",
        "benchmark result",
        "benchmark proven",
        "hallucination reduction proof",
        "hallucination reduction proven",
        "model superiority proof",
        "model superiority proven",
        "deployment authorized",
        "final answer released",
        "recursive self-improvement achieved",
        "AI consciousness demonstrated",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "universal-architecture.md"
        page.write_text(page.read_text() + f"\nUniversal Architecture Scaffold claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result


def test_sonya_adapter_contract_registry_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "sonya-adapter-contract-registry.md"

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "SONYA-ADAPTER-CONTRACT-REGISTRY-01"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "architecture_scaffold"
    assert phase["product_posture"] == "versioned_sonya_adapter_contracts"
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_adapter_contract_registry_only"
    assert phase["dashboard_summary"]["adapter_count"] == 11
    assert phase["dashboard_summary"]["all_adapters_disabled_or_blocked"] is True
    assert phase["dashboard_summary"]["enabled_live_adapter_count"] == 0
    assert "Adapter capability is not adapter authorization." in phase["claim_allowed"]

    commands = json.dumps(reproducibility)
    assert "Run-SONYA-ADAPTER-CONTRACT-REGISTRY01-Acceptance.ps1" in commands
    assert "SONYA-ADAPTER-CONTRACT-REGISTRY-01" in artifact_index["phases"]
    for artifact in (
        "sonya_adapter_contract_registry_packet.json",
        "sonya_adapter_capability_matrix_packet.json",
        "sonya_adapter_consent_matrix_packet.json",
        "sonya_adapter_failure_policy_packet.json",
        "sonya_adapter_telemetry_requirements_packet.json",
        "sonya_adapter_provenance_training_policy_packet.json",
        "sonya_adapter_contract_registry_01_acceptance_receipt.json",
    ):
        assert artifact in artifact_index["phases"]["SONYA-ADAPTER-CONTRACT-REGISTRY-01"]

    assert page.exists()
    page_text = page.read_text()
    assert "# Sonya Adapter Contract Registry" in page_text
    assert "Adapter capability is not adapter authorization." in page_text
    assert "all adapters disabled or blocked" in page_text
    assert "raw output is forbidden" in page_text
    assert "candidate packet required" in page_text
    assert "failure receipts required" in page_text
    assert "provenance-training policy is present" in page_text
    assert "Sonya Adapter Contract Registry" in quickstart
    assert "sonya-adapter-contract-registry.md" in index
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Adapter capability is not adapter authorization" in boundaries
    assert "all adapters disabled or blocked" in boundary_text
    assert "not adapter execution" in boundary_text
    assert "not network authorization" in boundary_text



def test_sonya_adapter_smoke_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "sonya-adapter-smoke.md"

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "SONYA-ADAPTER-SMOKE-00"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "fixture_adapter_contract_smoke"
    assert phase["product_posture"] == "adapter_contract_smoke_without_live_execution"
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_fixture_adapter_contract_smoke"
    assert phase["dashboard_summary"]["adapter_contract_registry_bound"] is True
    assert phase["dashboard_summary"]["no_live_adapter_execution"] is True
    assert phase["dashboard_summary"]["no_network_calls"] is True
    assert phase["dashboard_summary"]["no_remote_provider_calls"] is True
    assert phase["dashboard_summary"]["raw_output_rejected_or_absent"] is True
    assert phase["dashboard_summary"]["candidate_packet_emitted_for_fixture_model"] is True
    assert "Sonya Adapter Smoke exercises contracts, not live adapters." in phase["claim_allowed"]
    assert "SONYA-ADAPTER-CONTRACT-REGISTRY-01" in phase["prerequisite_phases"]

    commands = json.dumps(reproducibility)
    assert "Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1" in commands
    assert "SONYA-ADAPTER-SMOKE-00" in artifact_index["phases"]
    for artifact in (
        "sonya_adapter_smoke_packet.json",
        "sonya_adapter_smoke_review_packet.json",
        "sonya_adapter_selection_packet.json",
        "sonya_adapter_consent_check_packet.json",
        "sonya_adapter_capability_check_packet.json",
        "sonya_adapter_failure_receipt.json",
        "sonya_adapter_telemetry_packet.json",
        "sonya_adapter_provenance_event_packet.json",
        "sonya_adapter_fixture_candidate_packet.json",
        "sonya_adapter_smoke_00_acceptance_receipt.json",
    ):
        assert artifact in artifact_index["phases"]["SONYA-ADAPTER-SMOKE-00"]

    assert page.exists()
    page_text = page.read_text()
    assert "# Sonya Adapter Smoke" in page_text
    assert "Sonya Adapter Smoke exercises contracts, not live adapters." in page_text
    assert "raw output rejected" in page_text
    assert "candidate packet" in page_text
    assert "failure receipts" in page_text
    assert "telemetry events" in page_text
    assert "provenance events" in page_text
    assert "Sonya Adapter Smoke" in quickstart
    assert "sonya-adapter-smoke.md" in index
    assert "exercises contracts, not live adapters" in boundaries
    assert "not live adapter execution" in boundaries
    assert "not network authorization" in boundaries
    assert "failure receipts" in boundaries
    assert "telemetry events" in boundaries
    assert "provenance events" in boundaries


def test_validator_required_phases_include_sonya_adapter_smoke():
    assert "SONYA-ADAPTER-SMOKE-00" in VALIDATOR_REQUIRED_PHASES


def test_sonya_local_fixture_adapter_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "sonya-local-fixture-adapter.md"

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "SONYA-LOCAL-FIXTURE-ADAPTER-01"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "local_fixture_adapter_execution"
    assert phase["product_posture"] == "deterministic_local_adapter_execution_without_live_network_or_provider"
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_local_fixture_adapter_execution"
    assert phase["dashboard_summary"]["adapter_contract_registry_bound"] is True
    assert phase["dashboard_summary"]["adapter_smoke_bound"] is True
    assert phase["dashboard_summary"]["local_fixture_adapter_execution_performed"] is True
    assert phase["dashboard_summary"]["no_live_adapter_execution"] is True
    assert phase["dashboard_summary"]["no_network_calls"] is True
    assert phase["dashboard_summary"]["no_remote_provider_calls"] is True
    assert phase["dashboard_summary"]["candidate_packets_emitted"] is True
    assert phase["dashboard_summary"]["failure_receipts_visible"] is True
    assert phase["dashboard_summary"]["telemetry_events_visible"] is True
    assert phase["dashboard_summary"]["provenance_events_visible"] is True
    assert phase["dashboard_summary"]["candidate_packet_count"] == 3
    assert phase["dashboard_summary"]["failure_receipt_count"] == 6
    assert "fixture_text_model_adapter" in phase["dashboard_summary"]["executed_local_adapter_ids"]
    assert "remote_provider_placeholder_adapter" in phase["dashboard_summary"]["blocked_adapter_ids"]
    assert "Sonya Local Fixture Adapter executes deterministic local fixtures, not live adapters." in phase["claim_allowed"]
    assert "SONYA-ADAPTER-CONTRACT-REGISTRY-01" in phase["prerequisite_phases"]
    assert "SONYA-ADAPTER-SMOKE-00" in phase["prerequisite_phases"]

    commands = json.dumps(reproducibility)
    assert "Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1" in commands
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-01" in artifact_index["phases"]
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
        assert artifact in artifact_index["phases"]["SONYA-LOCAL-FIXTURE-ADAPTER-01"]

    assert page.exists()
    page_text = page.read_text()
    assert "# Sonya Local Fixture Adapter" in page_text
    assert "executes deterministic local fixtures, not live adapters" in page_text
    assert "local fixture adapter execution occurred" in page_text
    assert "candidate packets" in page_text
    assert "failure receipts" in page_text
    assert "telemetry events" in page_text
    assert "provenance events" in page_text
    assert "Sonya Local Fixture Adapter" in quickstart
    assert "sonya-local-fixture-adapter.md" in index
    assert "executes deterministic local fixtures, not live adapters" in boundaries
    assert "not live adapter execution" in boundaries
    assert "not network authorization" in boundaries
    assert "candidate packets" in boundaries
    assert "failure receipts" in boundaries
    assert "telemetry events" in boundaries
    assert "provenance events" in boundaries


def test_validator_required_phases_include_sonya_local_fixture_adapter():
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-01" in VALIDATOR_REQUIRED_PHASES


def test_validator_fails_if_sonya_local_fixture_adapter_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "live adapter execution",
        "network authorization",
        "remote provider calls",
        "model weight training",
        "production readiness",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "sonya-local-fixture-adapter.md"
        page.write_text(page.read_text() + f"\nSonya Local Fixture Adapter claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result


def test_evidence_review_pack_local_adapter_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "evidence-review-pack-local-adapter.md"

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "local_adapter_candidate_review"
    assert phase["product_posture"] == "local_adapter_candidate_routed_through_evidence_review_pack"
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_local_adapter_candidate_review"
    assert phase["dashboard_summary"]["local_adapter_candidate_bound"] is True
    assert phase["dashboard_summary"]["evidence_review_pack_path_used"] is True
    assert phase["dashboard_summary"]["ucc_control_profile_applied"] is True
    assert phase["dashboard_summary"]["raw_output_rejected_or_absent"] is True
    assert phase["dashboard_summary"]["unsupported_claims_listed"] is True
    assert phase["dashboard_summary"]["provenance_events_visible"] is True
    assert "Adapter output is not accepted as cognition directly." in phase["claim_allowed"]
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-01" in phase["prerequisite_phases"]
    assert "EVIDENCE-REVIEW-PACK-00" in phase["prerequisite_phases"]

    commands = json.dumps(reproducibility)
    assert "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1" in commands
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01" in artifact_index["phases"]
    assert "evidence_review_local_adapter_route_packet.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01"]
    assert "evidence_review_local_adapter_claim_map.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01"]

    assert page.exists()
    page_text = page.read_text()
    assert "Adapter output is not accepted as cognition directly." in page_text
    assert "Candidate packets require UCC-controlled review." in page_text
    assert "The claim map is not truth certification." in page_text
    assert "The candidate is not final answer." in page_text
    assert "Evidence Review Pack local adapter" in quickstart
    assert "evidence-review-pack-local-adapter.md" in index
    assert "Adapter output is not accepted as cognition directly." in boundaries
    assert "not accepted evidence" in boundaries
    assert "not adapter authorization" in boundaries


def test_validator_required_phases_include_evidence_review_pack_local_adapter():
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01" in VALIDATOR_REQUIRED_PHASES


def test_validator_fails_if_evidence_review_pack_local_adapter_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "claims accepted evidence",
        "claims adapter authorization",
        "model weight training",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "evidence-review-pack-local-adapter.md"
        page.write_text(page.read_text() + f"\nEvidence Review Pack local-adapter route {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result


def test_sonya_local_fixture_adapter_multi_route_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "sonya-local-fixture-adapter-multi-route.md"

    phase = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "SONYA-LOCAL-FIXTURE-ADAPTER-02")
    assert phase["evidence_type"] == "multi_adapter_local_fixture_route"
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_multi_adapter_local_fixture_route"
    assert phase["dashboard_summary"]["local_adapter_candidates_compared"] is True
    assert phase["dashboard_summary"]["selection_policy_applied"] is True
    assert phase["dashboard_summary"]["selected_candidate_requires_review"] is True
    assert phase["dashboard_summary"]["candidate_count"] == 3
    assert phase["dashboard_summary"]["selected_candidate_id"] == "candidate-fixture-summary"
    assert "Selection policy is not final answer." in phase["claim_allowed"]

    assert "Run-SONYA-LOCAL-FIXTURE-ADAPTER02-Acceptance.ps1" in json.dumps(reproducibility)
    assert "sonya_local_adapter_multi_route_packet.json" in artifact_index["phases"]["SONYA-LOCAL-FIXTURE-ADAPTER-02"]
    assert page.exists()
    page_text = page.read_text()
    assert "Selection policy is not final answer." in page_text
    assert "candidate comparison is not model quality benchmark" in page_text.lower()
    assert "sonya-local-fixture-adapter-multi-route.md" in index
    assert "Selection policy is not final answer." in boundaries
    assert "not adapter authorization" in boundaries
    assert "not a model quality benchmark" in boundaries


def test_validator_required_phases_include_sonya_local_fixture_adapter_multi_route():
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-02" in VALIDATOR_REQUIRED_PHASES


def test_validator_fails_if_sonya_local_fixture_adapter_multi_route_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "final answer selection",
        "claims adapter authorization",
        "model quality benchmark",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "sonya-local-fixture-adapter-multi-route.md"
        page.write_text(page.read_text() + f"\nSonya Local Fixture Adapter multi-route claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result


def test_validator_fails_if_sonya_adapter_smoke_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "adapter execution",
        "adapter executed",
        "network authorization",
        "network authorized",
        "remote provider calls",
        "remote provider called",
        "model weight training",
        "model weights trained",
        "production readiness",
        "production ready",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "sonya-adapter-smoke.md"
        page.write_text(page.read_text() + f"\nSonya Adapter Smoke claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result

def test_validator_fails_if_sonya_adapter_contract_registry_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "adapter execution",
        "adapter executed",
        "network authorization",
        "network authorized",
        "remote provider called",
        "remote provider call",
        "model weight training",
        "model weights trained",
        "production readiness",
        "production ready",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "sonya-adapter-contract-registry.md"
        page.write_text(page.read_text() + f"\nSonya Adapter Contract Registry claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result

def test_public_dashboard_outputs_do_not_include_stale_placeholder_commands(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    output_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted([*out_dir.glob("*.json"), *docs_dir.rglob("*.md")])
    )
    for fragment in STALE_COMMAND_FRAGMENTS:
        assert fragment not in output_text


def test_claim_boundary_index_contains_non_authority_rules(tmp_path):
    out_dir, _docs_dir = run_builder(tmp_path)
    payload = json.loads((out_dir / "claim_boundary_index.json").read_text())
    text = "\n".join(payload["boundaries"]).lower()
    for phrase in (
        "route is not authorization",
        "receipt is not truth certification",
        "model candidate is not answer",
        "admission is not execution",
        "dashboard is not deployment authority",
    ):
        assert phrase in text


def test_validator_passes_clean_dashboard(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
    assert result["passed"] is True


def test_validator_fails_if_public_utility_alpha_phase_is_removed(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard_path = out_dir / "experiment_suite_dashboard.json"
    dashboard = json.loads(dashboard_path.read_text())
    dashboard["accepted_phases"] = [
        phase
        for phase in dashboard["accepted_phases"]
        if phase["phase_id"] != "PUBLIC-UTILITY-ALPHA-00"
    ]
    dashboard_path.write_text(json.dumps(dashboard), encoding="utf-8")
    result = validate_dashboard(dashboard_path, docs_dir)
    assert result["passed"] is False
    assert "PUBLIC-UTILITY-ALPHA-00" in result["missing_accepted_phases"]


def test_validator_fails_if_public_utility_alpha_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "deployment readiness",
        "truth certification",
        "final answer release",
        "live model execution",
        "federation",
        "retrosynthesis runtime",
        "Omega detection",
        "Publisher finalization",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        alpha = docs_dir / "public-utility-alpha.md"
        alpha.write_text(alpha.read_text() + f"\nPublic Utility Alpha claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        assert claim.lower() in result["forbidden_claims_found"], result


def test_validator_fails_if_raw_baseline_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "hallucination reduction proven",
        "model superiority proven",
        "model quality benchmark",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        raw = docs_dir / "raw-baseline-comparison.md"
        raw.write_text(raw.read_text() + f"\nRAW-BASELINE-COMPARISON-00 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        assert claim.lower() in result["forbidden_claims_found"], result



def test_validator_fails_if_evidence_review_pack_phase_is_removed(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard_path = out_dir / "experiment_suite_dashboard.json"
    dashboard = json.loads(dashboard_path.read_text())
    dashboard["accepted_phases"] = [
        phase
        for phase in dashboard["accepted_phases"]
        if phase["phase_id"] != "EVIDENCE-REVIEW-PACK-00"
    ]
    dashboard_path.write_text(json.dumps(dashboard), encoding="utf-8")
    result = validate_dashboard(dashboard_path, docs_dir)
    assert result["passed"] is False
    assert "EVIDENCE-REVIEW-PACK-00" in result["missing_accepted_phases"]


def test_validator_fails_if_evidence_review_pack_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "truth certified",
        "hallucination reduction proven",
        "legal advice",
        "medical advice",
        "tax advice",
        "compliance certification",
        "deployment authorized",
        "production evaluation",
        "production ready",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        pack = docs_dir / "evidence-review-pack.md"
        pack.write_text(pack.read_text() + f"\nEvidence Review Pack claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        assert claim.lower() in result["forbidden_claims_found"], result


def test_validator_fails_if_rw_comp_01_phase_is_removed(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard_path = out_dir / "experiment_suite_dashboard.json"
    dashboard = json.loads(dashboard_path.read_text())
    dashboard["accepted_phases"] = [
        phase
        for phase in dashboard["accepted_phases"]
        if phase["phase_id"] != "RW-COMP-01"
    ]
    dashboard_path.write_text(json.dumps(dashboard), encoding="utf-8")
    result = validate_dashboard(dashboard_path, docs_dir)
    assert result["passed"] is False
    assert "RW-COMP-01" in result["missing_accepted_phases"]


def test_validator_fails_if_rw_comp_01_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "hallucination reduction proof",
        "hallucination reduction proven",
        "model superiority proof",
        "model superiority proven",
        "professional advice",
        "compliance certification",
        "deployment authorized",
        "production evaluation",
        "production ready",
        "live model evaluation",
        "remote provider evaluation",
        "final answer released",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "rw-comp-01.md"
        page.write_text(page.read_text() + f"\nRW-COMP-01 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        assert claim.lower() in result["forbidden_claims_found"], result


def test_validator_fails_if_rw_comp_02_phase_is_removed(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard_path = out_dir / "experiment_suite_dashboard.json"
    dashboard = json.loads(dashboard_path.read_text())
    dashboard["accepted_phases"] = [
        phase
        for phase in dashboard["accepted_phases"]
        if phase["phase_id"] != "RW-COMP-02"
    ]
    dashboard_path.write_text(json.dumps(dashboard), encoding="utf-8")
    result = validate_dashboard(dashboard_path, docs_dir)
    assert result["passed"] is False
    assert "RW-COMP-02" in result["missing_accepted_phases"]


def test_validator_fails_if_rw_comp_02_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "hallucination reduction proof",
        "hallucination reduction proven",
        "model superiority proof",
        "model superiority proven",
        "professional advice",
        "compliance certification",
        "deployment authorized",
        "production evaluation",
        "production ready",
        "live model evaluation",
        "remote provider evaluation",
        "final answer released",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "rw-comp-02.md"
        page.write_text(page.read_text() + f"\nRW-COMP-02 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        assert claim.lower() in result["forbidden_claims_found"], result

def test_validator_fails_if_dashboard_claims_deployment_readiness(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard_path = out_dir / "experiment_suite_dashboard.json"
    dashboard = json.loads(dashboard_path.read_text())
    dashboard["deployment_ready"] = True
    dashboard_path.write_text(json.dumps(dashboard), encoding="utf-8")
    result = validate_dashboard(dashboard_path, docs_dir)
    assert result["passed"] is False
    assert "deployment_ready" in result["bad_truthy_flags"]


def test_validator_fails_if_dashboard_claims_truth_certification(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard_path = out_dir / "experiment_suite_dashboard.json"
    dashboard = json.loads(dashboard_path.read_text())
    dashboard["truth_certified"] = True
    dashboard_path.write_text(json.dumps(dashboard), encoding="utf-8")
    result = validate_dashboard(dashboard_path, docs_dir)
    assert result["passed"] is False
    assert "truth_certified" in result["bad_truthy_flags"]


def test_validator_fails_if_retro_lane_is_runtime_execution(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    retro = docs_dir / "retro-lane-00.md"
    retro.write_text(retro.read_text() + "\nRETRO-LANE-00 is described as retrosynthesis runtime.\n")
    result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
    assert result["passed"] is False
    assert "retrosynthesis runtime" in result["forbidden_claims_found"]


def test_validator_fails_if_uni02d_is_universal_portability_proof(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    uni = docs_dir / "uni02d-sonya-gate.md"
    uni.write_text(uni.read_text() + "\nUNI-02D is universal portability proof.\n")
    result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
    assert result["passed"] is False
    assert "universal portability proof" in result["forbidden_claims_found"]


def test_reviewer_quickstart_includes_command_groups(tmp_path):
    _out_dir, docs_dir = run_builder(tmp_path)
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    assert "CoherenceLattice commands" in quickstart
    assert "Sophia commands" in quickstart
    assert "uvlm-publications commands" in quickstart


def test_status_marks_draft_public_review_and_external_review(tmp_path):
    out_dir, _docs_dir = run_builder(tmp_path)
    status = json.loads((out_dir / "status.json").read_text())
    assert status["dashboard_id"] == "PUBLIC-REPRO-DASHBOARD-01"
    assert status["status"] == "draft_public_review"
    assert status["requires_external_peer_review"] is True


def test_validator_cli_passes(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    completed = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--dashboard",
            str(out_dir / "experiment_suite_dashboard.json"),
            "--docs-dir",
            str(docs_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_sonya_local_fixture_adapter_lineage_clarity_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "sonya-local-fixture-adapter-lineage.md"

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "SONYA-LOCAL-FIXTURE-ADAPTER-03"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "methods_lineage_clarity"
    assert phase["product_posture"] == "source_current_experiment_lineage_clarity"
    assert phase["dashboard_summary"]["lineage_review_status"] == "accepted_as_lineage_clarity_packet"
    assert phase["dashboard_summary"]["current_experiment_id"] == "SONYA-LOCAL-FIXTURE-ADAPTER-02"
    assert phase["dashboard_summary"]["source_fixture_experiment_id_present"] is True
    assert phase["dashboard_summary"]["source_fixture_role_present"] is True
    assert phase["dashboard_summary"]["nested_source_identity_explained"] is True
    assert phase["dashboard_summary"]["ambiguous_experiment_id_inheritance_blocked"] is True
    assert phase["dashboard_summary"]["lineage_complete"] is True
    assert phase["dashboard_summary"]["lineage_is_not_authority"] is True
    assert phase["dashboard_summary"]["promotion_blocked"] is True
    assert phase["dashboard_summary"]["source_fixture_reference_not_stale_identity"] is True
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-01" in phase["prerequisite_phases"]
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-02" in phase["prerequisite_phases"]
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01" in phase["prerequisite_phases"]

    commands = json.dumps(reproducibility)
    assert "Run-SONYA-LOCAL-FIXTURE-ADAPTER03-Acceptance.ps1" in commands
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-03" in artifact_index["phases"]
    assert "sonya_local_adapter_lineage_packet.json" in artifact_index["phases"]["SONYA-LOCAL-FIXTURE-ADAPTER-03"]
    assert "sonya_local_adapter_lineage_review_packet.json" in artifact_index["phases"]["SONYA-LOCAL-FIXTURE-ADAPTER-03"]

    assert page.exists()
    page_text = page.read_text()
    assert "Source fixture references are not stale identity leakage." in page_text
    assert "Nested SONYA-LOCAL-FIXTURE-ADAPTER-01 references are source fixture dependencies, not stale identity leakage." in page_text
    assert "Current route identity is explicit." in page_text
    assert "Source fixture identity is explicit." in page_text
    assert "Evidence Review Pack local-adapter route references are explicit." in page_text
    assert "Lineage does not grant authority." in page_text
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-03" in quickstart
    assert "sonya-local-fixture-adapter-lineage.md" in index
    assert "Source fixture references are not stale identity leakage." in boundaries


def test_validator_required_phases_include_sonya_local_fixture_adapter_lineage_clarity():
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-03" in VALIDATOR_REQUIRED_PHASES


def test_validator_fails_if_sonya_local_fixture_adapter_lineage_clarity_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "adapter execution",
        "lineage authority",
        "network authorization",
        "remote provider calls",
        "stale identity proof of execution",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "sonya-local-fixture-adapter-lineage.md"
        page.write_text(page.read_text() + f"\nSonya Local Fixture Adapter lineage claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found, result
