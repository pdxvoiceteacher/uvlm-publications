from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

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
}


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
    assert dashboard["accepted_phase_count"] == 9


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
