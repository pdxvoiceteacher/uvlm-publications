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
    assert dashboard["accepted_phase_count"] == 12


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
