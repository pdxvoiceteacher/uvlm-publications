from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tools.build_public_repro_dashboard import _dedupe_accepted_phases
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
    "sonya-required-membrane-checkpoint.md",
    "sonya-adapter-smoke.md",
    "sonya-local-fixture-adapter.md",
    "evidence-review-pack-local-adapter.md",
    "evidence-review-pack-local-adapter-revision.md",
    "rw-comp-local-adapter.md",
    "provenance-memory-reservoir.md",
    "pmr-local-artifact-index.md",
    "ontology-claim-registry.md",
    "pmr-provenance-coherence-utility.md",
    "pmr-lifecycle-state-machine.md",
    "pmr-lifecycle-audit-preflight.md",
    "pmr-sophia-lifecycle-audit-review.md",
    "pmr-destructive-action-authorization-preflight.md",
    "pmr-architecture-diversity-checkpoint.md",
    "pmr-simulation-baseline-comparison.md",
    "pmr-simulation-statistical-analysis.md",
    "pmr-federation-stress-corpus.md",
    "pmr-human-provenance-context.md",
    "sonya-local-fixture-adapter-multi-route.md",
    "sonya-local-fixture-adapter-lineage.md",
    "local-review-runtime-v0.md",
    "local-review-metrics-flow.md",
    "runtime-metrics-seed-corpus.md",
    "pmr-local-queryable-store.md",
    "retrosynthesis-readiness.md",
    "retrosynthesis-local-prototype.md",
    "atlas-local-memory-admission-readiness.md",
    "atlas-local-memory-admission-prototype.md",
    "local-test-proxy-review.md",
    "ai-context-performance-continuity.md",
    "theorem-validation-pathway.md",
    "coop-entropy-dividend.md",
    "triadic-llm-metrics-smoke.md",
    "ucc-sophia-control-forensics.md",
    "ucc-standards-source-registry-and-materiality.md",
    "triadic-llm-smoke-pmr-inventory-contract-repair.md",
    "ai-forensics-dossier.md",
    "human-review-ux.md",
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
    "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02",
    "RW-COMP-LOCAL-ADAPTER-01",
    "PMR-00-PROVENANCE-MEMORY-RESERVOIR",
    "PMR-01-LOCAL-ARTIFACT-INDEX",
    "PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY",
    "PMR-03-LIFECYCLE-STATE-MACHINE",
    "PMR-04-LIFECYCLE-AUDIT-PREFLIGHT",
    "PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW",
    "SPEC-FRESHNESS-REGISTRY-00",
    "FUNDAMENTAL-COHERENCE-METRICS-00",
    "PMR-06-USER-CONFIRMATION-PREFLIGHT",
    "PMR-07-USER-CONFIRMATION-NEGATIVE-CONTROL",
    "PMR-08-VALID-USER-CONFIRMATION-RECEIPT-SCAFFOLD",
    "PMR-09-DESTRUCTIVE-ACTION-AUTHORIZATION-NEGATIVE-CONTROL",
    "PMR-10-DESTRUCTIVE-ACTION-AUTHORIZATION-PREFLIGHT",
    "PMR-ARCH-DIVERSITY-CHECKPOINT-00",
    "PMR-SIM-00",
    "PMR-STAT-00",
    "PMR-FED-STRESS-00",
    "PMR-HUMAN-PROVENANCE-00",
    "PMR-HUMAN-CONSENT-NEGATIVE-CONTROL-00",
    "SONYA-LOCAL-FIXTURE-ADAPTER-02",
    "SONYA-LOCAL-FIXTURE-ADAPTER-03",
    "SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00",
    "TEL-EVENT-STACK-00",
    "EVIDENCE-REVIEW-PRODUCT-LOOP-02",
    "EVIDENCE-REVIEW-METRICS-00",
    "COGNITIVE-WATERS-PATTERN-METRICS-00",
    "ONTOLOGY-CLAIM-REGISTRY-00",
    "LOCAL-SONYA-PATH-PORTABILITY-00",
    "TB-PRODUCT-SLICE-00",
    "TB-PRODUCT-SLICE-01",
    "TB-PRODUCT-SLICE-02",
    "SONYA-LOCAL-SERVER-GATEWAY-00",
    "SONYA-LOCAL-SERVER-GATEWAY-01",
    "SONYA-LOCAL-SERVER-GATEWAY-02",
    "LOCAL-SERVER-USER-FILE-INGRESS-00",
    "LOCAL-SERVER-USER-FILE-INGRESS-01",
    "USER-FACING-RECEIPT-UX-01",
    "LOCAL-SERVER-USER-FILE-INGRESS-02",
    "LAN-READINESS-PREFLIGHT-00",
    "LAN-AUTHORITY-MODEL-00",
    "LAN-AUTHORITY-NEGATIVE-CONTROL-00",
    "LAN-OPERATOR-CONSENT-PREFLIGHT-00",
    "LOCAL-REVIEW-RUNTIME-V0",
    "PMR-CONTEXT-AVAILABILITY-LEDGER-00",
    "MET-LOCAL-00",
    "WAVE-ROSETTA-METRIC-CALIBRATION-00",
    "TAF-RUNTIME-00",
    "SONYA-METRIC-MEMBRANE-COVERAGE-00",
    "COHERENCE-METRIC-FORMULA-REGISTRY-00",
    "METRIC-BOUND-SOURCE-TAXONOMY-00",
    "FLOW-RUNTIME-00",
    "RUNTIME-METRICS-CORPUS-SEED-00",
    "PMR-LOCAL-RUNTIME-QUERYABLE-STORE-00",
    "RETROSYNTHESIS-READINESS-00",
    "RETROSYNTHESIS-LOCAL-PROTOTYPE-00",
    "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00",
    "ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00",
    "HUMAN-REVIEW-PROXY-LOCAL-TESTING-00",
    "AI-CONTEXT-PERFORMANCE-CONTINUITY-00",
    "THEOREM-VALIDATION-PATHWAY-00",
    "COOP-ENTROPY-DIVIDEND-00",
    "TRIADIC-LLM-METRICS-SMOKE-00",
    "UCC-SOPHIA-CONTROL-FORENSICS-00",
    "UCC-STANDARDS-SOURCE-REGISTRY-AND-MATERIALITY-00",
    "TRIADIC-LLM-SMOKE-PMR-INVENTORY-CONTRACT-REPAIR-REVISION",
    "AI-FORENSICS-DOSSIER-00",
    "HUMAN-REVIEW-UX-00",
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
    "Run-SONYA-REQUIRED-MEMBRANE-CHECKPOINT00-Acceptance.ps1",
    "Run-TEL-EVENT-STACK00-Acceptance.ps1",
    "Run-SONYA-ADAPTER-SMOKE00-Acceptance.ps1",
    "Run-SONYA-LOCAL-FIXTURE-ADAPTER01-Acceptance.ps1",
    "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER01-Acceptance.ps1",
    "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER02-Acceptance.ps1",
    "Run-RW-COMP-LOCAL-ADAPTER01-Acceptance.ps1",
    "Run-PMR00-Acceptance.ps1",
    "Run-PMR01-Acceptance.ps1",
    "Run-PMR02-Acceptance.ps1",
    "Run-PMR03-Acceptance.ps1",
    "Run-PMR04-Acceptance.ps1",
    "Run-PMR05-Acceptance.ps1",
    "Run-PMR06-Acceptance.ps1",
    "Run-PMR07-Acceptance.ps1",
    "Run-PMR08-Acceptance.ps1",
    "Run-PMR09-Acceptance.ps1",
    "Run-PMR10-Acceptance.ps1",
    "Run-PMR-ARCH-DIVERSITY-CHECKPOINT00-Acceptance.ps1",
    "Run-PMR-SIM00-Acceptance.ps1",
    "Run-PMR-STAT00-Acceptance.ps1",
    "Run-PMR-FED-STRESS00-Acceptance.ps1",
    "Run-PMR-HUMAN-PROVENANCE00-Acceptance.ps1",
    "Run-SONYA-LOCAL-FIXTURE-ADAPTER02-Acceptance.ps1",
    "Run-SONYA-LOCAL-FIXTURE-ADAPTER03-Acceptance.ps1",
    "Run-SONYA-LOCAL-SERVER-GATEWAY00-Acceptance.ps1",
    "Run-SONYA-LOCAL-SERVER-GATEWAY01-Acceptance.ps1",
    "Run-SONYA-LOCAL-SERVER-GATEWAY02-Acceptance.ps1",
    "Run-LOCAL-SERVER-USER-FILE-INGRESS00-Acceptance.ps1",
    "Run-LOCAL-SERVER-USER-FILE-INGRESS01-Acceptance.ps1",
    "Run-PMR-CONTEXT-AVAILABILITY-LEDGER00-Acceptance.ps1",
    "build_runtime_metrics_seed_corpus",
    "Run-PMR-LOCAL-RUNTIME-QUERYABLE-STORE00-Acceptance.ps1",
    "build_pmr_local_query_store",
    "Run-RETROSYNTHESIS-READINESS00-Acceptance.ps1",
    "build_retrosynthesis_readiness_assessment",
    "build_retrosynthesis_local_prototype",
    "Run-ATLAS-LOCAL-MEMORY-ADMISSION-READINESS00-Acceptance.ps1",
    "build_atlas_local_memory_admission_readiness",
    "build_atlas_local_memory_admission_prototype",
    "build_local_test_proxy_review_receipt",
    "build_ai_context_performance_continuity",
    "build_theorem_validation_pathway",
    "build_triadic_llm_metrics_smoke",
    "build_sophia_ucc_control_review",
    "build_ucc_standards_source_registry",
    "build_ucc_materiality_profile",
    "build_ucc_materiality_override_receipt",
    "atlas_local_memory_admission_readiness",
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


def test_dedupe_accepted_phases_preserves_order_and_lets_later_entries_win():
    phases = [
        {"phase_id": "PHASE-A", "primary_artifacts": ["old.json"], "status": "accepted"},
        {"phase_id": "PHASE-B", "primary_artifacts": ["b.json"], "status": "accepted"},
        {"phase_id": "PHASE-A", "primary_artifacts": ["new.json"], "status": "accepted"},
    ]

    deduped = _dedupe_accepted_phases(phases)

    assert [phase["phase_id"] for phase in deduped] == ["PHASE-A", "PHASE-B"]
    assert len(deduped) == 2
    assert deduped[0]["primary_artifacts"] == ["new.json"]


def test_dashboard_contains_all_accepted_phases(tmp_path):
    out_dir, _docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    accepted_phases = dashboard["accepted_phases"]
    phase_ids = {entry["phase_id"] for entry in accepted_phases}
    assert len(accepted_phases) == len(phase_ids)
    assert phase_ids == REQUIRED_PHASES
    assert dashboard["accepted_phase_count"] == len(REQUIRED_PHASES)


def test_artifact_index_contains_all_accepted_phases(tmp_path):
    out_dir, _docs_dir = run_builder(tmp_path)
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())

    assert REQUIRED_PHASES <= set(artifact_index["phases"])


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
    assert "PMR-09-DESTRUCTIVE-ACTION-AUTHORIZATION-NEGATIVE-CONTROL" in VALIDATOR_REQUIRED_PHASES
    assert "PMR-10-DESTRUCTIVE-ACTION-AUTHORIZATION-PREFLIGHT" in VALIDATOR_REQUIRED_PHASES
    assert "PMR-ARCH-DIVERSITY-CHECKPOINT-00" in VALIDATOR_REQUIRED_PHASES


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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result



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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


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
    assert "PMR-09-DESTRUCTIVE-ACTION-AUTHORIZATION-NEGATIVE-CONTROL" in VALIDATOR_REQUIRED_PHASES


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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result

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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result

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


def test_validator_rejects_explicit_federation_punctuation_overclaims(tmp_path):
    for claim in ("Public Utility Alpha claims federation.", "Public Utility Alpha claims federation,"):
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_").replace(",", "comma").replace(".", "period"))
        alpha = docs_dir / "public-utility-alpha.md"
        alpha.write_text(alpha.read_text() + f"\n{claim}\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        assert "federation" in result["forbidden_claims_found"]



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
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_evidence_review_pack_local_adapter_revision_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "evidence-review-pack-local-adapter-revision.md"

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02"
    )
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "local_adapter_revision_loop"
    assert phase["product_posture"] == "candidate_revision_loop_with_structural_review_deltas"
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_local_adapter_revision_loop"
    assert phase["dashboard_summary"]["revise_summary_recommendation_consumed"] is True
    assert phase["dashboard_summary"]["revised_candidate_emitted"] is True
    assert phase["dashboard_summary"]["evidence_review_rerun_performed"] is True
    assert phase["dashboard_summary"]["deltas_reported"] is True
    assert phase["dashboard_summary"]["candidate_remains_not_final_answer"] is True
    assert phase["dashboard_summary"]["candidate_remains_not_accepted_evidence"] is True
    assert phase["dashboard_summary"]["unsupported_claim_count_delta"] == -1
    assert phase["dashboard_summary"]["uncertainty_missing_count_delta"] == -1
    assert phase["dashboard_summary"]["source_reference_visibility_delta"] == 1
    assert phase["dashboard_summary"]["structural_visibility_improved_candidate"] is True
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-01" in phase["prerequisite_phases"]
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-03" in phase["prerequisite_phases"]

    commands = json.dumps(reproducibility)
    assert "Run-EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER02-Acceptance.ps1" in commands
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02" in artifact_index["phases"]
    assert "evidence_review_local_adapter_revision_packet.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02"]
    assert "evidence_review_local_adapter_revision_delta.json" in artifact_index["phases"]["EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02"]

    assert page.exists()
    page_text = page.read_text()
    assert "Deltas are structural review descriptors, not hallucination reduction proof." in page_text
    assert "The revised candidate is not final answer and not accepted evidence." in page_text
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02" in quickstart
    assert "evidence-review-pack-local-adapter-revision.md" in index
    assert "Deltas are structural review descriptors, not hallucination reduction proof." in boundaries
    assert "Evidence Review Pack local-adapter revision loop is not model quality benchmark." in boundaries
    assert "Evidence Review Pack local-adapter revision loop is not final answer selection." in boundaries


def test_validator_required_phases_include_evidence_review_pack_local_adapter_revision():
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02" in VALIDATOR_REQUIRED_PHASES


def test_validator_fails_if_evidence_review_pack_local_adapter_revision_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "hallucination reduction proof",
        "model quality benchmark",
        "claims accepted evidence",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "evidence-review-pack-local-adapter-revision.md"
        page.write_text(page.read_text() + f"\nRevision loop claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_rw_comp_local_adapter_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    quickstart = (docs_dir / "reviewer-quickstart.md").read_text()
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    page = docs_dir / "rw-comp-local-adapter.md"

    phase = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "RW-COMP-LOCAL-ADAPTER-01")
    assert phase["status"] == "accepted"
    assert phase["evidence_type"] == "local_adapter_comparison_scaffold"
    assert phase["product_posture"] == "original_vs_revised_local_adapter_candidate_structural_review_delta"
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_local_adapter_comparison_scaffold"
    assert phase["dashboard_summary"]["all_comparison_arms_present"] is True
    assert phase["dashboard_summary"]["original_and_revised_candidates_compared"] is True
    assert phase["dashboard_summary"]["evidence_review_path_used_for_reviewed_arms"] is True
    assert phase["dashboard_summary"]["structural_visibility_descriptors_only"] is True
    assert phase["dashboard_summary"]["comparison_is_not_hallucination_reduction_proof"] is True
    assert phase["dashboard_summary"]["comparison_is_not_model_quality_benchmark"] is True
    assert phase["dashboard_summary"]["comparison_is_not_final_answer_selection"] is True
    assert phase["dashboard_summary"]["unsupported_claim_count_delta"] == -1
    assert phase["dashboard_summary"]["uncertainty_missing_count_delta"] == -1
    assert phase["dashboard_summary"]["source_reference_visibility_delta"] == 1
    assert phase["dashboard_summary"]["supported_claim_count_delta"] == 2
    assert "EVIDENCE-REVIEW-PACK-LOCAL-ADAPTER-02" in phase["prerequisite_phases"]
    assert "SONYA-LOCAL-FIXTURE-ADAPTER-02" in phase["prerequisite_phases"]

    commands = json.dumps(reproducibility)
    assert "Run-RW-COMP-LOCAL-ADAPTER01-Acceptance.ps1" in commands
    assert "RW-COMP-LOCAL-ADAPTER-01" in artifact_index["phases"]
    assert "rw_comp_local_adapter_packet.json" in artifact_index["phases"]["RW-COMP-LOCAL-ADAPTER-01"]
    assert "rw_comp_local_adapter_delta_packet.json" in artifact_index["phases"]["RW-COMP-LOCAL-ADAPTER-01"]

    assert page.exists()
    page_text = page.read_text()
    assert "Deltas are structural review descriptors only." in page_text
    assert "Candidate comparison is not final answer selection." in page_text
    assert "RW-COMP-LOCAL-ADAPTER-01" in quickstart
    assert "rw-comp-local-adapter.md" in index
    assert "Deltas are structural review descriptors only." in boundaries
    assert "RW-COMP local-adapter comparison is not hallucination reduction proof or a model quality benchmark." in boundaries
    assert "RW-COMP local-adapter comparison is not final answer selection." in boundaries


def test_validator_required_phases_include_rw_comp_local_adapter():
    assert "RW-COMP-LOCAL-ADAPTER-01" in VALIDATOR_REQUIRED_PHASES


def test_validator_fails_if_rw_comp_local_adapter_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "hallucination reduction proof",
        "model quality benchmark",
        "final answer selection",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "rw-comp-local-adapter.md"
        page.write_text(page.read_text() + f"\nRW-COMP local adapter claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_doctrine_and_local_artifact_index_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    boundaries = (docs_dir / "claim-boundaries.md").read_text()
    index = (docs_dir / "index.md").read_text()
    pmr00_page = docs_dir / "provenance-memory-reservoir.md"
    pmr01_page = docs_dir / "pmr-local-artifact-index.md"

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-00-PROVENANCE-MEMORY-RESERVOIR" in phase_ids
    assert "PMR-01-LOCAL-ARTIFACT-INDEX" in phase_ids
    pmr00 = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "PMR-00-PROVENANCE-MEMORY-RESERVOIR")
    pmr01 = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "PMR-01-LOCAL-ARTIFACT-INDEX")
    assert pmr00["dashboard_summary"]["review_status"] == "accepted_as_pmr_doctrine_and_policy_scaffold"
    assert pmr00["dashboard_summary"]["local_budget_policy_present"] is True
    assert pmr00["dashboard_summary"]["hash_encryption_distinction_present"] is True
    assert pmr00["dashboard_summary"]["federation_blocked_by_default"] is True
    assert pmr01["dashboard_summary"]["review_status"] == "accepted_as_pmr_local_artifact_index_scaffold"
    assert pmr01["dashboard_summary"]["artifact_count"] == 8
    assert pmr01["dashboard_summary"]["node_count"] == 8
    assert pmr01["dashboard_summary"]["edge_count"] == 9
    assert pmr01["dashboard_summary"]["graph_is_not_canon_graph"] is True

    commands = json.dumps(reproducibility)
    assert "Run-PMR00-Acceptance.ps1" in commands
    assert "Run-PMR01-Acceptance.ps1" in commands
    assert "pmr_doctrine_packet.json" in artifact_index["phases"]["PMR-00-PROVENANCE-MEMORY-RESERVOIR"]
    assert "pmr_local_artifact_index.json" in artifact_index["phases"]["PMR-01-LOCAL-ARTIFACT-INDEX"]
    assert "pmr_dependency_graph.json" in artifact_index["phases"]["PMR-01-LOCAL-ARTIFACT-INDEX"]
    assert pmr00_page.exists()
    assert pmr01_page.exists()
    assert "provenance-memory-reservoir.md" in index
    assert "pmr-local-artifact-index.md" in index
    assert "Memory is governed provenance under resource constraints." in boundaries
    assert "Hash is not encryption." in boundaries


def test_validator_required_phases_include_pmr_phases():
    assert "PMR-00-PROVENANCE-MEMORY-RESERVOIR" in VALIDATOR_REQUIRED_PHASES
    assert "PMR-01-LOCAL-ARTIFACT-INDEX" in VALIDATOR_REQUIRED_PHASES
    assert "PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY" in VALIDATOR_REQUIRED_PHASES
    assert "PMR-03-LIFECYCLE-STATE-MACHINE" in VALIDATOR_REQUIRED_PHASES
    assert "PMR-04-LIFECYCLE-AUDIT-PREFLIGHT" in VALIDATOR_REQUIRED_PHASES
    assert "PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW" in VALIDATOR_REQUIRED_PHASES


def test_validator_fails_if_pmr_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "Atlas canon",
        "memory write authorization",
        "federation authorization",
        "resource economy",
        "token economy",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "provenance-memory-reservoir.md"
        page.write_text(page.read_text() + f"\nPMR claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_02_gpcu_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR02-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-02-GLOBAL-PROVENANCE-COHERENCE-UTILITY"]
    assert "pmr_provenance_coherence_utility_packet.json" in artifacts
    assert "pmr_artifact_utility_scores.jsonl" in artifacts
    assert "pmr_lifecycle_recommendation_packet.json" in artifacts
    assert (docs_dir / "pmr-provenance-coherence-utility.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "GPCU is lifecycle/storage utility, not truth score." in boundary_text
    assert "GPCU is not reward entitlement." in boundary_text
    assert "GPCU is not token economy." in boundary_text


def test_validator_fails_if_pmr_02_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "truth score",
        "reward entitlement",
        "token economy",
        "pruning execution",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-provenance-coherence-utility.md"
        page.write_text(page.read_text() + f"\nPMR-02 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_03_lifecycle_state_machine_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-03-LIFECYCLE-STATE-MACHINE" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR03-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-03-LIFECYCLE-STATE-MACHINE"]
    assert "pmr_lifecycle_state_machine_packet.json" in artifacts
    assert "pmr_lifecycle_no_action_receipt.json" in artifacts
    assert "pmr_lifecycle_transition_candidates.jsonl" in artifacts
    assert (docs_dir / "pmr-lifecycle-state-machine.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Recommendation is not transition." in boundary_text
    assert "Transition candidate is not action." in boundary_text


def test_validator_fails_if_pmr_03_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "pruning execution",
        "deletion execution",
        "reward entitlement",
        "token economy",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-lifecycle-state-machine.md"
        page.write_text(page.read_text() + f"\nPMR-03 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_04_lifecycle_audit_preflight_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-04-LIFECYCLE-AUDIT-PREFLIGHT" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR04-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-04-LIFECYCLE-AUDIT-PREFLIGHT"]
    assert "pmr_lifecycle_audit_preflight_packet.json" in artifacts
    assert "pmr_lifecycle_audit_candidates.jsonl" in artifacts
    assert "pmr_lifecycle_audit_no_action_receipt.json" in artifacts
    assert (docs_dir / "pmr-lifecycle-audit-preflight.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Preflight is not approval." in boundary_text
    assert "Audit candidate is not action." in boundary_text


def test_validator_fails_if_pmr_04_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "Sophia approval",
        "pruning execution",
        "deletion execution",
        "reward entitlement",
        "token economy",
        "memory write authorization",
        "deployment authority",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-lifecycle-audit-preflight.md"
        page.write_text(page.read_text() + f"\nPMR-04 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_05_sophia_lifecycle_audit_review_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR05-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-05-SOPHIA-LIFECYCLE-AUDIT-REVIEW"]
    assert "pmr_sophia_lifecycle_audit_packet.json" in artifacts
    assert "pmr_sophia_lifecycle_no_approval_receipt.json" in artifacts
    assert "pmr_sophia_lifecycle_audit_rows.jsonl" in artifacts
    assert (docs_dir / "pmr-sophia-lifecycle-audit-review.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Sophia review is not Sophia approval." in boundary_text
    assert "Audit recommendation is not action." in boundary_text


def test_validator_fails_if_pmr_05_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "Sophia approval",
        "pruning execution",
        "deletion execution",
        "reward entitlement",
        "token economy",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-sophia-lifecycle-audit-review.md"
        page.write_text(page.read_text() + f"\nPMR-05 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_06_user_confirmation_preflight_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-06-USER-CONFIRMATION-PREFLIGHT" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR06-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-06-USER-CONFIRMATION-PREFLIGHT"]
    assert "pmr_user_confirmation_preflight_packet.json" in artifacts
    assert "pmr_user_confirmation_no_action_receipt.json" in artifacts
    assert "pmr_user_confirmation_prompt_packet.json" in artifacts
    assert (docs_dir / "pmr-user-confirmation-preflight.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "User confirmation request is not user confirmation." in boundary_text
    assert "User confirmation is not action." in boundary_text


def test_validator_fails_if_pmr_06_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "user confirmation execution",
        "user confirmation receipt",
        "pruning execution",
        "deletion execution",
        "reward entitlement",
        "token economy",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-user-confirmation-preflight.md"
        page.write_text(page.read_text() + f"\nPMR-06 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_07_user_confirmation_negative_control_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-07-USER-CONFIRMATION-NEGATIVE-CONTROL" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR07-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-07-USER-CONFIRMATION-NEGATIVE-CONTROL"]
    assert "pmr_user_confirmation_negative_control_packet.json" in artifacts
    assert "pmr_invalid_user_confirmation_attempts.jsonl" in artifacts
    assert "pmr_user_confirmation_negative_control_no_action_receipt.json" in artifacts
    assert (docs_dir / "pmr-user-confirmation-negative-control.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Invalid confirmation is not confirmation." in boundary_text
    assert "Scope-mismatched confirmation is not confirmation." in boundary_text


def test_validator_fails_if_pmr_07_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "valid user confirmation",
        "user confirmation receipt",
        "pruning execution",
        "deletion execution",
        "reward entitlement",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-user-confirmation-negative-control.md"
        page.write_text(page.read_text() + f"\nPMR-07 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_08_valid_user_confirmation_receipt_scaffold_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-08-VALID-USER-CONFIRMATION-RECEIPT-SCAFFOLD" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR08-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-08-VALID-USER-CONFIRMATION-RECEIPT-SCAFFOLD"]
    assert "pmr_valid_user_confirmation_receipt_packet.json" in artifacts
    assert "pmr_valid_user_confirmation_receipts.jsonl" in artifacts
    assert "pmr_user_confirmation_receipt_no_action_receipt.json" in artifacts
    assert (docs_dir / "pmr-user-confirmation-receipt-scaffold.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Valid user confirmation receipt is not action." in boundary_text
    assert "Confirmation authorizes eligibility for later action review, not action itself." in boundary_text


def test_pmr_09_destructive_action_authorization_negative_control_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-09-DESTRUCTIVE-ACTION-AUTHORIZATION-NEGATIVE-CONTROL" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR09-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-09-DESTRUCTIVE-ACTION-AUTHORIZATION-NEGATIVE-CONTROL"]
    assert "pmr_destructive_action_authorization_negative_control_packet.json" in artifacts
    assert "pmr_invalid_destructive_action_authorization_attempts.jsonl" in artifacts
    assert "pmr_destructive_action_authorization_no_action_receipt.json" in artifacts
    assert (docs_dir / "pmr-destructive-action-authorization-negative-control.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Valid confirmation receipt plus Sophia recommendation is not action authorization." in boundary_text
    assert "Explicit future action request and Sophia approval packet are required before destructive action." in boundary_text


def test_pmr_10_destructive_action_authorization_preflight_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    phase_ids = {entry["phase_id"] for entry in dashboard["accepted_phases"]}
    assert "PMR-10-DESTRUCTIVE-ACTION-AUTHORIZATION-PREFLIGHT" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR10-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-10-DESTRUCTIVE-ACTION-AUTHORIZATION-PREFLIGHT"]
    assert "pmr_destructive_action_authorization_preflight_packet.json" in artifacts
    assert "pmr_explicit_action_request_candidates.jsonl" in artifacts
    assert "pmr_sophia_approval_request_candidates.jsonl" in artifacts
    assert "pmr_destructive_action_authorization_preflight_no_action_receipt.json" in artifacts
    assert (docs_dir / "pmr-destructive-action-authorization-preflight.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Action request candidate is not explicit action request." in boundary_text
    assert "Sophia approval request candidate is not Sophia approval." in boundary_text
    assert "Authorization preflight is not authorization." in boundary_text


def test_pmr_architecture_diversity_checkpoint_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    accepted_phases = dashboard["accepted_phases"]
    phase_ids = {entry["phase_id"] for entry in accepted_phases}
    assert len(accepted_phases) == len(phase_ids)
    assert "PMR-ARCH-DIVERSITY-CHECKPOINT-00" in phase_ids
    commands = json.dumps(reproducibility)
    assert "Run-PMR-ARCH-DIVERSITY-CHECKPOINT00-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-ARCH-DIVERSITY-CHECKPOINT-00"]
    assert "pmr_architecture_diversity_checkpoint_packet.json" in artifacts
    assert "pmr_architecture_coverage_map.json" in artifacts
    assert "pmr_architecture_gap_register.json" in artifacts
    assert "pmr_next_lane_recommendation_packet.json" in artifacts
    assert (docs_dir / "pmr-architecture-diversity-checkpoint.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "PMR authorization ladder is not the whole Triadic Brain." in boundary_text
    assert "Pattern diversity is required." in boundary_text
    assert "Checkpoint recommendation is not execution." in boundary_text


def test_validator_fails_if_pmr_architecture_diversity_checkpoint_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "product completion",
        "runtime authority",
        "pruning execution",
        "deletion execution",
        "reward entitlement",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-architecture-diversity-checkpoint.md"
        page.write_text(page.read_text() + f"\nPMR-ARCH-DIVERSITY-CHECKPOINT-00 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_validator_fails_if_pmr_10_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "explicit action request",
        "Sophia approval packet",
        "destructive action authorization",
        "pruning execution",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-destructive-action-authorization-preflight.md"
        page.write_text(page.read_text() + f"\nPMR-10 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_validator_fails_if_pmr_09_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "destructive action authorization",
        "explicit action request",
        "Sophia approval packet",
        "destructive action receipt",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-destructive-action-authorization-negative-control.md"
        page.write_text(page.read_text() + f"\nPMR-09 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_validator_fails_if_pmr_08_makes_forbidden_claims(tmp_path):
    forbidden_claims = (
        "destructive action",
        "pruning execution",
        "deletion execution",
        "reward entitlement",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-user-confirmation-receipt-scaffold.md"
        page.write_text(page.read_text() + f"\nPMR-08 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        forbidden_found = [found.lower() for found in result["forbidden_claims_found"]]
        assert claim.lower() in forbidden_found or f"claims {claim.lower()}" in forbidden_found, result


def test_pmr_sim_00_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    accepted_phases = dashboard["accepted_phases"]
    phase_ids = [entry["phase_id"] for entry in accepted_phases]
    assert len(phase_ids) == len(set(phase_ids))
    assert "PMR-SIM-00" in phase_ids
    phase = next(entry for entry in accepted_phases if entry["phase_id"] == "PMR-SIM-00")
    assert phase["evidence_type"] == "simulation_scaffold"
    assert phase["dashboard_summary"]["pmr_policy_allowed_to_lose"] is True
    assert phase["dashboard_summary"]["production_policy_selected"] is False
    assert phase["claim_allowed"] == "PMR-SIM-00 demonstrates a deterministic synthetic fixture simulation scaffold comparing PMR-GPCU-style retention against simpler baselines while preserving non-production and non-authority boundaries."

    commands = json.dumps(reproducibility)
    assert "Run-PMR-SIM00-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-SIM-00"]
    assert "pmr_simulation_manifest.json" in artifacts
    assert "pmr_simulation_result_rows.jsonl" in artifacts
    assert "pmr_simulation_comparison_packet.json" in artifacts
    assert "pmr_simulation_statistics_packet.json" in artifacts
    assert (docs_dir / "pmr-simulation-baseline-comparison.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "PMR becomes scientific only when it can lose." in boundary_text
    assert "PMR policy is allowed to lose." in boundary_text
    assert "Simulation result is not production memory policy." in boundary_text


def test_dashboard_validator_rejects_pmr_sim_00_overclaims(tmp_path):
    for claim in (
        "PMR superiority proof",
        "production memory policy",
        "hallucination reduction proof",
        "federation proof",
        "reward economy proof",
    ):
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "pmr-simulation-baseline-comparison.md"
        page.write_text(page.read_text() + f"\nPMR-SIM-00 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_claims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found, result



def test_pmr_stat_00_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    accepted_phases = dashboard["accepted_phases"]
    phase_ids = [entry["phase_id"] for entry in accepted_phases]
    assert len(phase_ids) == len(set(phase_ids))
    assert "PMR-STAT-00" in phase_ids
    phase = next(entry for entry in accepted_phases if entry["phase_id"] == "PMR-STAT-00")
    assert phase["evidence_type"] == "analysis_scaffold"
    assert phase["dashboard_summary"]["descriptive_statistics_only"] is True
    assert phase["dashboard_summary"]["rank_table_not_production_policy_selection"] is True
    assert phase["dashboard_summary"]["production_policy_selected"] is False
    assert phase["claim_allowed"] == "PMR-STAT-00 demonstrates descriptive fixture-bound statistical analysis over PMR-SIM-00 outputs, including policy metric summaries, pair deltas, rank tables, sensitivity summaries, and failure-mode summaries, while preserving non-production and non-authority boundaries."

    commands = json.dumps(reproducibility)
    assert "Run-PMR-STAT00-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-STAT-00"]
    assert "pmr_stat_analysis_manifest.json" in artifacts
    assert "pmr_stat_policy_metric_summaries.jsonl" in artifacts
    assert "pmr_stat_policy_pair_deltas.jsonl" in artifacts
    assert "pmr_stat_rank_table.json" in artifacts
    assert "pmr_stat_sensitivity_packet.json" in artifacts
    assert "pmr_stat_failure_mode_packet.json" in artifacts
    assert (docs_dir / "pmr-simulation-statistical-analysis.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Descriptive fixture statistics are not real-world inference." in boundary_text
    assert "Rank table is not production policy selection." in boundary_text


def test_dashboard_validator_rejects_pmr_stat_00_overclaims(tmp_path):
    for claim in (
        "real-world inference",
        "production policy selection",
        "PMR superiority proof",
        "hallucination reduction proof",
    ):
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        page = docs_dir / "pmr-simulation-statistical-analysis.md"
        page.write_text(page.read_text() + f"\nPMR-STAT-00 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_claims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found, result



def test_pmr_fed_stress_00_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    accepted_phases = dashboard["accepted_phases"]
    phase_ids = [entry["phase_id"] for entry in accepted_phases]
    assert len(phase_ids) == len(set(phase_ids))
    assert "PMR-FED-STRESS-00" in phase_ids
    phase = next(entry for entry in accepted_phases if entry["phase_id"] == "PMR-FED-STRESS-00")
    assert phase["evidence_type"] == "stress_scaffold"
    assert phase["dashboard_summary"]["federation_stress_not_federation"] is True
    assert phase["dashboard_summary"]["network_calls_not_performed"] is True
    assert phase["claim_allowed"] == "PMR-FED-STRESS-00 demonstrates a deterministic synthetic federation stress corpus and failure-mode scaffold that models federation risks while preserving no-federation and no-network-authority boundaries."

    commands = json.dumps(reproducibility)
    assert "Run-PMR-FED-STRESS00-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-FED-STRESS-00"]
    assert "pmr_federation_stress_manifest.json" in artifacts
    assert "pmr_federation_node_fixtures.json" in artifacts
    assert "pmr_federation_stress_scenarios.json" in artifacts
    assert "pmr_federation_failure_mode_rows.jsonl" in artifacts
    assert "pmr_federation_propagation_risk_packet.json" in artifacts
    assert "pmr_federation_stress_statistics_packet.json" in artifacts
    assert (docs_dir / "pmr-federation-stress-corpus.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Federation stress corpus is not federation." in boundary_text
    assert "Federation stress result is not federation proof." in boundary_text
    assert "Hash is not encryption." in boundary_text


def test_dashboard_validator_rejects_pmr_fed_stress_00_overclaims(tmp_path):
    for claim in (
        "federation proof",
        "network authorization",
        "encrypted shard transfer",
        "reward entitlement",
    ):
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        page = docs_dir / "pmr-federation-stress-corpus.md"
        page.write_text(page.read_text() + f"\nPMR-FED-STRESS-00 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_claims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found or (claim.lower() == "federation proof" and "federation" in found), result



def test_pmr_human_provenance_00_indexes_docs_and_boundaries_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())

    accepted_phases = dashboard["accepted_phases"]
    phase_ids = [entry["phase_id"] for entry in accepted_phases]
    assert len(phase_ids) == len(set(phase_ids))
    assert "PMR-HUMAN-PROVENANCE-00" in phase_ids
    phase = next(entry for entry in accepted_phases if entry["phase_id"] == "PMR-HUMAN-PROVENANCE-00")
    assert phase["evidence_type"] == "architecture_scaffold"
    assert phase["dashboard_summary"]["human_provenance_not_identity_certification"] is True
    assert phase["dashboard_summary"]["consent_execution_performed"] is False
    assert phase["claim_allowed"] == "PMR-HUMAN-PROVENANCE-00 demonstrates a fixture-only human provenance and consent context scaffold for synthetic provenance, consent scope, correction, revocation, review participation, and lived-stakes annotation while preserving non-authority boundaries."

    commands = json.dumps(reproducibility)
    assert "Run-PMR-HUMAN-PROVENANCE00-Acceptance.ps1" in commands
    artifacts = artifact_index["phases"]["PMR-HUMAN-PROVENANCE-00"]
    assert "pmr_human_provenance_manifest.json" in artifacts
    assert "pmr_human_provenance_context_packet.json" in artifacts
    assert "pmr_human_consent_scope_packet.json" in artifacts
    assert "pmr_human_correction_request_packet.json" in artifacts
    assert "pmr_human_revocation_request_packet.json" in artifacts
    assert "pmr_human_lived_stakes_annotation_packet.json" in artifacts
    assert (docs_dir / "pmr-human-provenance-context.md").exists()
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "Human provenance context is not identity certification." in boundary_text
    assert "The system must not encode human = body or AI = mind." in boundary_text


def test_dashboard_validator_rejects_pmr_human_provenance_00_overclaims(tmp_path):
    for claim in (
        "identity certification",
        "consent execution",
        "human value score",
        "AI consciousness",
        "human consciousness",
    ):
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_").replace("-", "_"))
        page = docs_dir / "pmr-human-provenance-context.md"
        page.write_text(page.read_text() + f"\nPMR-HUMAN-PROVENANCE-00 claims {claim}.\n")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False
        found = [hit.lower() for hit in result["forbidden_claims_found"]]
        assert claim.lower() in found or f"claims {claim.lower()}" in found, result


def test_sonya_required_membrane_checkpoint_dashboard_entries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    phase = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "SONYA-REQUIRED-MEMBRANE-CHECKPOINT-00")
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_sonya_required_membrane_checkpoint"
    assert "sonya_required_membrane_checkpoint_packet.json" in phase["primary_artifacts"]
    assert "Sonya is the required execution membrane for model/tool/provider-facing paths." in (docs_dir / "claim-boundaries.md").read_text()
    assert "Missing Sonya posture must fail closed." in (docs_dir / "sonya-required-membrane-checkpoint.md").read_text()


def test_sonya_required_membrane_validator_rejects_positive_overclaims(tmp_path):
    forbidden_claims = (
        "SONYA membrane checkpoint claims provider call.",
        "SONYA membrane checkpoint claims raw output admission.",
        "SONYA membrane checkpoint claims live model execution.",
        "SONYA membrane checkpoint claims network authorization.",
        "SONYA membrane checkpoint claims adapter authorization.",
    )
    for claim in forbidden_claims:
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_").replace(".", ""))
        page = docs_dir / "sonya-required-membrane-checkpoint.md"
        page.write_text(page.read_text(encoding="utf-8") + f"\n{claim}\n", encoding="utf-8")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        assert result["forbidden_claims_found"], result


def test_sonya_required_membrane_validator_allows_bounded_negative_contexts(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    page = docs_dir / "sonya-required-membrane-checkpoint.md"
    page.write_text(
        page.read_text(encoding="utf-8")
        + "\nno remote provider call\nprovider calls not performed\nraw output is forbidden\nraw output is not cognition\nraw_output_admitted = false\nraw_output_forbidden = true\n",
        encoding="utf-8",
    )
    result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
    assert result["passed"] is True


def test_tel_event_stack_dashboard_entries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    phase = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "TEL-EVENT-STACK-00")
    assert "tel_event_stack_manifest.json" in phase["primary_artifacts"]
    assert phase["dashboard_summary"]["review_status"] == "accepted_as_tel_event_stack_scaffold"

def test_tel_event_stack_validator_rejects_overclaims(tmp_path):
    for claim in ("claims runtime authority", "claims surveillance", "claims memory write", "claims provider call", "claims network authorization", "claims peer review certification"):
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "tel-event-stack.md"
        page.write_text(page.read_text(encoding="utf-8") + f"\nTEL event stack {claim}.\n", encoding="utf-8")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False

def test_evidence_review_product_loop_dashboard_entries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    phase = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "EVIDENCE-REVIEW-PRODUCT-LOOP-02")
    assert "evidence_review_product_loop_manifest.json" in phase["primary_artifacts"]
    assert "evidence_review_claim_triage_rows.jsonl" in phase["primary_artifacts"]
    assert "Evidence Review product loop is not final answer selection." in (docs_dir / "claim-boundaries.md").read_text()


def test_evidence_review_product_loop_validator_rejects_overclaims(tmp_path):
    for claim in (
        "claims final answer selection",
        "claims accepted evidence",
        "claims truth certification",
        "claims hallucination reduction proof",
        "claims product release",
        "claims peer review certification",
    ):
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "evidence-review-product-loop.md"
        page.write_text(page.read_text(encoding="utf-8") + f"\nEVIDENCE-REVIEW-PRODUCT-LOOP-02 {claim}.\n", encoding="utf-8")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False


def test_evidence_review_metrics_dashboard_entries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    phase = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "EVIDENCE-REVIEW-METRICS-00")
    assert "evidence_review_metrics_manifest.json" in phase["primary_artifacts"]
    assert "Hypercompression reduces explanatory distance, not review obligation." in (docs_dir / "claim-boundaries.md").read_text()


def test_cognitive_waters_pattern_metrics_dashboard_entries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    phase = next(entry for entry in dashboard["accepted_phases"] if entry["phase_id"] == "COGNITIVE-WATERS-PATTERN-METRICS-00")
    assert "cognitive_waters_metrics_manifest.json" in phase["primary_artifacts"]
    assert "Pattern morphology is not consciousness proof." in (docs_dir / "claim-boundaries.md").read_text()


def test_validator_allows_bounded_truth_final_product_release_contexts(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    page = docs_dir / "claim-boundaries.md"
    page.write_text(
        page.read_text(encoding="utf-8")
        + "\nnot truth certification\n"
        + "truth certification blocked\n"
        + "truth certification not performed\n"
        + "truth certification packet\n"
        + "not final answer release\n"
        + "final answer not released\n"
        + "final_answer_released = false\n"
        + "not product release\n"
        + "product release not performed\n"
        + "product_release_performed = false\n"
        + "product release packet\n"
        + "reviewer utility metric is not product release\n",
        encoding="utf-8",
    )
    result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
    assert result["passed"] is True, result


def test_validator_rejects_claims_truth_final_answer_product_release(tmp_path):
    for claim in (
        "claims truth certification",
        "claims final answer release",
        "claims product release",
    ):
        out_dir, docs_dir = run_builder(tmp_path / claim.replace(" ", "_"))
        page = docs_dir / "claim-boundaries.md"
        page.write_text(page.read_text(encoding="utf-8") + f"\n{claim}\n", encoding="utf-8")
        result = validate_dashboard(out_dir / "experiment_suite_dashboard.json", docs_dir)
        assert result["passed"] is False, claim
        found = [hit.lower() for hit in result["forbidden_claims_found"]]
        assert claim in found or claim.removeprefix("claims ") in found, result


def test_ontology_claim_registry_page_contains_required_boundaries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    _ = out_dir
    page = (docs_dir / "ontology-claim-registry.md")
    assert page.exists()
    text = page.read_text(encoding="utf-8")
    assert "Ontology claim is not ontology proof." in text
    assert "Probabilistic confidence is not probabilistic certitude." in text
    assert "Run-ONTOLOGY-CLAIM-REGISTRY00-Acceptance.ps1" in text


def test_local_sonya_path_portability_dashboard_entries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    assert any(p["phase_id"] == "LOCAL-SONYA-PATH-PORTABILITY-00" for p in dashboard["accepted_phases"])
    repro = json.loads((out_dir / "reproducibility_index.json").read_text())
    command_blob = json.dumps(repro["commands"])
    assert "Run-LOCAL-SONYA-PATH-PORTABILITY00-Acceptance.ps1" in command_blob
    artifacts = json.loads((out_dir / "artifact_index.json").read_text())
    phase_artifacts = artifacts["phases"]["LOCAL-SONYA-PATH-PORTABILITY-00"]
    for a in ["local_sonya_path_portability_manifest.json","local_sonya_node_environment_packet.json","local_sonya_path_audit_rows.jsonl","local_sonya_path_policy_packet.json","local_sonya_path_portability_review_packet.json"]:
        assert a in phase_artifacts
    boundaries = (docs_dir / "claim-boundaries.md").read_text(encoding="utf-8")
    assert "User path is not system path." in boundaries
    assert "Example path is not runtime requirement." in boundaries
    assert "Localhost readiness is not LAN readiness." in boundaries


def test_tb_product_slice_dashboard_entries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    assert any(p["phase_id"] == "TB-PRODUCT-SLICE-00" for p in dashboard["accepted_phases"])
    repro = json.loads((out_dir / "reproducibility_index.json").read_text())
    assert "Run-TB-PRODUCT-SLICE00-Acceptance.ps1" in json.dumps(repro["commands"])
    artifacts = json.loads((out_dir / "artifact_index.json").read_text())
    phase_artifacts = artifacts["phases"]["TB-PRODUCT-SLICE-00"]
    for a in ["tb_product_slice_manifest.json","source_bundle_manifest.json","sonya_candidate_packet.json","claim_evidence_map.json","unsupported_claim_report.json","uncertainty_report.json","tel_events.jsonl","review_receipt.md"]:
        assert a in phase_artifacts
    boundaries = (docs_dir / "claim-boundaries.md").read_text(encoding="utf-8")
    assert "User-visible review receipt is required." in boundaries
    assert "Unsupported claim must remain visible." in boundaries


def test_tb_product_slice_01_dashboard_entries(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    assert any(p["phase_id"] == "TB-PRODUCT-SLICE-01" for p in dashboard["accepted_phases"])
    repro = json.loads((out_dir / "reproducibility_index.json").read_text())
    assert "Run-TB-PRODUCT-SLICE01-Acceptance.ps1" in json.dumps(repro["commands"])
    artifacts = json.loads((out_dir / "artifact_index.json").read_text())
    phase_artifacts = artifacts["phases"]["TB-PRODUCT-SLICE-01"]
    for a in ["tb_product_slice_01_manifest.json","multi_source_bundle_manifest.json","source_link_map.json","cross_source_conflict_report.json","review_receipt.md"]:
        assert a in phase_artifacts
    boundaries=(docs_dir/"claim-boundaries.md").read_text(encoding="utf-8")
    assert "Cross-source conflict is not contradiction resolution." in boundaries
    assert "Conflict must remain visible." in boundaries


def test_tb_product_slice_01_page_contains_required_content(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    _ = out_dir
    page = docs_dir / "tb-product-slice-01.md"
    assert page.exists()
    text = page.read_text(encoding="utf-8")
    assert "Cross-source conflict is not contradiction resolution." in text
    assert "Conflict must remain visible." in text
    assert "Run-TB-PRODUCT-SLICE01-Acceptance.ps1" in text
    assert "review_receipt.md" in text


def test_sonya_local_server_gateway_updates_present(tmp_path):
    out_dir, _ = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    idx = json.loads((out_dir / "artifact_index.json").read_text())
    bounds = json.loads((out_dir / "claim_boundary_index.json").read_text())["boundaries"]
    repro = json.loads((out_dir / "reproducibility_index.json").read_text())
    phase_ids = {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "SONYA-LOCAL-SERVER-GATEWAY-00" in phase_ids
    cmds = str(repro)
    assert "Run-SONYA-LOCAL-SERVER-GATEWAY00-Acceptance.ps1" in cmds
    art = idx["phases"]["SONYA-LOCAL-SERVER-GATEWAY-00"]
    for a in ["sonya_local_server_gateway_manifest.json","sonya_local_server_response_packet.json","sonya_local_server_review_packet.json","gateway_failure_receipts.jsonl","tb_product_slice_01_review_receipt.md"]:
        assert a in art
    for b in ["Localhost gateway is not LAN readiness.","Gateway response is not final answer.","Failure receipt is not permission to proceed."]:
        assert b in bounds


def test_sonya_local_server_gateway_01_updates_present(tmp_path):
    out_dir, _ = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    idx = json.loads((out_dir / "artifact_index.json").read_text())
    bounds = json.loads((out_dir / "claim_boundary_index.json").read_text())["boundaries"]
    repro = json.loads((out_dir / "reproducibility_index.json").read_text())
    phase_ids = {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "SONYA-LOCAL-SERVER-GATEWAY-01" in phase_ids
    assert "Run-SONYA-LOCAL-SERVER-GATEWAY01-Acceptance.ps1" in str(repro)
    art = idx["phases"]["SONYA-LOCAL-SERVER-GATEWAY-01"]
    for a in ["sonya_local_server_gateway_01_manifest.json","sonya_local_server_run_index_packet.json","sonya_local_server_retrieval_packet.json","sonya_local_server_gateway_01_review_packet.json","retrieval_failure_receipts.jsonl","tb_product_slice_01_review_receipt.md"]:
        assert a in art
    for b in ["Run retrieval is not memory write.","Run index is not PMR store.","Receipt retrieval is not final answer release.","Event retrieval is not authority.","Unknown run IDs must fail closed."]:
        assert b in bounds


def test_tb_product_slice_02_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "TB-PRODUCT-SLICE-02" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-TB-PRODUCT-SLICE02-Acceptance.ps1" in str(repro)
    art=idx["phases"]["TB-PRODUCT-SLICE-02"]
    for a in ["tb_product_slice_02_manifest.json","source_span_map.json","claim_classification_packet.json","receipt_ux_packet.json","review_receipt.md","tb_product_slice_02_review_packet.json"]:
        assert a in art
    for b in ["Source span is not truth certification.","Quoted source text is not accepted evidence.","Source conflict is not contradiction resolution.","Review receipt is not final answer.","Unsupported claims must remain visible."]:
        assert b in bounds


def test_sonya_local_server_gateway_02_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "SONYA-LOCAL-SERVER-GATEWAY-02" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-SONYA-LOCAL-SERVER-GATEWAY02-Acceptance.ps1" in str(repro)
    art=idx["phases"]["SONYA-LOCAL-SERVER-GATEWAY-02"]
    for a in ["sonya_local_server_gateway_02_manifest.json","sonya_local_server_gateway_02_review_packet.json","sonya_local_server_source_span_retrieval_packet.json","sonya_local_server_claim_classification_retrieval_packet.json","source_span_map.json","claim_classification_packet.json","gateway_failure_receipts.jsonl","retrieval_failure_receipts.jsonl"]:
        assert a in art
    for b in ["Source-span gateway review is not truth certification.","Claim classification is not semantic authority.","Claim classification retrieval is not final answer.","Unknown run IDs must fail closed."]:
        assert b in bounds


def test_local_server_user_file_ingress_00_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "LOCAL-SERVER-USER-FILE-INGRESS-00" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-LOCAL-SERVER-USER-FILE-INGRESS00-Acceptance.ps1" in str(repro)
    art=idx["phases"]["LOCAL-SERVER-USER-FILE-INGRESS-00"]
    for a in ["local_user_file_ingress_manifest.json","local_user_file_consent_packet.json","local_user_file_path_audit_rows.jsonl","local_user_file_normalization_map.json","local_user_file_ingress_review_packet.json","ingress_failure_receipts.jsonl","normalized_source_bundle_manifest.json","source_span_map.json","gateway_failure_receipts.jsonl"]:
        assert a in art
    for b in ["User file ingress is not memory write.","Copied run-local source is not PMR storage.","Missing consent must fail closed.","Unsupported file types must fail closed."]:
        assert b in bounds


def test_pmr_context_availability_ledger_00_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "PMR-CONTEXT-AVAILABILITY-LEDGER-00" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-PMR-CONTEXT-AVAILABILITY-LEDGER00-Acceptance.ps1" in str(repro)
    art=idx["phases"]["PMR-CONTEXT-AVAILABILITY-LEDGER-00"]
    for a in ["pmr_context_availability_ledger.json","pmr_context_dependency_map.json","pmr_context_reupload_queue.json","pmr_context_access_status_report.md","pmr_context_availability_review_packet.json"]:
        assert a in art
    for b in ["Expiration is not nonexistence.","Known inaccessible content is not unknown content.","Summary is not source.","Hash is not content access.","PMR ledger is not deletion authority.","PMR ledger is not pruning authority."]:
        assert b in bounds


def test_local_server_user_file_ingress_01_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "LOCAL-SERVER-USER-FILE-INGRESS-01" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-LOCAL-SERVER-USER-FILE-INGRESS01-Acceptance.ps1" in str(repro)
    art=idx["phases"]["LOCAL-SERVER-USER-FILE-INGRESS-01"]
    for a in ["local_user_file_ingress_01_manifest.json","local_user_file_ingress_request_packet.json","local_user_file_pmr_context_link_packet.json","local_user_file_ingress_receipt_ux_packet.json","local_user_file_ingress_01_review_packet.json"]:
        assert a in art
    for b in ["Explicit file-list ingress is not memory write.","Duplicate input audit is not duplicate input normalization.","A field claiming deduplication must be backed by normalized-output evidence.","PMR context links must not multiply duplicate source paths when deduplicate_source_paths is true."]:
        assert b in bounds


def test_user_facing_receipt_ux_01_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "USER-FACING-RECEIPT-UX-01" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-USER-FACING-RECEIPT-UX01-Acceptance.ps1" in str(repro)
    art=idx["phases"]["USER-FACING-RECEIPT-UX-01"]
    for a in ["local_user_file_human_receipt.md","local_user_file_receipt_ux_01_packet.json","local_user_file_receipt_next_actions.json","local_user_file_receipt_boundary_table.json"]:
        assert a in art
    for b in ["Receipt UX is not final answer.","Reviewer next action is not authority.","Failure receipt is not permission to proceed."]:
        assert b in bounds


def test_local_server_user_file_ingress_02_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "LOCAL-SERVER-USER-FILE-INGRESS-02" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-LOCAL-SERVER-USER-FILE-INGRESS02-Acceptance.ps1" in str(repro)
    art=idx["phases"]["LOCAL-SERVER-USER-FILE-INGRESS-02"]
    for a in ["local_review_request_02_packet.json","local_review_source_set_packet.json","local_review_intent_packet.json","local_review_receipt_preferences_packet.json","local_server_user_file_ingress_02_review_packet.json"]:
        assert a in art
    for b in ["Local review request is not final answer request.","Reviewer intent is not authority."]:
        assert b in bounds


def test_lan_readiness_preflight_00_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "LAN-READINESS-PREFLIGHT-00" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-LAN-READINESS-PREFLIGHT00-Acceptance.ps1" in str(repro)
    art=idx["phases"]["LAN-READINESS-PREFLIGHT-00"]
    for a in ["lan_readiness_preflight_manifest.json","lan_readiness_preflight_request_packet.json","lan_readiness_preflight_report.md","lan_readiness_preflight_report.json","lan_readiness_preflight_review_packet.json"]:
        assert a in art
    for b in ["LAN readiness preflight is not LAN enablement.","Loopback success is not LAN readiness.","Preflight report is not final answer.","Preflight report is not product release."]:
        assert b in bounds

def test_lan_authority_model_00_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "LAN-AUTHORITY-MODEL-00" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-LAN-AUTHORITY-MODEL00-Acceptance.ps1" in str(repro)
    art=idx["phases"]["LAN-AUTHORITY-MODEL-00"]
    for a in ["lan_authority_model_manifest.json","lan_authority_model_request_packet.json","lan_bind_scope_model.json","lan_remote_client_model.json","lan_consent_model.json","lan_network_risk_register.json","lan_authority_boundary_table.json"]:
        assert a in art
    for b in ["LAN authority model is not LAN enablement.","Role model is not authorization.","Network risk register is not network permission."]:
        assert b in bounds

def test_lan_authority_negative_control_00_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "LAN-AUTHORITY-NEGATIVE-CONTROL-00" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-LAN-AUTHORITY-NEGATIVE-CONTROL00-Acceptance.ps1" in str(repro)
    art=idx["phases"]["LAN-AUTHORITY-NEGATIVE-CONTROL-00"]
    for a in ["lan_authority_negative_control_manifest.json","lan_authority_negative_control_request_packet.json","lan_authority_negative_control_failure_receipts.jsonl","lan_authority_negative_control_review_packet.json","lan_authority_model_reference_packet.json"]:
        assert a in art
    for b in ["Negative control is not authorization.","Failed-closed LAN request is not permission to retry with broader authority.","Provider call request must fail closed."]:
        assert b in bounds


def test_lan_operator_consent_preflight_00_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    status=json.loads((out_dir/"status.json").read_text())
    phases = {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "LAN-OPERATOR-CONSENT-PREFLIGHT-00" in phases
    assert "Run-LAN-OPERATOR-CONSENT-PREFLIGHT00-Acceptance.ps1" in str(repro)
    artifacts = idx["phases"]["LAN-OPERATOR-CONSENT-PREFLIGHT-00"]
    for a in ["lan_operator_consent_preflight_manifest.json","lan_operator_consent_request_packet.json","lan_operator_consent_display_packet.json","lan_operator_consent_negative_control_receipts.jsonl"]:
        assert a in artifacts
    for b in ["Consent preflight is not consent execution.","Consent candidate is not consent.","Missing consent must fail closed."]:
        assert b in bounds
    assert status["lan_operator_consent_preflight_00_indexed"] is True
    assert status["not_consent_preflight_consent_execution"] is True


def test_local_review_runtime_v0_updates_present(tmp_path):
    out_dir,_=run_builder(tmp_path)
    dashboard=json.loads((out_dir/"experiment_suite_dashboard.json").read_text())
    idx=json.loads((out_dir/"artifact_index.json").read_text())
    bounds=json.loads((out_dir/"claim_boundary_index.json").read_text())["boundaries"]
    repro=json.loads((out_dir/"reproducibility_index.json").read_text())
    assert "LOCAL-REVIEW-RUNTIME-V0" in {p["phase_id"] for p in dashboard["accepted_phases"]}
    assert "Run-LOCAL-REVIEW-RUNTIME-V0-Acceptance.ps1" in str(repro)
    art=idx["phases"]["LOCAL-REVIEW-RUNTIME-V0"]
    for a in ["local_review_runtime_v0_manifest.json","local_review_runtime_v0_human_summary.md","local_review_runtime_v0_next_actions.json","local_review_runtime_v0_boundary_table.json","local_review_runtime_v0_review_packet.json"]:
        assert a in art
    for b in ["LOCAL-REVIEW-RUNTIME-V0 is not product release.","LOCAL-REVIEW-RUNTIME-V0 is not final answer authority.","LOCAL-REVIEW-RUNTIME-V0 is not truth certification."]:
        assert b in bounds


def test_local_review_metrics_flow_dashboard_entries_and_artifacts(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    accepted = {phase["phase_id"]: phase for phase in dashboard["accepted_phases"]}
    required_phases = {
        "MET-LOCAL-00": [
            "evidence_review_runtime_metrics_packet.json",
            "coherence_runtime_metrics_packet.json",
            "coherence_metric_input_ledger.json",
            "evidence_review_runtime_metrics_summary.md",
        ],
        "WAVE-ROSETTA-METRIC-CALIBRATION-00": ["wave_rosetta_metric_calibration_context.json"],
        "TAF-RUNTIME-00": ["coherence_action_functional_packet.json"],
        "SONYA-METRIC-MEMBRANE-COVERAGE-00": ["sonya_metric_membrane_coverage_packet.json"],
        "COHERENCE-METRIC-FORMULA-REGISTRY-00": [
            "coherence_metric_formula_registry.json",
            "coherence_metric_formula_registry_binding.json",
        ],
        "METRIC-BOUND-SOURCE-TAXONOMY-00": [
            "metric_bound_source_taxonomy.json",
            "metric_bound_profile_registry.json",
            "metric_bound_formula_binding.json",
        ],
        "FLOW-RUNTIME-00": [
            "cognitive_flow_morphology_packet.json",
            "cognitive_flow_topology_packet.json",
            "cognitive_flow_morphology_summary.md",
        ],
    }

    for phase_id, artifacts in required_phases.items():
        phase = accepted[phase_id]
        assert phase["repo"] == "pdxvoiceteacher/CoherenceLattice"
        assert phase["source_phase"] == "LOCAL-REVIEW-RUNTIME-V0"
        assert phase["status"] == "accepted_local_validation"
        assert phase["product_posture"] == "local_diagnostic_scaffold_not_product_release"
        assert phase["authority_posture"] == "non_authoritative"
        assert phase["public_claim_boundary"] == "bounded_diagnostic_only"
        assert phase["primary_artifacts"] == artifacts

    summary = accepted["FLOW-RUNTIME-00"]["dashboard_summary"]
    assert summary["evidence_metrics_status"] == "verified_diagnostic"
    assert summary["coherence_metrics_status"] == "verified_diagnostic"
    assert summary["taf_metric_status"] == "verified_diagnostic"
    assert summary["formula_binding_status"] == "bound"
    assert summary["metric_bound_binding_status"] == "bound"
    assert summary["wave_rosetta_baseline"] is True
    assert summary["wave_rosetta_is_baseline_not_universal_identity"] is True
    assert summary["sonya_metric_membrane_coverage_status"] == "covered"
    assert summary["sophia_decision"] == "pass"
    assert summary["tel_replay_status"] == "replayable"
    assert summary["flow_morphology_status"] == "observed_runtime_morphology"
    assert summary["flow_topology_status"] == "verified_diagnostic"
    assert summary["flow_node_count"] == 20
    assert summary["flow_edge_count"] == 14
    assert summary["spiral_turn_count"] == 9
    assert summary["repair_loop_count"] == 2
    assert summary["bottleneck_count"] == 0
    assert summary["upward_integration_score"] == 1
    assert summary["flow_continuity_score"] == 0.714286
    assert summary["repair_capacity_score"] == 1
    assert summary["poetic_alias"] == "waters_spiral_runtime_v0"

    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())["phases"]
    for phase_id, artifacts in required_phases.items():
        assert artifact_index[phase_id] == artifacts

    doc = (docs_dir / "local-review-metrics-flow.md").read_text(encoding="utf-8")
    assert "WAVE Rosetta is used as a calibration baseline, not universal identity" in doc
    assert "`waters_spiral_runtime_v0` as poetic alias only" in doc
    assert "No Omega artifact was emitted" in doc
    assert "Repeated runs are required for scientific claims" in doc


def test_local_review_metrics_flow_repro_command_and_boundaries(tmp_path):
    out_dir, _ = run_builder(tmp_path)
    repro = json.loads((out_dir / "reproducibility_index.json").read_text())
    repro_text = json.dumps(repro)
    assert "Run-LOCAL-REVIEW-RUNTIME-V0-Acceptance.ps1" in repro_text
    assert "total action functional, formula registry, metric bound taxonomy, cognitive flow morphology" in repro_text
    assert "-SophiaRoot C:\\\\UVLM\\\\Sophia" in repro_text
    assert "-EnableSophiaAudit" in repro_text

    boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())["boundaries"]
    for phase_id in (
        "MET-LOCAL-00",
        "WAVE-ROSETTA-METRIC-CALIBRATION-00",
        "TAF-RUNTIME-00",
        "SONYA-METRIC-MEMBRANE-COVERAGE-00",
        "COHERENCE-METRIC-FORMULA-REGISTRY-00",
        "METRIC-BOUND-SOURCE-TAXONOMY-00",
        "FLOW-RUNTIME-00",
    ):
        for boundary in (
            "product release",
            "final answer authority",
            "truth certification",
            "accepted evidence authority",
            "consciousness proof",
            "Omega detection",
            "universal ontology proof",
            "deployment authority",
            "provider runtime",
            "LAN enablement",
            "memory write",
            "federation",
        ):
            assert f"{phase_id} is not {boundary}." in boundaries



def test_runtime_metrics_seed_corpus_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    page = (docs_dir / "runtime-metrics-seed-corpus.md").read_text()
    index = (docs_dir / "index.md").read_text()

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "RUNTIME-METRICS-CORPUS-SEED-00"
    )
    assert phase["repo"] == "pdxvoiceteacher/CoherenceLattice"
    assert phase["source_phase"] == "LOCAL-REVIEW-RUNTIME-V0"
    assert phase["status"] == "accepted_local_validation"
    assert phase["publication_status"] == "dashboard_synced"
    assert phase["product_posture"] == "local_seed_corpus_not_population_calibration_not_product_release"
    assert phase["authority_posture"] == "non_authoritative"
    assert phase["public_claim_boundary"] == "bounded_seed_corpus_instrumentation_only"
    summary = phase["dashboard_summary"]
    assert summary["observation_count"] == 6
    assert summary["fixture_count"] == 6
    assert summary["pass_count"] == 2
    assert summary["watch_count"] == 1
    assert summary["revise_count"] == 1
    assert summary["incomplete_count"] == 1
    assert summary["invalid_boundary_violation_count"] == 1
    assert summary["population_calibration_status"] == "not_population_calibrated"
    assert summary["federation_status"] == "not_federated"
    assert summary["user_population_sample_count"] == 0
    assert summary["future_population_calibration_requires_federation_or_pilot_population"] is True
    assert summary["repeated_runs_required_for_scientific_claims"] is True
    assert summary["user_value_status"] == "observable_proxy_only"
    assert summary["artifact_count"] == 635
    assert summary["total_artifact_bytes"] == 3520816
    assert summary["bloat_warning_count"] == 1
    for key in (
        "seed_corpus_is_not_product_release",
        "seed_corpus_is_not_truth_certification",
        "seed_corpus_is_not_consciousness_proof",
        "seed_corpus_is_not_omega_detection",
        "seed_corpus_is_not_universal_ontology_proof",
        "seed_corpus_is_not_population_calibration",
        "seed_corpus_is_not_federation",
    ):
        assert summary[key] is True
    for artifact in (
        "runtime_metrics_seed_corpus.json",
        "runtime_metrics_seed_observations.jsonl",
        "runtime_performance_profile.json",
        "user_value_observable_packet.json",
        "runtime_metrics_seed_corpus_summary.md",
    ):
        assert artifact in artifact_index["phases"]["RUNTIME-METRICS-CORPUS-SEED-00"]
    for artifact in (
        "evidence_review_runtime_metrics_packet.json",
        "coherence_runtime_metrics_packet.json",
        "coherence_metric_input_ledger.json",
        "wave_rosetta_metric_calibration_context.json",
        "coherence_action_functional_packet.json",
        "sonya_metric_membrane_coverage_packet.json",
        "coherence_metric_formula_registry.json",
        "coherence_metric_formula_registry_binding.json",
        "metric_bound_source_taxonomy.json",
        "metric_bound_profile_registry.json",
        "metric_bound_formula_binding.json",
        "cognitive_flow_morphology_packet.json",
        "cognitive_flow_topology_packet.json",
        "cognitive_flow_morphology_summary.md",
    ):
        assert artifact in json.dumps(artifact_index)
    assert "build_runtime_metrics_seed_corpus" in json.dumps(reproducibility)
    assert "runtime-metrics-seed-corpus.md" in index
    assert "not population calibration" in page
    assert "not federated" in page
    assert "not product release" in page
    assert "not truth certification" in page
    assert "not consciousness proof" in page
    assert "not Omega detection" in page
    assert "not universal ontology proof" in page
    assert "not human benefit proof" in page
    assert "not market validation" in page
    assert "not deployment readiness" in page
    assert "not final answer authority" in page
    assert "not accepted evidence authority" in page
    assert "not memory write" in page
    assert "future population calibration requires pilot or federated population data" in page
    assert "Omega field state analysis is not implemented" in page
    assert "artifact_count = 635" in page
    assert "total_artifact_bytes = 3,520,816" in page
    assert "C:\\UVLM" in page
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "bounded seed corpus instrumentation only" in boundary_text
    assert "not population calibration" in boundary_text
    assert "not human benefit proof" in boundary_text



def test_pmr_local_queryable_store_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    status = json.loads((out_dir / "status.json").read_text())
    page = (docs_dir / "pmr-local-queryable-store.md").read_text()
    index = (docs_dir / "index.md").read_text()

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "PMR-LOCAL-RUNTIME-QUERYABLE-STORE-00"
    )
    assert phase["repo"] == "pdxvoiceteacher/CoherenceLattice"
    assert phase["source_phase"] == "LOCAL-REVIEW-RUNTIME-V0"
    assert phase["status"] == "accepted_local_validation"
    assert phase["publication_status"] == "dashboard_synced"
    assert phase["authority_posture"] == "non_authoritative"
    assert phase["public_claim_boundary"] == "bounded_local_provenance_retrieval_only"
    summary = phase["dashboard_summary"]
    assert summary["query_index_status"] == "indexed"
    assert summary["supported_query_type_count"] == 15
    assert summary["indexed_artifact_count"] == 44
    assert summary["indexed_dependency_edge_count"] == 34
    assert summary["indexed_metric_count"] == 37
    assert summary["indexed_formula_count"] == 19
    assert summary["indexed_bound_profile_count"] == 19
    assert summary["indexed_tel_event_count"] == 19
    assert summary["indexed_seed_observation_count"] == 6
    assert summary["indexed_flow_node_count"] == 20
    assert summary["indexed_sonya_coverage_row_count"] == 10
    assert summary["query_count"] == 15
    assert summary["completed_query_count"] == 14
    assert summary["no_match_query_count"] == 1
    assert summary["forbidden_authority_artifact_count"] == 0
    assert summary["pmr_query_posture"] == "local_provenance_retrieval_only"
    for query_type in (
        "artifact_by_name",
        "artifact_by_role",
        "artifact_by_retention_class",
        "dependency_upstream",
        "dependency_downstream",
        "metric_by_id",
        "formula_by_id",
        "bound_profile_by_metric",
        "tel_event_by_type",
        "sophia_decision_by_run",
        "seed_observation_by_fixture",
        "seed_observation_by_posture",
        "flow_node_by_stage",
        "sonya_coverage_by_artifact",
        "forbidden_authority_scan",
    ):
        assert query_type in summary["supported_query_types"]
        assert query_type in page
    for artifact in (
        "pmr_local_query_index.json",
        "pmr_local_query_smoke_results.jsonl",
        "pmr_local_query_receipt.json",
        "pmr_local_query_summary.md",
    ):
        assert artifact in artifact_index["phases"]["PMR-LOCAL-RUNTIME-QUERYABLE-STORE-00"]
    reproducibility_text = json.dumps(reproducibility)
    assert "Run-PMR-LOCAL-RUNTIME-QUERYABLE-STORE00-Acceptance.ps1" in reproducibility_text
    assert "build_pmr_local_query_store" in reproducibility_text
    assert "build_runtime_metrics_seed_corpus" in reproducibility_text
    assert "runtime_metrics_seed_corpus" in reproducibility_text
    assert "pmr_local_query" in reproducibility_text
    assert "pmr-local-queryable-store.md" in index
    for phrase in (
        "PMR query is local provenance retrieval only.",
        "PMR query is not memory write.",
        "PMR query is not retrosynthesis.",
        "PMR query is not Atlas memory admission.",
        "PMR query is not truth certification.",
        "PMR query is not product release.",
        "PMR query is not final answer.",
        "build_pmr_local_query_store",
        "build_runtime_metrics_seed_corpus",
        "runtime_metrics_seed_corpus",
        "pmr_local_query",
        "C:\\UVLM is a local validation example, not product default",
        "PMR query prepares the substrate for future retrosynthesis-readiness analysis, but does not perform retrosynthesis.",
    ):
        assert phrase in page
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "bounded local provenance retrieval only" in boundary_text
    assert "PMR query is not memory write." in boundary_text
    assert status["pmr_local_runtime_queryable_store_00_indexed"] is True
    assert status["not_pmr_query_memory_write"] is True
    assert status["not_pmr_query_retrosynthesis"] is True
    assert status["not_pmr_query_atlas_memory_admission"] is True



def test_retrosynthesis_readiness_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    status = json.loads((out_dir / "status.json").read_text())
    page = (docs_dir / "retrosynthesis-readiness.md").read_text()
    index = (docs_dir / "index.md").read_text()

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "RETROSYNTHESIS-READINESS-00"
    )
    assert phase["repo"] == "pdxvoiceteacher/CoherenceLattice"
    assert phase["source_phase"] == "PMR-LOCAL-RUNTIME-QUERYABLE-STORE-00"
    assert phase["status"] == "accepted_local_validation"
    assert phase["publication_status"] == "dashboard_synced"
    assert phase["authority_posture"] == "non_authoritative"
    assert phase["public_claim_boundary"] == "readiness_only_bounded_local_prototype_precondition"
    summary = phase["dashboard_summary"]
    assert summary["readiness_status"] == "ready_for_bounded_retrosynthesis_prototype"
    assert summary["readiness_score"] == 1.0
    assert summary["recommended_next_phase"] == "RETROSYNTHESIS-LOCAL-PROTOTYPE-00"
    assert summary["readiness_dimension_count"] == 16
    assert summary["failed_checks"] == 0
    assert summary["blocking_reasons"] == 0
    assert summary["memory_write_not_performed_evidence_refs"] == 5
    assert summary["atlas_admission_not_performed_evidence_refs"] == 5
    assert summary["pmr_query_receipt_status"] == "completed"
    assert summary["seed_corpus_observation_count"] == 6
    assert summary["population_calibration_status"] == "not_population_calibrated"
    assert summary["federation_status"] == "not_federated"
    assert summary["tel_replay_status"] == "replayable"
    for key in (
        "retrosynthesis_performed",
        "improvement_hypotheses_generated",
        "atlas_memory_write_performed",
        "memory_admission_performed",
        "federation_performed",
        "product_release_performed",
        "final_answer_emitted",
        "truth_certification_emitted",
        "consciousness_proof_emitted",
        "omega_detection_performed",
    ):
        assert summary[key] is False
    for artifact in (
        "retrosynthesis_readiness_packet.json",
        "retrosynthesis_readiness_checklist.json",
        "retrosynthesis_readiness_receipt.json",
        "retrosynthesis_readiness_summary.md",
    ):
        assert artifact in artifact_index["phases"]["RETROSYNTHESIS-READINESS-00"]
    reproducibility_text = json.dumps(reproducibility)
    assert "Run-RETROSYNTHESIS-READINESS00-Acceptance.ps1" in reproducibility_text
    assert "build_retrosynthesis_readiness_assessment" in reproducibility_text
    assert "build_pmr_local_query_store" in reproducibility_text
    assert "build_runtime_metrics_seed_corpus" in reproducibility_text
    assert "retrosynthesis_readiness" in reproducibility_text
    assert "retrosynthesis-readiness.md" in index
    for phrase in (
        "This is readiness, not retrosynthesis.",
        "No improvement hypotheses were generated.",
        "No Atlas memory write occurred.",
        "No memory admission occurred.",
        "No federation occurred.",
        "No product release occurred.",
        "No Omega detection occurred.",
        "Population calibration is not claimed.",
        "The system is ready only for a bounded local retrosynthesis prototype.",
        "build_retrosynthesis_readiness_assessment",
        "build_pmr_local_query_store",
        "build_runtime_metrics_seed_corpus",
        "retrosynthesis_readiness",
        "runtime_metrics_seed_corpus",
        "pmr_local_query",
        "C:\\UVLM is a local validation example, not product default",
        "This command builds readiness artifacts only.",
        "No improvement hypotheses are generated.",
        "No Atlas memory write occurs.",
        "No Atlas memory admission occurs.",
        "No truth certification occurs.",
        "No consciousness proof or universal ontology proof is emitted.",
    ):
        assert phrase in page
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "RETROSYNTHESIS-READINESS-00 is readiness, not retrosynthesis." in boundary_text
    assert "RETROSYNTHESIS-READINESS-00 is ready only for a bounded local retrosynthesis prototype." in boundary_text
    assert status["retrosynthesis_readiness_00_indexed"] is True
    assert status["not_retrosynthesis_performed"] is True
    assert status["not_improvement_hypotheses_generated"] is True
    assert status["not_retrosynthesis_readiness_memory_write"] is True
    assert status["not_retrosynthesis_readiness_atlas_memory_admission"] is True


def test_retrosynthesis_local_prototype_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    status = json.loads((out_dir / "status.json").read_text())
    page = (docs_dir / "retrosynthesis-local-prototype.md").read_text()
    index = (docs_dir / "index.md").read_text()

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "RETROSYNTHESIS-LOCAL-PROTOTYPE-00"
    )
    assert phase["repo"] == "pdxvoiceteacher/CoherenceLattice"
    assert phase["source_phase"] == "RETROSYNTHESIS-READINESS-00"
    assert phase["status"] == "accepted_local_validation"
    assert phase["publication_status"] == "dashboard_synced"
    assert phase["authority_posture"] == "non_authoritative"
    assert phase["public_claim_boundary"] == "candidate_only_human_review_required"
    summary = phase["dashboard_summary"]
    assert summary["prototype_status"] == "completed_candidate_generation"
    assert summary["readiness_observed"] == "ready_for_bounded_retrosynthesis_prototype"
    assert summary["candidate_hypothesis_count"] == 7
    assert summary["candidate_repair_plan_count"] == 3
    assert summary["pattern_observation_count"] == 5
    assert summary["reviewer_suggestion_count"] == 4
    assert summary["retrosynthesis_performed"] is True
    assert summary["memory_write_performed"] is False
    assert summary["atlas_memory_admission_performed"] is False
    assert summary["federation_performed"] is False
    assert summary["product_release_performed"] is False
    assert summary["final_answer_emitted"] is False
    assert summary["truth_certification_emitted"] is False
    assert summary["candidate_outputs_require_human_review"] is True
    for artifact in (
        "retrosynthesis_local_prototype_packet.json",
        "retrosynthesis_candidate_hypotheses.jsonl",
        "retrosynthesis_candidate_repair_plans.jsonl",
        "retrosynthesis_pattern_observations.jsonl",
        "retrosynthesis_local_prototype_receipt.json",
        "retrosynthesis_local_prototype_summary.md",
    ):
        assert artifact in artifact_index["phases"]["RETROSYNTHESIS-LOCAL-PROTOTYPE-00"]
    reproducibility_text = json.dumps(reproducibility)
    for fragment in (
        "build_runtime_metrics_seed_corpus",
        "build_pmr_local_query_store",
        "build_retrosynthesis_readiness_assessment",
        "build_retrosynthesis_local_prototype",
        "runtime_metrics_seed_corpus",
        "retrosynthesis_local_prototype",
        r"C:\\UVLM",
    ):
        assert fragment in reproducibility_text
    assert "retrosynthesis-local-prototype.md" in index
    for phrase in (
        "What was validated locally",
        "What artifacts were produced",
        "What candidate outputs were generated",
        "Candidate hypotheses are not truth.",
        "Repair plans are not authority.",
        "Pattern observations are local-seed-corpus-only.",
        "Human review is required",
        "No memory write occurred.",
        "No Atlas memory admission occurred.",
        "No federation occurred.",
        "No product release occurred.",
        "No provider runtime occurred.",
        "No LAN enablement occurred.",
        "No truth certification occurred.",
        "No final answer was emitted.",
        "No accepted evidence was emitted.",
        "No Omega detection occurred.",
        "No consciousness proof occurred.",
        "No universal ontology proof occurred.",
        "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00",
        "not Atlas memory admission yet",
        "build_retrosynthesis_local_prototype",
        "C:\\UVLM is a local validation example, not product default",
    ):
        assert phrase in page
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "RETROSYNTHESIS-LOCAL-PROTOTYPE-00 is bounded local candidate generation only." in boundary_text
    assert "Human review is required for RETROSYNTHESIS-LOCAL-PROTOTYPE-00 outputs." in boundary_text
    assert status["retrosynthesis_local_prototype_00_indexed"] is True
    assert status["retrosynthesis_local_prototype_candidate_generation_only"] is True
    assert status["not_local_prototype_memory_write"] is True
    assert status["not_local_prototype_atlas_memory_admission"] is True
    assert status["not_local_prototype_federation"] is True
    assert status["not_local_prototype_product_release"] is True
    assert status["not_local_prototype_truth_certification"] is True



def test_atlas_local_memory_admission_readiness_indexes_and_docs_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    status = json.loads((out_dir / "status.json").read_text())
    page = (docs_dir / "atlas-local-memory-admission-readiness.md").read_text()
    index = (docs_dir / "index.md").read_text()

    phase = next(
        entry
        for entry in dashboard["accepted_phases"]
        if entry["phase_id"] == "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00"
    )
    assert phase["repo"] == "pdxvoiceteacher/CoherenceLattice"
    assert phase["source_phase"] == "RETROSYNTHESIS-LOCAL-PROTOTYPE-00"
    assert phase["status"] == "accepted_local_validation"
    assert phase["publication_status"] == "dashboard_synced"
    assert phase["authority_posture"] == "non_authoritative"
    assert phase["public_claim_boundary"] == "readiness_only_local_review_gate_no_memory_write"
    summary = phase["dashboard_summary"]
    assert summary["readiness_status"] == "ready_for_bounded_atlas_memory_admission_prototype"
    assert summary["readiness_status"] != "ready_for_local_review_only_admission_gate"
    assert summary["source_prototype_status"] == "completed_candidate_generation"
    assert summary["readiness_score"] == 1
    assert summary["recommended_next_phase"] == "ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00"
    assert summary["readiness_dimensions"] == 21
    assert summary["readiness_dimension_count"] == 21
    assert summary["readiness_dimension_count"] != 12
    assert summary["failed_checks"] == 0
    assert summary["blocking_reasons"] == 0
    assert summary["candidate_hypotheses"] == 7
    assert summary["candidate_repair_plans"] == 3
    assert summary["pattern_observations"] == 5
    assert summary["local_review_only"] is True
    assert summary["atlas_memory_admission_performed"] is False
    assert summary["atlas_memory_write_performed"] is False
    assert summary["atlas_memory_candidate_written"] is False
    assert summary["memory_candidate_write_performed"] is False
    assert summary["memory_admission_performed"] is False
    assert summary["federation_performed"] is False
    assert summary["product_release_performed"] is False
    assert summary["final_answer_emitted"] is False
    assert summary["truth_certification_emitted"] is False
    for artifact in (
        "atlas_local_memory_admission_readiness_packet.json",
        "atlas_local_memory_admission_readiness_checklist.json",
        "atlas_local_memory_admission_readiness_receipt.json",
        "atlas_local_memory_admission_readiness_summary.md",
    ):
        assert artifact in artifact_index["phases"]["ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00"]
    reproducibility_text = json.dumps(reproducibility)
    for fragment in (
        "Run-ATLAS-LOCAL-MEMORY-ADMISSION-READINESS00-Acceptance.ps1",
        "build_runtime_metrics_seed_corpus",
        "build_pmr_local_query_store",
        "build_retrosynthesis_readiness_assessment",
        "build_retrosynthesis_local_prototype",
        "build_atlas_local_memory_admission_readiness",
        "atlas_local_memory_admission_readiness",
        "atlas_local_memory_admission_readiness_00",
        r"C:\\UVLM",
    ):
        assert fragment in reproducibility_text
    assert "atlas-local-memory-admission-readiness.md" in index
    stale_builder = "build_atlas_memory_admission_readiness"
    assert stale_builder not in page
    assert stale_builder not in reproducibility_text
    assert stale_builder not in json.dumps(dashboard)
    for phrase in (
        "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00 records Atlas memory admission readiness",
        "This is Atlas memory admission readiness, not Atlas memory admission.",
        "readiness_status = ready_for_bounded_atlas_memory_admission_prototype",
        "readiness_score = 1",
        "recommended_next_phase = ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00",
        "readiness_dimensions = 21",
        "readiness_dimension_count = 21",
        "candidate_hypotheses = 7",
        "candidate_repair_plans = 3",
        "pattern_observations = 5",
        "atlas_memory_admission_performed = false",
        "atlas_memory_write_performed = false",
        "atlas_memory_candidate_written = false",
        "memory_admission_performed = false",
        "No Atlas memory write occurred.",
        "No Atlas memory admission occurred.",
        "No memory candidate was written.",
        "No federation occurred.",
        "No product release occurred.",
        "No final answer was emitted.",
        "No truth certification occurred.",
        "No accepted evidence was emitted.",
        "No Omega detection occurred.",
        "No consciousness proof occurred.",
        "Human review is required before any future Atlas memory admission prototype.",
        "Run-ATLAS-LOCAL-MEMORY-ADMISSION-READINESS00-Acceptance.ps1",
        "from coherence.atlas.local_memory_admission_readiness import build_atlas_local_memory_admission_readiness",
        "build_atlas_local_memory_admission_readiness",
        "atlas_local_memory_admission_readiness",
        "C:\\UVLM is a local validation example, not product default",
    ):
        assert phrase in page
    boundary_text = "\n".join(claim_boundaries["boundaries"])
    assert "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00 is Atlas memory admission readiness, not Atlas memory admission." in boundary_text
    assert "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00 is not Atlas memory write." in boundary_text
    assert "ATLAS-LOCAL-MEMORY-ADMISSION-READINESS-00 is not memory candidate write." in boundary_text
    assert status["atlas_local_memory_admission_readiness_00_indexed"] is True
    assert status["not_atlas_memory_admission_readiness_memory_write"] is True
    assert status["not_atlas_memory_admission_readiness_atlas_memory_admission"] is True
    assert status["not_atlas_memory_admission_readiness_memory_candidate_write"] is True
    assert status["not_atlas_memory_admission_readiness_product_release"] is True
    assert status["not_atlas_memory_admission_readiness_federation"] is True
    assert status["not_atlas_memory_admission_readiness_truth_certification"] is True



def test_atlas_prototype_proxy_continuity_theorem_pages_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    status = json.loads((out_dir / "status.json").read_text())
    phase_by_id = {entry["phase_id"]: entry for entry in dashboard["accepted_phases"]}
    reproducibility_text = json.dumps(reproducibility)
    boundary_text = "\n".join(claim_boundaries["boundaries"])

    required_builders = (
        "build_runtime_metrics_seed_corpus",
        "build_pmr_local_query_store",
        "build_retrosynthesis_readiness_assessment",
        "build_retrosynthesis_local_prototype",
        "build_atlas_local_memory_admission_readiness",
        "build_atlas_local_memory_admission_prototype",
        "build_local_test_proxy_review_receipt",
        "build_ai_context_performance_continuity",
        "build_theorem_validation_pathway",
    )
    last = -1
    for builder in required_builders:
        position = reproducibility_text.find(builder)
        assert position != -1, builder
        assert position > last, builder
        last = position

    atlas = phase_by_id["ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00"]
    atlas_summary = atlas["dashboard_summary"]
    assert atlas_summary["prototype_status"] == "completed_candidate_admission_review"
    assert atlas_summary["candidate_admission_reviews_not_atlas_memory_admission"] is True
    assert atlas_summary["candidate_admission_reviews_not_memory_write"] is True
    assert atlas_summary["candidate_admission_reviews_not_memory_candidates"] is True
    assert atlas_summary["human_review_required"] is True
    assert atlas_summary["atlas_memory_admission_performed"] is False
    assert atlas_summary["atlas_memory_write_performed"] is False
    assert atlas_summary["atlas_memory_candidate_written"] is False
    assert atlas_summary["product_release_performed"] is False
    for artifact in (
        "atlas_local_memory_admission_prototype_packet.json",
        "atlas_candidate_admission_reviews.jsonl",
        "atlas_admission_eligibility_assessments.jsonl",
        "atlas_local_memory_admission_prototype_receipt.json",
        "atlas_local_memory_admission_prototype_summary.md",
    ):
        assert artifact in artifact_index["phases"]["ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00"]

    proxy = phase_by_id["HUMAN-REVIEW-PROXY-LOCAL-TESTING-00"]["dashboard_summary"]
    assert proxy["review_mode"] == "local_test_proxy_only"
    assert proxy["receipt_status"] == "emitted_local_test_proxy_only"
    assert proxy["human_review_required"] is True
    assert proxy["human_review_satisfied_for_local_test"] is True
    assert proxy["product_human_review_completed"] is False
    assert proxy["atlas_memory_admission_approved"] is False
    assert proxy["memory_write_approved"] is False
    assert proxy["deployment_approved"] is False
    assert proxy["federation_approved"] is False
    assert proxy["final_answer_approved"] is False
    assert proxy["accepted_evidence_approved"] is False
    assert proxy["truth_certification_approved"] is False
    assert "local_test_proxy_review_receipt.json" in artifact_index["phases"]["HUMAN-REVIEW-PROXY-LOCAL-TESTING-00"]

    continuity = phase_by_id["AI-CONTEXT-PERFORMANCE-CONTINUITY-00"]["dashboard_summary"]
    assert continuity["waiting_status"] == "WAITING_FOR_LOCAL_VALIDATION"
    assert continuity["context_pressure_level"] == "high"
    assert continuity["recommended_handoff_now"] is True
    assert continuity["continuity_packet_is_not_memory_write"] is True
    assert continuity["continuity_packet_is_not_truth_certification"] is True
    assert continuity["continuity_packet_is_not_product_release"] is True
    assert continuity["live_chat_is_not_primary_memory_substrate"] is True
    assert continuity["repo_persisted_continuity_is_durable_handoff_substrate"] is True
    for artifact in (
        "ai_context_continuity_packet.json",
        "active_phase_focus_packet.json",
        "validation_status_snapshot.json",
        "assistant_handoff_summary.md",
        "expired_or_external_file_manifest.json",
        "open_patch_queue.json",
        "context_budget_recommendation.md",
    ):
        assert artifact in artifact_index["phases"]["AI-CONTEXT-PERFORMANCE-CONTINUITY-00"]

    theorem = phase_by_id["THEOREM-VALIDATION-PATHWAY-00"]["dashboard_summary"]
    assert theorem["theorem_validation_pathway_status"] == "locally_validated"
    assert theorem["theorem_card_count"] == 1
    assert theorem["theorem_evidence_rows"] == 9
    assert theorem["theorem_counterexamples"] == 9
    assert theorem["theorem_cards_are_validation_artifacts_not_proof"] is True
    assert theorem["theorem_evidence_inputs_are_not_proof"] is True
    assert theorem["truth_certification_occurred"] is False
    assert theorem["product_release_occurred"] is False
    assert theorem["universal_ontology_proof_occurred"] is False
    assert theorem["consciousness_proof_occurred"] is False
    for artifact in (
        "theorem_claim_registry.json",
        "theorem_card_registry.json",
        "theorem_evidence_ledger.json",
        "theorem_counterexample_registry.json",
        "theorem_non_claim_boundary_table.json",
        "theorem_validation_receipt.md",
    ):
        assert artifact in artifact_index["phases"]["THEOREM-VALIDATION-PATHWAY-00"]

    coop = phase_by_id["COOP-ENTROPY-DIVIDEND-00"]["dashboard_summary"]
    assert coop["theorem_id"] == "COOP-ENTROPY-DIVIDEND-00"
    assert coop["proof_grade_current"] == "operational_metric_hypothesis"
    assert coop["proof_grade_target"] == "repeated_empirical_evidence"
    assert coop["proof_grade_claimed"] == "none_yet"
    assert coop["current_status"] == "scaffolded theorem card, not proven theorem"

    page_expectations = {
        "atlas-local-memory-admission-prototype.md": (
            "This is a bounded Atlas local memory admission prototype.",
            "Candidate admission reviews were generated.",
            "Candidate admission reviews are not Atlas memory admission.",
            "Candidate admission reviews are not Atlas memory write.",
            "Candidate admission reviews are not memory candidates.",
            "No Atlas memory write occurred.",
            "No Atlas memory admission occurred.",
            "No memory candidate was written.",
            "No Atlas memory entry was written.",
            "Human review is required before any future Atlas memory admission.",
        ),
        "local-test-proxy-review.md": (
            "Local-test proxy review is for deterministic local development validation only.",
            "Proxy review is not product human review.",
            "Proxy review is not Atlas admission approval.",
            "Proxy review is not memory write approval.",
            "Real human review is required before product use or actual memory admission.",
        ),
        "ai-context-performance-continuity.md": (
            "Live chat is not the primary memory substrate.",
            "Repo-persisted continuity artifacts preserve handoff state.",
            "Known files may exist even when not currently accessible.",
            "Context pressure can trigger recommended handoff.",
            "Continuity packets are not memory write.",
        ),
        "theorem-validation-pathway.md": (
            "This is a theorem validation pathway, not theorem proof.",
            "Theorem cards are not proof.",
            "Evidence ledger entries are evidence inputs, not proof.",
            "semantic_promotion_without_evidence is a failure class.",
        ),
        "coop-entropy-dividend.md": (
            "COOP-ENTROPY-DIVIDEND-00 is not proven.",
            "Current grade is operational_metric_hypothesis.",
            "Claimed grade is none_yet.",
            "Target grade is repeated_empirical_evidence.",
            "Repeated runs and external replication are required.",
            "It is not universal ontology proof.",
        ),
    }
    for page_name, phrases in page_expectations.items():
        text = (docs_dir / page_name).read_text(encoding="utf-8")
        for phrase in phrases:
            assert phrase in text

    for phrase in (
        "ATLAS-LOCAL-MEMORY-ADMISSION-PROTOTYPE-00 generates candidate admission reviews",
        "HUMAN-REVIEW-PROXY-LOCAL-TESTING-00 provides local deterministic development proxy review only",
        "AI-CONTEXT-PERFORMANCE-CONTINUITY-00 records repo-persisted continuity",
        "THEOREM-VALIDATION-PATHWAY-00 creates theorem cards",
        "COOP-ENTROPY-DIVIDEND-00 is scaffolded as an operational metric hypothesis",
    ):
        assert phrase in boundary_text

    assert status["atlas_local_memory_admission_prototype_00_indexed"] is True
    assert status["human_review_proxy_local_testing_00_indexed"] is True
    assert status["ai_context_performance_continuity_00_indexed"] is True
    assert status["theorem_validation_pathway_00_indexed"] is True
    assert status["coop_entropy_dividend_00_indexed"] is True



def test_triadic_llm_ucc_source_materiality_pages_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    status = json.loads((out_dir / "status.json").read_text())
    phase_by_id = {entry["phase_id"]: entry for entry in dashboard["accepted_phases"]}
    reproducibility_text = json.dumps(reproducibility)
    boundary_text = "\n".join(claim_boundaries["boundaries"])

    for builder in (
        "build_triadic_llm_metrics_smoke",
        "build_sophia_ucc_control_review",
        "build_ucc_standards_source_registry",
        "build_ucc_materiality_profile",
        "build_ucc_materiality_override_receipt",
    ):
        assert builder in reproducibility_text

    smoke = phase_by_id["TRIADIC-LLM-METRICS-SMOKE-00"]["dashboard_summary"]
    assert smoke["smoke_status"] == "completed"
    assert smoke["span_linked_claim_count"] == 1
    assert smoke["unsupported_claim_count"] == 1
    assert smoke["raw_model_output_final_answer"] is False
    assert smoke["provider_runtime_performed"] is False
    assert smoke["product_release_performed"] is False
    assert smoke["final_answer_emitted"] is False
    assert smoke["truth_certification_emitted"] is False
    assert smoke["memory_write_performed"] is False
    assert smoke["atlas_memory_admission_performed"] is False
    for artifact in (
        "llm_metrics_smoke_request.json",
        "sonya_model_candidate_packet.json",
        "source_integrity_packet.json",
        "source_span_map.json",
        "claim_classification_packet.json",
        "claim_evidence_map.json",
        "unsupported_claim_report.json",
        "coherence_runtime_metrics_packet.json",
        "coherence_action_functional_packet.json",
        "ai_decision_trace_packet.json",
        "review_receipt.md",
        "llm_metrics_smoke_receipt.json",
    ):
        assert artifact in artifact_index["phases"]["TRIADIC-LLM-METRICS-SMOKE-00"]

    ucc = phase_by_id["UCC-SOPHIA-CONTROL-FORENSICS-00"]["dashboard_summary"]
    assert ucc["ucc_profile_id"] == "local_forensic_controls_fixture_v0"
    assert ucc["control_source_type"] == "synthetic_fixture"
    assert ucc["control_review_status"] == "completed_diagnostic_review"
    assert ucc["satisfied_control_count"] == 5
    assert ucc["failed_control_count"] == 0
    assert ucc["partial_control_count"] == 0
    assert ucc["uncertain_control_count"] == 1
    assert ucc["control_review_is_not_compliance_certification"] is True
    assert ucc["control_review_is_not_professional_attestation"] is True
    assert ucc["control_review_is_not_truth_certification"] is True
    assert ucc["control_review_requires_human_review"] is True
    for artifact in (
        "ucc_control_profile_packet.json",
        "ucc_control_selection_receipt.json",
        "sophia_ucc_control_review_packet.json",
        "ucc_control_evidence_map.json",
        "ucc_control_gap_report.json",
        "ucc_control_non_certification_boundary_table.json",
        "ucc_control_review_summary.md",
    ):
        assert artifact in artifact_index["phases"]["UCC-SOPHIA-CONTROL-FORENSICS-00"]

    source = phase_by_id["UCC-STANDARDS-SOURCE-REGISTRY-AND-MATERIALITY-00"]["dashboard_summary"]
    assert source["source_profile_count"] == 2
    assert source["active_design_fixture_ref"] == "local_forensic_controls_fixture_v0"
    assert source["real_world_reference_example_ref"] == "nist_csf_2_0_reference"
    assert source["nist_reference_is_marketing_example_only"] is True
    assert source["nist_source_text_stored"] is False
    assert source["nist_materiality_profile_applied"] is False
    assert source["active_source_rows_are_synthetic_fixture_and_nist_reference_only"] is True
    assert source["materiality_override_control"] == "uncertainty_visible"
    assert source["prior_materiality"] == "medium"
    assert source["override_materiality"] == "high"
    assert source["override_is_ad_hoc"] is True
    assert source["override_is_not_certification"] is True
    assert source["override_does_not_modify_source_standard"] is True
    for artifact in (
        "ucc_standards_source_registry.json",
        "ucc_materiality_profile.json",
        "ucc_materiality_override_receipt.json",
        "ucc_standards_source_registry_summary.md",
    ):
        assert artifact in artifact_index["phases"]["UCC-STANDARDS-SOURCE-REGISTRY-AND-MATERIALITY-00"]

    repair = phase_by_id["TRIADIC-LLM-SMOKE-PMR-INVENTORY-CONTRACT-REPAIR-REVISION"]["dashboard_summary"]
    assert repair["sonya_model_candidate_packet_pmr_visible"] is True
    assert repair["triadic_llm_smoke_artifacts_inventory_visible"] is True
    assert repair["triadic_llm_smoke_artifacts_parity_visible"] is True
    assert repair["visibility_repair_creates_final_answer_authority"] is False
    assert repair["visibility_repair_creates_provider_runtime"] is False
    assert repair["visibility_repair_creates_product_release"] is False

    page_expectations = {
        "triadic-llm-metrics-smoke.md": (
            "raw model output is not final answer",
            "Sonya model candidate is not final answer",
            "raw model output is final answer",
            "Raw model output is not final answer.",
            "Sonya model candidate packet is candidate-only.",
            "At least one claim is source-span linked.",
            "At least one unsupported claim is visible.",
            "Metrics are diagnostic and non-authoritative.",
            "No provider runtime occurred.",
            "No product release occurred.",
            "No memory write occurred.",
            "No truth certification occurred.",
        ),
        "ucc-sophia-control-forensics.md": (
            "UCC/Sophia control review is diagnostic, not certification.",
            "UCC control review is not legal compliance certification.",
            "UCC control review is not audit opinion.",
            "UCC control review is not professional attestation.",
            "UCC control review is not clinical certification.",
            "UCC control review is not academic endorsement.",
            "UCC control review is not truth certification.",
            "UCC control review is not final answer authority.",
            "UCC control review is not product release.",
            "UCC control review requires human review.",
        ),
        "ucc-standards-source-registry-and-materiality.md": (
            "Synthetic fixture proves universal internal-control design.",
            "NIST CSF 2.0 is included as a reference-only real-world applicability example.",
            "NIST control text is not ingested.",
            "NIST reference is not compliance certification.",
            "No AICPA, COSO, PRISMA, ISO, SOC, PCAOB, clinical, legal, or academic standards are ingested in this patch.",
            "User overrides do not modify the source standard.",
            "User overrides are not professional judgment.",
            "User overrides are not certification.",
            "Human review remains required.",
        ),
        "triadic-llm-smoke-pmr-inventory-contract-repair.md": (
            "sonya_model_candidate_packet.json is PMR-visible.",
            "Triadic LLM smoke artifacts are inventory-visible and parity-visible.",
            "Visibility repair does not create final-answer authority.",
            "Visibility repair does not create provider runtime or product release.",
        ),
    }
    for page_name, phrases in page_expectations.items():
        text = (docs_dir / page_name).read_text(encoding="utf-8")
        for phrase in phrases:
            assert phrase in text

    required_blocked_overclaims = (
        "Atlas memory admission occurred",
        "Atlas memory write occurred",
        "memory candidate was written",
        "raw model output is final answer",
        "UCC review certifies compliance",
        "NIST compliance is certified",
        "NIST controls were ingested",
        "theorem validation proves theorem",
        "COOP-ENTROPY-DIVIDEND-00 is proven",
        "evidence ledger certifies truth",
        "Omega detection",
        "product release",
        "provider runtime",
        "population calibration",
    )
    for phrase in required_blocked_overclaims:
        assert phrase in boundary_text

    for phrase in (
        "TRIADIC-LLM-METRICS-SMOKE-00 demonstrates a local candidate-to-forensic-review smoke",
        "raw model output is not final answer",
        "Sonya model candidate is not final answer",
        "UCC-SOPHIA-CONTROL-FORENSICS-00 applies a synthetic UCC fixture as diagnostic control review",
        "UCC-STANDARDS-SOURCE-REGISTRY-AND-MATERIALITY-00 provides universal source-profile",
        "NIST source text is not ingested.",
        "Visibility repair does not create final-answer authority.",
    ):
        assert phrase in boundary_text

    assert status["triadic_llm_metrics_smoke_00_indexed"] is True
    assert status["ucc_sophia_control_forensics_00_indexed"] is True
    assert status["ucc_standards_source_registry_and_materiality_00_indexed"] is True
    assert status["triadic_llm_smoke_pmr_inventory_contract_repair_revision_indexed"] is True


def test_ai_forensics_dossier_page_and_registry_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    status = json.loads((out_dir / "status.json").read_text())
    phase_by_id = {entry["phase_id"]: entry for entry in dashboard["accepted_phases"]}
    reproducibility_text = json.dumps(reproducibility)
    boundary_text = "\n".join(claim_boundaries["boundaries"])

    assert "AI-FORENSICS-DOSSIER-00" in phase_by_id
    dossier = phase_by_id["AI-FORENSICS-DOSSIER-00"]["dashboard_summary"]
    assert dossier["dossier_status"] == "completed"
    assert dossier["dossier_mode"] == "user_facing_forensic_summary"
    assert dossier["dossier_sections"] == 16
    assert dossier["span_linked_claim_count"] == 1
    assert dossier["unsupported_claim_count"] == 1
    assert dossier["satisfied_control_count"] == 5
    assert dossier["uncertain_control_count"] == 1
    assert dossier["source_profile_count"] == 2
    assert dossier["nist_reference_only"] is True
    assert dossier["nist_source_text_stored"] is False
    assert dossier["human_review_required"] is True
    for flag in (
        "raw_model_output_final_answer",
        "final_answer_emitted",
        "accepted_evidence_emitted",
        "truth_certification_emitted",
        "compliance_certification_emitted",
        "audit_opinion_emitted",
        "professional_attestation_emitted",
        "product_release_performed",
        "provider_runtime_performed",
        "memory_write_performed",
        "atlas_memory_admission_performed",
    ):
        assert dossier[flag] is False

    for artifact in (
        "ai_forensics_dossier_packet.json",
        "ai_forensics_dossier_section_index.json",
        "ai_forensics_dossier.md",
        "ai_forensics_dossier_receipt.json",
    ):
        assert artifact in artifact_index["phases"]["AI-FORENSICS-DOSSIER-00"]

    for builder in (
        "build_triadic_llm_metrics_smoke",
        "build_sophia_ucc_control_review",
        "build_ai_forensics_dossier",
    ):
        assert builder in reproducibility_text

    page = docs_dir / "ai-forensics-dossier.md"
    assert page.exists()
    page_text = page.read_text(encoding="utf-8")
    required_page_phrases = (
        "Triadic Brain turns AI outputs into auditable, source-linked, control-aware forensic dossiers.",
        "The dossier is AI process forensics.",
        "The dossier is not model mind-reading.",
        "The dossier is not hidden chain-of-thought disclosure.",
        "This dossier is not a final answer.",
        "This dossier is not truth certification.",
        "This dossier is not compliance certification.",
        "This dossier is not audit opinion.",
        "This dossier is not professional attestation.",
        "Raw model output is not final answer.",
        "UCC control review is diagnostic, not certification.",
        "NIST CSF 2.0 is reference-only in this run.",
        "NIST control text is not ingested.",
        "Materiality override does not modify the source standard.",
        "Human review remains required.",
        "No provider runtime occurred.",
        "No product release occurred.",
        "No memory write occurred.",
        "No Atlas memory admission occurred.",
        "AI Forensics Dossier is final answer",
        "AI Forensics Dossier certifies truth",
        "AI Forensics Dossier certifies compliance",
        "AI Forensics Dossier is audit opinion",
        "AI Forensics Dossier is professional attestation",
        "AI Forensics Dossier reveals hidden chain of thought",
        "AI Forensics Dossier performs model mind-reading",
    )
    for phrase in required_page_phrases:
        assert phrase in page_text
        assert phrase in boundary_text or phrase in page_text

    assert "AI-FORENSICS-DOSSIER-00 packages a local AI candidate" in boundary_text
    assert status["ai_forensics_dossier_00_indexed"] is True
    assert status["not_ai_forensics_dossier_final_answer"] is True
    assert status["not_ai_forensics_dossier_truth_certification"] is True
    assert status["not_ai_forensics_dossier_compliance_certification"] is True
    assert status["not_ai_forensics_dossier_provider_runtime"] is True


def test_human_review_ux_page_and_registry_are_generated(tmp_path):
    out_dir, docs_dir = run_builder(tmp_path)
    dashboard = json.loads((out_dir / "experiment_suite_dashboard.json").read_text())
    reproducibility = json.loads((out_dir / "reproducibility_index.json").read_text())
    artifact_index = json.loads((out_dir / "artifact_index.json").read_text())
    claim_boundaries = json.loads((out_dir / "claim_boundary_index.json").read_text())
    status = json.loads((out_dir / "status.json").read_text())
    phase_by_id = {entry["phase_id"]: entry for entry in dashboard["accepted_phases"]}
    reproducibility_text = json.dumps(reproducibility)
    boundary_text = "\n".join(claim_boundaries["boundaries"])

    assert "HUMAN-REVIEW-UX-00" in phase_by_id
    review = phase_by_id["HUMAN-REVIEW-UX-00"]["dashboard_summary"]
    assert review["review_status"] == "completed"
    assert review["review_mode"] == "human_review_dossier_ux"
    assert review["review_sections"] == 11
    assert review["allowed_decisions"] == 6
    assert review["default_decision"] == "needs_more_evidence"
    assert review["human_review_occurred"] is True
    assert review["local_test_mode"] is True
    for flag in (
        "product_human_review_completed",
        "final_answer_approved",
        "accepted_evidence_approved",
        "truth_certification_approved",
        "compliance_certification_approved",
        "audit_opinion_approved",
        "professional_attestation_approved",
        "product_release_approved",
        "provider_runtime_approved",
        "memory_write_approved",
        "atlas_memory_admission_approved",
    ):
        assert review[flag] is False
    for decision in (
        "approve_for_local_next_step",
        "request_revision",
        "reject_candidate",
        "defer_review",
        "needs_more_evidence",
        "escalate_to_professional_review",
    ):
        assert decision in review["allowed_decision_values"]

    for artifact in (
        "human_review_ux_packet.json",
        "human_review_action_menu.json",
        "human_review_decision_receipt.json",
        "human_review_summary.md",
    ):
        assert artifact in artifact_index["phases"]["HUMAN-REVIEW-UX-00"]

    for builder in (
        "build_triadic_llm_metrics_smoke",
        "build_sophia_ucc_control_review",
        "build_ai_forensics_dossier",
        "build_human_review_ux_packet",
    ):
        assert builder in reproducibility_text

    page = docs_dir / "human-review-ux.md"
    assert page.exists()
    page_text = page.read_text(encoding="utf-8")
    required_page_phrases = (
        "Human Review UX presents an AI Forensics Dossier for bounded review.",
        "The reviewer inspected an AI Forensics Dossier.",
        "The default local-test decision is needs_more_evidence.",
        "Human review remains bounded by the selected action.",
        "The review decision is not final-answer authority.",
        "The review decision is not truth certification.",
        "The review decision is not compliance certification.",
        "The review decision is not audit opinion.",
        "The review decision is not professional attestation.",
        "The review decision is not product release.",
        "The review decision is not memory write.",
        "The review decision is not Atlas memory admission.",
        "Professional or compliance use requires appropriate qualified review.",
        "Product human review is not completed in local test mode.",
        "Human Review UX creates final answer authority",
        "Human Review UX certifies truth",
        "Human Review UX certifies compliance",
        "Human Review UX is audit opinion",
        "Human Review UX is professional attestation",
        "Human Review UX approves product release",
        "Human Review UX approves provider runtime",
        "Human Review UX approves memory write",
        "Human Review UX approves Atlas memory admission",
        "local test review is product human review",
        "needs_more_evidence is approval",
        "approve_for_local_next_step is final answer approval",
        "escalate_to_professional_review is professional attestation",
    )
    for phrase in required_page_phrases:
        assert phrase in page_text
    assert "HUMAN-REVIEW-UX-00 presents an AI Forensics Dossier" in boundary_text
    assert status["human_review_ux_00_indexed"] is True
    assert status["not_human_review_ux_final_answer_authority"] is True
    assert status["not_human_review_ux_truth_certification"] is True
    assert status["not_human_review_ux_compliance_certification"] is True
